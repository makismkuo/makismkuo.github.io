---
title: "sub2api：一个接口统一管理多个 AI 模型"
date: 2026-05-23
draft: false
tags: ["部署", "sub2api", "API"]
---

## 为什么需要 API 中转

做 AI 相关的开发，难免会遇到一个情况：不同的模型各自有独立的 API Key、独立的接口地址、独立的计费方式。OpenAI 一套、Claude 一套、DeepSeek 一套、本地模型又是一套。

每次写代码都要在代码里硬编码这些信息。换模型的时候，改代码、测试、部署，一个流程走下来小半天就没了。

sub2api 解决的就是这个问题。它是一个轻量级的 API 中转层，把所有模型的接口统一成一个地址。你的代码只需要配置一个 base_url 和一个 api_key，剩下的事情交给它处理。

## 架构

```
你的代码 → sub2api → 路由到具体模型
                     ├── OpenAI
                     ├── Claude
                     ├── DeepSeek
                     └── 其他
```

从代码的角度看，它永远只跟一个地址打交道。至于请求最终去了哪，那是不需要关心的事情。

## 配置

sub2api 的配置是一个 YAML 文件，里面定义各个模型的接入信息：

```yaml
models:
  gpt-4o:
    provider: openai
    api_key: sk-openai-xxx
  claude-sonnet-4:
    provider: anthropic
    api_key: sk-ant-xxx
  deepseek-chat:
    provider: deepseek
    api_key: sk-ds-xxx
```

每增加一个新模型，只需要在这里加几行配置。客户端代码不需要任何改动。

## 部署时遇到的几个问题

**第一个问题是模型名的一致性。** 配置里写的模型名，客户端调用时必须完全一致。我一开始配的是 `deepseek-chat`，客户端传的是 `deepseek`，结果返回 404。排查了好久才意识到是名字对不上。

**第二个是关于模型伪装。** sub2api 支持把模型改名，比如把 DeepSeek 的接口伪装成 GPT-4 的格式。有些做 API 转售的人会这么做。但我个人不建议这个做法——改名的模型在调试时很难排查问题，而且如果你的接口是对外的，这种行为也不够诚实。

**第三个是日志。** sub2api 会记录每次调用的详细信息，包括模型、token 数、耗时。这些日志在排查问题或者做用量统计时很有用。建议定期查看。

## 实际使用场景

我现在把 Telegram Bot 和 Hermes Agent 都接入了 sub2api。之前如果 DeepSeek 挂了，我得手动改客户端的 API 地址才能切换到 OpenAI。现在只需要在 sub2api 的配置里改一行，重启服务就行，对客户端来说完全无感。

如果只是自己用一两个模型，sub2api 的价值不大。但如果模型数量超过三个，或者你需要频繁切换模型，它能省下不少时间。
