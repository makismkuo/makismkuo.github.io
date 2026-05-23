---
title: "写了个交易机器人：双均线策略的实盘记录"
date: 2026-05-23
draft: false
tags: ["部署", "交易", "OKX", "Python"]
---

## 为什么写交易机器人

做量化交易的人大概都有类似的想法：K 线不用一直盯着，让机器来执行策略，人在旁边看着就好。这样既不会被情绪左右，也不用天天坐在屏幕前。

这个想法本身没有问题，但实盘跑起来之后，你会发现很多细节是回测时根本想不到的。这篇文章主要记录我用 Python + CCXT 写的一个 OKX 合约交易机器人，从策略设计到部署上线的完整过程，希望能给同样在尝试的朋友一些参考。

![双均线策略逻辑](/images/trading-strategy.svg)

## 策略选择

选了一个最简单的趋势跟踪策略：双均线交叉。

均线的逻辑很直观——短期均线（MA5）代表最近的价格趋势，长期均线（MA20）代表较长时间的趋势。当短期线上穿长期线时（金叉），意味着趋势可能向上，开多。当短期线下穿长期线时（死叉），趋势可能转弱，平多或开空。

这个策略的好处是容易理解，也容易执行。坏处是它在震荡行情里表现很差——价格反复穿越均线，频繁开平仓，手续费吃掉大部分利润。

### 核心代码逻辑

策略循环的核心逻辑大概是这样的：

```python
import ccxt
import pandas as pd
import time
from datetime import datetime

exchange = ccxt.okx({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'password': 'YOUR_API_PASSPHRASE',
    'enableRateLimit': True,
})

symbol = 'BTC-USDT-SWAP'
timeframe = '1m'
limit = 50
position_size = 50  # USDT
leverage = 3

def get_ma_crossover():
    """获取最新两根K线，计算MA5和MA20，判断是否金叉/死叉"""
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    
    # 获取倒数第二根（上一根已收盘的K线）和倒数第三根的金叉状态
    prev_ma5 = df['ma5'].iloc[-3]
    prev_ma20 = df['ma20'].iloc[-3]
    curr_ma5 = df['ma5'].iloc[-2]
    curr_ma20 = df['ma20'].iloc[-2]
    
    # 金叉：之前MA5 <= MA20，现在MA5 > MA20
    golden_cross = prev_ma5 <= prev_ma20 and curr_ma5 > curr_ma20
    # 死叉：之前MA5 >= MA20，现在MA5 < MA20
    death_cross = prev_ma5 >= prev_ma20 and curr_ma5 < curr_ma20
    
    return golden_cross, death_cross

def get_position():
    """查询当前持仓"""
    positions = exchange.fetch_positions([symbol])
    for pos in positions:
        if pos['symbol'] == symbol and float(pos['contracts']) > 0:
            return pos
    return None

def place_order(side, amount):
    """下单，带止盈止损"""
    # 先设置杠杆
    exchange.set_leverage(leverage, symbol)
    
    # 开仓
    order = exchange.create_market_order(
        symbol, side, amount, 
        params={'leverage': leverage}
    )
    
    # 获取开仓均价，设置止盈止损
    # 这里需要根据实际成交价来设置
    # 实际项目中会从 order 或后续查询中获取 fill price
    print(f"{datetime.now()} | {'多头' if side == 'buy' else '空头'}开仓 | 数量: {amount}")
    return order

def main_loop():
    """主循环"""
    print(f"策略启动: {symbol} | 时间周期: {timeframe} | 杠杆: {leverage}x")
    
    while True:
        try:
            golden, death = get_ma_crossover()
            position = get_position()
            
            if golden and not position:
                # 金叉且无持仓 → 开多
                place_order('buy', position_size)
            elif death and position:
                # 死叉且有持仓 → 平多（可改为开空，根据策略偏好）
                exchange.create_market_order(symbol, 'sell', position['contracts'])
                print(f"{datetime.now()} | 平仓")
            
            time.sleep(10)  # 每10秒检查一次
        except Exception as e:
            print(f"错误: {e}")
            time.sleep(30)

if __name__ == '__main__':
    main_loop()
```

实际项目中还需要处理很多边界情况：API 限频、网络断开重连、订单未完全成交、止盈止损的挂单管理等等。下面会详细说。

## 参数配置

| 参数 | 值 |
|------|-----|
| 周期 | 1分钟 K 线 |
| 杠杆 | 3 倍 |
| 单笔交易 | 50 USDT |
| 止盈 | 0.3% |
| 止损 | 0.15% |

选择 1 分钟 K 线是因为这个策略在短周期上的信号更多，适合快速验证。但相应的，交易频率也会很高，手续费是一笔不能忽略的成本。

杠杆用 3 倍，不算高，给波动留了足够的缓冲空间。50 USDT 一单，配合 3 倍杠杆，实际名义价值是 150 USDT，爆仓价格距离入场点大约有 30% 以上，安全性上没什么问题。

