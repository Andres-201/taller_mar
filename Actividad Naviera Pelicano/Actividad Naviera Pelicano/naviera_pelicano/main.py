"""Naviera Pelícano. Ejecuta este archivo (F5 en VS Code o «python main.py») y se abre el simulador en el navegador.

Python hace los cálculos; la página de la carpeta web/ solo los muestra.
La página le pide los resultados a este pequeño servidor en la dirección /api/plan.
"""

import json
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import datos
from planificador import planificar

CARPETA_WEB = Path(__file__).parent / "web"
PUERTO = 8000


def calcular(rutas, paquetes):
    """Ejecuta los algoritmos y junta los datos con los resultados para enviarlos a la página."""
    plan = planificar(datos.PUERTOS, datos.CONEXIONES, rutas, paquetes, datos.PUERTO_BASE)
    return {"base": datos.PUERTO_BASE, "puertos": datos.PUERTOS, "conexiones": datos.CONEXIONES,
            "rutas": rutas, "paquetes": paquetes, "plan": plan}


class Servidor(SimpleHTTPRequestHandler):
    # Tipos de archivo explícitos: en algunos Windows los .js se anuncian mal y el navegador no los ejecuta
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".html": "text/html; charset=utf-8",
                      ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(CARPETA_WEB), **kwargs)  # los archivos se sirven desde web/

    def do_GET(self):
        if self.path == "/api/plan":  # al abrir la página: datos de ejemplo de datos.py
            self.responder(calcular(datos.RUTAS, datos.PAQUETES))
        else:
            super().do_GET()  # index.html, estilos.css, app.js, costas.json

    def do_POST(self):  # cuando cambias algo en la página, llegan las rutas y paquetes nuevos
        try:
            cuerpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            self.responder(calcular(cuerpo["rutas"], cuerpo["paquetes"]))
        except (KeyError, TypeError, ValueError) as error:
            self.responder({"error": f"Datos no válidos: {error}"}, estado=400)

    def responder(self, contenido, estado=200):
        texto = json.dumps(contenido, ensure_ascii=False).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(texto)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # al recargar siempre se ve la última versión
        super().end_headers()

    def log_message(self, *args):
        pass  # no llenar la terminal con cada petición


if __name__ == "__main__":
    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", PUERTO), Servidor)
    except OSError:
        raise SystemExit(f"El puerto {PUERTO} está ocupado: quizá el simulador ya está abierto en otra terminal.")
    print(f"Simulador abierto en http://localhost:{PUERTO}  (Ctrl+C para cerrarlo)")
    webbrowser.open(f"http://localhost:{PUERTO}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("Simulador cerrado.")
