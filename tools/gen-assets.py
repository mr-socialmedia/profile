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

RIGHT = 936  # names end here, next to the logo on the right
_, aw = shape('cairo-ar.woff2', 800, 'محمد رضا', 74, 0, 0)
_, nw0 = shape('syne.woff2', 800, 'Mohamed Reda', 26, 0, 0, 0)
LS = 1.5                      # letter-spacing; the font size is then chosen so both names have exactly the same width
FSL = 26 * (aw - 11 * LS) / nw0
name, _ = shape('syne.woff2', 800, 'Mohamed Reda', FSL, RIGHT - aw, 214, LS)
ar, _ = shape('cairo-ar.woff2', 800, 'محمد رضا', 74, RIGHT - aw, 172)

# ---- terminal: the information, typed like code ----
MONO, CW, FS = 'JetBrainsMono-Bold.ttf', 9.0, 15
C = {'k': '#e8e9ec', 'p': '#7d818c', 's': '#c4ff47', 'c': '#7d818c', 'w': '#ffffff'}
lines = [  # list of (colour, text) segments per line
    [('c', '// vibe coding')],
    [('p', '$ '), ('w', 'whoami')],
    [('s', '> '), ('k', 'Full-stack developer')],
    [('s', '> '), ('k', 'Brand · Web · AI automation')],
    [('s', '✓ '), ('k', '10+ years · 1000+ projects')],
    [('s', '✓ '), ('k', '250+ clients · Gulf & Egypt')],
    [('s', '✓ '), ('k', 'Websites · Apps · Dashboards')],
    [('s', '✓ '), ('k', 'SEO · GEO · AI videos')],
    [('s', '→ '), ('w', 'www.mr-gfx.com')],
]
TX, TY, LH = 86, 94, 25       # text origin inside the card
TOTAL = 19.0                    # seconds per loop
STEP = 1.5                     # seconds each line takes to type
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
<circle cx="1054" cy="170" r="250" fill="url(#gl)" class="halo"/>
{traces}{nodes}
<g transform="translate(966 82)">
 <circle class="ring" cx="88" cy="88" r="104" fill="none" stroke="#c4ff47" stroke-opacity=".4" stroke-dasharray="3 14" stroke-linecap="round"/>
 <svg class="mark" x="14" y="14" width="148" height="148" viewBox="0 0 40 40">{inner}</svg>
</g>
<g class="name"><path d="{name}" fill="#cfd2d8"/></g>
<g class="ar"><path d="{ar}" fill="#ffffff"/></g>
<g transform="translate(58 34)">
 <rect width="330" height="272" rx="16" fill="#07080b" fill-opacity=".88" stroke="#c4ff47" stroke-opacity=".3"/>
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

# =====================================================================================================
# Panels for the README. Every image has its own dark background, so it reads on GitHub's light and dark themes.
# =====================================================================================================
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
PANEL_CSS = '''<style>
.in{opacity:0;animation:in .7s cubic-bezier(.2,.9,.2,1) forwards}
@keyframes in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pu 2.6s ease-in-out infinite}@keyframes pu{50%{transform:scale(1.7);opacity:.35}}
.grow{transform-box:fill-box;transform-origin:top;animation:gr 1.6s cubic-bezier(.2,.9,.2,1) both}@keyframes gr{from{transform:scaleY(0)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.in{opacity:1}}
</style>'''
def panel_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<defs><linearGradient id="pb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07080b"/><stop offset="1" stop-color="#0d130a"/></linearGradient>'
            f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#c4ff47" fill-opacity=".09"/></pattern></defs>{PANEL_CSS}'
            f'<rect width="{w}" height="{h}" rx="22" fill="url(#pb)"/><rect width="{w}" height="{h}" rx="22" fill="url(#dots)"/>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="21.5" fill="none" stroke="#c4ff47" stroke-opacity=".28"/>')

