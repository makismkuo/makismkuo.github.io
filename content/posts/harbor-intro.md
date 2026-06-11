---
title: "Harbor：一行命令拉起你全部的本地 AI 栈"
date: 2026-06-11
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "效率工具"]
---

## 工具

折腾本地 LLM 的人都知道那种 frustration：装好 Ollama，又要配 Open WebUI，想加个搜索引擎发现 SearXNG 要写半天配置，想做图还要部署 ComfyUI，每一个服务单独配 Docker Compose，端口冲突、环境变量忘记设、模型路径找不到——半天过去了，一个对话都没聊上。

[Harbor](https://github.com/av/harbor) 就是来解决这个问题的。一条命令拉起完整的本地 AI 栈，所有服务预配好、预互联，零手动配置。

## 核心功能

`harbor up` 是它的灵魂。你想用 Ollama 做后端 + Open WebUI 做前端，就：

```bash
harbor up ollama
```

想加上联网搜索和语音对话：

```bash
harbor up searxng speaches
```

Harbor 会自动编排 Docker Compose，把所有服务连接好。它支持的引擎包括 Ollama、llama.cpp、vLLM、MLX（macOS Metal 加速）、TabbyAPI、SGLang 等十几个。前端除了 Open WebUI，还有 ChatUI、Morphic、Perplexica 等可选。

另一个杀手特性是 `harbor launch`—— 把 Harbor 后端直接挂到你在用的编程 agent 上：

```bash
harbor launch --backend ollama --model qwen3.5:4b codex
```

这行命令拉起模型，生成 provider 配置，然后启动 Codex CLI 直接连过去。支持的宿主工具包括 Claude Code、Codex、Copilot、OpenCode、Hermes 等十几个。

## 为什么值得关注

最打动我的是它对"用完即走"的理解。项目文档说："如果你改主意了，删掉 ~/.harbor 目录就行——没有残留服务，没有系统级修改。" 整个项目是 Python + Shell 写的，用户的数据和配置全在自己机器上，不存在服务端锁定的问题。

生态整合也做得扎实：ComfyUI + Flux 做图、Speaches 做语音、SearXNG 做 RAG 搜索、Metamcp 管理 MCP 工具、Traefik（预配反向代理 + SSL）、Bifrost AI 网关——几乎覆盖了本地 LLM 的所有场景。

Harbor 还有一个 companion GUI app，不习惯 CLI 的人也能用。手机端可以扫 QR 码从局域网访问，甚至内置了隧道功能暴露到公网。

## 简单示例

从零开始：

```bash
# 安装（一行）
curl -fsSL https://harbor-npm.pages.dev/install.sh | sh

# 拉起 Ollama + Open WebUI
harbor up ollama

# 打开 http://localhost:33800 就能聊了
# 加个联网搜索
harbor up searxng
```

macOS 用户还能用 Docker Model Runner 或 MLX 在宿主机上跑 Metal 加速推理，不走容器，性能更好。

## 总结

Harbor 不是另一个 AI 框架，而是一个称职的"部署管家"。它把本地 LLM 从"工程项目"变成了"工具"。如果你经常需要在不同模型、不同前端、不同辅助服务之间切换，Harbor 能省下大量重复配置时间。3054 颗星，Apache-2.0 协议，活跃维护，值得一试。

---

**Seb**
