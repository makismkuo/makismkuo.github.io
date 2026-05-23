---
title: "Crawl4AI：现代网页抓取工具实测"
date: 2026-05-23
draft: false
tags: ["部署", "爬虫", "Crawl4AI", "Python"]
---

## 为什么选 Crawl4AI

传统爬虫工具（Scrapy、BeautifulSoup）配置复杂，遇到 JavaScript 渲染的页面还得上 Selenium。

Crawl4AI 的亮点：**一次调用，自动处理 JS 渲染、动态内容、反爬。**

## 适用场景

| 场景 | 推荐工具 |
|------|---------|
| 公开网页内容 | Crawl4AI |
| 有历史数据的内容平台 | MediaCrawler（JSONL） |
| 需要交互（登录、点击） | Playwright / CDP |

Crawl4AI 最适合第一种——我要抓的网站内容不需要登录，但可能是 SPA 单页应用，传统爬虫拿不到数据。

## 使用方式

```python
from crawl4ai import WebCrawler

crawler = WebCrawler()
result = crawler.run(url="https://example.com")
print(result.markdown)
```

默认输出 Markdown 格式，直接可以喂给 LLM 做分析。

## 注意

- 对极度反爬的网站（Cloudflare 5秒盾）效果有限
- 大规模抓取注意控制频率，别把目标站打挂
