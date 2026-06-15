---
title: "skillshare：一个命令把 AI 技能同步到所有 CLI 工具"
date: 2026-06-15
draft: false
tags: ["开源", "推荐", "GitHub"]
---

## 项目简介

如果你同时用 Claude Code、Codex、Cursor、Copilot、OpenCode……你会遇到一个让人抓狂的问题：每个工具都有自己的 skills 文件夹。你在 Claude 里写好了一个 prompt skill，还得手动复制到 Codex 那边，再复制到 Cursor 里。改一次就要复制 N 次，永远有人忘了哪个没更新。

[s​killshare](https://github.com/runkids/skillshare)（⭐ 2225）用一句话解决了这个问题：**一个命令，所有工具同步**。它是 Go 写的单二进制工具，支持 macOS / Linux / Windows，安装后一条 `skillshare sync` 就能把你的 skills、agents、rules 同步到 60+ 个 AI CLI 工具上，底层用 symlink（Windows 上用 NTFS Junction），不改文件结构，没有注册中心，没有 telemetry。

## 核心功能

- **One source of truth**：你的 skills 统一放在 `~/.config/skillshare/skills/`，`sync` 命令会 symlink 到各个工具的路径，改一个全员生效。
- **从 Git 安装 skill 包**：`skillshare install github.com/reponame/skills`，自动下载并链接。
- **内置安全审计**：`skillshare audit` 会扫描已安装的 skills 是否存在 prompt injection 或数据泄露风险——这在多来源安装场景下尤其重要。
- **Extras 系统**：不只是 skills，还能管理 rules、commands、prompts 和任意文件资源。
- **Project scope**：把 skills 放在项目仓库的 `.skillshare/` 里，团队共享，随代码提交。
- **Web UI**：`skillshare ui` 启动一个本地仪表盘，可以可视化查看、搜索、管理所有 skills。
- **细粒度过滤**：通过 `.skillignore`、`SKILL.md` 的 `targets` 字段、per-target include/exclude 精确控制每个 skill 流向哪些工具。

## 为什么值得关注

2025-2026 年最大的趋势之一就是 AI CLI 工具大爆发。Claude Code、Codex、OpenCode、OpenClaw、Gemini CLI……每隔几周就有新工具出现。但这些工具的生态系统是割裂的——每个工具都有自己的 skill/agent 目录，彼此不认识。

skillshare 补上了这个缺失的基础设施层。它不是又一个 AI 工具，而是让所有 AI 工具能正常工作的管理工具。Go 单二进制、MIT 许可、无外部依赖，理念上有点像 nvm（Node.js 版本管理器）——不解决AI问题，解决AI工具的工具化问题。

另外它的安全审计功能设计得很聪明：从外面安装 skills 时自动扫描，避免你无意中引入了 prompt injection。这对团队协作场景尤其有价值。

## 简单示例

```bash
# 安装
brew install skillshare

# 初始化——自动检测你装了哪些 AI CLI 工具
skillshare init

# 写一个你本地的 skill（就是一个标准 markdown）
mkdir -p ~/.config/skillshare/skills/my-junior-dev
cat > ~/.config/skillshare/skills/my-junior-dev/SKILL.md << 'EOF'
---
name: my-junior-dev
description: 帮我审查 Python 代码，只关注性能和安全性
---
当用户让你 review Python 代码时，重点关注性能瓶颈和常见安全漏洞。
EOF

# 一键同步到所有 AI 工具
skillshare sync

# 从 GitHub 安装第三方 skill 包
skillshare install github.com/awesome-org/awesome-skills

# 审计已安装的 skills
skillshare audit
```

## 总结

skillshare 解决了一个真实又普遍的问题——AI CLI 工具的 skill 管理碎片化。它没有做超越自己定位的事：不搞 agent、不搞编排、不搞 LLM，只是一个扎实的工具管理工具。Go 实现让它轻量、跨平台、无依赖。如果你同时在用两个以上的 AI CLI 工具，你可能今天就需要它。

项目地址：[github.com/runkids/skillshare](https://github.com/runkids/skillshare)
