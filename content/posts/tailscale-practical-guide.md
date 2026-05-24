---
title: "用 Tailscale 打通多台服务器：告别公网 IP 和复杂配置"
date: 2026-05-24
draft: false
tags: ["网络", "Tailscale", "WireGuard", "VPN", "服务器", "运维"]
---

## 前言

大家好，我是Seb。

事情是这样的：我手上有三四台服务器，香港的、新加坡的、美国的，还有一台家里的 NAS。每台机器上都跑着不同的服务——Bot、API 中转、数据分析、文件存储。平时 ssh 过去操作就算了，但这些服务之间经常需要互相通信。

比如我的 Telegram Bot（跑在香港的 VPS 上）需要从家里的 NAS 上拉数据，完成之后再推给新加坡的 API 中转。以前的做法是什么？让每台机器都暴露一个公网端口，然后用 IP + 端口互相访问。结果就是：防火墙规则写了一堆、端口开了一大串、每次加新机器都要重新配置一遍。麻烦不说，安全上也心虚——多开一个端口就多一个攻击面。

后来我试了 Tailscale，用了一段时间，发现这个工具确实把这类问题解决得挺利索。这篇文章就把我的使用过程踩过的坑、总结的经验都写出来，希望对有类似需求的朋友有点帮助。

![Tailscale 网络拓扑图](/images/tailscale-arch.svg)

## 为什么是 Tailscale？

市面上的组网方案不少，我试过几个，简单说说对比。

### WireGuard

WireGuard 本身是个非常优秀的 VPN 协议，配置也不算复杂——写个 conf 文件，双方各跑一个 wg-quick 就行。核心问题是：它要求至少一端有公网 IP。如果两台机器都在 NAT 后面（比如家里的 NAS 和公司的笔记本），就需要一台有公网 IP 的中继服务器做"打洞"。而且 WireGuard 没有自动发现机制，每加一台设备都得手动更新所有机器的配置。三台机器还好，五台以上就开始烦了。

### FRP

FRP 更适合做端口转发，而不是组网。它的模式是：内网机器主动连接到公网服务器，公网服务器再把请求转发到内网。用来暴露一个 Web 服务很方便，但要让多台机器组成一个平面网络，FRP 就有点力不从心了。每次转发都需要配置一个端口，服务多了之后维护成本不低。

### ZeroTier

ZeroTier 和 Tailscale 理念类似，但我个人体验是 ZeroTier 的连接稳定性不太稳定。同样是 UDP 打洞，Tailscale 的连接成功率明显更高。ZeroTier 的自建控制器也折腾过，配置起来比 Tailscale 复杂不少。

### Tailscale

Tailscale 的优势总结下来就几点：

1. **零配置组网** — 装好客户端，登录同一个账号，机器自动发现、自动连接
2. **基于 WireGuard** — 底层用的是 WireGuard 协议，传输效率和安全性都有保障
3. **NAT 穿透能力强** — 大部分情况下能直接 P2P 打洞，打不通才走中继
4. **ACL（访问控制列表）** — 可以精细控制哪些机器能访问哪些端口
5. **免费版够用** — 个人用户 100 台设备以内免费

我的场景比较简单——几台服务器组成一个内网，服务之间互相调用。Tailscale 正好完美覆盖这个需求，而且几乎没有学习成本。

## 部署过程

### 第一步：安装 Tailscale

Tailscale 支持几乎所有主流操作系统，安装方式很统一。以 Linux 服务器为例：

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

就这么一行。装完之后跑一下：

```bash
sudo tailscale up
```

它会弹出一个链接，复制到浏览器里用 GitHub/Google/Microsoft 账号登录就行。登录完成后，这台机器就自动加入你的 Tailnet（Tailscale 网络）了。

每台机器上重复同样的操作。我花了大概十分钟，把香港 VPS、新加坡 VPS、美国 VPS 和家里的 NAS 全部加进了同一个网络。

### 第二步：验证连通性

登录完之后，用 `tailscale status` 看看效果：

```bash
$ tailscale status
100.x.x.x    hk-vps          makismkuo@    linux   -
100.x.x.x    sg-vps          makismkuo@    linux   -
100.x.x.x    us-vps          makismkuo@    linux   -
100.x.x.x    nas-home        makismkuo@    linux   -
```

每台机器都拿到了一个 100.x.x.x 的 Tailscale IP。现在，在任何一台机器上 ping 别的机器的 Tailscale IP：

```bash
# 在 hk-vps 上 ping 家里的 NAS
ping 100.x.x.x
```

如果能通，组网就完成了。我四台机器之间互相 ping 了一下，延迟基本和直连差不多——香港到新加坡 30ms 左右，是 P2P 直连，没有走中继。

### 第三步：配置子网路由（关键）

