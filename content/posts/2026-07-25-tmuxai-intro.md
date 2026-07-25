---
title: "TmuxAI：你的 tmux 里住了一个 AI 结对程序员"
date: 2026-07-25
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "AI工具"]
description: "TmuxAI 是直接嵌入 tmux 会话的 AI 终端助手——它能观察你所有窗格的内容、理解上下文、自动执行命令，就像一个坐在你旁边看屏幕的结对程序员。"
---

## 项目简介

大多数 AI 终端助手要求你**跳出**当前环境——粘贴代码到聊天框、切换到另一个 TUI、或者按特定格式输入命令。[TmuxAI](https://github.com/alvinunreal/tmuxai)（⭐1909）走了另一条路：它直接嵌入 tmux 窗口，观察你所有窗格正在显示的内容，理解上下文，然后用一个专用的 Chat Pane 和你对话、在 Exec Pane 执行命令。你不用改变任何工作流。

它的设计灵感来自真人结对编程：一个同事坐在你旁边，看着你的屏幕，理解场景，然后帮忙。TmuxAI 把这个模式自动化了。

## 核心功能

**Observe Mode（默认模式）。** 你在 Chat Pane 里说话，TmuxAI 自动读取当前 tmux 窗口所有可见窗格的内容——运行中的命令、输出、shell 类型、操作系统。AI 回复后，如果建议执行某条命令，它会在 Exec Pane 执行，等待几秒，捕捉新输出，继续处理。你可以用空格/回车控制等待倒计时，随时介入。整个过程不需要离开 tmux。

**Prepare Mode。** 如果你需要更精准的命令追踪，`/prepare` 命令会自定义你的 shell 提示符（支持 bash/zsh/fish），加入特殊标记。这样 TmuxAI 能精确知道命令何时结束、退出码是什么，不再需要固定等待时间——按需等待，更快也更准。

**Watch Mode。** 这是最"主动"的模式。开启后 TmuxAI 会**持续观察**你在 Exec Pane 敲的命令，自动分析是否有更好的替代方案。比如你写了一个复杂的 `awk` 管道，它会建议 `jq` 的方案；你手动 `grep | cut | sort` 组合，它会推荐更简洁的写法。像有一个 senior 在旁边瞟了一眼你的终端然后说"其实你这个用一行 X 就行"。

**Knowledge Base & Skills。** 支持自定义知识库（加载特定目录的文档到上下文）和 Skills（预定义提示词模板，比如"解释这段代码"、"帮我 review"）。可以用 `/kb` 和 `/skill` 在会话中切换。Skills 还支持 auto-match 功能——根据当前窗口内容自动激活相关 skill。

**多模型 + MCP 支持。** 配置文件中可以定义多个模型（OpenAI、OpenRouter、Azure、Requesty 等），运行时用 `/model` 切换。同时支持 MCP Server 工具扩展，这意味着你可以给 TmuxAI 挂上自定义的工具（数据库查询、API 调用等）。

## 为什么值得关注

现有的 CLI AI 工具有两类：一类是"问答型"，你在终端里打字问 AI，它回答（像 `yai`、`shell_gpt`）；另一类是"编码 Agent"，接管文件系统自己干活（像 Claude Code、Codex）。TmuxAI 卡在中间，找到了一个很独特的定位——**它不接管你的工作，但看着你工作，随时能帮忙。**

这个定位的优势非常实际：

1. **零切换成本**。你不需要离开 tmux、不需要粘贴代码。AI 看到的就是你看到的，上下文自动生效。
2. **适用于所有终端工作**。不只是写代码——排查服务器问题、调试数据库、操作 Kubernetes、分析日志文件，全都能用。
3. **观察 + 建议**的模式比"替你写"更安全。AI 建议命令，你审阅后确认执行，它再读结果。你始终在控制回路里。

用 Go 编写，单二进制安装（`curl -fsSL https://get.tmuxai.dev | bash`），macOS 和 Linux 都支持。

## 快速上手

```bash
# 安装
curl -fsSL https://get.tmuxai.dev | bash

# 配置 ~/.config/tmuxai/config.yaml
mkdir -p ~/.config/tmuxai
# 写入：一个模型配置（OpenRouter / OpenAI / Requesty）

# 在 tmux 会话中启动
tmuxai
```

然后就进入 Chat Pane，可以直接问问题。所有窗格的内容自动成为上下文。

## 总结

TmuxAI 不是一个"AI 写代码"的工具——它是一种**终端协作方式**。它用 tmux 原生的窗格模型，实现了一个观察-建议-执行的 AI 协作循环。如果你已经在 tmux 里工作，这是目前最自然的 AI 集成方式。

项目地址：[github.com/alvinunreal/tmuxai](https://github.com/alvinunreal/tmuxai)
