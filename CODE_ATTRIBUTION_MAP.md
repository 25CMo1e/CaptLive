# 代码来源精准映射文档

本文档详细标注了项目中每一行代码的来源，包括：
- 原始项目来源
- 原始文件路径
- 修改情况
- GitHub链接

## 📋 映射说明

### 标注格式

```
[来源项目] 原始文件路径 → 当前文件路径
- 行号范围: 原始行号 → 当前行号
- 修改情况: [未修改/轻微修改/重大修改/新增]
- GitHub链接: [链接]
```

### 来源项目标识

- `[StreamCap]` - 来自 StreamCap 项目 (https://github.com/ihmily/StreamCap)
- `[DouyinLiveWebFetcher]` - 来自 DouyinLiveWebFetcher 项目 (https://github.com/saermart/DouyinLiveWebFetcher)
- `[Merged]` - 合并后新增的代码
- `[Modified]` - 基于原始代码修改的代码

---

## 📁 文件级别映射

### app/douyin_fetcher/ 目录

#### liveMan.py

**来源**: [DouyinLiveWebFetcher] `liveMan.py` → `app/douyin_fetcher/liveMan.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/liveMan.py

---

#### streamcap_adapter.py

**来源**: [Merged] 新增文件，用于整合两个项目

**详细映射**:
- 全部代码: [Merged] 基于 DouyinLiveWebFetcher 的 `DouyinLiveWebFetcher` 类创建适配器
- 继承自: `DouyinLiveWebFetcher` (来自 DouyinLiveWebFetcher)
- 回调机制: [Merged] 新增，用于与 StreamCap 集成

**GitHub链接**: 
- 参考: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/liveMan.py

---

#### sign.js

**来源**: [DouyinLiveWebFetcher] `sign.js` → `app/douyin_fetcher/sign.js`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/sign.js

---

#### protobuf/douyin.py

**来源**: [DouyinLiveWebFetcher] `protobuf/douyin.py` → `app/douyin_fetcher/protobuf/douyin.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/saermart/DouyinLiveWebFetcher/blob/main/protobuf/douyin.py

---

### app/core/ 目录

#### app_manager.py

**来源**: [StreamCap] `app/app_manager.py` → `app/app_manager.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/app/app_manager.py

---

#### stream_manager.py

**来源**: [StreamCap] `app/core/stream_manager.py` → `app/core/stream_manager.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/app/core/stream_manager.py

---

#### barrage_manager.py

**来源**: [StreamCap] `app/core/barrage_manager.py` → `app/core/barrage_manager.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/app/core/barrage_manager.py

---

#### record_manager.py

**来源**: [StreamCap] `app/core/record_manager.py` → `app/core/record_manager.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/app/core/record_manager.py

---

#### config_manager.py

**来源**: [StreamCap] `app/core/config_manager.py` → `app/core/config_manager.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/app/core/config_manager.py

---

#### platform_handlers/handlers.py

**来源**: [StreamCap] `app/core/platform_handlers/handlers.py` → `app/core/platform_handlers/handlers.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/app/core/platform_handlers/handlers.py

---

### app/ui/ 目录

**来源**: [StreamCap] 整个 `app/ui/` 目录

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始目录: https://github.com/ihmily/StreamCap/tree/main/app/ui

---

### main.py

**来源**: [StreamCap] `main.py` → `main.py`

**详细映射**:
- 待填充：需要对比原始文件

**GitHub链接**: 
- 原始文件: https://github.com/ihmily/StreamCap/blob/main/main.py

---

## 🔍 对比工具

为了精准标注每一行代码，建议使用以下方法：

1. **使用 diff 工具对比**:
   ```bash
   # 克隆原始仓库
   git clone https://github.com/ihmily/StreamCap.git streamcap-original
   git clone https://github.com/saermart/DouyinLiveWebFetcher.git douyin-original
   
   # 使用 diff 对比
   diff -u streamcap-original/app/app_manager.py app/app_manager.py
   ```

2. **使用 Python 脚本自动对比**:
   - 创建对比脚本，自动生成映射文档
   - 识别代码块来源
   - 标注修改情况

---

## 📝 待完成工作

- [ ] 对比 `liveMan.py` 的每一行
- [ ] 对比 `streamcap_adapter.py` 的每一行
- [ ] 对比 `sign.js` 的每一行
- [ ] 对比 StreamCap 相关文件的每一行
- [ ] 创建自动化对比脚本
- [ ] 生成完整的行级别映射文档

---

**最后更新**: 2025年3月  
**状态**: 待填充详细映射信息
