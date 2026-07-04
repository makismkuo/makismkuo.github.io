---
title: "Harbor：一条命令拉起你的本地 LLM 全家桶"
date: 2026-07-04T16:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI工具"]
---

## 项目简介

如果你试过自己搭一套本地 LLM 环境，你一定知道有多烦：装 Ollama、配 Open WebUI、折腾 SearXNG 做联网搜索、再搞 ComfyUI 画图……每个服务都要手动配置 Docker Compose，调端口，连环境变量，一不小心就掉坑里。**Harbor**（GitHub：[av/harbor](https://github.com/av/harbor)，⭐3120）就是来解决这个问题的 —— 一条命令拉起完整的本地 LLM 栈，所有服务预连好，开箱即用。

## 核心功能

Harbor 的核心理念是「配置零摩擦」。你只需要装好 Harbor CLI，然后敲 `harbor up ollama`，它就会自动拉起 Ollama + Open WebUI，并且让两个服务互相连通。想加联网搜索？再敲 `harbor up searxng`，SearXNG 自动接入 WebUI。想语音聊天？`harbor up speaches`，TTS/STT 全套到位。

它管理着 **超过 90 种服务**，分为三类：

- **后端引擎**：Ollama、llama.cpp、vLLM、MLX、SGLang、TabbyAPI、KTransformers 等几乎全部主流推理引擎
- **前端界面**：Open WebUI、LibreChat、Lobe Chat、AnythingLLM、ChatUI 等
- **卫星服务**：Dify（工作流）、ComfyUI（图像生成）、SearXNG（搜索）、Perplexica（AI 搜索）、n8n（自动化）、MetaMCP（MCP 管理）、Hermes Agent、OpenHands、Browser Use 等等

所有服务之间已经预配好网络连通和环境变量，你完全不用手动编辑任何配置文件。

此外，Harbor 还提供了几个很实用的高阶功能：

- **`harbor launch`**：把本地推理引擎直接接入 Codex、Claude Code、OpenCode 等编码工具，`harbor launch --backend ollama --model qwen3.5:4b codex` 一键搞定
- **Harbor Boost**：内置 agentic 工作流模块（web research、read-before-edit、deliverable audit），`harbor launch --workflow shipyard` 可编排编码 agent 的完整流程
- **`harbor qr` / `harbor url`**：打印二维码，手机上直接访问本地服务
- **`harbor tunnel`**：内置隧道，安全地暴露服务到外网
- **`harbor eject`**：想脱离 Harbor？把你的配置导出为标准 docker-compose.yml

## 为什么值得关注

Harbor 解决的是**本地 AI 最大的痛点 —— 配环境**。它让「搭一套本地 LLM 环境」从半小时的手动配置变成一条命令。

对开发者来说，这意味着：

1. **零门槛试错**：想试试 vLLM 比 Ollama 快多少？`harbor up vllm`，一秒切换
2. **编码工具链一键打通**：本地跑着模型，`harbor launch codex` 直接让编码 agent 用上本地推理
3. **完整的本地替代方案**：LLM + 搜索 + 语音 + 图片 + 工作流，全套本地部署，不依赖任何云服务
4. **配置可移植**：`harbor eject` 让你随时脱离 Harbor，既不 vendor lock-in 也不丢失已有环境

项目的活跃度也很健康 —— 作者 av 持续更新，社区在 Discord 上活跃，Wiki 文档非常完整。

## 简单示例

```bash
# 装 Harbor（macOS）
brew install av/harbor/harbor

# 一条命令拉起 Ollama + Open WebUI，所有服务预连好
harbor up ollama

# 再加个联网搜索
harbor up searxng

# 用本地模型跑 Codex
harbor launch --backend ollama --model qwen3.5:4b codex

# 想看看手机上能不能访问？
harbor qr
```

就这四步，你已经有一个完整的本地 AI 栈了 —— 能聊天、能联网搜索、能用编码 agent，全部在本地跑。

## 总结

Harbor 是当前最成熟的本地 LLM 一站式管理工具之一。如果你已经在用或者想尝试本地 AI，它是你工具箱里最值得加的那一个。项目在 GitHub 上开源，Python 编写，MIT 协议，社区活跃 —— [av/harbor](https://github.com/av/harbor) 值得一个 star。
