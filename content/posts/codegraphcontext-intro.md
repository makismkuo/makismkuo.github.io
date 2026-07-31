---
title: "CodeGraphContext：把你的代码变成 AI 可查询的知识图谱"
date: 2026-07-31
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "AI"]
---

AI 编程助手越用越顺手，但有一个痛始终没解决：**它不懂你的项目结构**。你丢一个文件过去它知道里面有什么，但"这个函数谁调了""这个类继承链有多长"——它两眼一抹黑。把整个仓库塞进 context 也不是办法。

**CodeGraphContext**（CGC）就是来填这个坑的。一个开源 CLI + MCP 服务器，把你的代码索引成知识图谱，让 AI 助手能像读项目结构图谱一样理解你的代码库。

## 核心功能

CGC 的工作原理很直接：用 Tree-sitter 解析源码，提取函数、类、继承、调用、导入等关系，存入图数据库，然后通过 CLI 或 MCP 接口查询。

- **支持 23 种语言**：Python、JS/TS、Rust、Go、Java、C++ 全覆盖，每种语言都能提取调用链、类层次、导入关系
- **双模式**：CLI 工具直接查（`cgc analyze callers my_func`），或者启动 MCP Server 让 AI 助手自动调用
- **多种图数据库后端**：默认使用嵌入式 FalkorDB Lite（零配置），也支持 KuzuDB、Neo4j 甚至远程集群
- **Live 文件监控**：`cgc watch` 实时跟踪文件变化，自动更新图谱
- **预索引包**：可以直接加载知名开源项目的 `.cgc` 包，免去索引等待
- **交互可视化**：生成漂亮的暗色 HTML 知识图谱，节点可点、可搜索、可展开

## 为什么值得关注

市面上已经有不少"代码上下文"工具（repomix、llmctx、gitingest），但它们做的是**线性拼接**——把文件文字串起来。CGC 做的是**结构建模**——它保留调用关系、继承层次、模块边界这些 grep 永远找不出来的信息。

举个例子：你想知道 `main()` 的完整调用链跨越了多少个文件。grep 只能告诉你"这里出现了"，CGC 直接给你一张调用图，从入口到叶子路径一目了然。在 AI 助手那边，这意味着模型不再靠猜测回答"这个函数的副作用是什么"——它可以切实查到。

项目用 Python 写，pip 一键安装，Docker 也能跑不装 Python。作者 Shashank Shekhar Singh 维护积极，社区有 Discord。

## 简单上手

```bash
# 安装
pip install codegraphcontext

# 索引当前目录
cgc index .

# 查函数调用者
cgc analyze callers main

# 查死代码
cgc analyze dead-code

# 启动 MCP Server，连进你的 AI IDE
cgc mcp start
```

连进 Cursor / VS Code / Claude 之后，你可以在 AI chat 里直接问："`AuthManager` 类依赖了哪些模块？"或者"帮我找出所有没有被调用的函数"——这些过去要靠翻代码或者写脚本才能回答的问题，现在一句话搞定。

## 总结

在 AI 编码这一波浪潮里，"给 AI 正确的上下文"比"用更贵的模型"重要得多。CodeGraphContext 从代码结构的角度解决了这个问题，而且做得足够轻量——`pip install` 就能用，不需要部署额外服务。如果你的日常开发已经离不开 AI 助手，这个工具值得花 10 分钟装上试试。

GitHub：[CodeGraphContext/CodeGraphContext](https://github.com/CodeGraphContext/CodeGraphContext)（⭐4k+，MIT 协议）
