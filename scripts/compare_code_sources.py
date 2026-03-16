#!/usr/bin/env python3
"""
代码来源对比工具

用于对比当前项目代码与原始GitHub仓库的代码，生成详细的代码来源映射文档。

使用方法:
    python scripts/compare_code_sources.py

需要先克隆原始仓库:
    git clone https://github.com/ihmily/StreamCap.git ../streamcap-original
    git clone https://github.com/saermart/DouyinLiveWebFetcher.git ../douyin-original
"""

import os
import difflib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 原始仓库路径（需要用户手动克隆）
STREAMCAP_ORIGINAL = PROJECT_ROOT.parent / "streamcap-original"
DOUYIN_ORIGINAL = PROJECT_ROOT.parent / "douyin-original"

# 文件映射配置
FILE_MAPPINGS = {
    # DouyinLiveWebFetcher 文件映射
    "app/douyin_fetcher/liveMan.py": {
        "source": "douyin",
        "original_path": "liveMan.py",
        "repo": "DouyinLiveWebFetcher",
        "url": "https://github.com/saermart/DouyinLiveWebFetcher/blob/main/liveMan.py"
    },
    "app/douyin_fetcher/sign.js": {
        "source": "douyin",
        "original_path": "sign.js",
        "repo": "DouyinLiveWebFetcher",
        "url": "https://github.com/saermart/DouyinLiveWebFetcher/blob/main/sign.js"
    },
    "app/douyin_fetcher/protobuf/douyin.py": {
        "source": "douyin",
        "original_path": "protobuf/douyin.py",
        "repo": "DouyinLiveWebFetcher",
        "url": "https://github.com/saermart/DouyinLiveWebFetcher/blob/main/protobuf/douyin.py"
    },
    "app/douyin_fetcher/streamcap_adapter.py": {
        "source": "merged",
        "original_path": None,
        "repo": "Merged",
        "url": None,
        "note": "基于 DouyinLiveWebFetcher 的 liveMan.py 创建"
    },
    
    # StreamCap 文件映射（示例，需要补充完整）
    "app/app_manager.py": {
        "source": "streamcap",
        "original_path": "app/app_manager.py",
        "repo": "StreamCap",
        "url": "https://github.com/ihmily/StreamCap/blob/main/app/app_manager.py"
    },
    "app/core/stream_manager.py": {
        "source": "streamcap",
        "original_path": "app/core/stream_manager.py",
        "repo": "StreamCap",
        "url": "https://github.com/ihmily/StreamCap/blob/main/app/core/stream_manager.py"
    },
    "app/core/barrage_manager.py": {
        "source": "streamcap",
        "original_path": "app/core/barrage_manager.py",
        "repo": "StreamCap",
        "url": "https://github.com/ihmily/StreamCap/blob/main/app/core/barrage_manager.py"
    },
    "main.py": {
        "source": "streamcap",
        "original_path": "main.py",
        "repo": "StreamCap",
        "url": "https://github.com/ihmily/StreamCap/blob/main/main.py"
    },
}


