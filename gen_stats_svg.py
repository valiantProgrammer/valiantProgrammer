"""Generates stats-dashboard.svg, an animated profile stats dashboard.
Edit the DATA section, run `python gen_stats_svg.py`, commit the SVG."""
import math

# ---------------- DATA (edit me) ----------------
STATS = [("Total Stars", 6), ("Total Commits", 527), ("Total PRs", 2),
         ("Total Issues", 0), ("Contributed to", 26)]
COMMIT_LANGS = [("JavaScript", 36, "#f1e05a"), ("Jupyter Notebook", 36, "#DA5B0B"),
                ("Python", 22, "#3572A5"), ("CSS", 4, "#8a5cf5"), ("HTML", 2, "#e34c26")]
REPO_LANGS = [("Jupyter Notebook", 38, "#DA5B0B"), ("JavaScript", 30, "#f1e05a"),
              ("Python", 14, "#3572A5"), ("CSS", 11, "#8a5cf5"), ("TypeScript", 7, "#3178c6")]
# commits per UTC hour, 0..23
HOURS = [0, 0, 4, 1, 8, 9, 10, 10, 16, 13, 18, 13, 19, 14, 59, 30, 23, 42, 27, 34, 10, 0, 0, 0]
ACCENT, ACCENT2 = "#00FFD4", "#00CED1"
# ------------------------------------------------

W, H = 900, 540
CARD_W, CARD_H = 430, 245
POS = [(10, 10), (460, 10), (10, 285), (460, 285)]

css = """
text{font-family:'Courier New',Consolas,monospace}
.title{font-size:19px;font-weight:700;fill:#00FFD4}
.lbl{font-size:14px;fill:#c9d1d9}
.val{font-size:14px;font-weight:700;fill:#00FFD4}
.sub{font-size:11px;fill:#8b949e}
.card{fill:url(#bg);stroke:#00CED1;stroke-opacity:.55;stroke-width:1.2}
.fade{opacity:0;animation:fade .7s ease-out forwards}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.seg{fill:none;stroke-width:22;animation:draw 1.4s cubic-bezier(.4,0,.2,1) forwards;stroke-dasharray:0 400}
@keyframes draw{to{stroke-dasharray:var(--len) 400}}
.bar{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:grow .8s cubic-bezier(.3,1.3,.5,1) forwards}
@keyframes grow{to{transform:scaleY(1)}}
.ring{fill:none;stroke:#00FFD4;stroke-width:3;stroke-linecap:round;stroke-dasharray:60 254;
transform-box:fill-box;transform-origin:center;animation:spin 4s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.25;transform:scale(1)}50%{opacity:.7;transform:scale(1.08)}}
.scan{animation:scan 5s linear infinite}
@keyframes scan{from{transform:translateX(-440px)}to{transform:translateX(900px)}}
"""

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
         f'<stop offset="0" stop-color="#0a0a0a"/><stop offset="1" stop-color="#0d1b1f"/></linearGradient>'
         f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="#8a5cf5"/></linearGradient>'
         f'<linearGradient id="sc" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{ACCENT}" stop-opacity=".12"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="all"><rect width="{W}" height="{H}"/></clipPath></defs>')
o.append(f'<style>{css}</style>')


def card(i, title, delay):
    x, y = POS[i]
    o.append(f'<g class="fade" style="animation-delay:{delay}s">')
    o.append(f'<rect class="card" x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="14"/>')
    o.append(f'<text class="title" x="{x+24}" y="{y+38}">{title}</text>')
    o.append(f'<line x1="{x+24}" y1="{y+48}" x2="{x+70}" y2="{y+48}" stroke="{ACCENT}" stroke-width="2"/>')
    return x, y


def donut(x, y, data, delay):
    cx, cy, r = x + 330, y + 140, 58
    C = 2 * math.pi * r
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#161b22" stroke-width="22"/>')
    cum = 0
    for k, (_, pct, col) in enumerate(data):
        ln = pct / 100 * C - 2
        ang = -90 + cum * 3.6
        o.append(f'<circle class="seg" cx="{cx}" cy="{cy}" r="{r}" stroke="{col}" '
                 f'transform="rotate({ang:.2f} {cx} {cy})" '
                 f'style="--len:{ln:.2f}px;animation-delay:{delay+k*0.15:.2f}s"/>')
        cum += pct
    for k, (name, pct, col) in enumerate(data):
        ly = y + 82 + k * 30
        o.append(f'<rect x="{x+24}" y="{ly-11}" width="13" height="13" rx="3" fill="{col}"/>')
        o.append(f'<text class="lbl" x="{x+46}" y="{ly}">{name}</text>')
        o.append(f'<text class="sub" x="{x+210}" y="{ly}" text-anchor="end">{pct}%</text>')


# Card 0: stats
x, y = card(0, "Stats", 0.0)
for k, (n, v) in enumerate(STATS):
    ry = y + 80 + k * 30
    o.append(f'<circle cx="{x+30}" cy="{ry-5}" r="3.5" fill="{ACCENT}"/>')
    o.append(f'<text class="lbl" x="{x+46}" y="{ry}">{n}</text>')
    o.append(f'<text class="val" x="{x+230}" y="{ry}" text-anchor="end">{v}</text>')
cx, cy = x + 330, y + 140
o.append(f'<circle class="pulse" cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{ACCENT}" stroke-width="1"/>')
o.append(f'<circle cx="{cx}" cy="{cy}" r="50" fill="#0d1b1f" stroke="#161b22" stroke-width="4"/>')
o.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="50"/>')
commits = dict(STATS).get("Total Commits", 0)
o.append(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="26" font-weight="700" fill="{ACCENT}">{commits}</text>')
o.append(f'<text class="sub" x="{cx}" y="{cy+22}" text-anchor="middle">commits</text>')
o.append('</g>')

# Card 1 and 2: donuts
x, y = card(1, "Top Languages by Commit", 0.15)
donut(x, y, COMMIT_LANGS, 0.5)
o.append('</g>')
x, y = card(2, "Top Languages by Repo", 0.3)
donut(x, y, REPO_LANGS, 0.7)
o.append('</g>')

# Card 3: commits per hour
x, y = card(3, "Commits by Hour (UTC)", 0.45)
base, maxh, bw, gap = y + 212, 120, 12, 3.8
mx = max(HOURS) or 1
for k, v in enumerate(HOURS):
    if v == 0:
        continue
    h = v / mx * maxh
    bx = x + 28 + k * (bw + gap)
    o.append(f'<rect class="bar" x="{bx:.1f}" y="{base-h:.1f}" width="{bw}" height="{h:.1f}" rx="2" '
             f'fill="url(#bar)" style="animation-delay:{0.8+k*0.04:.2f}s"/>')
o.append(f'<line x1="{x+24}" y1="{base}" x2="{x+CARD_W-20}" y2="{base}" stroke="#30363d"/>')
for hr in (0, 6, 12, 18, 23):
    tx = x + 28 + hr * (bw + gap) + bw / 2
    o.append(f'<text class="sub" x="{tx:.1f}" y="{base+16}" text-anchor="middle">{hr}</text>')
o.append('</g>')

# scanning light across everything
o.append(f'<g clip-path="url(#all)"><rect class="scan" x="0" y="0" width="120" height="{H}" fill="url(#sc)"/></g>')
o.append('</svg>')

with open("stats-dashboard.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote stats-dashboard.svg")
