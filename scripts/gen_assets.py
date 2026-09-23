#!/usr/bin/env python3
"""Generate the profile README SVG assets in dark and light variants.

Usage:  python3 scripts/gen_assets.py            # writes into Assets/
        python3 scripts/gen_assets.py <dir>      # writes into <dir>

The SVGs use only inline CSS and system fonts, so they render inside
GitHub's image proxy. Each graphic has a -dark and -light variant that
README.md selects with <picture> / prefers-color-scheme.
"""
import math, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "Assets")
os.makedirs(OUT, exist_ok=True)

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0d1117", bg2="#111827", panel="#161b22", panel2="#1c2230", border="#30363d",
                 text="#e6edf3", muted="#8b949e", faint="#21262d",
                 a1="#2dd4bf", a2="#818cf8", a3="#38bdf8", glow="#2dd4bf"),
    "light": dict(bg="#ffffff", bg2="#f3f6fb", panel="#f6f8fa", panel2="#eef2f7", border="#d0d7de",
                  text="#1f2328", muted="#57606a", faint="#eaeef2",
                  a1="#0d9488", a2="#4f46e5", a3="#0369a1", glow="#0d9488"),
}

def write(name, theme, body):
    path = os.path.join(OUT, f"{name}-{theme}.svg")
    with open(path, "w") as f:
        f.write(body)
    print("wrote", path)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- banner
def banner(t):
    c = THEMES[t]
    W, H = 1200, 300
    # deterministic node graph on the right side
    nodes = [
        (860, 70), (935, 140), (1010, 60), (1090, 120), (1150, 60),
        (880, 205), (960, 245), (1040, 190), (1120, 235), (1160, 165),
        (800, 140), (820, 250), (985, 120)
    ]
    edges = [(0,1),(1,2),(2,3),(3,4),(1,12),(12,3),(0,10),(10,5),(5,6),(6,7),(7,8),(8,9),(9,3),
             (1,7),(12,7),(5,11),(11,6),(10,11),(2,12),(4,9)]
    parts = []
    for i,(a,b) in enumerate(edges):
        x1,y1 = nodes[a]; x2,y2 = nodes[b]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge" style="animation-delay:{(i*0.37)%4:.2f}s"/>')
    for i,(x,y) in enumerate(nodes):
        r = 5 if i % 3 else 7
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="node" style="animation-delay:{(i*0.53)%3:.2f}s"/>')
    graph = "\n".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Satvik Praveen</title>
