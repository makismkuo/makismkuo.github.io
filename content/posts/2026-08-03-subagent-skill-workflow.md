---
title: "Subagent、Skill、Workflow：给 AI 编码助手分工的正确姿势"
date: 2026-08-03
draft: false
tags: ["Claude Code", "AI Agent", "Subagent", "Skill", "Workflow", "深度解析"]
description: "Claude Code 把能力拆成了 Subagent、Skill、Workflow 三套机制，很多人用了一阵还是分不清。这篇文章讲清楚三者到底怎么分工、什么时候该用哪个，以及几条实打实的硬约束。"
---

Claude Code 更新到带 Subagent 和 Skill 的版本之后，网上又吵起来了：有人说"Subagent 是来抢 Workflow 饭碗的"，有人反驳"Skill 才是终极答案"。评论区火药味十足。

两边吵什么我不站队，但背后有个更值得想的问题：**这三样东西到底什么关系？为什么一个编码助手要拆出三种"加能力"的方式？**

如果你也在 Claude Code、Codex 或者别的 Agent 工具里见过这些词，却一直没搞明白该用哪个，这篇文章就是写给你的。

## 它到底是什么

一句话：**Subagent 是"人"，Skill 是"说明书"，Workflow 是"流水线"。**

- **Subagent** 是一个拥有独立人格设定和工具权限的子 Agent。你可以在主对话里 `@agent` 叫它出来干活，它有自己的系统提示词，只看到你允许它看的东西。
- **Skill** 是一份 Markdown 格式的能力说明书，教 Agent 在特定场景下怎么做某件事，通常配一组参考文件。它不改变 Agent 是谁，只改变它"会什么"。
- **Workflow** 是把多个步骤、多个角色串起来的编排脚本，定义"先做什么、再做什么、什么条件下分叉"。

三者不是竞争关系，而是**三个不同的抽象层次**。搞混它们，才是大多数配置翻车的根源。

## 用 n8n 来理解

如果你用过 n8n 或者 Dify，这套东西其实不陌生：

💡 **n8n 里的节点 ≈ Subagent**（一个独立执行单元），**节点模板 ≈ Skill**（可复用的做法），**整个 workflow 画布 ≈ Workflow**（编排本身）。

在 Claude Code 里，Subagent 负责"干某一类活"，Skill 负责"教它怎么干"，Workflow 负责"把几类活串起来按顺序干"。粒度从小到大：Skill < Subagent < Workflow。

## Subagent vs Skill vs Workflow

| 维度 | Subagent | Skill | Workflow |
|------|----------|-------|----------|
| 本质 | 独立的子 Agent | 能力说明（Markdown） | 步骤编排 |
| 改变什么 | 谁在干活 | 会干什么 | 按什么顺序干 |
| 何时生效 | 被 @ 调用时 | 相关任务自动触发 | 显式启动时 |
| 典型用途 | 代码审查、写测试、文档 | 特定框架/规范的最佳实践 | 多阶段复杂任务 |
| 可以组合 | 被 Workflow 调用 | 被 Subagent 引用 | 调用多个 Subagent |

**最容易踩的坑**：想给 Agent 加"知识"时用 Subagent，结果把一大段说明写进了子 Agent 的提示词里。知识应该放 Skill，Subagent 只负责"专注地执行"。

## 三步实操

### 第一步：先写一个 Skill

在项目的 `.claude/skills/` 下建目录，写一份 `SKILL.md`：

```markdown
---
name: frontend-review
description: 检查前端代码的响应式和可访问性问题
---

# 前端审查

审查时重点检查：
1. 移动端 375px 宽度下是否有横向滚动
2. 交互元素是否有键盘可达性
3. 颜色对比度是否达到 WCAG AA

参考文件见 references/checklist.md
```

以后 Agent 遇到前端相关任务，会自动加载这份说明书。**Skill 不需要"被调用"，它是被动触发的。**

### 第二步：把一个角色做成 Subagent

在 `.claude/agents/` 下建文件：

```markdown
---
name: code-reviewer
description: 专职代码审查，只做审查不写代码
tools: Read, Grep, Glob
---

你是资深代码审查员。你只负责指出问题，不负责修复。
每次审查按以下顺序：可读性 → 边界情况 → 安全问题。
```

然后在对话里 `@code-reviewer 看看这个 PR 的改动`，它就会以这个身份独立干活。

### 第三步：把流程串成 Workflow

当任务稳定成套路——比如"改动 → 单测 → 审查 → 修 bug → 回归"——就该上 Workflow 了：

```yaml
steps:
  - name: implement
    prompt: 按需求实现功能
  - name: test
    prompt: 为改动补充单元测试
    on_error: fix
  - name: review
    agent: code-reviewer
```

到这里，你会发现三者其实是层层嵌套的：Workflow 编排 Subagent，Subagent 参考 Skill。

## 硬约束

这套体系不是万能的，有几个实打实的限制：

- **Skill 不是代码**。它只是文本说明，没法保证 Agent 一定按它执行。想强制执行，得靠 Workflow 或工具约束。
- **Subagent 上下文隔离是把双刃剑**。它看不到主对话的全部内容，适合"隔离审查"，但需要你主动把上下文喂给它，忘了喂就是答非所问。
- **Workflow 实打实烧 token**。每多一个步骤、多一个子 Agent，都是完整的一次模型调用。编排得越细，账单越好看不了。
- **调试成本高**。三个机制叠在一起，出问题时你很难说清是哪个环节的锅。先跑通小流程，再往上叠。

## 什么时候该用什么

**用 Skill 的场景：**
- 团队有明确的代码规范、提交规范、文档规范
- 有现成的最佳实践想固化下来
- 想让 Agent 懂某个框架的特定写法

**用 Subagent 的场景：**
- 任务需要专注且独立（审查、测试、搜索）
- 不想让主 Agent 被无关上下文污染
- 需要不同角色分工协作

**用 Workflow 的场景：**
- 流程已经稳定，天天重复
- 需要严格顺序和错误处理
- 多个 Subagent 要协作完成一件事

**别急着用的场景：** 一次性任务、探索性任务、还在频繁改流程的阶段。先手工跑几遍，稳定了再固化。

## 聊聊我的感受

用了一阵子之后，我的感受是：这三样东西的边界没那么玄乎，**本质是"分工"这件事在不同粒度上的体现**。

以前写提示词，恨不得把所有东西塞进一段话里。现在学会了拆：知识放 Skill，角色放 Subagent，流程放 Workflow。拆完之后，主对话干净了，每个环节也都能单独测试。

但也别过度设计。我见过有人为了一个小任务配了三个 Subagent 加一个 Workflow，结果跑一次烧掉的 token 比省下的时间还值钱。工具是给你省事的，不是给你添乱的。

至于 Subagent 和 Workflow 谁取代谁——我觉得它们会长期共存。分工的颗粒度不同，解决的问题就不同，谈不上谁淘汰谁。你按自己的节奏用就好。

觉得有用的话，随手点个 ⭐ 或者分享给正在折腾 Agent 的朋友，就是对我最大的支持。

——Seb
