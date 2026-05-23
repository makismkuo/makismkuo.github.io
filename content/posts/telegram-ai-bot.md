---
title: "把 AI 塞进 Telegram：Bot 接入踩坑实录"
date: 2026-05-23
draft: false
tags: ["部署", "Telegram", "Bot"]
---

## 动机

每天打开 Telegram 的次数比打开微信还多。与其在浏览器和 Telegram 之间来回切换去用 AI，不如直接把 AI 搬到 Telegram 里。

想象一下：在群里 @ 一个 Bot，它直接回答你的问题。不用开网页、不用登录、不用切换 App。

这才是 AI 该有的样子——你感觉不到它的存在。

## 架构

```
你发消息 → Telegram → Bot → Hermes Gateway → AI 模型
                                               ↓
                                          回复发回来
```

## 部署遇到的坑

### 1. 服务器位置

Telegram API 在国内被墙得死死的。一开始我用国内服务器连，Bot 跟死了一样——消息发出去，10 分钟没反应。

换成 HK 服务器后，秒回。

**结论：Telegram Bot 必须跑在境外服务器上，没有例外。**

### 2. Webhook vs Polling

两种方式：Webhook（Telegram 主动推给你）和 Polling（你不断去问"有没有新消息"）。

Webhook 延迟低，适合部署在公网服务器上。Polling 适合本地开发测试。

我一开始用的 Polling，后来发现每次启动 Bot 都要等十几秒才连上。换了 Webhook 后——秒级响应。

### 3. Privacy Mode

默认情况下，Bot 在群聊里只能读到 @ 它的消息。如果想让 Bot 读取群里的所有对话，需要在 BotFather 里关闭 Privacy Mode。

第一次没关这个，Bot 像一个选择性失聪的人——你 @ 它才理你，旁边人说话它当听不见。

## 接入 AI

通过 sub2api，Bot 后面可以随时切换模型。今天用 DeepSeek，明天换 Claude，Bot 代码不用改一行。

## 目前用法

- 个人 AI 助手
- 交易机器人推送通知（开平仓实时提醒）
- 后续计划：接入更多自动化工作流

现在我在手机上就能调 AI 了。在地铁上问个问题，到家之前答案已经在了。
