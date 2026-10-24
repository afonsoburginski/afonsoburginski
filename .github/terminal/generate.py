"""Generates assets/terminal.svg — a typing terminal animation for the profile README.
Each character is revealed on its own timer, so it works with any monospace font.
Usage: python3 .github/terminal/generate.py [--static]  (--static = final frame, for previews)"""
import sys
from xml.sax.saxutils import escape

STATIC = "--static" in sys.argv
W, BAR, PAD_X, TOP, LH, FS = 820, 40, 34, 84, 29, 15
CMD_T, OUT_T, GAP, HOLD = 0.05, 0.014, 0.4, 5.0

# kind: cmd = "$ " prompt + typed command · out = output · link = highlighted output
LINES = [
    ("cmd", "whoami"),
    ("out", "afonso burginski · senior software engineer"),
    ("cmd", "cat specialty.txt"),
    ("out", "video streaming · real-time media · distributed systems"),
    ("cmd", "ls case-studies/"),
    ("out", "stormz-plus   orbit   studio   nextjs-ffmpeg-transcoder"),
    ("cmd", "open afonsodev.com"),
    ("link", "→ https://afonsodev.com"),
]
C = dict(bg="#0d1117", bar="#161b22", prompt="#ffb020", cmd="#e6edf3", out="#7aa2f7", link="#ffb020", dim="#6e7681")
H = TOP + (len(LINES) + 1) * LH + 6

# pass 1: schedule
t, sched = 0.6, []
for kind, text in LINES:
    step = CMD_T if kind == "cmd" else OUT_T
    sched.append((kind, text, t, step))
    t += len(text) * step + (len("$ ") * 0 if kind != "cmd" else 0) + GAP
cursor_t = t - GAP
total = t + HOLD


def anim(start):
    if STATIC:
        return ""
    k = start / total
    return (f'<animate attributeName="fill-opacity" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" '
            f'keyTimes="0;{k:.5f};1" values="0;1;1"/>')


rows = []
for i, (kind, text, t0, step) in enumerate(sched):
    y = TOP + i * LH
    parts = []
    if kind == "cmd":
        parts.append(f'<tspan fill="{C["prompt"]}" font-weight="700" fill-opacity="{1 if STATIC else 0}">$ {anim(t0 - 0.05)}</tspan>')
    color = {"cmd": C["cmd"], "out": C["out"], "link": C["link"]}[kind]
    weight = ' font-weight="700"' if kind == "link" else ""
    for j, ch in enumerate(text):
        parts.append(f'<tspan fill="{color}"{weight} fill-opacity="{1 if STATIC else 0}">{escape(ch)}{anim(t0 + j * step)}</tspan>')
    rows.append(f'<text x="{PAD_X}" y="{y}">{"".join(parts)}</text>')

cy = TOP + len(LINES) * LH
k = cursor_t / total
cursor = (f'<animate attributeName="opacity" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" '
          f'keyTimes="0;{k:.5f};{k + 0.04:.5f};{k + 0.08:.5f};{k + 0.12:.5f};{k + 0.16:.5f};{k + 0.20:.5f};1" values="0;1;0;1;0;1;0;1"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: afonso burginski, senior software engineer. Video streaming, real-time media, distributed systems. afonsodev.com">
<style>text{{font-family:ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,monospace;font-size:{FS}px;white-space:pre}}</style>
<rect width="{W}" height="{H}" rx="12" fill="{C['bg']}" stroke="#30363d"/>
<path d="M0 12a12 12 0 0 1 12-12h{W-24}a12 12 0 0 1 12 12v{BAR-12}H0z" fill="{C['bar']}"/>
<circle cx="24" cy="{BAR/2}" r="6" fill="#ff5f56"/><circle cx="46" cy="{BAR/2}" r="6" fill="#ffbd2e"/><circle cx="68" cy="{BAR/2}" r="6" fill="#27c93f"/>
<text x="{W/2}" y="{BAR/2+5}" text-anchor="middle" fill="{C['dim']}" style="font-size:13px">afonso@portfolio — ~</text>
{"".join(rows)}
<text x="{PAD_X}" y="{cy}" fill="{C['prompt']}" font-weight="700">$ </text>
<rect x="{PAD_X + 20}" y="{cy - FS + 1}" width="9" height="{FS + 3}" fill="{C['cmd']}" opacity="{1 if STATIC else 0}">{"" if STATIC else cursor}</rect>
</svg>'''
open("assets/terminal.svg", "w").write(svg)
print(round(len(svg) / 1024, 1), "KB · cycle", round(total, 1), "s")
