"""Mochila 0/1: qué paquetes suben al buque para llevar el mayor valor posible.

El buque tiene dos límites: peso máximo (kg) y cantidad máxima de paquetes.
Cada paquete se lleva completo o no se lleva (por eso es 0/1).
"""

from functools import cache


def mochila(paquetes, peso_max, max_paquetes):
    """Devuelve la lista de paquetes elegidos."""

    @cache  # programación dinámica: cada caso (i, peso_libre, cupos) se calcula una sola vez
    def mejor_valor(i, peso_libre, cupos):
        """Mayor valor que se puede lograr con los paquetes desde el i en adelante."""
        if i == len(paquetes) or cupos == 0:
            return 0
        sin_llevarlo = mejor_valor(i + 1, peso_libre, cupos)
        paquete = paquetes[i]
        if paquete["peso"] > peso_libre:
            return sin_llevarlo  # no cabe
        llevandolo = paquete["valor"] + mejor_valor(i + 1, peso_libre - paquete["peso"], cupos - 1)
        return max(sin_llevarlo, llevandolo)

    # Reconstruir la respuesta: si saltarse el paquete i empeora el resultado, ese paquete va a bordo
    elegidos = []
    peso_libre, cupos = peso_max, max_paquetes
    for i, paquete in enumerate(paquetes):
        if mejor_valor(i, peso_libre, cupos) != mejor_valor(i + 1, peso_libre, cupos):
            elegidos.append(paquete)
            peso_libre -= paquete["peso"]
            cupos -= 1
    return elegidos
