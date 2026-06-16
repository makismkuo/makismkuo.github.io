---
title: "aislop：一个命令抓出AI代码里的「注水肉」"
slug: "aislop-intro"
description: "50+条规则、8种语言、亚秒级检测——用aislop揪出AI编码助手留下的隐蔽坏代码"
date: 2026-06-16T18:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "代码质量"]
categories: ["开发工具"]
---

## 项目简介

GitHub 上每天都有新工具诞生，但能戳到真实痛点的少。`aislop`（scanaislop/aislop，391⭐）就是那种「一用就懂」的工具：**它扫描你的项目，找出 AI 编码助手留在代码里的各种隐蔽问题**。

Claude Code、Cursor、Codex、OpenCode 这些工具写代码飞快，但也会留下特有的「AI 痕迹」——给显而易见的代码加注释、吞掉异常、扔出 `as any` 强制类型、幻觉导入不存在的模块、复制粘贴大量重复辅助函数、留下一堆 TODO 占位符。测试能过，lint 能过，但代码质量在慢慢腐烂。

aislop 就是来抓这些的。

## 核心功能

- **50+ 条检测规则**，覆盖 TypeScript、JavaScript、Python、Go、Rust、Ruby、PHP 等 8 种语言
- **评分系统**：每次扫描输出 0–100 分，同一份代码得分恒定，不存在 LLM 评估的「随缘」问题
- **亚秒级运行**：整个检测是纯静态分析，不需要调 API，不需要 GPU，跑完即出结果
- **多种运行模式**：`scan` 扫描整个项目，`fix` 自动修复机械性问题，`agent` 调用你的 AI 编码助手来修复，`ci` 输出 JSON 格式做 CI 门禁
- **Git 集成**：只扫描变更文件（`--changes`），适合 PR 审查场景，还支持 pre-commit hook
- **可配置规则**：支持自定义 severity、排除文件、SARIF 输出（可直接导入 GitHub Code Scanning）

安装极其简单：

```bash
npx aislop@latest scan      # 不需要安装，直接跑
pipx install aislop          # Python 用户
brew install scanaislop/tap/aislop  # macOS
```

## 为什么值得关注

现在很多团队已经在 CI 里配了 ESLint、Pylint、golangci-lint 等传统 linter，但**传统 linter 不会发现的「AI 特有」坏味道**才是真正的盲区。

比如 AI 编码助手特别喜欢写这样的代码：

```typescript
// 遍历数组，把每个元素乘2
const doubled = arr.map(x => x * 2);
```

这种「小学生写注释」的行为，普通的静态分析工具根本不会报错。aislop 的规则里专门有一类就是 **narrative comments**——检测那些解释"显而易见之事"的废话注释。

再比如：

- `swallowed-exceptions`：catch 块只写了 `console.error` 或直接空着
- `as-any-casts`：过多的类型断言，表示 AI 搞不定类型推断
- `hallucinated-imports`：导入不存在的模块或路径
- `dead-code`：定义了但从未使用的函数/变量
- `oversized-functions`：单个函数超过合理行数
- `todo-stubs`：只写了 TODO 注释但没有任何实现的函数体

每个项目跑一次 `aislop scan`，得分会直接显示在终端，还可以在 README 上挂一个 badge，让代码质量可见。

## 简单示例

```bash
# 扫描当前项目
npx aislop@latest scan

# 只看本次改动
npx aislop@latest scan --changes

# 输出 JSON 给 CI 使用
npx aislop@latest scan --json

# 自动修复机械性问题
npx aislop@latest fix

# 设置 pre-commit hook
npx aislop@latest hook install
```

如果项目是 AI 编码助手生成的，第一次跑 `aislop scan` 的分数很可能让你惊讶——这不是说代码不能用，而是说有很多可以清理的「技术债」被 AI 悄悄埋下了。

## 总结

aislop 不是要替代传统 linter，而是补上了它们在 AI 时代的盲区。80% 的规则属于「不看不知道，看完觉得确实该改」的类型。MIT 协议，免费 CLI，没有 runtime 依赖，值得每个深度使用 AI 编码助手的团队加进流程里。