止盈 0.3%、止损 0.15%，这个比例是我回测不同参数组合后选出来的。胜率大概在 60% 左右，盈亏比刚好能让账户整体盈利。如果胜率下降到 50% 以下，这个比例就会开始亏钱，所以参数不是设好就完事的，要定期观察。

### 资金管理的一点经验

我一开始犯过的一个错误——单笔仓位占比太高。当时只算了止损百分比，没算连续亏损的情况。如果连续亏损 5 单，账户回撤直接超过 30%，心态上就很难受了。

后来调整了资金管理规则：每笔交易的亏损不超过总资金的 2%。以 68 USDT 的总资金为例，每单亏 0.15% 对应约 0.075 USDT（50 * 3 * 0.15% = 0.225，但这里的 0.15% 是价格的百分比），实际算下来连续亏 20 单也不会有太大问题，这才安心一些。

**核心原则：永远假设最坏情况会发生，让资金管理来保护你，而不是靠策略。**

```python
# 资金管理模块示例
def calculate_position_size(balance, risk_per_trade=0.02, stop_loss_pct=0.0015):
    """
    根据账户余额、单笔风险和止损比例计算仓位
    balance: 账户余额 (USDT)
    risk_per_trade: 单笔最大亏损比例 (2%)
    stop_loss_pct: 止损比例 (0.15%)
    """
    max_loss = balance * risk_per_trade
    position = max_loss / stop_loss_pct
    return min(position, balance)  # 不超过总余额
```

## 部署方式

代码放在 HK 服务器上的 `/opt/okx-bot/` 目录下。用 systemd 配置成了服务，开机自动启动，崩溃自动重启。

### 目录结构

```
/opt/okx-bot/
├── bot.py          # 主程序
├── config.yaml     # 配置文件
├── logger.py       # 日志模块
├── notifier.py     # Telegram通知模块
├── requirements.txt
└── okx.service     # systemd 服务文件
```

### Systemd 服务配置

```ini
[Unit]
Description=okx-bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/okx-bot/bot.py
Restart=always
RestartSec=10
User=root
WorkingDirectory=/opt/okx-bot
StandardOutput=append:/var/log/okx-bot.log
StandardError=append:/var/log/okx-bot.log

[Install]
WantedBy=multi-user.target
```

启动方式：

```bash
sudo cp okx.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable okx-bot
sudo systemctl start okx-bot
# 查看状态
sudo systemctl status okx-bot
# 查看日志
journalctl -u okx-bot -f
```

### 配置文件结构

```yaml
# config.yaml
exchange:
  name: okx
  api_key: "YOUR_API_KEY"
  api_secret: "YOUR_SECRET"
  password: "YOUR_PASSPHRASE"
  sandbox: false  # 先开沙箱测试

strategy:
  symbol: "BTC-USDT-SWAP"
  timeframe: "1m"
  ma_fast: 5
  ma_slow: 20
  leverage: 3
  position_size: 50  # USDT
  take_profit_pct: 0.3
  stop_loss_pct: 0.15
  check_interval: 10  # 检查间隔（秒）

telegram:
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"
```

把 API Key 和密码放在配置文件里，方便修改，也方便多个策略共用一套代码。不过要注意权限控制——OKX 的 API Key 只开交易权限就够了，不要开提币权限。

### 沙箱测试，别急着上真钱

这一步非常重要，但很多人跳过了——直接在实盘跑。我建议先在 OKX 沙箱环境（sandbox）里跑至少一周，观察策略是否按预期执行，有没有逻辑漏洞，API 调用有没有报错。

切换到沙箱只需要改一行：

```python
exchange = ccxt.okx({
    'apiKey': 'SANDBOX_API_KEY',
    'secret': 'SANDBOX_SECRET',
    'password': 'SANDBOX_PASSPHRASE',
    'enableRateLimit': True,
    'urls': {
        'api': {
            'public': 'https://www.okx.com/api/v5/public',
            'private': 'https://www.okx.com/api/v5/private'
        }
    }
})
```

或者直接用 ccxt 自带的 `exchange.set_sandbox_mode(True)`。

## Telegram 通知

交易信号通过 Telegram Bot 推送到手机上。每次开仓、平仓、止盈止损都会收到一条通知。这样不用一直看电脑，有异常情况手机上第一时间知道。

Telegram 通知的实现很简单：

```python
import requests

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.chat_id = chat_id
    
    def send_message(self, text):
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        try:
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            print(f"Telegram 通知失败: {e}")

notifier = TelegramNotifier(config['telegram']['bot_token'], config['telegram']['chat_id'])

# 使用时
notifier.send_message(
    f"🤖 <b>开多</b>\n"
    f"价格: {current_price}\n"
    f"数量: {position_size} USDT\n"
    f"杠杆: {leverage}x\n"
    f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
```

通知消息里加上价格、数量、盈亏状态这些关键信息，方便快速判断当前运行情况。另外我还加了一个"心跳"通知，每天早上 8 点发一条汇总消息，告诉我当前持仓、当日交易次数、累计盈亏，即使没有交易信号也能确认程序还在正常运行。

