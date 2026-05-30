---
title: "Headroom：给你的 AI 代理上下文"减肥"，Token 省 60-95%"
date: 2026-05-30
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "开发工具"]
---

## 一个每天都在烧钱的问题

用 AI 编码代理（Claude Code、Cursor、Codex、Aider）的人，应该都有过这种体验：代理跑了几百步，每一步都把工具输出、日志、搜索结果的原文塞进上下文，Token 消耗像流水一样。月底看账单，发现一大半费用花在了重复的、冗长的上下文上。

更有意思的是，这些上下文里的大部分内容，LLM 读过一次就不需要再读了——但每次调用都得重新传输。

Headroom 就是冲这个问题来的。

项目地址：[github.com/chopratejas/headroom](https://github.com/chopratejas/headroom)，目前 2078 个 Star，Apache 2.0 协议，Python/TypeScript 双实现。2026 年 1 月才发布，社区已经用它省了 600 亿+ Token。

## Headroom 干了什么

一句话：**在 AI 代理读取内容之前，先把它压缩到原来的 5%-40%，同时保留原始数据以备需要时还原。**

它不是简单的 gzip——上下文压缩的原理是**语义级压缩**。它识别内容是 JSON、代码还是自然语言，分别用不同的策略处理：

- **SmartCrusher**：处理 JSON 结构，去掉冗余的键名和重复对象
- **CodeCompressor**：基于 AST 分析，压缩代码文件但不破坏逻辑
- **Kompress-base**：自家训练的 HuggingFace 模型，专攻自然语言文本压缩

压缩后的内容依然可读，LLM 能直接理解。如果有需要，它还通过 **CCR（可逆压缩）** 机制把源文件存在本地，LLM 可以通过 MCP 工具按需取回。

## 怎么用

### 方式一：一键包装（最省事）

```bash
pip install "headroom-ai[all]"

# 包装 Claude Code
headroom wrap claude

# 包装 Codex
headroom wrap codex

# 包装 Cursor（会打印配置，粘贴一次即可）
headroom wrap cursor

# 包装 Aider
headroom wrap aider
```

包装之后，代理的所有输入输出自动经过压缩层，零代码改动。

### 方式二：代理模式

如果你不想包装，也可以起一个本地代理，任何兼容 OpenAI 的客户端都可以用：

```bash
headroom proxy --port 8787
```

然后把你的 API endpoint 改成 `http://localhost:8787/v1` 即可。

### 方式三：作为库嵌入

Python 代码里直接调用：

```python
from headroom import compress

messages = [
    {"role": "user", "content": huge_tool_output}
]
compressed = compress(messages)
# compressed 只有原来的 8%-30%
```

TypeScript 也一样：

```typescript
import { compress } from 'headroom-ai';
const result = await compress(messages);
```

### headroom learn：让代理从错误中学习

这个功能比较有意思。`headroom learn` 会扫描代理失败的运行记录，分析失败模式，然后把修正方案写进 `CLAUDE.md` 或 `AGENTS.md`。下次代理再遇到类似问题，就不用再踩同一个坑了。

```bash
headroom learn --session /path/to/failed/session
```

本质上是在做一个自动化的经验积累——失败的每一分钱都不白花。

## 效果到底怎么样

官方给出的基准测试挺实在的：

| 场景 | 压缩前 | 压缩后 | 节省 |
|------|-------|-------|------|
| 代码搜索（100 条结果） | 17,765 | 1,408 | 92% |
| 线上故障排查 | 65,694 | 5,118 | 92% |
| GitHub Issue 分类 | 54,174 | 14,761 | 73% |
| 代码库探索 | 78,502 | 41,254 | 47% |

标准基准测试上，准确性没有下降——GSM8K 数学推理 87% → 87%，TruthfulQA 甚至从 53% 涨到 56%。

换句话说，压缩掉的都是冗余信息，模型该理解的都理解了。

## 为什么值得关注

说几个点：

**首先是省钱。** 如果你的代理每天消耗几百万 Token，把输入压缩到 10%-30% 意味着成本直接降一个数量级。对于重度用户，一个月省下来的费用可能就覆盖一台 M4 Mac Mini 了。

**其次是本地优先。** 所有压缩都在本地完成，数据不出机器。之前也有一类 Token 压缩服务是把文本发到云端 API 去压缩，头都大了——为了省钱把数据送给别人。Headroom 的路线是对的。

**第三是跨代理共享。** 它的内存系统支持 Claude Code、Codex、Gemini 等不同代理共享同一份压缩上下文和记忆，不会因为换了工具就丢失上下文。

**第四是可逆。** 很多压缩方案是一锤子买卖，压缩了就拿不回原样了。Headroom 的 CCR 保证原始文件永远可以按需取回。如果你担心 LLM 因为信息压缩而遗漏关键细节，这个机制能兜底。

## 不足

也不是没有槽点。HEADROOM_API_KEY 的设置有点迷惑——它其实只是用来同步排行榜数据的，不压缩也能用，但首次使用时多了一个配置步骤。

另外，在沙箱环境（比如某些 CI/CD 管道）里跑不了，因为需要本地进程做压缩。这种情况下只能考虑用它的库模式预先处理内容。

还有一个是 109 个 open issue，说明项目还很早，迭代过程中 API 可能会有变动。

## 适合谁

- 每天用 AI 编码代理写代码的人
- 管理多个代理、想统一管理上下文的人
- 对 Token 费用敏感的个人开发者或小团队
- 对数据隐私有要求、不想把数据上传到第三方压缩服务的人

如果你刚好属于这些人群之一，Headroom 值得花十分钟试一下。装个包，跑一句 `headroom wrap`，就能看到效果。

项目地址：[github.com/chopratejas/headroom](https://github.com/chopratejas/headroom)
