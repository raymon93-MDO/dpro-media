"""Vistas axonométricas (isométricas) modernas de los modelos DPRO, en SVG.

Ejes: x hacia la derecha-abajo, y hacia la izquierda-abajo (frente/calle), z arriba.
Caras visibles: superior, frente (y máx.) y lateral derecho (x máx.).
"""
import math
import random

C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))

PAL = {
    "plaster": ("#FBFAF8", "#EEEBE6", "#D8D3CB"),   # top, frente, lateral
    "graph": ("#565C63", "#3B4148", "#2B3035"),
    "conc": ("#D2CFC9", "#BDB9B2", "#A6A29B"),
    "brick": ("#C9714F", "#B65D3E", "#9A4B30"),
    "wood": ("#C08A5E", "#A3714A", "#875A39"),
    "black": ("#3A3F44", "#1F2327", "#16191C"),
}
GLASS = "#9DB3C2"
GLASS2 = "#C9D7E0"
FRAME = "#1B1F23"
WOOD = "#A3714A"
WOODD = "#7E5435"
LAWN = "#B6C99A"
LAWN_EDGE = "#9DB27F"
PAVE = "#E3DED5"
WATER = "#7CC3DC"


class Scene:
    def __init__(self):
        self.items = []  # (orden, svg)
        self.pts = []

    # proyección en unidades (m) — se escala al final
    @staticmethod
    def P(x, y, z=0.0):
        return ((x - y) * C30, (x + y) * S30 - z)

    def poly(self, pts3, fill, order, stroke="none", sw=0, op=1.0):
        p = [self.P(*q) for q in pts3]
        self.pts += p
        self.items.append((order, ("poly", p, fill, stroke, sw, op)))

    def circle(self, x, y, z, r, fill, order, op=1.0):
        cx, cy = self.P(x, y, z)
        self.pts += [(cx - r, cy - r), (cx + r, cy + r)]
        self.items.append((order, ("circ", (cx, cy), r, fill, op)))

    def line(self, a, b, col, w, order, op=1.0):
        pa, pb = self.P(*a), self.P(*b)
        self.items.append((order, ("line", pa, pb, col, w, op)))

    # ---------- primitivas 3D ----------
    def box(self, x, y, z, w, d, h, mat="plaster", order=None, top=True):
        t, f, s = PAL[mat] if isinstance(mat, str) else mat
        o = order if order is not None else (x + w + y + d) * 10 + z * 0.1
        x1, y1, z1 = x + w, y + d, z + h
        self.poly([(x, y1, z), (x1, y1, z), (x1, y1, z1), (x, y1, z1)], f, o)          # frente
        self.poly([(x1, y, z), (x1, y1, z), (x1, y1, z1), (x1, y, z1)], s, o + 0.01)   # lateral
        if top:
            self.poly([(x, y, z1), (x1, y, z1), (x1, y1, z1), (x, y1, z1)], t, o + 0.02)
        return o

    def front_rect(self, y, x0, x1, z0, z1, fill, order, stroke="none", sw=0):
        self.poly([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], fill, order, stroke, sw)

    def side_rect(self, x, y0, y1, z0, z1, fill, order, stroke="none", sw=0):
        self.poly([(x, y0, z0), (x, y1, z0), (x, y1, z1), (x, y0, z1)], fill, order, stroke, sw)

    def glass_front(self, y, x0, x1, z0, z1, order, mull=2):
        self.front_rect(y + 0.005, x0 - 0.05, x1 + 0.05, z0 - 0.05, z1 + 0.05, FRAME, order)
        self.front_rect(y + 0.01, x0, x1, z0, z1, GLASS, order + 0.001)
        # reflejo diagonal
        h = z1 - z0
        self.poly([(x0 + (x1 - x0) * 0.15, y + 0.012, z1), (x0 + (x1 - x0) * 0.42, y + 0.012, z1),
                   (x0 + (x1 - x0) * 0.22, y + 0.012, z0), (x0, y + 0.012, z0 + h * 0.25)], GLASS2, order + 0.002, op=0.55)
        for i in range(1, mull):
            xx = x0 + (x1 - x0) * i / mull
            self.front_rect(y + 0.015, xx - 0.025, xx + 0.025, z0, z1, FRAME, order + 0.003)

    def glass_side(self, x, y0, y1, z0, z1, order, mull=1):
        self.side_rect(x + 0.005, y0 - 0.05, y1 + 0.05, z0 - 0.05, z1 + 0.05, FRAME, order)
        self.side_rect(x + 0.01, y0, y1, z0, z1, "#7F96A6", order + 0.001)
        for i in range(1, mull):
            yy = y0 + (y1 - y0) * i / mull
            self.side_rect(x + 0.015, yy - 0.025, yy + 0.025, z0, z1, FRAME, order + 0.002)

    def slats_front(self, y, x0, x1, z0, z1, order, gap=0.11, bw=0.045):
        n = int((x1 - x0) / gap)
        for i in range(n + 1):
            xx = x0 + i * (x1 - x0) / n
            self.front_rect(y + 0.03, xx - bw / 2, xx + bw / 2, z0, z1, WOOD if i % 2 else "#B27F55", order)

    def slats_side(self, x, y0, y1, z0, z1, order, gap=0.11, bw=0.045):
        n = int((y1 - y0) / gap)
        for i in range(n + 1):
            yy = y0 + i * (y1 - y0) / n
            self.side_rect(x + 0.03, yy - bw / 2, yy + bw / 2, z0, z1, WOODD if i % 2 else WOOD, order)

    def lattice_front(self, y, x0, x1, z0, z1, order):
        self.front_rect(y + 0.005, x0, x1, z0, z1, "#4A3A30", order)
        bw, bh, gx, gz = 0.24, 0.075, 0.07, 0.055
        zz, r = z0, 0
        while zz < z1 - 0.01:
            off = (bw + gx) / 2 if r % 2 else 0
            xx = x0 - off
            while xx < x1:
                a, b = max(xx, x0), min(xx + bw, x1)
                if b > a:
                    self.front_rect(y + 0.01, a, b, zz, min(zz + bh, z1), "#C26A48", order + 0.001)
                xx += bw + gx
            zz += bh + gz
            r += 1

    def door_front(self, y, x0, x1, h, order):
        self.front_rect(y + 0.005, x0 - 0.04, x1 + 0.04, 0, h + 0.04, FRAME, order)
        self.slats_front(y - 0.02, x0, x1, 0, h, order + 0.001, gap=0.08, bw=0.05)

    def parapet(self, x, y, w, d, z, mat="plaster", t=0.12, h=0.18, order=0):
        """Pretil perimetral sobre una cubierta plana."""
        self.box(x, y, z, w, t, h, mat, order=order)            # fondo
        self.box(x, y, z, t, d, h, mat, order=order + 0.01)     # izquierda
        self.box(x + w - t, y, z, t, d, h, mat, order=order + 0.02)
        self.box(x, y + d - t, z, w, t, h, mat, order=order + 0.03)

    def ground(self, x0, y0, x1, y1, fill=LAWN, z=0.0, order=-100):
        self.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], fill, order)

    def slab_edge(self, x0, y0, x1, y1, z, t, order):
        """Losa fina en voladizo (blanca) con sombra debajo."""
        self.box(x0, y0, z, x1 - x0, y1 - y0, t, "plaster", order=order)

    def shadow(self, x, y, w, d, h, order=-50, k=(0.55, -0.15)):
        dx, dy = h * k[0], h * k[1]
        pts = [(x, y + d), (x + w, y + d), (x + w + dx, y + d + dy), (x + w + dx, y + dy), (x + dx, y + dy), (x, y)]
        self.poly([(a, b, 0.001) for a, b in pts], "#3B4A36", order, op=0.18)

    def tree(self, x, y, h=4.5, r=1.4, col=("#8FAA78", "#7A9765", "#A8BF92"), flower=False, order=None):
        o = order if order is not None else (x + y) * 10 + 5
        self.shadow(x - 0.3, y - 0.3, 0.6, 0.6, h * 0.6, order=-49)
        tx, ty = self.P(x, y, 0)
        self.line((x, y, 0), (x, y, h * 0.6), "#7A6553", 0.16, o)
        rnd = random.Random(int(x * 13 + y * 7))
        cols = ("#E59BC0", "#D27BA6", "#F3B9D4") if flower else col
        for i in range(7):
            ang = rnd.uniform(0, 6.28)
            rr = r * rnd.uniform(0.55, 0.8)
            cx = x + math.cos(ang) * r * 0.45
            cy = y + math.sin(ang) * r * 0.45
            cz = h * 0.72 + rnd.uniform(-0.3, 0.6)
            self.circle(cx, cy, cz, rr, cols[i % 3], o + 0.01 * i)

    def shrubs(self, x0, x1, y, order, col="#7F9C69"):
        rnd = random.Random(int(x0 * 10 + y))
        x = x0
        while x < x1:
            self.circle(x, y, 0.25, rnd.uniform(0.22, 0.32), col if rnd.random() > 0.3 else "#93AF7C", order)
            x += 0.3

    def pool(self, x, y, w, d, order=-40):
        self.ground(x - 0.6, y - 0.6, x + w + 0.6, y + d + 0.6, PAVE, 0.002, order)
        self.poly([(x, y, 0.003), (x + w, y, 0.003), (x + w, y + d, 0.003), (x, y + d, 0.003)], WATER, order + 1)
        self.poly([(x, y, 0.004), (x + w, y, 0.004), (x + w, y + 0.25, 0.004), (x, y + 0.25, 0.004)], "#5AA9C6", order + 2)
        self.poly([(x, y, 0.004), (x + 0.25, y, 0.004), (x + 0.25, y + d, 0.004), (x, y + d, 0.004)], "#5AA9C6", order + 2)

    # ---------- render ----------
    def svg(self, W, H, pad=40, y_off=0):
        xs = [p[0] for p in self.pts]
        ys = [p[1] for p in self.pts]
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
        s = min((W - 2 * pad) / (maxx - minx), (H - 2 * pad) / (maxy - miny))
        ox = (W - (maxx - minx) * s) / 2 - minx * s
        oy = (H - (maxy - miny) * s) / 2 - miny * s + y_off
        out = []
        for _, it in sorted(self.items, key=lambda t: t[0]):
            if it[0] == "poly":
                _, p, fill, stroke, sw, op = it
                d = " ".join(f"{ox+a*s:.1f},{oy+b*s:.1f}" for a, b in p)
                o = f' opacity="{op}"' if op < 1 else ""
                out.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{o}/>')
            elif it[0] == "circ":
                _, (cx, cy), r, fill, op = it
                o = f' opacity="{op}"' if op < 1 else ""
                out.append(f'<circle cx="{ox+cx*s:.1f}" cy="{oy+cy*s:.1f}" r="{r*s:.1f}" fill="{fill}"{o}/>')
            else:
                _, a, b, col, w, op = it
                out.append(f'<line x1="{ox+a[0]*s:.1f}" y1="{oy+a[1]*s:.1f}" x2="{ox+b[0]*s:.1f}" y2="{oy+b[1]*s:.1f}" '
                           f'stroke="{col}" stroke-width="{w*s:.1f}" stroke-linecap="round"/>')
        return "\n".join(out)


