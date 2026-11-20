import re, random
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W='/home/user/MR-WEB/web/scripts/telegram-assets/'
def load(name, wght):
    f=TTFont(W+name); f=instantiateVariableFont(f,{'wght':wght}); f.flavor=None; import io
    b=io.BytesIO(); f.save(b); return f,b.getvalue()
def text_path(name,wght,text,size,x,y,rtl=False,tracking=0):
    f,data=load(name,wght); face=hb.Face(data); font=hb.Font(face)
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font,buf,{"kern":True,"liga":True})
    gs=f.getGlyphSet(); order=f.getGlyphOrder(); upm=f['head'].unitsPerEm; s=size/upm
    total=sum(p.x_advance for p in buf.glyph_positions)*s+tracking*len(buf.glyph_infos)
    cx=x-total if rtl else x
    pen=SVGPathPen(gs,ntos=lambda v:('%.1f'%v).rstrip('0').rstrip('.')); pos=0
    for info,p in zip(buf.glyph_infos,buf.glyph_positions):
        g=order[info.codepoint]
        tp=TransformPen(pen,(s,0,0,-s,cx+pos+p.x_offset*s,y-p.y_offset*s)); gs[g].draw(tp)
        pos+=p.x_advance*s+tracking
    return pen.getCommands(), total

logo=open('/home/user/MR-WEB/web/public/brand/mr-mark.svg').read()
inner=re.search(r'<svg[^>]*>(.*)</svg>',logo,re.S).group(1)
inner=inner.replace('id="tl"','id="lt"').replace('url(#tl)','url(#lt)')

name,_=text_path('syne.woff2',800,'Mohamed Reda',46,262,172,tracking=0)
role,_=text_path('outfit.woff2',400,'Full-stack developer  ·  Creative technologist  ·  AI automation',21,264,214)
ar,_=text_path('cairo-ar.woff2',700,'محمد رضا، أبني الهوية والمواقع والأنظمة',27,1000-0,262,rtl=False)
# arabic: place left aligned at 264 using total width
ar,aw=text_path('cairo-ar.woff2',700,'محمد رضا، أبني الهوية والمواقع والأنظمة',27,264,262)
eyebrow,_=text_path('outfit.woff2',600,'MR GFX  ·  KUWAIT  ·  AR / EN',15,264,120,tracking=3)

random.seed(7)
cols=''
chars='01{}<>/=;$#'
for i in range(26):
    x=20+i*46+random.randint(-8,8); d=random.uniform(9,18); delay=-random.uniform(0,18)
    s=''.join(random.choice(chars) for _ in range(14))
    col=''.join(f'<tspan x="{x}" dy="16">{c if c not in "<>" else {"<":"&lt;",">":"&gt;"}[c]}</tspan>' for c in s)
    cols+=f'<text class="rain" style="animation-duration:{d:.1f}s;animation-delay:{delay:.1f}s">{col}</text>'
