# 代码来源与作者声明

本项目由两个开源项目合并并修改而来。以下详细列出了代码的来源和原作者信息。

## 📚 代码来源

### 1. StreamCap

**项目名称**: StreamCap  
**GitHub仓库**: [ihmily/StreamCap](https://github.com/ihmily/StreamCap)  
**作者**: Hmily  
**许可证**: Apache License 2.0

**使用的代码部分**:
- 项目主体架构和UI框架
- 直播录制核心功能
- 多平台支持适配器
- 配置管理和应用管理模块
- UI组件和页面视图

**相关文件**:
- `app/app_manager.py` - 应用管理器
- `app/core/` - 核心业务逻辑模块
- `app/ui/` - 用户界面组件
- `app/core/platform_handlers/` - 平台处理器
- `main.py` - 程序入口
- 以及其他大部分项目文件

---

### 2. DouyinLiveWebFetcher

**项目名称**: DouyinLiveWebFetcher (抖音网页版弹幕数据抓取)  
**GitHub仓库**: [saermart/DouyinLiveWebFetcher](https://github.com/saermart/DouyinLiveWebFetcher)  
**原作者联系方式**:
- 微博: [@kukushka](https://weibo.com/u/7751075499)
- B站: [B站主页](https://space.bilibili.com/4690313)
- 邮箱: kukushka@126.com

**使用的代码部分**:
- 抖音弹幕抓取核心逻辑
- WebSocket连接和消息处理
- Protobuf消息解析
- 签名算法实现

**相关文件**:
- `app/douyin_fetcher/liveMan.py` - 抖音弹幕抓取核心逻辑
- `app/douyin_fetcher/sign.js` - 签名算法
- `app/douyin_fetcher/protobuf/` - Protobuf定义和解析
- `DouyinLiveWebFetcher-main/` - 原始代码目录（保留作为参考）

---

## 🔄 修改说明

本项目在合并两个开源项目的基础上进行了以下修改和整合：

1. **架构整合**: 将DouyinLiveWebFetcher的弹幕抓取功能整合到StreamCap的架构中
2. **适配器模式**: 创建了`streamcap_adapter.py`作为适配器，将DouyinLiveWebFetcher集成到StreamCap的平台处理器体系
3. **功能增强**: 在原有功能基础上添加了新的特性和优化
4. **代码重构**: 对部分代码进行了重构以提高可维护性

---

## 📝 原始项目声明

### DouyinLiveWebFetcher 原始声明

> 本代码库所有代码均只用于学习研究交流，严禁用于包括但不限于商业谋利、破坏系统、盗取个人信息等不良不法行为，违反此声明使用所产生的一切后果均由违反声明使用者承担。

> 如果涉及侵权请联系作者删除本库代码，此repo仅仅用于学习交流。

---

## 🙏 致谢

感谢以下开源项目的作者和贡献者：

- **Hmily** - StreamCap项目的创建者和维护者
- **saermart** (DouyinLiveWebFetcher作者) - 抖音弹幕抓取技术的实现者
- 所有为这两个项目做出贡献的开发者

---

## 📄 许可证

本项目遵循以下许可证：

- StreamCap部分: Apache License 2.0
- DouyinLiveWebFetcher部分: 请参考原项目许可证声明

---

## 📞 联系方式

如有关于代码来源或使用的问题，请联系：

- StreamCap相关问题: [GitHub Issues](https://github.com/ihmily/StreamCap/issues)
- DouyinLiveWebFetcher相关问题: 通过原作者的微博、B站或邮箱联系

---

**最后更新**: 2025年3月
