"""Generates assets/header.svg and assets/stats.svg (text is converted to outlines, so no font is needed to view them).
Usage: pip install fonttools brotli uharfbuzz && python3 tools/gen-assets.py"""
import io, os, re
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'assets')
_cache = {}
def load(name, wght):
    k = (name, wght)
    if k not in _cache:
        f = TTFont(os.path.join(HERE, 'fonts', name))
        if 'fvar' in f: f = instantiateVariableFont(f, {'wght': wght})
        f.flavor = None; b = io.BytesIO(); f.save(b); _cache[k] = (f, b.getvalue())
    return _cache[k]
def shape(name, wght, text, size, x, y, tracking=0):
    f, data = load(name, wght); font = hb.Font(hb.Face(data))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf, {"kern": True, "liga": False})
    gs = f.getGlyphSet(); order = f.getGlyphOrder(); s = size / f['head'].unitsPerEm
    pen = SVGPathPen(gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.')); pos = 0
    for info, p in zip(buf.glyph_infos, buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + pos + p.x_offset * s, y - p.y_offset * s)))
        pos += p.x_advance * s + tracking
    return pen.getCommands(), pos

logo = open(os.path.join(HERE, 'm-mark.svg')).read()
inner = re.search(r'<svg[^>]*>(.*)</svg>', logo, re.S).group(1).replace('id="tl"', 'id="lt"').replace('url(#tl)', 'url(#lt)')

name, nw = shape('syne.woff2', 800, 'Mohamed Reda', 26, 266, 214, 1)
_, aw = shape('cairo-ar.woff2', 800, 'محمد رضا', 74, 0, 0)
ar, _ = shape('cairo-ar.woff2', 800, 'محمد رضا', 74, 266, 172)

# ---- terminal: the information, typed like code ----
MONO, CW, FS = 'JetBrainsMono-Bold.ttf', 9.0, 15
C = {'k': '#e8e9ec', 'p': '#7d818c', 's': '#c4ff47', 'c': '#7d818c', 'w': '#ffffff'}
lines = [  # list of (colour, text) segments per line
    [('c', '// vibe coding')],
    [('p', '$ '), ('w', 'vibe '), ('s', '"premium bilingual site"')],
    [('s', '✓ '), ('k', 'brand + design system')],
    [('s', '✓ '), ('k', 'web · api · database')],
    [('s', '✓ '), ('k', 'ai · bots · automation')],
    [('s', '→ '), ('w', 'live '), ('p', '· Kuwait · AR / EN')],
]
TX, TY, LH = 850, 112, 27       # text origin inside the card
TOTAL = 16.0                    # seconds per loop
STEP = 1.55                     # seconds each line takes to type
paths, css = '', ''
for i, segs in enumerate(lines):
    n = sum(len(t) for _, t in segs); x = TX; y = TY + i * LH
    g = ''
    for col, t in segs:
        d, adv = shape(MONO, 700, t, FS, x, y)
        g += f'<path d="{d}" fill="{C[col]}"/>'; x = x + len(t) * CW
    t0 = 0.8 + i * STEP; t1 = t0 + STEP * 0.8
    a, b = t0 / TOTAL * 100, t1 / TOTAL * 100
    css += (f'.t{i}{{animation:ty{i} {TOTAL}s steps({n}) infinite}}'
            f'@keyframes ty{i}{{0%,{a:.2f}%{{width:0}}{b:.2f}%,93%{{width:{n * CW + 2:.0f}px}}97%,100%{{width:0}}}}')
    paths += f'<clipPath id="cl{i}"><rect class="t{i}" x="{TX - 1}" y="{y - 20}" height="28" width="0"/></clipPath><g clip-path="url(#cl{i})">{g}</g>'
