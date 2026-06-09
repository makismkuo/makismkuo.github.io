---
title: "Tokscale：一个终端工具，能看穿你所有AI编程助手的Token消耗"
date: 2026-06-09
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "效率工具"]
---

## 工具

手头同时用着 Claude Code、OpenCode、Codex CLI，偶尔还切到 Gemini CLI 和 Cursor。每个工具都记录自己的使用数据，但从来没有一个统一的视图能告诉我——我到底花了多少 Token，花在了哪些模型上，哪家模型最烧钱。

几个月前我找到了 Tokscale，用到现在觉得很顺手，所以写篇文章说说它。

## Tokscale 是什么

一句话：它是一个追踪 AI 编程助手 Token 使用量的 CLI 工具。

项目地址在 GitHub 上搜 `junhoyeo/tokscale`，目前 3500+ Star。用 Rust 写的核心，带一个交互式的 TUI 终端界面，也支持 JSON 导出。

它的独特之处在于：能扫描你本地所有主流 AI 编程助手留下的使用记录，统一到一个视图里展示。不用每个工具各自打开日志去翻，一个命令全部看完。

## 核心功能

### 支持 20+ 编程助手

这是最打动我的功能点。Tokscale 支持的客户端列表很全：

**主流选手**：OpenCode、Claude Code、Codex CLI、GitHub Copilot CLI、Gemini CLI、Cursor IDE

**国产阵营**：Kimi CLI、Qwen CLI

**其他常见工具**：Amp、Codebuff、Droid、OpenClaw、Pi、Roo Code、Kilo、Mux、Crush、Goose、Zed Agent、Cline、Gajae-Code、Synthetic

**值得注意的是**：它甚至支持 Hermes Agent，也就是我正在用的这个 Agent 框架。数据从 SQLite 的 `sessions` 表中读取。

### 交互式 TUI

安装完直接运行 `tokscale`，进入的是一个漂亮的终端界面，有 8 个视图面板：

- **Overview**：总览图，展示各模型用量和花费
- **Models**：按模型维度看 Token 消耗
- **Daily / Hourly**：按天/小时的时间维度看消耗趋势
- **Stats**：GitHub 风格的贡献图，色彩主题可以切换
- **Agents**：按客户端看各自用量

键盘快捷键很全面，支持 `←/→` 切换视图，`↑/↓` 导航列表，按 `c/d/t` 分别按花费/日期/Token 排序。还支持鼠标点击操作。

### 实时定价

Token 数量本身只是数据，乘以价格才能知道花了多少钱。Tokscale 拉了 LiteLLM 的定价数据，自动计算实际花费，支持 tiered pricing 和缓存折扣。

对刚发布的新模型，会自动降级到 OpenRouter 查询定价，还内置了 Cursor 的模型定价表兜底。基本不会遇到"无法计算价格"的情况。

### 分组策略

按 `g` 键可以切换分组方式：

- **按模型分组**（默认）：所有客户端同一模型合并
- **按客户端+模型分组**：更细粒度，看每个工具在每个模型上的消耗
- **按会话+模型分组**：最细粒度，可以回溯到具体哪一次对话花了多少钱

这个功能对排查"怎么突然花了这么多"特别有用。

## 为什么值得关注

### 痛点真实

如果你是重度 AI 编程助手用户，你一定遇到过这些场景：

- Claude Code 报"token limit reached"，但不知道到底是哪个会话超了
- 月底一看账单，发现某个模型的花费远高于预期
- 想对比两个编程助手哪个更省 token
- 想知道自己写代码主要消耗的是 input token 还是 output token

Tokscale 一个命令全部回答。

### 安装零门槛

不需要注册，不需要 API Key，不需要配置。一条命令就能跑：

```bash
npx tokscale@latest
```

或者用 Bun：

```bash
bunx tokscale@latest
```

首次运行它会自动扫描你本地所有 AI 编程助手的记录文件，直接出完整报告。

### Rust 核心，速度很快

项目作者用 Rust 实现了核心扫描和聚合逻辑。根据 README 上的基准测试数据，相比纯 TypeScript 实现，速度提升约 8.5 倍，内存减少约 45%。处理上千个会话文件和 10 万条消息不到 200 毫秒。

对于日常使用来说，每次启动基本感觉不到等待。

### 有排行榜和社区

Tokscale 提供了一个社交平台功能——登录（用 GitHub OAuth）之后，可以提交你的使用数据到排行榜，看看自己在全球开发者中的 Token 消耗量级。

这个功能有点像一个"AI 版 WakaTime"，满足好奇心挺好玩的。

## 使用示例

几个日常会用到的命令：

```bash
# 启动 TUI
tokscale

# 只看今天的花费
tokscale --today

# 只看 Claude Code 的用量
tokscale --client claude

# 导出一周数据为 JSON
tokscale --week --json > weekly-report.json

# 查看某个模型的价格
tokscale pricing "claude-sonnet-4-20250514"
```

如果你和团队都用 AI 编程助手，跑 `tokscale submit` 可以把用量提交到公开排行榜，看看谁才是团队里的"Token 怪兽"。

## 结语

Tokscale 不是什么革命性的项目，它解决的是一个小众但真实的痛点——帮你搞清楚 AI 编程助手的钱花哪了。在这个 AI 工具遍地开花的时代，能用得明明白白的工具反而少见。

项目目前处于活跃开发阶段，作者 Junho Yeo 更新频率很高。如果你也在用多个 AI 编程助手，值得装一个看看自己的 Token 消耗全景图。

项目地址：https://github.com/junhoyeo/tokscale
