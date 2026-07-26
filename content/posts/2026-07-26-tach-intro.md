---
title: "Tach：用 Rust 给你的 Python 代码上防依赖乱引用的保险"
date: 2026-07-26
draft: false
tags: ["开源", "推荐", "GitHub", "Python", "CLI工具"]
description: "Tach 是一个用 Rust 写的 Python 依赖边界检查工具——帮你维护模块之间的依赖关系，防止 import 乱飞，支持 CI 集成和可视化依赖图。"
---

## 项目简介

Python 项目一大了，最头疼的问题之一就是**依赖关系混乱**——utils 模块 import 了 services，services 又 import 了 utils，变成循环依赖；底层模块偷偷引用了上层模块；本不该知道对方存在的包在代码里互相调用。

传统解决方案靠架构文档和 code review 人工把关，但人工总有疏忽。[Tach](https://github.com/tach-org/tach)（⭐2775）是一个用 Rust 实现的 Python 依赖边界检查工具，字面意思就是"栓"住你的模块依赖关系。它让你在 `tach.toml` 里声明每个模块可以依赖谁，然后用 `tach check` 扫描整个项目，找到所有违规的 import——和你的 CI 跑在一起，每次提交自动校验。

## 核心功能

**声明式模块间依赖。** 在项目根目录跑 `tach init`，它会列出你的目录结构，你用方向键把每个 Python 包/模块标记为一个"模块"（module），然后编辑生成的 `tach.toml`，声明每个模块允许依赖哪些其他模块。写错了？`tach check` 会直接报错：

```bash
❌ tach/check.py[L8]: Cannot use 'tach.filesystem'.
Module 'tach' cannot depend on 'tach.filesystem'.
```

**可视化依赖图。** `tach show` 生成 DOT 格式的依赖图谱，`tach show --web` 在浏览器里看可交互的图——哪个模块依赖谁、有没有循环依赖，一目了然。每次重构完跑一下，效果比看架构图文档靠谱一百倍。

**细粒度接口控制 + 分层架构。** 除了"模块 A 可以 import 模块 B"这种粗粒度约束，Tach 还支持定义每个模块的**公开接口**（interfaces）——外部模块只能 import 接口里指定的内容，不能深入模块内部实现细节。同时支持分层架构约束（layers），比如 data 层不能直接 import presentation 层。

**Tach report 反向追溯。** `tach report my_module.py` 告诉你：这个模块的 import 来自哪里、被哪些模块引用——快速定位耦合点，重构前必跑。

**CI 深度集成。** 它原生支持 pre-commit hook（`tach install`）、GitHub Actions、VS Code 插件。每次 PR 提交，CI 自动 check，不合规直接阻断合并。

## 为什么值得关注

在 Python 生态里，类似的工具有 `pylint` 的 import 检查、`import-linter` 等，但 Tach 有几个很实在的优势：

1. **Rust 实现，扫描飞快。** 实测大型 monorepo 项目跑一次 `tach check` 在几百毫秒内完成，几乎没有感知——不像某些用 Python 写的检查工具要等几秒。
2. **渐进式采用。** 你不需要一次性定义所有模块。可以先只约束核心的几个模块，其他用 `unchecked_modules` 跳过。想先尝试一下玩一玩，五分钟就能看到效果。
3. **零运行时开销。** Tach 只在 CI/pre-commit 时运行，不侵入你的运行时代码，不像某些装饰器/代理方案会影响性能。
4. **写的是 Rust 但开发者体验是纯 Python。** 安装就是 `pip install tach`，指令风格完全是 Python 工具的习惯——没有 Rust 工具常见的"你要装个编译环境"的门槛。

对于在维护中大型 Python 项目、monorepo、或者微服务分包但没有严格执行依赖的团队来说，Tach 的 ROI 非常高——每天花 5 秒跑一次检查，换来的是一次架构腐化的提前发现。

## 使用示例

```bash
# 安装
pip install tach

# 在你的 Python 项目里初始化——交互式选择模块边界
tach init

# 运行检查
tach check

# 查看依赖图
tach show --web

# 查看某个模块的依赖关系
tach report my_package/core
```

三步上手：装好、定义模块、跑 check。如果项目已经有清晰的目录结构，10 分钟就配好。

## 总结

Tach 是一个"简单到没有学习成本、硬核到能防住架构腐化"的工具。项目开源在 [GitHub](https://github.com/tach-org/tach)，采用 Rust 底核 + Python 前端的设计，目前在 ⭐2775，发展势头不错（2024 年 1 月才创建）。如果你厌倦了在 Python 项目里靠人脑维护依赖关系，或者你的 `__init__.py` 已经出现循环 import 的苗头，值得试试。
