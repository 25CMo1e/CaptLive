#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置Git历史记录以显示代码原作者

这个脚本会帮助设置Git仓库，使得在GitHub上可以看到代码的原始作者信息。
"""

import subprocess
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# 原作者信息
AUTHORS = {
    "streamcap": {
        "name": "Hmily",
        "email": "ihmily@example.com",  # 请替换为实际邮箱或使用GitHub noreply邮箱
        "github": "ihmily"
    },
    "douyin": {
        "name": "saermart",
        "email": "kukushka@126.com",
        "github": "saermart"
    }
}

# 文件映射到原作者
FILE_AUTHOR_MAP = {
    # StreamCap 文件
    "app/app_manager.py": "streamcap",
    "app/core/": "streamcap",
    "app/ui/": "streamcap",
    "main.py": "streamcap",
    
    # DouyinLiveWebFetcher 文件
    "app/douyin_fetcher/liveMan.py": "douyin",
    "app/douyin_fetcher/sign.js": "douyin",
    "app/douyin_fetcher/protobuf/": "douyin",
    
    # 合并后的文件（可以标注为当前用户）
    "app/douyin_fetcher/streamcap_adapter.py": None,  # 新文件，不指定原作者
}


def run_git_command(cmd, check=True):
    """运行git命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if check and result.returncode != 0:
            print(f"错误: {cmd}")
            print(result.stderr)
        return result
    except Exception as e:
        print(f"执行命令失败: {e}")
        return None


def check_git_repo():
    """检查是否是Git仓库"""
    result = run_git_command("git rev-parse --git-dir", check=False)
    return result and result.returncode == 0


def init_git_repo():
    """初始化Git仓库"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if not check_git_repo():
        print("初始化Git仓库...")
        run_git_command("git init")
        print("[OK] Git仓库已初始化")
    else:
        print("[OK] Git仓库已存在")


def create_mailmap():
    """创建.mailmap文件"""
    mailmap_content = """# .mailmap 文件用于统一显示作者信息
# 格式: 正确显示名称 <正确邮箱> <提交时使用的名称> <提交时使用的邮箱>

# StreamCap 项目作者
Hmily <ihmily@example.com> Hmily <ihmily@example.com>
ihmily <ihmily@example.com> Hmily <ihmily@example.com>

# DouyinLiveWebFetcher 项目作者
saermart <kukushka@126.com> saermart <kukushka@126.com>
bubu <kukushka@126.com> saermart <kukushka@126.com>
"""
    
    mailmap_file = PROJECT_ROOT / ".mailmap"
    with open(mailmap_file, 'w', encoding='utf-8') as f:
        f.write(mailmap_content)
    print("[OK] .mailmap 文件已创建")


def setup_git_config():
    """设置Git配置"""
    print("\n请设置Git用户信息:")
    print("1. 使用以下命令设置全局配置:")
    print("   git config --global user.name 'Your Name'")
    print("   git config --global user.email 'your.email@example.com'")
    print("\n2. 或者仅为当前仓库设置:")
    print("   git config user.name 'Your Name'")
    print("   git config user.email 'your.email@example.com'")


def create_initial_commit_with_attribution():
    """创建初始提交，标注代码来源"""
    print("\n创建初始提交...")
    print("注意: 为了在GitHub上显示原作者信息，建议使用以下方法:")
    print("\n方法1: 使用 --author 参数提交特定文件")
    print("  git add app/douyin_fetcher/liveMan.py")
    print(f"  git commit --author='{AUTHORS['douyin']['name']} <{AUTHORS['douyin']['email']}>' -m 'Add liveMan.py from DouyinLiveWebFetcher'")
    print("\n方法2: 使用 git filter-branch 重写历史（如果已有提交）")
    print("  参考: https://git-scm.com/docs/git-filter-branch")


def create_attribution_guide():
    """创建Git属性标注指南"""
    guide = """# Git代码作者标注指南

## 方法1: 在提交时指定作者（推荐）

### 提交DouyinLiveWebFetcher的文件
```bash
git add app/douyin_fetcher/liveMan.py
git commit --author="saermart <kukushka@126.com>" -m "Add liveMan.py from DouyinLiveWebFetcher"
```

### 提交StreamCap的文件
```bash
git add app/app_manager.py
git commit --author="Hmily <ihmily@example.com>" -m "Add app_manager.py from StreamCap"
```

### 提交合并后的新文件
```bash
git add app/douyin_fetcher/streamcap_adapter.py
git commit -m "Add streamcap_adapter.py (merged code)"
```

## 方法2: 使用 .mailmap 文件统一显示

已创建 .mailmap 文件，Git会自动使用它来统一显示作者信息。

查看贡献者统计:
```bash
git shortlog -sn
```

## 方法3: 重写已有提交的历史（如果已有提交）

如果仓库已有提交，可以使用 git filter-branch 或 git filter-repo 重写历史:

```bash
# 安装 git-filter-repo (推荐)
pip install git-filter-repo

# 重写特定文件的作者
git filter-repo --path app/douyin_fetcher/liveMan.py \\
    --commit-callback '
if b"liveMan.py" in commit.file_changes:
    commit.author_name = b"saermart"
    commit.author_email = b"kukushka@126.com"
'
```

## 方法4: 使用GitHub的CODEOWNERS文件

已创建 .github/CODEOWNERS 文件，GitHub会在PR中自动@代码所有者。

## 在GitHub上查看作者信息

1. **查看文件历史**: 点击文件，然后点击"History"
2. **查看每行作者**: 点击文件，然后点击"Blame"
3. **查看贡献者**: 在仓库页面点击"Contributors"

## 注意事项

- 使用 --author 参数时，邮箱地址应该是GitHub账户关联的邮箱
- 如果原作者没有GitHub账户，可以使用格式: "Name <name@users.noreply.github.com>"
- .mailmap 文件可以帮助统一显示不同的作者名称变体
"""
    
    guide_file = PROJECT_ROOT / "GIT_ATTRIBUTION_GUIDE.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    print(f"[OK] Git标注指南已创建: {guide_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("Git代码作者标注设置工具")
    print("=" * 60)
    print()
    
    # 初始化Git仓库
    init_git_repo()
    
    # 创建.mailmap文件
    create_mailmap()
    
    # 创建CODEOWNERS文件（已在之前创建）
    print("[OK] CODEOWNERS 文件已存在")
    
    # 创建指南
    create_attribution_guide()
    
    # 设置说明
    setup_git_config()
    
    # 提交说明
    create_initial_commit_with_attribution()
    
    print("\n" + "=" * 60)
    print("设置完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 设置Git用户信息（见上方说明）")
    print("2. 添加文件: git add .")
    print("3. 使用 --author 参数提交文件（见 GIT_ATTRIBUTION_GUIDE.md）")
    print("4. 推送到GitHub: git push")


if __name__ == "__main__":
    main()
