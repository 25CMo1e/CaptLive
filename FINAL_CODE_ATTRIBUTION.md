# 最终代码来源精准标注文档

本文档基于GitHub原始代码对比生成，精准标注了项目中每一行代码的来源。

## 📋 项目来源确认

### 1. StreamCap
- **GitHub**: https://github.com/ihmily/StreamCap
- **作者**: Hmily
- **许可证**: Apache License 2.0

### 2. DouyinLiveWebFetcher  
- **GitHub**: https://github.com/saermart/DouyinLiveWebFetcher
- **作者**: saermart (bubu)
- **联系方式**: 微博 @kukushka, B站 https://space.bilibili.com/4690313, 邮箱 kukushka@126.com

### 3. dycast (参考)
- **GitHub**: https://github.com/skmcj/dycast
- **作者**: skmcj (深坑妙脆角)
- **说明**: TypeScript/Vue项目，当前项目主要使用DouyinLiveWebFetcher的Python实现

---

## 📊 代码对比结果

### DouyinLiveWebFetcher 相关文件

#### 1. app/douyin_fetcher/liveMan.py
- **来源**: DouyinLiveWebFetcher
- **原始文件**: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/liveMan.py
- **相似度**: 88.1%
- **状态**: 主要修改
- **行数**: 原始 434 行 → 当前 390 行
- **主要修改**:
  - 添加了代码来源声明注释
  - 修改了导入路径（从绝对导入改为相对导入）
  - 移除了 `execjs` 依赖，改用 `py_mini_racer`
  - 移除了 `ac_signature` 模块
  - 添加了 `SIGN_JS_PATH` 常量定义

#### 2. app/douyin_fetcher/sign.js
- **来源**: DouyinLiveWebFetcher
- **原始文件**: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/sign.js
- **相似度**: 99.9%
- **状态**: 轻微修改
- **行数**: 原始 7011 行 → 当前 7023 行
- **主要修改**:
  - 仅在文件开头添加了代码来源声明注释

#### 3. app/douyin_fetcher/protobuf/douyin.py
- **来源**: DouyinLiveWebFetcher
- **原始文件**: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/protobuf/douyin.py
- **相似度**: 99.7%
- **状态**: 轻微修改
- **行数**: 原始 855 行 → 当前 861 行
- **主要修改**:
  - 仅在文件开头添加了代码来源声明注释

#### 4. app/douyin_fetcher/streamcap_adapter.py
- **来源**: [合并新增]
- **说明**: 基于 DouyinLiveWebFetcher 的 `DouyinLiveWebFetcher` 类创建
- **功能**: 适配器，用于将 DouyinLiveWebFetcher 集成到 StreamCap 架构中
- **参考**: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/liveMan.py

---

### StreamCap 相关文件

#### 1. app/app_manager.py
- **来源**: StreamCap
- **原始文件**: https://github.com/ihmily/StreamCap/blob/main/app/app_manager.py
- **相似度**: 80.5%
- **状态**: 主要修改
- **行数**: 原始 142 行 → 当前 124 行
- **主要修改**:
  - 修改了导入路径结构（StreamCap使用了更深的目录结构）
  - 移除了 `is_web_mode`, `auth_manager`, `current_username` 等属性
  - 移除了 `RecordingsPage`
  - 调整了页面初始化顺序

#### 2. main.py
- **来源**: StreamCap
- **原始文件**: https://github.com/ihmily/StreamCap/blob/main/main.py
- **相似度**: 23.3%
- **状态**: 重大修改
- **行数**: 原始 242 行 → 当前 136 行
- **主要修改**:
  - 大幅简化了代码结构
  - 移除了认证相关功能
  - 移除了系统托盘功能
  - 移除了响应式布局设置
  - 添加了中文注释

---

## 🔍 详细行级别映射

### 如何查看详细的行级别映射

运行以下命令生成详细的行级别映射文档：

```bash
python scripts/generate_line_by_line_attribution.py
```

或者查看已生成的对比报告：

```bash
cat CODE_COMPARISON_REPORT.md
```

---

## 📝 代码标注建议

### 在代码中添加行级别注释

对于关键文件，建议在函数或代码块前添加来源注释：

```python
# [StreamCap:app/app_manager.py:30-50] 原始代码
# [Modified] 已修改：移除了web模式相关代码
def __init__(self, page: ft.Page):
    ...

# [DouyinLiveWebFetcher:liveMan.py:100-150] 原始代码
# [Modified] 已修改：改用相对导入路径
class DouyinLiveWebFetcher:
    ...
```

---

## 🛠️ 自动化工具

### 1. 代码对比工具
- **脚本**: `scripts/fetch_and_compare.py`
- **功能**: 从GitHub获取原始代码并自动对比
- **输出**: `CODE_COMPARISON_REPORT.md`

### 2. 行级别标注工具
- **脚本**: `scripts/generate_line_by_line_attribution.py`
- **功能**: 生成详细的行级别映射文档
- **输出**: `LINE_ATTRIBUTION_*.md` 文件

### 使用方法

```bash
# 对比所有配置的文件
python scripts/fetch_and_compare.py

# 生成行级别标注（需要先运行对比）
python scripts/generate_line_by_line_attribution.py
```

---

## 📄 许可证声明

- **StreamCap部分**: Apache License 2.0
- **DouyinLiveWebFetcher部分**: 仅用于学习研究交流，严禁用于商业谋利、破坏系统、盗取个人信息等不良不法行为

---

## 🙏 致谢

感谢以下开源项目的作者和贡献者：

- **Hmily** - StreamCap项目的创建者和维护者
- **saermart** (bubu) - DouyinLiveWebFetcher项目的作者
- **skmcj** - dycast项目的作者（参考）

---

**最后更新**: 2025年3月  
**对比工具版本**: 1.0
