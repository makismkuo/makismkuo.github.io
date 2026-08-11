#!/usr/bin/env python3
"""Generate dark-tech SVG architecture diagram (Harbor style)."""
import sys

def harbor_style_arch(title, layers, center_text="Harbor"):
    """Generate a dark-tech layered architecture SVG.
    
    Args:
        title: Diagram title
        layers: list of dicts with {name, items: [str], color: str}
        center_text: Center orchestrator label
    """
    box_w, box_h = 180, 48
    gap = 16
    layer_gap = 60
    svg_w = 900
    svg_h = 200 + len(layers) * (box_h + layer_gap)
    
    lines = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0e1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#141832;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#6366f1"/>
    </marker>
  </defs>
  <rect width="{svg_w}" height="{svg_h}" fill="url(#bg)"/>
  
  <!-- Grid pattern -->
  <g opacity="0.03">
    <line x1="0" y1="0" x2="{svg_w}" y2="0" stroke="#6366f1" stroke-width="1"/>
    <line x1="0" y1="100" x2="{svg_w}" y2="100" stroke="#6366f1" stroke-width="1"/>
    <line x1="0" y1="200" x2="{svg_w}" y2="200" stroke="#6366f1" stroke-width="1"/>
  </g>
  
  <text x="{svg_w/2}" y="40" text-anchor="middle" fill="#c7d2fe" font-family="sans-serif" font-size="20" font-weight="bold">{title}</text>
''']
    
    y = 80
    # Draw each layer
    for i, layer in enumerate(layers):
        n = len(layer["items"])
        row_y = y + i * (box_h + layer_gap)
        
        # Center orchestrator
        if i == len(layers)//2 and center_text:
            cx, cy = svg_w//2, row_y + box_h//2
            lines.append(f'  <rect x="{cx-70}" y="{row_y}" width="140" height="{box_h}" rx="8" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>')
            lines.append(f'  <text x="{cx}" y="{cy+5}" text-anchor="middle" fill="#c7d2fe" font-family="sans-serif" font-size="13" font-weight="bold" filter="url(#glow)">{center_text}</text>')
            
            # Layer label
            lines.append(f'  <text x="{cx}" y="{row_y-12}" text-anchor="middle" fill="#818cf8" font-family="sans-serif" font-size="11">{layer["name"]}</text>')
            
            # Arrows from center to items
            for j, item in enumerate(layer["items"]):
                ix = svg_w//2 - (n-1)*100//2 + j*100
                lines.append(f'  <line x1="{cx+70}" y1="{cy}" x2="{ix-90}" y2="{cy}" stroke="#6366f1" stroke-width="1" marker-end="url(#arrow)" opacity="0.5"/>')
                ix2 = svg_w//2 + (n-1)*100//2 - j*100 + 90
                if ix2 != ix:
                    lines.append(f'  <line x1="{cx-70}" y1="{cy}" x2="{ix2}" y2="{cy}" stroke="#6366f1" stroke-width="1" marker-end="url(#arrow)" opacity="0.5"/>')
            continue
        
        # Layer label
        lx = 50
        lines.append(f'  <text x="{lx}" y="{row_y-8}" fill="#6366f1" font-family="sans-serif" font-size="12" font-weight="bold">{layer["name"]}</text>')
        
        # Items
        for j, item in enumerate(layer["items"]):
            ix = lx + 20 + j * (box_w + gap)
            lines.append(f'  <rect x="{ix}" y="{row_y}" width="{box_w}" height="{box_h}" rx="6" fill="#1e1b4b" stroke="{layer["color"]}" stroke-width="1" opacity="0.9"/>')
            lines.append(f'  <text x="{ix+box_w/2}" y="{row_y+box_h/2+4}" text-anchor="middle" fill="{layer["color"]}" font-family="sans-serif" font-size="12">{item}</text>')
    
    lines.append('</svg>')
    return '\n'.join(lines)

if __name__ == "__main__":
    # Example: Harbor-style architecture
    layers = [
        {"name": "USER ACCESS", "items": ["CLI", "Web UI", "Mobile", "API"], "color": "#a5b4fc"},
        {"name": "ORCHESTRATION", "items": [], "color": "#818cf8"},
        {"name": "BACKENDS", "items": ["Ollama", "llama.cpp", "vLLM", "MLX", "DMR"], "color": "#67e8f9"},
        {"name": "SERVICES", "items": ["Open WebUI", "ComfyUI", "SearXNG", "Speaches"], "color": "#f472b6"},
    ]
    print(harbor_style_arch("Harbor Architecture", layers, "Harbor CLI"))
