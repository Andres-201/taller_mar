"""Datos del problema: puertos, rutas marítimas, rutas de la naviera (buques) y paquetes."""

PUERTO_BASE = "CTG"  # todos los buques salen de Cartagena y regresan allí

# Puertos = nodos del grafo. lon y lat sirven para ubicarlos en el mapa.
# "etiqueta" dice de qué lado del punto se escribe el nombre (n, s, e, w, ne, nw).
PUERTOS = [
    {"id": "CTG", "nombre": "Cartagena",     "pais": "Colombia",             "lon": -75.55, "lat": 10.40, "etiqueta": "w"},
    {"id": "BAQ", "nombre": "Barranquilla",  "pais": "Colombia",             "lon": -74.85, "lat": 11.08, "etiqueta": "nw"},
    {"id": "SMR", "nombre": "Santa Marta",   "pais": "Colombia",             "lon": -74.22, "lat": 11.25, "etiqueta": "ne"},
    {"id": "COL", "nombre": "Colón",         "pais": "Panamá",               "lon": -79.91, "lat": 9.37,  "etiqueta": "s"},
    {"id": "LIM", "nombre": "Puerto Limón",  "pais": "Costa Rica",           "lon": -83.03, "lat": 9.99,  "etiqueta": "s"},
    {"id": "KIN", "nombre": "Kingston",      "pais": "Jamaica",              "lon": -76.80, "lat": 17.95, "etiqueta": "s"},
    {"id": "HAV", "nombre": "La Habana",     "pais": "Cuba",                 "lon": -82.36, "lat": 23.15, "etiqueta": "n"},
    {"id": "SDQ", "nombre": "Santo Domingo", "pais": "República Dominicana", "lon": -69.88, "lat": 18.46, "etiqueta": "s"},
    {"id": "SJU", "nombre": "San Juan",      "pais": "Puerto Rico",          "lon": -66.11, "lat": 18.47, "etiqueta": "n"},
    {"id": "WIL", "nombre": "Willemstad",    "pais": "Curazao",              "lon": -68.93, "lat": 12.11, "etiqueta": "n"},
    {"id": "LGU", "nombre": "La Guaira",     "pais": "Venezuela",            "lon": -66.93, "lat": 10.60, "etiqueta": "s"},
    {"id": "BGI", "nombre": "Bridgetown",    "pais": "Barbados",             "lon": -59.62, "lat": 13.10, "etiqueta": "s"},
]

# Rutas marítimas = aristas del grafo, con su distancia en millas náuticas (mn).
# "via" son puntos de paso [lon, lat] que solo se usan para dibujar la línea rodeando la costa.
CONEXIONES = [
    {"a": "CTG", "b": "BAQ", "millas": 75,  "via": [[-75.66, 10.66], [-75.2, 11.08]]},
    {"a": "BAQ", "b": "SMR", "millas": 39,  "via": [[-74.55, 11.2]]},
    {"a": "CTG", "b": "COL", "millas": 272, "via": [[-76.3, 10.2], [-78.6, 9.85], [-79.72, 9.68]]},
    {"a": "COL", "b": "LIM", "millas": 192, "via": [[-81.0, 9.72], [-82.55, 10.12]]},
    {"a": "CTG", "b": "KIN", "millas": 459, "via": []},
    {"a": "SMR", "b": "KIN", "millas": 429, "via": []},
    {"a": "COL", "b": "KIN", "millas": 546, "via": []},
    {"a": "KIN", "b": "HAV", "millas": 785, "via": [[-76.8, 17.78], [-77.3, 17.55], [-78.5, 17.75], [-82.8, 19.4], [-85.35, 21.75], [-84.9, 22.6], [-83.6, 23.28]]},
    {"a": "LIM", "b": "HAV", "millas": 956, "via": [[-82.55, 11.6], [-82.2, 14.6], [-83.4, 17.5], [-85.35, 21.75], [-84.9, 22.6], [-83.6, 23.28]]},
    {"a": "KIN", "b": "SDQ", "millas": 432, "via": [[-76.78, 17.8], [-76.3, 17.7], [-75.6, 17.65], [-73.6, 17.6], [-71.3, 17.3]]},
    {"a": "SDQ", "b": "SJU", "millas": 238, "via": [[-68.8, 17.9], [-68.0, 18.25], [-67.3, 18.7]]},
    {"a": "SDQ", "b": "WIL", "millas": 385, "via": []},
    {"a": "SMR", "b": "WIL", "millas": 351, "via": [[-72.6, 12.35], [-71.55, 12.75], [-70.0, 12.85], [-69.3, 12.25]]},
    {"a": "WIL", "b": "LGU", "millas": 149, "via": []},
    {"a": "LGU", "b": "BGI", "millas": 464, "via": [[-64.2, 11.4], [-61.6, 11.75]]},
    {"a": "SJU", "b": "BGI", "millas": 553, "via": [[-65.5, 18.65], [-64.0, 18.6], [-62.3, 15.0], [-60.95, 14.27]]},
]

