---
title: "abtop：像 htop 监控系统一样监控你的 AI 编码代理"
date: 2026-06-08
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
---

如果你同时跑几个 AI 编码代理（Claude Code、Codex CLI、OpenCode）在干活，大概率遇到过这样的情况：

- 某个代理是不是卡住了？context 窗口满没满？
- 速率限制是不是快到了？
- 哪个 session 开了哪个端口？有没有孤儿进程没清理？
- 这些代理之间，哪个的任务进度最快？

逐一打开终端窗口去看，效率很低。如果能像 `htop` 一样，开一个 TUI 把所有信息汇总到一块，一屏看完就好了。

**abtop** 就是干这个的。

## abtop 是什么

abtop 是一个终端 TUI 工具，定位是"AI 编码代理的任务管理器"。灵感来自系统监控工具 btop/htop——只不过它监控的不是 CPU 和内存，而是 Claude Code、Codex CLI 和 OpenCode 的运行状态。

项目地址：[github.com/graykode/abtop](https://github.com/graykode/abtop)，目前 2500+ Star，Rust 编写，MIT 协议。

## 核心功能

abtop 从本地进程和文件状态中发现正在运行的代理 session，不做任何网络请求，不需要 API Key，也不需要认证——纯本地只读。

它展示的信息包括：

- **session 发现**：自动检测当前在跑的 Claude Code、Codex CLI、OpenCode 会话
- **token 用量**：实时显示 token 消耗和速率限制余量
- **context 窗口百分比**：直观的进度条，告诉你 context 还剩多少，附带警告
- **子代理树**：展开查看 agent 衍生的子进程和子任务
- **端口检测**：哪个 agent 起了哪些端口，帮你发现遗忘的孤儿端口
- **Git 状态**：当前工作的 Git 分支、是否有未提交修改
- **当前任务描述**：各个代理正在执行的提示词摘要
- **内存状态**：session 的内存占用

支持多 profile——即使你在不同的目录用了多个 Claude Code 配置，它也能一并发现并展示。

## 为什么值得关注

### 痛点确实存在

AI 编码代理越来越强大，但管理它们的体验还停留在石器时代。用 AI 代理就像请了一群外包程序员同时干活——你只能敲敲键盘问"你干嘛呢"，它们各自回答。abtop 相当于给了你一个"管理后台"，一屏总览全局。

对于同时使用多个代理的开发者来说，这个工具直击了一个真实且频繁遇到的痛点。

### 本地只读，安全可控

不调用任何外部 API，不发送任何数据，纯粹从文件系统和进程表读取信息。这意味着即使你在企业内部环境使用，也没有任何合规风险。

### 超预期的细节

abtop 在一些细节上做得很用心：

- **主题系统**：内置 12 个 TUI 主题，包括 4 个色盲友好主题，`t` 键循环切换
- **tmux 集成**：按 Enter 可以直接跳到对应代理的 tmux pane，不用手动切窗口
- **中文支持**：设置 `language = "zh"` 即可切换中文界面，对中文用户友好
- **一次快照模式**：`abtop --once` 打印当前状态然后退出，适合 CI 或脚本集成
- **配置过滤**：可以隐藏不用的 agent 类型，比如只显示 Claude Code

## 安装和使用

安装很简单，一行命令：

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/graykode/abtop/releases/latest/download/abtop-installer.sh | sh
```

或者用 Cargo：

```bash
cargo install abtop
```

使用上几乎没有学习成本：

```bash
abtop           # 启动 TUI
abtop --once    # 打印快照后退出
```

在 TUI 界面中：

| 按键 | 功能 |
|------|------|
| `↑`/`↓` 或 `k`/`j` | 选择 session |
| `Enter` | 跳转到对应终端（tmux 内） |
| `x` | 终止选中的 session |
| `X` | 清理所有孤儿端口 |
| `t` | 切换主题 |
| `r` | 强制刷新 |
| `q` | 退出 |

如果你在用 tmux，可以开一个 pane 跑 abtop，其他 pane 分别跑不同的代理，按 Enter 一键跳转。这个操作体验非常流畅。

配置项写在 `~/.config/abtop/config.toml`，可以指定主题、隐藏某些 agent、添加额外配置路径、切换语言。

## 和类似工具的对比

| 工具 | 定位 | 星数 |
|------|------|------|
| abtop | AI 代理 TUI 任务管理器 | ~2500 |
| agent-deck | AI 代理终端 session 管理器 | ~2600 |
| claude-devtools | Claude Code 专属调试工具 | ~3500 |

agent-deck 更侧重"你在终端里同时管理多个 agent 会话的窗口切换"，而 abtop 更像监控仪表盘——你不需要切换到那个 agent 的窗口，直接在 abtop 里就能看到它的状态。

claude-devtools 是 Claude Code 专属的，功能更深（日志、工具调用分析），但仅限于 Claude Code。abtop 覆盖了 Claude Code、Codex CLI、OpenCode 三种，更通用。

## 结语

abtop 不是那种能改变编程范式的工具，它解决的是一个具体的小问题——"多个 AI 代理同时跑的时候，我怎么一屏看清它们都在干嘛"。但正因为问题足够具体，它的解法才足够实用。

如果你只是偶尔用一下 Claude Code，可能不需要它。但如果你已经习惯同时跑多个代理、或者日常工作流里 AI 编码工具是标配，装一个 abtop 花不了两分钟，但每天都能省下点翻窗口的时间。

你可以在 [GitHub 上的 abtop 仓库](https://github.com/graykode/abtop) 查看源码和文档。
