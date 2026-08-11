---
title: "gitlogue：把你的 Git 历史变成一部终端电影"
date: 2026-07-22
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "Rust"]
description: "gitlogue 是一个 Rust 构建的 CLI 工具，能把 Git 提交历史变成带打字动画、语法高亮和文件树过渡的终端回放。支持 29 种语言、9 种主题、屏幕保护模式。"
---

你有没有想过——Git 日志只是一堆 hash 和 diff，能不能像看代码直播一样看到自己的项目一步步长起来？

**gitlogue** 做到了。一个用 Rust + Ratatui 构建的 CLi 工具，把你的 Git 提交历史变成一部带打字动画、语法高亮和文件树过渡的「终端电影」。

## 项目简介

gitlogue 由日本开发者 Yuji Ueki（@unhappychoice）创建，用 Rust 和 tree-sitter 实现。项目在 GitHub 获得 4800+ Star，ISC 开源协议。安装极其简单：

```bash
# macOS
brew install gitlogue

# 一行脚本
curl -fsSL https://raw.githubusercontent.com/unhappychoice/gitlogue/main/install.sh | bash

# 或 Cargo
cargo install gitlogue
```

然后在你的任意 Git 仓库里运行 `gitlogue`——立刻开始播放。

## 核心功能

- **动画回放**：每次提交以打字动画重现——光标移动、代码输入、删除、文件切换，逼真到像有人在直播写代码
- **随时切换视角**：`Space` 暂停/播放，`n`/`p` 切到下一个/上一个提交，`h`/`l` 逐行步进
- **Tree-sitter 语法高亮**：支持 29 种语言（Go、Rust、Python、TypeScript、Swift……），不是傻白文本
- **文件树 + 统计**：右边栏显示项目结构，每个文件旁边标注增删行数
- **屏幕保护模式**：不加参数直接跑，无限随机播放仓库历史，适合挂在副屏上
- **9 种内置主题**：Nord、Dracula、Catppuccin……也可以自定义
- **灵活过滤**：按作者（`--author "john"`）、日期范围（`--after "2024-01-01"`）、文件模式（`--ignore "*.ipynb"`）筛选提交
- **Diff 模式**：`gitlogue diff` 显示工作区的暂存/未暂存变更，不依赖提交，适合写代码时的实时预览

日常用法：

```bash
# 屏幕保护模式（无限随机回放）
gitlogue

# 回放最近 5 个提交
gitlogue --commit HEAD~5..HEAD

# 指定主题和速度
gitlogue --theme dracula --speed 20

# 按作者过滤
gitlogue --author "makismkuo"
```

## 为什么值得关注

Git 可视化工具不少——GitHub 有 Insights，本地有 GitKraken、Sourcetree——但它们都是「基于时间轴的静态展示」。gitlogue 的独特之处在于**时间性**：你看到的不是最终状态，而是代码如何一步步变成现在的样子。

这对几个场景特别有用：

1. **代码审查**：PR review 时用 `gitlogue --commit HEAD~10..HEAD`，直观看到修改顺序和上下文，比逐文件看 diff 高效
2. **分享/演示**：录屏配合 gitlogue 做技术分享，比翻 PPT 生动多了
3. **回顾学习**：回放自己的项目，能清晰看到编码节奏——哪里在试探、哪里在重构、哪里一次性提交太多
4. **桌面装饰**：副屏挂着 gitlogue，让访客觉得你在实时coding（以及真正的屏幕保护都太无聊了）

## 总结

gitlogue 把一个再平常不过的需求——「看看代码是怎么改的」——变成了一个好看的终端体验。4800+ Star 的社区认可、Rust 的性能、tree-sitter 的高亮质量，都让它不只是个玩具。

如果你写 Git 提交，或者只是想找点新鲜玩意儿装饰你的终端，值得一试。

```bash
brew install gitlogue && cd your-project && gitlogue
```
