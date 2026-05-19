<div align="center">
<img src="preview/show.jpg" width="100%" />

# MatesX

> 记忆 · 表情 · 动作 · 多端 · 轻量

[English](README.md) | [中文版](README_zh.md)
</div>

## 🎯 项目主旨
- **支持个人玩家自定义自己的AI伙伴**
- **支持面向海量 C 端用户的超高并发数字人服务**

### 三大核心目标：

1. ✅ **大规模高并发 C 端数字人对话管理**

2. ✅ **记忆、情感、表情与动作管理**

3. ✅ **桌面端、APP、小程序多端共用，超轻量级架构**

---

## 🚀 核心功能

### 1. 🗣️ 数字人全链路对话引擎
> `VAD（语音活动检测） → ASR（语音识别） → LLM（大语言模型） → TTS（语音合成） → 数字人驱动`

### 2. 🧠 mem0 级记忆功能
- 长短期记忆融合，支持个性化对话历史存储与上下文理解
- 用户画像动态构建，记忆持久化、跨设备同步

### 3. 😊 实时情感解析
- 基于语音语调、语义内容、对话节奏的多模态情感识别
- 输出情感标签（开心/悲伤/愤怒/惊讶等）驱动表情与语调变化

### 4. 🎭 自由表情 & 自由动作
- 大模型算法建模，支持骨骼/BlendShape 驱动
- 实时根据对话内容、情感状态自动匹配表情与肢体语言

---

## 📱 多端支持

| 平台          | 支持状态 | 技术路线       | 预览                                   |                                                                                            |
|-------------|------|------------|----------------------------------------|--------------------------------------------------------------------------------------------|
| Windows     | ✅    | electron   | <img src="preview/windows.jpg" width="120" />      | [exe link](https://github.com/kleinlee/MatesX/releases/download/v1.0/matesx-win32-x64.zip) |
| macOS       | ✅    | electron   |                                        ||
| Android app | ✅    | webview    | <img src="preview/android.jpg" width="120" />      | [apk link](https://github.com/kleinlee/MatesX/releases/download/v1.0/app-debug.apk)        |
| 微信小程序       | ✅    | webview    | <img src="preview/mini-program.jpg" width="120" /> | 小程序:MatesX数字生命                                                                             |   
| Web         | ✅    | WebGL 渲染支持 | <img src="preview/web.jpg" width="120" />        | [web link](https://www.matesx.com)                                                         |
> 💡 所有平台共享同一套核心引擎，代码复用率 > 99%，极致轻量（核心模块 < 5MB）

---

## 🛠️ 快速开始

```bash
git clone https://github.com/kleinlee/MatesX.git
cd MatesX
pip install -r requirements.txt
```
部署对话语音模型云服务（alibaba dashscope）

修改utils/dashscope.py 中的：
```bash
# 配置大模型专属接口
DASHSCOPE_API_KEY = ""     # 请到阿里云百炼开通API-key
DASHSCOPE_TOKEN_URL = "https://dashscope.aliyuncs.com/api/v1/tokens"
DASHSCOPE_LLM_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 默认的记忆文件配置地址
memory_data_url = "http://localhost:8000/api/assets/{avatar_id}/memory.bin"
# 默认的语音文件云存储地址（用于语音克隆）
OSS_URL = "https://matesx.oss-cn-beijing.aliyuncs.com/audio/user"

# 配置 MatesX形象平台秘钥
MatesX_key = ""           # 从matesx.cn获取
# 可选: 配置腾讯云 大模型音色
USE_TENCENT_TTS = True   # 默认为False（优先使用阿里云音色）
class TencentTtsConfig:
    SECRET_ID = ""
    SECRET_KEY = ""
    APP_ID = 
```
开启服务：
```bash
python main.py
```
然后打开 http://localhost:8000/web/home.html 享用吧

## 定制形象
此项目不提供复杂的底层算法实现而专注于轻量但完备的应用。

对于个人爱好者，我们会在[matesx网页程序](https://www.matesx.com)定期提供免费额度。

对于开发者，[联系我](preview/wechat.jpg)获取3个免费额度秘钥。请参阅 [API](preview/API.md) 的API付费调用方式，可欢迎使用[matesx platform](https://matesx.com/platform.html)来管理你的形象。

---

## ⚡ 无服务器最简部署

> **无需服务器！** 输入阿里百炼 API-key 即可直接开始对话

| | |
|---|---|
| **🌐 在线体验** | [https://kleinlee.github.io/character.html](https://kleinlee.github.io/character.html) |
| **📦 源码地址** | [https://github.com/kleinlee/kleinlee.github.io](https://github.com/kleinlee/kleinlee.github.io) |

如果你想保持最小的代码实现，这是最简部署方式——纯静态部署，所有计算（VAD、唇形同步、表情驱动）都在浏览器端完成。只需填入阿里百炼 API-key，即可直接与数字人对话！

---

### 编译
支持windows、mac、android、mini-program

参考 [platform文件夹](platform/README.md) 

### 高并发及云端同步
- 升级为云端数据库
- 资源放置到OSS

## License
Apache License 2.0

## 联系
|  微信交流群| QQ群聊                                                                        |
|------------------|----------------------------------------------------------------------------------------|
| <img src="preview/wechat.jpg" width="480" alt="MatesX 官方微信"/> | <img src="preview/qq.jpg" width="480" alt="MatesX 官方QQ"/>|

