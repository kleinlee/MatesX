<div align="center">
<img src="preview/show.jpg" width="100%" />

# MatesX

> Memory · Expression · Motion · Multi-platform · Lightweight

[English](README.md) | [中文版](README_zh.md)
</div>

## 🎯 Project Mission
- **Enable individual users to customize their own AI companions**
- **Support ultra-high concurrency digital human services targeting massive C-end users**

### Three Core Objectives:

1. ✅ Large-scale C-end Digital Human Conversation Management

2. ✅ Memory, emotion, Expression & Motion Management

3. ✅ Cross-platform Support for Desktop, APP, Mini Programs with Ultra-lightweight Architecture

---

## 🚀 Core Features

### 1. 🗣️ End-to-End Digital Human Conversation Engine
> VAD (Voice Activity Detection) → ASR (Automatic Speech Recognition) → LLM (Large Language Model) → TTS (Text-to-Speech) → Digital Human Animation

### 2. 🧠 mem0-Level Memory Functionality
- Fusion of long-term and short-term memory, supporting personalized dialogue history storage and contextual understanding
- Dynamic user profiling, persistent memory with cross-device synchronization

### 3. 😊 Real-time Emotion Analysis
- Multimodal emotion recognition based on voice tone, semantic content, and dialogue rhythm
- Outputs emotion tags (happy/sad/angry/surprised, etc.) to drive facial expressions and vocal intonation

### 4. 🎭 Free Expression & Free Motion
- Driven by large-model algorithms, supports skeletal/BlendShape animation
- Automatically matches facial expressions and body language in real-time based on dialogue content and emotional state

---

## 📱 Multi-platform Support

| Platform | Status | Tech Stack | Preview | |
|-----------------|--------|----------------|-------------------------------------------|-----------------------------------------------------------------------------------------|
| Windows | ✅ | electron | <img src="preview/windows.jpg" width="120" /> | [exe link](https://github.com/kleinlee/MatesX/releases/download/v1.0/matesx-win32-x64.zip) |
| macOS | ✅ | electron | ||
| Android app | ✅ | webview | <img src="preview/android.jpg" width="120" /> | [apk link](https://github.com/kleinlee/MatesX/releases/download/v1.0/app-debug.apk) |
| WeChat Mini Program | ✅ | webview | <img src="preview/mini-program.jpg" width="120" /> | 小程序:MatesX数字生命 |
| Web | ✅ | WebGL rendering support | <img src="preview/web.jpg" width="120" /> | [web link](https://www.matesx.com)  |
> 💡 All platforms share the same core engine, code reuse rate > 99%, extremely lightweight (core module < 5MB)

---

## 🛠️ Quick Start

```bash 
git clone https://github.com/kleinlee/MatesX.git
cd MatesX
pip install -r requirements.txt
```
Deploy cloud-based conversation & speech models (Alibaba DashScope)

Modify utils/dashscope.py:
```bash
# Configure LLM-specific API
DASHSCOPE_API_KEY = ""     # Obtain API-key from Alibaba Cloud Bailian
DASHSCOPE_TOKEN_URL = "https://dashscope.aliyuncs.com/api/v1/tokens"
DASHSCOPE_LLM_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# default memory file location
memory_data_url = "http://localhost:8000/api/assets/{avatar_id}/memory.bin"
# default OSS location for voice-clone
OSS_URL = "https://matesx.oss-cn-beijing.aliyuncs.com/audio/user"

# Configure MatesX Avatar key
MatesX_key = ""           # Obtain key from matesx.cn
# Optional: config if using Tencent cloud TTS
USE_TENCENT_TTS = True  # default: False (prefer Alibaba Cloud voice by default)
class TencentTtsConfig:
    SECRET_ID = ""
    SECRET_KEY = ""
    APP_ID = 
```

Start service:
```bash
python main.py
```
Then open http://localhost:8000/web/home.html to enjoy!

### Custom Avatars
This project does not offer underlying algorithm implementations but focuses on lightweight yet comprehensive applications.

For individual enthusiasts, get free credits on [Matesx official web application](https://www.matesx.com). 

For developers, receive 3 free credits by [contacting us](preview/wechat.jpg). please refer to the [API](preview/API.md) for API calling. 
Use [matesx platform](https://matesx.com/platform.html) to manage your avatars.

---

## ⚡ Serverless Minimal Deployment

> **No server required!** Enter your Alibaba Bailian API-key to start chatting instantly.

| | |
|---|---|
| **🌐 Live Demo** | [https://kleinlee.github.io/character.html](https://kleinlee.github.io/character.html) |
| **📦 Source Code** | [https://github.com/kleinlee/kleinlee.github.io](https://github.com/kleinlee/kleinlee.github.io) |

This is the simplest deployment option - pure static deployment with all computation (VAD, lip-sync, expression driving) done directly in the browser. Just fill in your Alibaba Bailian API-key and start talking to the digital human immediately!

---

### Compilation
support Windows, macOS, Android, Mini-Program

Refer to the [platform](platform/README.md) folder

### High Concurrency & Cloud Sync
- Upgrade to cloud database
- Host resources on OSS

## License
Apache License 2.0

## Contact
| join WeChat group                                             | Join QQ group                                            |
|---------------------------------------------------------------|-------------------------------------------------------------|
| <img src="preview/wechat.jpg" width="480" alt="MatesX 官方微信"/> | <img src="preview/qq.jpg" width="480" alt="MatesX 官方QQ"/>|

