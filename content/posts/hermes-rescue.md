---
title: "Hermes Rescue：给本地 AI Agent 做的急救包"
date: 2026-05-24
draft: false
tags: ["开源", "Hermes", "macOS", "部署", "工具"]
---

## 为什么做这个工具

用 Hermes Agent 一段时间后，遇到了一个很常见的场景——

某个平台 Bot 没反应了。打开 Web UI 一看，要么是 Gateway 挂了，要么是 API key 过期了，要么是网络代理断了。每次出问题都要在终端里翻来覆去检查好几样东西：进程在不在跑、端口通不通、配置文件对不对。

修本身不难，但反复修同一个问题就有点烦了。

做 Hermes Rescue 的动机很简单：**把检查+修复这件事自动化，变成一个双击能跑的 macOS 工具。**

![Hermes Rescue 的检查流程示意](/images/hermes-rescue-demo.svg)

## 它能干什么

Hermes Rescue 是一个纯 Shell + AppleScript 的工具集，核心脚本 `hermes-client.sh` 提供了几个命令：

```
./hermes-client.sh fix          # 一键检查和修复
./hermes-client.sh doctor       # 只检查不修复
./hermes-client.sh api          # 粘贴 DeepSeek API key
./hermes-client.sh api-custom   # 配置自定义 API 端点
./hermes-client.sh status       # 查看 Gateway 状态
./hermes-client.sh restart      # 强制重启 Gateway
./hermes-client.sh logs         # 查看最近日志
./hermes-client.sh open         # 打开 Hermes Web UI
```

最常用的是 `fix` 命令。它会依次检查：

1. Hermes 安装文件是否存在
2. Web UI 能不能打开（端口 8787）
3. Gateway 是否在运行
4. Gateway API 是否响应（端口 8642）
5. 代理端口 1082 是否正常
6. 最近日志里有没有超时/限流/断连等异常

每项检查都有清晰的 ✓/✗ 标识，发现问题自动修，修完告诉你下一步该做什么。

## macOS App 版本

除了 CLI，还打包了一个 macOS .app 应用，双击启动后弹出一个菜单：

```
Fix Hermes        # 一键修复
Doctor            # 诊断模式
Set DeepSeek API  # 设置 API key
Custom API        # 自定义配置
Open Web UI       # 打开界面
View Logs         # 查看日志
Self Test         # 自检
```

不需要打开终端，点击即可操作。打包脚本也放在 repo 里了，自己跑 `./build-app.sh` 就能生成。

## 技术细节

### 架构

```
Hermes Rescue.app / hermes-client.sh
        │
        ├── fix        → 检查状态 → 发现问题 → 自动修复
        ├── doctor     → 检查状态 → 输出报告
        ├── api        → 备份 config.yaml → 写入新 API key
        └── build-app  → Shell → .app (通过 osa Applescript)
```

### 安全设计

- 无遥测、无上传、无后台更新
- API key 只写入本地的 `~/.hermes/config.yaml`
- 修改配置前先备份（`config.yaml` + `.bak.时间戳`）
- 脚本只读不写系统文件

### 工作原理

`fix` 命令本质上是对 Hermes 的常用故障做了一次覆盖式检查。思路是：

如果一个 Agent 不响应了，先怀疑基础设施（进程、端口、网络），再怀疑配置（API key、代理），最后看日志里的异常信号。

不依赖任何第三方依赖，用 macOS 自带的工具（curl、lsof、pgrep、launchctl）就能跑。

## 实际使用的效果

放一段实际运行的输出：

```
==> 检查 Web UI
✓ Web UI 正常：http://127.0.0.1:8787

==> 检查消息网关
! 网关没在跑，开始自动拉起

==> 启动 Hermes Gateway
✓ 网关已恢复
running      : true
configured   : true
platforms    : [{"name": "weixin", "label": "Weixin"}]

==> 下一步
1. 微信 Bot 不回话？发一句"在吗"测试。
2. 如果回复很慢：检查 API 超时或限流提示。
3. 如果 Telegram 不通：确认代理客户端和 1082 端口。
4. 如果模型 API 挂了：运行 ./hermes-client.sh api 粘贴新 key。
```

最常修的两个问题：Gateway 进程意外退出、API key 过期。这两样占了 80% 的"Bot 不回复"场景。

## 这个项目有谁在用

目前主要是 Hermes Agent 的用户。如果你：

- 用 `hermes gateway run` 跑 Agent
- 遇到过 Bot 不回复的情况
- 每次排查都要查好几个地方
- 想让家人或非技术同事也能一键重启 Agent

那这个工具可能对你有用。

## 关于开源

项目是 MIT 许可，开源在 [github.com/makismkuo/hermes-rescue](https://github.com/makismkuo/hermes-rescue)。配置、打包、发布都有现成脚本。

后续计划加的功能：

- 更多平台适配（目前只跑过 macOS Sequoia）
- Telegram 代理健康检查的增强
- 定时自检+告警

有什么想法欢迎提 issue。

——Seb