# ---- experience timeline (data: mr-gfx.com about page) ----
EXP = [('Jul 2026 – now', 'Marketing & AI Specialist', 'Al-Nawadi Holding'),
       ('2025 – now', 'Founder', 'Munjiz · Cairo'),
       ('2024 – now', 'Founder & CEO', 'Mashhor Hub LLC · Kuwait'),
       ('Jan 2023 – Jun 2026', 'Marketing Specialist', 'RAprime & Prime Media'),
       ('Apr 2022 – Aug 2023', 'Agency Manager', 'Media Life Advertising & Marketing'),
       ('Jan 2021 – May 2023', 'Social Media Specialist', 'Al-Dawaeya Pharmacies'),
       ('Dec 2019 – Jan 2021', 'Senior Graphic Designer', 'Pharma Life'),
       ('2018 – 2020', 'Content Creator & News Editor', 'Al-Shahed TV')]
W, RH, TOP = 1000, 62, 92
H = TOP + len(EXP) * RH + 26
t, _ = shape('syne.woff2', 800, 'EXPERIENCE', 15, 44, 46, 4)
s = panel_open(W, H, 'Experience: ' + '; '.join(f'{r}, {o}, {p}' for p, r, o in EXP)) + f'<path d="{t}" fill="#c4ff47"/>'
s += f'<rect class="grow" x="305" y="{TOP - 8}" width="2" height="{len(EXP) * RH - 24}" fill="#c4ff47" fill-opacity=".35"/>'
for i, (per, role, org) in enumerate(EXP):
    y = TOP + i * RH; d = f'style="animation-delay:{.15 + i * .18:.2f}s"'
    pp, pw = shape('outfit.woff2', 500, per, 17, 0, 0); pp, _ = shape('outfit.woff2', 500, per, 17, 280 - pw, y + 6)
    rr, _ = shape('syne.woff2', 700, role, 21, 336, y + 4)
    oo, _ = shape('outfit.woff2', 400, org, 17, 336, y + 30)
    live = 'now' in per
    s += (f'<g class="in" {d}><path d="{pp}" fill="{"#c4ff47" if live else "#9aa0aa"}"/>'
          f'<circle cx="306" cy="{y}" r="6" fill="#07080b" stroke="#c4ff47" stroke-width="2"/>'
          + (f'<circle class="pulse" cx="306" cy="{y}" r="3.5" fill="#c4ff47"/>' if live else '')
          + f'<path d="{rr}" fill="#ffffff"/><path d="{oo}" fill="#a9afb9"/></g>')
# right column: education and languages (from the about page)
side = [('EDUCATION', ["Bachelor's in Accounting", 'Faculty of Commerce, Cairo University', 'English section · 2014 – 2017']),
        ('LANGUAGES', ['Arabic · native', 'English · professional']),
        ('BASE', ['Kuwait · Egypt · the Gulf'])]
yy = TOP - 8
for j, (hd, ls) in enumerate(side):
    hp, _ = shape('syne.woff2', 800, hd, 13, 700, yy, 3); blk = f'<path d="{hp}" fill="#c4ff47"/>'
    for n, ln in enumerate(ls):
        lp, _ = shape('outfit.woff2', 500 if n == 0 else 400, ln, 17, 700, yy + 28 + n * 25)
        blk += f'<path d="{lp}" fill="{"#ffffff" if n == 0 else "#a9afb9"}"/>'
    s += f'<g class="in" style="animation-delay:{1.4 + j * .25:.2f}s">{blk}</g>'
    yy += 28 + len(ls) * 25 + 34
open(os.path.join(OUT, 'experience.svg'), 'w').write(s + '</svg>')

