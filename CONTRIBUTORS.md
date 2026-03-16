# 贡献者与代码来源

## 📝 项目说明

本项目由两个开源项目合并并修改而来。以下列出了所有代码来源和贡献者信息。

## 🔗 原始项目

### 1. StreamCap

**项目名称**: StreamCap  
**GitHub仓库**: [ihmily/StreamCap](https://github.com/ihmily/StreamCap)  
**作者**: Hmily  
**许可证**: Apache License 2.0

**贡献的代码**:
- 项目主体架构和UI框架
- 直播录制核心功能
- 多平台支持适配器
- 配置管理和应用管理模块
- UI组件和页面视图

---

### 2. DouyinLiveWebFetcher

**项目名称**: DouyinLiveWebFetcher (抖音网页版弹幕数据抓取)  
**GitHub仓库**: [saermart/DouyinLiveWebFetcher](https://github.com/saermart/DouyinLiveWebFetcher)  
**原作者**: saermart (bubu)

**联系方式**:
- 微博: [@kukushka](https://weibo.com/u/7751075499)
- B站: [B站主页](https://space.bilibili.com/4690313)
- 邮箱: kukushka@126.com

**贡献的代码**:
- 抖音弹幕抓取核心逻辑 (`app/douyin_fetcher/liveMan.py`)
- WebSocket连接和消息处理
- Protobuf消息解析 (`app/douyin_fetcher/protobuf/`)
- 签名算法实现 (`app/douyin_fetcher/sign.js`)

**原始声明**:
> 本代码库所有代码均只用于学习研究交流，严禁用于包括但不限于商业谋利、破坏系统、盗取个人信息等不良不法行为，违反此声明使用所产生的一切后果均由违反声明使用者承担。

---

## 🔄 项目整合者

本项目在合并两个开源项目的基础上进行了以下工作：

1. **架构整合**: 将DouyinLiveWebFetcher的弹幕抓取功能整合到StreamCap的架构中
2. **适配器开发**: 创建了`streamcap_adapter.py`作为适配器，将DouyinLiveWebFetcher集成到StreamCap的平台处理器体系
3. **功能增强**: 在原有功能基础上添加了新的特性和优化
4. **代码重构**: 对部分代码进行了重构以提高可维护性

---

## 📄 许可证

- **StreamCap部分**: Apache License 2.0
- **DouyinLiveWebFetcher部分**: 请参考原项目许可证声明

---

## 🙏 致谢

感谢以下开源项目的作者和贡献者：

- **Hmily** - StreamCap项目的创建者和维护者
- **saermart** (bubu) - DouyinLiveWebFetcher项目的作者
- 所有为这两个项目做出贡献的开发者

---

**最后更新**: 2025年3月