def brisa():
    S = Scene()
    S.ground(-1.2, -1.5, 9.2, 11.5, LAWN, order=-200)
    S.ground(-1.2, -1.5, 9.2, 11.5, "none", order=-199)
    # vereda y senda de acceso
    S.ground(-0.4, 7.2, 4.4, 9.2, PAVE, 0.003, -150)
    S.ground(1.35, 9.2, 2.35, 11.5, PAVE, 0.003, -150)
    # sombras
    S.shadow(0, 0, 8.0, 7.2, 3.4)
    # volumen social
    o1 = S.box(0, 0, 0, 4.4, 7.2, 3.0, ("#E2DED7", "#EEEBE6", "#D8D3CB"), order=10)
    S.parapet(0, 0, 4.4, 7.2, 3.0, order=11)
    S.lattice_front(7.2, 0.15, 1.15, 0, 2.7, o1 + 0.1)
    S.door_front(7.2, 1.35, 2.3, 2.35, o1 + 0.1)
    S.glass_front(7.2, 2.55, 4.25, 0, 2.5, o1 + 0.1, 2)
    # volumen dormitorios (grafito)
    o2 = S.box(4.4, 0, 0, 3.6, 7.2, 3.45, "graph", order=20)
    S.glass_front(7.2, 5.5, 7.5, 0.9, 2.35, o2 + 0.1, 3)
    S.slats_front(7.2, 5.5, 6.5, 0.9, 2.35, o2 + 0.2)
    S.glass_side(8.0, 3.0, 3.6, 1.6, 2.2, o2 + 0.1)
    S.slats_side(8.0, 4.4, 6.9, 0.3, 3.2, o2 + 0.1)
    # pretil
    S.parapet(4.4, 0, 3.6, 7.2, 3.45, "graph", order=o2 + 0.3)
    # galería: losa fina y columnas
    S.box(-0.2, 8.98, 0, 0.12, 0.12, 2.8, "black", order=60)
    S.box(-0.3, 7.2, 2.8, 4.7, 1.95, 0.14, "plaster", order=62)
    S.shrubs(4.6, 8.0, 7.45, 63)
    S.shrubs(-0.9, -0.3, 7.8, 9)
    S.tree(-0.4, -0.6, 5.2, 1.6, order=1)
    S.tree(9.6, 2.0, 4.2, 1.3, order=150)
    S.shrubs(-0.9, -0.3, 10.6, 70)
    return S


ISO = {"brisa58": brisa}
