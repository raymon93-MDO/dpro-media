"""Carrusel con render fotorrealista (Gemini) + planta + vista 3D + ficha. 1080x1350."""
import base64
import io
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402

import slides3 as s3  # noqa: E402
import iso  # noqa: E402
from models import MODELS  # noqa: E402

W, H = s3.W, s3.H
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_W = base64.b64encode(open(os.path.join(HERE, "assets", "logo_white.png"), "rb").read()).decode()


def b64_cover(path, w=W, h=H, focus=0.55):
    im = Image.open(path).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x0, y0 = (im.width - w) // 2, int((im.height - h) * focus)
    im = im.crop((x0, y0, x0 + w, y0 + h))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


def render_cover(m, render_path, total):
    T = s3.T
    IH = 990
    img = b64_cover(render_path, W, IH, focus=0.62)
    o = [f'<rect width="{W}" height="{H}" fill="#14181C"/>',
         f'<image x="0" y="0" width="{W}" height="{IH}" href="data:image/jpeg;base64,{img}"/>',
         '<defs><linearGradient id="sh" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#14181C" stop-opacity="1"/></linearGradient>'
         '<linearGradient id="tp" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#000" stop-opacity="0.35"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="220" fill="url(#tp)"/>',
         f'<rect x="0" y="{IH-170}" width="{W}" height="171" fill="url(#sh)"/>',
         f'<image x="68" y="56" width="74" height="{74*357/456:.0f}" href="data:image/png;base64,{LOGO_W}"/>',
         T(W - 72, 104, f"NUEVO MODELO  ·  01/0{total}", 18, 600, "#FFFFFF", "end", ls=3),
         T(72, 1018, m["nombre"].split()[0].upper(), 20, 700, s3.ORANGE, ls=5),
         T(66, 1116, " ".join(m["nombre"].split()[1:]), 96, 300, "#FFFFFF"),
         T(72, 1156, m["bajada"], 26, 400, "#E8E4DE")]
    cw = (W - 144) / len(m["stats"])
    for i, (v, lab) in enumerate(m["stats"]):
        x = 72 + i * cw
        o.append(T(x, 1226, v, 40, 300, "#FFFFFF"))
        o.append(T(x, 1254, lab.upper(), 13, 600, "#AEB8C2", ls=2))
    o.append(f'<line x1="72" y1="1280" x2="{W-72}" y2="1280" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1"/>')
    o.append(T(72, 1320, "Render ilustrativo · Diseño original DPRO", 17, 400, "#D8D3CA"))
    o.append(T(W - 72, 1320, "Deslizá →", 20, 600, s3.ORANGE, "end"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(o)}</svg>'


def iso_slide(m, n, total):
    T = s3.T
    o = [s3.logo(72, 64, 64), T(W - 72, 104, f"VISTA 3D  ·  0{n}/0{total}", 18, 500, s3.MUTED, "end", ls=3),
         T(66, 220, m["nombre"], 56, 300, s3.INK),
         T(72, 262, "Volumetría y materiales", 22, 400, s3.MUTED),
         f'<g transform="translate(0,280)">{iso.ISO[m["key"]]().svg(W, 900, pad=50)}</g>',
         s3.footer("y te pasamos el costo estimado para tu terreno")]
    return s3.doc("\n".join(o))


def retitle(svg, n, total):
    return svg.replace(f"0{n}/03", f"0{n}/0{total}")


def build(key, render_path, outdir):
    m = next(x for x in MODELS if x["key"] == key)
    has_iso = key in iso.ISO
    total = 4 if has_iso else 3
    slides = [render_cover(m, render_path, total), retitle(s3.plan_slide(m, 2), 2, total)]
    if has_iso:
        slides.append(iso_slide(m, 3, total))
    slides.append(retitle(s3.spec_slide(m, total), total, total).replace(f"0{total}/03", f"0{total}/0{total}"))
    os.makedirs(outdir, exist_ok=True)
    files = []
    for i, svg in enumerate(slides, start=1):
        base = os.path.join(outdir, f"{key}_{i}")
        open(base + ".svg", "w").write(svg)
        subprocess.run(["rsvg-convert", base + ".svg", "-o", base + ".png"], check=True)
        Image.open(base + ".png").convert("RGB").save(base + ".jpg", "JPEG", quality=92, optimize=True)
        os.remove(base + ".svg")
        os.remove(base + ".png")
        files.append(base + ".jpg")
    return files


if __name__ == "__main__":
    # uso: python3 slides4.py <modelo> <render.jpg> <carpeta_salida>
    print("\n".join(build(sys.argv[1], sys.argv[2], sys.argv[3])))
