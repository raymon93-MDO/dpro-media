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




# ---------------- Post: cómo leer un plano (educativo) ----------------

def _brisa_plan(x, y, w, h):
    from models import MODELS
    from plan import Plan
    m = [m for m in MODELS if m["key"] == "brisa58"][0]
    return Plan(m["floors"][0], w, h, x, y).render()


def plano_1():
    o = [header(1, 3, "APRENDÉ CON DPRO"),
         _brisa_plan(60, 170, W - 120, 640),
         T(72, 900, "GUÍA RÁPIDA", 18, 600, ORANGE, ls=5),
         T(66, 1000, "Cómo leer", 92, 300, INK),
         T(66, 1100, "el plano de tu casa", 80, 300, INK),
         T(72, 1160, "Lo que tenés que entender antes de construir", 26, 400, MUTED),
         footer("y te explicamos tu plano punto por punto")]
    return doc("\n".join(o))


def plano_2():
    o = [header(2, 3, "LOS 4 ELEMENTOS"), T(66, 220, "Qué mirar en un plano", 56, 300, INK)]
    tips = [("01", "Las cotas", "Los números sobre las líneas son medidas en metros: largo y ancho de cada ambiente y del total."),
            ("02", "Los ambientes", "Cada espacio lleva su nombre y su superficie en m². Sumados te dan los m² cubiertos."),
            ("03", "Puertas y ventanas", "El arco muestra hacia dónde abre la puerta. Las líneas finas en el muro son ventanas."),
            ("04", "Lo cubierto y lo semicubierto", "Galerías y quinchos se marcan aparte: tienen techo pero no cierre completo.")]
    y = 300
    for n, t, d in tips:
        o.append(T(72, y + 34, n, 40, 300, ORANGE))
        o.append(T(180, y + 22, t, 29, 500, INK))
        s, yy = para(180, y + 60, d, 23, 820, MUTED)
        o.append(s)
        y = yy + 40
    o.append(footer("y te explicamos tu plano punto por punto"))
    return doc("\n".join(o))


def plano_3():
    o = [header(3, 3, "POR QUÉ IMPORTA"), T(66, 220, "Un buen plano te ahorra", 56, 300, INK)]
    tips = [("Cambios en obra", "Cada cambio a mitad de camino suma material, mano de obra y días."),
            ("Discusiones", "Con medidas claras, vos, el maestro de obras y el proveedor hablan el mismo idioma."),
            ("Sorpresas en el presupuesto", "Del plano sale el cómputo: cuánto material lleva cada rubro.")]
    y = 340
    for t, d in tips:
        o.append(f'<rect x="72" y="{y - 6}" width="6" height="96" fill="{ORANGE}"/>')
        o.append(T(104, y + 26, t, 34, 500, INK))
        s, yy = para(104, y + 72, d, 25, 860, MUTED)
        o.append(s)
        y = yy + 70
    o.append(footer("y te armamos plano + cómputo para tu terreno"))
    return doc("\n".join(o))


# ---------------- Post: construir por etapas (educativo) ----------------

