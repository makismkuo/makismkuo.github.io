---
title: "Tokscale：用Rust TUI跟踪你的AI编码Token消耗"
date: 2026-07-11
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "AI工具"]
description: "Tokscale 是一个开源的 CLI+TUI 工具，集中追踪 40+ AI 编程助手的 Token 使用和费用。支持 OpenCode、Claude Code、Codex、Hermes Agent、Gemini CLI 等。安装即用，附带全球排行榜。"
---

AI 编码助手越来越多：OpenCode、Claude Code、Codex、Hermes Agent、Gemini CLI、Cursor……每个都有自己的 token 计费逻辑，月底对账全靠感觉。有没有一个工具能把所有 agent 的用量统一看到？**Tokscale** 就是答案。

## 项目简介

Tokscale 由韩国开发者 Junho Yeo 创建，是一个用 **Rust + Ratatui** 构建的跨平台 CLI 工具，专门用来聚合和可视化你在 40+ AI 编程代理上的 token 消耗和费用。项目已在 GitHub 获得 4300+ Star，MIT 开源协议。

安装简单到令人发指：一行命令即可启动完整的交互式 TUI。

```bash
npx tokscale@latest
```

## 核心功能

- **40+ agent 全覆盖** — 从 OpenCode、Claude Code、Codex、Hermes Agent、Gemini CLI、Cursor、Copilot CLI 到 Kimi、Qwen、Pi、Roo Code、Cline、Goose……几乎你能想到的 AI 编程工具都支持
- **交互式 TUI** — 8 个视图标签页：总览、模型、每日、每小时、统计、Agent 等；支持键盘导航、鼠标点击、颜色主题切换
- **实时定价** — 通过 LiteLLM 获取最新模型定价，支持 OpenAI、Anthropic、OpenRouter 等多源。输入/输出/缓存读/缓存写/推理 token 明细悉数呈现
- **GitHub 风格贡献图** — 2D/3D 可视化，自定义颜色主题，一眼看出你的编码强度
- **全局排行榜** — 提交你的用量数据，和全球开发者一较高下
- **原生 Rust 核心** — 比纯 JS 方案快 10 倍

## 为什么值得关注

开发者切身的痛点往往催生最好的工具。Tokscale 解决的问题非常具体：**多个 AI agent 的 token 用量分散在不同目录、不同格式里，人工对账痛苦不堪**。它自动扫描 `~/.claude/`、`~/.codex/`、`~/.hermes/` 等路径，解析各种 JSONL/SQLite 格式，统一成一个界面。

特别值得一提的是它对 **Hermes Agent** 的原生支持 — 直接从 `$HERMES_HOME/state.db` 读取 session 级用量数据，连多 profile 场景也覆盖到了。如果你同时使用多个 AI 编码工具，Tokscale 基本是必装品。

## 用法一览

```bash
# 启动 TUI（默认）
tokscale

# 只看今日用量
tokscale --today

# JSON 输出，供脚本消费
tokscale models --json

# 只看特定 agent
tokscale --client claude,codex
```

## 总结

Tokscale 是 AI 编程时代的一个基础设施级工具。它的定位精准——解决多 agent 用户的真实痛点——且实现质量极高（Rust 核心、美观 TUI、活跃维护）。如果你日常使用 2 个以上的 AI 编程助手，Tokscale 会让你的用量管理从「靠猜」变成「靠看」。

**GitHub**: [github.com/junhoyeo/tokscale](https://github.com/junhoyeo/tokscale)
**安装**: `npx tokscale@latest`