我的 NAS 上还跑着一些 Docker 容器，它们的 IP 是 172.17.0.x 网段。如果想让其他服务器直接访问这些容器，需要启用子网路由。

在 NAS 上执行：

```bash
sudo tailscale up --advertise-routes=172.17.0.0/24,192.168.1.0/24
```

然后在 Tailscale 的管理后台（https://login.tailscale.com）里，找到这台机器，把这两个路由网段批准（Approve）一下。

这样，其他服务器就能直接通过 172.17.0.x 访问 NAS 的 Docker 容器了，就像在同一个局域网里一样。

### 第四步：配置 MagicDNS

Tailscale 支持 MagicDNS——开启之后，每台机器可以用主机名代替 Tailscale IP 来访问。比如不用记 100.x.x.x，直接 ssh hk-vps 就行。

```bash
sudo tailscale up --accept-dns=true
```

在管理后台的 DNS 页面勾选 "Enable MagicDNS" 就行。之后所有机器自动获得机器名解析：

```bash
$ ping hk-vps
PING hk-vps.tailnet-name.ts.net (100.x.x.x) ...
```

这个功能对日常操作提升很大——不用记 IP、不用维护 /etc/hosts、加新机器自动生效。

## 踩坑记录

### 坑一：Exit Node 导致断连

Tailscale 有个 Exit Node 功能，可以把某台机器的流量全部路由到另一台机器的网络出口。我在香港 VPS 上开了 Exit Node，本地连上去想测试一下，结果把自己 ssh 断了。

原因是：我本地机器通过 Tailscale 连上香港 VPS 的 Exit Node 之后，本地机器的所有流量都走香港出口了，包括 ssh 会话本身。但香港 VPS 的防火墙只允许 22 端口从特定 IP 访问，流量从 Exit Node 出去后源 IP 变了，防火墙直接把包丢了。

解决办法很简单——在使用 Exit Node 前，先确保目标机器有 allow incoming 规则，或者用 ACL 放行。我现在只在特定场景下用 Exit Node，比如临时需要从国外 IP 访问某个服务，用完就关掉。

### 坑二：国内机器连接不稳定

香港 VPS 连 Tailscale 的中继服务器（位于国外）时，偶尔会断连。检一下发现是 DERP（中继服务器）的连接超时了。

解决方法是自建一个 DERP 服务器。Tailscale 支持自建中继节点，我找了一台延迟最低的 VPS（跟主要机器同机房），用 Docker 搭了一个：

```bash
docker run -d \
  --name=derper \
  --restart=always \
  -p 443:443 -p 3478:3478/udp \
  -v /root/derper:/data \
  -e DERP_DOMAIN=derp.yourdomain.com \
  ghcr.io/yangchuansheng/derper:latest
```

然后在管理后台把自建 DERP 加进列表中。之后国内机器的连接稳定性明显改善——因为中继节点离得更近了。

### 坑三：重启后 Tailscale 不会自动启动

这是个小问题，但第一次遇到的时候挺懵的。某些 Linux 发行版上，Tailscale 安装后不会自动设置开机自启。

```bash
sudo systemctl enable tailscaled
```

做了这个之后就好了。另外注意如果防火墙有严格的出站规则，要放行 Tailscale 的端口：UDP 41641（打洞用）和 TCP 443（中继用）。

## 现在的使用情况

组网跑了一段时间，现在的情况是：

- 所有服务器之间通过 Tailscale IP 互相访问，不暴露任何公网端口
- 家里 NAS 上的 Docker 容器可以直接被 VPS 上的服务调用
- 加新机器只需要装 Tailscale 跑一次 up，不需要改任何现有配置
- 登录管理后台就能看到所有机器的在线状态和流量统计

最明显的感受是：组网这件事变得几乎无感了。以前要花半天配置 WireGuard、写路由表、维护 /etc/hosts，现在十分钟搞定，而且基本不用维护。Tailscale 在后台会自动处理重连、打洞、密钥轮换这些事情，我完全感觉不到它的存在——这是最好的状态。

## 一些建议

如果你手里有超过两台服务器（或者一台服务器加一台本地机器），并且它们之间需要通信，强烈建议试试 Tailscale。不用从 WireGuard 开始折腾，不用买云厂商的 VPC 产品，装个客户端、登录、完事。

免费版支持 100 台设备，个人和小团队完全够用。如果需要更细粒度的访问控制或者审计日志，可以订阅 Team 版，每个月几美元。

最后提醒一点：Tailscale 不是传统的 VPN 工具。它不代理你所有的上网流量（除非你主动开 Exit Node），它做的事情更接近"组建一个安全的内网"。理解这个定位之后，用起来思路就清晰了。

有什么问题欢迎交流。Seb，下篇见。

——Seb
