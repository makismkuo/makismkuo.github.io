---
title: "网页抓取新选择：我为什么换掉了 Scrapy"
date: 2026-05-23
draft: false
tags: ["部署", "爬虫", "Crawl4AI"]
---

## 旧时代的痛苦

如果你用过 Scrapy，你应该知道那种感觉：配置一个爬虫的时间，比手动复制粘贴还长。

而且现在网页越来越"现代"了——内容是用 JavaScript 动态渲染的，你以为你抓到了数据，结果打开一看全是 `<div id="root"></div>`。

我受够了。

## 遇到了 Crawl4AI

它是那种"一用就回不去"的工具。不仅自动处理 JavaScript 渲染，还能直接输出 Markdown 格式——喂给 AI 分析刚刚好。

```python
from crawl4ai import WebCrawler

crawler = WebCrawler()
result = crawler.run(url="https://example.com")
print(result.markdown)  # 直接出 Markdown
```

## 什么时候用它

用了一段时间，总结了一套选型标准：

| 需求 | 用这个 |
|------|--------|
| 抓公开网页内容 | Crawl4AI |
| 爬小红书/微博等平台的历史数据 | MediaCrawler |
| 需要登录、交互、填表单 | Playwright / Chrome CDP |

Crawl4AI 最适合第一种——不用登录、不用交互，但页面是动态渲染的。这也是最常见的场景。

## 一个小遗憾

遇到开了 Cloudflare 5 秒盾的网站，它也没办法。这不能怪它——Cloudflare 那玩意连正经浏览器都要验证一下你是不是机器人。

不过大多数网站没那么狠。够用了。
