"""Dijkstra: la distancia más corta desde un puerto de origen hasta todos los demás."""

import heapq


def dijkstra(grafo, origen):
    """grafo = {"CTG": [("BAQ", 75), ("KIN", 459), ...], "BAQ": [...], ...}

    Devuelve tres cosas:
      distancias: {puerto: millas mínimas desde el origen}
      previos:    {puerto: puerto desde el que se llega en el camino más corto}
      pasos:      qué pasó cada vez que se visitó un puerto (para mostrarlo en la página)
    """
    distancias = {puerto: float("inf") for puerto in grafo}
    previos = {puerto: None for puerto in grafo}
    distancias[origen] = 0
    visitados = set()
    cola = [(0, origen)]  # cola de prioridad: siempre sale el puerto con menor distancia
    pasos = []

    while cola:
        distancia, puerto = heapq.heappop(cola)
        if puerto in visitados:
            continue
        visitados.add(puerto)

        # ¿Llegar a cada vecino pasando por este puerto es más corto que lo conocido?
        actualizados = []
        for vecino, millas in grafo[puerto]:
            nueva = distancia + millas
            if nueva < distancias[vecino]:
                distancias[vecino] = nueva
                previos[vecino] = puerto
                heapq.heappush(cola, (nueva, vecino))
                actualizados.append([vecino, nueva])
        pasos.append({"puerto": puerto, "distancia": distancia, "actualizados": actualizados})

    return distancias, previos, pasos


def camino(previos, destino):
    """Arma el camino siguiendo los 'previos' desde el destino hacia atrás."""
    puertos = []
    while destino is not None:
        puertos.insert(0, destino)
        destino = previos[destino]
    return puertos
