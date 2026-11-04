#!/usr/bin/env python3
"""
make_diagrams.py – erzeugt die schematischen Technik-Grafiken (SVG, DE/EN).
Generates the schematic technique diagrams (SVG, German/English labels).

  python3 scripts/make_diagrams.py
  → content/assets/diagrams/<name>-de.svg / <name>-en.svg

Farben: Palette unten (PAL) – an design/theme.ts angelehnt; hier ändern, Skript neu laufen lassen.
"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "assets" / "diagrams"

PAL = dict(
    ink="#231f1b",
    muted="#6d665d",
    steel="#7a7f87",
    steel_dark="#4b4f55",
    anvil="#3d3f43",
    anvil_face="#5b5e64",
    wood="#9a6a3a",
    arrow="#b4471b",
    accent2="#2f5d7c",
    hot1="#fff2b0",
    hot2="#ffb347",
    hot3="#e2632b",
    hot4="#9b3a1a",
    paper="#fffdf9",
)
FONT = "Alegreya Sans, Source Sans Pro, Helvetica, Arial, sans-serif"


# ------------------------------------------------------------------ primitives
def svg(w, h, body, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
  <linearGradient id="hot" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{PAL['hot4']}"/><stop offset="0.35" stop-color="{PAL['hot3']}"/>
    <stop offset="0.7" stop-color="{PAL['hot2']}"/><stop offset="1" stop-color="{PAL['hot1']}"/>
  </linearGradient>
  <linearGradient id="hotR" x1="1" x2="0" y1="0" y2="0">
    <stop offset="0" stop-color="{PAL['hot4']}"/><stop offset="0.35" stop-color="{PAL['hot3']}"/>
    <stop offset="0.7" stop-color="{PAL['hot2']}"/><stop offset="1" stop-color="{PAL['hot1']}"/>
  </linearGradient>
  <linearGradient id="hotEven" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{PAL['hot2']}"/><stop offset="1" stop-color="{PAL['hot3']}"/>
  </linearGradient>
  <linearGradient id="hotEnd" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{PAL['steel']}"/><stop offset="0.55" stop-color="{PAL['steel']}"/>
    <stop offset="0.7" stop-color="{PAL['hot4']}"/><stop offset="0.85" stop-color="{PAL['hot3']}"/><stop offset="1" stop-color="{PAL['hot2']}"/>
  </linearGradient>
  <linearGradient id="hotTop" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{PAL['hot2']}"/><stop offset="0.3" stop-color="{PAL['hot3']}"/>
    <stop offset="0.5" stop-color="{PAL['hot4']}"/><stop offset="0.65" stop-color="{PAL['steel']}"/><stop offset="1" stop-color="{PAL['steel']}"/>
  </linearGradient>
  <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{PAL['arrow']}"/>
  </marker>
  <marker id="arb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{PAL['accent2']}"/>
  </marker>
</defs>
{body}
</svg>
"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def wrap(s, n):
    words, out, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


def text(x, y, s, size=15, anchor="middle", color=None, weight="normal", italic=False):
    s = esc(s)
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color or PAL["ink"]}" font-weight="{weight}"{st}>{s}</text>'


def lines(x, y, rows, size=14, anchor="middle", color=None, lh=1.25):
    return "".join(text(x, y + i * size * lh, r, size, anchor, color) for i, r in enumerate(rows))


def step(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="12" fill="{PAL["ink"]}"/>' + text(x, y + 5, str(n), 14, color="#fff", weight="bold")


def arrow(x1, y1, x2, y2, color="arrow", w=2.5, dash=False):
    m = "ar" if color == "arrow" else "arb"
    c = PAL["arrow"] if color == "arrow" else PAL["accent2"]
    d = ' stroke-dasharray="5 4"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#{m})"{d}/>'


def curved_arrow(cx, cy, r, a0, a1, color="arrow"):
    m = "ar" if color == "arrow" else "arb"
    c = PAL["arrow"] if color == "arrow" else PAL["accent2"]
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" fill="none" stroke="{c}" stroke-width="2.5" marker-end="url(#{m})"/>'


def rect(x, y, w, h, fill, stroke=None, rx=0, sw=1.2):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}/>'


def poly(pts, fill, stroke=None, sw=1.2):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<polygon points="{p}" fill="{fill}"{s}/>'


def bar(x, y, w, h, kind="hot"):
    fill = {"hot": "url(#hot)", "hotR": "url(#hotR)", "even": "url(#hotEven)", "end": "url(#hotEnd)",
            "cold": PAL["steel"], "top": "url(#hotTop)"}[kind]
    return rect(x, y, w, h, fill, PAL["steel_dark"], 2)


def anvil(x, y, w=240, horn=True, hardy=True, scale=1.0, label=False):
    """Seitenansicht; (x,y) = linke obere Ecke der Bahn."""
    s = scale
    fh = 30 * s  # Bahndicke
    out = []
    if horn:
        out.append(f'<path d="M{x},{y+2} C{x-40*s},{y+2} {x-80*s},{y+6*s} {x-105*s},{y+14*s} C{x-80*s},{y+22*s} {x-40*s},{y+34*s} {x},{y+48*s} Z" fill="{PAL["anvil"]}"/>')
    out.append(rect(x, y, w, fh, PAL["anvil_face"]))
    out.append(rect(x, y, w, 4 * s, "#8a8e95"))  # Bahn
    waist_top = y + fh
    out.append(poly([(x + 20 * s, waist_top), (x + w - 25 * s, waist_top), (x + w - 55 * s, waist_top + 45 * s), (x + 55 * s, waist_top + 45 * s)], PAL["anvil"]))
    out.append(poly([(x + 55 * s, waist_top + 45 * s), (x + w - 55 * s, waist_top + 45 * s), (x + w - 15 * s, waist_top + 75 * s), (x + 15 * s, waist_top + 75 * s)], PAL["anvil"]))
    if hardy:
        out.append(rect(x + w - 34 * s, y + 6 * s, 12 * s, fh - 6 * s, "#26282b"))
        out.append(f'<circle cx="{x + w - 58 * s}" cy="{y + 16 * s}" r="{4.5 * s}" fill="#26282b"/>')
    return "".join(out)


def hammer(cx, cy, angle=0, peen=None, scale=1.0, handle=True):
    """Schmiedehammer, Bahn nach unten bei angle=0; (cx,cy) = Mitte der Bahn."""
    s = scale
    g = [f'<g transform="translate({cx},{cy}) rotate({angle}) scale({s})">']
    if handle:
        g.append(rect(-5, -62, 125, 10, PAL["wood"], "#6b4423", 3))
    g.append(rect(-20, -84, 40, 78, "#3a3c40", "#202225", 3))  # Kopf (stehend)
    g.append(rect(-22, -12, 44, 12, "#55585e", "#202225", 2))  # Bahn
    if peen == "cross":
        g.append(poly([(-20, -84), (20, -84), (4, -100), (-4, -100)], "#3a3c40"))
    g.append("</g>")
    return "".join(g)


def strike(x, y, n=3):
    """Schlagstriche"""
    o = []
    for i in range(n):
        a = -150 + i * 60 / max(n - 1, 1)
        o.append(f'<line x1="{x + 14*math.cos(math.radians(a)):.1f}" y1="{y + 14*math.sin(math.radians(a)):.1f}" x2="{x + 26*math.cos(math.radians(a)):.1f}" y2="{y + 26*math.sin(math.radians(a)):.1f}" stroke="{PAL["arrow"]}" stroke-width="2"/>')
    return "".join(o)


def panel_title(x, y, s):
    return text(x, y, s, 15, weight="bold")


def caption(x, y, rows, size=13):
    n = int(690 / (size * 0.52))
    wrapped = [w for r in rows for w in wrap(r, n)]
    return lines(x, y, wrapped, size, color=PAL["muted"])


def section(x, y, shape, size=34, fill="url(#hotEven)"):
    """Querschnitt-Symbol"""
    h = size / 2
    if shape == "square":
        return rect(x - h, y - h, size, size, fill, PAL["steel_dark"])
    if shape == "diamond":
        return poly([(x, y - h * 1.15), (x + h * 0.8, y), (x, y + h * 1.15), (x - h * 0.8, y)], fill, PAL["steel_dark"])
    if shape == "octagon":
        k = h * 0.414
        return poly([(x - k, y - h), (x + k, y - h), (x + h, y - k), (x + h, y + k), (x + k, y + h), (x - k, y + h), (x - h, y + k), (x - h, y - k)], fill, PAL["steel_dark"])
    if shape == "round":
        return f'<circle cx="{x}" cy="{y}" r="{h}" fill="{fill}" stroke="{PAL["steel_dark"]}"/>'
    if shape == "flat":
        return rect(x - h * 1.3, y - h * 0.35, size * 1.3, size * 0.35, fill, PAL["steel_dark"])
    if shape == "rhomb":
        return poly([(x - h * 1.1, y - h * 0.6), (x + h * 0.6, y - h * 0.9), (x + h * 1.1, y + h * 0.6), (x - h * 0.6, y + h * 0.9)], fill, PAL["steel_dark"])
    raise ValueError(shape)


# ------------------------------------------------------------------ diagrams
def d_anvil(L):
    t = dict(
        de=["Amboss – Bezeichnungen", "Horn", "Bahn (gehärtet)", "Vorschlag / Tisch", "Hardyloch", "Pritchelloch", "Kante (leicht gerundet)", "Fuß", "Stock (Holz) – Bahn auf Faust- bis Handgelenkhöhe"],
        en=["Anvil – parts", "Horn", "Face (hardened)", "Step / table", "Hardy hole", "Pritchel hole", "Edge (slightly radiused)", "Foot", "Stand (wood) – face at knuckle to wrist height"],
    )[L]
    x, y = 250, 120
    b = [anvil(x, y, 300, scale=1.25)]
    b.append(rect(x + 30, y + 37 + 94, 240, 70, PAL["wood"], "#6b4423", 2))
    b.append(rect(x - 20, y + 4, 26, 8, "#8a8e95"))  # Vorschlag-Andeutung
    b.append(text(360, 40, t[0], 18, weight="bold"))
    b.append(arrow(150, 75, 175, 125, "blue") + text(140, 68, t[1], 14))
    b.append(arrow(360, 70, 360, 115, "blue") + text(360, 62, t[2], 14))
    b.append(arrow(225, 95, 245, 118, "blue") + text(215, 90, t[3], 14))
    b.append(arrow(600, 82, 519, 118, "blue") + text(610, 76, t[4], 14))
    b.append(arrow(478, 70, 478, 132, "blue") + text(478, 62, t[5], 14))
    b.append(arrow(572, 168, 553, 134, "blue") + text(565, 185, t[6], 13, anchor="start"))
    b.append(arrow(630, 225, 590, 225, "blue") + text(640, 230, t[7], 13, anchor="start"))
    b.append(caption(360, 345, [t[8]]))
    return svg(720, 365, "".join(b), t[0])


def d_volume(L):
    t = dict(
        de=["Volumenkonstanz: Was dünner wird, wird länger", "20 × 20 × 100 mm", "10 × 10 × 400 mm", "V = 40 cm³", "V = 40 cm³",
            "Beim Freiformschmieden bleibt das Volumen (fast) gleich – Zunderverlust ca. 1–3 % je Hitze.", "Zuschnitt rechnen: Länge = Volumen ÷ Querschnitt (+ Zugabe)."],
        en=["Volume constancy: thinner means longer", "20 × 20 × 100 mm", "10 × 10 × 400 mm", "V = 40 cm³", "V = 40 cm³",
            "In open-die forging volume stays (almost) constant – scale loss approx. 1–3 % per heat.", "Stock length = volume ÷ cross-section (+ allowance)."],
    )[L]
    b = [text(360, 34, t[0], 18, weight="bold")]
    b.append(bar(60, 90, 100, 40, "even") + text(110, 80, t[1], 13) + text(110, 155, t[3], 13, color=PAL["muted"]))
    b.append(arrow(190, 110, 250, 110))
    b.append(bar(270, 100, 400, 20, "even") + text(470, 90, t[2], 13) + text(470, 145, t[4], 13, color=PAL["muted"]))
    b.append(caption(360, 195, [t[5], t[6]]))
    return svg(720, 240, "".join(b), t[0])


def d_drawing(L):
    t = dict(
        de=["Strecken", "Auf der Bahn / dem Horn", "Material fließt in Längsrichtung", "Querschnitt-Folge", "Quadrat", "90° drehen", "Achteck", "Rund",
            "Faustregel: Querschnitt nie flacher als ~1 : 1,5 schlagen, sonst kippt er zum Rhombus.", "Schmales Werkzeug (Horn, Finne, Kehleisen) streckt schneller als die breite Bahn.", "Rhombus → Kaltfalte"],
        en=["Drawing out", "On the face / the horn", "Material flows lengthwise", "Cross-section sequence", "Square", "turn 90°", "Octagon", "Round",
            "Rule of thumb: never forge the section flatter than ~1 : 1.5, or it collapses into a rhombus.", "Narrow tools (horn, cross-peen, fuller) draw faster than the broad face.", "Rhombus → cold shut"],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    # left: bar on horn
    b.append(anvil(150, 160, 180, scale=0.9))
    b.append(bar(55, 140, 230, 18, "hot"))
    b.append(hammer(95, 138, 0, scale=0.8))
    b.append(strike(95, 120))
    b.append(arrow(85, 180, 30, 180) + arrow(110, 180, 175, 180))
    b.append(text(110, 270, t[1], 14, weight="bold") + caption(110, 290, [t[2]]))
    # right: cross-sections
    b.append(text(540, 80, t[3], 15, weight="bold"))
    xs = [420, 500, 580, 660]
    shapes = ["square", "square", "octagon", "round"]
    labels = [t[4], t[5], t[6], t[7]]
    for i, (xx, sh, lb) in enumerate(zip(xs, shapes, labels)):
        if i == 1:
            b.append(f'<g transform="rotate(0 {xx} 130)">{section(xx, 130, "square", 28)}</g>')
            b.append(curved_arrow(xx, 130, 26, -120, -30, "blue"))
        else:
            b.append(section(xx, 130, sh, 34 if i == 0 else 30))
        b.append(text(xx, 178, lb, 13))
        if i < 3:
            b.append(arrow(xx + 22, 130, xx + 55, 130, w=1.8))
    b.append(section(480, 235, "rhomb", 34, PAL["steel"]) + text(560, 240, t[10], 13, anchor="start", color=PAL["arrow"]))
    b.append(f'<line x1="440" y1="205" x2="520" y2="265" stroke="{PAL["arrow"]}" stroke-width="3"/><line x1="520" y1="205" x2="440" y2="265" stroke="{PAL["arrow"]}" stroke-width="3"/>')
    b.append(caption(360, 320, [t[8], t[9]]))
    return svg(720, 370, "".join(b), t[0])


def d_spreading(L):
    t = dict(
        de=["Breiten (Aufsicht)", "Finne längs zur Stabachse", "→ Material fließt quer: Breiten", "Finne quer zur Stabachse", "→ Material fließt längs: Strecken",
            "Breiten mit der Bahn: Schläge vom Zentrum fächerförmig nach außen führen; Kanten zwischendurch hochkant nachschlagen, sonst reißen sie ein."],
        en=["Spreading (top view)", "Peen parallel to the bar axis", "→ material moves sideways: spreading", "Peen across the bar axis", "→ material moves lengthwise: drawing",
            "Spreading with the face: fan blows outward from the centre; dress the edges on edge from time to time, or they will crack."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    # left panel
    b.append(f'<path d="M40,105 L170,105 C215,105 245,70 300,65 L300,175 C245,170 215,135 170,135 L40,135 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    for i in range(5):
        xx = 205 + i * 18
        b.append(f'<line x1="{xx}" y1="{110 - i*6}" x2="{xx}" y2="{130 + i*6}" stroke="{PAL["hot4"]}" stroke-width="3" stroke-linecap="round"/>')
    b.append(arrow(250, 120, 250, 55) + arrow(250, 120, 250, 190))
    b.append(text(170, 225, t[1], 14, weight="bold") + caption(170, 245, [t[2]]))
    # right panel
    b.append(rect(410, 105, 230, 30, "url(#hot)", PAL["steel_dark"]))
    for i in range(5):
        xx = 520 + i * 18
        b.append(f'<line x1="{xx-8}" y1="120" x2="{xx+8}" y2="120" stroke="{PAL["hot4"]}" stroke-width="3" stroke-linecap="round" transform="rotate(90 {xx} 120) rotate(90 {xx} 120)"/>')
        b.append(f'<line x1="{xx}" y1="108" x2="{xx}" y2="132" stroke="{PAL["hot4"]}" stroke-width="3" stroke-linecap="round" transform="rotate(90 {xx} 120)"/>')
    b.append(arrow(600, 120, 690, 120))
    b.append(text(540, 225, t[3], 14, weight="bold") + caption(540, 245, [t[4]]))
    b.append(caption(360, 295, [t[5]]))
    return svg(720, 335, "".join(b), t[0])


def d_upsetting(L):
    t = dict(
        de=["Stauchen", "Nur die Zone erhitzen,", "die dicker werden soll", "Kurz stauchen – Stab", "senkrecht auf der Bahn", "Ausknicken sofort", "auf der Bahn richten",
            "Abschrecken der Nachbarzonen (Kühlen mit Wasser) begrenzt die Stauchzone. Lange Stäbe: liegend gegen Stauchklotz oder Ambossseite."],
        en=["Upsetting", "Heat only the zone", "that should get thicker", "Upset in short heats –", "bar upright on the face", "Straighten any bend", "immediately on the face",
            "Quenching the neighbouring zones (cooling with water) limits the upset. Long bars: horizontally against an upsetting block or the anvil side."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    # 1
    b.append(step(40, 60, 1))
    b.append(f'<g transform="rotate(-90 120 170)">{bar(60, 158, 160, 24, "end")}</g>')
    b.append(text(120, 335, t[1], 13) + text(120, 352, t[2], 13))
    # 2
    b.append(step(270, 60, 2))
    b.append(anvil(290, 250, 140, horn=False, hardy=False, scale=0.6))
    b.append(f'<path d="M346,250 L374,250 L374,158 C386,150 388,130 384,120 L336,120 C332,130 334,150 346,158 Z" fill="url(#hotTop)" stroke="{PAL["steel_dark"]}"/>')
    b.append(hammer(360, 116, 0, scale=0.7))
    b.append(arrow(400, 80, 400, 112))
    b.append(text(360, 335, t[3], 13) + text(360, 352, t[4], 13))
    # 3
    b.append(step(500, 60, 3))
    b.append(f'<path d="M585,250 Q620,185 585,110" fill="none" stroke="url(#hotEven)" stroke-width="22" stroke-linecap="butt"/>')
    b.append(f'<line x1="540" y1="180" x2="575" y2="180" stroke="{PAL["arrow"]}" stroke-width="3"/>' + text(530, 185, "!", 26, color=PAL["arrow"], weight="bold"))
    b.append(text(600, 335, t[5], 13) + text(600, 352, t[6], 13))
    b.append(caption(360, 390, [t[7]], 12.5))
    return svg(720, 425, "".join(b), t[0])


def d_taper(L):
    t = dict(
        de=["Spitzen", "Stab im Spitzenwinkel anheben,", "Hammer gleich geneigt führen", "Fünf Spitzenquerschnitte (nach M. Aspery)", "Vierkant", "Achtkant", "Rund", "Meißel", "Raute",
            "Spitze zuerst kurz und dick vorschmieden, dann ausziehen – nicht die äußerste Spitze überhitzen (verbrennt)."],
        en=["Tapering / pointing", "Raise the bar to the taper angle,", "tilt the hammer to match", "Five taper cross-sections (after M. Aspery)", "Square", "Octagon", "Round", "Chisel", "Diamond",
            "Forge the taper short and stout first, then draw it out – don't overheat the very tip (it burns)."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(anvil(90, 200, 220, scale=0.8, hardy=False, horn=False))
    b.append(f'<g transform="rotate(-9 260 200)"><path d="M40,180 L250,180 L300,193 L250,200 L40,200 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/></g>')
    b.append(hammer(255, 175, -9, scale=0.75))
    b.append(strike(265, 150))
    b.append(text(190, 300, t[1], 13) + text(190, 317, t[2], 13))
    b.append(text(560, 80, t[3], 14, weight="bold"))
    for i, (sh, lb) in enumerate(zip(["square", "octagon", "round", "flat", "diamond"], t[4:9])):
        xx = 440 + i * 60
        b.append(section(xx, 135, sh, 30))
        b.append(text(xx, 180, lb, 12.5))
    # side view of a taper
    b.append(f'<path d="M430,230 L620,230 L690,245 L620,260 L430,260 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(caption(360, 352, [t[9]], 12.5))
    return svg(720, 385, "".join(b), t[0])


def d_shoulder(L):
    t = dict(
        de=["Absetzen", "Halber Schlag: Hammerbahn zur Hälfte", "über die Ambosskante", "Einseitige Schulter", "Beidseitig: wenden und am gleichen Punkt", "erneut absetzen – oder Setzhammer / Kehleisen",
            "Die Schulter liegt dort, wo die Ambosskante den Stab trägt. Kante leicht gerundet → Hohlkehle statt Kerbe (Kerbwirkung!)."],
        en=["Shouldering / setting down", "Half-faced blow: half of the hammer face", "overhangs the anvil edge", "One-sided shoulder", "Two-sided: turn over and set down at the", "same spot – or use a set hammer / fuller",
            "The shoulder forms where the anvil edge supports the bar. A slightly radiused edge gives a fillet instead of a notch (notch effect!)."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(anvil(60, 170, 170, horn=False, scale=0.8, hardy=False))
    b.append(bar(110, 146, 230, 24, "hotR"))
    b.append(hammer(230, 146, 0, scale=0.8))
    b.append(f'<line x1="230" y1="60" x2="230" y2="250" stroke="{PAL["accent2"]}" stroke-dasharray="4 4"/>')
    b.append(text(180, 280, t[1], 13) + text(180, 297, t[2], 13))
    # result one-sided
    b.append(f'<path d="M420,120 L540,120 L548,132 L640,132 L640,144 L420,144 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(530, 105, t[3], 13, weight="bold"))
    # two-sided
    b.append(f'<path d="M420,200 L540,200 L548,208 L640,208 L640,216 L548,216 L540,224 L420,224 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(530, 255, t[4], 13) + text(530, 272, t[5], 13))
    b.append(caption(360, 328, [t[6]], 12.5))
    return svg(720, 365, "".join(b), t[0])


def d_fuller(L):
    t = dict(
        de=["Kehlen (Einkerben)", "Ober- und Untergesenk (Federkehleisen)", "Kehlen begrenzen und verdrängen Material", "Danach zwischen den Kehlen strecken / ausgleichen",
            "Kehleisen strecken bevorzugt quer zur Kehle. Kanten der Kehle stets rund – scharfe Kerben werden zu Rissen."],
        en=["Fullering", "Top and bottom fuller (spring fuller)", "Fullers isolate and displace material", "Then draw out / dress between the grooves",
            "Fullers move material mainly at right angles to the groove. Keep fuller edges round – sharp notches become cracks."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(rect(170, 165, 12, 60, "#3a3c40") + f'<circle cx="176" cy="160" r="12" fill="#55585e" stroke="#202225"/>')
    b.append(bar(60, 136, 230, 20, "even"))
    b.append(f'<circle cx="176" cy="132" r="12" fill="#55585e" stroke="#202225"/>' + rect(170, 80, 12, 44, "#3a3c40"))
    b.append(f'<path d="M176,80 C176,50 240,50 260,70 L260,230 C240,250 176,250 176,228" fill="none" stroke="#3a3c40" stroke-width="5"/>')
    b.append(rect(140, 60, 72, 18, "#55585e", "#202225") + arrow(176, 28 + 10, 176, 56))
    b.append(text(175, 275, t[1], 13))
    # result
    b.append(f'<path d="M400,120 L470,120 Q480,132 490,120 L560,120 Q570,132 580,120 L650,120 L650,150 L580,150 Q570,138 560,150 L490,150 Q480,138 470,150 L400,150 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(525, 105, t[2], 13))
    b.append(f'<path d="M400,200 L470,200 Q480,210 490,210 L560,210 Q570,210 580,200 L650,200 L650,230 L580,230 Q570,220 560,220 L490,220 Q480,220 470,230 L400,230 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(525, 260, t[3], 13))
    b.append(caption(360, 315, [t[4]], 12.5))
    return svg(720, 355, "".join(b), t[0])


def d_split(L):
    t = dict(
        de=["Spalten", "Schrotmeißel auf Schrotunterlage", "(nicht auf der Bahn!)", "Von beiden Seiten bis zur Mitte", "einschroten, Grund runden", "Schenkel aufbiegen,", "dann einzeln weiterformen",
            "Spaltgrund rund halten (gerundete Meißelschneide oder Bohrung Ø 3–5 mm) – ein spitzer Grund reißt beim Aufbiegen weiter."],
        en=["Splitting", "Hot chisel on a cutting plate", "(never on the anvil face!)", "Cut to the middle from both sides,", "keep the bottom of the split round", "Open the legs,", "then forge each one on its own",
            "Keep the root of the split round (rounded chisel edge or a 3–5 mm drilled hole) – a sharp root keeps tearing as you open it."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(step(40, 60, 1) + rect(40, 200, 200, 8, "#c9b38a", "#8a7650") + anvil(50, 208, 180, horn=False, hardy=False, scale=0.55))
    b.append(bar(50, 178, 180, 22, "hot"))
    b.append(poly([(180, 176), (190, 176), (194, 110), (176, 110)], "#55585e", "#202225") + rect(172, 92, 26, 20, "#3a3c40"))
    b.append(text(140, 285, t[1], 13) + text(140, 302, t[2], 13, color=PAL["muted"]))
    b.append(step(270, 60, 2))
    b.append(f'<path d="M280,160 L380,160 L380,175 C380,178 384,180 388,180 L470,180 L470,184 L388,184 C384,184 380,186 380,189 L380,204 L280,204 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(f'<circle cx="381" cy="182" r="3.5" fill="{PAL["paper"]}" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(375, 285, t[3], 13) + text(375, 302, t[4], 13))
    b.append(step(500, 60, 3))
    b.append(f'<path d="M520,170 L600,170 C620,170 640,140 680,110 L690,122 C655,150 640,175 625,182 C640,189 655,214 690,242 L680,254 C640,224 620,194 600,194 L520,194 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(605, 285, t[5], 13) + text(605, 302, t[6], 13))
    b.append(caption(360, 340, [t[7]], 12.5))
    return svg(720, 375, "".join(b), t[0])


def d_punch(L):
    t = dict(
        de=["Lochen, Schlitzen & Dornen", "Lochdorn ca. ¾ der Dicke", "eintreiben (Dorn kühlen!)", "Wenden: dunkler Fleck", "zeigt die Lochstelle", "Über Pritchel-/Hardyloch:", "Butzen austreiben",
            "Aufdornen: Dorn (Drift)", "weitet auf Endmaß", "Schlitzen statt Lochen: Schlitzmeißel teilt nur, entfernt kein Material → Stab „bläht“ sich zum Auge (stärker als gelocht).",
            "Butzen"],
        en=["Punching, slitting & drifting", "Drive the punch about ¾", "through (cool the punch!)", "Flip over: a dark spot", "marks the hole position", "Over pritchel/hardy hole:", "drive the slug out",
            "Drifting: the drift", "opens the hole to size", "Slitting instead of punching: the slitter only parts, removes no material → the bar swells into an eye (stronger than punched).",
            "slug"],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    W = 170
    for i in range(4):
        x0 = 20 + i * W
        b.append(step(x0 + 15, 60, i + 1))
        b.append(rect(x0 + 15, 200, 140, 40, PAL["anvil_face"]))
        if i == 2:
            b.append(rect(x0 + 75, 200, 20, 40, "#26282b"))
        if i < 3:
            b.append(rect(x0 + 25, 170, 120, 30, "url(#hotEven)", PAL["steel_dark"]))
        if i == 0:
            b.append(poly([(x0 + 78, 192), (x0 + 92, 192), (x0 + 96, 120), (x0 + 74, 120)], "#55585e", "#202225"))
            b.append(rect(x0 + 72, 100, 26, 20, "#3a3c40"))
        if i == 1:
            b.append(rect(x0 + 78, 170, 14, 7, "#5a2410"))
            b.append(curved_arrow(x0 + 85, 140, 28, 200, 340, "blue"))
        if i == 2:
            b.append(poly([(x0 + 78, 168), (x0 + 92, 168), (x0 + 96, 110), (x0 + 74, 110)], "#55585e", "#202225"))
            b.append(rect(x0 + 78, 205, 14, 10, PAL["hot3"], PAL["steel_dark"]) + text(x0 + 120, 225, t[10], 11, color="#fff"))
            b.append(arrow(x0 + 85, 218, x0 + 85, 250))
        if i == 3:
            b.append(f'<path d="M{x0+25},170 L{x0+60},170 C{x0+68},160 {x0+102},160 {x0+110},170 L{x0+145},170 L{x0+145},200 L{x0+110},200 C{x0+102},210 {x0+68},210 {x0+60},200 L{x0+25},200 Z" fill="url(#hotEven)" stroke="{PAL["steel_dark"]}"/>')
            b.append(poly([(x0 + 78, 200), (x0 + 92, 200), (x0 + 100, 120), (x0 + 70, 120)], "#55585e", "#202225"))
            b.append(f'<line x1="{x0+66}" y1="140" x2="{x0+104}" y2="140" stroke="#202225"/>')
        tt = [(t[1], t[2]), (t[3], t[4]), (t[5], t[6]), (t[7], t[8])][i]
        b.append(text(x0 + 85, 275, tt[0], 12.5) + text(x0 + 85, 291, tt[1], 12.5))
    b.append(caption(360, 330, [t[9]], 12.5))
    return svg(720, 370, "".join(b), t[0])


def d_cut(L):
    t = dict(
        de=["Abschroten (Trennen)", "Abschrot im Hardyloch", "Rundum einkerben, Steg ~⅓ stehen lassen", "Über der Kante abbrechen –", "nie bis auf die Abschrot-Schneide durchschlagen",
            "Schrotmeißel (Warmschrot) immer auf Schrotunterlage oder Weichplatte; Kaltschrot nur für ungehärtete, kalte Werkstoffe."],
        en=["Hot cutting", "Hardy in the hardy hole", "Nick all round, leave a ~⅓ web", "Snap it off over the edge –", "never strike through onto the hardy edge",
            "Use a hot chisel only on a cutting plate or soft plate; a cold chisel is only for unhardened, cold stock."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(anvil(120, 190, 220, horn=False, scale=0.8))
    b.append(poly([(282, 190), (300, 190), (296, 165), (286, 165)], "#55585e", "#202225"))
    b.append(bar(150, 140, 220, 24, "hot"))
    b.append(poly([(283, 164), (299, 164), (291, 156)], PAL["paper"]))
    b.append(hammer(291, 138, 0, scale=0.75))
    b.append(text(220, 290, t[1], 13, weight="bold") + text(220, 307, t[2], 13))
    b.append(f'<path d="M440,140 L560,140 L566,148 L560,156 L440,156 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(f'<path d="M574,140 L660,140 L660,156 L574,156 L568,148 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}" transform="rotate(12 574 148)"/>')
    b.append(text(560, 200, t[3], 13) + text(560, 217, t[4], 13))
    b.append(caption(360, 345, [t[5]], 12.5))
    return svg(720, 385, "".join(b), t[0])


def d_bend(L):
    t = dict(
        de=["Biegen", "Über die Ambosskante: rechter Winkel", "Über das Horn: Bögen, Ösen, Ringe", "Schnecke (Volute) beginnen:", "Ende über der Kante anbiegen, dann einrollen",
            "Biegezone gezielt erhitzen – nur dort biegt es. Scharfe Innenecke? Vorher stauchen (siehe Stauchen).", "Biegelänge Ring: L ≈ π · (Innen-Ø + Materialdicke)"],
        en=["Bending", "Over the anvil edge: right angle", "Over the horn: curves, eyes, rings", "Starting a scroll:", "turn the tip over the edge, then roll it in",
            "Heat only the bending zone – that is where it bends. Sharp inside corner? Upset first (see upsetting).", "Stock length for a ring: L ≈ π · (inside Ø + thickness)"],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(anvil(30, 160, 150, horn=False, hardy=False, scale=0.65))
    b.append(f'<path d="M40,140 L168,140 Q180,140 180,152 L180,240 L160,240 L160,160 L40,160 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(curved_arrow(170, 150, 45, -80, 10))
    b.append(text(120, 280, t[1], 13))
    b.append(anvil(380, 170, 120, hardy=False, scale=0.75))
    b.append(f'<path d="M290,150 C330,120 380,140 395,160 C410,180 395,215 360,220" fill="none" stroke="url(#hotEven)" stroke-width="16"/>')
    b.append(text(360, 280, t[2], 13))
    b.append(f'<path d="M640,180 C640,150 600,140 585,160 C572,178 590,198 608,190 C620,184 616,170 606,172" fill="none" stroke="url(#hot)" stroke-width="10"/>' +
             f'<line x1="640" y1="180" x2="640" y2="245" stroke="{PAL["hot3"]}" stroke-width="10"/>')
    b.append(text(590, 280, t[3], 13) + lines(590, 297, wrap(t[4], 30), 12, color=PAL["muted"]))
    b.append(caption(360, 345, [t[5], t[6]], 12.5))
    return svg(720, 390, "".join(b), t[0])


def d_twist(L):
    t = dict(
        de=["Tordieren (Verdrehen)", "Schraubstock", "Wendeisen", "Gleichmäßige Hitze = gleichmäßige Steigung", "Zonen begrenzen: Enden mit Wasser kühlen",
            "Vierkant zeigt die Drehung am besten; Anzahl der Umdrehungen mitzählen (Kreidestrich). Nach dem Drehen auf Holz geraderichten – nicht auf Stahl (Kanten bleiben scharf)."],
        en=["Twisting", "Vise", "Twisting wrench", "Even heat = even pitch", "Limit the zone: cool the ends with water",
            "Square stock shows the twist best; count the turns (chalk mark). Straighten on wood after twisting – not on steel (keeps the edges crisp)."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    b.append(rect(60, 110, 40, 90, "#3a3c40") + rect(100, 110, 40, 90, "#4a4c50") + text(100, 225, t[1], 13))
    b.append(rect(140, 140, 440, 26, PAL["steel"], PAL["steel_dark"]))
    for i in range(12):
        xx = 200 + i * 28
        b.append(f'<path d="M{xx},140 L{xx+18},166" stroke="{PAL["hot4"]}" stroke-width="5"/>')
    b.append(rect(190, 140, 340, 26, "url(#hotEven)", PAL["steel_dark"]) .replace('fill="url(#hotEven)"', 'fill="url(#hotEven)" fill-opacity="0.55"'))
    for i in range(12):
        xx = 196 + i * 28
        b.append(f'<path d="M{xx},140 L{xx+18},166" stroke="{PAL["hot4"]}" stroke-width="4" opacity="0.8"/>')
    b.append(rect(580, 60, 18, 190, "#3a3c40", "#202225", 3) + rect(570, 138, 38, 30, "#55585e", "#202225", 3))
    b.append(curved_arrow(589, 153, 75, -60, 60))
    b.append(text(640, 270, t[2], 13))
    b.append(text(360, 270, t[3], 13) + text(360, 287, t[4], 13, color=PAL["muted"]))
    b.append(caption(360, 325, [t[5]], 12.5))
    return svg(720, 365, "".join(b), t[0])


def d_weld(L):
    t = dict(
        de=["Feuerschweißen – Überlappschweißung", "Enden stauchen", "(Materialzugabe)", "Schäften: Schweißfase,", "leicht ballig", "Bei Schweißhitze auflegen,", "erster Schlag mittig", "Zum Ausgangs-", "querschnitt schmieden",
            "Schweißhitze ≈ 1250–1350 °C (weißgelb, beginnende Funken); Flussmittel (Borax) ab Rotglut. Ballige Fase drückt Zunder und Flussmittel von innen nach außen."],
        en=["Forge welding – lap (scarf) weld", "Upset the ends", "(extra material)", "Scarf: welding bevel,", "slightly convex", "At welding heat lay on,", "first blow in the middle", "Forge back to", "the original section",
            "Welding heat ≈ 1250–1350 °C (white-yellow, first sparks); flux (borax) from red heat. A convex scarf squeezes scale and flux from the inside out."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    W = 175
    for i in range(4):
        x0 = 15 + i * W
        b.append(step(x0 + 15, 60, i + 1))
    # 1 upset
    b.append(f'<path d="M30,140 L120,140 C130,140 135,134 150,134 L150,166 C135,166 130,160 120,160 L30,160 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(100, 230, t[1], 12.5) + text(100, 246, t[2], 12.5))
    # 2 scarf
    b.append(f'<path d="M205,140 L290,140 C300,138 315,136 330,134 Q320,150 290,166 L205,166 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(text(275, 230, t[3], 12.5) + text(275, 246, t[4], 12.5))
    # 3 lay on
    b.append(f'<path d="M370,150 L440,150 Q470,150 490,138 Q470,162 440,166 L370,166 Z" fill="url(#hot)" stroke="{PAL["steel_dark"]}"/>')
    b.append(f'<path d="M520,134 L460,134 Q430,138 418,150 Q440,148 460,150 L520,150 Z" fill="url(#hotR)" stroke="{PAL["steel_dark"]}"/>')
    b.append(hammer(455, 132, 0, scale=0.6) + strike(455, 112))
    b.append(text(450, 230, t[5], 12.5) + text(450, 246, t[6], 12.5))
    # 4 finished
    b.append(rect(560, 140, 140, 20, "url(#hotEven)", PAL["steel_dark"]))
    b.append(f'<line x1="625" y1="140" x2="635" y2="160" stroke="{PAL["hot4"]}" stroke-dasharray="2 3"/>')
    b.append(text(630, 230, t[7], 12.5) + text(630, 246, t[8], 12.5))
    b.append(caption(360, 290, [t[9]], 12.5))
    return svg(720, 330, "".join(b), t[0])


HEAT = [  # Glühfarben (Richtwerte, Tageslicht abgedunkelt)
    (550, "#3d0f08", "dunkelbraun", "dark brown"),
    (630, "#5a1408", "braunrot", "brown-red"),
    (680, "#7a1a0a", "dunkelrot", "dark red"),
    (740, "#a4200c", "dunkelkirschrot", "dark cherry"),
    (780, "#c42a10", "kirschrot", "cherry red"),
    (850, "#e03c12", "hellkirschrot", "light cherry"),
    (900, "#f05a18", "hellrot", "bright red"),
    (950, "#f77c22", "gelbrot", "orange"),
    (1000, "#fb9b30", "dunkelgelb", "dark yellow"),
    (1100, "#ffc04a", "gelb", "yellow"),
    (1200, "#ffe07a", "hellgelb", "light yellow"),
    (1300, "#fff7d0", "weiß", "white"),
]
TEMPER = [
    (200, "#f2e3b3", "weißgelb", "pale yellow"),
    (220, "#e9cf7e", "strohgelb", "straw"),
    (230, "#dcb653", "goldgelb", "gold"),
    (240, "#c9973b", "gelbbraun", "yellow-brown"),
    (250, "#a8702c", "braunrot", "brown"),
    (260, "#8a4d3a", "purpur", "purple"),
    (280, "#5b3a78", "violett", "violet"),
    (290, "#2f3f8a", "dunkelblau", "dark blue"),
    (320, "#5a87b8", "hellblau", "light blue"),
    (350, "#8a97a3", "grau", "grey"),
]


def d_colours(L):
    de = L == "de"
    title = "Glühfarben & Anlassfarben (Richtwerte für unlegierten Stahl)" if de else "Heat colours & temper colours (guide values, plain carbon steel)"
    b = [text(360, 30, title, 17, weight="bold")]
    b.append(text(20, 62, "Glühfarben – Schmiedetemperaturen" if de else "Heat colours – forging temperatures", 14, anchor="start", weight="bold"))
    w = 650 / len(HEAT)
    for i, (temp, col, n_de, n_en) in enumerate(HEAT):
        x = 50 + i * w
        b.append(rect(x, 72, w, 46, col))
        b.append(text(x + w / 2, 135, f"{temp}", 12))
        b.append(f'<text x="{x + w/2}" y="150" font-size="10.5" text-anchor="end" fill="{PAL["muted"]}" transform="rotate(-35 {x + w/2} 150)">{n_de if de else n_en}</text>')
    # ranges
    def rng(t0, t1, y, label, color):
        def xpos(T):
            for i in range(len(HEAT) - 1):
                if HEAT[i][0] <= T <= HEAT[i + 1][0]:
                    f = (T - HEAT[i][0]) / (HEAT[i + 1][0] - HEAT[i][0])
                    return 50 + (i + 0.5 + f) * w
            return 50 + (len(HEAT) - 0.5) * w if T > HEAT[-1][0] else 50 + 0.5 * w
        x0, x1 = xpos(t0), xpos(t1)
        return rect(x0, y, x1 - x0, 8, color, rx=4) + text((x0 + x1) / 2, y + 22, label, 12, color=color, weight="bold")
    b.append(rng(800, 1150, 205, "Schmiedebereich Baustahl (S235)" if de else "Forging range mild steel (S235)", PAL["accent2"]))
    b.append(rng(800, 1050, 240, "Werkzeugstahl (z. B. C45, C60, 1.2842 – Datenblatt!)" if de else "Tool steel (e.g. C45, 1045, O1 – check data sheet!)", PAL["arrow"]))
    b.append(rng(1250, 1300, 205, "Schweißhitze" if de else "Welding heat", PAL["hot4"]))
    b.append(text(20, 300, "Anlassfarben – Oxidfarben auf blanker Fläche (°C)" if de else "Temper colours – oxide colours on bright steel (°C)", 14, anchor="start", weight="bold"))
    w2 = 680 / len(TEMPER)
    for i, (temp, col, n_de, n_en) in enumerate(TEMPER):
        x = 20 + i * w2
        b.append(rect(x, 310, w2, 40, col))
        b.append(text(x + w2 / 2, 367, f"{temp}", 12))
        b.append(text(x + w2 / 2, 382, n_de if de else n_en, 10.5, color=PAL["muted"]))
    b.append(caption(360, 415, [
        "Unter ~750 °C (dunkelrot) nicht mehr kräftig schmieden; 200–350 °C: Blausprödigkeit – hier nie schlagen." if de else
        "Stop heavy forging below ~750 °C (dark red); 200–350 °C: blue brittleness – never strike in this range.",
        "Farben in abgedunkelter Werkstatt beurteilen; Tageslicht täuscht um 100 °C und mehr." if de else
        "Judge colours in a dim shop; daylight can fool you by 100 °C or more."], 12.5))
    return svg(720, 440, "".join(b), title)


def d_blows(L):
    t = dict(
        de=["Hammerführung – Grundschläge", "Voller Schlag", "flach, Bahn parallel", "Geneigter Schlag", "Material schieben", "Halber Schlag", "über die Kante → Absatz", "Finnenschlag", "gerichteter Materialfluss",
            "Locker greifen, aus Schulter + Ellbogen + Handgelenk schlagen, Hammer zurückfedern lassen. Treffen vor Kraft."],
        en=["Hammer control – basic blows", "Flat blow", "face parallel", "Angled blow", "pushes material", "Half-faced blow", "over the edge → step", "Peen blow", "directional flow",
            "Loose grip, strike from shoulder + elbow + wrist, let the hammer rebound. Accuracy before force."],
    )[L]
    b = [text(360, 30, t[0], 20, weight="bold")]
    for i in range(4):
        x0 = 20 + i * 172
        b.append(rect(x0 + 10, 190, 150, 30, PAL["anvil_face"]))
        b.append(rect(x0 + 10, 190, 150, 4, "#8a8e95"))
        if i == 2:
            b.append(rect(x0 + 10, 190, 90, 30, PAL["anvil_face"]) + rect(x0 + 100, 190, 60, 30, PAL["paper"]))
        b.append(bar(x0 + 20, 170, 135, 20, "even"))
        ang = [0, -15, 0, 0][i]
        cx = [x0 + 85, x0 + 80, x0 + 100, x0 + 85][i]
        b.append(hammer(cx, 168, ang, peen="cross" if i == 3 else None, scale=0.7, handle=True) if i != 3 else
                 f'<g transform="translate({x0+85},168) scale(0.7)">' + rect(-5, -110, 125, 10, PAL["wood"], "#6b4423", 3) +
                 poly([(-20, -10), (20, -10), (4, 6), (-4, 6)], "#55585e", "#202225") + rect(-20, -88, 40, 78, "#3a3c40", "#202225", 3) + "</g>")
        b.append(text(x0 + 85, 255, t[1 + 2 * i], 14, weight="bold") + text(x0 + 85, 272, t[2 + 2 * i], 12.5, color=PAL["muted"]))
    b.append(caption(360, 315, [t[9]], 12.5))
    return svg(720, 355, "".join(b), t[0])


DIAGRAMS = {
    "amboss": d_anvil,
    "volumen": d_volume,
    "strecken": d_drawing,
    "breiten": d_spreading,
    "stauchen": d_upsetting,
    "spitzen": d_taper,
    "absetzen": d_shoulder,
    "kehlen": d_fuller,
    "spalten": d_split,
    "lochen": d_punch,
    "abschroten": d_cut,
    "biegen": d_bend,
    "tordieren": d_twist,
    "feuerschweissen": d_weld,
    "gluehfarben": d_colours,
    "schlaege": d_blows,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        for L in ("de", "en"):
            (OUT / f"{name}-{L}.svg").write_text(fn(L), encoding="utf-8")
    print(f"{len(DIAGRAMS) * 2} SVGs → {OUT}")


if __name__ == "__main__":
    main()
