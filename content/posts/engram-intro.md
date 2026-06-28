---
title: "Engram：给AI编程助手一个不会失忆的大脑"
date: 2026-06-28T10:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
description: "Engram是一个Go编写的持久化记忆系统——让你的Claude Code、OpenCode、Gemini CLI等AI编程agent跨会话记住上下文，不再每次从头开始。单二进制，零依赖，支持MCP协议。"
---

## 项目简介

你的AI编程助手每次重启会话都会忘掉一切。这不是你的错——这是所有LLM会话的先天缺陷。**Engram**（⭐~4700）正是为了解决这个问题而生：一个Go编写的单二进制持久化记忆系统，让AI agent真正拥有"大脑"。

项目名字源自神经科学术语"engram"（记忆痕迹），寓意给AI留下物理层面的记忆轨迹。它通过 SQLite + FTS5 全文搜索存储在本地，同时暴露 CLI、HTTP API、MCP 服务器和交互式 TUI 四种访问方式——**任何支持 MCP 的 AI agent 都能直接接入**。

## 核心功能

Engram 最打动人的地方是它的简洁设计哲学：**一个二进制，一个 SQLite 文件，零外部依赖**。不需要 Node.js、不需要 Python、不需要 Docker。

亮点功能：

- **MCP 原生支持**：Claude Code 一行命令 `claude plugin marketplace add Gentleman-Programming/engram && claude plugin install engram` 即可接入，OpenCode、Gemini CLI 等同样简单
- **全场景覆盖**：支持 Claude Code、OpenCode、Gemini CLI、Codex、VS Code (Copilot)、Antigravity、Cursor、Windsurf、Kilo Code、Qwen Code 等十余种主流 AI agent
- **FTS5 全文搜索**：基于 SQLite FTS5，记忆不是简单的 KV 存储，而是可搜索的知识库
- **TUI 界面**：内置终端交互界面，可以浏览、搜索、管理记忆
- **零配置运行**：大多数 agent 下 Engram 作为短生命周期的 stdio 子进程自动启动，用户无需手动管理服务

## 为什么值得关注

如果你每天使用 AI 编程 agent 超过 30 分钟，Engram 能带来的体验提升是质变的。想象一下这些场景：

- Claude Code 在长对话中被 context window 截断后，能自动从 Engram 恢复关键项目上下文
- OpenCode 启动新会话时，直接加载之前 session 中记录的技术决策和架构约定
- 多个不同的 agent（Claude Code + Gemini CLI + Codex）共享同一个记忆库，协作时不再各自为政

这些不是画饼——Engram 通过 MCP 协议让 agent 读写 SQLite 数据库，所有记忆以结构化方式存储，agent 能通过自然语言查询和写入。

另一个加分项是它的"活跃度"。项目 2026 年 2 月创建，仅 4 个月就接近 5000 star。维护者将 Engram 作为"Gentleman Programming"生态的核心组件持续迭代，文档质量非常高——每个 agent 的接入指南、架构说明、团队协作方案都有专门文档。

## 简单示例

```bash
# macOS 安装
brew install gentleman-programming/tap/engram

# 接入 Claude Code（一行命令）
claude plugin marketplace add Gentleman-Programming/engram
claude plugin install engram

# 接入 OpenCode
engram setup opencode

# 接入 Gemini CLI
engram setup gemini-cli

# 查看 TUI 界面
engram tui
```

就这么简单。安装后你的 AI agent 会开始自动记录和检索记忆，跨会话持续工作。

对于需要 HTTP API 的场景（比如 OpenCode 的会话追踪插件），还可以启动服务模式：`engram serve`（默认端口 7437）。

## 总结

Engram 解决了一个真实且普遍的问题，用最轻量的方式实现。它不是又一个需要复杂配置的框架——一个二进制一条命令就能让你的 AI agent 拥有持久记忆。如果你在日常工作中重度使用 AI 编程助手，这个项目值得立刻尝试。

**GitHub**: [github.com/Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)  
**License**: MIT  | **语言**: Go  | **Star**: ~4700
