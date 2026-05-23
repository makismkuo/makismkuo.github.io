---
title: "搭建 sub2api AI API 中转：省钱又灵活"
date: 2026-05-23
draft: false
tags: ["部署", "sub2api", "API", "服务器"]
author: "Seb"
---

## 为什么需要 API 中转

做 AI 开发时间长了，手里攒的模型越来越多：OpenAI 的 GPT-4o、Claude 的 Sonnet 4、DeepSeek 的 V3 和 R1、还有本地跑的 Llama……每个模型都有自己的 API Key、独立的接口地址、不一样的计费方式。

一开始没啥感觉，反正写死一个模型也能用。但当你开始做稍微复杂点的项目——比如一个 Telegram Bot 同时接了好几个模型，或者你在做 RAG 应用需要根据任务类型自动选模型——这时候问题就来了：

- 代码里到处都是不同的 base_url 和 api_key
- 想换模型，得改代码、重新测试、重新部署
- 某个模型挂了切到另一个，手忙脚乱
- 月底对账一看，每个平台各算各的，根本理不清到底花了多少钱

**sub2api 就是来解决这些问题的。** 它本质上是一个轻量级的反向代理层，把你的所有 API 请求统一到一个入口。你的代码只认一个地址、一个 Key，背后路由到哪个模型由 sub2api 说了算。

## 架构概览

```
┌─────────────────┐     ┌──────────┐     ┌──────────────┐
│  你的客户端代码  │────▶│ sub2api  │────▶│  OpenAI      │
│  (Bot/Agent/App) │     │  (中转)   │     ├──────────────┤
└─────────────────┘     │          │     │  Claude      │
                        │          │     ├──────────────┤
                        │          │     │  DeepSeek    │
                        │          │     ├──────────────┤
                        │          │     │  其他/本地    │
                        └──────────┘     └──────────────┘
```

客户端看到的就是一个标准的 OpenAI 兼容 API。你传一个请求过来，sub2api 根据你指定的模型名，自动决定转发到哪个后端，拿到响应后再原样返回给你。中间的所有差异——不同厂商的认证方式、请求格式、响应结构——都由它来抹平。

## 部署

### 环境准备

sub2api 用 Go 写的，单二进制文件就能跑，部署非常轻量。推荐放在香港或新加坡的服务器上，国内直连速度快，延迟低。

```bash
# 下载最新版
wget https://github.com/songquanpeng/sub2api/releases/latest/download/sub2api-linux-amd64.tar.gz
tar -xzf sub2api-linux-amd64.tar.gz

# 给执行权限
chmod +x sub2api
```

或者直接用 Docker：

```bash
docker run -d \
  --name sub2api \
  -p 8080:8080 \
  -v $(pwd)/config.yaml:/etc/sub2api/config.yaml \
  songquanpeng/sub2api
```

### 配置文件详解

核心就一个 YAML 文件，里面定义所有后端的接入信息。下面是一个完整的配置示例，覆盖了最常见的几种场景：

```yaml
# /etc/sub2api/config.yaml

server:
  listen: ":8080"
  # 可以用自定义路径前缀，默认空
  base_path: ""
  # 全局限流（每秒请求数），0 表示不限
  rate_limit: 0

# 日志级别：debug / info / warn / error
log:
  level: info
  # 日志文件，不配就输出到 stdout
  file: /var/log/sub2api/access.log

# Token 管理：客户端调用时携带的 API Key
# 可以配多个，每个可以有不同权限
tokens:
  - key: "sk-my-master-key"
    name: "master"
    rate_limit: 100
  - key: "sk-bot-key"
    name: "telegram-bot"
    models:                                 # 限制只能调特定的模型
      - gpt-4o
      - claude-sonnet-4
    rate_limit: 30
    quota: 1000000                          # 配额，单位 token（可选）

# 模型路由配置
models:
  # 可以直接使用模型的原名
  gpt-4o:
    provider: openai
    api_key: sk-proj-xxxxxxxxxxxxxxxx
    # 可以不配 base_url，用默认的
    # base_url: https://api.openai.com/v1

  # 也可以给它换个名字
  deepseek-chat:
    provider: deepseek
    api_key: sk-xxxxxxxxxxxxxxxx
    base_url: https://api.deepseek.com/v1

  # Claude 的配置稍有不同，需要额外配一个 version header
  claude-sonnet-4:
    provider: anthropic
    api_key: sk-ant-xxxxxxxxxxxxxxxx
    # Anthropic 需要 version 头
    headers:
      anthropic-version: "2023-06-01"

  # 本地模型通过 Ollama 接入
  local-llama:
    provider: openai
    api_key: not-needed
    base_url: http://localhost:11434/v1
    model_mapping:
      model_name: llama3.1

  # 支持改名，但我不建议这样做
  # gpt-4-turbo:                       # <-- 客户端传这个名
  #   provider: deepseek               # <-- 实际走的是 DeepSeek
  #   api_key: sk-xxxxxxxxxxxxxxxx
  #   base_url: https://api.deepseek.com/v1
```

