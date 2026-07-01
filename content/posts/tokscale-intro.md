---
title: "用 Tokscale 追踪你的 AI 编码代理 Token 消耗"
date: 2026-07-01T00:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
description: "Tokscale 是一个 Rust 编写的 CLI 工具，帮你追踪所有 AI 编码代理的 Token 使用量和花费，支持 Claude Code、Codex、Cursor 等 30+ 平台。"
---

![Tokscale Hero](/images/tokscale-hero.png)

如果你同时在用多个 AI 编码助手——Claude Code 写后端、Codex 改前端、Cursor 做重构——月底想知道自己到底花了多少钱，基本只能靠猜。

**Tokscale** 就是为了解决这个问题而生的。它是一个 Rust 编写的命令行工具，能自动扫描你本地所有 AI 编码代理的使用记录，汇总成一份清晰的 Token 和费用报告。项目地址：[github.com/junhoyeo/tokscale](https://github.com/junhoyeo/tokscale)，当前 ⭐4k。

### 核心功能

Tokscale 的核心能力就一句话：**找到你机器上所有 AI 代理的本地数据，解析、汇总、展示**。

它目前支持 **30+ 个客户端**，包括：Claude Code、OpenCode、Codex CLI、Copilot CLI、Cursor IDE、Gemini CLI、Qwen CLI、Kimi CLI、Hermes Agent、Zed Agent、Roo Code、Goose、Pi、Codebuff、Amp、Antigravity、Warp/Oz、Grok Build 等等。几乎覆盖了市面上所有主流的 AI 编码工具。

安装即用，一行命令启动漂亮的全屏 TUI：

```bash
npx tokscale@latest
```

界面包含 8 个视图：总览（图表+Top 模型）、模型排行、日/时/分钟粒度的消耗趋势、贡献热度图、Agent 对比。输入输出缓存推理四种 Token 分开统计，价格实时从 LiteLLM 获取，新模型自动回退到 OpenRouter 查价。

除了 TUI，它也支持 `--json` 输出，方便集成到自己的监控脚本或 CI 流程。

### 为什么值得关注

AI 编码代理正在从"偶尔用用"变成"日常主力工具"，但对应的成本追踪却几乎没有像样的工具。Claude Code 的账单在 Anthropic Console 里，Codex 的去 OpenAI，Cursor 的单独计费——各自为政，没有统一视图。

Tokscale 填补了这个空白。它**不依赖任何 API 调用**，纯本地扫描 JSONL 和 SQLite 文件，隐私安全；Rust 核心带来极快的解析速度；而且作者几乎每周都在更新，社区活跃。

另一个细节：它内置了 **session 留存提醒**——Claude Code 默认 30 天清理历史记录，Tokscale 会提示你关闭清理以保持数据完整，这比踩坑了才发现要友好得多。

### 快速上手

```bash
# 直接运行（自动扫描所有已安装的客户端）
npx tokscale@latest

# 只看本周 Claude Code 的花费
npx tokscale@latest --week --client claude

# 导出 JSON 给其他工具
npx tokscale@latest models --json > report.json

# 查看某个模型当前定价
npx tokscale@latest pricing "claude-sonnet-4-20250514"
```

TUI 快捷键也很顺手：`←/→` 切换视图、`c/d/t` 按花费/日期/Token 排序、`p` 切换 9 种配色主题、`e` 导出 JSON。

### 总结

如果你每天都在用 AI 编码工具，Tokscale 是一个"早知道就好"的工具——它让你不再对自己的 Token 消耗两眼一抹黑。开源、Rust 写、支持 30+ 平台、有漂亮 TUI，值得放进你的开发者工具箱。

[GitHub: junhoyeo/tokscale](https://github.com/junhoyeo/tokscale)
