"""Dibujo de plantas arquitectónicas en SVG a partir de models.py."""
from models import room_area

NAVY = "#0C3553"
ORANGE = "#F07A1D"
WALL = "#1E2A35"
FURN = "#8C97A3"
FLOOR = "#FFFFFF"
WET = "#EEF4F8"
SEMI = "#F4EEE5"
DIM = "#5B6773"

T_EXT = 0.20
T_INT = 0.12


def fmt(v):
    s = f"{v:.2f}".replace(".", ",")
    return s


class Plan:
    def __init__(self, floor, box_w, box_h, ox=0, oy=0, dims=True, font=1.0):
        self.f = floor
        self.dims = dims
        self.font = font
        rooms = floor["rooms"]
        self.rx0 = min(r[1] for r in rooms)
        self.rx1 = max(r[1] + r[3] for r in rooms)
        self.ry0 = min(r[2] for r in rooms)
        self.ry1 = max(r[2] + r[4] for r in rooms)
        xs = [self.rx0, self.rx1] + [s[1] for s in floor.get("semi", [])] + [s[1] + s[3] for s in floor.get("semi", [])]
        ys = [self.ry0, self.ry1] + [s[2] for s in floor.get("semi", [])] + [s[2] + s[4] for s in floor.get("semi", [])]
        if floor.get("pool"):
            p = floor["pool"]
            xs += [p[0] - 0.8, p[0] + p[2] + 0.8]
            ys += [p[1] + p[3] + 0.8]
        self.bx0, self.bx1, self.by0, self.by1 = min(xs), max(xs), min(ys), max(ys)
        m = 1.6 if dims else 0.4  # margen para cotas (m)
        mw = (self.bx1 - self.bx0) + 2 * m
        mh = (self.by1 - self.by0) + 2 * m
        self.s = min(box_w / mw, box_h / mh)
        # centrar
        self.ox = ox + (box_w - mw * self.s) / 2 + m * self.s - self.bx0 * self.s
        self.oy = oy + (box_h - mh * self.s) / 2 + m * self.s - self.by0 * self.s
        self.out = []

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, y):
        return self.oy + y * self.s

    def L(self, l):
        return l * self.s

    def add(self, s):
        self.out.append(s)

    # ---------- primitivas ----------
    def rect(self, x, y, w, h, fill="none", stroke="none", sw=0, extra=""):
        self.add(f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{self.L(w):.1f}" height="{self.L(h):.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:.2f}" {extra}/>')

    def line(self, x1, y1, x2, y2, stroke=FURN, sw=1.2, extra=""):
        self.add(f'<line x1="{self.X(x1):.1f}" y1="{self.Y(y1):.1f}" x2="{self.X(x2):.1f}" y2="{self.Y(y2):.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw:.2f}" {extra}/>')

    def text(self, x, y, t, size, weight=500, fill=NAVY, anchor="middle", extra=""):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{size:.1f}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>')

    # ---------- render ----------
    def render(self):
        f = self.f
        fw = max(1.0, self.s * 0.012)
        # semicubiertos
        for name, x, y, w, h in f.get("semi", []):
            self.rect(x, y, w, h, SEMI, "#B9A98F", 1.4, 'stroke-dasharray="7 5"')
        if f.get("pool"):
            px, py, pw, ph = f["pool"]
            self.rect(px - 0.8, py - 0.8, pw + 1.6, ph + 1.6, "#EDE6DA", "#C9BBA5", 1.2)
            self.rect(px, py, pw, ph, "#8FC9E3", "#4E9CC0", 2)
            for i in range(1, 5):
                yy = py + ph * i / 5
                self.add(f'<path d="M{self.X(px+0.3):.1f},{self.Y(yy):.1f} q{self.L(0.4):.1f},-{self.L(0.12):.1f} {self.L(0.8):.1f},0 '
                         f't{self.L(0.8):.1f},0 t{self.L(0.8):.1f},0 t{self.L(0.8):.1f},0 t{self.L(0.8):.1f},0 t{self.L(0.8):.1f},0" '
                         f'fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity="0.7"/>')
        # pisos
        for name, x, y, w, h, t in f["rooms"]:
            self.rect(x, y, w, h, WET if t == "h" else FLOOR)
        # baño suite encima del dormitorio
        for name, x, y, w, h, t in f["rooms"]:
            if t == "h":
                self.rect(x, y, w, h, WET)
                # grilla de cerámica
                step = 0.3
                gx = x + step
                while gx < x + w - 0.01:
                    self.line(gx, y, gx, y + h, "#DCE6EE", 0.8)
                    gx += step
                gy = y + step
                while gy < y + h - 0.01:
                    self.line(x, gy, x + w, gy, "#DCE6EE", 0.8)
                    gy += step
        # muros
        ext = []
        segs = []
        for name, x, y, w, h, t in f["rooms"]:
            segs += [("h", y, x, x + w), ("h", y + h, x, x + w), ("v", x, y, y + h), ("v", x + w, y, y + h)]
        for o, c, a, b in segs:
            is_ext = (o == "h" and (abs(c - self.ry0) < 1e-6 or abs(c - self.ry1) < 1e-6)) or \
                     (o == "v" and (abs(c - self.rx0) < 1e-6 or abs(c - self.rx1) < 1e-6))
            t = T_EXT if is_ext else T_INT
            if o == "h":
                self.rect(a - T_EXT / 2, c - t / 2, b - a + T_EXT, t, WALL)
            else:
                self.rect(c - t / 2, a - T_EXT / 2, t, b - a + T_EXT, WALL)
        # vanos
        def gap(o, c, a, b):
            t = T_EXT + 0.04
            if o == "h":
                self.rect(a, c - t / 2, b - a, t, FLOOR)
            else:
                self.rect(c - t / 2, a, t, b - a, FLOOR)
        for o, c, a, b in f.get("opens", []):
            gap(o, c, a, b)
            if o == "h":
                self.line(a, c, b, c, "#C3CBD3", 1, 'stroke-dasharray="4 4"')
            else:
                self.line(c, a, c, b, "#C3CBD3", 1, 'stroke-dasharray="4 4"')
        for o, c, a, b, g in f.get("doors", []):
            gap(o, c, a, b)
            L = b - a
            sg = 1 if g == "+" else -1
            if o == "h":
                hx, hy = a, c
                ex, ey = a, c + sg * L
                self.line(hx, hy, ex, ey, WALL, 1.8)
                sweep = 0 if sg > 0 else 1
                self.add(f'<path d="M{self.X(b):.1f},{self.Y(c):.1f} A{self.L(L):.1f},{self.L(L):.1f} 0 0 {sweep} {self.X(ex):.1f},{self.Y(ey):.1f}" '
                         f'fill="none" stroke="{FURN}" stroke-width="1" stroke-dasharray="3 3"/>')
            else:
                hx, hy = c, a
                ex, ey = c + sg * L, a
                self.line(hx, hy, ex, ey, WALL, 1.8)
                sweep = 1 if sg > 0 else 0
                self.add(f'<path d="M{self.X(c):.1f},{self.Y(b):.1f} A{self.L(L):.1f},{self.L(L):.1f} 0 0 {sweep} {self.X(ex):.1f},{self.Y(ey):.1f}" '
                         f'fill="none" stroke="{FURN}" stroke-width="1" stroke-dasharray="3 3"/>')
        for o, c, a, b in f.get("windows", []):
            t = T_EXT
            if o == "h":
                self.rect(a, c - t / 2, b - a, t, "#D7ECF7", WALL, 1)
                self.line(a, c, b, c, WALL, 1)
            else:
                self.rect(c - t / 2, a, t, b - a, "#D7ECF7", WALL, 1)
                self.line(c, a, c, b, WALL, 1)
        # muebles
        for it in f.get("furn", []):
            getattr(self, "f_" + it[0])(*it[1:])
        # rótulos
        for r in f["rooms"]:
            name, x, y, w, h, t = r
            a = room_area(f, r)
            cx, cy = x + w / 2, y + h / 2
            labs = f.get("labels", {})
            size = min(self.L(0.42), 30) * self.font
            if t == "c" and a < 3:
                size *= 0.75
            if name in labs:
                if labs[name] is None:
                    continue
                cx, cy, sc = labs[name]
                size *= sc
            px, py = self.X(cx), self.Y(cy)
            self.text(px, py - size * 0.1, name.upper(), size * 0.62, 700, NAVY,
                      extra='style="letter-spacing:0.5px" paint-order="stroke" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"')
            self.text(px, py + size * 0.72, f"{fmt(a)} m²", size * 0.56, 500, DIM,
                      extra='paint-order="stroke" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"')
        for name, x, y, w, h in f.get("semi", []):
            size = min(self.L(0.42), 30) * self.font
            px, py = self.X(x + w / 2), self.Y(y + h / 2)
            if name == "Quincho":
                py = self.Y(y + h * 0.78)
            if name == "Cochera":
                py = self.Y(y + h * 0.5)
            self.text(px, py - size * 0.1, name.upper(), size * 0.62, 700, "#7A6A52",
                      extra='paint-order="stroke" stroke="#F4EEE5" stroke-width="5" stroke-linejoin="round"')
            self.text(px, py + size * 0.72, f"{fmt(w*h)} m²", size * 0.56, 500, "#7A6A52",
                      extra='paint-order="stroke" stroke="#F4EEE5" stroke-width="5" stroke-linejoin="round"')
        if f.get("pool"):
            px, py, pw, ph = f["pool"]
            size = min(self.L(0.42), 30) * self.font
            self.text(self.X(px + pw / 2), self.Y(py + ph / 2) + size * 0.2, "PISCINA 6 x 3 m", size * 0.62, 700, "#1F5F80",
                      extra='paint-order="stroke" stroke="#8FC9E3" stroke-width="4" stroke-linejoin="round"')
        if self.dims:
            self.dimensions()
        return "\n".join(self.out)

    # ---------- cotas ----------
    def dim_h(self, xs, y, off):
        yy = self.Y(y) + off
        for i in range(len(xs) - 1):
            a, b = xs[i], xs[i + 1]
            self.add(f'<line x1="{self.X(a):.1f}" y1="{yy:.1f}" x2="{self.X(b):.1f}" y2="{yy:.1f}" stroke="{DIM}" stroke-width="1"/>')
            if self.L(b - a) > 26:
                self.text((self.X(a) + self.X(b)) / 2, yy - 5, fmt(b - a), 13 * self.font, 500, DIM)
        for x in xs:
            self.add(f'<line x1="{self.X(x)-4:.1f}" y1="{yy+4:.1f}" x2="{self.X(x)+4:.1f}" y2="{yy-4:.1f}" stroke="{DIM}" stroke-width="1.4"/>')
            self.add(f'<line x1="{self.X(x):.1f}" y1="{yy-7:.1f}" x2="{self.X(x):.1f}" y2="{yy+7:.1f}" stroke="{DIM}" stroke-width="0.8"/>')

    def dim_v(self, ys, x, off):
        xx = self.X(x) + off
        for i in range(len(ys) - 1):
            a, b = ys[i], ys[i + 1]
            self.add(f'<line x1="{xx:.1f}" y1="{self.Y(a):.1f}" x2="{xx:.1f}" y2="{self.Y(b):.1f}" stroke="{DIM}" stroke-width="1"/>')
            if self.L(b - a) > 26:
                cx, cy = xx - 6, (self.Y(a) + self.Y(b)) / 2
                self.text(cx, cy, fmt(b - a), 13 * self.font, 500, DIM, extra=f'transform="rotate(-90 {cx:.1f} {cy:.1f})"')
        for y in ys:
            self.add(f'<line x1="{xx-4:.1f}" y1="{self.Y(y)+4:.1f}" x2="{xx+4:.1f}" y2="{self.Y(y)-4:.1f}" stroke="{DIM}" stroke-width="1.4"/>')
            self.add(f'<line x1="{xx-7:.1f}" y1="{self.Y(y):.1f}" x2="{xx+7:.1f}" y2="{self.Y(y):.1f}" stroke="{DIM}" stroke-width="0.8"/>')

    def dimensions(self):
        f = self.f
        rs = f["rooms"]
        top = sorted({round(v, 2) for r in rs if abs(r[2] - self.ry0) < 1e-6 for v in (r[1], r[1] + r[3])} |
                     {round(v, 2) for s in f.get("semi", []) if abs(s[2] - self.ry0) < 1e-6 for v in (s[1], s[1] + s[3])})
        left = sorted({round(v, 2) for r in rs if abs(r[1] - self.rx0) < 1e-6 for v in (r[2], r[2] + r[4])})
        g = 0.55 * self.s
        self.dim_h(top, self.by0, -g)
        self.dim_h([top[0], top[-1]], self.by0, -g - 26)
        self.dim_v(left, self.bx0, -g)
        self.dim_v([self.ry0, self.ry1], self.bx0, -g - 26)

    # ---------- muebles ----------
    def _r(self, x, y, w, h, fill="#FFFFFF", rx=0.0, sw=1.2, stroke=FURN):
        self.add(f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{self.L(w):.1f}" height="{self.L(h):.1f}" rx="{self.L(rx):.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def f_bed(self, x, y, w, h):
        self._r(x, y, w, h, "#FFFFFF", 0.05)
        pw = (w - 0.3) / 2
        self._r(x + 0.1, y + 0.1, pw, 0.35, "#F3F5F7", 0.06)
        self._r(x + 0.2 + pw, y + 0.1, pw, 0.35, "#F3F5F7", 0.06)
        self._r(x, y + h * 0.42, w, h * 0.58, "#E6EDF3", 0.05)
        self.line(x, y + h * 0.42 + 0.18, x + w, y + h * 0.42 + 0.18, FURN, 0.9)

    def f_bed1(self, x, y, w, h):
        self._r(x, y, w, h, "#FFFFFF", 0.05)
        self._r(x + 0.12, y + 0.1, w - 0.24, 0.3, "#F3F5F7", 0.06)
        self._r(x, y + h * 0.4, w, h * 0.6, "#E6EDF3", 0.05)

    def f_sofa(self, x, y, w, h, back):
        self._r(x, y, w, h, "#E9E2D6", 0.08)
        b = 0.2
        if back == "l":
            self._r(x, y, b, h, "#DCD2C2", 0.05)
            self._r(x, y, w, b, "#DCD2C2", 0.05)
            self._r(x, y + h - b, w, b, "#DCD2C2", 0.05)
        elif back == "r":
            self._r(x + w - b, y, b, h, "#DCD2C2", 0.05)
            self._r(x, y, w, b, "#DCD2C2", 0.05)
            self._r(x, y + h - b, w, b, "#DCD2C2", 0.05)
        elif back == "b":
            self._r(x, y + h - b, w, b, "#DCD2C2", 0.05)
            self._r(x, y, b, h, "#DCD2C2", 0.05)
            self._r(x + w - b, y, b, h, "#DCD2C2", 0.05)

    def f_coffee(self, x, y, w, h):
        self._r(x, y, w, h, "#F4EFE7", 0.08)

    def f_tv(self, x, y, w, h):
        self._r(x, y, w, h, "#3A4652", 0.02, 0.8, "#3A4652")

    def _chairs(self, x, y, w, h, n):
        cw = 0.42
        for i in range(n):
            cx = x + (i + 0.5) * w / n - cw / 2
            self._r(cx, y - 0.32, cw, 0.28, "#FFFFFF", 0.06)
            self._r(cx, y + h + 0.04, cw, 0.28, "#FFFFFF", 0.06)

    def f_table(self, x, y, w, h):
        n = 3 if w >= 1.7 else 2
        if w < h:
            self._r(x, y, w, h, "#F4EFE7", 0.04)
            return
        self._chairs(x, y, w, h, n)
        self._r(x, y, w, h, "#F4EFE7", 0.04)

    def f_bigtable(self, x, y, w, h):
        self._chairs(x, y, w, h, 5)
        self._r(x, y, w, h, "#E8DCC8", 0.04)

    def f_counter(self, x, y, w, h):
        self._r(x, y, w, h, "#F0F2F4", 0, 1.0)

    def f_island(self, x, y, w, h):
        self._r(x, y, w, h, "#E8EBEE", 0.03, 1.0)
        for i in range(3):
            cx = x + (i + 0.5) * w / 3
            self.add(f'<circle cx="{self.X(cx):.1f}" cy="{self.Y(y+h+0.3):.1f}" r="{self.L(0.18):.1f}" fill="#FFFFFF" stroke="{FURN}" stroke-width="1.1"/>')

    def f_sink(self, x, y, o="h"):
        w, h = (0.8, 0.45) if o == "h" else (0.45, 0.8)
        self._r(x, y, w, h, "#FFFFFF", 0.04, 1.0)
        self._r(x + 0.06, y + 0.06, w - 0.12, h - 0.12, "#EAF2F7", 0.05, 0.8)

    def f_stove(self, x, y, o="h"):
        w, h = (0.6, 0.45) if o == "h" else (0.45, 0.6)
        self._r(x, y, w, h, "#FFFFFF", 0.02, 1.0)
        for i in range(2):
            for j in range(2):
                cx = x + w * (0.27 + 0.46 * i)
                cy = y + h * (0.27 + 0.46 * j)
                self.add(f'<circle cx="{self.X(cx):.1f}" cy="{self.Y(cy):.1f}" r="{self.L(0.07):.1f}" fill="none" stroke="{FURN}" stroke-width="1"/>')

    def f_wc(self, x, y, side):
        tw, td, bl, bw = 0.42, 0.18, 0.5, 0.36
        if side == "t":
            self._r(x, y, tw, td, "#FFFFFF", 0.03, 1.0)
            self.add(f'<ellipse cx="{self.X(x+tw/2):.1f}" cy="{self.Y(y+td+bl/2-0.02):.1f}" rx="{self.L(bw/2):.1f}" ry="{self.L(bl/2):.1f}" fill="#FFFFFF" stroke="{FURN}" stroke-width="1.1"/>')
        elif side == "b":
            self._r(x, y - td, tw, td, "#FFFFFF", 0.03, 1.0)
            self.add(f'<ellipse cx="{self.X(x+tw/2):.1f}" cy="{self.Y(y-td-bl/2+0.02):.1f}" rx="{self.L(bw/2):.1f}" ry="{self.L(bl/2):.1f}" fill="#FFFFFF" stroke="{FURN}" stroke-width="1.1"/>')
        elif side == "r":
            self._r(x - td, y, td, tw, "#FFFFFF", 0.03, 1.0)
            self.add(f'<ellipse cx="{self.X(x-td-bl/2+0.02):.1f}" cy="{self.Y(y+tw/2):.1f}" rx="{self.L(bl/2):.1f}" ry="{self.L(bw/2):.1f}" fill="#FFFFFF" stroke="{FURN}" stroke-width="1.1"/>')

    def f_lav(self, x, y, side):
        w, h = 0.55, 0.42
        yy = y if side == "t" else y - h
        self._r(x, yy, w, h, "#FFFFFF", 0.04, 1.0)
        self.add(f'<ellipse cx="{self.X(x+w/2):.1f}" cy="{self.Y(yy+h/2):.1f}" rx="{self.L(0.18):.1f}" ry="{self.L(0.13):.1f}" fill="#EAF2F7" stroke="{FURN}" stroke-width="0.9"/>')

    def f_shower(self, x, y, w, h):
        self._r(x, y, w, h, "#E3EEF5", 0, 1.0)
        self.line(x, y, x + w, y + h, FURN, 0.8)
        self.line(x + w, y, x, y + h, FURN, 0.8)
        self.add(f'<circle cx="{self.X(x+w/2):.1f}" cy="{self.Y(y+h/2):.1f}" r="{self.L(0.04):.1f}" fill="{FURN}"/>')

    def f_washer(self, x, y):
        self._r(x, y, 0.6, 0.6, "#FFFFFF", 0.04, 1.0)
        self.add(f'<circle cx="{self.X(x+0.3):.1f}" cy="{self.Y(y+0.32):.1f}" r="{self.L(0.2):.1f}" fill="#EAF2F7" stroke="{FURN}" stroke-width="1"/>')

    def f_closet(self, x, y, w, h):
        self._r(x, y, w, h, "#F4EFE7", 0, 1.0)
        n = int(w / 0.5)
        for i in range(1, n):
            self.line(x + i * w / n, y, x + i * w / n, y + h, FURN, 0.8)

    def f_stairs(self, x, y, w, h):
        n = int(h / 0.27)
        for i in range(1, n):
            self.line(x + 0.05, y + i * h / n, x + w - 0.05, y + i * h / n, FURN, 0.9)
        self.add(f'<line x1="{self.X(x+w/2):.1f}" y1="{self.Y(y+h-0.15):.1f}" x2="{self.X(x+w/2):.1f}" y2="{self.Y(y+0.25):.1f}" '
                 f'stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arrow)"/>')

    def f_car(self, x, y, w, h):
        self._r(x, y, w, h, "#FFFFFF", 0.45, 1.3, "#A7B0B9")
        self._r(x + 0.2, y + h * 0.22, w - 0.4, h * 0.2, "#E6EDF3", 0.15, 1.0, "#A7B0B9")
        self._r(x + 0.2, y + h * 0.66, w - 0.4, h * 0.14, "#E6EDF3", 0.12, 1.0, "#A7B0B9")

    def f_grill(self, x, y, w, h):
        self._r(x, y, w, h, "#B5583A", 0.02, 1.0, "#7A3A24")
        self._r(x + 0.12, y + 0.12, w - 0.24, h - 0.3, "#3A3F44", 0.02, 0.8, "#3A3F44")
        for i in range(1, 6):
            xx = x + 0.12 + i * (w - 0.24) / 6
            self.line(xx, y + 0.14, xx, y + h - 0.2, "#8C97A3", 0.8)
