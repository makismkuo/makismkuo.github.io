---
title: "OKX 合约交易机器人：双均线策略实战"
date: 2026-05-23
draft: false
tags: ["部署", "交易", "OKX", "Python"]
---

## 思路

最简单的趋势跟随策略：双均线金叉死叉。

- MA5 上穿 MA20 → 开多
- MA5 下穿 MA20 → 开空/平仓
- 1 分钟 K 线，3 倍杠杆

源码基于 CCXT 库，连接 OKX 交易所 API。

## 参数调优

当前配置（小号 68U 测试）：

| 参数 | 值 |
|------|-----|
| 每单金额 | 50 U |
| 杠杆 | 3x |
| 止盈 | 0.3% |
| 止损 | 0.15% |

## 部署

跑在 HK 服务器上，systemd 托管：

```
/opt/okx-bot/
├── bot.py          # 主逻辑
├── config.yaml     # API Key + 参数
└── okx.service     # systemd 单元
```

## 注意

- 需要先在 OKX 开通 API 交易权限
- 小资金先跑，观察胜率再调整参数
- Telegram Bot 通知开平仓，手机随时看
