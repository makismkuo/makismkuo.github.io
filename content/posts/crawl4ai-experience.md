---
title: "对比了几款网页爬虫，我选了 Crawl4AI"
date: 2026-05-23
draft: false
tags: ["部署", "爬虫", "Crawl4AI", "Python"]
---

## 爬虫工具的选择

写爬虫的需求大多数人都会遇到——想从某个网站上抓取一些内容做分析。

传统的爬虫工具大致分两类。一类是 Scrapy 这样的完整框架，功能强大，但配置复杂。写一个简单的抓取任务可能需要定义 Item、Pipeline、Middleware 等多个组件。另一类是 Requests + BeautifulSoup 的组合，上手简单，但遇到 JavaScript 渲染的页面就无能为力了。

Crawl4AI 的出现填补了两者之间的空白。它的定位是"专为 LLM 时代设计的爬虫工具"。

## 为什么选 Crawl4AI

最大的理由是它对 JavaScript 渲染的支持。现在的网页大部分是前后端分离的，数据通过异步请求加载，页面最终内容由 JavaScript 渲染生成。如果用传统爬虫去抓取这类网站，拿到的是空的 HTML 骨架，真正的数据根本不在这里。

Crawl4AI 内置了浏览器引擎，会自动执行页面上的 JavaScript，等页面完全渲染后再提取内容。这意味着你不必为了一个需要 JS 渲染的页面去额外配置 Selenium 或 Playwright。

另外，它的默认输出格式是 Markdown。这个细节在实际使用中很实用——抓取到的内容可以直接喂给 LLM 做分析，省去了格式转换的步骤。

## 安装和基本使用

Crawl4AI 的安装很简单，一行命令搞定：

```bash
pip install crawl4ai
```

装完之后跑一个小例子试试：

```python
from crawl4ai import WebCrawler

crawler = WebCrawler()
result = crawler.run(url="https://example.com")
print(result.markdown)
```

默认输出就是 Markdown，干净整洁。如果你需要原始 HTML，也可以拿到：

```python
print(result.html)        # 原始 HTML
print(result.extracted_content)  # 提取后的内容
```

## 更高级的抓取配置

实际项目里，一条 URL 裸跑往往不够。Crawl4AI 提供了丰富的配置选项，这里分享几个常用的场景。

### 设置超时和等待

有的页面加载很慢，尤其是那些带大量图片和图表的网站。可以给爬虫指定最长等待时间：

```python
result = crawler.run(
    url="https://example.com/slow-page",
    wait_until="networkidle",   # 等待网络请求空闲
    timeout=30                  # 最长等 30 秒
)
```

`wait_until` 参数有几个选项：
- `"domcontentloaded"` — DOM 解析完毕即可，不等待图片等资源
- `"load"` — 等待所有资源加载完成
- `"networkidle"` — 网络请求空闲后（推荐给 SPA 单页应用）

### 提取特定内容

有时候你不需要整个页面的内容，只需要某个区域。可以用 CSS 选择器来限定范围：

```python
result = crawler.run(
    url="https://example.com",
    css_selector="article.main-content"
)
```

这样只会提取 `<article class="main-content">` 里的内容，去掉导航栏、广告、页脚等噪音。配合 LLM 分析的时候，这个功能非常实用——大量无关内容会影响模型的理解质量。

### 批量抓取

如果需要抓取多个页面，可以用 `run_many`：

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

results = crawler.run_many(urls, concurrency=3)
for result in results:
    print(f"抓取完成: {result.url}")
    # 保存到文件
    with open(f"output/{result.url.split('/')[-1]}.md", "w") as f:
        f.write(result.markdown)
```

`concurrency` 控制并发数量，建议不要设太高，以免被目标网站封 IP。我一般控制在 3 到 5 之间。

## 实战：抓取一个 Vue 开发的文档站

前不久我需要抓取一个 Vue 开发的文档站点，把所有页面内容导出成 Markdown 做本地检索。这个站点是典型的 SPA，所有路由都在前端控制，传统爬虫根本拿不到数据。

用 Crawl4AI 一套搞定：

```python
from crawl4ai import WebCrawler
import os

crawler = WebCrawler()
base_url = "https://docs.example.com"
pages = [
    "/getting-started",
    "/installation",
    "/configuration",
    "/api/reference",
    "/api/examples",
]

os.makedirs("docs_output", exist_ok=True)

for page in pages:
    url = base_url + page
    print(f"正在抓取: {url}")
    
    result = crawler.run(
        url=url,
        wait_until="networkidle",
        timeout=20
    )
    
    if result.success:
        filename = page.replace("/", "_").strip("_") + ".md"
        filepath = os.path.join("docs_output", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {result.title}\n\n")
            f.write(result.markdown)
        print(f"  保存到 {filepath}")
    else:
        print(f"  抓取失败: {result.error_message}")
```

跑了大概两分钟，所有页面全部抓完。之前用 Scrapy + Selenium 配过类似的任务，花了大半天时间调中间件和代理，Crawl4AI 确实省事不少。

## 关于反爬的处理

很多朋友关心 Crawl4AI 能不能过 Cloudflare。老实说，效果有限。Cloudflare 的 5 秒盾在浏览器层面做人机检测，自动化工具很难绕过。

但也不是完全没招。有几个小技巧可以试试：

```python
result = crawler.run(
    url="https://example.com",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
    disable_security=True,
    headless=False  # 非无头模式运行，减少被检测的风险
)
```

- 设置合理的 User-Agent，不要用默认的
- 关闭无头模式，虽然会弹出浏览器窗口，但更像真实用户
- 控制抓取频率，加一些延迟

但说句实话，如果目标网站开了严格模式的 Cloudflare 防护，还是放弃吧，换别的途径获取数据更高效。

## 不同场景的工具选择

根据自己的使用经验，我整理了一个简单的选型参考：

- **抓取公开网页内容，不需要登录**：Crawl4AI 足够了
- **抓取 SPA 单页应用**：Crawl4AI 的 `networkidle` 模式很好用
- **需要抓取社交媒体平台的历史数据**：MediaCrawler 更合适，它对小红书、微博等平台的登录和反爬处理更完善
- **需要模拟用户操作、填表单、点按钮**：用浏览器自动化工具 Chrome CDP 或者 Playwright
- **大规模数据采集**：Scrapy + 分布式架构仍然是工业级选择

## 结语

Crawl4AI 的优点在于上手快、配置少、开箱即用。尤其适合做 AI 相关项目的时候，从网页上抓取素材喂给 LLM。项目地址在 GitHub 上搜 craw4ai 就能找到，目前社区也挺活跃，遇到问题基本能搜到解决方案。

如果你对爬虫的需求刚好是"不需要登录，但页面是动态渲染的"，Crawl4AI 的性价比比 Scrapy + Selenium 的组合要高很多。装个包，跑个脚本，几分钟就能把数据拿到手。
