<p align="center">
  <h1 align="center">🤖 TermChat</h1>
  <p align="center">
    <strong>Lightweight Universal Terminal AI Chat Assistant</strong>
  </p>
  <p align="center">
    <a href="#-简体中文">简体中文</a> ·
    <a href="#-繁體中文">繁體中文</a> ·
    <a href="#-english">English</a>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome">
  </p>
</p>

---

<a id="-简体中文"></a>

## 🎉 项目介绍

**TermChat** 是一款轻量级的通用终端 AI 对话助手，专为开发者打造。它支持多种大语言模型（LLM）后端，提供流式输出、会话管理、Markdown 渲染等核心功能，让你在终端中即可享受流畅的 AI 对话体验。

### 💡 灵感来源与差异化亮点

受 GitHub Trending 热门项目 DeepSeek-TUI 启发，TermChat 在其产品理念基础上进行了全面差异化升级：

- 🌐 **多 LLM 后端支持** — 不仅限于单一模型，支持 OpenAI、DeepSeek、Ollama、Groq、Together AI、OpenRouter 等主流平台
- 💾 **会话管理系统** — 创建、切换、搜索、导出多个独立对话会话，所有记录持久化存储
- 🎨 **精美终端 UI** — 基于 Rich 库的 Markdown 渲染、语法高亮、多主题切换
- ⚡ **流式实时输出** — 逐字流式显示 AI 回复，体验流畅自然
- 🔧 **零门槛配置** — 环境变量自动读取、一键初始化配置文件
- 🐍 **Python 生态** — 低贡献门槛，丰富的扩展可能

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🤖 **多模型支持** | OpenAI / DeepSeek / Ollama / Groq / Together / OpenRouter |
| ⚡ **流式输出** | 实时逐字显示 AI 回复，响应迅速 |
| 💬 **多会话管理** | 创建、切换、删除、搜索多个独立对话 |
| 📝 **Markdown 渲染** | 完整支持 Markdown 格式、代码高亮 |
| 🎨 **多主题切换** | Monokai / Dark / Light 三套精美主题 |
| 🔍 **历史搜索** | 跨会话全文搜索历史消息 |
| 📤 **会话导出** | 一键导出对话为 Markdown 文件 |
| 🔌 **OpenAI 兼容** | 支持所有 OpenAI 兼容 API 接口 |
| ⚙️ **灵活配置** | YAML 配置文件 + 环境变量双重管理 |
| 🧪 **完整测试** | 27 个单元测试，代码质量有保障 |

---

## 🚀 快速开始

### 环境要求

- **Python** >= 3.9
- **pip** (Python 包管理器)
- 一个 LLM API Key（OpenAI / DeepSeek / Groq 等）

### 安装

```bash
# 使用 pip 安装
pip install termchat

# 或从源码安装
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e .
```

### 初始化配置

```bash
# 创建默认配置文件
termchat --init
```

配置文件位置：`~/.termchat/config.yaml`

### 设置 API Key

**方式一：编辑配置文件**

```bash
# 编辑配置文件，填入你的 API Key
nano ~/.termchat/config.yaml
```

**方式二：使用环境变量**

```bash
export OPENAI_API_KEY="sk-your-key"
export DEEPSEEK_API_KEY="sk-your-key"
export GROQ_API_KEY="gsk-your-key"
```

### 启动对话

```bash
termchat
```

---

## 📖 详细使用指南

### 基本对话

启动 TermChat 后，直接输入消息即可开始对话：

```
[openai] default> 你好，请介绍一下你自己
```

### 命令列表

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助信息 |
| `/clear` | 清空当前对话 |
| `/new <name>` | 创建新会话 |
| `/switch <name>` | 切换到指定会话 |
| `/sessions` | 列出所有会话 |
| `/delete <name>` | 删除指定会话 |
| `/provider <name>` | 切换 LLM 提供商 |
| `/model <name>` | 更换当前模型 |
| `/providers` | 列出所有可用提供商 |
| `/config` | 显示当前配置 |
| `/theme <name>` | 切换主题 (monokai/dark/light) |
| `/save` | 保存当前会话 |
| `/search <query>` | 搜索历史消息 |
| `/export <path>` | 导出会话为 Markdown |
| `/test` | 测试当前提供商连接 |
| `/quit` | 退出 TermChat |

