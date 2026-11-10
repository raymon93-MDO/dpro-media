"""Plantilla minimalista (clara, mucho aire, tipografía fina) 1080x1350 para DPRO."""
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facade2
from models import MODELS, room_area
from plan import Plan, fmt

facade2.MODE = "light"
FACADES = facade2.FACADES

BG = "#F5F3EF"
INK = "#1C232A"
MUTED = "#7A838C"
RULE = "#D8D3CA"
ORANGE = "#F07A1D"
W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = base64.b64encode(open(os.path.join(HERE, "assets", "DPRO_Logo2.png"), "rb").read()).decode()
DEFS = ('<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker></defs>')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, t, size, weight=400, fill=INK, anchor="start", ls=0, family="Inter"):
    extra = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{esc(t)}</text>')


def wrap(t, size, maxw):
    cw, out, cur = size * 0.5, [], ""
    for w in t.split():
        nxt = (cur + " " + w).strip()
        if len(nxt) * cw > maxw and cur:
            out.append(cur)
            cur = w
        else:
            cur = nxt
    return out + ([cur] if cur else [])


def logo(x, y, w):
    return f'<image x="{x}" y="{y}" width="{w}" height="{w*357/456:.0f}" href="data:image/png;base64,{LOGO}"/>'


def doc(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}<rect width="{W}" height="{H}" fill="{BG}"/>{body}</svg>'


def header(n, kicker):
    return "\n".join([logo(72, 64, 64), T(W - 72, 104, f"{kicker}  ·  0{n}/03", 18, 500, MUTED, "end", ls=3)])


def footer(sub):
    return "\n".join([f'<line x1="72" y1="1232" x2="{W-72}" y2="1232" stroke="{RULE}" stroke-width="1"/>',
                      T(72, 1282, "Escribí PLANO por WhatsApp", 26, 500, INK),
                      T(72, 1312, sub, 19, 400, MUTED),
                      T(W - 72, 1290, "→", 34, 300, ORANGE, "end")])


def stats_row(items, y, size=54):
    o = []
    cw = (W - 144) / len(items)
    for i, (v, lab) in enumerate(items):
        x = 72 + i * cw
        o.append(T(x, y, v, size, 300, INK))
        o.append(T(x, y + 34, lab.upper(), 15, 600, MUTED, ls=2))
    return "\n".join(o)


def cover(m, n):
    import iso
    if m["key"] in iso.ISO:
        art = f'<g transform="translate(0,150)">{iso.ISO[m["key"]]().svg(W, 760, pad=60)}</g>'
    else:
        art = f'<g transform="translate(0,170)">{FACADES[m["key"]](W, 700)}</g>'
    o = [header(n, "NUEVO MODELO"),
         art,
         T(72, 930, m["nombre"].split()[0].upper(), 18, 600, ORANGE, ls=5)]
    name = " ".join(m["nombre"].split()[1:])
    o.append(T(66, 1046, name, 96, 300, INK))
    o.append(T(72, 1092, m["bajada"], 24, 400, MUTED))
    o.append(stats_row(m["stats"], 1176, 44))
    o.append(footer("y te pasamos el costo estimado para tu terreno"))
    return doc("\n".join(o))


def plan_slide(m, n):
    o = [header(n, "PLANTA"), T(66, 220, m["nombre"], 56, 300, INK)]
    floors = m["floors"]
    top, bottom = 250, 1050
    if len(floors) == 1:
        o.append(Plan(floors[0], W - 100, bottom - top, 50, top).render())
    else:
        bw = (W - 100) / 2
        for i, f in enumerate(floors):
            o.append(T(50 + bw * i + bw / 2, top + 24, f["titulo"].upper(), 16, 600, MUTED, "middle", ls=3))
            o.append(Plan(f, bw, bottom - top - 30, 50 + bw * i, top + 30, font=0.85).render())
    cub = sum(room_area(f, r) for f in floors for r in f["rooms"])
    items = [(fmt(cub), "m² cubiertos" + (" / unidad" if len(floors) > 1 else ""))] + \
            [(fmt(s[3] * s[4]), f"m² {s[0].lower()}") for f in floors for s in f.get("semi", [])]
    o.append(stats_row(items, 1148, 40))
    o.append(footer("Medidas en metros · anteproyecto ilustrativo"))
    return doc("\n".join(o))


def spec_slide(m, n):
    o = [header(n, "FICHA TÉCNICA"), T(66, 220, m["nombre"], 56, 300, INK)]
    multi = len(m["floors"]) > 1
    rows = []
    for f in m["floors"]:
        for r in f["rooms"]:
            rows.append((r[0] + ((" · PB" if f["titulo"] == "Planta baja" else " · PA") if multi else ""), room_area(f, r)))
    cub = sum(a for _, a in rows)
    x0, cw, y = 72, 440, 290
    rh = 42 if len(rows) <= 9 else 38
    for nm, a in rows:
        o.append(T(x0, y + rh * 0.62, nm, 22, 400, INK))
        o.append(T(x0 + cw, y + rh * 0.62, fmt(a), 22, 400, INK, "end"))
        y += rh
        o.append(f'<line x1="{x0}" y1="{y}" x2="{x0+cw}" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
    y += 22
    o.append(T(x0, y + 28, "TOTAL CUBIERTO" + (" / UNIDAD" if multi else ""), 15, 600, MUTED, ls=2))
    o.append(T(x0 + cw, y + 40, fmt(cub) + " m²", 44, 300, ORANGE, "end"))
    y += 80
    for nm, a in m["ficha_extra"]:
        o.append(T(x0, y + 22, nm, 19, 400, MUTED))
        o.append(T(x0 + cw, y + 22, fmt(a), 19, 400, MUTED, "end"))
        y += 34
    rx, rw, ry = 600, 408, 290
    for title, body in [("LOTE MÍNIMO", [m["lote"]]), ("IDEAL PARA", wrap(m["perfil"], 22, rw))]:
        o.append(T(rx, ry + 14, title, 15, 600, MUTED, ls=2))
        ry += 26
        for ln in body:
            o.append(T(rx, ry + 26, ln, 24 if title == "LOTE MÍNIMO" else 22, 400, INK))
            ry += 32
        ry += 34
    o.append(T(rx, ry + 14, "TERMINACIONES", 15, 600, MUTED, ls=2))
    ry += 30
    for s in m["sistema"]:
        for j, ln in enumerate(wrap(s, 21, rw)):
            o.append(T(rx, ry + 22, ln, 21, 400, INK))
            ry += 29
        ry += 12
    ry += 22
    o.append(T(rx, ry + 14, "POR ETAPAS", 15, 600, ORANGE, ls=2))
    ry += 26
    for ln in wrap(m["etapas"], 21, rw):
        o.append(T(rx, ry + 22, ln, 21, 400, MUTED))
        ry += 29
    o.append(footer("y te armamos el cómputo y presupuesto por rubro"))
    return doc("\n".join(o))


def build(outdir, keys=None):
    os.makedirs(outdir, exist_ok=True)
    files = []
    for m in MODELS:
        if keys and m["key"] not in keys:
            continue
        for i, fn in enumerate((cover, plan_slide, spec_slide), start=1):
            base = os.path.join(outdir, f"{m['key']}_{i}")
            open(base + ".svg", "w").write(fn(m, i))
            subprocess.run(["rsvg-convert", base + ".svg", "-o", base + ".png"], check=True)
            files.append(base + ".png")
    return files


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out3"
    print("\n".join(build(out, sys.argv[2:] or None)))
