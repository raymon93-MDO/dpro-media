"""Láminas informativas (novedades / educativas) con la plantilla minimalista de slides3. 1080x1350."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slides3 import BG, INK, MUTED, RULE, ORANGE, W, H, T, wrap, logo, doc, footer  # noqa: E402


def header(n, total, kicker):
    return "\n".join([logo(72, 64, 64), T(W - 72, 104, f"{kicker}  ·  0{n}/0{total}", 18, 500, MUTED, "end", ls=3)])


def para(x, y, text, size, maxw, fill=INK, weight=400, lh=1.4):
    o = []
    for ln in wrap(text, size, maxw):
        o.append(T(x, y, ln, size, weight, fill))
        y += size * lh
    return "\n".join(o), y


def source(text):
    return T(72, 1196, text, 17, 400, MUTED)


def icon_house_rain(cx, cy, s=1.0):
    """Ícono lineal original: casa con lluvia y viento."""
    k = lambda v: v * s  # noqa: E731
    o = [f'<g transform="translate({cx},{cy})" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    # nube
    o.append(f'<path d="M{k(-150)},{k(-170)} a{k(50)},{k(50)} 0 0 1 {k(60)},{k(-60)} a{k(70)},{k(70)} 0 0 1 {k(130)},{k(-10)} '
             f'a{k(48)},{k(48)} 0 0 1 {k(20)},{k(70)} z" stroke="{INK}" stroke-width="3"/>')
    for i in range(6):
        x = k(-130 + i * 40)
        o.append(f'<line x1="{x}" y1="{k(-140)}" x2="{x - k(18)}" y2="{k(-95)}" stroke="{ORANGE}" stroke-width="3"/>')
    # viento
    for j, (y, l) in enumerate([(-40, 90), (-5, 130), (30, 70)]):
        o.append(f'<path d="M{k(-330)},{k(y)} h{k(l)} a{k(14)},{k(14)} 0 1 0 {k(-14)},{k(-14)}" stroke="{MUTED}" stroke-width="2.5"/>')
    # casa
    o.append(f'<path d="M{k(-170)},{k(10)} L{k(0)},{k(-70)} L{k(170)},{k(10)}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<rect x="{k(-130)}" y="{k(0)}" width="{k(260)}" height="{k(170)}" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<rect x="{k(-30)}" y="{k(80)}" width="{k(60)}" height="{k(90)}" stroke="{INK}" stroke-width="2.5"/>')
    o.append(f'<rect x="{k(-105)}" y="{k(40)}" width="{k(55)}" height="{k(45)}" stroke="{INK}" stroke-width="2.5"/>')
    o.append(f'<rect x="{k(50)}" y="{k(40)}" width="{k(55)}" height="{k(45)}" stroke="{INK}" stroke-width="2.5"/>')
    # canaleta y bajada
    o.append(f'<path d="M{k(130)},{k(4)} h{k(26)} v{k(166)} h{k(30)}" stroke="{ORANGE}" stroke-width="4"/>')
    # terreno con pendiente
    o.append(f'<path d="M{k(-260)},{k(172)} L{k(300)},{k(190)}" stroke="{MUTED}" stroke-width="2"/>')
    o.append(f'<path d="M{k(200)},{k(205)} l{k(50)},{k(2)} m{k(-12)},{k(-9)} l{k(12)},{k(9)} l{k(-12)},{k(9)}" stroke="{ORANGE}" stroke-width="2.5"/>')
    o.append('</g>')
    return "\n".join(o)


def icon_bars(x, y):
    """Gráfico lineal ilustrativo (sin escala), original."""
    o = []
    hs = [120, 150, 135, 175, 200, 240]
    for i, h in enumerate(hs):
        c = ORANGE if i == len(hs) - 1 else RULE
        o.append(f'<rect x="{x + i * 120}" y="{y - h}" width="72" height="{h}" fill="{c}"/>')
    o.append(f'<line x1="{x - 20}" y1="{y}" x2="{x + 6 * 120}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
    o.append(T(x + 6 * 120, y + 30, "Gráfico ilustrativo", 15, 400, MUTED, "end"))
    return "\n".join(o)


# ---------------- Post: novedades BCP (miércoles) ----------------

def sector_1():
    o = [header(1, 3, "NOVEDADES DEL SECTOR"),
         icon_bars(170, 640),
         T(72, 760, "INFORME BCP · SETIEMBRE 2026", 18, 600, ORANGE, ls=5),
         T(66, 870, "La construcción", 92, 300, INK),
         T(66, 970, "vuelve a empujar", 92, 300, INK),
         T(72, 1030, "La economía creció 3,9 % y la obra fue parte del impulso.", 26, 400, MUTED),
         source("Fuente: Banco Central del Paraguay, vía La Nación (13/11/2026)"),
         footer("y planificá tu obra con números claros")]
    return doc("\n".join(o))


def sector_2():
    o = [header(2, 3, "QUÉ DICE EL INFORME"), T(66, 220, "Los datos", 56, 300, INK)]
    stats = [("3,9 %", "crecimiento interanual · setiembre"), ("5,5 %", "acumulado enero–setiembre")]
    y = 340
    for v, lab in stats:
        o.append(T(72, y + 60, v, 96, 300, ORANGE))
        o.append(T(72, y + 104, lab.upper(), 16, 600, MUTED, ls=2))
        y += 190
    y += 10
    o.append(f'<line x1="72" y1="{y}" x2="{W-72}" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
    y += 60
    for t in ["La industria, la energía y la construcción compensaron la caída del sector primario.",
              "El repunte de la construcción vino de una mayor ejecución de obras públicas y privadas."]:
        o.append(T(72, y, "—", 26, 400, ORANGE))
        s, y = para(116, y, t, 28, 860)
        o.append(s)
        y += 26
    o.append(source("Fuente: BCP, Informe de Estudios Económicos, vía La Nación (13/11/2026)"))
    o.append(footer("y te contamos cómo arrancar tu obra"))
    return doc("\n".join(o))


def sector_3():
    o = [header(3, 3, "PARA TU OBRA"), T(66, 220, "¿Qué significa para vos?", 56, 300, INK)]
    tips = [("01", "Más obras, más demanda", "Cuadrillas y materiales se ocupan. Reservá fechas con tiempo."),
            ("02", "Cómputo antes de arrancar", "Sabé cuánto material y mano de obra lleva cada rubro."),
            ("03", "Comprá por etapas", "Planificá las compras según el avance y evitá parar la obra."),
            ("04", "Un plano completo", "Menos cambios en obra, menos sorpresas en el presupuesto.")]
    y = 330
    for n, t, d in tips:
        o.append(T(72, y + 34, n, 40, 300, ORANGE))
        o.append(T(180, y + 22, t, 30, 500, INK))
        s, _ = para(180, y + 62, d, 24, 820, MUTED)
        o.append(s)
        y += 190
    o.append(footer("y te armamos el cómputo y presupuesto por rubro"))
    return doc("\n".join(o))


# ---------------- Post: tormentas (viernes) ----------------

def clima_1():
    o = [header(1, 3, "OBRA SEGURA"),
         icon_house_rain(560, 520, 1.25),
         T(72, 880, "TEMPORADA DE TORMENTAS", 18, 600, ORANGE, ls=5),
         T(66, 980, "Tu casa, lista", 92, 300, INK),
         T(66, 1080, "para el temporal", 92, 300, INK),
         T(72, 1140, "4 claves de diseño antes de construir", 26, 400, MUTED),
         footer("y revisamos tu proyecto con vos")]
    return doc("\n".join(o))


def clima_2():
    o = [header(2, 3, "4 CLAVES"), T(66, 220, "Viento y lluvia se diseñan", 56, 300, INK)]
    tips = [("01", "Techo calculado para el viento", "Estructura y anclajes según la norma de viento y tu zona: no es lo mismo un lote abierto que uno rodeado de casas."),
            ("02", "Lluvia intensa, no solo total", "No es igual 10 mm en un día que en una hora. Canaletas y bajadas se dimensionan para el chaparrón fuerte."),
            ("03", "El agua sale del lote", "Pendientes del patio hacia afuera, rejillas y piso interior por encima del terreno."),
            ("04", "Lo diseñado se ejecuta", "Los criterios del plano tienen que llegar a la obra: control en cada etapa.")]
    y = 300
    for n, t, d in tips:
        o.append(T(72, y + 34, n, 40, 300, ORANGE))
        o.append(T(180, y + 22, t, 29, 500, INK))
        s, yy = para(180, y + 60, d, 23, 820, MUTED)
        o.append(s)
        y = yy + 40
    o.append(source("Basado en la entrevista a Diego Bentel (Capaco) en InfoNegocios (20/10/2026)"))
    o.append(footer("y revisamos tu proyecto con vos"))
    return doc("\n".join(o))


def clima_3():
    o = [header(3, 3, "CHECKLIST"), T(66, 220, "Antes de techar, revisá", 56, 300, INK)]
    items = ["Pendiente del techo adecuada al material elegido",
             "Canaletas y bajadas suficientes para toda la superficie",
             "Encuentros de techo y muros bien sellados",
             "Losas y terrazas con impermeabilización y desagüe",
             "Patio con pendiente hacia la calle o el desagüe",
             "Piso interior más alto que el terreno exterior"]
    y = 330
    for t in items:
        o.append(f'<rect x="72" y="{y - 30}" width="34" height="34" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
        o.append(f'<path d="M80,{y - 13} l8,9 l14,-18" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round"/>')
        s, _ = para(136, y, t, 28, 860)
        o.append(s)
        o.append(f'<line x1="72" y1="{y + 44}" x2="{W-72}" y2="{y + 44}" stroke="{RULE}" stroke-width="1"/>')
        y += 120
    o.append(footer("y lo dejamos resuelto en el plano"))
    return doc("\n".join(o))


POSTS = {"sector": [sector_1, sector_2, sector_3], "tormentas": [clima_1, clima_2, clima_3]}


def build(key, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = []
    for i, fn in enumerate(POSTS[key], start=1):
        base = os.path.join(outdir, f"{key}_{i}")
        open(base + ".svg", "w").write(fn())
        subprocess.run(["rsvg-convert", base + ".svg", "-o", base + ".png"], check=True)
        subprocess.run(["convert", base + ".png", "-background", BG, "-flatten", "-quality", "92", base + ".jpg"], check=True)
        os.remove(base + ".svg"); os.remove(base + ".png")
        files.append(base + ".jpg")
    return files


if __name__ == "__main__":
    print("\n".join(build(sys.argv[1], sys.argv[2])))
