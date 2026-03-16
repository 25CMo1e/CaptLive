# Git代码作者标注指南

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
git filter-repo --path app/douyin_fetcher/liveMan.py \
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
