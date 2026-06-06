---
title: "yek：一个 Rust 写的代码序列化工具，比同类快 230 倍"
date: 2026-06-06
draft: false
tags: ["开源", "推荐", "GitHub", "Rust", "CLI", "AI"]
---

## 用一个问题开场

用 AI 工具（Claude Code、Copilot、ChatGPT）帮忙分析代码的时候，最常见的操作是什么？

把一段代码粘贴进去。

但如果要分析的是一个完整的项目呢？十几甚至上百个文件，逐个复制粘贴显然不现实。你可能会写一个脚本，遍历目录、拼接文本，然后再处理各种边界情况——二进制文件要跳过，node_modules 要排除，顺序要合理。

这个问题很常见，但一直没有特别好的答案。直到我发现了 **yek**。

## yek 是什么

yek（波斯语「一」的意思）是一个 Rust 写的命令行工具，功能很简单：**把一个目录下的文本文件序列化成一个文件，方便丢给 LLM 处理**。

项目地址：https://github.com/mohsen1/yek

它不是什么新鲜概念——同类工具已经有 Repomix 等。但 yek 的独特之处在于性能和设计取舍，后文会详细说。

## 核心功能

yek 开箱即用，在项目目录里直接跑一行命令就行：

```bash
yek
```

默认行为已经覆盖了大部分需求：
- 自动读取 `.gitignore`，跳过不需要的文件
- 分析 Git 提交历史，判断哪些文件更重要（修改越频繁的文件优先级越高）
- 自动识别二进制文件、大文件并跳过
- 输出到一个临时文件，打印文件路径

更实用的是一些进阶用法：

**按 Token 数截断输出**：AI 工具有上下文窗口限制，yek 的 `--tokens` 参数可以按 token 数限制输出大小，超出部分自动丢弃低优先级的文件：

```bash
yek --tokens 128k
```

**管道输出到剪贴板**：在 macOS 上配合 pbcopy 可以直接粘到对话里：

```bash
yek src/ | pbcopy
```

**处理特定文件或目录**：支持 glob 模式，可以精确控制要包含的内容：

```bash
yek "src/**/*.ts" "tests/**"
```

**行号输出**：需要引用代码行时很有用：

```bash
yek --line-numbers
```

**JSON 输出**：如果想自己写脚本处理结果，JSON 格式更方便：

```bash
yek --json
```

**自定义模板**：可以通过 `--output-template` 控制输出格式，默认是 `>>>> FILE_PATH\nFILE_CONTENT`。

## 真正厉害的地方

yek 最有意思的设计是**文件优先级排序**。

默认情况下，输出文件中**最重要的文件排在最后面**。这看起来反直觉，但背后有合理的考虑——LLM 对上下文末尾的内容注意力更强，所以把核心代码放在最后，让 AI 能更好地理解关键逻辑。优先级排序依据的是 Git 历史：改动越频繁的文件，越可能是项目的核心代码。

此外，yek 还支持 YAML/TOML/JSON 格式的配置文件（`yek.yaml`），可以在项目根目录放一个，团队共享统一的序列化规则：

```yaml
ignore_patterns:
  - "ai-prompts/**"
  - "__generated__/**"

priority_rules:
  - score: 100
    pattern: "^src/lib/"
  - score: 90
    pattern: "^src/"
  - score: 80
    pattern: "^docs/"

max_size: "128K"
```

## 性能对比：不是一个量级

yek 用 Rust 实现，这是它最大的优势。作者拿 Next.js 项目做了一次对比测试：

| 工具 | 耗时 |
|------|------|
| **yek** | **5.19 秒** |
| Repomix | 22.24 分钟 |

**yek 比 Repomix 快 230 倍**。

这并不是 Repomix 写得不好——它是用 TypeScript 写的，处理大型项目时 Node.js 的文件 I/O 和字符串处理确实是瓶颈。Rust 在这个场景下优势巨大，而且 yek 大量并行化处理，充分利用了多核 CPU。

这个性能差距在实际体验中是非常明显的。Repomix 跑一个中等规模项目可能要等几分钟，yek 几乎是瞬间完成。试过之后，很难再回到慢速工具。

## 安装很简单

macOS 和 Linux 一条命令搞定：

```bash
curl -fsSL https://azimi.me/yek.sh | bash
```

Windows 用 PowerShell：

```powershell
irm https://azimi.me/yek.ps1 | iex
```

也支持从源码构建（需要 Rust 工具链）：

```bash
cargo install yek
```

## 使用场景

yek 最适合两类人：

**AI 辅助编程的用户**。不管你用的是 Claude Code、Copilot、ChatGPT 还是 Codex，只要需要把项目上下文喂给 AI，yek 就是那个「用了就回不去」的工具。我现在的 workflow 是：改完代码 → `yek src/ api/ | pbcopy` → 粘到对话里让 AI review。

**需要批量分析代码的人**。比如做代码 Review、技术评估、代码迁移方案等，需要把大量文件处理成可分析的格式，yek 一键搞定。

## 值得关注的点

yek 目前还在活跃开发中，GitHub 上的 issues 里有很多功能提案。项目有 12 个 open issues，大多数是 feature request，作者回复积极。从 2025 年 1 月创建到现在一年多，2400+ stars，社区认可度不错。

需要注意的局限：
- 主要用于给 LLM 消费，不是通用的文件合并工具
- 中文等非 ASCII 字符的 token 计数可能不太准确（取决于底层 tokenizer）
- 输出模板目前只支持 `FILE_PATH` 和 `FILE_CONTENT` 两个占位符

## 结语

yek 解决的是一个具体但高频的问题：在 AI 时代，如何高效地把项目代码交给 LLM 分析。它用 Rust 的性能优势把一个本来需要几十分钟的操作压缩到几秒，而且设计上处处为 LLM 的使用场景考虑——优先级排序、Token 截断、管道输出、配置文件。

项目地址：https://github.com/mohsen1/yek

如果你是 AI 辅助编程的重度用户，yek 值得装一个试试。5 秒装完，之后每次需要把代码给 AI 看的时候都能省几分钟。
