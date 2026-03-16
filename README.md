# CaptLive

基于 StreamCap 和 DouyinLiveWebFetcher 合并开发的直播录制工具，可一键抓取直播间弹幕，视频，下单信息。自动检测开播并进行录制。

## 📋 项目说明

本项目由多个开源项目合并并修改而来：

### 1. StreamCap
- **GitHub**: [ihmily/StreamCap](https://github.com/ihmily/StreamCap)
- **作者**: Hmily
- **许可证**: Apache License 2.0
- **说明**: 多平台直播录制工具，提供项目主体架构和UI框架

### 2. DouyinLiveWebFetcher
- **GitHub**: [saermart/DouyinLiveWebFetcher](https://github.com/saermart/DouyinLiveWebFetcher)
- **作者**: saermart (bubu)
- **联系方式**: 
  - 微博: [@kukushka](https://weibo.com/u/7751075499)
  - B站: [B站主页](https://space.bilibili.com/4690313)
  - 邮箱: kukushka@126.com
- **说明**: 抖音网页版弹幕数据抓取，提供抖音弹幕抓取核心逻辑

### 3. dycast (参考)
- **GitHub**: [skmcj/dycast](https://github.com/skmcj/dycast)
- **作者**: skmcj (深坑妙脆角)
- **说明**: TypeScript/Vue项目，当前项目主要使用DouyinLiveWebFetcher的Python实现

详细代码来源和作者信息请查看 [ATTRIBUTION.md](./ATTRIBUTION.md) 和 [FINAL_CODE_ATTRIBUTION.md](./FINAL_CODE_ATTRIBUTION.md)

## 🚀 快速开始

### 环境要求

- Python 3.10+
- FFmpeg
- Node.js v18+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
python main.py
```

## 📚 文档

- [代码来源声明](./ATTRIBUTION.md) - 详细的代码来源和作者信息
- [最终代码来源标注](./FINAL_CODE_ATTRIBUTION.md) - 基于GitHub对比的精准代码来源标注
- [Git作者标注指南](./GIT_ATTRIBUTION_GUIDE.md) - 如何在GitHub上显示代码原作者
- [技术指南](./技术指南.md) - 项目技术文档
- [论文章节说明](./README_论文章节说明.md) - 论文章节文档说明

## ⚠️ 重要声明

### 代码使用声明

本项目中的代码来自以下开源项目：

- **StreamCap**: Apache License 2.0
- **DouyinLiveWebFetcher**: 仅用于学习研究交流，严禁用于商业谋利、破坏系统、盗取个人信息等不良不法行为

**使用本项目代码时，请遵守原项目的许可证和使用声明。**

### 侵权声明

如果涉及侵权，请联系原作者：
- **StreamCap**: [GitHub Issues](https://github.com/ihmily/StreamCap/issues)
- **DouyinLiveWebFetcher**: 
  - 微博: [@kukushka](https://weibo.com/u/7751075499)
  - B站: [B站主页](https://space.bilibili.com/4690313)
  - 邮箱: kukushka@126.com
- **dycast**: [GitHub Issues](https://github.com/skmcj/dycast/issues)

## 🙏 致谢

感谢以下开源项目的作者和贡献者：

- **Hmily** - [StreamCap](https://github.com/ihmily/StreamCap) 项目的创建者和维护者
- **saermart (bubu)** - [DouyinLiveWebFetcher](https://github.com/saermart/DouyinLiveWebFetcher) 项目的作者
- **skmcj (深坑妙脆角)** - [dycast](https://github.com/skmcj/dycast) 项目的作者（参考）
- 所有为这些项目做出贡献的开发者

## 📄 许可证

本项目遵循以下许可证：

- **StreamCap 部分**: Apache License 2.0
- **DouyinLiveWebFetcher 部分**: 仅用于学习研究交流，严禁用于商业谋利、破坏系统、盗取个人信息等不良不法行为

详细说明请查看 [ATTRIBUTION.md](./ATTRIBUTION.md) 和 [FINAL_CODE_ATTRIBUTION.md](./FINAL_CODE_ATTRIBUTION.md)

---

**注意**: 本项目仅用于学习研究交流，请勿用于商业用途或违法行为。
