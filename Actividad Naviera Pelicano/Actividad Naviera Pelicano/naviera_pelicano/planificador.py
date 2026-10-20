"""Une los tres algoritmos: para cada buque decide qué carga, en qué orden entrega y por dónde navega."""

from algoritmos.dijkstra import camino, dijkstra
from algoritmos.mochila import mochila
from algoritmos.vecino_cercano import vecino_mas_cercano


def construir_grafo(puertos, conexiones):
    """Lista de adyacencia: {"CTG": [("BAQ", 75), ...], ...}. Las rutas marítimas van en los dos sentidos."""
    grafo = {p["id"]: [] for p in puertos}
    for c in conexiones:
        grafo[c["a"]].append((c["b"], c["millas"]))
        grafo[c["b"]].append((c["a"], c["millas"]))
    return grafo


def planificar(puertos, conexiones, rutas, paquetes, base):
    grafo = construir_grafo(puertos, conexiones)

    # Dijkstra desde cada puerto: distancias y caminos más cortos entre todos los puertos
    distancias, caminos, pasos_dijkstra = {}, {}, {}
    for origen in grafo:
        distancias[origen], previos, pasos_dijkstra[origen] = dijkstra(grafo, origen)
        caminos[origen] = {destino: camino(previos, destino) for destino in grafo}

    resultado_rutas = {}
    for ruta in rutas:
        # 1. Mochila: qué paquetes de esta ruta suben al buque
        candidatos = [p for p in paquetes if p["destino"] in ruta["puertos"]]
        a_bordo = mochila(candidatos, ruta["peso_max"], ruta["max_paquetes"])

        # 2. Vecino más cercano: en qué orden se visitan los puertos de esos paquetes
        paradas = [puerto for puerto in ruta["puertos"] if any(p["destino"] == puerto for p in a_bordo)]
        orden, pasos_vecino = vecino_mas_cercano(base, paradas, distancias)

        # 3. Dijkstra: el camino por mar entre cada parada (sale de la base y regresa a ella)
        secuencia = [base, *orden, base] if orden else []
        recorrido = [base] if orden else []
        llegadas = {}
        millas = 0
        for desde, hasta in zip(secuencia, secuencia[1:]):
            millas += distancias[desde][hasta]
            recorrido += caminos[desde][hasta][1:]
            if hasta != base:
                llegadas[hasta] = {"parada": len(llegadas) + 1, "millas": millas, "horas": millas / ruta["nudos"]}

        resultado_rutas[ruta["id"]] = {
            "a_bordo": [p["codigo"] for p in a_bordo],
            "peso": sum(p["peso"] for p in a_bordo),
            "valor": sum(p["valor"] for p in a_bordo),
            "orden": orden,
            "pasos_vecino": pasos_vecino,
            "recorrido": recorrido,
            "llegadas": llegadas,
            "millas": millas,
            "horas": millas / ruta["nudos"],
        }

    return {"distancias": distancias, "caminos": caminos, "pasos_dijkstra": pasos_dijkstra, "rutas": resultado_rutas}
