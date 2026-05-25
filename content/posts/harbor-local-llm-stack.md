---
title: "Harbor：一条命令拉起你的本地 LLM 全家桶"
date: 2026-05-25
draft: false
tags: ["开源", "推荐", "GitHub", "LLM", "本地部署"]
---

想在本地跑 LLM，最折腾的是什么？不是模型本身，是搭环境。

装 Ollama → 配 Open WebUI → 搞个搜索引擎做 RAG → 再来个语音模型……每一步都有兼容性问题、端口冲突、配置项搞不清。弄完两天过去了，模型还没跑一次。

[Harbor](https://github.com/av/harbor) 解决的就是这个问题。一条命令拉起你需要的所有服务，全自动配好。

### 它不是又一个 Docker 编排工具

市面上用 Docker Compose 做 AI 栈部署的方案不少，但 Harbor 的区别是：**它知道这些服务之间怎么连接**。

你执行 `harbor up ollama`，它不仅启动 Ollama，还会自动把 Ollama 注册到 Open WebUI 的后端列表里。加一个 SearXNG 做搜索，Open WebUI 的 RAG 功能自动生效。再加 Speaches，语音对话直接能用。

这些互通逻辑是内置的，不用你自己写环境变量或者配置 API 地址。

### 实际用起来什么样

```
# 最简启动
harbor up ollama

# 带 Web 界面 + 搜索 RAG
harbor up open-webui searxng

# 全家桶：后端 + 前端 + 搜索 + 语音
harbor up ollama open-webui searxng speaches

# 用 llama.cpp 替代 Ollama
harbor up llamacpp
harbor llamacpp args -ngl 32
```

支持的 backend 包括 Ollama、llama.cpp、vLLM、TabbyAPI。前端除了 Open WebUI 还有 Text Generation Web UI、Lobe Chat、KoboldCPP。

### 适合谁

- 想在本地跑 LLM 但不熟悉 Docker 的人
- 需要快速试不同后端/前端组合的开发者
- 用 AI Agent（Claude Code、Codex 等）需要本地推理的人

### 缺点

- 版本迭代快，偶尔有 breaking change
- 一些服务的默认配置不是最优，需要手动微调
- 没有 GPU passthrough 的自动检测（需要自己确认）

### 总结

Harbor 不是一个非用不可的工具，但它把本地 LLM 部署的**心智负担**降到了最低。如果你已经有一套手动搭好的环境，没必要迁移；如果每次想试新模型都要折腾半小时环境，那它值得一试。

安装就一行：

```
curl -fsSL https://raw.githubusercontent.com/av/harbor/main/install.sh | bash
```

项目地址：[github.com/av/harbor](https://github.com/av/harbor)
