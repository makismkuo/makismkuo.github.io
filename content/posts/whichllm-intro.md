---
title: "哪款本地大模型最适合你的电脑？一条命令搞定"
date: 2026-05-28
draft: false
tags: ["开源", "推荐", "GitHub", "LLM", "AI工具"]
---

## 一个问题

买新显卡或者刚入手 Mac Studio 的时候，很多人会面临同一个困惑：我这台机器能跑多大的模型？跑哪款模型效果最好？

凭经验猜，多半会错。RTX 4090 用户可能会直接去下 70B 的模型，结果发现推理慢得没法用。而 MacBook 用户可能以为自己只能跑 7B 以下的模型，却不知道 MoE 架构的 30B 模型在统一内存上跑得飞快。

传统的做法是挨个下载、试跑、删掉、再下载。一个 GGUF 模型动辄十几 GB，试错成本很高。这正是 whichllm 要解决的问题。

## whichllm 是什么

[whichllm](https://github.com/Andyyyy64/whichllm) 是一个命令行工具，全自动检测你的硬件配置（GPU/CPU/内存），从 HuggingFace 上筛选出最适合你机器的模型，并按照实际基准测试得分排名。

一句话概括：**一条命令，告诉你哪款本地 LLM 在你电脑上跑得最好。**

它不靠参数数量排序——那些 70B 模型可能根本放不进你的显存，或者即使放进去也慢得无法接受。它用的是真实的基准评测分数（LiveBench、Artificial Analysis、Aider、Chatbot Arena 等），结合你的硬件算力，给出一个综合推荐。

## 核心功能

### 一键推荐

```bash
uvx whichllm@latest
```

不需要安装任何东西，`uvx` 自动拉取并运行。输出结果直接告诉你排名前三的模型，以及预估的推理速度。

```text
$ whichllm --gpu "RTX 4090"

#1  Qwen/Qwen3.6-27B     27.8B  Q5_K_M   score 92.8    27 t/s
#2  Qwen/Qwen3-32B       32.0B  Q4_K_M   score 83.0    31 t/s
#3  Qwen/Qwen3-30B-A3B   30.0B  Q5_K_M   score 82.7   102 t/s
```

注意看：排名第一的不是显存能装下的最大模型（32B），而是综合得分更高的 27B 模型。这就是 whichllm 和"只看显存容量"的工具之间的根本区别。

### 买显卡前的模拟

如果正打算升级显卡，可以模拟不同硬件：

```bash
whichllm --gpu "RTX 5090"
whichllm --gpu "H100"
```

买之前就知道每张卡的实际表现，省得花冤枉钱。

### 反向规划：为模型配显卡

反过来，如果你想跑某个特定模型（比如 Llama 3 70B），可以问它需要什么硬件：

```bash
whichllm plan "llama 3 70b"
```

会告诉你需要多少显存、量化到多少位才能塞进去、预估推理速度是多少。

### 一键运行

选定了模型之后，直接启动对话：

```bash
whichllm run "qwen 2.5 1.5b gguf"
```

它会自动下载最佳量化的 GGUF 版本，初始化推理环境，然后进入交互式聊天。全程不用手动安装 `llama-cpp-python` 之类的依赖。

### 拿到就能用的代码片段

对于需要写代码调用的场景：

```bash
whichllm snippet "qwen 7b"
```

直接打印出一段可复制的 Python 代码，帮你省去查文档的时间。

### 更多实用功能

- `--profile coding` 按使用场景筛选（通用/编程/视觉/数学）
- `--json` 输出 JSON，方便接入脚本和 Pipeline
- `whichllm upgrade "RTX 4090" "RTX 5090"` 对比升级前后的效果
- `--gpu "RTX 4060"` 甚至支持指定显存变体，比如 `"RTX 5060 16"`

## 为什么值得关注

选择本地模型这件事，过去几乎完全依赖社区经验和试错。whichllm 的价值在于把这件事**工程化了**。

它的评分机制很讲究。基准分数按证据可信度加权——直接在目标模型上跑过的评测（direct）权重最高，从同类模型继承的分数（inherited）要打折扣，上传者自报的分数（self-reported）几乎不计入。这样就不会出现"某个小模型借用了大模型的成绩单"这种误导情况。

更关键的是，它的数据是**实时从 HuggingFace API 拉取**的，不是静态快照。这意味着每次运行都能看到最新的模型发布和社区热度变化。

从技术实现上看，它的显存估算考虑了 weights、KV cache、activation 和框架开销，而不是简单用参数量除以 2。对于量化模型的推理速度预估，也按 quantization 类型和 GPU 内存带宽做了精细建模。

## 使用场景

- **刚配了新电脑**——跑一下 whichllm，看看自己这台机器能发挥什么水平
- **打算升级显卡**——先用 `--gpu` 模拟目标显卡，确认提升幅度
- **写代码要用到本地模型**——`whichllm snippet` 直接输出可运行的 Python 代码
- **给团队推荐模型配置**——用 `--json` 输出，集成到自动化脚本里
- **选型对比**——用 upgrade 命令对比多张显卡的性价比

## 安装方式

```bash
# 推荐：一次性使用（零安装）
uvx whichllm@latest

# 或者通过 Homebrew 安装
brew install andyyyy64/whichllm/whichllm

# 或者用 pip 安装
pip install whichllm
```

## 结语

本地模型的选择正在从"凭经验估算"走向"数据驱动"。whichllm 的思路很清晰——不替你判断什么模型好，而是用真实的基准数据加上你机器的实际配置，给出一个你可以信赖的推荐排名。

对于经常在本地跑 LLM 的开发者来说，这个工具省下的时间远比安装它花的时间多。项目目前在 GitHub 上 1800+ star，社区活跃，文档完善，是一个值得放进工具箱的小工具。

项目地址：[github.com/Andyyyy64/whichllm](https://github.com/Andyyyy64/whichllm)