<desc id="desc">PhD Researcher in Medical AI, ML Engineer, Generative AI</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['bg2']}"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{c['a1']}"/><stop offset="0.55" stop-color="{c['a3']}"/><stop offset="1" stop-color="{c['a2']}"/>
  </linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{c['a2']}" stop-opacity="0.22"/><stop offset="1" stop-color="{c['a2']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.2" fill="{c['border']}"/>
  </pattern>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <style>
    .name {{ font: 700 54px {FONT}; fill: {c['text']}; letter-spacing: -0.5px; }}
    .tag  {{ font: 500 21px {FONT}; fill: {c['text']}; opacity: .92; }}
    .sub  {{ font: 400 15.5px {FONT}; fill: {c['muted']}; }}
    .edge {{ stroke: {c['a3']}; stroke-width: 1.2; stroke-opacity: .35; animation: edgePulse 4s ease-in-out infinite; }}
    .node {{ fill: {c['a1']}; stroke: {c['bg']}; stroke-width: 2; animation: nodePulse 3s ease-in-out infinite; }}
    @keyframes edgePulse {{ 0%,100% {{ stroke-opacity:.25 }} 50% {{ stroke-opacity:.6 }} }}
    @keyframes nodePulse {{ 0%,100% {{ opacity:.7 }} 50% {{ opacity:1 }} }}
  </style>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" opacity=".55"/>
  <circle cx="1010" cy="150" r="230" fill="url(#halo)"/>
  {graph}
  <rect x="0" y="0" width="7" height="{H}" fill="url(#accent)"/>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{c['border']}"/>
<text x="64" y="128" class="name">Satvik Praveen</text>
<rect x="66" y="146" width="150" height="4" rx="2" fill="url(#accent)"/>
<text x="64" y="192" class="tag">PhD Researcher in Medical AI  ·  ML Engineer  ·  Generative AI</text>
<text x="64" y="228" class="sub">Ph.D. Computer Engineering, University of South Florida  ·  M.S. Data Science, Texas A&amp;M University</text>
</svg>
'''

# ---------------------------------------------------------------- workflow
ICONS = {
    "db": '''<ellipse cx="0" cy="-9" rx="11" ry="4.5"/><path d="M-11 -9v18c0 2.5 4.9 4.5 11 4.5s11-2 11-4.5v-18"/><path d="M-11 0c0 2.5 4.9 4.5 11 4.5S11 2.5 11 0"/>''',
    "chip": '''<rect x="-9" y="-9" width="18" height="18" rx="3"/><rect x="-4" y="-4" width="8" height="8" rx="1.5"/><path d="M-3 -13v4M3 -13v4M-3 9v4M3 9v4M-13 -3h4M-13 3h4M9 -3h4M9 3h4"/>''',
    "chart": '''<path d="M-12 12h24"/><rect x="-10" y="0" width="5" height="10" rx="1"/><rect x="-2.5" y="-7" width="5" height="17" rx="1"/><rect x="5" y="-12" width="5" height="22" rx="1"/>''',
    "rocket": '''<path d="M0 -13c5 3 8 9 8 15l-3 3h-10l-3-3c0-6 3-12 8-15z"/><circle cx="0" cy="-3" r="2.5"/><path d="M-5 5l-5 3 2-6M5 5l5 3-2-6M-2 8l2 5 2-5"/>''',
}

def workflow(t):
    c = THEMES[t]
    W, H = 1180, 280
    stages = [
        ("db", "Data Ingestion", "Pipelines · validation · versioning"),
        ("chip", "Training & Tuning", "PyTorch · experiments · configs"),
        ("chart", "Evaluation & Ablations", "Benchmarks · metrics · rigor"),
        ("rocket", "Deployment & Monitoring", "Docker · AWS · HPRC · observability"),
    ]
    cw, ch, gap, x0, y0 = 255, 118, 30, 34, 96
    cards, links = [], []
    for i,(ic, title, sub) in enumerate(stages):
        x = x0 + i*(cw+gap)
        cards.append(f'''<g transform="translate({x},{y0})">
  <rect width="{cw}" height="{ch}" rx="14" class="card"/>
  <rect x="0" y="0" width="{cw}" height="4" rx="2" fill="url(#accent)" opacity=".9"/>
  <g transform="translate(30,52)" class="icon">{ICONS[ic]}</g>
  <text x="58" y="47" class="ttl">{esc(title)}</text>
  <text x="58" y="72" class="sub">{esc(sub)}</text>
  <text x="{cw-16}" y="{ch-12}" class="num" text-anchor="end">0{i+1}</text>
</g>''')
        if i < len(stages)-1:
            lx1 = x+cw; lx2 = x+cw+gap; ly = y0+ch/2
            links.append(f'''<line x1="{lx1+4}" y1="{ly}" x2="{lx2-6}" y2="{ly}" class="flow"/>
<path d="M{lx2-9} {ly-5} L{lx2-2} {ly} L{lx2-9} {ly+5}" class="arrow"/>''')
    # feedback loop from last card bottom to first card bottom
    fx1 = x0 + 3*(cw+gap) + cw/2; fx2 = x0 + cw/2; fy = y0+ch; loopy = fy+36
    loop = f'''<path d="M{fx1} {fy+4} V{loopy} H{fx2} V{fy+12}" class="loop"/>
<path d="M{fx2-5} {fy+18} L{fx2} {fy+8} L{fx2+5} {fy+18}" class="arrow"/>
<rect x="{(fx1+fx2)/2-76}" y="{loopy-11}" width="152" height="22" rx="11" class="pill"/>
<text x="{(fx1+fx2)/2}" y="{loopy+4}" class="pilltxt" text-anchor="middle">iterate · ablate · improve</text>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">ML Systems Workflow</title>
<desc id="desc">Data ingestion, training and tuning, evaluation and ablations, deployment and monitoring, with an iterate loop.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{c['a1']}"/><stop offset="0.55" stop-color="{c['a3']}"/><stop offset="1" stop-color="{c['a2']}"/>
  </linearGradient>
  <style>
    .h1  {{ font: 700 22px {FONT}; fill: {c['text']}; }}
    .h2  {{ font: 400 14px {FONT}; fill: {c['muted']}; }}
    .card {{ fill: {c['panel']}; stroke: {c['border']}; }}
    .icon {{ fill: none; stroke: {c['a1']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    .ttl {{ font: 600 15px {FONT}; fill: {c['text']}; }}
    .sub {{ font: 400 12px {FONT}; fill: {c['muted']}; }}
    .num {{ font: 700 12px {FONT}; fill: {c['border']}; letter-spacing: 1px; }}
    .flow {{ stroke: {c['a3']}; stroke-width: 2; stroke-dasharray: 6 6; animation: dash 1.2s linear infinite; }}
    .loop {{ fill: none; stroke: {c['a2']}; stroke-width: 1.6; stroke-dasharray: 5 6; opacity: .8; animation: dash 1.6s linear infinite; }}
    .arrow {{ fill: none; stroke: {c['a3']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    .pill {{ fill: {c['bg']}; stroke: {c['border']}; }}
    .pilltxt {{ font: 500 11.5px {FONT}; fill: {c['muted']}; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -24; }} }}
  </style>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{c['bg']}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{c['border']}"/>
<text x="34" y="44" class="h1">ML Systems Workflow</text>
<text x="34" y="68" class="h2">From raw data to deployed models — reproducible, rigorously evaluated, owned end-to-end</text>
{''.join(links)}
{''.join(cards)}
{loop}
</svg>
'''

# ---------------------------------------------------------------- interests
def interests(t):
    c = THEMES[t]
    W = H = 480; cx = cy = 240; R = 165
    sats = [
        ("Applied ML", "Deep Learning"),
        ("Computer Vision", "3D Reconstruction"),
        ("Multimodal AI", "Vision–Language"),
        ("NLP", "Large Language Models"),
        ("Data Analytics", "Visualization & Storytelling"),
        ("Model Deployment", "Scalable Workflows"),
    ]
    edges, boxes = [], []
    bw, bh = 160, 50
    for i,(l1,l2) in enumerate(sats):
        ang = math.radians(-90 + i*60)
        x = cx + R*math.cos(ang); y = cy + R*math.sin(ang)
        edges.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="edge" style="animation-delay:{i*0.4:.1f}s"/>')
        boxes.append(f'''<g transform="translate({x-bw/2:.1f},{y-bh/2:.1f})">
  <rect width="{bw}" height="{bh}" rx="12" class="box"/>
  <circle cx="14" cy="{bh/2}" r="3.5" class="dot"/>
  <text x="26" y="{bh/2-4}" class="l1">{esc(l1)}</text>
  <text x="26" y="{bh/2+12}" class="l2">{esc(l2)}</text>
</g>''')
    stars = "".join(
        f'<circle cx="{(i*97+31)%W}" cy="{(i*61+17)%H}" r="{1.1 if i%2 else 1.6}" class="star" style="animation-delay:{(i*0.7)%5:.1f}s"/>'
        for i in range(26))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Areas of Interest</title>
<desc id="desc">Medical AI at the hub, connected to applied ML, computer vision, multimodal AI, NLP and LLMs, analytics, and deployment.</desc>
<defs>
  <radialGradient id="hub" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{c['a1']}" stop-opacity=".35"/><stop offset="1" stop-color="{c['a2']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/>
  </linearGradient>
  <style>
    .edge {{ stroke: {c['a3']}; stroke-width: 1.4; stroke-dasharray: 4 7; stroke-opacity: .6; animation: dash 2.4s linear infinite; }}
    .ring {{ fill: none; stroke: {c['border']}; stroke-dasharray: 2 6; }}
    .box  {{ fill: {c['panel']}; stroke: {c['border']}; }}
    .dot  {{ fill: url(#accent); }}
    .l1   {{ font: 600 12.5px {FONT}; fill: {c['text']}; }}
    .l2   {{ font: 400 10.5px {FONT}; fill: {c['muted']}; }}
    .hubc {{ fill: {c['panel']}; stroke: url(#accent); stroke-width: 2.5; }}
    .hub1 {{ font: 700 15px {FONT}; fill: {c['text']}; }}
    .hub2 {{ font: 400 11px {FONT}; fill: {c['muted']}; }}
    .star {{ fill: {c['a3']}; opacity: .35; animation: twinkle 5s ease-in-out infinite; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -22; }} }}
    @keyframes twinkle {{ 0%,100% {{ opacity:.15 }} 50% {{ opacity:.6 }} }}
  </style>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="{c['bg']}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{c['border']}"/>
{stars}
<circle cx="{cx}" cy="{cy}" r="{R}" class="ring"/>
<circle cx="{cx}" cy="{cy}" r="120" fill="url(#hub)"/>
{''.join(edges)}
<circle cx="{cx}" cy="{cy}" r="58" class="hubc"/>
<text x="{cx}" y="{cy-2}" class="hub1" text-anchor="middle">Medical AI</text>
<text x="{cx}" y="{cy+16}" class="hub2" text-anchor="middle">&amp; Healthcare</text>
{''.join(boxes)}
</svg>
'''

# ---------------------------------------------------------------- compass (guiding principles)
def compass(t):
    c = THEMES[t]
    W, H = 380, 340; cx, cy = 190, 170; R = 92
    ticks = []
    for i in range(72):
        a = math.radians(i*5)
        big = i % 18 == 0
        mid = i % 6 == 0
        r1 = R-(12 if big else 8 if mid else 4)
        x1 = cx + r1*math.cos(a); y1 = cy + r1*math.sin(a)
        x2 = cx + R*math.cos(a); y2 = cy + R*math.sin(a)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{"tb" if big else "tm" if mid else "ts"}"/>')
    labels = [
        (cx, 34, "middle", "First Principles"),
        (cx+R+12, cy+4, "start", "Impact"),
        (cx, cy+R+30, "middle", "Clarity"),
        (cx-R-12, cy+4, "end", "Ownership"),
    ]
    lab = "".join(f'<text x="{x}" y="{y}" text-anchor="{an}" class="lab">{esc(s)}</text>' for x,y,an,s in labels)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Guiding Principles</title>
<desc id="desc">A compass whose cardinal points read First Principles, Impact, Clarity, and Ownership.</desc>
<defs>
  <linearGradient id="needle" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/>
  </linearGradient>
  <radialGradient id="face" cx="0.5" cy="0.4" r="0.6">
    <stop offset="0" stop-color="{c['panel2']}"/><stop offset="1" stop-color="{c['panel']}"/>
  </radialGradient>
  <style>
    .ts {{ stroke: {c['border']}; stroke-width: 1; }}
    .tm {{ stroke: {c['muted']}; stroke-width: 1.2; opacity: .8; }}
    .tb {{ stroke: {c['a3']}; stroke-width: 2; }}
    .lab {{ font: 600 12.5px {FONT}; fill: {c['text']}; }}
    .card {{ font: 700 11px {FONT}; fill: {c['muted']}; letter-spacing: 1.5px; }}
    .needle {{ transform-origin: {cx}px {cy}px; animation: sway 6s ease-in-out infinite; }}
    @keyframes sway {{ 0%,100% {{ transform: rotate(-14deg) }} 50% {{ transform: rotate(14deg) }} }}
  </style>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="{c['bg']}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{c['border']}"/>
<circle cx="{cx}" cy="{cy}" r="{R+2}" fill="url(#face)" stroke="{c['border']}"/>
{''.join(ticks)}
<circle cx="{cx}" cy="{cy}" r="{R-18}" fill="none" stroke="{c['border']}" stroke-dasharray="3 5"/>
<text x="{cx}" y="{cy-R+38}" text-anchor="middle" class="card">N</text>
<text x="{cx+R-32}" y="{cy+4}" text-anchor="middle" class="card">E</text>
<text x="{cx}" y="{cy+R-28}" text-anchor="middle" class="card">S</text>
<text x="{cx-R+32}" y="{cy+4}" text-anchor="middle" class="card">W</text>
<g class="needle">
  <path d="M{cx} {cy-66} L{cx+9} {cy} L{cx-9} {cy} Z" fill="url(#needle)"/>
  <path d="M{cx} {cy+66} L{cx+9} {cy} L{cx-9} {cy} Z" fill="{c['border']}"/>
</g>
<circle cx="{cx}" cy="{cy}" r="7" fill="{c['bg']}" stroke="{c['a1']}" stroke-width="2.5"/>
{lab}
</svg>
'''

for t in THEMES:
    write("banner", t, banner(t))
    write("ml-workflow", t, workflow(t))
    write("interests", t, interests(t))
    write("principles", t, compass(t))
