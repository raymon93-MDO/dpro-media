# Modelos originales DPRO. Coordenadas en metros: x hacia la derecha, y hacia el frente (calle abajo).
# Room: (nombre, x, y, w, h, tipo)  tipo: "s" seco, "h" húmedo, "c" circulación
# Semi: áreas semicubiertas (galería, quincho, cochera, balcón)
# Doors: (orient, coord_fija, desde, hasta, giro). Bisagra en "desde". giro "+"/"-": hacia +eje o -eje.
# Opens: vanos sin puerta. Windows: ventanas / corredizos.

MODELS = [
    dict(
        key="brisa58",
        nombre="Casa Brisa 58",
        bajada="Casa compacta para lote de 10x12",
        lote="10 x 12 m",
        perfil="Primera vivienda para una pareja o familia chica",
        chips=["58 m²", "2 dormitorios", "1 baño", "Galería"],
        floors=[dict(
            titulo="Planta única",
            rooms=[
                ("Cocina-comedor", 0, 0, 4.4, 3.6, "s"),
                ("Estar", 0, 3.6, 4.4, 3.6, "s"),
                ("Dormitorio 2", 4.4, 0, 3.6, 2.8, "s"),
                ("Pasillo", 4.4, 2.8, 1.4, 1.4, "c"),
                ("Baño", 5.8, 2.8, 2.2, 1.4, "h"),
                ("Dormitorio 1", 4.4, 4.2, 3.6, 3.0, "s"),
            ],
            semi=[("Galería", 0, 7.2, 8.0, 2.0)],
            opens=[("h", 3.6, 0.15, 4.25), ("v", 4.4, 3.0, 3.9)],
            doors=[("h", 7.2, 1.4, 2.3, "-"), ("h", 2.8, 4.6, 5.4, "-"), ("v", 5.8, 3.45, 4.15, "+"),
                   ("h", 4.2, 4.6, 5.4, "+"), ("h", 0, 0.4, 1.2, "+")],
            windows=[("h", 7.2, 2.6, 4.0), ("h", 7.2, 5.6, 7.4), ("h", 0, 5.6, 7.4), ("h", 0, 2.0, 3.6),
                     ("v", 8.0, 3.0, 3.6), ("v", 0, 4.4, 6.2)],
            furn=[("counter", 1.6, 0.0, 2.8, 0.6), ("sink", 2.5, 0.08), ("stove", 3.6, 0.08),
                  ("table", 1.2, 1.6, 1.4, 0.8), ("sofa", 0.12, 4.4, 0.85, 2.0, "l"), ("coffee", 1.5, 5.0, 0.6, 1.0),
                  ("tv", 4.15, 4.6, 0.12, 1.4),
                  ("bed", 5.6, 4.35, 1.4, 1.9), ("bed", 5.6, 0.12, 1.4, 1.9),
                  ("lav", 6.0, 2.95, "t"), ("wc", 6.75, 2.92, "t"), ("shower", 7.4, 2.92, 0.55, 0.55)],
            labels={"Dormitorio 2": (6.3, 2.3, 0.9), "Dormitorio 1": (6.3, 6.65, 1.0), "Baño": (6.9, 3.85, 0.8)},
        )],
        ficha_extra=[("Galería (semicubierta)", 16.0)],
        sistema=["Celosía de ladrillo en el acceso", "Volumen de dormitorios grafito con listones de madera",
                 "Galería con losa fina e iluminación embutida", "Aberturas de aluminio negro"],
        stats=[("58", "m² cubiertos"), ("2", "dormitorios"), ("1", "baño"), ("10x12", "lote mínimo")],
        etapas="Se puede construir en 2 etapas: primero estar, cocina, baño y dormitorio 1; después el dormitorio 2.",
    ),
    dict(
        key="nanduti92",
        nombre="Casa Ñandutí 92",
        bajada="Casa familiar de 3 dormitorios con suite",
        lote="15 x 25 m",
        perfil="Familia con hijos que necesita suite y cochera",
        chips=["92 m²", "3 dormitorios", "2 baños", "Cochera"],
        floors=[dict(
            titulo="Planta única",
            rooms=[
                ("Cocina", 0, 0, 5.0, 3.4, "s"),
                ("Estar-comedor", 0, 3.4, 5.0, 5.0, "s"),
                ("Lavadero", 5.0, 0, 1.8, 1.4, "h"),
                ("Baño", 5.0, 1.4, 1.8, 2.4, "h"),
                ("Dorm. principal", 6.8, 0, 4.2, 3.8, "s"),
                ("Baño suite", 9.4, 0, 1.6, 2.2, "h"),
                ("Pasillo", 5.0, 3.8, 6.0, 1.2, "c"),
                ("Dormitorio 2", 5.0, 5.0, 3.0, 3.4, "s"),
                ("Dormitorio 3", 8.0, 5.0, 3.0, 3.4, "s"),
            ],
            semi=[("Galería", 0, 8.4, 5.0, 2.4), ("Cochera", -3.4, 3.0, 3.4, 5.4)],
            opens=[("h", 3.4, 0.15, 4.85), ("v", 5.0, 3.95, 4.85)],
            doors=[("h", 8.4, 0.4, 1.4, "-"), ("v", 5.0, 0.3, 1.1, "+"), ("h", 3.8, 5.4, 6.1, "-"),
                   ("h", 3.8, 7.1, 7.9, "-"), ("h", 2.2, 9.6, 10.3, "-"), ("h", 5.0, 5.15, 5.95, "+"),
                   ("h", 5.0, 8.15, 8.95, "+"), ("v", 0, 5.6, 6.5, "+")],
            windows=[("h", 0, 1.0, 3.6), ("h", 8.4, 2.4, 4.6), ("h", 8.4, 5.7, 7.3), ("h", 8.4, 8.7, 10.3),
                     ("h", 0, 7.3, 9.0), ("v", 11.0, 2.4, 3.4), ("h", 0, 5.4, 6.4), ("h", 0, 9.8, 10.6), ("v", 11.0, 6.0, 7.4)],
            furn=[("counter", 0.0, 0.0, 3.0, 0.6), ("sink", 1.6, 0.08), ("stove", 0.5, 0.08), ("island", 1.2, 1.9, 2.4, 0.8),
                  ("table", 0.9, 4.0, 1.8, 0.9), ("sofa", 4.1, 5.6, 0.85, 2.1, "r"), ("coffee", 3.1, 6.2, 0.6, 0.9),
                  ("washer", 6.1, 0.15), ("lav", 5.25, 1.55, "t"), ("shower", 6.15, 1.55, 0.55, 0.55), ("wc", 6.8, 2.5, "r"),
                  ("bed", 7.2, 0.4, 1.6, 2.0), ("lav", 9.6, 0.15, "t"), ("shower", 10.35, 0.15, 0.55, 0.55), ("wc", 11.0, 1.2, "r"),
                  ("bed1", 6.75, 6.35, 1.0, 1.9), ("bed1", 9.75, 6.35, 1.0, 1.9),
                  ("car", -2.9, 3.6, 2.4, 4.4)],
            labels={"Dorm. principal": (8.2, 3.05, 0.9), "Baño suite": (10.0, 1.0, 0.7), "Dormitorio 2": (5.9, 7.3, 0.7),
                    "Dormitorio 3": (8.9, 7.3, 0.7), "Baño": (5.75, 3.0, 0.8), "Lavadero": (5.55, 0.95, 0.7), "Cocina": (2.5, 1.45, 1.0)},
        )],
        ficha_extra=[("Galería (semicubierta)", 12.0), ("Cochera (semicubierta)", 18.36)],
        sistema=["Estar con ventanal de doble altura", "Dormitorios en ladrillo visto con listones de madera",
                 "Cochera bajo losa en voladizo", "Suite con baño privado e isla de cocina"],
        stats=[("92", "m² cubiertos"), ("3", "dormitorios"), ("2", "baños"), ("15x25", "lote mínimo")],
        etapas="Se puede construir en 2 etapas: primero la zona social, la suite y el baño; después los dormitorios 2 y 3.",
    ),
    dict(
        key="duo70",
        nombre="Dúplex Dúo 70",
        bajada="Dúplex de 2 plantas, 2 unidades en un lote",
        lote="12 x 30 m (2 unidades)",
        perfil="Inversión para alquilar o vender, o vivienda para una familia chica",
        chips=["70 m² c/u", "2 dormitorios", "1,5 baños", "2 plantas"],
        floors=[
            dict(titulo="Planta baja",
                 rooms=[
                     ("Cocina", 0, 0, 3.2, 2.6, "s"),
                     ("Estar-comedor", 0, 2.6, 5.8, 3.4, "s"),
                     ("Toilette", 3.2, 0, 1.6, 1.4, "h"),
                     ("Hall", 3.2, 1.4, 1.6, 1.2, "c"),
                     ("Escalera", 4.8, 0, 1.0, 2.6, "c"),
                 ],
                 semi=[("Cochera", 0, 6.0, 5.8, 5.0)],
                 opens=[("h", 2.6, 0.15, 3.1), ("h", 2.6, 3.3, 5.65), ("v", 4.8, 1.0, 2.5)],
                 doors=[("h", 6.0, 0.5, 1.4, "-"), ("h", 1.4, 3.4, 4.1, "-"), ("h", 0, 1.5, 2.3, "+")],
                 windows=[("h", 6.0, 2.0, 5.2), ("h", 0, 2.5, 3.05), ("h", 0, 3.5, 4.5)],
                 furn=[("counter", 0.0, 0.0, 0.6, 2.3), ("sink", 0.08, 1.2, "v"), ("stove", 0.08, 0.3, "v"), ("table", 1.3, 1.2, 1.2, 0.8),
                       ("sofa", 2.3, 5.05, 2.4, 0.85, "b"), ("coffee", 3.0, 4.1, 1.0, 0.6), ("wc", 4.2, 0.12, "t"), ("lav", 3.35, 0.15, "t"),
                       ("stairs", 4.8, 0, 1.0, 2.6), ("car", 1.7, 6.3, 2.4, 4.4)],
                 labels={"Escalera": None, "Toilette": (3.85, 1.05, 0.7)}),
            dict(titulo="Planta alta",
                 rooms=[
                     ("Dormitorio 2", 0, 0, 2.8, 3.0, "s"),
                     ("Baño", 2.8, 0, 2.0, 1.6, "h"),
                     ("Hall", 2.8, 1.6, 3.0, 1.4, "c"),
                     ("Escalera", 4.8, 0, 1.0, 1.6, "c"),
                     ("Dorm. principal", 0, 3.0, 5.8, 3.0, "s"),
                 ],
                 semi=[("Balcón", 0, 6.0, 5.8, 1.0)],
                 opens=[("h", 1.6, 4.85, 5.65)],
                 doors=[("v", 2.8, 2.05, 2.8, "-"), ("h", 1.6, 3.0, 3.7, "-"), ("h", 3.0, 3.1, 3.9, "+")],
                 windows=[("h", 0, 0.5, 2.3), ("h", 6.0, 0.6, 3.0), ("h", 6.0, 3.4, 5.4), ("h", 0, 3.2, 4.4)],
                 furn=[("bed1", 0.3, 0.6, 1.0, 1.9), ("bed", 0.6, 3.6, 1.6, 2.0), ("closet", 4.0, 3.15, 1.65, 0.6),
                       ("wc", 4.15, 0.12, "t"), ("lav", 3.0, 0.15, "t"), ("shower", 4.2, 1.0, 0.55, 0.55), ("stairs", 4.8, 0, 1.0, 1.6)],
                 labels={"Escalera": None, "Baño": (3.6, 0.95, 0.75), "Dorm. principal": (3.6, 5.0, 1.0)}),
        ],
        ficha_extra=[("Cochera (semicubierta)", 29.0), ("Balcón", 5.8)],
        sistema=["2 unidades espejadas con medianera de celosía de ladrillo", "Planta alta en voladizo, grafito con listones",
                 "Cada unidad con acceso, cochera y patio propios", "Balcón con baranda de vidrio"],
        stats=[("70", "m² por unidad"), ("2", "dormitorios"), ("1,5", "baños"), ("2", "unidades")],
        etapas="Se puede construir primero una unidad y después la segunda, o las dos juntas para bajar el costo por m².",
    ),
    dict(
        key="lapacho90",
        nombre="Quinta Lapacho",
        bajada="Casa de quinta con quincho y piscina",
        lote="15 x 30 m",
        perfil="Fines de semana, reuniones familiares o alquiler de temporada",
        chips=["90 m² techados", "2 dormitorios", "Quincho", "Piscina"],
        floors=[dict(
            titulo="Planta única",
            rooms=[
                ("Dormitorio 1", 0, 0, 3.5, 3.4, "s"),
                ("Dormitorio 2", 3.5, 0, 3.5, 3.4, "s"),
                ("Baño", 0, 3.4, 2.2, 2.6, "h"),
                ("Cocina-estar", 2.2, 3.4, 4.8, 2.6, "s"),
            ],
            semi=[("Quincho", 7.0, 0, 8.0, 6.0)],
            pool=(8.0, 7.6, 6.0, 3.0),
            opens=[],
            doors=[("h", 3.4, 2.4, 3.2, "-"), ("h", 3.4, 3.8, 4.6, "-"), ("v", 2.2, 3.7, 4.4, "-"),
                   ("h", 6.0, 3.6, 4.5, "-")],
            windows=[("h", 0, 0.8, 2.6), ("h", 0, 4.4, 6.2), ("v", 0, 0.8, 2.6), ("h", 6.0, 5.0, 6.6), ("h", 6.0, 0.6, 1.6),
                     ("v", 7.0, 0.8, 2.6), ("v", 7.0, 4.2, 5.8)],
            furn=[("bed", 0.9, 0.12, 1.6, 2.0), ("bed1", 3.9, 0.12, 1.0, 1.9), ("bed1", 5.6, 0.12, 1.0, 1.9),
                  ("wc", 1.5, 6.0, "b"), ("lav", 0.2, 6.0, "b"), ("shower", 0.12, 3.52, 0.6, 0.6),
                  ("counter", 4.8, 3.4, 2.1, 0.6), ("sink", 5.5, 3.48), ("sofa", 2.35, 3.9, 0.85, 1.9, "l"),
                  ("grill", 13.9, 0.0, 1.1, 0.9), ("counter", 9.4, 0.0, 4.5, 0.6), ("sink", 10.5, 0.08),
                  ("bigtable", 9.3, 2.5, 3.2, 1.0)],
            labels={"Dormitorio 1": (1.75, 2.75, 0.9), "Dormitorio 2": (5.25, 2.75, 0.9), "Baño": (1.1, 4.5, 0.85), "Cocina-estar": (5.2, 4.75, 0.9)},
        )],
        ficha_extra=[("Quincho (semicubierto)", 48.0), ("Piscina 6 x 3 m", 18.0)],
        sistema=["Techo plano continuo con cielorraso de madera", "Quincho abierto con parrilla de ladrillo y mesada",
                 "Bloque de dormitorios en hormigón y grafito", "Ventanales corredizos hacia el quincho"],
        stats=[("90", "m² techados"), ("48", "m² de quincho"), ("2", "dormitorios"), ("6x3", "piscina")],
        etapas="Se puede construir primero el quincho con baño y cocina, y después los dormitorios y la piscina.",
    ),
]


def room_area(f, r):
    a = r[3] * r[4]
    for o in f["rooms"]:
        if o is not r and o[1] >= r[1] and o[2] >= r[2] and o[1] + o[3] <= r[1] + r[3] and o[2] + o[4] <= r[2] + r[4]:
            a -= o[3] * o[4]
    return a


def check():
    for m in MODELS:
        for f in m["floors"]:
            xs = [r[1] for r in f["rooms"]] + [r[1] + r[3] for r in f["rooms"]]
            ys = [r[2] for r in f["rooms"]] + [r[2] + r[4] for r in f["rooms"]]
            W, D = max(xs) - min(xs), max(ys) - min(ys)
            tot = sum(room_area(f, r) for r in f["rooms"])
            print(m["key"], f["titulo"], f"{W}x{D} = {W*D:.2f}  suma ambientes = {tot:.2f}")


if __name__ == "__main__":
    check()
