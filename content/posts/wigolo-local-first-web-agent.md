---
title: "wigolo：给你的 AI Agent 装上免费、本地的 Web 大脑"
date: 2026-07-23
draft: false
tags: ["开源", "推荐", "GitHub"]
---

## 项目简介

AI 编码助手已经很强了，但它们有一个共同的短板：查东西得靠第三方 API。每次 `search`、`fetch`、`crawl` 背后都是计费请求，跑多几次账单就上去了。**wigolo** 正是来填这个坑的——一个**本地优先、不依赖云服务**的 Web 智能层，让 AI Agent 自己就能完成搜索、抓取、提取、研究，且每查询 $0。

项目由 KnockOutEZ 开发，2026 年 4 月发布，至今已收获 3400+ Star。用一句话概括：**把付费 Web 搜索 API 的全部能力，装进你本地的 npx 命令里。**

## 核心功能

wigolo 通过 MCP（Model Context Protocol）暴露了 10 个工具：

- **search** — 融合 18 个搜索引擎的并行多引擎搜索，自带 ML 重排名和可解释评分
- **fetch** — 智能渲染网页：纯 HTTP → 无头浏览器自动升级，反爬自动处理
- **crawl** — 全站抓取：BFS/DFS/Sitemap 模式，支持 robots.txt
- **extract** — 结构化抽取：表格、json-ld、Schema.org 等
- **research** — 自动分解问题 → 并行检索 → 合成带引用的报告
- **agent** — 自主收集循环：计划 → 搜索 → 抓取 → 合成
- 以及 cache、find_similar、diff、watch 等辅助工具

接入方式也很灵活：可以作为 MCP Server 挂到 Claude Code/Cursor/Codex 里，也可以 REST API 自托管，或者通过官方 SDK（TypeScript/Python）嵌入自己的应用。

## 为什么值得关注

**它解决了一个真痛点。** 用过 Tavily、Exa、Firecrawl 的开发者都知道，这些服务按查询计费，而 Agent 调用 API 的频率远高于人工——一次 research 任务轻松跑几十个请求，账单肉眼可见地涨。wigolo 把所有处理放在本机：搜索通过公共搜索引擎的直连适配器，reranker 和 embedding 跑在本地模型上，结果缓存到 `~/.wigolo/`。没有 API key，没有计费，反复查同样问题零成本。

更关键的是它**对 Agent 友好**。每条搜索结果都带逐字节偏移的原文引用、可解释的评分分解、失败引擎的标记。Agent 拿到的不只是结果，而是足以自己做判断的证据链。

对比表格也很清晰：

| 特性 | wigolo | Firecrawl / Exa / Tavily |
|---|---|---|
| API Key | 不需要 | 需要 |
| 单次查询成本 | $0 | 计费 |
| 本地缓存+离线 | ✅ | ❌ |
| 数据不出本机 | ✅ | ❌ |

## 快速上手

安装只需要 Node ≥20 和一个命令：

```bash
npx wigolo init                     # 初始化本地引擎 + 浏览器 + 模型
npx wigolo init --agents=claude-code  # 顺便配好 Claude Code 的 MCP
```

初始化后就可以直接在聊天里用。如果要让 research 工具生成更完整的中文报告，加一个免费的 Gemini key：

```bash
export WIGOLO_LLM_PROVIDER=gemini
export GEMINI_API_KEY=<你的免费key>
```

健康检查也很简单：`wigolo doctor`。

## 总结

wigolo 是那种**装上就回不去**的工具——它把付费 Web 搜索 API 等价的能力变成零成本的本地服务，而且数据不出设备，稳定可靠。对于重度使用 AI Agent 的开发者，这相当于一年省下几百甚至上千美元的 API 费用，同时获得更透明的结果和更快的响应速度。

项目目前处于公开 Beta，但核心功能已经稳定（7600+ 测试用例）。它不会变成付费产品——AGPL 许可证和作者的公开承诺都确保了这一点。无论你是 Claude Code 的重度用户，还是自己搭建 Agent 框架，wigolo 都值得一试。

GitHub: [KnockOutEZ/wigolo](https://github.com/KnockOutEZ/wigolo)
