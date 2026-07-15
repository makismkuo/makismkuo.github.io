---
title: "pydantic-deep-agents：能"平行宇宙"式分叉的终端AI助手，Claude Code的Python开源替代"
date: 2026-07-15T00:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "AI工具", "Python"]
---

## 项目简介

[pydantic-deep-agents](https://github.com/vstorm-co/pydantic-deepagents)（简称 pydantic-deep）是一个开源的终端 AI 助手 + Python 框架，定位明确：**你可以在自己的机器上，用任何模型（Claude、GPT、Gemini、本地模型），跑一个功能几乎对标 Claude Code 的 AI 编程助手**。

项目当前 973 星，MIT 协议，活跃维护中（最近一次更新就在昨天）。它名字有点长，但做的事情非常清晰——一个仓库，给你两样东西：

1. **终端 TUI 助手**：`curl` 一行安装，然后 `pydantic-deep` 启动一个交互式终端，像 Claude Code 一样规划、编辑文件、跑命令、搜索网页、分叉子代理。
2. **Python 框架**：同一个代码库暴露 `create_deep_agent()` 函数，让你在自己的 Python 应用里嵌入一个全功能自主代理——自带文件系统、Shell、规划、记忆、沙箱执行、MCP 支持。

## 核心功能

### ⑂ Live Run Forking（独家杀招）

这是 pydantic-deep 最亮眼的功能，**没有任何其他工具做得到**。

传统 AI 代理遇到"方案 A 还是方案 B"的抉择时，只能赌一条路。pydantic-deep 的 Live Run Forking 让它**全都要**：一次 `agent.run()` 在执行中遇到分叉点，自动分裂成 N 个完全隔离的并行分支，每个分支有独立的**写时复制文件系统**（文件读取共享，写入隔离）、各自的 steering message 和预算上限。所有分支并行执行，最后由一个 **AI 裁判**（或测试结果、或手动选择）选出优胜者，合并回主流程。

用法简单到离谱：

```python
agent = create_deep_agent(model="anthropic:claude-sonnet-4-6", forking=True)
```

终端里更直观：

```
/fork                    # 分裂当前会话
>>A 用装饰器实现         # 分支 A
>>B 用上下文管理器实现    # 分支 B
/merge                   # AI 裁判自动裁决
```

对于代码重构、技术选型这类场景，这功能简直是"后悔药"——不用反复重试，让 AI 自己并行探索最优解。

### 🧠 完整的代理基础设施

除了 Forking，pydantic-deep 提供了生产级 AI 代理所需的一切：

- **工具调用**：文件读写、Shell执行、web搜索/抓取、浏览器自动化（Playwright）
- **多代理/群组**：可以派生子代理并行工作，有共享 TODO 列表和消息总线
- **持久记忆**：跨会话的 MEMORY.md，自动注入 system prompt
- **无限制上下文**：自动摘要压缩，永远不会撞到上下文墙
- **Docker 沙箱**：隔离执行环境，项目目录挂载为 /workspace
- **检查点**：随时保存状态、回退、分叉探索不同路径
- **技能系统**：可复用的 YAML 技能模板

### 🔌 全模型兼容 + MCP 协议支持

框架基于 Pydantic AI 构建，支持 Anthropic、OpenAI、Gemini、Ollama（本地模型）作为后端。同时原生支持 **MCP（Model Context Protocol）**，可以连接 GitHub、Figma、自定义 MCP 服务器——也就是说，你可以直接把 Claude Code 的 MCP 配置搬过来用。

## 为什么值得关注

当前 AI 编程工具市场有个尴尬：**好用的不开源（Claude Code），开源的功能不全（Aider、LangGraph 等）**。pydantic-deep 是第一个在功能完整度上真正接近 Claude Code 的开源替代方案，而且有两项独特优势：

1. **模型自由**——不绑定 Anthropic，你选什么模型它就用什么。本地模型也行，省钱又隐私。
2. **Live Run Forking**——这是 Claude Code 做不到的，Aider 做不到的，LangGraph 和 CrewAI 也做不到的独特能力。当你的代理在"用装饰器还是上下文管理器"之间犹豫时，它能全试一遍再选最优。

同时它也是**终端助手 + Python 框架**二合一。你可以先用终端体验，然后 `pip install pydantic-deep` 在自己应用里 `create_deep_agent()` 嵌入代理能力——同一个 API，两种用法。

安装简单到令人发指：

```bash
# 终端助手（一行命令，自动装 uv + CLI）
curl -fsSL https://raw.githubusercontent.com/vstorm-co/pydantic-deep/main/install.sh | bash
pydantic-deep

# 或者作为框架
pip install pydantic-deep
```

## 简单示例

```python
from pydantic_deep import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    forking=True,  # 启用并行分叉能力
)

result = await agent.run("""
重构这个 Flask 认证模块：
- 提取 UserService 类
- 添加 JWT 支持
- 写单元测试
""")
```

终端 TUI 模式下的体验类似 Claude Code——全屏、流式输出、文件 diff、工具调用面板，一行安装即刻拥有。

## 总结

pydantic-deep-agents 是 2026 年 AI 开发工具领域最被低估的开源项目之一。它用 973 星就做到了一件事：**给你一个完全开源、模型自由、还附带独家"平行宇宙"分叉能力的 Claude Code 替代品**。

如果你在用或者想用 AI 编程助手，又不想被锁定在某个模型或平台上——这就是你要找的那个。安装两分钟，体验两小时，之后你会奇怪为什么这么强的项目只有不到一千星。

**项目地址**：https://github.com/vstorm-co/pydantic-deepagents
**文档**：https://vstorm-co.github.io/pydantic-deepagents/
