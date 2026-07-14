---
title: "CLI Printing Press：一个会给任何API造CLI的工具"
date: 2026-07-14
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "AI工具"]
description: "CLI Printing Press 能自动分析任何API（甚至没有文档的网站），生成Go语言CLI + MCP服务器，还内置SQLite本地数据层和Agent原生输出。"
---

## 项目简介

[CLI Printing Press](https://github.com/mvanhorn/cli-printing-press) 是一个元工具（meta-tool）——它不是给你用的某个CLI，而是帮你**造**CLI的工具。你给它一个API（OpenAPI 规范、一个URL、甚至一个HAR抓包文件），它先做竞争对手分析、再琢磨这个API的"非显而易见价值"（Non-Obvious Insight）、然后自动生成一个完整可用的 Go CLI 加上一个 MCP Server。当前 ⭐3957。

## 核心功能

**解读任意API。** 有 OpenAPI 规范最好——直接喂进去。没有？给一个网站的URL，它会启动浏览器、抓取流量、反向工程出API结构，然后基于这个结构生成CLI。ESPN 这种完全没有公开API的网站都能整出一个 `espn-pp-cli`。

**吸收 + 超越。** 生成之前，系统会扫描已有的 Claude Code 插件、MCP 服务器、社区CLI，列出竞争对手的所有功能——然后确保自己的CLI覆盖所有功能 + 加上 SQLite 本地存储、离线搜索、FTS5全文索引。数据存在本地之后，"冷门工单"、"团队健康度"、"瓶颈分析"这类跨资源查询就自然实现了。

**双接口。** 一次生成产出两个二进制文件：`<api>-pp-cli`（Cobra CLI）和 `<api>-pp-mcp`（MCP Server）。终端Agent用CLI，IDE Agent 用 MCP，共享同一个 `internal/client` 和 `internal/store`，零代码重复。

**Agent原生设计。** 每条命令都有 `--json`、`--select`、`--compact`、`--dry-run` 等标志。管道模式自动 JSON 输出，不需要 `--json` 参数。退出码有7种类型（0=成功、3=未找到、4=认证失败、5=API错误、7=限流），Agent 可以不解析错误文本就直接重试。`--compact` 模式只返回核心字段，减少 60-80% token 消耗。

## 为什么值得关注

这个项目背后有一个很聪明的观察：**好的CLI不是端点包装器，而是领域洞察的载体。**

以 Discord 为例——它有300多个API端点，但 Peter Steinberger 写的 [discrawl](https://github.com/steipete/discrawl) 只提供了11条命令（sync、search、sql、tail、mentions、members），却拿了583颗星。为什么？因为它理解了"Discord 不只是个聊天工具，它是可搜索的知识库"——每条消息都是机构记忆。11条精心设计的命令比300个端点包装器有用得多。

CLI Printing Press 把这个思考过程自动化了。Phase 0 先定义这个API的 Non-Obvious Insight（比如"Stripe 不只是支付处理器，它是业务健康监视器"）。然后生成的CLI就不会只是 CRUD 包装器，而会有 `health`、`reconcile`、`stale`、`orphans` 这类有业务意义的命令。

## 简单示例

安装后，在 Claude Code 里直接用 Slash Command：

```bash
# 为 Notion 生成 CLI + MCP Server
/printing-press Notion

# 为某个网站生成（无API、无文档）
/printing-press https://example.com

# 重新生成已发布的 CLI
/printing-press-reprint notion
```

也可以直接使用 CLI 二进制：

```bash
# 搜索一家俱乐部的信息
espn-pp-cli search "Los Angeles Lakers"

# 查找超过30天无人维护的工单
linear-pp-cli stale --days 30
```

输出经过设计的退出码让 AI Agent 自动纠错，不需要解析自然语言错误消息。

## 总结

CLI Printing Press 的角度很独特——它不是又一个 CLI 工具，而是一个 CLI 生成工厂。对于 API 平台方（想给自己的 API 做一个高质量 CLI）、Agent 开发者（需要更好的工具来操作外部服务）、或者对 Agent 工作流有追求的个人来说，这个项目提供了从 API 到完整 CLI+MCP 的一站式方案。Go 编写，安装简单，产出质量经过机械化的 Shipcheck 验证。值得一试。

```bash
curl -fsSL https://raw.githubusercontent.com/mvanhorn/cli-printing-press/main/scripts/install.sh | bash
```
