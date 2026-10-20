# Naviera Pelícano · Simulador de entregas marítimas

Una naviera entrega paquetes por mar desde Cartagena a 11 puertos del Caribe con 4 buques.
**Python** hace los cálculos con tres algoritmos y una **página HTML** los muestra en un mapa.

| Algoritmo | Pregunta que responde |
|-----------|-----------------------|
| Mochila 0/1 | ¿Qué paquetes suben a cada buque sin pasar del máximo de paquetes ni del peso máximo? |
| Vecino más cercano | ¿En qué orden entrega el buque? (siempre va al puerto pendiente más cercano) |
| Dijkstra | ¿Cuál es el camino más corto por mar entre dos puertos? |

## Cómo ejecutarlo

1. Abre la carpeta `naviera_pelicano` en Visual Studio Code.
2. Abre `main.py` y presiona **F5**. Se abre el navegador con el simulador.
3. Para cerrarlo, presiona **Ctrl+C** en la terminal.

No hay que instalar nada: solo Python 3.10 o superior. Para correr las pruebas:

```bash
python -m unittest pruebas -v
```

## Archivos

```
naviera_pelicano/
├── main.py               Arranca el servidor y abre la página
├── datos.py              Puertos, rutas marítimas, buques y paquetes
├── planificador.py       Usa los 3 algoritmos para cada buque
├── algoritmos/
│   ├── dijkstra.py       Camino más corto
│   ├── vecino_cercano.py Orden de entrega
│   └── mochila.py        Qué paquetes suben al buque
├── web/
│   ├── index.html        Estructura de la página
│   ├── estilos.css       Colores y diseño
│   ├── app.js            Dibuja el mapa y las pestañas con los resultados de Python
│   └── costas.json       Costas del Caribe para el mapa (Natural Earth)
└── pruebas.py            Pruebas de los algoritmos
```

## Cómo funciona

1. `main.py` levanta un servidor en `http://localhost:8000`.
2. La página (`web/app.js`) le pide el plan a Python en `/api/plan`.
3. Python (`planificador.py`) ejecuta Dijkstra, la mochila y el vecino más cercano y responde con los resultados.
4. Si en la página cambias la capacidad de un buque o agregas/quitas un paquete, la página manda los datos nuevos
   a Python, que vuelve a calcular todo.

Los cambios hechos en la página no se guardan: al recargar vuelven los datos de `datos.py`.
Para cambiar los datos de forma permanente, edita `datos.py`.

## Resultados con los datos de ejemplo

19 de 26 paquetes a bordo, 8.310 kg, US$ 37.000 en fletes y 7.140 millas náuticas de navegación.