### 切换提供商

```
[openai] default> /provider deepseek
✓ Switched to provider 'deepseek' (model: deepseek-chat)
```

### 使用 Ollama 本地模型

确保 Ollama 已启动，然后切换提供商：

```
[openai] default> /provider ollama
✓ Switched to provider 'ollama' (model: llama3)
```

### 导出对话

```
[openai] default> /export my_chat.md
✓ Session exported to my_chat.md
```

---

## 💡 设计思路与迭代规划

### 设计理念

TermChat 的核心理念是**「终端即界面，简洁即力量」**。我们相信开发者最熟悉的工作环境就是终端，因此将 AI 对话能力无缝融入终端体验，无需打开浏览器或额外应用。

### 技术选型

- **Python** — 生态丰富、贡献门槛低、异步支持完善
- **Rich** — 终端渲染天花板，Markdown/语法高亮开箱即用
- **Prompt Toolkit** — 成熟的终端交互库，自动补全和历史记录
- **httpx** — 现代异步 HTTP 客户端，流式支持优秀

### 后续规划

- [ ] 🖼️ 图片输入支持（多模态对话）
- [ ] 🔄 对话分支管理
- [ ] 📊 Token 用量统计与成本追踪
- [ ] 🔌 插件系统（自定义命令扩展）
- [ ] 🌐 Web UI 模式（浏览器访问）
- [ ] 📱 MCP 协议集成

---

## 📦 安装与部署

### pip 安装（推荐）

```bash
pip install termchat
```

### 从源码安装

```bash
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e .
```

### 开发模式

```bash
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e ".[dev]"
pytest  # 运行测试
ruff check src/  # 代码检查
```

### 兼容环境

| 环境 | 最低版本 |
|------|----------|
| Python | 3.9+ |
| OS | Linux / macOS / Windows |
| 终端 | 任何支持 ANSI 的终端 |

---

## 🤝 贡献指南

欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<a id="-繁體中文"></a>

## 🎉 專案介紹

**TermChat** 是一款輕量級的通用終端 AI 對話助手，專為開發者打造。它支援多種大語言模型（LLM）後端，提供串流輸出、會話管理、Markdown 渲染等核心功能，讓你在終端中即可享受流暢的 AI 對話體驗。

### 💡 靈感來源與差異化亮點

受 GitHub Trending 熱門專案 DeepSeek-TUI 啟發，TermChat 在其產品理念基礎上進行了全面差異化升級：

- 🌐 **多 LLM 後端支援** — 不僅限於單一模型，支援 OpenAI、DeepSeek、Ollama、Groq、Together AI、OpenRouter 等主流平台
- 💾 **會話管理系統** — 建立、切換、搜尋、匯出多個獨立對話會話，所有記錄持久化儲存
- 🎨 **精美終端 UI** — 基於 Rich 函式庫的 Markdown 渲染、語法高亮、多主題切換
- ⚡ **串流即時輸出** — 逐字串流顯示 AI 回覆，體驗流暢自然
- 🔧 **零門檻配置** — 環境變數自動讀取、一鍵初始化設定檔
- 🐍 **Python 生態** — 低貢獻門檻，豐富的擴展可能

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🤖 **多模型支援** | OpenAI / DeepSeek / Ollama / Groq / Together / OpenRouter |
| ⚡ **串流輸出** | 即時逐字顯示 AI 回覆，回應迅速 |
| 💬 **多會話管理** | 建立、切換、刪除、搜尋多個獨立對話 |
| 📝 **Markdown 渲染** | 完整支援 Markdown 格式、程式碼高亮 |
| 🎨 **多主題切換** | Monokai / Dark / Light 三套精美主題 |
| 🔍 **歷史搜尋** | 跨會話全文搜尋歷史訊息 |
| 📤 **會話匯出** | 一鍵匯出對話為 Markdown 檔案 |
| 🔌 **OpenAI 相容** | 支援所有 OpenAI 相容 API 介面 |
| ⚙️ **靈活配置** | YAML 設定檔 + 環境變數雙重管理 |
| 🧪 **完整測試** | 27 個單元測試，程式碼品質有保障 |

