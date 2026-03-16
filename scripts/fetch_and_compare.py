#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从GitHub获取原始代码并对比

直接从GitHub获取原始文件内容，无需本地克隆仓库。
"""

import os
import sys
import difflib
from pathlib import Path
import urllib.request
import urllib.parse
import json

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# GitHub Raw URL 模板
GITHUB_RAW_TEMPLATE = {
    "streamcap": "https://raw.githubusercontent.com/ihmily/StreamCap/main/{path}",
    "douyin": "https://raw.githubusercontent.com/saermart/DouyinLiveWebFetcher/main/{path}",
    "dycast": "https://raw.githubusercontent.com/skmcj/dycast/main/{path}"
}

# 文件映射 - 可以扩展更多文件
FILE_MAPPINGS = {
    # DouyinLiveWebFetcher 文件
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
    
    # StreamCap 文件（示例，可根据需要添加更多）
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
    
    # 注意：dycast 是 TypeScript/Vue 项目，与当前 Python 项目不同
    # 如果项目中确实使用了 dycast 的代码，请添加相应映射
}


def fetch_github_file(repo_type: str, file_path: str) -> tuple[list[str], bool]:
    """从GitHub获取文件内容"""
    url = GITHUB_RAW_TEMPLATE[repo_type].format(path=file_path)
    
    try:
        print(f"正在获取: {url}")
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read().decode('utf-8')
            return content.splitlines(keepends=True), True
    except Exception as e:
        print(f"获取失败: {e}")
        return [], False


def read_local_file(file_path: Path) -> list[str]:
    """读取本地文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"读取本地文件失败: {e}")
        return []


def compare_files(local_lines: list[str], remote_lines: list[str], local_path: str, remote_path: str) -> dict:
    """对比两个文件"""
    if not local_lines:
        return {"status": "local_empty", "similarity": 0.0}
    
    if not remote_lines:
        return {"status": "remote_empty", "similarity": 0.0}
    
    # 计算相似度
    similarity = difflib.SequenceMatcher(None, local_lines, remote_lines).ratio()
    
    # 生成差异
    diff = list(difflib.unified_diff(
        remote_lines,
        local_lines,
        fromfile=f"原始: {remote_path}",
        tofile=f"当前: {local_path}",
        lineterm=''
    ))
    
    # 判断修改程度
    if similarity == 1.0:
        status = "identical"
    elif similarity > 0.95:
        status = "minor_changes"
    elif similarity > 0.7:
        status = "major_changes"
    else:
        status = "heavily_modified"
    
    return {
        "status": status,
        "similarity": similarity,
        "diff": diff,
        "local_lines": len(local_lines),
        "remote_lines": len(remote_lines)
    }


def analyze_file(file_path_str: str, mapping: dict) -> dict:
    """分析单个文件"""
    local_file = PROJECT_ROOT / file_path_str
    
    if not local_file.exists():
        return {
            "file": file_path_str,
            "error": "本地文件不存在"
        }
    
    local_lines = read_local_file(local_file)
    remote_lines, success = fetch_github_file(mapping["source"], mapping["original_path"])
    
    if not success:
        return {
            "file": file_path_str,
            "error": "无法获取远程文件"
        }
    
    comparison = compare_files(
        local_lines,
        remote_lines,
        file_path_str,
        mapping["original_path"]
    )
    
    return {
        "file": file_path_str,
        "mapping": mapping,
        "comparison": comparison
    }


def generate_report() -> str:
    """生成对比报告"""
    report_lines = []
    report_lines.append("# 代码来源精准对比报告\n\n")
    report_lines.append("本报告通过直接对比GitHub上的原始代码生成。\n\n")
    report_lines.append("## 对比结果\n\n")
    
    for file_path_str, mapping in FILE_MAPPINGS.items():
        report_lines.append(f"### {file_path_str}\n\n")
        report_lines.append(f"- **来源项目**: {mapping['repo']}\n")
        report_lines.append(f"- **原始路径**: {mapping['original_path']}\n")
        report_lines.append(f"- **GitHub链接**: {mapping['url']}\n\n")
        
        print(f"\n正在分析: {file_path_str}")
        result = analyze_file(file_path_str, mapping)
        
        if "error" in result:
            report_lines.append(f"**错误**: {result['error']}\n\n")
        else:
            comp = result["comparison"]
            similarity_percent = comp["similarity"] * 100
            
            report_lines.append(f"**相似度**: {similarity_percent:.1f}%\n")
            report_lines.append(f"**状态**: {comp['status']}\n")
            report_lines.append(f"**行数**: 原始 {comp['remote_lines']} 行 -> 当前 {comp['local_lines']} 行\n\n")
            
            if comp["status"] != "identical" and comp.get("diff"):
                report_lines.append("**差异预览** (前50行):\n```diff\n")
                report_lines.extend(comp["diff"][:50])
                report_lines.append("\n```\n\n")
        
        report_lines.append("---\n\n")
    
    return "".join(report_lines)


def main():
    """主函数"""
    print("=" * 60)
    print("代码来源对比工具 (从GitHub获取)")
    print("=" * 60)
    
    report = generate_report()
    
    report_file = PROJECT_ROOT / "CODE_COMPARISON_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[OK] 报告已生成: {report_file}")
    print("\n提示: 查看 CODE_COMPARISON_REPORT.md 了解详细的代码对比结果")


if __name__ == "__main__":
    main()