def _stages(x, y):
    o = []
    for i in range(4):
        cx = x + i * 230
        h = 90 + i * 70
        o.append(f'<rect x="{cx}" y="{y - h}" width="170" height="{h}" fill="{ORANGE if i == 3 else "none"}" stroke="{INK}" stroke-width="3"/>')
        o.append(T(cx + 85, y + 50, f"Etapa {i + 1}", 22, 500, MUTED, "middle"))
    o.append(f'<line x1="{x - 30}" y1="{y}" x2="{x + 4 * 230 - 30}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
    return "\n".join(o)


def etapas_1():
    o = [header(1, 3, "CONSTRUÍ A TU RITMO"),
         _stages(120, 700),
         T(72, 900, "PLANIFICACIÓN", 18, 600, ORANGE, ls=5),
         T(66, 1000, "Tu casa,", 92, 300, INK),
         T(66, 1100, "por etapas", 92, 300, INK),
         T(72, 1160, "Cómo avanzar sin parar la obra ni rehacer trabajos", 26, 400, MUTED),
         footer("y te armamos el plan por etapas")]
    return doc("\n".join(o))


def etapas_2():
    o = [header(2, 3, "EL ORDEN"), T(66, 220, "Las 4 etapas de una obra", 56, 300, INK)]
    tips = [("01", "Cimientos y estructura", "Lo que no se ve y sostiene todo. Se hace bien una sola vez."),
            ("02", "Muros y techo", "Con el techo puesto, la obra queda protegida de la lluvia."),
            ("03", "Instalaciones y revoques", "Cañerías y cableado antes de revocar, para no romper después."),
            ("04", "Terminaciones", "Pisos, aberturas, pintura y artefactos: lo que más se ve.")]
    y = 300
    for n, t, d in tips:
        o.append(T(72, y + 34, n, 40, 300, ORANGE))
        o.append(T(180, y + 22, t, 29, 500, INK))
        s, yy = para(180, y + 60, d, 23, 820, MUTED)
        o.append(s)
        y = yy + 40
    o.append(footer("y te armamos el plan por etapas"))
    return doc("\n".join(o))


def etapas_3():
    o = [header(3, 3, "LA CLAVE"), T(66, 220, "Pensá la casa completa", 56, 300, INK),
         T(66, 290, "aunque la hagas de a poco", 56, 300, INK)]
    tips = [("El plano completo, desde el inicio", "Así la etapa 1 ya queda lista para lo que viene."),
            ("Cómputo por etapa", "Sabés cuánto material y mano de obra necesitás en cada paso."),
            ("Dejá previstas las ampliaciones", "Cañerías, cimientos y aberturas pensadas para crecer.")]
    y = 420
    for t, d in tips:
        o.append(f'<rect x="72" y="{y - 6}" width="6" height="96" fill="{ORANGE}"/>')
        o.append(T(104, y + 26, t, 34, 500, INK))
        s, yy = para(104, y + 72, d, 25, 860, MUTED)
        o.append(s)
        y = yy + 70
    o.append(footer("y te armamos el plan por etapas"))
    return doc("\n".join(o))


# ---------------- Post: obras frenadas por deuda (novedades) ----------------

def icon_paused_house(cx, cy):
    """Ícono lineal original: casa a medio construir con símbolo de pausa."""
    o = [f'<g transform="translate({cx},{cy})" fill="none" stroke-linecap="round" stroke-linejoin="round">']
    o.append(f'<path d="M-200,0 L0,-150 L200,0" stroke="{INK}" stroke-width="4" stroke-dasharray="18 14"/>')
    o.append(f'<path d="M-160,-30 V190 H160 V-30" stroke="{INK}" stroke-width="3"/>')
    for i in range(5):
        y = 150 - i * 40
        w = 320 - i * 50
        o.append(f'<line x1="-160" y1="{y}" x2="{-160 + w}" y2="{y}" stroke="{RULE}" stroke-width="3"/>')
    o.append(f'<line x1="-260" y1="190" x2="260" y2="190" stroke="{MUTED}" stroke-width="2"/>')
    o.append(f'<circle cx="190" cy="-90" r="62" fill="{BG}" stroke="{ORANGE}" stroke-width="4"/>')
    o.append(f'<line x1="172" y1="-115" x2="172" y2="-65" stroke="{ORANGE}" stroke-width="8"/>')
    o.append(f'<line x1="208" y1="-115" x2="208" y2="-65" stroke="{ORANGE}" stroke-width="8"/>')
    o.append('</g>')
    return "\n".join(o)


def deuda_1():
    o = [header(1, 3, "NOVEDADES DEL SECTOR"),
         icon_paused_house(540, 520),
         T(72, 860, "CAPACO · NOVIEMBRE 2026", 18, 600, ORANGE, ls=5),
         T(66, 970, "Obras que se frenan", 88, 300, INK),
         T(66, 1066, "por falta de pago", 88, 300, INK),
         T(72, 1126, "Qué pasa en la obra pública y cómo cuidar la tuya", 26, 400, MUTED),
         source("Fuente: InfoNegocios, con datos de Capaco (18/11/2026)"),
         footer("y planificá tu obra con números claros")]
    return doc("\n".join(o))


def deuda_2():
    o = [header(2, 3, "LOS DATOS"), T(66, 220, "Lo que advierte Capaco", 56, 300, INK)]
    stats = [("US$ 350 M", "deuda del estado con constructoras · capital + intereses"),
             ("30.000–40.000", "empleos del sector en riesgo si no se regulariza")]
    y = 340
    for v, lab in stats:
        o.append(T(72, y + 60, v, 88, 300, ORANGE))
        o.append(T(72, y + 104, lab.upper(), 16, 600, MUTED, ls=2))
        y += 190
    y += 10
    o.append(f'<line x1="72" y1="{y}" x2="{W-72}" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
    y += 60
    for t in ["A octubre había 176 trámites de pago pendientes en el MOPC, de 83 empresas y consorcios.",
              "Según Capaco, ya hay obras paralizadas y el gremio pide regularizar los pagos."]:
        o.append(T(72, y, "—", 26, 400, ORANGE))
        s, y = para(116, y, t, 28, 860)
        o.append(s)
        y += 26
    o.append(source("Fuente: InfoNegocios, «Construcción sin cimiento financiero» (18/11/2026)"))
    o.append(footer("y te contamos cómo arrancar tu obra"))
    return doc("\n".join(o))


def deuda_3():
    o = [header(3, 3, "PARA TU OBRA"), T(66, 220, "Que la tuya no se frene", 56, 300, INK)]
    tips = [("01", "Pagá por avance", "Cada pago contra un avance medido en obra, no por adelantado."),
            ("02", "Todo por escrito", "Alcance, plazos y forma de pago en un contrato claro."),
            ("03", "Cómputo y cronograma", "Sabé cuánto lleva cada etapa y cuándo la vas a pagar."),
            ("04", "Etapas que cierran", "Arrancá una etapa cuando tengas cubierta la etapa completa.")]
    y = 330
    for n, t, d in tips:
        o.append(T(72, y + 34, n, 40, 300, ORANGE))
        o.append(T(180, y + 22, t, 30, 500, INK))
        s, _ = para(180, y + 62, d, 24, 820, MUTED)
        o.append(s)
        y += 190
    o.append(footer("y te armamos el cómputo y el plan de pagos"))
    return doc("\n".join(o))


# ---------------- Educativos de los modelos nuevos (Yvoty, Tajy, Trío) ----------------

def _g(cx, cy, body):
    return f'<g transform="translate({cx},{cy})" fill="none" stroke-linecap="round" stroke-linejoin="round">{body}</g>'


def icon_shop_home():
    """Ícono lineal original: salón con vidriera abajo y vivienda arriba."""
    b = [f'<rect x="-180" y="-220" width="360" height="190" stroke="{INK}" stroke-width="4"/>',
         f'<rect x="-120" y="-180" width="110" height="80" stroke="{INK}" stroke-width="3"/>',
         f'<rect x="30" y="-180" width="90" height="80" stroke="{INK}" stroke-width="3"/>',
         f'<rect x="-180" y="-30" width="360" height="220" stroke="{INK}" stroke-width="4"/>',
         f'<line x1="-220" y1="-30" x2="220" y2="-30" stroke="{ORANGE}" stroke-width="8"/>',
         f'<rect x="-150" y="20" width="200" height="170" stroke="{ORANGE}" stroke-width="3"/>',
         f'<line x1="-50" y1="20" x2="-50" y2="190" stroke="{ORANGE}" stroke-width="2"/>',
         f'<rect x="100" y="40" width="50" height="150" stroke="{INK}" stroke-width="3"/>',
         f'<line x1="-260" y1="190" x2="260" y2="190" stroke="{MUTED}" stroke-width="2"/>']
    return _g(540, 560, "".join(b))


def icon_one_two():
    """Ícono lineal original: una planta vs dos plantas sobre el mismo lote."""
    b = [f'<rect x="-300" y="60" width="260" height="130" stroke="{INK}" stroke-width="4"/>',
         f'<rect x="80" y="-80" width="170" height="135" stroke="{ORANGE}" stroke-width="4"/>',
         f'<rect x="80" y="55" width="170" height="135" stroke="{INK}" stroke-width="4"/>',
         f'<rect x="250" y="55" width="80" height="135" stroke="{RULE}" stroke-width="3" stroke-dasharray="10 8"/>',
         f'<line x1="-340" y1="190" x2="-0" y2="190" stroke="{MUTED}" stroke-width="2"/>',
         f'<line x1="40" y1="190" x2="370" y2="190" stroke="{MUTED}" stroke-width="2"/>']
    return _g(540, 540, "".join(b)) + T(400, 790, "1 planta", 24, 500, MUTED, "middle") + T(705, 790, "2 plantas", 24, 500, MUTED, "middle")


def icon_three_units():
    """Ícono lineal original: tres unidades en hilera con pasillo lateral."""
    b = [f'<line x1="-260" y1="-230" x2="-260" y2="210" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="16 12"/>']
    for i in range(3):
        y = -230 + i * 150
        b.append(f'<rect x="-200" y="{y}" width="420" height="120" stroke="{INK}" stroke-width="4"/>')
        b.append(f'<rect x="-200" y="{y + 40}" width="20" height="44" fill="{ORANGE}" stroke="none"/>')
        b.append(T(10, y + 72, f"Unidad {i + 1}", 26, 500, MUTED, "middle"))
    return _g(540, 520, "".join(b))


def _cover(kicker, icon, label, t1, t2, sub, foot):
    return doc("\n".join([header(1, 3, kicker), icon, T(72, 900, label, 18, 600, ORANGE, ls=5),
                          T(66, 1000, t1, 84, 300, INK), T(66, 1096, t2, 84, 300, INK),
                          T(72, 1156, sub, 26, 400, MUTED), footer(foot)]))


def _tips(n, kicker, title, tips, foot, y=330, step=190):
    o = [header(n, 3, kicker), T(66, 220, title, 56, 300, INK)]
    for i, (t, d) in enumerate(tips, start=1):
        o.append(T(72, y + 34, f"0{i}", 40, 300, ORANGE))
        o.append(T(180, y + 22, t, 30, 500, INK))
        s, _ = para(180, y + 62, d, 24, 820, MUTED)
        o.append(s)
        y += step
    o.append(footer(foot))
    return doc("\n".join(o))


F_SALON = "y te armamos el plano con salón y vivienda"
F_PLANTAS = "y vemos qué conviene en tu lote"
F_RENTA = "y te armamos el cómputo por unidad"


def salon_1():
    return _cover("TU CASA, TU NEGOCIO", icon_shop_home(), "PLANIFICACIÓN", "Que tu casa", "te deje ingresos",
                  "Un salón al frente: lo que hay que prever desde el plano", F_SALON)


def salon_2():
    return _tips(2, "DESDE EL PLANO", "Lo que se decide antes", [
        ("Acceso independiente", "La vivienda con su propia entrada, sin pasar por el salón."),
        ("Medidores separados", "Luz y agua del salón aparte: más orden y más fácil de alquilar."),
        ("Baño y depósito en el salón", "Lo mínimo para que funcione cualquier rubro."),
        ("Estructura para crecer", "Columnas y losa calculadas para la planta alta, aunque se haga después.")], F_SALON)


def salon_3():
    return _tips(3, "ANTES DE ARRANCAR", "Verificá esto primero", [
        ("Qué usos permite tu zona", "Consultá en tu municipalidad antes de diseñar el salón."),
        ("Frente y vereda", "Vidriera, alero y una vereda en condiciones venden solos."),
        ("Planta baja primero", "El salón puede empezar a rendir mientras se termina la vivienda.")], F_SALON, y=360, step=230)


def plantas_1():
    return _cover("¿QUÉ CONVIENE?", icon_one_two(), "DISEÑO", "¿1 planta", "o 2 plantas?",
                  "Cómo elegir según tu lote, tu familia y tu presupuesto", F_PLANTAS)


def plantas_2():
    return _tips(2, "LA COMPARACIÓN", "Lo que cambia", [
        ("Una planta", "Sin escaleras y más simple de construir, pero ocupa más terreno."),
        ("Dos plantas", "Libera patio en lotes angostos. Necesita escalera y estructura calculada."),
        ("Techo y cimientos", "En 2 plantas, el mismo techo cubre el doble; los cimientos se calculan para ese peso."),
        ("Quién vive", "Con personas mayores, conviene un dormitorio en planta baja.")], F_PLANTAS)


def plantas_3():
    return _tips(3, "PARA DECIDIR", "Preguntate esto", [
        ("¿Cuánto patio querés?", "Si el patio importa y el lote es angosto, subí."),
        ("¿Vas a ampliar?", "Si es así, dejá la losa y la escalera previstas desde el inicio."),
        ("¿Cuánto podés invertir hoy?", "Las 2 plantas se pueden hacer por etapas: primero la baja.")], F_PLANTAS, y=360, step=230)


def renta_1():
    return _cover("INVERSIÓN", icon_three_units(), "INVERSIÓN", "Construir", "para alquilar",
                  "Cómo pensar departamentos para alquilar desde el plano", F_RENTA)


def renta_2():
    return _tips(2, "EL DISEÑO", "Lo que busca un inquilino", [
        ("Entrada propia", "Un pasillo lateral y cada unidad con su acceso."),
        ("Medidores individuales", "Cada inquilino paga su luz y su agua."),
        ("Espacios bien resueltos", "Dormitorio, baño y cocina-estar con buena luz natural."),
        ("Un lugar afuera", "Una galería chica suma mucho al alquilar.")], F_RENTA)


def renta_3():
    return _tips(3, "LOS NÚMEROS", "Para que rinda", [
        ("Materiales que duran", "Menos mantenimiento entre un inquilino y el siguiente."),
        ("De a una unidad", "La primera empieza a rendir mientras se hace la siguiente."),
        ("Presupuesto real", "Hacé los números con un cómputo por rubro, no con estimaciones.")], F_RENTA, y=360, step=230)


POSTS = {"sector": [sector_1, sector_2, sector_3], "tormentas": [clima_1, clima_2, clima_3],
         "plano": [plano_1, plano_2, plano_3], "etapas": [etapas_1, etapas_2, etapas_3],
         "deuda": [deuda_1, deuda_2, deuda_3], "salon": [salon_1, salon_2, salon_3],
         "plantas": [plantas_1, plantas_2, plantas_3], "renta": [renta_1, renta_2, renta_3]}


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
