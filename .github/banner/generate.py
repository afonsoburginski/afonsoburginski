"""Generates assets/banner.svg: animated ASCII gradient banner for the profile README."""
import math

COLS, ROWS, FRAMES, DUR = 118, 13, 16, 8
CW, LH, FS = 7.2, 15, 12
W, H = 880, ROWS * LH + 34
X0, Y0 = (W - COLS * CW) / 2, 30
RAMP = "·.:-=+*#%@"
BG, FG = "#0d1117", "#e6edf3"


def field(x, y, t):
    v = (math.sin(x * 0.085 + t) + math.sin(y * 0.9 + x * 0.05 - t) + math.sin(x * 0.045 + y * 0.28 + t)
         + math.sin(math.hypot(x - COLS / 2, (y - ROWS / 2) * 3) * 0.16 - t * 2)) / 4
    return (v + 1) / 2


def frame(k):
    t = 2 * math.pi * k / FRAMES
    rows = []
    for y in range(ROWS):
        s = "".join(RAMP[min(int(field(x, y, t) * len(RAMP)), len(RAMP) - 1)] for x in range(COLS))
        rows.append(f'<text x="{X0}" y="{Y0 + y * LH}" textLength="{COLS * CW:.1f}" lengthAdjust="spacing">{s}</text>')
    return "".join(rows)


frames = "".join(
    f'<g class="f" style="animation-delay:-{DUR - k * DUR / FRAMES:.3f}s" fill="url(#g)">{frame(k)}</g>'
    for k in range(FRAMES)
)
step = 100 / FRAMES
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Afonso Burginski — Senior Software Engineer">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{FS}px;white-space:pre}}
.f{{opacity:0;animation:show {DUR}s steps(1,end) infinite}}
@keyframes show{{0%{{opacity:1}}{step:.3f}%{{opacity:0}}100%{{opacity:0}}}}
.t{{font-size:34px;font-weight:700;fill:{FG};letter-spacing:3px}}
.s{{font-size:12px;fill:#9da7b3;letter-spacing:1px}}
</style>
<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="#2dd4bf"/><stop offset=".5" stop-color="#60a5fa"/><stop offset="1" stop-color="#a78bfa"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{W} 0" dur="{DUR}s" repeatCount="indefinite"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
{frames}
<rect x="{W/2-320}" y="{H/2-44}" width="640" height="88" rx="10" fill="{BG}" fill-opacity=".86"/>
<text class="t" x="{W/2}" y="{H/2-4}" text-anchor="middle">AFONSO BURGINSKI</text>
<text class="s" x="{W/2}" y="{H/2+24}" text-anchor="middle">SENIOR SOFTWARE ENGINEER · VIDEO STREAMING · DISTRIBUTED SYSTEMS</text>
</svg>'''
open("assets/banner.svg", "w").write(svg)
print(len(svg) // 1024, "KB")