---

## 🚀 快速開始

### 環境需求

- **Python** >= 3.9
- **pip**（Python 套件管理器）
- 一個 LLM API Key（OpenAI / DeepSeek / Groq 等）

### 安裝

```bash
# 使用 pip 安裝
pip install termchat

# 或從原始碼安裝
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e .
```

### 初始化配置

```bash
# 建立預設設定檔
termchat --init
```

設定檔位置：`~/.termchat/config.yaml`

### 設定 API Key

**方式一：編輯設定檔**

```bash
nano ~/.termchat/config.yaml
```

**方式二：使用環境變數**

```bash
export OPENAI_API_KEY="sk-your-key"
export DEEPSEEK_API_KEY="sk-your-key"
export GROQ_API_KEY="gsk-your-key"
```

### 啟動對話

```bash
termchat
```

---

## 📖 詳細使用指南

### 基本對話

啟動 TermChat 後，直接輸入訊息即可開始對話：

```
[openai] default> 你好，請介紹一下你自己
```

### 命令列表

| 命令 | 說明 |
|------|------|
| `/help` | 顯示說明資訊 |
| `/clear` | 清空目前對話 |
| `/new <name>` | 建立新會話 |
| `/switch <name>` | 切換到指定會話 |
| `/sessions` | 列出所有會話 |
| `/delete <name>` | 刪除指定會話 |
| `/provider <name>` | 切換 LLM 提供者 |
| `/model <name>` | 更換目前模型 |
| `/providers` | 列出所有可用提供者 |
| `/config` | 顯示目前配置 |
| `/theme <name>` | 切換主題 (monokai/dark/light) |
| `/save` | 儲存目前會話 |
| `/search <query>` | 搜尋歷史訊息 |
| `/export <path>` | 匯出會話為 Markdown |
| `/test` | 測試目前提供者連線 |
| `/quit` | 結束 TermChat |

---

## 💡 設計思路與迭代規劃

### 設計理念

TermChat 的核心理念是**「終端即介面，簡潔即力量」**。我們相信開發者最熟悉的工作環境就是終端，因此將 AI 對話能力無縫融入終端體驗，無需開啟瀏覽器或額外應用。

### 後續規劃

- [ ] 🖼️ 圖片輸入支援（多模態對話）
- [ ] 🔄 對話分支管理
- [ ] 📊 Token 用量統計與成本追蹤
- [ ] 🔌 外掛系統（自訂命令擴展）
- [ ] 🌐 Web UI 模式（瀏覽器存取）

---

## 📦 安裝與部署

### pip 安裝（推薦）

```bash
pip install termchat
```

### 從原始碼安裝

```bash
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e .
```

### 開發模式

```bash
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e ".[dev]"
pytest
ruff check src/
```

---

## 🤝 貢獻指南

歡迎所有形式的貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

---

## 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

---

<a id="-english"></a>

## 🎉 Introduction

**TermChat** is a lightweight universal terminal AI chat assistant designed for developers. It supports multiple LLM backends with streaming output, session management, Markdown rendering, and more — bringing a seamless AI conversation experience right to your terminal.

### 💡 Inspiration & Differentiation

Inspired by the trending GitHub project DeepSeek-TUI, TermChat delivers a comprehensively upgraded experience:

- 🌐 **Multi-LLM Backend** — Not limited to a single model; supports OpenAI, DeepSeek, Ollama, Groq, Together AI, OpenRouter, and more
- 💾 **Session Management** — Create, switch, search, and export multiple independent chat sessions with persistent storage
- 🎨 **Beautiful Terminal UI** — Markdown rendering, syntax highlighting, and multi-theme support powered by Rich
- ⚡ **Streaming Output** — Real-time character-by-character AI response display for a natural experience
- 🔧 **Zero-Friction Setup** — Auto-read environment variables, one-command config initialization
- 🐍 **Python Ecosystem** — Low contribution barrier with rich extension possibilities

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Model Support** | OpenAI / DeepSeek / Ollama / Groq / Together / OpenRouter |
| ⚡ **Streaming Output** | Real-time token-by-token AI response display |
| 💬 **Multi-Session** | Create, switch, delete, and search across multiple conversations |
| 📝 **Markdown Rendering** | Full Markdown support with syntax highlighting |
| 🎨 **Theme Switching** | Monokai / Dark / Light themes |
| 🔍 **History Search** | Full-text search across all sessions |
| 📤 **Session Export** | One-click export to Markdown files |
| 🔌 **OpenAI Compatible** | Works with any OpenAI-compatible API |
| ⚙️ **Flexible Config** | YAML config file + environment variable support |
| 🧪 **Well Tested** | 27 unit tests ensuring code quality |

