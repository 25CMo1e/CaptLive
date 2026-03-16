#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成行级别的代码来源标注

为每个文件生成详细的行级别映射，标注每一行代码的来源。
"""

import difflib
from pathlib import Path
import urllib.request
from typing import List, Tuple, Dict

PROJECT_ROOT = Path(__file__).parent.parent

GITHUB_RAW_TEMPLATE = {
    "streamcap": "https://raw.githubusercontent.com/ihmily/StreamCap/main/{path}",
    "douyin": "https://raw.githubusercontent.com/saermart/DouyinLiveWebFetcher/main/{path}"
}


def fetch_file(repo_type: str, file_path: str) -> List[str]:
    """从GitHub获取文件"""
    url = GITHUB_RAW_TEMPLATE[repo_type].format(path=file_path)
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8').splitlines()
    except:
        return []


def read_local_file(file_path: Path) -> List[str]:
    """读取本地文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except:
        return []


def generate_line_mapping(local_lines: List[str], remote_lines: List[str]) -> Dict[int, Tuple[int, str]]:
    """
    生成行级别映射
    
    返回: {当前行号: (原始行号, 状态)}
    状态: 'identical', 'modified', 'added', 'deleted'
    """
    mapping = {}
    matcher = difflib.SequenceMatcher(None, remote_lines, local_lines)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # 完全相同的行
            for local_idx, remote_idx in enumerate(range(i1, i2)):
                mapping[j1 + local_idx] = (remote_idx, 'identical')
        elif tag == 'replace':
            # 替换的行
            for local_idx in range(j1, j2):
                if i1 < len(remote_lines):
                    mapping[local_idx] = (i1, 'modified')
        elif tag == 'delete':
            # 删除的行（在当前文件中不存在）
            pass
        elif tag == 'insert':
            # 新增的行
            for local_idx in range(j1, j2):
                mapping[local_idx] = (-1, 'added')
    
    return mapping


def generate_attribution_file(file_path_str: str, mapping_config: Dict) -> str:
    """为单个文件生成行级别标注文档"""
    local_file = PROJECT_ROOT / file_path_str
    
    if not local_file.exists():
        return f"# {file_path_str}\n\n文件不存在\n"
    
    local_lines = read_local_file(local_file)
    remote_lines = fetch_file(mapping_config["source"], mapping_config["original_path"])
    
    if not remote_lines:
        return f"# {file_path_str}\n\n无法获取原始文件\n"
    
    line_mapping = generate_line_mapping([l.rstrip('\n\r') for l in local_lines], remote_lines)
    
    doc_lines = []
    doc_lines.append(f"# {file_path_str} - 行级别代码来源标注\n\n")
    doc_lines.append(f"- **来源项目**: {mapping_config['repo']}\n")
    doc_lines.append(f"- **原始路径**: {mapping_config['original_path']}\n")
    doc_lines.append(f"- **GitHub链接**: {mapping_config['url']}\n\n")
    doc_lines.append("## 行级别映射\n\n")
    doc_lines.append("| 当前行号 | 原始行号 | 状态 | 代码预览 |\n")
    doc_lines.append("|---------|---------|------|----------|\n")
    
    # 只显示前100行和前50行修改/新增的行
    shown_lines = 0
    modified_shown = 0
    
    for local_idx, (remote_idx, status) in sorted(line_mapping.items()):
        if local_idx >= len(local_lines):
            continue
        
        code_preview = local_lines[local_idx].strip()[:50]
        if len(code_preview) > 50:
            code_preview += "..."
        
        status_emoji = {
            'identical': '✓',
            'modified': '~',
            'added': '+',
            'deleted': '-'
        }.get(status, '?')
        
        # 限制输出
        if status == 'identical' and shown_lines < 100:
            doc_lines.append(f"| {local_idx+1} | {remote_idx+1 if remote_idx >= 0 else '-'} | {status_emoji} {status} | `{code_preview}` |\n")
            shown_lines += 1
        elif status in ['modified', 'added'] and modified_shown < 50:
            doc_lines.append(f"| {local_idx+1} | {remote_idx+1 if remote_idx >= 0 else '-'} | {status_emoji} {status} | `{code_preview}` |\n")
            modified_shown += 1
    
    doc_lines.append(f"\n\n**总计**: {len(local_lines)} 行\n")
    doc_lines.append(f"- 完全相同: {sum(1 for s in line_mapping.values() if s[1] == 'identical')} 行\n")
    doc_lines.append(f"- 已修改: {sum(1 for s in line_mapping.values() if s[1] == 'modified')} 行\n")
    doc_lines.append(f"- 新增: {sum(1 for s in line_mapping.values() if s[1] == 'added')} 行\n")
    
    return "".join(doc_lines)


def main():
    """主函数"""
    FILE_MAPPINGS = {
        "app/douyin_fetcher/liveMan.py": {
            "source": "douyin",
            "original_path": "liveMan.py",
            "repo": "DouyinLiveWebFetcher",
            "url": "https://github.com/saermart/DouyinLiveWebFetcher/blob/main/liveMan.py"
        },
    }
    
    print("生成行级别代码来源标注...")
    
    for file_path, mapping in FILE_MAPPINGS.items():
        print(f"处理: {file_path}")
        attribution = generate_attribution_file(file_path, mapping)
        
        output_file = PROJECT_ROOT / f"LINE_ATTRIBUTION_{file_path.replace('/', '_').replace('.', '_')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(attribution)
        
        print(f"  已生成: {output_file}")
    
    print("\n完成!")


if __name__ == "__main__":
    main()
