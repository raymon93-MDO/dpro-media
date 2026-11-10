"""Fachadas modernas al atardecer (vista frontal) para los modelos DPRO."""
import random

MODE = "dusk"  # "dusk" o "light"

PLASTER = "#ECEAE6"
PLASTER_SH = "#D9D6D0"
CHAR = "#2C3136"
CHAR2 = "#23282C"
CONC = "#B9B6AF"
CONC2 = "#A7A49D"
WOOD = "#A06B43"
WOOD2 = "#7C5032"
BRICK = "#B65D3E"
BRICK2 = "#8E4429"
FRAME = "#15191C"
LAWN = "#4E6B3F"
LAWN2 = "#3E5832"
PATH = "#C9C3B8"


class Elev:
    def __init__(self, W, H, x0, x1, mh, ground_frac=0.78):
        self.W, self.H = W, H
        self.gy = H * ground_frac
        mw = x1 - x0
        self.s = min((W * 0.90) / (mw + 1.2), (self.gy * 0.74) / mh)
        self.ox = (W - mw * self.s) / 2 - x0 * self.s
        self.out = []
        self.uid = random.randint(0, 99999)

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, z):
        return self.gy - z * self.s

    def L(self, l):
        return l * self.s

    def add(self, s):
        self.out.append(s)

    def box(self, x, z, w, h, fill, extra=""):
        self.add(f'<rect x="{self.X(x):.1f}" y="{self.Y(z+h):.1f}" width="{self.L(w):.1f}" height="{self.L(h):.1f}" fill="{fill}" {extra}/>')

    def background(self):
        W, H, gy, u = self.W, self.H, self.gy, self.uid
        self.add(f'''<defs>
<linearGradient id="sky{u}" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#1D2B3C"/><stop offset="0.45" stop-color="#4C5D74"/>
 <stop offset="0.78" stop-color="#C99A86"/><stop offset="1" stop-color="#F2C08F"/></linearGradient>
<linearGradient id="warm{u}" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#FFE3A8"/><stop offset="1" stop-color="#F0A95A"/></linearGradient>
<linearGradient id="glass{u}" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="{'#CBD5DC' if MODE == 'light' else '#4F6378'}"/><stop offset="1" stop-color="{'#9EAEBA' if MODE == 'light' else '#2C3A49'}"/></linearGradient>
<radialGradient id="glow{u}" cx="0.5" cy="0" r="1">
 <stop offset="0" stop-color="#FFD58A" stop-opacity="0.75"/><stop offset="1" stop-color="#FFD58A" stop-opacity="0"/></radialGradient>
<linearGradient id="lawn{u}" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="{LAWN}"/><stop offset="1" stop-color="#2F4426"/></linearGradient>
<linearGradient id="pool{u}" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#5FC2DE"/><stop offset="1" stop-color="#2A7FA3"/></linearGradient>
</defs>''')
        if MODE == "light":
            self.add(f'<rect width="{W}" height="{H}" fill="#F5F3EF"/>')
            self.add(f'<rect x="0" y="{gy:.1f}" width="{W}" height="{H-gy:.1f}" fill="#F5F3EF"/>')
            self.add(f'<line x1="0" y1="{gy:.1f}" x2="{W}" y2="{gy:.1f}" stroke="#C9C1B4" stroke-width="1.5"/>')
            return
        self.add(f'<rect width="{W}" height="{H}" fill="url(#sky{u})"/>')
        rnd = random.Random(3)
        for i in range(40):
            self.add(f'<circle cx="{rnd.uniform(0,W):.0f}" cy="{rnd.uniform(0,H*0.3):.0f}" r="{rnd.uniform(0.6,1.6):.1f}" fill="#FFFFFF" opacity="{rnd.uniform(0.2,0.6):.2f}"/>')
        # siluetas de árboles lejanos
        pts = [f"0,{gy:.0f}"]
        x = 0
        while x < W:
            pts.append(f"{x:.0f},{gy - rnd.uniform(30, 85):.0f}")
            x += rnd.uniform(18, 40)
        pts.append(f"{W},{gy:.0f}")
        self.add(f'<polygon points="{" ".join(pts)}" fill="#2B3A3A" opacity="0.55"/>')
        self.add(f'<rect x="0" y="{gy:.1f}" width="{W}" height="{H-gy:.1f}" fill="url(#lawn{u})"/>')

    def tree(self, x, h=5.0, r=1.6, col="#2F4432", flower=None):
        tx = self.X(x)
        self.add(f'<rect x="{tx-self.L(0.08):.1f}" y="{self.Y(h*0.6):.1f}" width="{self.L(0.16):.1f}" height="{self.L(h*0.6):.1f}" fill="{'#8C7A68' if MODE == 'light' else '#2A211B'}"/>')
        c = flower or col
        if MODE == "light":
            c = "#E7A9C6" if flower else "#A9B79C"
        cy = self.Y(h * 0.74)
        for dx, dy, rr in [(0, 0, 1), (-0.65, 0.3, 0.72), (0.7, 0.25, 0.75), (0.15, -0.5, 0.65)]:
            self.add(f'<circle cx="{tx+self.L(r*dx):.1f}" cy="{cy+self.L(r*dy):.1f}" r="{self.L(r*rr):.1f}" fill="{c}"/>')
        if flower:
            rnd = random.Random(int(x * 10))
            for _ in range(60):
                self.add(f'<circle cx="{tx+self.L(rnd.uniform(-r*1.3,r*1.3)):.1f}" cy="{cy+self.L(rnd.uniform(-r*1.0,r*0.8)):.1f}" r="{self.L(0.07):.1f}" fill="#FFC1DC"/>')

    def palm(self, x, h=4.0):
        tx = self.X(x)
        self.add(f'<rect x="{tx-self.L(0.07):.1f}" y="{self.Y(h):.1f}" width="{self.L(0.14):.1f}" height="{self.L(h):.1f}" fill="{'#8C7A68' if MODE == 'light' else '#2A211B'}"/>')
        for a in (-60, -25, 15, 50, 85, 120, 160, 200):
            self.add(f'<ellipse cx="{tx:.1f}" cy="{self.Y(h):.1f}" rx="{self.L(1.2):.1f}" ry="{self.L(0.18):.1f}" fill="{'#9AAA8D' if MODE == 'light' else '#24382A'}" transform="rotate({a} {tx:.1f} {self.Y(h):.1f})"/>')

    def plaster(self, x, z, w, h, col=PLASTER):
        self.box(x, z, w, h, col)

    def concrete(self, x, z, w, h):
        self.box(x, z, w, h, CONC)
        for i in range(1, int(w / 1.2) + 1):
            self.add(f'<line x1="{self.X(x+i*1.2):.1f}" y1="{self.Y(z):.1f}" x2="{self.X(x+i*1.2):.1f}" y2="{self.Y(z+h):.1f}" stroke="{CONC2}" stroke-width="1"/>')
        for j in range(1, int(h / 0.6) + 1):
            self.add(f'<line x1="{self.X(x):.1f}" y1="{self.Y(z+j*0.6):.1f}" x2="{self.X(x+w):.1f}" y2="{self.Y(z+j*0.6):.1f}" stroke="{CONC2}" stroke-width="0.6" opacity="0.6"/>')

    def slats(self, x, z, w, h, gap=0.12, bw=0.06, back=None, vertical=True):
        if back:
            self.box(x, z, w, h, back)
        if vertical:
            n = int(w / gap)
            for i in range(n + 1):
                self.box(x + i * w / n - bw / 2 if i else x, z, bw, h, WOOD if i % 2 else "#AE7A50")
        else:
            n = int(h / gap)
            for i in range(n):
                self.box(x, z + i * h / n, w, bw, WOOD)

    def lattice(self, x, z, w, h):
        """Celosía de ladrillo (cobogó) con luz cálida atrás."""
        self.box(x, z, w, h, "#E6D8C3" if MODE == "light" else f"url(#warm{self.uid})")
        bw, bh, gx, gz = 0.25, 0.07, 0.08, 0.06
        row = 0
        zz = z
        while zz < z + h - 0.01:
            off = (bw + gx) / 2 if row % 2 else 0
            xx = x - off
            while xx < x + w:
                a, b = max(xx, x), min(xx + bw, x + w)
                if b > a:
                    self.box(a, zz, b - a, min(bh, z + h - zz), BRICK)
                xx += bw + gx
            # tabique horizontal
            self.box(x, zz + bh, w, min(gz * 0.35, max(0, z + h - zz - bh)), BRICK2)
            zz += bh + gz
            row += 1

    def bricks(self, x, z, w, h):
        self.box(x, z, w, h, BRICK)
        rh = 0.14
        r = 0
        zz = z
        while zz < z + h:
            self.add(f'<line x1="{self.X(x):.1f}" y1="{self.Y(zz):.1f}" x2="{self.X(x+w):.1f}" y2="{self.Y(zz):.1f}" stroke="{BRICK2}" stroke-width="0.9"/>')
            bx = x + (0.13 if r % 2 else 0)
            while bx < x + w:
                self.add(f'<line x1="{self.X(bx):.1f}" y1="{self.Y(zz):.1f}" x2="{self.X(bx):.1f}" y2="{self.Y(min(zz+rh, z+h)):.1f}" stroke="{BRICK2}" stroke-width="0.7"/>')
                bx += 0.26
            zz += rh
            r += 1

    def glass(self, x, z, w, h, n=2, lit=True, frame=FRAME):
        if MODE == "light":
            lit = False
        self.box(x - 0.04, z - 0.04, w + 0.08, h + 0.08, frame)
        self.box(x, z, w, h, f"url(#warm{self.uid})" if lit else f"url(#glass{self.uid})")
        if lit:
            # interior sugerido: lámpara colgante y mueble
            self.add(f'<rect x="{self.X(x+w*0.15):.1f}" y="{self.Y(z+0.55):.1f}" width="{self.L(w*0.4):.1f}" height="{self.L(0.4):.1f}" fill="#C98845" opacity="0.55"/>')
            self.add(f'<circle cx="{self.X(x+w*0.7):.1f}" cy="{self.Y(z+h-0.45):.1f}" r="{self.L(0.12):.1f}" fill="#FFF6DD"/>')
            self.add(f'<line x1="{self.X(x+w*0.7):.1f}" y1="{self.Y(z+h):.1f}" x2="{self.X(x+w*0.7):.1f}" y2="{self.Y(z+h-0.35):.1f}" stroke="{frame}" stroke-width="1"/>')
        for i in range(1, n):
            self.box(x + i * w / n - 0.025, z, 0.05, h, frame)

    def door(self, x, w=1.0, h=2.3):
        self.box(x - 0.04, 0, w + 0.08, h + 0.04, FRAME)
        self.slats(x, 0, w, h, gap=0.09, bw=0.05, back=WOOD2)
        self.box(x + w - 0.14, 0.9, 0.04, 0.5, "#D8C39A")

    def slab(self, x, z, w, t=0.22, col=PLASTER, light=True, downlights=()):
        self.box(x, z, w, t, col)
        self.box(x, z - 0.04, w, 0.04, "#000000", 'opacity="0.25"')
        for dx in (downlights if MODE != "light" else ()):
            cx = self.X(dx)
            top = self.Y(z)
            hh = self.L(z)
            self.add(f'<polygon points="{cx-self.L(0.06):.1f},{top:.1f} {cx+self.L(0.06):.1f},{top:.1f} {cx+self.L(0.75):.1f},{top+hh:.1f} {cx-self.L(0.75):.1f},{top+hh:.1f}" fill="url(#glow{self.uid})" opacity="0.5"/>')
            self.add(f'<circle cx="{cx:.1f}" cy="{top+1.5:.1f}" r="{self.L(0.05):.1f}" fill="#FFF3D1"/>')

    def column(self, x, z, h, w=0.12):
        self.box(x, z, w, h, FRAME)

    def uplight(self, x, h=2.5):
        cx = self.X(x)
        self.add(f'<polygon points="{cx-self.L(0.05):.1f},{self.Y(0):.1f} {cx+self.L(0.05):.1f},{self.Y(0):.1f} {cx+self.L(0.4):.1f},{self.Y(h):.1f} {cx-self.L(0.4):.1f},{self.Y(h):.1f}" fill="#FFE0A0" opacity="0.18"/>')

    def plants(self, x, w, h=0.55, col="#3C5A33"):
        if MODE == "light":
            col = "#9BB08E"
        n = max(2, int(w / 0.3))
        rnd = random.Random(int(x * 100))
        for i in range(n):
            cx = self.X(x + (i + 0.5) * w / n)
            hh = self.L(h * rnd.uniform(0.7, 1.2))
            self.add(f'<ellipse cx="{cx:.1f}" cy="{self.Y(0)-hh*0.45:.1f}" rx="{self.L(w/n*0.7):.1f}" ry="{hh*0.55:.1f}" fill="{col}"/>')

    def path(self, x, w):
        if MODE == "light":
            return
        u = self.L(w)
        cx = self.X(x)
        self.add(f'<polygon points="{cx:.1f},{self.Y(0):.1f} {cx+u:.1f},{self.Y(0):.1f} {cx+u*1.35:.1f},{self.H:.1f} {cx-u*0.35:.1f},{self.H:.1f}" fill="{PATH}" opacity="0.85"/>')

    def car(self, x):
        X, Y, L = self.X, self.Y, self.L
        self.add(f'<rect x="{X(x):.1f}" y="{Y(1.25):.1f}" width="{L(4.2):.1f}" height="{L(0.75):.1f}" rx="{L(0.25):.1f}" fill="#3B4248"/>')
        self.add(f'<path d="M{X(x+0.9):.1f},{Y(1.25):.1f} L{X(x+1.5):.1f},{Y(1.75):.1f} L{X(x+3.0):.1f},{Y(1.75):.1f} L{X(x+3.6):.1f},{Y(1.25):.1f} Z" fill="#59656F"/>')
        for wx in (x + 0.9, x + 3.3):
            self.add(f'<circle cx="{X(wx):.1f}" cy="{Y(0.42):.1f}" r="{L(0.36):.1f}" fill="#111"/>')
        self.add(f'<rect x="{X(x+4.0):.1f}" y="{Y(1.05):.1f}" width="{L(0.2):.1f}" height="{L(0.12):.1f}" fill="#FFF1C2"/>')

    def svg(self):
        return "\n".join(self.out)


def brisa(W, H):
    e = Elev(W, H, -0.6, 8.6, 3.8)
    e.background()
    e.tree(-1.8, 5.2, 1.6)
    e.palm(9.8, 4.2)
    e.box(-0.4, 0, 8.8, 0.2, "#D8D2C7")
    # volumen social blanco
    e.plaster(0, 0.2, 4.4, 2.9)
    e.lattice(0.15, 0.2, 1.05, 2.6)
    e.door(1.35, 1.0, 2.3)
    e.glass(2.6, 0.2, 1.6, 2.3, 2)
    # volumen dormitorios en voladizo, oscuro con listones
    e.box(4.4, 0.2, 3.6, 3.4, CHAR)
    e.glass(5.0, 0.95, 2.4, 1.5, 3)
    e.slats(5.0, 0.95, 1.2, 1.5, gap=0.14, bw=0.05)
    e.box(4.3, 3.6, 3.9, 0.12, CHAR2)
    # losa fina de galería
    e.slab(-0.5, 2.95, 4.95, 0.18, PLASTER, downlights=(1.0, 2.6, 3.7))
    e.column(-0.4, 0.2, 2.75)
    e.plants(5.0, 2.6, 0.45)
    e.plants(-0.4, 0.5, 0.6)
    e.path(1.35, 1.0)
    return e.svg()


def nanduti(W, H):
    e = Elev(W, H, -4.0, 11.6, 4.2)
    e.background()
    e.tree(-5.2, 5.6, 1.7)
    e.tree(12.8, 5.0, 1.5)
    e.box(-3.8, 0, 15.2, 0.2, "#D8D2C7")
    # cochera bajo losa continua
    e.car(-3.7)
    # volumen social: doble altura
    e.plaster(0, 0.2, 5.0, 3.8)
    e.glass(2.0, 0.2, 2.9, 3.6, 3)
    e.door(0.6, 1.0, 2.4)
    e.lattice(0.0, 2.75, 1.9, 1.25)
    # muro de hormigón separador
    e.concrete(5.0, 0.2, 0.5, 3.6)
    # volumen dormitorios: ladrillo visto + listones
    e.bricks(5.5, 0.2, 5.5, 2.95)
    e.glass(6.0, 0.95, 1.6, 1.4, 2)
    e.glass(8.9, 0.95, 1.6, 1.4, 2)
    e.slats(8.9, 0.95, 1.6, 1.4, gap=0.13, bw=0.05)
    e.box(5.4, 3.15, 5.8, 0.15, CHAR2)
    # losa continua sobre cochera + acceso
    e.slab(-4.0, 3.05, 4.0, 0.2, CHAR, downlights=(-3.0, -1.0))
    e.column(-3.95, 0.2, 2.85)
    e.slab(-0.2, 4.0, 5.4, 0.2, PLASTER)
    e.plants(5.6, 5.2, 0.45)
    e.path(0.6, 1.0)
    return e.svg()


def duo(W, H):
    e = Elev(W, H, -0.4, 12.0, 6.6)
    e.background()
    e.tree(-1.6, 5.4, 1.5)
    e.tree(13.3, 5.0, 1.4)
    e.box(-0.3, 0, 12.2, 0.18, "#D8D2C7")
    for k, mir in ((0.0, False), (5.8, True)):
        def xx(x, w=0):
            return k + (5.8 - x - w if mir else x)
        # PB blanca, retirada
        e.plaster(k, 0.18, 5.8, 2.75)
        e.door(xx(0.5, 1.0), 1.0, 2.3)
        e.glass(xx(2.0, 3.4), 0.18, 3.4, 2.4, 3)
        # PA en voladizo, oscura
        e.box(k - (0.0 if not mir else 0.0), 2.95, 5.8, 2.95, CHAR)
        e.glass(xx(0.5, 3.0), 3.1, 3.0, 2.2, 3)
        e.slats(xx(3.8, 1.6), 3.1, 1.6, 2.5, gap=0.12, bw=0.05)
        e.box(k, 2.95, 5.8, 0.06, "#000000", 'opacity="0.3"')
        # baranda vidrio
        e.box(xx(0.5, 3.0), 3.1, 3.0, 0.95, "#BFD6E3", 'opacity="0.35"')
        e.box(k, 5.9, 5.8, 0.14, CHAR2)
        e.uplight(xx(0.3), 2.5)
        e.plants(xx(2.0, 3.4), 3.4, 0.4)
    # medianera celosía
    e.lattice(5.55, 0.18, 0.5, 5.85)
    return e.svg()


def lapacho(W, H):
    e = Elev(W, H, -0.8, 15.8, 4.2)
    e.background()
    e.tree(-2.2, 5.8, 1.8, flower="#D6609A")
    e.palm(17.0, 4.6)
    e.box(-0.6, 0, 16.4, 0.25, "#D8D2C7")
    # piscina (borde, vista frontal)
    e.box(7.6, 0.0, 6.8, 0.25, "#E2DCD0")
    e.box(8.0, 0.03, 6.0, 0.16, f"url(#pool{e.uid})")
    # bloque cerrado: hormigón + madera
    e.concrete(0, 0.25, 2.2, 2.9)
    e.box(2.2, 0.25, 4.8, 2.9, CHAR)
    e.glass(2.6, 0.25, 2.2, 2.4, 2)
    e.slats(5.2, 0.25, 1.6, 2.65, gap=0.12, bw=0.05)
    e.glass(0.5, 1.2, 1.2, 1.0, 1, lit=False)
    # quincho: techo plano fino con cielorraso de madera
    e.box(7.0, 0.25, 8.0, 2.75, "#3A3128")
    e.box(7.0, 2.7, 8.0, 0.3, WOOD)  # cielorraso madera visto en perspectiva
    for i in range(16):
        e.box(7.0 + i * 0.5, 2.7, 0.04, 0.3, WOOD2)
    e.box(9.4, 0.25, 4.5, 0.9, "#D7D2C9")
    e.box(9.4, 1.15, 4.5, 0.05, "#888")
    e.bricks(13.9, 0.25, 1.1, 2.45)
    e.box(14.05, 0.95, 0.8, 0.55, "#FF9A3C", 'opacity="0.85"')
    # mesa
    e.box(9.3, 0.95, 3.2, 0.07, WOOD)
    for i in range(5):
        e.box(9.45 + i * 0.62, 0.25, 0.38, 0.45, "#1E1E1E")
    e.slab(-0.6, 3.15, 16.2, 0.22, PLASTER, downlights=(8.2, 10.4, 12.6, 14.6))
    for cx in (7.0, 14.95):
        e.column(cx - 0.06, 0.25, 2.9)
    e.plants(0.0, 2.0, 0.5)
    return e.svg()


FACADES = {"brisa58": brisa, "nanduti92": nanduti, "duo70": duo, "lapacho90": lapacho}
