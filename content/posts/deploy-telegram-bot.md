---
title: "Telegram Bot 接入 AI 模型：从 API 到群聊"
date: 2026-05-23
draft: false
tags: ["部署", "Telegram", "Bot", "API"]
---

## 架构

```
用户 → Telegram → Bot → Hermes Gateway → AI 模型
                                         ↓
                                   回复发回用户
```

Telegram Bot 作为前端，通过 Hermes Gateway 调用 AI 模型。用户发消息，AI 回答，全程在 Telegram 里完成。

## 部署要点

### Bot Token

在 [@BotFather](https://t.me/BotFather) 创建 Bot，拿到 Token。

### 直连 vs 轮询

机器人跑在 HK 服务器上，**用 Webhook 直连**（不用 Polling），延迟更低。

### 模型对接

- 通过 sub2api 统一路由到 DeepSeek 等模型
- 支持流式输出（打字机效果）

## 用途

- 个人 AI 助手（日常问答）
- 交易机器人通知（开平仓实时推送）
- 以后可以扩展成客服、自动化工作流

## 坑

- 国内服务器连 Telegram API 不稳定，**HK 服务器是必须的**
- Bot 的 Privacy Mode 默认开启，群聊里要手动关闭才能读到所有消息
