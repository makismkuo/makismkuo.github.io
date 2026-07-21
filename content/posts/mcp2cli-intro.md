---
title: "mcp2cli：一个CLI通吃所有API，省掉99%的Token"
date: 2026-07-21
draft: false
tags: ["开源", "推荐", "GitHub"]
---

## 这是什么

开发者每天都在和API打交道 —— 从MCP服务器到OpenAPI文档到GraphQL端点。以往每次交互都需要写胶水代码、查文档、或者把冗长的schema灌进AI上下文里。

**mcp2cli** 彻底解决了这个问题：一个命令，把任何API变成终端CLI，零代码生成，运行时动态发现。

GitHub → [knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli) | Python | ⭐ 2305 | MIT 协议

## 核心功能

### 三合一模式
- **MCP 模式**：`mcp2cli --mcp https://mcp.example.com/sse` 直接连接MCP服务器，list / call tool
- **OpenAPI 模式**：`mcp2cli --spec ./openapi.json list-pets` 解析任意REST API
- **GraphQL 模式**：`mcp2cli --graphql https://api.example.com/graphql users --limit 10` — 自动发现query/mutation，生成selection set

### 最亮眼的设计：Bake 模式
```bash
mcp2cli bake create mygit --mcp-stdio "npx @mcp/github"
mcp2cli @mygit search-repos --query "rust"
```
保存连接配置后，用 `@name` 调用，再也不用每次都敲一遍 --spec / --auth-header。

### 实用细节
- **OAuth支持**：authorization code + PKCE 或 client credentials，token自动缓存刷新
- **Usage-Aware排序**：按调用频率/最近使用给工具列表排序，AI agent调用时减少无效选择
- **--json / --toon**：机器可读输出 + TOON编码（比JSON省40-60%token）
- **Secrets安全**：支持 `env:` / `file:` 前缀，防止敏感信息暴露在进程列表
- **缓存**：自动缓存spec，支持自定义TTL和强制刷新

### AI Agent Skill
mcp2cli 附带一个可安装的skill：`npx skills add knowsuchagency/mcp2cli --skill mcp2cli`，安装后Claude Code / Cursor / Codex等编码agent可以直接调用任意API，甚至从API自动生成skill文件。

## 为什么值得关注

用一句话概括：**它把API调用的心智成本压到了零。**

当前AI开发的趋势是Agent化 —— agent需要调用大量工具。但如果每个工具的schema都要塞进上下文，token消耗是天文数字。mcp2cli让agent只需发一个紧凑的CLI命令，而不是几百行JSON schema。作者声称可节省 **96-99%** 的tool schema token，放在LLM调用的单价下，这差异非常可观。

安装只需 `uv tool install mcp2cli`，不需要任何配置。对于自己常用的API场景，一次bake永久复用。对于开发团队，它也能替代Postman/Insomnia做轻量API调试。

## 快速上手

```bash
# 一行命令完成
uvx mcp2cli --mcp https://mcp.example.com/sse --list

# 或全局安装
uv tool install mcp2cli
mcp2cli --spec https://petstore3.swagger.io/api/v3/openapi.json --list

# 调个接口
mcp2cli --mcp-stdio "npx @modelcontextprotocol/server-filesystem /tmp" read-file --path /tmp/hello.txt
```

## 总结

mcp2cli 是那种"用过就回不去"的工具。它不是又一个API客户端，而是把API和CLI两个世界的鸿沟填平了 —— 对AI Agent来说是降本利器，对普通开发者是日常效率提升。2300+ stars 说明它已经在被大量使用，但离出圈还有距离，值得趁早用上。

**适合人群**：任何需要调API的开发者、正在搭建AI Agent系统的团队、MCP生态的深度用户。
