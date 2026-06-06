---
title: "Codex Desktop 一直 Reconnecting？先查代理"
date: 2026-06-06
draft: false
tags: ["Codex", "网络", "代理", "macOS", "AI工具"]
---

## 先说现象

最近不少人遇到一个很烦的问题：Codex Desktop 每次打开，或者刚开始提问时，总会先来几次 `Reconnecting`。有时候是 3 次，有时候是 5 次，最后可能连上，也可能直接卡住。

这个问题看起来像是 Codex 不稳定，或者模型接口抽风。但我这次排下来，更多时候不是模型的问题，而是网络链路的问题。

更准确一点说：**Codex Desktop 要走的连接，没有被你的代理环境稳定接住。尤其是 WebSocket / WSS 这类长连接，在某些代理配置里特别容易出问题。**

![Codex Desktop Reconnecting 代理修复示意图](/images/codex-reconnecting-proxy.svg)

## 为什么会这样

普通网页请求失败了，大不了重新请求一次。但 Codex Desktop 这种工具不是普通网页。它需要持续和后端服务保持通信，过程中会涉及流式响应、长连接、工具调用状态同步。

如果你的网络环境是这样：

```text
Codex Desktop → 系统网络 → 代理软件 → 外网服务
```

但 Codex 没有正确读到代理，或者 WebSocket 没有被代理软件正确转发，就会出现一个很典型的表现：

```text
打开 Codex
开始连接
断一下
Reconnecting
再断一下
Reconnecting
重复几次
```

所以这类问题不要一上来就怀疑账号、模型、插件。先看代理链路。

## 三种解决方案

### 方案一：给 Codex 明确写代理环境变量

这是我最推荐先做的一步。思路很简单：不要让 Codex 自己猜代理，直接告诉它 HTTP/HTTPS 代理在哪。

在 macOS 上，先看系统代理端口：

```bash
scutil --proxy
```

如果看到类似：

```text
HTTPEnable : 1
HTTPProxy : 127.0.0.1
HTTPPort : 1082
HTTPSEnable : 1
HTTPSProxy : 127.0.0.1
HTTPSPort : 1082
```

那就说明系统 HTTP/HTTPS 代理入口是：

```text
127.0.0.1:1082
```

然后创建或更新：

```text
~/.codex/.env
```

写入：

```env
HTTP_PROXY="http://127.0.0.1:1082"
HTTPS_PROXY="http://127.0.0.1:1082"
```

注意，不要照抄我的端口。你的代理端口可能是 `7890`、`7897`、`1080`、`1082`，要以自己机器上的实际端口为准。

写完之后，完全退出 Codex Desktop，再重新打开。

### 方案二：开启 Clash Verge 的 TUN 模式

如果你用的是 Clash Verge，一种更粗暴但有效的办法是开启 TUN 模式。

TUN 模式的作用是从系统底层接管流量。这样很多不会主动读取系统代理的程序，也能被强制带进代理链路里。

它的好处是省心，坏处是影响范围更大。开了以后，不只是 Codex，其他应用的网络也可能一起被接管。所以如果你本来就有一套比较复杂的本地网络规则，开启前最好心里有数。

我的建议是：

- 只修 Codex：优先写 `~/.codex/.env`
- 多个软件都出网异常：再考虑 TUN 模式

### 方案三：禁用 WebSocket，改走 Responses

还有一种方案是在 Codex 的 `config.toml` 里，对 provider 做更明确的配置：

```toml
wire_api = "responses"
supports_websockets = false
```

这个思路是：既然当前网络环境下 WebSocket 容易断，那就别让它走 WebSocket。

但我不建议一上来就改这个。原因很简单：`config.toml` 里往往还有模型、插件、项目权限等配置，乱改容易把别的东西带坏。除非你清楚自己正在改哪个 provider，否则先从 `.env` 代理入手更稳。

## 我这次本机怎么修的

我本机的系统代理检查结果是：

```text
HTTPProxy : 127.0.0.1
HTTPPort  : 1082
HTTPSProxy: 127.0.0.1
HTTPSPort : 1082
```

所以我创建了：

```text
/Users/makismkuo/.codex/.env
```

内容是：

```env
HTTP_PROXY="http://127.0.0.1:1082"
HTTPS_PROXY="http://127.0.0.1:1082"
```

然后做了两步验证：

```bash
nc -vz 127.0.0.1 1082
```

确认端口能连上。

再用代理访问一个 HTTPS 地址，看到：

```text
HTTP/1.1 200 Connection established
```

这就说明代理隧道是能建立的。

最后重启 Codex Desktop。

## 一个简单排查顺序

以后再遇到 Codex 一直重连，我会按这个顺序查：

1. 先看代理软件是否开着
2. 用 `scutil --proxy` 找到当前 HTTP/HTTPS 端口
3. 检查 `~/.codex/.env` 里的端口是否一致
4. 用 `nc -vz 127.0.0.1 端口` 测试端口
5. 重启 Codex Desktop
6. 还不行，再考虑 TUN 模式或禁用 WebSocket

这类问题最烦的地方在于，它不像代码报错那样给你一个明确位置。它更像网络中间某一段接触不良：看起来是应用卡住，实际是代理没接住。

所以别急着大修。先把代理入口写清楚，很多 `Reconnecting` 就会安静下来。

——Seb