# cursor follows the line being typed
cur = ''
for i, segs in enumerate(lines):
    n = sum(len(t) for _, t in segs); t0 = 0.8 + i * STEP; t1 = t0 + STEP * 0.8
    a, b = t0 / TOTAL * 100, t1 / TOTAL * 100
    nxt = (t0 + STEP) / TOTAL * 100
    css += (f'.cu{i}{{opacity:0;animation:co{i} {TOTAL}s steps(1) infinite,cx{i} {TOTAL}s steps({n}) infinite}}'
            f'@keyframes co{i}{{0%{{opacity:0}}{a:.2f}%{{opacity:1}}{nxt:.2f}%{{opacity:0}}}}'
            f'@keyframes cx{i}{{0%,{a:.2f}%{{transform:translateX(0)}}{b:.2f}%,100%{{transform:translateX({n * CW:.0f}px)}}}}')
    cur += f'<rect class="cu{i}" x="{TX}" y="{TY + i * LH - 15}" width="8" height="19" fill="#c4ff47"/>'
last = len(lines) - 1
css += f'.blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}'

traces = ''.join(f'<path class="tr" d="{d}" style="animation-delay:{-i * 3}s"/><path class="tb" d="{d}"/>' for i, d in enumerate(
    ['M0 300H120L160 262H420L450 292H640', 'M1200 40H1060L1020 78H900']))
nodes = ''.join(f'<circle class="nd" cx="{x}" cy="{y}" r="4" style="animation-delay:{-i * .9}s"/>' for i, (x, y) in enumerate([(160, 262), (450, 292), (1060, 40)]))
rain = ''
import random; random.seed(11)
for i, x in enumerate([60, 210, 400, 560, 700, 790, 1100]):
    d = random.uniform(12, 20); delay = -random.uniform(0, 14)
    s = ''.join(random.choice('01{}</>=;') for _ in range(12))
    col = ''.join(f'<tspan x="{x}" dy="17">{ {"<": "&lt;", ">": "&gt;"}.get(c, c) }</tspan>' for c in s)
    rain += f'<text class="rain" style="animation-duration:{d:.1f}s;animation-delay:{delay:.1f}s">{col}</text>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" role="img" aria-label="Mohamed Reda, MR GFX. Full-stack developer, creative technologist, AI automation. Kuwait, Arabic and English.">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06070a"/><stop offset=".6" stop-color="#0a0e09"/><stop offset="1" stop-color="#0f1509"/></linearGradient>