## 几个实盘发现的问题

实盘跑下来，有几个之前在回测里没注意到的问题：

### 1. 止损比止盈更容易触发

0.3% 的止盈和 0.15% 的止损，按照这个比例，需要有 2:1 的胜率才能盈利。实际跑下来，胜率大概在 60% 左右，刚好覆盖亏损单。

但这里有一个坑——滑点。在波动剧烈的时候，止损单实际成交价可能比预设的止损价低不少。比如止损设 0.15%，实际成交可能到了 0.2%~0.25%，这就把盈亏比进一步恶化了。我在代码里加了一个统计模块，记录每一次止盈止损的实际成交价和预设价的偏差：

```python
def track_slippage(expected_price, filled_price, side):
    slippage = abs(filled_price - expected_price) / expected_price * 100
    # 记录到 CSV，定期分析
    with open('slippage_log.csv', 'a') as f:
        f.write(f"{datetime.now()},{side},{expected_price},{filled_price},{slippage:.4f}%\n")
```

跑了一周后发现平均滑点在 0.02%~0.05% 之间，极端情况下能到 0.1%。这个数据让我决定把止盈止损的触发值稍微放宽一点，给滑点留点余量。

### 2. 网络延迟对交易的影响

从信号出现到实际下单，中间有几百毫秒的延迟。对于 1 分钟 K 线来说，这个延迟是可以接受的。但如果切换到秒级策略，延迟就是一个必须解决的问题。

我遇到过一次比较严重的延迟：服务器（HK）到 OKX 的 API 节点，某天下午延迟突然飙升到 2~3 秒。原因是路由绕路了，可能是 ISP 的问题。2~3 秒的延迟对于 1 分钟 K 线策略来说，虽然不会造成灾难性后果，但如果恰好发生在关键信号附近，成交价格会跟预期差很多。

应对方法是在代码里加了一个延迟监控：

```python
def check_latency():
    """检查 API 延迟，如果太高就告警"""
    start = time.time()
    exchange.fetch_ticker(symbol)
    latency = (time.time() - start) * 1000  # 毫秒
    if latency > 1000:
        notifier.send_message(f"⚠️ 延迟告警: {latency:.0f}ms")
    return latency
```

如果延迟持续过高，可以考虑换服务器位置或者用交易所的 WebSocket API 代替 REST API。

### 3. 资金管理才是真正的防线

第三个发现其实是最重要的。我用了 68 USDT 的小号在跑，亏完了也不会影响主力资金。对于刚开始跑实盘的策略来说，这是一个比较稳妥的做法——先用小钱验证，稳定了再考虑加仓。

很多人上来就上大资金，想着"回测效果好，应该没问题"。但回测和实盘是两回事——回测里不会出现 API 连接失败、不会出现交易所维护、不会出现滑点超出预期、更不会出现你的策略在某种市场环境下突然失效。

**所以我建议：实盘的资金一定是亏完了也不心疼的金额。** 等跑了一两个月，数据稳定了，再考虑是不是要加仓。如果连 68 USDT 都赚不到钱，加仓到 680 USDT 只会亏更多。

### 4. 震荡行情是最大的敌人

双均线策略最大的问题就是震荡。价格在 MA5 和 MA20 之间反复穿越，策略会频繁开平仓，每一笔都亏一点手续费，积累下来就是不小的损失。

我跑了大概两周，其中有一周 BTC 在 6 万到 6 万 2 之间反复震荡，策略在那周亏了大约 5%。后来我在代码里加了一个过滤条件——当价格在一定时间内波动幅度小于某个阈值时，暂停交易：

```python
def should_skip_trade(df, volatility_threshold=0.005):
    """如果最近 N 根 K 线的波动太小，跳过交易避免震荡磨损"""
    recent_high = df['high'].iloc[-10:].max()
    recent_low = df['low'].iloc[-10:].min()
    volatility = (recent_high - recent_low) / recent_low
    if volatility < volatility_threshold:
        return True  # 波动太小，跳过
    return False
```

这个简单的过滤条件在震荡行情里省了不少手续费，虽然也会错过一些趋势启动的早期信号，但总体来说利大于弊。

## 总结

双均线策略虽然简单，但跑实盘的过程中学到的东西远比策略本身复杂——API 对接的坑、网络延迟的影响、滑点对盈亏比的侵蚀、震荡行情的过滤、资金管理的重要性……这些在回测里是看不出来的。

目前跑了小半个月，账户小幅盈利。接下来的计划是：

1. 收集更多实盘数据，优化止盈止损比例
2. 测试在波动率过滤条件下是否还能提高胜率
3. 如果稳定盈利，考虑增加第二个策略做组合对冲
4. 把 REST API 换成 WebSocket，降低延迟

如果你也在做类似的事情，建议从最小资金开始，多关注日志和统计数据，不要只看总盈亏。后面跑顺了再分享新的进展。