def read_file_lines(file_path: Path) -> List[str]:
    """读取文件的所有行"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"错误: 无法读取文件 {file_path}: {e}")
        return []


def compare_files(current_file: Path, original_file: Optional[Path]) -> Dict:
    """对比两个文件，返回差异信息"""
    if original_file is None or not original_file.exists():
        return {
            "status": "original_not_found",
            "similarity": 0.0,
            "diff": [],
            "note": "原始文件不存在，可能是新增文件"
        }
    
    current_lines = read_file_lines(current_file)
    original_lines = read_file_lines(original_file)
    
    if not current_lines:
        return {
            "status": "current_file_empty",
            "similarity": 0.0,
            "diff": []
        }
    
    if not original_lines:
        return {
            "status": "original_file_empty",
            "similarity": 0.0,
            "diff": []
        }
    
    # 计算相似度
    similarity = difflib.SequenceMatcher(None, current_lines, original_lines).ratio()
    
    # 生成差异
    diff = list(difflib.unified_diff(
        original_lines,
        current_lines,
        fromfile=str(original_file),
        tofile=str(current_file),
        lineterm=''
    ))
    
    # 判断修改程度
    if similarity == 1.0:
        status = "identical"
    elif similarity > 0.9:
        status = "minor_changes"
    elif similarity > 0.5:
        status = "major_changes"
    else:
        status = "heavily_modified"
    
    return {
        "status": status,
        "similarity": similarity,
        "diff": diff[:100],  # 只保留前100行差异
        "current_lines": len(current_lines),
        "original_lines": len(original_lines)
    }


def get_original_file_path(mapping: Dict, file_path: Path) -> Optional[Path]:
    """获取原始文件路径"""
    if mapping["source"] == "douyin":
        return DOUYIN_ORIGINAL / mapping["original_path"]
    elif mapping["source"] == "streamcap":
        return STREAMCAP_ORIGINAL / mapping["original_path"]
    else:
        return None


def analyze_file(file_path: Path, mapping: Dict) -> Dict:
    """分析单个文件的来源"""
    original_file = get_original_file_path(mapping, file_path)
    
    comparison = compare_files(file_path, original_file)
    
    return {
        "file": str(file_path.relative_to(PROJECT_ROOT)),
        "mapping": mapping,
        "comparison": comparison,
        "original_file": str(original_file) if original_file else None
    }


def generate_attribution_report() -> str:
    """生成代码来源报告"""
    report_lines = []
    report_lines.append("# 代码来源对比报告\n")
    report_lines.append(f"生成时间: {Path(__file__).stat().st_mtime}\n\n")
    
    report_lines.append("## 📋 对比结果\n\n")
    
    for file_path_str, mapping in FILE_MAPPINGS.items():
        file_path = PROJECT_ROOT / file_path_str
        
        if not file_path.exists():
            report_lines.append(f"### [ERROR] {file_path_str}\n")
            report_lines.append("文件不存在\n\n")
            continue
        
        report_lines.append(f"### {file_path_str}\n\n")
        report_lines.append(f"- **来源项目**: {mapping['repo']}\n")
        
        if mapping.get("original_path"):
            report_lines.append(f"- **原始路径**: {mapping['original_path']}\n")
            report_lines.append(f"- **GitHub链接**: {mapping['url']}\n")
        
        if mapping.get("note"):
            report_lines.append(f"- **备注**: {mapping['note']}\n")
        
        report_lines.append("\n")
        
        # 执行对比
        analysis = analyze_file(file_path, mapping)
        comparison = analysis["comparison"]
        
        if comparison["status"] == "original_not_found":
            report_lines.append("[WARNING] **原始文件未找到** - 请确保已克隆原始仓库\n\n")
        elif comparison["status"] == "identical":
            report_lines.append("[OK] **完全一致** - 代码未修改\n\n")
        else:
            similarity_percent = comparison["similarity"] * 100
            report_lines.append(f"[INFO] **相似度**: {similarity_percent:.1f}%\n")
            report_lines.append(f"[INFO] **状态**: {comparison['status']}\n")
            report_lines.append(f"[INFO] **行数**: 原始 {comparison.get('original_lines', 0)} 行 -> 当前 {comparison.get('current_lines', 0)} 行\n\n")
            
            if comparison.get("diff"):
                report_lines.append("**主要差异** (前20行):\n```diff\n")
                report_lines.extend(comparison["diff"][:20])
                report_lines.append("\n```\n\n")
        
        report_lines.append("---\n\n")
    
    return "".join(report_lines)


def main():
    """主函数"""
    import sys
    import io
    # 设置UTF-8编码输出
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 60)
    print("代码来源对比工具")
    print("=" * 60)
    print()
    
    # 检查原始仓库是否存在
    if not STREAMCAP_ORIGINAL.exists():
        print(f"[WARNING] StreamCap 原始仓库未找到: {STREAMCAP_ORIGINAL}")
        print("   请运行: git clone https://github.com/ihmily/StreamCap.git ../streamcap-original")
        print()
    
    if not DOUYIN_ORIGINAL.exists():
        print(f"[WARNING] DouyinLiveWebFetcher 原始仓库未找到: {DOUYIN_ORIGINAL}")
        print("   请运行: git clone https://github.com/saermart/DouyinLiveWebFetcher.git ../douyin-original")
        print()
    
    # 生成报告
    print("正在生成对比报告...")
    report = generate_attribution_report()
    
    # 保存报告
    report_file = PROJECT_ROOT / "CODE_COMPARISON_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"[OK] 报告已生成: {report_file}")
    print()
    print("提示: 查看 CODE_COMPARISON_REPORT.md 了解详细的代码对比结果")


if __name__ == "__main__":
    main()