# ---- skills (data: mr-gfx.com about + stack pages) ----
GROUPS = [
 ('PROGRAMMING', ['Next.js', 'React', 'TypeScript', 'Node.js', 'Express', 'Python', 'Tailwind CSS', 'Expo · React Native', 'PostgreSQL', 'Supabase', 'Firebase', 'SQLite', 'Playwright', 'Vitest']),
 ('AI & AUTOMATION', ['Claude & OpenAI APIs', 'Gemini API', 'MCP servers', 'Make', 'n8n', 'Prompt workflows', 'CRM automation', 'Telegram bots']),
 ('MARKETING', ['Performance marketing', 'Media buying', 'Influencer marketing', 'SEO', 'GEO', 'Positioning & offers']),
 ('CREATIVE', ['Brand identity', 'Graphic design', 'Video production', 'AI videos', 'Campaign concepts', 'Content writing']),
]
W, PAD, CH, GAP = 1000, 44, 36, 10
y = 46; body = ''; k = 0
for title, items in GROUPS:
    tt, _ = shape('syne.woff2', 800, title, 15, PAD, y, 4); body += f'<g class="in" style="animation-delay:{k * .05:.2f}s"><path d="{tt}" fill="#c4ff47"/></g>'
    y += 22; x = PAD
    for it in items:
        _, w = shape('outfit.woff2', 600, it, 16, 0, 0); cw = w + 30
        if x + cw > W - PAD: x = PAD; y += CH + GAP
        p, _ = shape('outfit.woff2', 600, it, 16, x + 15, y + 23)
        body += (f'<g class="in" style="animation-delay:{.1 + k * .06:.2f}s"><rect x="{x}" y="{y}" width="{cw:.1f}" height="{CH}" rx="{CH / 2}" fill="#10140c" stroke="#c4ff47" stroke-opacity=".38"/>'
                 f'<path d="{p}" fill="#f2f4f7"/></g>')
        x += cw + GAP; k += 1
    y += CH + 34
H = y - 8
open(os.path.join(OUT, 'skills.svg'), 'w').write(panel_open(W, H, 'Skills: ' + '; '.join(f'{t}: ' + ', '.join(i) for t, i in GROUPS)) + body + '</svg>')

# ---- tagline: own dark pill, readable on any GitHub theme ----
tl = ['I build brands, sites, dashboards and automation.', 'Websites, apps, bots and AI workflows, built end to end.',
      'Marketing and engineering under one roof.', 'Bilingual Arabic / English, RTL done right.']
texts = ''; css = ''
for i, line in enumerate(tl):
    _, lw = shape(MONO, 700, line, 20, 0, 0); p, _ = shape(MONO, 700, line, 20, 450 - lw / 2, 33)
    texts += f'<path class="l l{i}" d="{p}" fill="#c4ff47"/>'; css += f'.l{i}{{animation-delay:{i * 3}s}}'
open(os.path.join(OUT, 'tagline.svg'), 'w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="52" viewBox="0 0 900 52" role="img" aria-label="{esc(' '.join(tl))}">
<style>.l{{opacity:0;animation:cy 12s infinite}}{css}@keyframes cy{{0%{{opacity:0;transform:translateY(8px)}}4%,22%{{opacity:1;transform:none}}27%,100%{{opacity:0;transform:translateY(-8px)}}}}@media (prefers-reduced-motion:reduce){{.l{{animation:none;opacity:0}}.l0{{opacity:1}}}}</style>
<rect width="900" height="52" rx="26" fill="#07080b"/><rect x=".5" y=".5" width="899" height="51" rx="25.5" fill="none" stroke="#c4ff47" stroke-opacity=".4"/>
<circle cx="30" cy="26" r="4" fill="#c4ff47"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>{texts}</svg>''')

# ---- divider: mid green with a dark core, visible on white and on black ----
open(os.path.join(OUT, 'divider.svg'), 'w').write('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="20" viewBox="0 0 1200 20" aria-hidden="true">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7cb800" stop-opacity="0"/><stop offset=".5" stop-color="#7cb800"/><stop offset="1" stop-color="#7cb800" stop-opacity="0"/></linearGradient></defs>
<rect y="9" width="1200" height="2" fill="url(#g)"/>
<circle cy="10" r="5.5" fill="#c4ff47" stroke="#07080b" stroke-width="2"><animate attributeName="cx" values="0;1200" dur="5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="5s" repeatCount="indefinite"/></circle></svg>''')
print('panels ok')