<radialGradient id="gl"><stop offset="0" stop-color="#c4ff47" stop-opacity=".42"/><stop offset="1" stop-color="#c4ff47" stop-opacity="0"/></radialGradient>
<pattern id="hex" width="56" height="97" patternUnits="userSpaceOnUse" patternTransform="scale(.7)"><path d="M28 0L56 16V48L28 64L0 48V16ZM28 64V97" fill="none" stroke="#c4ff47" stroke-opacity=".045"/></pattern>
<clipPath id="r"><rect width="1200" height="340" rx="24"/></clipPath>
</defs>
<style>
.rain{{font:12px ui-monospace,Menlo,Consolas,monospace;fill:#c4ff47;opacity:0;animation:fall linear infinite}}
@keyframes fall{{0%{{transform:translateY(-220px);opacity:0}}15%,85%{{opacity:.16}}100%{{transform:translateY(340px);opacity:0}}}}
.tb{{fill:none;stroke:#c4ff47;stroke-opacity:.14;stroke-width:1.5}}
.tr{{fill:none;stroke:#c4ff47;stroke-width:2;stroke-linecap:round;stroke-dasharray:36 460;animation:flow 7s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-496}}}}
.nd{{fill:#c4ff47;transform-box:fill-box;transform-origin:center;animation:pulse 3.4s ease-in-out infinite}}@keyframes pulse{{50%{{opacity:.2;transform:scale(.6)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:spin 26s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}
.halo{{animation:halo 4s ease-in-out infinite}}@keyframes halo{{50%{{opacity:.5}}}}
.lg-head,.lg-rib{{transform-box:fill-box;transform-origin:center;animation:pop 1s cubic-bezier(.2,.9,.2,1) both}}.lg-rib{{animation-delay:.25s}}.mark{{animation:float 5s ease-in-out 1.4s infinite}}@keyframes float{{50%{{transform:translateY(-4px)}}}}
.lg-sw,.lg-star,.lg-chip{{animation:fade 1s .5s both}}
@keyframes pop{{from{{opacity:0;transform:translateY(24px) scale(.85)}}to{{opacity:1;transform:none}}}}@keyframes fade{{from{{opacity:0}}}}
.name{{animation:rise 1s .3s cubic-bezier(.2,.9,.2,1) both}}.ar{{animation:rise 1s .6s both}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}}}
.bar{{transform-origin:left;animation:grow 2s .2s cubic-bezier(.2,.9,.2,1) both}}@keyframes grow{{from{{transform:scaleX(0)}}}}
{css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.rain{{opacity:0}}{''.join(f'.t{i}{{width:300px}}' for i in range(len(lines)))}.tr{{stroke-dasharray:none;stroke-opacity:.3}}}}
</style>
<g clip-path="url(#r)">
<rect width="1200" height="340" fill="url(#bg)"/><rect width="1200" height="340" fill="url(#hex)"/>
{rain}
<circle cx="150" cy="170" r="250" fill="url(#gl)" class="halo"/>
{traces}{nodes}
<g transform="translate(58 82)">
 <circle class="ring" cx="88" cy="88" r="104" fill="none" stroke="#c4ff47" stroke-opacity=".4" stroke-dasharray="3 14" stroke-linecap="round"/>
 <svg class="mark" x="14" y="14" width="148" height="148" viewBox="0 0 40 40">{inner}</svg>
</g>
<g class="name"><path d="{name}" fill="#cfd2d8"/></g>
<g class="ar"><path d="{ar}" fill="#ffffff"/></g>
<g transform="translate(822 52)">
 <rect width="330" height="236" rx="16" fill="#07080b" fill-opacity=".88" stroke="#c4ff47" stroke-opacity=".3"/>
 <circle cx="22" cy="22" r="5" fill="#ff5f56"/><circle cx="40" cy="22" r="5" fill="#ffbd2e"/><circle cx="58" cy="22" r="5" fill="#c4ff47"/>
</g>
<g transform="translate(-0 0)">{paths}{cur}</g>
<rect class="bar" x="0" y="332" width="1200" height="8" fill="#c4ff47"/>
</g>
</svg>'''
open(os.path.join(OUT, 'header.svg'), 'w').write(svg)

# ---- stats ----
cards = [('10+', 'YEARS'), ('1000+', 'PROJECTS'), ('250+', 'CLIENTS')]; g = ''
for i, (n, l) in enumerate(cards):
    cx = 145 + i * 305
    _, wn = shape('syne.woff2', 800, n, 46, 0, 0); pn, _ = shape('syne.woff2', 800, n, 46, cx - wn / 2, 84)
    _, wl = shape('outfit.woff2', 600, l, 15, 0, 0, 3); pl, _ = shape('outfit.woff2', 600, l, 15, cx - wl / 2 + 0, 116, 3)
    g += f'<g class="c c{i + 1}"><rect class="card" x="{10 + i * 305}" y="10" width="270" height="130" rx="18"/><path d="{pn}" fill="#c4ff47"/><path d="{pl}" fill="#a6a6ad"/></g>'
open(os.path.join(OUT, 'stats.svg'), 'w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="150" viewBox="0 0 900 150" role="img" aria-label="10+ years, 1000+ projects, 250+ clients">
<style>.card{{fill:#0d0e12;stroke:#c4ff47;stroke-opacity:.22}}.c{{opacity:0;animation:in .8s ease-out forwards}}.c2{{animation-delay:.2s}}.c3{{animation-delay:.4s}}@keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}@media (prefers-reduced-motion:reduce){{.c{{animation:none;opacity:1}}}}</style>
{g}</svg>''')
print('ok')
