---
title: "RMUX：一个跨平台 tmux 替代品，有 Python/TypeScript SDK"
date: 2026-07-13
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "终端"]
description: "RMUX 是用 Rust 写的跨平台终端复用器，兼容 tmux 命令，原生支持 Windows/macOS/Linux，还有 Python 和 TypeScript SDK，可以用代码控制终端。"
---

## 项目简介

[RMUX](https://github.com/Helvesec/rmux) 是一个用 Rust 编写的原生跨平台终端复用器引擎，当前 ⭐2387。它实现了 90+ 个 tmux 兼容命令，在 Linux、macOS 和 Windows 上原生运行——不需要 WSL 或 Cygwin。更关键的是，它提供 Rust、Python、TypeScript 三种 typed SDK，让开发者可以用代码直接控制终端会话。

## 核心功能

**原生跨平台**是 RMUX 最大的差异化点。tmux 在 Windows 上基本不可用，而 RMUX 的 Windows 后端是原生 Rust 实现，`winget install rmux` 或 `scoop install rmux` 即可安装。macOS 上 `brew install rmux`、Linux 上 APT/DNF/Cargo 都支持。

**Typed SDK** 让 RMUX 超越了普通复用器。在 Python 里可以这样：

```python
from rmux import Session
s = Session()
pane = s.split_window(cwd="/projects/myapp")
pane.send_keys("npm run dev")
output = pane.capture_output()
```

这意味着 AI agent、测试脚本、CI pipeline 可以程序化地操控终端，而不需要 hack tmux 的控制模式。

**Web Share** 功能让终端会话可以通过浏览器共享，使用混合后量子端到端加密，团队调试或远程协作时非常实用。

**Claude Teammate Mode** 集成让 Claude Code 能在 RMUX workspace 中作为团队成员运行，实现多 agent 协作。

## 为什么值得关注

AI 编码工具的兴起让终端复用变得比以往更重要——开发者经常同时运行 Claude Code、测试、dev server、日志 tail。RMUX 的 typed SDK 让 agent 可以直接管理这些终端窗格，而不需要人为介入。

如果你在用 tmux 但苦于 Windows 支持不好，或者想用 Python/TypeScript 编程化控制终端，RMUX 是目前最成熟的方案。项目已发布 v0.8.0，CI 通过 OpenSSF 最佳实践认证，质量有保障。

## 快速上手

```bash
# macOS
brew install rmux

# 启动一个会话
rmux new-session -s mysession

# 垂直分屏
rmux split-window -h

# 安装 Python SDK
pip install librmux

# 用 Python 控制终端
python -c "from rmux import Session; s=Session(); p=s.split_window(); p.send_keys('htop')"
```

## 总结

RMUX 填补了一个真实空白：一个跨平台、可编程的终端复用器，既有 tmux 的用户体验，又提供 typed SDK 给开发者扩展。如果你做 AI agent 开发、跨平台工具、或者只是想在 Windows 上获得 tmux 般的体验，值得一试。

GitHub: [github.com/Helvesec/rmux](https://github.com/Helvesec/rmux)
