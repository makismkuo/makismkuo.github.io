---
title: "AgentShield：给 AI Agent 做个体检"
date: 2026-05-27
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "安全"]
---

## 一个你想过但没查过的问题

如果你在用 Claude Code、Codex、Cursor 这类 AI 编码助手，大概率已经习惯让它们替你跑脚本、读文件、写代码。

但你有没有想过一个问题——你给它们的权限，到底有多大？

Claude Code 的 `.claude/` 目录里，可能藏着硬编码的 API Key、给了全局 Bash 权限的 allow rule、自动安装和执行外部脚本的 hook 配置。平时不会出事，但万一哪个 MCP 插件供应链被投毒，或者哪篇文档里的 curl 命令钓了鱼，后果就很直接。

AgentShield 就是干这个的。它不是 LLM 安全理论，是一个能直接跑的安全扫描器。

## 项目速览

项目名 AgentShield，GitHub 上搜 `affaan-m/agentshield` 就能找到，目前 700+ stars，MIT 协议。

一句话概括：扫描 AI Agent 的配置文件，找出安全漏洞，并给出修复建议。支持的扫描对象包括 Claude Code、OpenCode、Codex、Gemini CLI、VS Code 等主流 AI 开发工具的配置。

## 它能扫什么

AgentShield 把安全隐患分成五大类，总共 102 条检测规则：

**密钥泄露** —— 配置里有没有直接写了 API Key？不管是 Anthropic 的 `sk-ant-` 开头的密钥，还是 OpenAI、AWS、GitHub Token，只要出现在不该出现的地方，都会报出来。而且支持自动修复，把硬编码的密钥替换成 `${ENV_VAR}` 引用。

**权限越界** —— 你的 agent 有没有 `Bash(*)` 这种全局命令执行权限？有没有 `Write(*)` 这种全局写权限？有没有 `--dangerously-skip-permissions` 这种一键裸奔配置？AgentShield 会提示你把通配符缩小到具体命令。

**Hook 注入** —— 配置里有没有预处理钩子（PreToolUse hooks）在运行 curl 并传外部变量？有没有 hook 把错误输出静默丢弃？有没有 hook 在安装全局 npm 包？这些是实际攻击中最常被利用的入口。

**MCP 服务器风险** —— 你的 MCP 配置里有没有 `npx -y` 这种无确认安装？有没有连接到远程 SSE/HTTP 服务器的 MCP？有没有挂载根目录文件系统的 filesystem server？每个都有具体风险说明。

**Agent 配置审查** —— 有没有 agent 被配置成"自动运行"、"不要询问"？有没有隐藏指令用零宽字符嵌入？有没有 base64 编码的后门？这些都是 prompt injection 的实际攻击面。

## 怎么用

一行命令跑起来，不需要安装任何依赖：

```bash
npx ecc-agentshield scan
```

它会自动发现 `~/.claude/` 目录，扫描所有配置文件，然后给你一份带评级的报告：

```
AgentShield Security Report

Grade: F (0/100)

Score Breakdown
Secrets        ░░░░░░░░░░░░░░░░░░░░ 0
Permissions    ░░░░░░░░░░░░░░░░░░░░ 0
Hooks          ░░░░░░░░░░░░░░░░░░░░ 0
MCP Servers    ░░░░░░░░░░░░░░░░░░░░ 0
Agents         ░░░░░░░░░░░░░░░░░░░░ 0

● CRITICAL  Hardcoded Anthropic API key
  CLAUDE.md:13
  Evidence: sk-ant-a...cdef
  Fix: Replace with environment variable reference [auto-fixable]

● CRITICAL  Overly permissive allow rule: Bash(*)
  settings.json
  Fix: Restrict to specific commands: Bash(git *), Bash(npm *)
```

评分从 A 到 F，带 0-100 的数值分，一目了然。

如果想全局安装慢慢扫：

```bash
npm install -g ecc-agentshield
agentshield scan
```

还有一些实用的子命令：

```bash
# 指定目录扫描
agentshield scan --path /path/to/project

# 自动修复安全的小问题（替换硬编码密钥）
agentshield scan --fix

# JSON 输出，方便 CI 集成
agentshield scan --format json

# 生成 HTML 安全报告
agentshield scan --format html > report.html
```

## 值得用在哪

**日常检查** —— 第一次用 AI 编码助手之前跑一次，看看有没有不自知的安全隐患。很多人装了 Claude Code 就直接用默认配置，默认配置权限给得相当宽。

**CI 流水线** —— AgentShield 有 GitHub Action，可以直接集成进 CI。每次 PR 自动扫描配置，发现高危漏洞就 fail pipeline：

```yaml
- name: AgentShield Security Scan
  uses: affaan-m/agentshield@v1
  with:
    path: "."
    min-severity: "medium"
```

**团队管理** —— 支持策略评分（policy evaluation），可以定义组织的安全基线，扫描结果跟基线对比，新引入的风险一目了然。

## 深度分析模式

如果装了 Claude Code，还可以用 `--opus` 模式跑红蓝对抗分析。它会启动三个 Agent：

1. **红队（攻击者）** —— 寻找可被利用的攻击路径
2. **蓝队（防御者）** —— 评估现有的防护措施
3. **审计者** —— 综合双方观点，输出优先修复列表

这个模式需要 `ANTHROPIC_API_KEY` 环境变量，跑一轮大概一两分钟，但输出的分析质量确实比纯规则扫描高一个层级。

## 不足

说几个实际使用中感受到的局限：

规则有点多。100 多条规则扫下来，结果列表挺长的，尤其是 MCP 配置丰富的项目，需要花时间逐条审核。项目方也意识到了这个问题，用了 `runtimeConfidence` 字段来区分"当前正在运行的配置"和"模板/示例文件"，但初次使用者还是会觉得报告有点密。

对国内开发者来说，完全依赖 npm 安装（`npx ecc-agentshield`），如果网络不通畅可能会慢。不过安装到本地后第二次使用就没这个问题了。

范围主要是 Claude Code 生态。虽然也支持 Codex、Gemini CLI、VS Code 等工具的配置扫描，但最完善的规则覆盖还是围绕 `.claude/` 目录。如果用 Cursor 或 Windsurf 这类产品，可能需要额外确认兼容性。

## 总结

AgentShield 解决的是一个真实存在但容易被忽视的问题：AI Agent 的安全配置。它的价值不在于规则有多全面，而在于让安全变得可检查、可量化、可修复。

对于重度使用 AI 编码助手的团队和个人开发者来说，花两分钟跑一次扫描，看看自己的 agent 配置里有没有裸奔的权限和硬编码的密钥，算是一笔很划算的安全投入。

项目地址：https://github.com/affaan-m/agentshield
