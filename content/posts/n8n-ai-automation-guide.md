---
title: "n8n：不只是自动化工具，你的 AI 代理也该用它"
date: 2026-06-22
draft: false
tags: ["开源", "推荐", "自动化", "AI工具", "Docker", "n8n", "工作流"]
---

今年 4 月，n8n 宣布完成 6000 万美元 B 轮融资。一个做流程自动化的开源项目，在资本寒冬过去还能拿到这么一轮，说明了几件事：一是企业级工作流自动化的大浪确实来了，二是自部署类的工具正在从"geek 玩具"变成正经的采购项。

融资多少我不评价，但 n8n 过去两年的变化才更值得聊——它从一个"可视化 Zapier 替代品"，进化成了一套 AI Agent 的基础设施。

去年开始，n8n 陆续加入了 **AI Agent 节点**、**LangChain 集成**、**MCP 支持**。现在你可以用它编排一个完整的 AI 工作流：LLM 判断意图 → 调用 API 取数 → 结构化输出 → 触发下游动作。整个过程在可视化界面上拖拽完成，不需要写一行后端胶水代码。

我把它部署在自己的服务器上跑了两个月，有些感受值得记一笔。

## n8n 到底是什么

一句话：**n8n 是一个开源的工作流自动化引擎，支持自部署。**

核心概念很简单——你通过拖拽节点来构建流程。一个流程的基本骨架：

```
[触发器] → [数据处理] → [API 调用] → [输出/存储]
```

每个方块都是一个"节点"（Node），节点之间用连线相连，数据在节点间流动。n8n 内置了 **400+ 个节点**，覆盖从 HTTP 请求、数据库操作、邮件发送到 Slack 通知、AI 模型调用等各种能力。

安装方式也很直接——Docker 一行就搞定，数据存本地，没有外部依赖。

### 如果你用过 Zapier…

可以把 n8n 理解为 Zapier 的开源自部署版本。概念几乎一样：触发器（Webhook、定时、邮件）→ 动作（发 Slack 消息、写数据库、调 API）。区别就两点：

- **数据不过第三方**。Zapier 的所有执行发生在它的服务器上，你的业务数据要经过一次外部传输。n8n 跑在你自己的服务器上，数据不出边界。
- **全部可控**。自定义节点、JavaScript 代码块、条件分支、循环——n8n 的灵活性比 Zapier 高一个数量级，代价是你得自己维护它。

## n8n vs 其他自动化工具（一张表说清楚）

很多人会在 n8n、Make（原 Integromat）和 Huginn 之间纠结。我的看法：

| 维度 | n8n | Make (Integromat) | Huginn |
|------|-----|-------------------|--------|
| 开源 | ✅ MIT 协议 | ❌ 闭源 SaaS | ✅ MIT 协议 |
| 自部署 | ✅ Docker | ❌ | ✅ Docker |
| 界面 | 可视化拖拽 | 可视化拖拽 | 纯配置（无 GUI） |
| AI Agent | ✅ 原生支持 | ❌ | ❌ |
| 节点数量 | 400+ | 1000+ | 50+ |
| 社区版限制 | 无 | N/A（免费版有限） | 无 |
| 上手难度 | 低 | 低 | 高 |

Huginn 虽然也开源，但它是**配置驱动的**——你要写 YAML 或者 Ruby 脚本来定义 agent。对开发者来说倒不是不能接受，但要给非技术队友用就麻烦了。Make 的体验最好，但 SaaS 贵且数据要走第三方。

n8n 站在了两者之间：可视化拖拽降低门槛，开源自部署保留自由度，AI Agent 节点是加分项。

## 💡 用 Docker 部署，十分钟上手

部署 n8n 我踩过一次坑——社区版默认用 SQLite，数据量大了会慢。如果你准备长期用，建议直接上 PostgreSQL。

```yaml
# docker-compose.yml
version: "3.8"
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_DATABASE_TYPE=postgresdb
      - N8N_DATABASE_POSTGRESDB_HOST=postgres
      - N8N_DATABASE_POSTGRESDB_DATABASE=n8n
      - N8N_DATABASE_POSTGRESDB_USER=n8n
      - N8N_DATABASE_POSTGRESDB_PASSWORD=your_password
      - N8N_SECURE_COOKIE=false  # 开发环境用，生产环境改 true
    volumes:
      - ./n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=your_password
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
```

启动：

```bash
docker compose up -d
```

打开 `http://你的IP:5678`，注册管理员账号，就可以开始拖拽了。

💡 **小贴士**：部署时加个反向代理（Nginx/Caddy）配 HTTPS，不然 Webhook 触发不了——不少外部服务（GitHub、Slack）要求回调地址是 HTTPS。

## 三步做出第一个实际可用的工作流

### Step 1：定时抓 RSS + AI 摘要

这是最实用的入门场景。我每天用这个工作流来自动抓取几个技术博客的 RSS，让 AI 生成摘要后推送到 Telegram。

