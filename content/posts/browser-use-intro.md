---
title: "browser-use：让 AI 替你操作浏览器的开源工具"
date: 2026-06-04
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "自动化"]
---

## 一个问题

你有没有遇到过这种场景：想从某个网站批量导出数据，但对方没有开放 API；或者每天需要登录后台，重复点几个按钮下载报表；又或者想自动化一个网页操作流程，但实在不想去写 Playwright/Selenium 的选择器。

以往的解决方案都有痛点。写脚本的话，页面结构一变选择器就失效。用 RPA 工具的话，又太重太贵。其实我们真正需要的，是一个能理解网页内容、根据实际情况灵活操作的自动化工具。

[browser-use](https://github.com/browser-use/browser-use) 就是从这个角度切入的——它让 AI 模型直接操作浏览器，像人一样看屏幕、点按钮、填表单。

## browser-use 是什么

browser-use 是一个 Python 开源项目，核心思路是把 AI 模型（目前支持 GPT-4o、Claude 等）和 Playwright 浏览器自动化结合起来。你给它一个目标，比如"登录后台，找到这周的订单，导出成 CSV"，它就会：

1. 打开浏览器，访问指定 URL
2. 截取当前页面的截图
3. 用 LLM 分析截图，决定下一步做什么（点击哪个按钮、往哪个输入框填什么内容）
4. 执行操作
5. 继续截图、分析、执行，直到目标达成

整个过程你不需要写一句 CSS 选择器或 XPath。AI 通过视觉和理解能力"看懂"页面，而不是通过 DOM 结构。

## 为什么值得关注

### 1. 解决了自动化脚本的最大痛点

传统网页自动化最让人头疼的就是维护成本。今天还能跑的选择器，明天页面改个 class 名就废了。browser-use 通过截图 + 视觉理解来操作页面，相当于从"麻醉师手术"变成了"医生手术"——它看得懂页面内容，而不是按坐标去点击。

### 2. 代码量极少

同样一个任务，用 Playwright 写可能需要几十上百行——定位元素、等待加载、处理异常，每一步都得精确控制。用 browser-use，只需要几行：

```python
from browser_use import Agent
import asyncio

async def main():
    agent = Agent(
        task="访问 github.com/trending，把前 10 个项目名称和星标数记下来",
        llm=LLM(model="gpt-4o")
    )
    result = await agent.run()
    print(result)
```

对比一下传统的 Playwright 方案：定位 `article` 下的 `h2` 标签、提取 `a` 标签的文本、找到 `svg` 旁边的数字……光写选择器就得折腾半天。

### 3. 灵活应对动态页面

遇到 SPA 页面、弹窗、懒加载内容，传统脚本的处理方式往往很脆弱——元素还没渲染就去点击，或者弹窗把元素挡住了。browser-use 通过持续截图和分析，天然能处理这些动态变化。

### 4. 可扩展性强

它提供了注册自定义 Action 的能力。比如你想加一个"滚动到底部"或者"下载所有图片"的操作，可以自己注册。框架本身的设计也比较干净，Action 的定义是基于 Pydantic 模型的，扩展起来很直观。

## 使用示例

先安装：

```bash
pip install browser-use
```

还需要安装 Playwright 的浏览器：

```bash
playwright install
```

设置好 API Key（支持 OpenAI、Anthropic、Google 等）：

```bash
export OPENAI_API_KEY=your-key
```

然后就可以跑了：

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI
import asyncio

async def main():
    agent = Agent(
        task="在百度搜索'2026年最佳开源项目'，把前三个结果的标题和链接记录下来",
        llm=ChatOpenAI(model="gpt-4o")
    )
    result = await agent.run()
    print(result.extracted_content())

asyncio.run(main())
```

它会打开浏览器窗口（可以配置无头模式），你可以看到它一步步操作的过程。执行完之后会返回提取到的结构化内容。

如果你需要更细粒度的控制，可以指定具体 URL，或者让它在多个页面之间导航：

```python
agent = Agent(
    task="1. 打开 GitHub 登录页面\n2. 输邮箱\n3. 输密码\n4. 点登录\n5. 打开我的仓库列表\n6. 找到最新的 Issue，复制内容",
    llm=ChatOpenAI(model="gpt-4o")
)
```

这种多步骤的流程，传统脚本要处理各种等待和异常状态，代码很容易膨胀。browser-use 把这个复杂度封装到了 LLM 的判断逻辑里。

## 适用场景

用了一段时间，我觉得以下几个场景特别合适：

- **数据抓取**：从没有 API 的网站提取数据，尤其是页面结构经常变的
- **表单自动化**：自动填表、提交、截图确认
- **跨系统操作**：需要在多个 Web 系统之间搬运数据，又没有方便的集成接口
- **UI 测试**：给 QA 团队做回归测试，异常情况会自动截图留证
- **日常巡检**：定时登录后台检查某些指标是否正常

但也要说一句实话，它不适合所有场景。如果你的需求是"每秒抓取 1000 个页面"，那用 Playwright/DOM 选择器的传统方案仍然更快。AI 理解截图是要花时间的，而且调用 LLM 有成本。browser-use 更适合对灵活性要求高、对速度要求不那么极致的场景。

## 社区和生态

项目目前还挺活跃，GitHub 上星标接近 3000。文档写得比较清晰，有快速上手的例子，也提供了 Docker 镜像方便部署。遇到问题提 Issue 回复速度还可以。

另外社区的扩展生态也在慢慢起来——有人贡献了对 Hugging Face Space 的支持，有人做了截图缓存来减少 API 调用次数，还有人包装成了 MCP Server 方便和 Cursor 之类的编辑器集成。

## 总结

browser-use 的价值不在于技术多深，而在于它重新思考了"网页自动化到底应该怎么做"这个问题。它放弃了 DOM 选择器这种脆弱的方式，转而用 AI 的视觉理解能力来操作页面——这个方向上的探索本身就很有意义。

如果你经常写爬虫或者做 Web 自动化，建议试试这个项目。它可能不会完全取代 Playwright 或者 Puppeteer，但在很多场景下，它能帮你省下大量的选择和调试时间。项目地址：[browser-use/browser-use](https://github.com/browser-use/browser-use)
