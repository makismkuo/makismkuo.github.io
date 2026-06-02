---
title: "Agent Deck：统一管理你的AI编码助手"
date: 2026-06-02
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI工具"]
---

## 一个问题

Claude Code 在写前端、OpenCode 在修后端 Bug、Codex 在重构那个遗留模块——你的终端里同时跑着三四个 AI 编码会话。

然后你要切换看看进度。切到第一个，它在跑，没问题。切到第二个，它卡住了，等你输入。切到第三个，哦？已经跑完了？还是崩了？

这时候你意识到问题所在：**AI 编码助手越来越多，但管理它们的工具几乎没有。**

每个 AI 编码助手都有自己的终端窗口、自己的会话、自己的状态。你今天开了哪些会话？哪些还在跑、哪些在等你、哪些已经完了？全靠脑子记。项目一多，信息过载是必然的。

## Agent Deck 是什么

[Agent Deck](https://github.com/asheshgoplani/agent-deck) 是一个开源的终端 TUI 工具，为管理 AI 编码会话而生。你可以把它理解成 **htop for AI coding agents**——一个统一的指挥中心，让你在一个界面里看到所有 AI 编码助手的状态、切换会话、管理配置。

项目用 Go 语言编写，底层基于 tmux 和 Bubble Tea，目前 2587 星，MIT 协议开源。

## 核心功能

### 1. 统一的会话管理

Agent Deck 启动后，你会看到一个分组的会话列表。每个会话显示状态、名称、所属项目、运行时间。状态用带颜色的图标表示：

- **🟢 运行中**（绿色）—— Agent 正在工作
- **🟡 等待输入**（黄色）—— 需要你回应
- **⚪ 空闲**（灰色）—— 等你下指令
- **🔴 错误**（红色）—— 出问题了

按 `Enter` 可以直接 attach 到会话。按 `n` 新建会话。按 `d` 删除不再需要的会话。

### 2. Fork 会话

这是最实用的功能之一。你在 Claude Code 里跑了一个分析任务，但想同时尝试另一种处理方式——按 `f` 键 fork 当前会话。新会话继承完整的对话历史，互不干扰。可以 fork 再 fork，像 git 分支一样探索多个方向。

### 3. MCP 管理器

通常给一个会话添加 MCP 工具（比如 Web 搜索、浏览器自动化）需要编辑配置文件重启。Agent Deck 里按 `m` 打开 MCP 管理器，按空格切换开关，按 Tab 切换作用域（当前会话/全局）。MCP 定义一次，随时开闭。

### 4. 技能管理器

类似 MCP，Claude Skills 也可以通过 Agent Deck 统一管理。按 `s` 打开技能列表，选择需要的技能 attach 到当前会话，自动写入 `.claude/skills`。

### 5. Cost 追踪

对重度用户来说这是刚需。按 `$` 打开成本看板，查看今日、本周、本月所有 AI 编码会话的花费。支持 14 种主流模型的定价，按会话/按模型/按分组查看。还支持设置预算上限——达到阈值时自动告警。

## 为什么值得关注

**AI 编码工具爆发了，但生态位缺失了一块。** 每个人都在造更好的编码助手，但没人解决"同时用多个编码助手"的体验问题。Agent Deck 填补的就是这个空白。

几点理由：

1. **切合当下痛点**——用 AI 编码的人越来越多，同时跑两三个会话是常态。Agent Deck 解决的是真实需求。
2. **功能克制且完善**——没有堆砌功能。能做的事：管理会话、fork、MCP/技能管理、成本追踪。每项都做得比较扎实。
3. **你不一定需要它。** 如果你只用一个 AI 编码工具，一次只跑一个会话，那 Agent Deck 对你没用。但如果你像我一样，同时用两三个，它会成为 daily driver。

**另外值得提的一点**：项目有完整的中继功能（Conductor），可以接 Telegram/Slack/Discord 通知。当某个会话卡住等待输入时，通过手机直接收到通知并远程回复——适合把任务扔在服务器上跑，自己离线。

## 安装和上手

安装极其简单：

```bash
curl -fsSL https://raw.githubusercontent.com/asheshgoplani/agent-deck/main/install.sh | bash
```

或者 Homebrew：

```bash
brew install asheshgoplani/tap/agent-deck
```

装完直接运行：

```bash
agent-deck
```

TUI 启动后，按 `n` 新建一个会话：

```bash
# 在 TUI 里按 n，会提示输入项目目录和要使用的 agent
# 或者直接在 CLI 里添加
agent-deck add . -c claude
```

这会在当前目录启动一个新 Claude 会话，并自动出现在 Agent Deck 的会话列表中。

常用快捷键：

| 快捷键 | 作用 |
|--------|------|
| `Enter` | Attach 到会话 |
| `n` | 新建会话 |
| `f` / `F` | Fork（快速/自定义） |
| `m` | MCP 管理器 |
| `s` | Skills 管理器 |
| `$` | 成本看板 |
| `/` | 搜索会话 |
| `?` | 查看全部快捷键 |

## 不足与局限

客观说几个：

- **重度依赖 tmux**——如果你不用 tmux，Agent Deck 会替你装一个，但学习成本需要自己承担。不过作者提供了 socket 隔离，不会影响你现有的 tmux 配置。
- **主要支持 Claude**——虽然也支持 Gemini、OpenCode、Codex 等，但特性覆盖程度不一。Claude 用户受益最大。
- **功能太多**——版本迭代快，功能在快速增长，有些文档还没跟上。但核心功能已经稳定可用。

## 总结

Agent Deck 解决的是一个很具体的问题——"同时管好几个 AI 编码会话"。它的设计思路清晰：统一看板 + 快捷操作 + 配置管理。没有为了 AI 而 AI，纯粹是个做好本职工作的 TUI 工具。

如果你同时用多款 AI 编码工具，或者经常开着好几个 Claude/OpeCode 会话，值得一试。

项目地址：[github.com/asheshgoplani/agent-deck](https://github.com/asheshgoplani/agent-deck)
