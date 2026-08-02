---
title: "Restterm：把 Postman 塞进终端，一个命令搞定 REST/GraphQL/gRPC 调试"
date: 2026-08-02
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "API"]
description: "Restterm 是一个键盘驱动的终端 API 客户端，支持 REST、GraphQL、gRPC、WebSocket 和 SSE，请求以 .http 纯文本文件保存，可 diff、可 review、可版本管理，还内置 OAuth、SSH 隧道、Mock 服务器和 CI 命令行运行器。"
---

调试 API 时，很多人习惯打开 Postman 或 Insomnia——但请求配置存在云端、要登录、界面笨重，还没法跟代码一起做 Code Review。**Restterm**（[github.com/unkn0wn-root/resterm](https://github.com/unkn0wn-root/resterm)，1827 Stars，Go 编写）是一个键盘驱动的终端 API 客户端，让你在终端里完成一切：REST、GraphQL、gRPC、WebSocket、SSE 全支持，请求是普通的 `.http` 文本文件，可以 diff、可以 review、可以像代码一样进 Git。

## 核心功能

- **五大协议开箱即用**：HTTP、GraphQL、gRPC、WebSocket、SSE，一个工具全覆盖，不用再为不同协议装不同客户端
- **请求即代码**：请求保存在 `.http` 文件里，支持 `@capture`/`@var`/`@assert` 变量与断言、`@workflow`/`@step` 多步流程、`@when`/`@if` 条件逻辑，自动化逻辑直接写在请求文件里
- **内置鉴权与隧道**：OAuth 2.0（含 PKCE）、复用已有 CLI 的认证、SSH 隧道和 Kubernetes 端口转发，无需额外工具
- **Mock 服务器**：用同一份请求文件声明 mock，支持按 query/header/body 匹配、响应序列、调用次数校验、热重载，前后端联调不用等后端
- **CLI 运行器**：`resterm run` 可无界面执行请求文件，输出 JSON/JUnit，直接接入 CI；还有 `--request` 选择器按名字跑单个请求
- **Vim 风格操作**：全键盘控制，`Ctrl+Enter` 发送请求，支持 `/` 搜索、`:w`/`:q` 命令、内联帮助和上下文底栏提示

## 为什么值得关注

首先是**隐私和可移植**：没有账号、没有云同步、没有遥测，一切都在本机，请求文件直接进 Git，团队共享、Review、审计都跟代码一样自然。其次是**一条命令打通日常**：`brew install resterm` 就能用，没有界面负担，SSH 到服务器上也能继续调试。再次是**工程化程度高**：Mock、CI、鉴权、隧道这些"真项目才用得上"的能力都内置了，不是玩具级的 curl 封装。而且它的 headless 包暴露了 Go API，想在自己代码里复用这套请求引擎也完全可行。

## 简单示例

```bash
# 安装并初始化工作区
brew install resterm
mkdir my-api && cd my-api
resterm init          # 生成示例请求和 dev 环境

# 启动 TUI，Ctrl+Enter 发送当前请求
resterm

# 无界面运行：直接执行请求文件，适合 CI
resterm run --request Echo requests.http
```

`resterm init` 会生成指向 httpbin.org 的示例请求和 `resterm.env.json` 环境文件，跑通 Echo 请求即可看到 JSON 响应；`resterm mock ./requests.http` 还能把同一份文件变成本地 Mock 服务。

## 总结

Restterm 的核心理念是"请求即代码"：把 API 调试从图形界面里解放出来，回到开发者最熟悉的终端和 Git 工作流。如果你受够了 Postman 的账号体系和笨重界面，或者经常在服务器上调试接口，它会是顺手又强大的替代品。五协议支持 + Mock + CI 运行器的组合，让它从"好玩的 TUI"直接跃升为可以写进团队工作流的正经工具。
