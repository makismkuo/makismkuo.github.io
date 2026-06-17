---
title: "AutoCLI：一条命令抓遍 55+ 网站，开发者必备的 Rust CLI 神器"
date: 2026-06-17T10:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "Rust"]
description: "AutoCLI 是一个用 Rust 重写的超快命令行工具，一条命令就能从 Twitter、Reddit、B站、小红书等 55+ 网站获取信息，速度比同类工具快 12 倍，内存只用十分之一。"
---

## 项目简介

[AutoCLI](https://github.com/nashsu/AutoCLI) 是一个用 Rust 编写的命令行工具，前身是基于 Node.js 的 OpenCLI。它的一条核心使命是：**一条命令从任意网站获取信息**。目前内置 55 个站点、333 条命令，覆盖 Twitter/X、Reddit、YouTube、Hacker News、B站、知乎、小红书等主流平台，还支持 Electron 桌面应用控制、本地 CLI 工具集成（gh、docker、kubectl），以及 AI 驱动的适配器自动生成。

项目目前 **2.8k stars**，仍处于快速迭代阶段（最新 v0.3.2），在开发者社区中口碑很好。

## 核心功能

AutoCLI 最大的特点就是 **快** 和 **小**。它是 Rust 从零重写的版本，单二进制文件仅 4.7MB，零运行时依赖——这意味着你不需要装 Node.js、Python 或其他环境，下载就能用。

- **55+ 站点一站式 CLI 入口**：`autocli hackernews top` 看 HN 热帖，`autocli bilibili hot` 刷 B 站热门，`autocli twitter search "rust lang"` 搜推文。输出支持 table、JSON、YAML、CSV、Markdown 多种格式，方便管道处理。
- **浏览器会话复用**：通过 Chrome 扩展复用已登录的浏览器会话，免去管理 Cookie 和 Token 的麻烦。
- **YAML Pipeline 声明式配置**：可以用 YAML 描述数据抓取流程，零代码添加新适配器。
- **AI 适配器自动生成**：`autocli generate --ai` 配合 LLM 自动分析任意网站结构并生成适配器，生成的适配器可在 autocli.ai 社区共享。
- **CLI 工具透视**：`autocli register mycli` 注册本地 CLI 工具后，AI Agent 就能自动发现和调用所有已注册的命令。
- **AI Agent 原生友好**：配置 `AGENT.md` 后，OpenClaw、Claude Code 等 AI 代理可以自动发现 AutoCLI 的全部能力。

性能上对比原版 Node.js 实现：内存占用从 99MB 降到 15MB（6.6 倍），B站热门命令从 20 秒降到 1.66 秒（12 倍），知乎热榜从 20 秒降到 1.77 秒（11.6 倍）。

## 为什么值得关注

日常开发中有太多场景需要从不同网站获取信息——查 Hacker News 的讨论趋势、看 Reddit 的技术热帖、搜 B 站的 Rust 教程、跟踪 X 上的 AI 动态。以前每个网站都要找不同的工具、写不同的脚本。

AutoCLI 把这些统一成了一个接口。而且它的设计不是那种"拿来用但跑不起来"的项目——安装只需要一条 `curl` 命令，没有 Node、Python 之类的运行时依赖，对 AI Agent 也有原生支持。对于写 CLI 工具、做自动化工作流、或者单纯想减少浏览器操作的开发者来说，这是一个开箱即用的省力工具。

## 简单示例

```bash
# 一行安装（macOS/Linux）
curl -fsSL https://raw.githubusercontent.com/nashsu/autocli/main/scripts/install.sh | sh

# 查看 Hacker News 当前热帖前 5
autocli hackernews top --limit 5

# 搜知乎 "Rust 2026"
autocli zhihu search "Rust 2026" --limit 10 --format json

# 查看 B 站今日热门视频
autocli bilibili hot --limit 20

# 生成 shell 补全
autocli completion zsh >> ~/.zshrc
```

不需要浏览器的时候（Hacker News、Dev.to、Lobsters 等公共站点），装完就能直接用。需要登录态的场景装一下 Chrome 扩展即可。

## 总结

AutoCLI 把 55+ 网站的信息获取统一到了一个 4.7MB 的 CLI 里，速度快、体积小、零依赖，对 AI Agent 的集成度也做得不错。如果你厌倦了为一个网站写一个爬虫脚本，或者想给 AI Agent 装备一个"全网访问能力"，AutoCLI 值得一试。
