---
title: "Axon：给你的代码库建一个知识图谱"
date: 2026-07-05
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "AI"]
---

## 一句话

`Axon` 把整个代码库索引成一个知识图谱——调用关系、类型依赖、执行流、耦合度、死代码一览无余。​不仅有个 Web UI 让你交互式浏览，还能通过 MCP 协议接入 AI 编码 Agent，让它不再是"盲人摸象"式地改代码。

## 为什么需要它

当你的 AI Agent（Claude Code、Cursor 等）准备修改 `UserService.validate()` 时，它并不知道有 47 个函数依赖这个返回值，3 条执行流经过它，`payment_handler.py` 和它在 git 历史里 80% 的情况下同时变化。

AI 编码助手面对的是"平面文本"。它们会 grep 找调用者，会漏掉间接依赖，而且上下文窗口有限，读不了整个调用链。LSP 给不出调用图，grep 返回的是字符串不是结构。

Axon 的解法很简单粗暴：**在索引阶段就预计算出代码结构**，之后 Agent 每次调用工具都能直接拿到完整上下文——一次调用搞定，不用反复搜索。

## 核心功能

**一键索引**——`pip install axoniq` 然后 `axon analyze .`，几秒钟就把代码库建成知识图谱。内置 tree-sitter 解析器支持 Python、TypeScript、JavaScript。

**交互式 Web UI**——`axon ui` 启动本地仪表盘（localhost:8420），包含力导向图可视化的 Explorer 视图、代码健康度的 Analysis 视图、Cypher 查询控制台。Cmd+K 搜索，符号点开就能看到调用链、影响半径、所属社区。

**MCP 集成**——这才是杀手锏。在项目配置里加上 Axon 的 MCP Server，AI Agent 就能直接调用 `axon_query`（混合搜索）、`axon_context`（符号全景）、`axon_impact`（影响半径分析）、`axon_dead_code`（死代码列表）等工具。每个工具返回值里还带"下一步提示"，引导 Agent 自然地进行深入调查。

**影响分析**——按深度分组：Depth 1 直接调用者（一定崩）、Depth 2 间接调用者（可能崩）、Depth 3+ 传递影响（建议评估）。每条边带置信度评分。

**死代码检测**——多轮扫描，能识别框架入口、装饰器、协议类、覆盖方法，不是简单的"零调用者"就报告。

**执行流追踪**——自动检测框架入口点（Flask/Express route、Click command、`test_*` 函数），BFS 遍历整个调用图输出执行流程。

**Git 耦合分析**——分析 6 个月的提交历史，找出静态分析发现不了的隐藏依赖。`user.py` 和 `auth_middleware.py` 总是一起改？Axon 会告诉你。

**零云依赖**——全部本地运行，解析、存储、嵌入、搜索都在本机，不需要 API key，数据不出机器。

## 上手体验

```bash
pip install axoniq
cd your-project
axon analyze .     # 索引
axon ui            # 打开 Web UI
```

配 AI Agent 也简单，在项目 `.mcp.json` 里加上：

```json
{
  "mcpServers": {
    "axon": {
      "command": "axon",
      "args": ["serve", "--watch"]
    }
  }
}
```

然后 Agent 就能用 `axon_impact("validate")` 一次查到所有受影响符号，按深度分组带置信度——不用反复 grep。

## 适合谁用

- **重度 AI 编码用户**——Claude Code、Cursor、Codex 的用户，想让 Agent 改代码时"知道自己在改什么"
- **大项目维护者**——代码库大到记不住所有调用关系，需要一个结构化的导航工具
- **做重构决策时**——改一个函数之前先看看影响半径，比出事后修复省太多时间
- **Code Review 辅助**——对比分支时看符号级差异，比看文本 diff 直观得多

## 总结

Axon 解决了 AI 编码领域一个真实且被忽视的问题：**Agent 对代码库结构没有感知**。它把 LSP、调用图、git 历史融合成一个知识图谱，以直观的 UI 和标准化的 MCP 工具暴露出来。

700+ GitHub Stars，MIT 许可，纯 Python 实现，一键安装——属于那种"用了就回不去"的工具。

> GitHub: [harshkedia177/axon](https://github.com/harshkedia177/axon)
> 安装: `pip install axoniq`
