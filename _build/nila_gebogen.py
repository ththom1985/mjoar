"""NILA neu (Thorsten 14.11.): gebogene Glashalme mit kleinem Logo unten, Bleistiftstil wie zeichnung.py."""
import math, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zeichnung import kopf, FUSS, strich, STIFT
W = H = 400
logo = open(r"C:/dev/mjoar/assets/start/../web/logo.svg" if os.path.exists(r"C:/dev/mjoar/assets/web/logo.svg") else r"../webdesign/a/logo.svg", encoding="utf-8").read()
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', logo).group(1).split()]
inner = re.sub(r'^[\s\S]*?<svg[^>]*>', '', logo).replace('</svg>', '').replace('currentColor', STIFT)

def mittellinie(x0, yb, lg, kn, bogen, oben, r_bogen=26, n=40):
    """Punkte von unten nach oben: gerader Schaft, Bogen nach rechts (Winkel bogen°), kurzes Endstück."""
    pts = [(x0, yb), (x0, yb - lg)]
    cx, cy = x0 + r_bogen, yb - lg
    for i in range(1, n + 1):
        a = math.radians(180 - bogen * i / n)
        pts.append((cx + r_bogen * math.cos(a), cy - r_bogen * math.sin(a)))
    a = math.radians(bogen)                      # Richtung des Endstücks
    ex, ey = pts[-1]; d = (math.sin(a), -math.cos(a))
    pts.append((ex + d[0] * oben, ey + d[1] * oben))
    return pts

def versatz(pts, r):
    links, rechts = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        links.append((x + nx * r, y + ny * r)); rechts.append((x - nx * r, y - ny * r))
    return links, rechts

def p(pts): return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)

def halm(x0, yb, lg, bogen, grau, i):
    r = 6.5
    m = mittellinie(x0, yb, lg, 0, bogen, 34)
    l, re_ = versatz(m, r)
    out = strich(p(l), 1.1, .88) + strich(p(re_), 1.1, .88)
    # Öffnungen als Ellipsen quer zur Richtung
    for (a, b) in [(l[0], re_[0]), (l[-1], re_[-1])]:
        cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        out += f'<g transform="rotate({ang:.1f} {cx:.1f} {cy:.1f})">' + strich(f"M{cx-r:.1f} {cy:.1f} A{r} 2.6 0 1 1 {cx+r:.1f} {cy:.1f} A{r} 2.6 0 1 1 {cx-r:.1f} {cy:.1f}", .85, .75) + '</g>'

    if grau:   # Rauchglas: feine Schraffur im Schaft
        for k in range(30):
            t = k / 29; yy = yb - 6 - t * (lg - 10)
            out += f'<path d="M{x0-r+1.6:.1f} {yy+3.5:.1f} L{x0+r-1.6:.1f} {yy-2.5:.1f}" stroke="{STIFT}" stroke-width=".55" opacity=".33"/>\n'
    else:      # Klarglas: Glanzlinie
        out += f'<path d="M{x0+r-2.6:.1f} {yb-14:.1f} L{x0+r-2.6:.1f} {yb-lg+6:.1f}" stroke="{STIFT}" stroke-width=".5" opacity=".28"/>\n'
    # kleines Logo längs, unten
    lw = 44; s = lw / vb[2]; lh = vb[3] * s
    out += (f'<g transform="translate({x0-lh/2:.1f} {yb-14:.1f}) rotate(-90) scale({s:.4f}) translate({-vb[0]:.2f} {-vb[1]:.2f})" opacity=".62">'
            f'{inner}</g>\n')
    return out

out = kopf()
basis = 352; lg = 236
for i, (dx, grau, bogen) in enumerate([(-63, False, 38), (-21, True, 38), (21, False, 38), (63, True, 38)]):
    out += halm(188 + dx, basis + (i % 2) * 4, lg - (i % 2) * 4, bogen, grau, i)
svg = out.replace(f'viewBox="0 0 400 500"', 'viewBox="0 0 400 400"') + ""
svg = svg if 'viewBox="0 0 400 400"' in svg else svg.replace('viewBox="0 0 ', 'viewBox="0 0 ', 1)
open(os.path.join(os.path.dirname(__file__), "nila_gebogen.svg"), "w", encoding="utf-8").write(svg + FUSS if not svg.endswith(FUSS) else svg)
print("ok")