重点说几个参数：

- **`tokens` 下的 `models` 字段**：可以限制某个 token 只能访问特定的模型。比如给 Telegram Bot 的 token 只开放 GPT-4o 和 Claude，不给它访问 DeepSeek 的权限。
- **`quota`**：配额限制，按 token 计费。到了配额自动拒绝请求，防止失控。
- **`rate_limit`**：支持全局限流和 token 级别的限流双重控制。
- **`model_mapping`**：如果后端模型名和你配置的不一样，可以在这里映射。例如 local-llama 在服务端叫 `llama3.1`，但客户端传的是 `local-llama`。

### 启动运行

```bash
./sub2api --config /etc/sub2api/config.yaml
```

默认监听 8080 端口，用 systemd 管理起来就可以跑在生产环境了：

```ini
# /etc/systemd/system/sub2api.service
[Unit]
Description=sub2api API Proxy
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/sub2api --config /etc/sub2api/config.yaml
Restart=always
RestartSec=10
User=nobody

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now sub2api
```

## 客户端接入

不管你在服务端配了多少模型，客户端看 sub2api 就是一个标准的 OpenAI 兼容 API。对接方式完全一致：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://your-sub2api.com/v1",
    api_key="sk-bot-key"          # 上面配置的 token
)

# 调用，模型名必须和配置文件严格一致
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "你好"}]
)
```

**关键原则：不要在客户端写死模型切换逻辑。** 客户端只负责发请求，模型路由全交给服务端。想换模型，改服务端配置重启就行，客户端代码一行不动。

## 部署实战中踩过的坑

### 模型名必须完全一致

这个我吃过大亏。配置里写的是 `deepseek-chat`，客户端传的是 `deepseek`，结果 sub2api 找不到匹配的模型，返回 404。排查了大半个小时才意识到名字对不上。

**解决方法：** 建立命名规范。我会在配置文件的注释里标明每个模型的对外名称，客户端开发者也以这个注释为准。加新模型时两边同步确认。

### 日志是最好的调试工具

sub2api 的日志非常详细，每条请求都会记录：

```
[2026-05-23 10:15:32] POST /v1/chat/completions
  → model: gpt-4o
  → token: sk-bot-key (telegram-bot)
  → status: 200
  → prompt_tokens: 520, completion_tokens: 180
  → duration: 1.32s
```

碰到问题先看日志：模型名对不对、token 有没有权限、响应时间是否正常——一目了然。

### 关于模型改名（真不建议）

sub2api 支持把一个模型伪装成另一个名字，比如把 DeepSeek 的接口配置成 `gpt-4-turbo` 的名字。有些人会这么做，原因无非是想让客户端不用改代码就能用不同模型。

**我的建议是：别这么干。** 原因有三：

1. **调试时极度痛苦**——日志里显示调用的是 `gpt-4-turbo`，实际扣费走的是 DeepSeek，对账根本对不上
2. **不同模型的能力边界不同**——你以为在调 GPT-4o，结果实际是 DeepSeek，输出了不符合预期的内容，排查起来一头雾水
3. **不够诚实**——如果接口是给团队或客户用的，改名等于在掩盖真实使用的模型，出了问题很难解释

正确的做法是：服务端配一个统一的名字（比如 `fast-model`），在注释里说明它当前指向哪个后端。切换时改配置、重启、通知相关方。透明比任何"聪明"的做法都省心。

## 实际使用感受

我现在把 Telegram Bot 和 Hermes Agent 都接入了 sub2api。

最实用的场景是：某个模型挂了或者限流严重时，我不需要改任何客户端代码，只需要在 sub2api 的配置文件里把路由切换一下，重启服务就行。对客户端来说，接口地址没变、API Key 没变、模型名没变，完全无感。

用量统计也很方便。sub2api 自己就有日志和统计，不用去每个平台的后台查账。每个月花在 AI 上的钱，一眼就能看清楚。

## 适合谁用

如果你只用一个模型、跑个小玩具，sub2api 确实用不上。但如果你：

- **同时用 3 个以上的模型**，不想在代码里到处写 API Key
- **做产品/服务**，需要统一管理团队成员的 API 调用
- **需要用量控制和计费**，防止某个服务把预算跑光
- **经常在不同模型之间切换**，对比效果或做 A/B 测试

那 sub2api 能帮你省下不少折腾的时间。配置一次，后面就清净了。

## 总结

sub2api 做的不是什么复杂的事，它就是把你从一堆 API Key 和接口地址的琐碎管理中解放出来。一个入口、一份配置、一个统一的日志和统计，原理简单，但用起来很顺手。

部署起来也不费劲：一个二进制文件、一个 YAML 配置文件，十分钟就能跑起来。核心就记住一条——**服务端做路由，客户端做业务**，各司其职，代码就会清爽很多。