# Rutas de la naviera: cada una es un buque con los puertos que atiende y su capacidad.
#   max_paquetes = cuántos paquetes puede llevar   peso_max = cuántos kg puede llevar
#   nudos = velocidad (1 nudo = 1 milla náutica por hora)
RUTAS = [
    {"id": "costera",  "nombre": "Ruta Costera",   "buque": "Ciénaga I",      "puertos": ["BAQ", "SMR"],               "max_paquetes": 4, "peso_max": 1500, "nudos": 12, "color": "#bd7406"},
    {"id": "istmo",    "nombre": "Ruta del Istmo", "buque": "Darién Express", "puertos": ["COL", "LIM"],               "max_paquetes": 5, "peso_max": 2000, "nudos": 14, "color": "#12805a"},
    {"id": "antillas", "nombre": "Ruta Antillas",  "buque": "Gran Antillano", "puertos": ["KIN", "SDQ", "SJU", "HAV"], "max_paquetes": 6, "peso_max": 3000, "nudos": 16, "color": "#2a56c0"},
    {"id": "oriental", "nombre": "Ruta Oriental",  "buque": "Sotavento",      "puertos": ["WIL", "LGU", "BGI"],        "max_paquetes": 5, "peso_max": 2200, "nudos": 14, "color": "#c2382d"},
]

# Paquetes: nombre, puerto destino, peso en kg y valor del flete en US$.
# La ruta de cada paquete es la que atiende su puerto destino.
PAQUETES = [
    {"codigo": "PK-101", "nombre": "Café de origen",             "destino": "SMR", "peso": 420, "valor": 1850},
    {"codigo": "PK-102", "nombre": "Repuestos de motor",         "destino": "BAQ", "peso": 780, "valor": 2300},
    {"codigo": "PK-103", "nombre": "Medicamentos refrigerados",  "destino": "BAQ", "peso": 150, "valor": 2900},
    {"codigo": "PK-104", "nombre": "Textiles de algodón",        "destino": "SMR", "peso": 380, "valor": 900},
    {"codigo": "PK-105", "nombre": "Cacao en grano",             "destino": "BAQ", "peso": 500, "valor": 1400},
    {"codigo": "PK-106", "nombre": "Equipos de cómputo",         "destino": "SMR", "peso": 240, "valor": 2100},
    {"codigo": "PK-201", "nombre": "Flores frescas",             "destino": "COL", "peso": 260, "valor": 1700},
    {"codigo": "PK-202", "nombre": "Maquinaria agrícola",        "destino": "LIM", "peso": 900, "valor": 3100},
    {"codigo": "PK-203", "nombre": "Electrodomésticos",          "destino": "COL", "peso": 540, "valor": 1900},
    {"codigo": "PK-204", "nombre": "Insumos médicos",            "destino": "LIM", "peso": 180, "valor": 1500},
    {"codigo": "PK-205", "nombre": "Calzado de cuero",           "destino": "COL", "peso": 330, "valor": 1100},
    {"codigo": "PK-206", "nombre": "Paneles solares",            "destino": "LIM", "peso": 620, "valor": 2400},
    {"codigo": "PK-301", "nombre": "Repuestos navales",          "destino": "KIN", "peso": 700, "valor": 2600},
    {"codigo": "PK-302", "nombre": "Arroz empacado",             "destino": "HAV", "peso": 850, "valor": 1300},
    {"codigo": "PK-303", "nombre": "Medicinas genéricas",        "destino": "HAV", "peso": 200, "valor": 2800},
    {"codigo": "PK-304", "nombre": "Materiales de construcción", "destino": "SDQ", "peso": 950, "valor": 2000},
    {"codigo": "PK-305", "nombre": "Artesanías wayuu",           "destino": "SDQ", "peso": 120, "valor": 650},
    {"codigo": "PK-306", "nombre": "Equipos electrónicos",       "destino": "SJU", "peso": 300, "valor": 2500},
    {"codigo": "PK-307", "nombre": "Muebles de madera",          "destino": "KIN", "peso": 640, "valor": 1450},
    {"codigo": "PK-308", "nombre": "Confitería",                 "destino": "SJU", "peso": 410, "valor": 1150},
    {"codigo": "PK-401", "nombre": "Frutas tropicales",          "destino": "WIL", "peso": 480, "valor": 1350},
    {"codigo": "PK-402", "nombre": "Herramientas",               "destino": "LGU", "peso": 560, "valor": 1700},
    {"codigo": "PK-403", "nombre": "Cosméticos",                 "destino": "BGI", "peso": 150, "valor": 1900},
    {"codigo": "PK-404", "nombre": "Papel y cartón",             "destino": "LGU", "peso": 720, "valor": 980},
    {"codigo": "PK-405", "nombre": "Café especial",              "destino": "BGI", "peso": 260, "valor": 1600},
    {"codigo": "PK-406", "nombre": "Llantas",                    "destino": "WIL", "peso": 680, "valor": 1500},
]
