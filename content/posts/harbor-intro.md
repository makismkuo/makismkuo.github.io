---
title: "Harbor：一条命令搞定你的本地 LLM 全家桶"
date: 2026-07-06
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "LLM", "DevOps"]
---

## 项目简介

[**Harbor**](https://github.com/av/harbor)（3.1k Stars）是一个 CLI 工具，让你用一条命令启动完整的本地 LLM 基础设施——后端（Ollama、llama.cpp、vLLM），前端（Open WebUI），再加上搜索引擎、语音对话、图片生成等配套服务，全部预配置好，即开即用。

作者把它定位为"Stop configuring your AI stack. Start using it." 如果你曾经花一下午翻 Docker Compose 文档，就为了让 Open WebUI 连上 SearXNG 跑 Web RAG，Harbor 就是为你写的。

## 核心功能

安装后只需要一条命令：

```bash
# 启动 Ollama + Open WebUI
harbor up

# 加 Web 搜索和语音
harbor up searxng speaches

# 加图片生成
harbor up comfyui
```

Harbor 会自动编排 Docker Compose 服务、打通网络、写入配置。它目前支持的服务超过 30 个：

- **推理后端**：Ollama、llama.cpp、vLLM、TGI、MLX（macOS Metal 加速）
- **前端**：Open WebUI、ChatUI、Morphic
- **搜索/RAG**：SearXNG、Perplexica、Local Deep Research
- **语音**：Speaches（OpenAI 兼容的 TTS/STT）
- **图片**：ComfyUI + Flux
- **工作流**：Dify、n8n、Flowise、LangFlow
- **MCP 生态**：MetamCP、MCPO

更厉害的是 `harbor launch` 命令——它会启动一个后端，然后把模型自动挂到 Claude Code、Codex、OpenCode、Copilot 等编码工具上，不用手动改 provider 配置：

```bash
harbor launch --backend ollama --model qwen3.5:4b codex
```

还有 Harbor Boost 模块，可以把 web 研究、任务锚定、交付物审计组合成工作流预设（shipyard、agent-code、research-quick），跑一次 `harbor launch --workflow shipyard` 就自动串联整套流程。

## 为什么值得关注

本地 LLM 的瓶颈从来不是模型本身，而是"基础设施地狱"：装 Ollama → 装 Open WebUI → 配 SearXNG → 搞语音集成 → 写 Docker Compose → 调试网络……每一步都有坑。

Harbor 把这个过程从"半天起步"压缩到"三秒一条命令"。它不做任何假设——你可以在一条命令里换后端、加服务、指定模型参数。同时它也懂 macOS 生态（DMR、MLX 直接走 Metal 加速，不用起容器），对开发者友好到骨子里。

对于还在纠结"要不要部署本地 LLM"的团队和个人，Harbor 直接把决策成本降到了零。装一下试半小时，不合适删掉也没负担。

## 简单上手

```bash
# 安装
curl -fsSL https://harbor.run/install.sh | sh

# 启动最简配置（Ollama + Open WebUI）
harbor up -d

# 查看所有运行中的服务
harbor ps

# 用 QR 码在手机上打开 Open WebUI
harbor qr

# 拉个模型到 Ollama
harbor exec ollama pull qwen3.5:4b

# 停止全部
harbor down
```

安装后浏览器打开 `http://localhost:3000` 就能用 Open WebUI 了。

## 总结

Harbor 解决的是一个实际且普遍的问题：本地 LLM 部署的繁琐配置。它不像有些项目做一套封闭的"一键方案"把你锁死——它用 Docker Compose 包装了数十个真实服务，你自由组合，也能单独替换。3.1k Stars 和频繁更新的节奏说明社区正在用它。

如果你玩本地模型但不想当运维，或者想给团队搭一套内网 AI 环境，Harbor 值得花十分钟试试。