节点链路：

```
[Schedule] → [RSS Feed Read] → [Code: 格式化内容] → [OpenAI: 生成摘要] → [Telegram: 发送消息]
```

1. **Schedule** 设置每天 9:00 触发
2. **RSS Feed Read** 填入 RSS 地址，设置 `maxItems: 5`
3. **Code 节点**（JavaScript）把标题和链接拼接成一段文字
4. **OpenAI 节点** 填 API Key，prompt 写"用三句话总结以下文章，保持中文"
5. **Telegram 节点** 填入 Bot Token 和 Chat ID

跑起来之后，每天早上自动收到 AI 帮你读过的技术早报。

### Step 2：Webhook + AI 邮件分类

第二步接入外部事件。用 Webhook 接收邮件转发 → AI 判断分类 → 写入 Notion 数据库。

```
[Webhook] → [OpenAI: 分类判断] → [Switch: 按类别路由] → [Notion: 创建记录]
```

这个工作流的妙处在于 **Switch 节点**——AI 返回"bug/report/question/other"后，Switch 把不同的结果路由到不同的 Notion 数据库。Bug 类进 bug tracker，Question 类进 FAQ 库。不写一行 if-else。

### Step 3：AI Agent 自主执行（高级）

这是 n8n 从 1.40 版本开始最亮眼的能力——**AI Agent 节点**。

你给 Agent 一个任务描述，它自己决定调用哪些工具来完成：

```
[Chat Trigger] → [AI Agent] → 内部自动路由到工具节点 → [Respond to Webhook]
```

Agent 可以调用的工具包括：搜索引擎、计算器、数据库查询、HTTP 请求、任何自定义 API。配置方式是在 Agent 节点的"Tools"列表里勾选可用工具。

我实际用它做了一个"技术方案调研助手"：在聊天框输入"帮我调研 Postgres vs MySQL 在自部署场景下的差异"，Agent 自己去搜文档、对比特性、输出结构化对比表。整个过程的编排不用写代码。

## 硬约束：n8n 不是万能的

两个月跑下来，有几点必须坦诚说：

**社区版没有高级权限管理**。不能精确控制"每个用户能看哪些工作流"。团队协作的话，要么用付费版（n8n Cloud），要么在外面套一层 Nginx 做基本隔离。

**复杂流程的调试体验一般**。看到某个节点报错，点进去只能看到 JSON 日志，没有 step-through 调试器。对于超过 20 个节点的流程，排查问题靠运气居多。

**执行性能有上限**。社区版不支持横向扩展，所有工作流跑在同一个 Node.js 进程里。如果你的场景需要每秒几千次执行（高并发 Webhook），n8n 不是合适的方案——选 Temporal 或者 Airflow 更靠谱。

**AI Agent 节点实打实烧 token**。每次 Agent 调用都会产生多轮 LLM 往返，一次"帮我查个资料"可能烧掉你 5000-10000 tokens。跑之前估算好成本。

## 什么时候该用 n8n

✅ **适合的场景：**

- 个人/小团队的自部署自动化需求
- 需要 AI 参与决策的工作流（分类、摘要、判断）
- 跨系统数据同步（A → B，定时或事件触发）
- 替换 Zapier/Make 的高成本方案
- 数据敏感不能走第三方 SaaS

❌ **不适合的场景：**

- 企业级权限管理要求高
- 高吞吐量的实时系统
- 核心业务依赖的流程（n8n 本身挂了怎么办？）
- 需要 CICD 级可靠性保障

## 聊聊我的感受

用了一段时间后，我对 n8n 的定位有了新的认识——**它不是一个"拖拽版 Node-RED"**，更像是**可视化的胶水代码生成器**。

过去你要串联两个服务，要么写一个 Python 脚本跑 cron，要么写一个 Serverless Function 挂着。最麻烦的不是写代码，是处理异常、重试、日志、状态管理。n8n 把这些内建了——每个节点都有自动重试、错误处理分支、执行日志，相当于把后端开发中最无聊的部分抽出来交给你拖拽。

AI Agent 的加入让事情更有趣。以前"自动化"是固定的 if-this-then-that，现在 Agent 能在推理层面做判断——不是"如果是邮件 A 就转发"，而是"判断这封邮件的意图并路由到合适的地方"。这是一个量级的变化：**从规则驱动到意图驱动**。

当然，它还没有到"非技术用户也能用"的程度。环境变量、JSON 解析、Webhook 签名验证，这些概念对不会编程的人来说仍然有门槛。但它让一个前端/全栈开发者，花十分钟就能搭出一个过去要写一天的后端胶水服务。

如果你也在自部署各种服务，n8n 值得放进你的工具箱。

> 项目地址：[github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
> 本文的 Docker Compose 配置也在我的 [GitHub 仓库](https://github.com/makismkuo) 里可以找到。

——Seb
