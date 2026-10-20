"""Vecino más cercano: el buque siempre va al puerto pendiente que tenga más cerca."""


def vecino_mas_cercano(origen, paradas, distancias):
    """distancias[a][b] = millas mínimas de a hasta b (las calcula Dijkstra).

    Devuelve:
      orden: las paradas en el orden en que se visitan
      pasos: en cada paso, desde dónde sale, qué opciones tenía y cuál eligió
    """
    actual = origen
    pendientes = list(paradas)
    orden, pasos = [], []

    while pendientes:
        mas_cercano = min(pendientes, key=lambda puerto: distancias[actual][puerto])
        opciones = {puerto: distancias[actual][puerto] for puerto in pendientes}
        pasos.append({"desde": actual, "opciones": opciones, "elegido": mas_cercano})
        orden.append(mas_cercano)
        pendientes.remove(mas_cercano)
        actual = mas_cercano

    return orden, pasos