---

## 🚀 Quick Start

### Requirements

- **Python** >= 3.9
- **pip** package manager
- An LLM API key (OpenAI / DeepSeek / Groq, etc.)

### Installation

```bash
# Install via pip
pip install termchat

# Or install from source
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e .
```

### Initialize Configuration

```bash
termchat --init
```

Config file location: `~/.termchat/config.yaml`

### Set API Key

**Option 1: Edit config file**

```bash
nano ~/.termchat/config.yaml
```

**Option 2: Use environment variables**

```bash
export OPENAI_API_KEY="sk-your-key"
export DEEPSEEK_API_KEY="sk-your-key"
export GROQ_API_KEY="gsk-your-key"
```

### Start Chatting

```bash
termchat
```

---

## 📖 Usage Guide

### Basic Chat

After launching TermChat, simply type your message:

```
[openai] default> Hello, introduce yourself
```

### Command Reference

| Command | Description |
|---------|-------------|
| `/help` | Show help information |
| `/clear` | Clear current conversation |
| `/new <name>` | Create a new session |
| `/switch <name>` | Switch to a session |
| `/sessions` | List all sessions |
| `/delete <name>` | Delete a session |
| `/provider <name>` | Switch LLM provider |
| `/model <name>` | Change model |
| `/providers` | List available providers |
| `/config` | Show current configuration |
| `/theme <name>` | Switch theme (monokai/dark/light) |
| `/save` | Save current session |
| `/search <query>` | Search message history |
| `/export <path>` | Export session to Markdown |
| `/test` | Test provider connection |
| `/quit` | Exit TermChat |

### Switching Providers

```
[openai] default> /provider deepseek
✓ Switched to provider 'deepseek' (model: deepseek-chat)
```

### Using Ollama (Local Models)

Make sure Ollama is running, then switch the provider:

```
[openai] default> /provider ollama
✓ Switched to provider 'ollama' (model: llama3)
```

### Export Conversations

```
[openai] default> /export my_chat.md
✓ Session exported to my_chat.md
```

---

## 💡 Design Philosophy & Roadmap

### Philosophy

**"Terminal as interface, simplicity as power."** We believe the terminal is the developer's most natural workspace. TermChat seamlessly integrates AI conversation capabilities into the terminal experience — no browser or extra apps needed.

### Tech Stack

- **Python** — Rich ecosystem, low contribution barrier, excellent async support
- **Rich** — Best-in-class terminal rendering with Markdown and syntax highlighting
- **Prompt Toolkit** — Mature terminal interaction with auto-completion and history
- **httpx** — Modern async HTTP client with excellent streaming support

### Roadmap

- [ ] 🖼️ Image input support (multimodal chat)
- [ ] 🔄 Conversation branching
- [ ] 📊 Token usage & cost tracking
- [ ] 🔌 Plugin system (custom command extensions)
- [ ] 🌐 Web UI mode
- [ ] 📱 MCP protocol integration

---

## 📦 Installation & Deployment

### pip Install (Recommended)

```bash
pip install termchat
```

### From Source

```bash
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e .
```

### Development Mode

```bash
git clone https://github.com/gitstq/termchat.git
cd termchat
pip install -e ".[dev]"
pytest  # Run tests
ruff check src/  # Lint
```

### Compatible Environments

| Environment | Minimum Version |
|-------------|-----------------|
| Python | 3.9+ |
| OS | Linux / macOS / Windows |
| Terminal | Any ANSI-compatible terminal |

---

## 🤝 Contributing

Contributions of all forms are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push the branch: `git push origin feature/amazing-feature`
5. Submit a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
