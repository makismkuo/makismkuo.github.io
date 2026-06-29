---
title: "Entire CLI：给 AI 写的每一行代码上个户口"
date: 2026-06-29
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI", "开发工具"]
---

用 AI 编码助手写代码，现在已经是很多开发者的日常了。但有一个问题越来越烦人：**AI 代理在仓库里改了一堆文件，Commit message 写得很漂亮，可你完全不知道这些代码是怎么来的。**

是哪个 prompt 导致的变更？改了哪些文件？中间有没有走错路然后回退？这些都成了黑盒。传统 `git log` 只能告诉你"改了什么"，但说不清"为什么改"。

**Entire CLI** 就是来解决这个问题的。

## Entire CLI 是什么

Entire 是一个开源 CLI 工具，它挂接到你的 Git 工作流中，自动捕捉 AI 代理的每次对话、每个 prompt/response、每次工具调用，并把这些数据索引到 `git log` 旁边，形成一个可搜索的"代码诞生记录"。

项目刚发布不久，目前在 GitHub 上已有 **4562 颗星**（github.com/entireio/cli），支持 macOS、Linux 和 Windows。安装方式很友好：Homebrew、Scoop、install.sh 三管齐下。

## 核心功能

- **自动捕捉 AI 会话**：Claude Code、Codex、Gemini、Pi、Cursor 等主流 AI 编码代理都支持。装好之后后台静默运行，零切换成本。
- **会话与 Commit 双向索引**：每次你或代理提交代码，完整的 prompt 记录、响应内容、修改的文件列表、token 用量都存入 `entire/checkpoints/v1` 分支，和你的 commit 一一对应。
- **"倒带"恢复**：代理跑偏了？随时回滚到之前的 checkpoint，恢复代码到那个状态，无缝继续。
- **跨会话恢复**：`entire session resume <branch>` 可以恢复之前在某个分支上的所有 AI 会话上下文。
- **Git Worktree 友好**：多个工作区跑不同 AI 代理也不会冲突。

## 为什么值得关注

AI 辅助编码最大的隐患之一是**不可追溯**。当代码出问题的时候，你没法知道是哪个 prompt 引发了这次变更、中间经过了多少步骤、是不是某个工具调用引入了 bug。传统代码审查流程在 AI 编写的代码面前几乎失效。

Entire 解决的就是这个信任问题。它把 AI 编写代码的"思考过程"保留下来，和最终的代码变更锁在一起。这对个人开发者来说，意味着你永远不会搞丢"当时为什么要这么写"的上下文；对团队来说，Code Review 终于可以追溯到 AI 的原始输出，而不仅仅是看一个人写的 commit message。

另一个很实用的场景是新成员 onboarding：直接 `entire session resume` 恢复之前某个分支上的 AI 工作记录，新人就能看到从 prompt 到代码的完整路径，比翻文档快得多。

## 快速上手

```bash
# macOS 安装
brew tap entireio/tap
brew install --cask entire

# 在项目里启用
cd your-project
entire enable

# 查看状态
entire status

# 正常用你的 AI 代理，剩下的 Entire 自动处理
entire log  # 查看历史会话
```

`entire enable` 会创建配置、安装 Git hooks，然后提示你选择要跟踪哪些 AI 代理。之后每次你和 AI 代理交互并提交代码，会话数据自动落盘。

## 总结

Entire CLI 填补了一个真实存在的空白：AI 辅助编码的**可追溯性**。它不是又一个花哨的 AI 工具，而是一个基础设施级别的补丁——让 Git 生态适应 AI 协作的新现实。开源、轻量、实用，值得每个重度使用 AI 编码代理的开发者装起来试试。
