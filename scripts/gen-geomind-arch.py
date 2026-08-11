#!/usr/bin/env python3
"""Generate GeoMind architecture diagram (Harbor-style dark tech)."""
import sys

def geomind_arch():
    svg_w, svg_h = 900, 650
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0e1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#141832;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="glow-blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366f1;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#818cf8;stop-opacity:0" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-strong">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="{svg_w}" height="{svg_h}" fill="url(#bg)"/>
  
  <!-- Grid pattern -->
  <g opacity="0.03" stroke="#6366f1" stroke-width="0.5">
    {''.join(f'<line x1="0" y1="{y}" x2="{svg_w}" y2="{y}"/>' for y in range(0, svg_h, 40))}
    {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{svg_h}"/>' for x in range(0, svg_w, 40))}
  </g>

  <!-- Title -->
  <text x="{svg_w/2}" y="45" text-anchor="middle" fill="#c7d2fe" font-family="sans-serif" font-size="22" font-weight="bold" filter="url(#glow-strong)">GeoMind 架构</text>
  <text x="{svg_w/2}" y="70" text-anchor="middle" fill="#818cf8" font-family="sans-serif" font-size="12">GEO Intelligence CLI</text>

  <!-- Layer 1: User Interface -->
  <text x="60" y="115" fill="#6366f1" font-family="sans-serif" font-size="12" font-weight="bold">用户接口</text>
  <rect x="60" y="125" width="180" height="44" rx="6" fill="#1e1b4b" stroke="#a5b4fc" stroke-width="1.2" opacity="0.9"/>
  <text x="150" y="152" text-anchor="middle" fill="#a5b4fc" font-family="sans-serif" font-size="13">终端 CLI (click)</text>
  <rect x="260" y="125" width="180" height="44" rx="6" fill="#1e1b4b" stroke="#a5b4fc" stroke-width="1.2" opacity="0.9"/>
  <text x="350" y="152" text-anchor="middle" fill="#a5b4fc" font-family="sans-serif" font-size="13">HTML 报告 (Jinja2)</text>
  <rect x="460" y="125" width="180" height="44" rx="6" fill="#1e1b4b" stroke="#a5b4fc" stroke-width="1.2" opacity="0.9"/>
  <text x="550" y="152" text-anchor="middle" fill="#a5b4fc" font-family="sans-serif" font-size="13">对比模式</text>

  <!-- Arrow: Layer 1 → 2 -->
  <line x1="150" y1="169" x2="150" y2="200" stroke="#6366f1" stroke-width="1.5" marker-end="none" opacity="0.6"/>
  <line x1="350" y1="169" x2="350" y2="200" stroke="#6366f1" stroke-width="1.5" marker-end="none" opacity="0.6"/>

  <!-- Layer 2: Core Engine -->
  <rect x="60" y="200" width="780" height="160" rx="10" fill="none" stroke="#818cf8" stroke-width="1" stroke-dasharray="6,3" opacity="0.4"/>
  <text x="80" y="225" fill="#818cf8" font-family="sans-serif" font-size="12" font-weight="bold">核心引擎</text>

  <!-- Analyzer -->
  <rect x="340" y="230" width="200" height="44" rx="8" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>
  <text x="440" y="257" text-anchor="middle" fill="#c7d2fe" font-family="sans-serif" font-size="14" font-weight="bold" filter="url(#glow)">GEO Analyzer</text>

  <!-- Checks grid (4x2) -->
  <g font-family="sans-serif" font-size="11">
    <rect x="80" y="290" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#67e8f9" stroke-width="0.8" opacity="0.8"/>
    <text x="160" y="309" text-anchor="middle" fill="#67e8f9">标题检查</text>
    
    <rect x="255" y="290" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#67e8f9" stroke-width="0.8" opacity="0.8"/>
    <text x="335" y="309" text-anchor="middle" fill="#67e8f9">描述检查</text>
    
    <rect x="430" y="290" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#67e8f9" stroke-width="0.8" opacity="0.8"/>
    <text x="510" y="309" text-anchor="middle" fill="#67e8f9">标题结构检查</text>
    
    <rect x="605" y="290" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#f472b6" stroke-width="0.8" opacity="0.8"/>
    <text x="685" y="309" text-anchor="middle" fill="#f472b6">结构化数据</text>

    <rect x="80" y="325" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#67e8f9" stroke-width="0.8" opacity="0.8"/>
    <text x="160" y="344" text-anchor="middle" fill="#67e8f9">可读性检查</text>
    
    <rect x="255" y="325" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#67e8f9" stroke-width="0.8" opacity="0.8"/>
    <text x="335" y="344" text-anchor="middle" fill="#67e8f9">链接分析</text>
    
    <rect x="430" y="325" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#fbbf24" stroke-width="0.8" opacity="0.8"/>
    <text x="510" y="344" text-anchor="middle" fill="#fbbf24">性能检查</text>
    
    <rect x="605" y="325" width="160" height="30" rx="4" fill="#1e1b4b" stroke="#f472b6" stroke-width="0.8" opacity="0.8"/>
    <text x="685" y="344" text-anchor="middle" fill="#f472b6">FAQ检测</text>
  </g>

  <!-- Arrow: Layer 2 → 3 -->
  <line x1="350" y1="360" x2="350" y2="395" stroke="#6366f1" stroke-width="1.5" opacity="0.6"/>
  <line x1="550" y1="360" x2="550" y2="395" stroke="#6366f1" stroke-width="1.5" opacity="0.6"/>

  <!-- Layer 3: Data Layer -->
  <text x="60" y="420" fill="#6366f1" font-family="sans-serif" font-size="12" font-weight="bold">数据层</text>
  <rect x="60" y="430" width="230" height="44" rx="6" fill="#1e1b4b" stroke="#34d399" stroke-width="1.2" opacity="0.9"/>
  <text x="175" y="457" text-anchor="middle" fill="#34d399" font-family="sans-serif" font-size="13">HTTP 抓取 (httpx)</text>
  <rect x="310" y="430" width="230" height="44" rx="6" fill="#1e1b4b" stroke="#34d399" stroke-width="1.2" opacity="0.9"/>
  <text x="425" y="457" text-anchor="middle" fill="#34d399" font-family="sans-serif" font-size="13">HTML 解析 (BeautifulSoup)</text>
  <rect x="560" y="430" width="230" height="44" rx="6" fill="#1e1b4b" stroke="#34d399" stroke-width="1.2" opacity="0.9"/>
  <text x="675" y="457" text-anchor="middle" fill="#34d399" font-family="sans-serif" font-size="13">报告渲染 (Rich / Jinja2)</text>

  <!-- Arrow: Layer 3 → 4 -->
  <line x1="350" y1="474" x2="350" y2="510" stroke="#6366f1" stroke-width="1.5" opacity="0.6"/>

  <!-- Layer 4: Output -->
  <text x="60" y="530" fill="#6366f1" font-family="sans-serif" font-size="12" font-weight="bold">输出</text>
  <rect x="60" y="540" width="360" height="44" rx="6" fill="#1e1b4b" stroke="#f472b6" stroke-width="1.2" opacity="0.9"/>
  <text x="240" y="567" text-anchor="middle" fill="#f472b6" font-family="sans-serif" font-size="13">终端 GEO 评分报告（彩色 + Emoji）</text>
  <rect x="460" y="540" width="360" height="44" rx="6" fill="#1e1b4b" stroke="#f472b6" stroke-width="1.2" opacity="0.9"/>
  <text x="640" y="567" text-anchor="middle" fill="#f472b6" font-family="sans-serif" font-size="13">HTML 可分享报告 + 优化建议</text>

  <!-- Bottom info -->
  <text x="450" y="620" text-anchor="middle" fill="#4f46e5" font-family="sans-serif" font-size="11">Fansen.tech · GEO Intelligence</text>
</svg>'''

if __name__ == "__main__":
    print(geomind_arch())
