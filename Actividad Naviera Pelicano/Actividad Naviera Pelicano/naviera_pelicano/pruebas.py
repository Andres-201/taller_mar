"""Pruebas de los algoritmos. Ejecutar con:  python -m unittest pruebas -v"""

import itertools
import unittest

import datos
from algoritmos.dijkstra import camino, dijkstra
from algoritmos.mochila import mochila
from algoritmos.vecino_cercano import vecino_mas_cercano
from planificador import planificar

GRAFO = {"A": [("B", 4), ("C", 1)], "B": [("A", 4), ("C", 2), ("D", 5)],
         "C": [("A", 1), ("B", 2), ("D", 8)], "D": [("B", 5), ("C", 8)]}


class Pruebas(unittest.TestCase):
    def test_dijkstra(self):
        distancias, previos, _ = dijkstra(GRAFO, "A")
        self.assertEqual(distancias, {"A": 0, "B": 3, "C": 1, "D": 8})
        self.assertEqual(camino(previos, "D"), ["A", "C", "B", "D"])

    def test_vecino_mas_cercano(self):
        distancias = {p: dijkstra(GRAFO, p)[0] for p in GRAFO}
        orden, _ = vecino_mas_cercano("A", ["B", "C", "D"], distancias)
        self.assertEqual(orden, ["C", "B", "D"])

    def test_mochila_igual_a_probar_todas_las_combinaciones(self):
        for ruta in datos.RUTAS:
            candidatos = [p for p in datos.PAQUETES if p["destino"] in ruta["puertos"]]
            mejor = max(sum(p["valor"] for p in combo)
                        for n in range(ruta["max_paquetes"] + 1)
                        for combo in itertools.combinations(candidatos, n)
                        if sum(p["peso"] for p in combo) <= ruta["peso_max"])
            elegidos = mochila(candidatos, ruta["peso_max"], ruta["max_paquetes"])
            self.assertEqual(sum(p["valor"] for p in elegidos), mejor)

    def test_ningun_buque_se_pasa_de_su_capacidad(self):
        plan = planificar(datos.PUERTOS, datos.CONEXIONES, datos.RUTAS, datos.PAQUETES, datos.PUERTO_BASE)
        for ruta in datos.RUTAS:
            resultado = plan["rutas"][ruta["id"]]
            self.assertLessEqual(len(resultado["a_bordo"]), ruta["max_paquetes"])
            self.assertLessEqual(resultado["peso"], ruta["peso_max"])
        self.assertEqual(sum(r["valor"] for r in plan["rutas"].values()), 37000)


if __name__ == "__main__":
    unittest.main()
