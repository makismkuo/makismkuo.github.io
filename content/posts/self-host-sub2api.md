---
title: "sub2api：一个接口调所有 AI 模型，省心又省钱"
date: 2026-05-23
draft: false
tags: ["部署", "sub2api", "API"]
---

## 痛点

你有没有这种经历——钱包里揣着 OpenAI 的 Key，又买了 Claude 的额度，DeepSeek 便宜也得充点钱，最后手上有三四张 API Key，每次换模型还得改代码？

我忍了两个月，终于受不了了。

## sub2api 是干嘛的

简单说，它就是一个"API 路由器"。你只需要一个地址、一个 Key，它帮你把请求转发到真正的模型后面：

```
你的代码 → sub2api → 自动路由到 OpenAI / Claude / DeepSeek / 其他
```

## 部署

在 HK 服务器上跑了一个实例，配置文件里写好各个模型的 API Key 和地址，客户端统一指向 sub2api。

配置大概长这样：

```yaml
models:
  gpt-4o:
    provider: openai
    api_key: sk-xxx
  claude-sonnet:
    provider: anthropic
    api_key: sk-ant-xxx
  deepseek:
    provider: deepseek
    api_key: sk-ds-xxx
```

## 两个教训

**第一个：模型名要严格一致。** 客户端传 `deepseek-chat`，服务端配 `deepseek`，那就是 404。踩了半小时才发现——亏。

**第二个：不要搞品牌伪装。** 有人把 DeepSeek 改名成 GPT-4 去卖 API，我试了一下，后面排查问题完全是灾难。诚实地用实际模型名，你好我也好。

## 现在怎么用

Telegram Bot、Hermes Agent 都走 sub2api 统一出口。想换模型改一个配置文件就行，客户端代码不用动。

爽。