circ=[
 'M0 300H120L160 260H420L450 290H760',
 'M1200 60H1040L1000 100H820L790 70H600',
 'M0 40H90L120 70H240',
 'M1200 320H1100L1070 290H930',
]
traces=''.join(f'<path class="tr" d="{d}" style="animation-delay:{-i*1.7}s"/><path class="tb" d="{d}"/>' for i,d in enumerate(circ))
nodes=''.join(f'<circle class="nd" cx="{x}" cy="{y}" r="4" style="animation-delay:{-i*.6}s"/>' for i,(x,y) in enumerate([(160,260),(450,290),(760,300),(1040,60),(820,100),(600,60),(240,70),(1070,290),(930,290)]))

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" role="img" aria-label="Mohamed Reda, MR GFX. Full-stack developer, creative technologist, AI automation.">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06070a"/><stop offset=".6" stop-color="#0b0f0a"/><stop offset="1" stop-color="#10160a"/></linearGradient>
<radialGradient id="gl"><stop offset="0" stop-color="#c4ff47" stop-opacity=".5"/><stop offset="1" stop-color="#c4ff47" stop-opacity="0"/></radialGradient>
<linearGradient id="ink" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#f1ffd0"/><stop offset="1" stop-color="#c4ff47"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4ff47" stop-opacity="0"/><stop offset=".5" stop-color="#c4ff47" stop-opacity=".16"/><stop offset="1" stop-color="#c4ff47" stop-opacity="0"/></linearGradient>
<pattern id="hex" width="56" height="97" patternUnits="userSpaceOnUse" patternTransform="scale(.7)"><path d="M28 0L56 16V48L28 64L0 48V16ZM28 64V97M0 48L-28 64M56 48L84 64" fill="none" stroke="#c4ff47" stroke-opacity=".07"/></pattern>
<clipPath id="r"><rect width="1200" height="340" rx="24"/></clipPath>
<mask id="fade"><rect width="1200" height="340" fill="#fff"/><rect width="1200" height="340" fill="url(#lm)"/></mask>
<linearGradient id="lm" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
</defs>
<style>
.rain{{font:12px ui-monospace,Menlo,Consolas,monospace;fill:#c4ff47;opacity:0;animation:fall linear infinite}}
@keyframes fall{{0%{{transform:translateY(-240px);opacity:0}}15%{{opacity:.22}}85%{{opacity:.22}}100%{{transform:translateY(340px);opacity:0}}}}
.tb{{fill:none;stroke:#c4ff47;stroke-opacity:.18;stroke-width:1.5}}
.tr{{fill:none;stroke:#c4ff47;stroke-width:2.2;stroke-linecap:round;stroke-dasharray:40 400;animation:flow 6s linear infinite;filter:drop-shadow(0 0 4px #c4ff47)}}
@keyframes flow{{to{{stroke-dashoffset:-440}}}}
.nd{{fill:#c4ff47;animation:pulse 3s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.2;transform:scale(.6)}}}}
.nd{{transform-box:fill-box;transform-origin:center}}
.scan{{animation:sc 7s linear infinite}}@keyframes sc{{from{{transform:translateY(-120px)}}to{{transform:translateY(340px)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}
.ring2{{animation-duration:16s;animation-direction:reverse}}
.halo{{animation:halo 4s ease-in-out infinite}}@keyframes halo{{50%{{opacity:.45}}}}
.lg-m{{transform-box:fill-box;transform-origin:center;animation:pop 1s cubic-bezier(.2,.9,.2,1) both}}
.lg-r{{transform-box:fill-box;transform-origin:center;animation:pop 1s .2s cubic-bezier(.2,.9,.2,1) both}}
.lg-sw,.lg-star,.lg-chip{{animation:fade 1s .5s both}}
@keyframes pop{{from{{opacity:0;transform:translateY(24px) scale(.85)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.name{{animation:rise 1s .3s cubic-bezier(.2,.9,.2,1) both}}.role{{animation:rise 1s .55s both}}.ar{{animation:rise 1s .75s both}}.eb{{animation:rise 1s .1s both}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.bar{{animation:grow 2s .2s cubic-bezier(.2,.9,.2,1) both}}@keyframes grow{{from{{transform:scaleX(0)}}}}.bar{{transform-origin:left}}
.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.ln{{opacity:0;animation:ty 10s infinite}}.l2{{animation-delay:1.2s}}.l3{{animation-delay:2.4s}}.l4{{animation-delay:3.6s}}
@keyframes ty{{0%{{opacity:0;transform:translateX(-8px)}}5%,90%{{opacity:1;transform:none}}100%{{opacity:0}}}}
.term{{font:600 13px ui-monospace,Menlo,Consolas,monospace}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.rain{{opacity:.12}}.ln{{opacity:1}}.tr{{stroke-dasharray:none;stroke-opacity:.4}}}}
</style>
<g clip-path="url(#r)">
<rect width="1200" height="340" fill="url(#bg)"/>
<rect width="1200" height="340" fill="url(#hex)"/>
<g>{cols}</g>
<circle cx="150" cy="170" r="260" fill="url(#gl)" class="halo"/>
<circle cx="1050" cy="300" r="220" fill="url(#gl)" opacity=".35"/>
{traces}{nodes}
<rect class="scan" width="1200" height="120" fill="url(#scan)"/>
<g transform="translate(58 82)">
 <circle class="ring" cx="88" cy="88" r="102" fill="none" stroke="#c4ff47" stroke-opacity=".45" stroke-dasharray="3 14" stroke-linecap="round"/>
 <circle class="ring ring2" cx="88" cy="88" r="118" fill="none" stroke="#c4ff47" stroke-opacity=".2" stroke-dasharray="40 30"/>
 <svg x="14" y="14" width="148" height="148" viewBox="0 0 40 40">{inner}</svg>
</g>
<g class="eb"><path d="{eyebrow}" fill="#c4ff47" opacity=".85"/></g>
<g class="name"><path d="{name}" fill="url(#ink)"/></g>
<g class="role"><path d="{role}" fill="#d8dadf"/></g>
<g class="ar"><path d="{ar}" fill="#c4ff47"/></g>
<g transform="translate(880 96)">
 <rect width="272" height="150" rx="14" fill="#07080b" fill-opacity=".82" stroke="#c4ff47" stroke-opacity=".3"/>
 <circle cx="20" cy="20" r="5" fill="#ff5f56"/><circle cx="38" cy="20" r="5" fill="#ffbd2e"/><circle cx="56" cy="20" r="5" fill="#c4ff47"/>
 <g class="term">
  <text class="ln" x="20" y="58" fill="#8b8f98">$ <tspan fill="#e8e9ec">npm run ship</tspan></text>
  <text class="ln l2" x="20" y="82" fill="#c4ff47">✓ brand · design system</text>
  <text class="ln l3" x="20" y="104" fill="#c4ff47">✓ web · api · database</text>
  <text class="ln l4" x="20" y="126" fill="#c4ff47">✓ automation · live <tspan class="cur">▌</tspan></text>
 </g>
</g>
<rect class="bar" x="0" y="332" width="1200" height="8" fill="#c4ff47"/>
</g>
</svg>'''
open('/home/user/profile/assets/header.svg','w').write(svg)
print(len(svg))

# stats with brand font as outlines
cards=[('10+','YEARS'),('1000+','PROJECTS'),('250+','CLIENTS')]
g=''
for i,(n,l) in enumerate(cards):
    cx=145+i*305
    _,wn=text_path('syne.woff2',800,n,46,0,0); pn,_=text_path('syne.woff2',800,n,46,cx-wn/2,84)
    _,wl=text_path('outfit.woff2',600,l,15,0,0,tracking=3); pl,_=text_path('outfit.woff2',600,l,15,cx-wl/2,116,tracking=3)
    g+=f'<g class="c c{i+1}"><rect class="card" x="{10+i*305}" y="10" width="270" height="130" rx="18"/><path d="{pn}" fill="#c4ff47"/><path d="{pl}" fill="#a6a6ad"/></g>'
st=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="150" viewBox="0 0 900 150" role="img" aria-label="10+ years, 1000+ projects, 250+ clients">
<style>.card{{fill:#0d0e12;stroke:#c4ff47;stroke-opacity:.22}}.c{{opacity:0;animation:in .8s ease-out forwards}}.c2{{animation-delay:.2s}}.c3{{animation-delay:.4s}}@keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}@media (prefers-reduced-motion:reduce){{.c{{animation:none;opacity:1}}}}</style>
{g}</svg>'''
open('/home/user/profile/assets/stats.svg','w').write(st)
