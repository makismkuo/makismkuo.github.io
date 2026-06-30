---
title: "Harbor：一行命令启动你本地的全套 LLM 堆栈"
date: 2026-06-30
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
---

想在本地跑 LLM，光装个 Ollama 是不够的。你还得配前端（Open WebUI）、搭搜索（SearXNG）、连 RAG 管线、搞语音聊天……每个服务单独折腾 docker-compose，调了半天网络配置，最后模型没跑起来，人先跑了。

**Harbor**（⭐3112）就是来解决这个痛点的。一条 `harbor up` 命令，就能把整套本地 LLM 堆栈——后端、前端、搜索、语音、MCP、图片生成——全部预配好、互联互通、直接可用。

## 核心功能

Harbor 本质上是一个 **Docker Compose 编排器 + 服务目录**。它内置了 90+ 个服务的配置模板，涵盖：

- **后端推理引擎**：Ollama、llama.cpp、vLLM、MLX（macOS Metal 加速）、SGLang、TGI 等
- **前端 UI**：Open WebUI、LibreChat、LobeChat、AnythingLLM 等
- **卫星服务**：SearXNG（搜索）、Dify/n8n（工作流）、ComfyUI（图片）、Speaches（语音）、MCP 工具、Bolt.new 等
- **Agent 工具**：Aider、OpenHands、Browser Use、Coding Agent 启动、自查 Agent

所有服务之间已预先配置好互联——启动 Open WebUI 和 SearXNG，聊天界面自动就有了网页搜索能力。

## 为什么值得关注

我试过几个「本地 AI 堆栈」项目，大部分要么预配过度（塞了一堆你不用的服务），要么配置不够（装完还得你自己东连西连）。Harbor 的取舍做得很好：

**1. 按需启动。** 不装全家桶。想试语音？`harbor up speaches`。要图片？`harbor up comfyui`。每个服务独立，不影响其他。

**2. 一站式集成。** SearXNG 配 Open WebUI、Speaches 配语音输入、harbor launch 配 Claude Code/Codex——全都开箱即用。

**3. Agent 工作流。** Harbor Boost 模块可以编排多步 agent 流程：先深搜，再读代码，改完自动审计。`harbor launch --workflow shipyard` 把一整条管线接到你的编码代理上。

**4. 不锁死。** `harbor eject` 可以把当前配置导出成独立 docker-compose.yml，随时搬家。

## 快速上手

```bash
# 安装（macOS/Linux）
curl -fsSL https://raw.githubusercontent.com/av/harbor/main/install.sh | sh

# 从最简单的开始：Ollama + Open WebUI
harbor up ollama

# 再加搜索和语音
harbor up searxng speaches

# 启动后，在浏览器打开 http://localhost:33801 就能用了

# 想用其他后端？几秒切换
harbor up llamacpp    # llama.cpp
harbor up vllm        # vLLM
harbor up mlx         # macOS Metal 原生推理
```

整个配置数据存在 `~/.harbor/` 下，`harbor help` 随时查看全部命令。

## 总结

Harbor 是目前见过最务实的本地 LLM 管理工具。它不做无谓的包装，而是把 Docker Compose、服务发现、预配互联这些脏活替你干了，让你只用关心一件事：选什么模型、跑什么服务。

对于想认真玩本地 AI 但不想花一整天写 docker-compose 的开发者，Harbor 是我的首选推荐。

GitHub: [av/harbor](https://github.com/av/harbor)
