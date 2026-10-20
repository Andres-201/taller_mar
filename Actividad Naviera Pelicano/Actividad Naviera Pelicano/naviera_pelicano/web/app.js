// Parte visual del simulador. Python (main.py) hace todos los cálculos; este archivo solo los muestra.

// ---------------------------------------------------------------- estado de la página
let datos = null;          // lo que responde Python: puertos, conexiones, rutas, paquetes y el plan calculado
let costas = [];           // polígonos de la costa para dibujar el mapa
let pestana = 'rutas';     // pestaña abierta
let rutaFiltro = 'todas';  // ruta que se resalta en el mapa
let dijOrigen = 'CTG';
let dijDestino = 'HAV';
let puertoElegido = null;  // puerto que se tocó en el mapa

// ---------------------------------------------------------------- utilidades
const $ = (selector) => document.querySelector(selector);
const numero = (n) => Math.round(n).toLocaleString('es-CO');
const horas = (h) => { const t = Math.round(h); return t >= 24 ? `${Math.floor(t / 24)} d ${t % 24} h` : `${t} h`; };
const esc = (texto) => String(texto).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const puerto = (id) => datos.puertos.find((p) => p.id === id);
const nombre = (id) => puerto(id).nombre;
const rutaDe = (idPuerto) => datos.rutas.find((r) => r.puertos.includes(idPuerto));
const textoCamino = (ids) => ids.map(nombre).join(' → ');
const aBordo = (codigo) => Object.values(datos.plan.rutas).some((r) => r.a_bordo.includes(codigo));
const visible = (ruta) => rutaFiltro === 'todas' || rutaFiltro === ruta.id;

// ---------------------------------------------------------------- comunicación con Python
async function pedirPlan(cambios) {
  try {
    const opciones = cambios
      ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cambios) }
      : undefined;
    const respuesta = await fetch('/api/plan', opciones);
    const json = await respuesta.json();
    if (!respuesta.ok) throw new Error(json.error);
    datos = json;
    dibujar();
  } catch (error) {
    $('#panel').innerHTML = `<p class="error">No se pudo calcular (${esc(error.message)}). Abre la página ejecutando «python main.py».</p>`;
  }
}

// Manda a Python las rutas y paquetes actuales para que vuelva a calcular todo
const recalcular = () => pedirPlan({ rutas: datos.rutas, paquetes: datos.paquetes });

// ---------------------------------------------------------------- mapa (proyección de Mercator)
const ANCHO = 1000;
const merc = (lat) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));
const ESCALA = ANCHO / ((29 * Math.PI) / 180);  // el mapa va de 87° O a 58° O (29 grados)
const ALTO = (merc(24.6) - merc(7)) * ESCALA;     // y de 7° N a 24.6° N
const xy = ([lon, lat]) => [((lon + 87) * Math.PI / 180) * ESCALA, (merc(24.6) - merc(lat)) * ESCALA];
const linea = (puntos) => 'M' + puntos.map((p) => xy(p).map((v) => v.toFixed(1)).join(' ')).join(' L');

// Puntos [lon, lat] de un camino que pasa por varios puertos, siguiendo las rutas marítimas
function trazado(ids) {
  const puntos = [];
  for (let i = 0; i < ids.length - 1; i++) {
    const a = ids[i], b = ids[i + 1];
    const c = datos.conexiones.find((c) => (c.a === a && c.b === b) || (c.a === b && c.b === a));
    const tramo = [[puerto(c.a).lon, puerto(c.a).lat], ...c.via, [puerto(c.b).lon, puerto(c.b).lat]];
    if (c.a !== a) tramo.reverse();
    puntos.push(...tramo);
  }
  return puntos;
}

function dibujarMapa() {
  const etiqueta = { n: [0, -11, 'middle'], s: [0, 21, 'middle'], e: [11, 5, 'start'], w: [-11, 5, 'end'], ne: [8, -8, 'start'], nw: [-8, -8, 'end'] };
  let svg = `<rect class="mar" width="${ANCHO}" height="${ALTO}"/>`;
  svg += `<path class="tierra" d="${costas.map((anillo) => linea(anillo) + ' Z').join(' ')}"/>`;

  // Rutas marítimas (aristas del grafo) con sus millas
  for (const c of datos.conexiones) {
    const puntos = trazado([c.a, c.b]).map(xy);
    const a = puntos[Math.floor((puntos.length - 1) / 2)], b = puntos[Math.ceil((puntos.length - 1) / 2)];
    svg += `<path class="conexion" d="${linea(trazado([c.a, c.b]))}"/>`;
    svg += `<text class="millas" x="${(a[0] + b[0]) / 2}" y="${(a[1] + b[1]) / 2 - 3}">${c.millas}</text>`;
  }

  // Recorrido de cada buque (un poco corrido para que no se tapen entre sí)
  datos.rutas.forEach((ruta, i) => {
    const r = datos.plan.rutas[ruta.id];
    if (r.recorrido.length === 0) return;
    const apagada = pestana === 'dijkstra' || !visible(ruta);
    svg += `<path class="recorrido ${apagada ? 'apagada' : ''}" stroke="${ruta.color}" transform="translate(${i * 2.5 - 4} ${i * 2.5 - 4})" d="${linea(trazado(r.recorrido))}"/>`;
  });

  // Camino más corto elegido en la pestaña Dijkstra
  if (pestana === 'dijkstra') {
    svg += `<path class="camino-corto" d="${linea(trazado(datos.plan.caminos[dijOrigen][dijDestino]))}"/>`;
  }

  // Puertos: lleno si el buque para ahí, vacío si no; el número es el orden de parada
  for (const p of datos.puertos) {
    const [x, y] = xy([p.lon, p.lat]);
    const [dx, dy, ancla] = etiqueta[p.etiqueta];
    const esBase = p.id === datos.base;
    const ruta = rutaDe(p.id);
    const color = esBase ? '#10222a' : ruta.color;
    const llegada = esBase ? null : datos.plan.rutas[ruta.id].llegadas[p.id];
    let texto = (llegada ? `${llegada.parada}. ` : '') + p.nombre;
    if (pestana === 'dijkstra') texto = `${p.nombre} · ${numero(datos.plan.distancias[dijOrigen][p.id])} mn`;
    svg += `<g class="puerto" data-puerto="${p.id}">
      <circle cx="${x}" cy="${y}" r="${esBase ? 8 : 6}" fill="${llegada || esBase ? color : 'white'}" stroke="${color}"/>
      <text x="${x + dx}" y="${y + dy}" text-anchor="${ancla}">${texto}</text></g>`;
    if (p.id === puertoElegido && pestana !== 'dijkstra') svg += `<circle class="elegido" cx="${x}" cy="${y}" r="13"/>`;
  }

  $('#mapa').setAttribute('viewBox', `0 0 ${ANCHO} ${ALTO.toFixed(0)}`);
  $('#mapa').innerHTML = svg;
}

// Cuadro con la información del puerto que se tocó en el mapa
function dibujarInfo() {
  if (!puertoElegido) {
    $('#info').innerHTML = '<p class="nota">Toca un puerto del mapa para ver sus paquetes y su camino desde Cartagena.</p>';
    return;
  }
  const p = puerto(puertoElegido);
  if (p.id === datos.base) {
    $('#info').innerHTML = `<h3>${p.nombre} <small>puerto base</small></h3>` + datos.rutas.map((ruta) => {
      const r = datos.plan.rutas[ruta.id];
      return `<p>${ruta.buque} (${ruta.nombre}): ${r.orden.length ? `${numero(r.millas)} mn, ${horas(r.horas)}` : 'no zarpa'}</p>`;
    }).join('');
    return;
  }
  const ruta = rutaDe(p.id);
  const llegada = datos.plan.rutas[ruta.id].llegadas[p.id];
  const paquetes = datos.paquetes.filter((q) => q.destino === p.id);
  $('#info').innerHTML = `<h3>${p.nombre} <small>${p.pais}</small></h3>
    <p>${ruta.nombre} · ${llegada ? `parada ${llegada.parada}, llega en ${horas(llegada.horas)}` : 'sin entregas en este viaje'}</p>
    <p class="nota">Camino más corto desde Cartagena (Dijkstra): ${numero(datos.plan.distancias[datos.base][p.id])} mn ·
      ${textoCamino(datos.plan.caminos[datos.base][p.id])}</p>
    ${paquetes.map((q) => `<p>${aBordo(q.codigo) ? '<span class="si">✓ a bordo</span>' : '<span class="no">✕ en espera</span>'}
      ${esc(q.nombre)} · ${numero(q.peso)} kg · US$ ${numero(q.valor)}</p>`).join('') || '<p class="nota">No hay paquetes para este puerto.</p>'}`;
}

// ---------------------------------------------------------------- pestañas
function panelRutas() {
  return datos.rutas.filter(visible).map((ruta) => {
    const r = datos.plan.rutas[ruta.id];
    const itinerario = r.orden.length
      ? `Cartagena → ${r.orden.map((id) => `${nombre(id)} (${horas(r.llegadas[id].horas)})`).join(' → ')} → Cartagena`
      : 'No zarpa: ningún paquete cabe con esta capacidad.';
    return `<div class="tarjeta" style="border-left-color:${ruta.color}">
      <h3 style="color:${ruta.color}">${ruta.nombre}</h3>
      <p class="nota">Buque ${ruta.buque} · puertos: ${ruta.puertos.map(nombre).join(', ')}</p>
      <p>Paquetes: <b>${r.a_bordo.length} / ${ruta.max_paquetes}</b> <progress max="${ruta.max_paquetes}" value="${r.a_bordo.length}"></progress>
         &nbsp; Peso: <b>${numero(r.peso)} / ${numero(ruta.peso_max)} kg</b> <progress max="${ruta.peso_max}" value="${r.peso}"></progress></p>
      <p>Fletes a bordo: <b>US$ ${numero(r.valor)}</b> · Recorrido: <b>${numero(r.millas)} mn</b> · ${horas(r.horas)} a ${ruta.nudos} nudos</p>
      <p>${itinerario}</p>
      <div class="campos">
        <label>Máx. paquetes <input type="number" min="1" max="20" value="${ruta.max_paquetes}" data-ruta="${ruta.id}" data-campo="max_paquetes"></label>
        <label>Peso máximo (kg) <input type="number" min="100" step="50" value="${ruta.peso_max}" data-ruta="${ruta.id}" data-campo="peso_max"></label>
        <label>Velocidad (nudos) <input type="number" min="5" max="30" value="${ruta.nudos}" data-ruta="${ruta.id}" data-campo="nudos"></label>
      </div>
    </div>`;
  }).join('') + '<button data-accion="ejemplo">Volver a los datos de ejemplo</button>';
}

function panelPaquetes() {
  const destinos = datos.rutas.map((r) => r.puertos.map((id) => `<option value="${id}">${nombre(id)} · ${r.nombre}</option>`).join('')).join('');
  const filas = datos.paquetes.filter((p) => visible(rutaDe(p.destino))).map((p) => `<tr>
      <td>${p.codigo}</td><td>${esc(p.nombre)}</td><td>${nombre(p.destino)}</td><td>${rutaDe(p.destino).nombre}</td>
      <td>${numero(p.peso)} kg</td><td>US$ ${numero(p.valor)}</td>
      <td>${aBordo(p.codigo) ? '<span class="si">A bordo</span>' : '<span class="no">En espera</span>'}</td>
      <td><button data-quitar="${p.codigo}">Quitar</button></td></tr>`).join('');
  return `<div class="tarjeta">
      <h3>Agregar paquete</h3>
      <form id="nuevo">
        <label>Nombre <input name="nombre" required maxlength="60"></label>
        <label>Destino <select name="destino">${destinos}</select></label>
        <label>Peso (kg) <input name="peso" type="number" min="1" required></label>
        <label>Flete (US$) <input name="valor" type="number" min="0" required></label>
        <button>Agregar</button>
      </form>
    </div>
    <table><tr><th>Código</th><th>Paquete</th><th>Destino</th><th>Ruta</th><th>Peso</th><th>Flete</th><th>Estado</th><th></th></tr>${filas}</table>`;
}

function panelMochila() {
  return `<div class="formula">Mejor valor = máx( no llevar el paquete,  valor del paquete + mejor valor con lo que queda )
Límites de cada buque: peso máximo y cantidad máxima de paquetes</div>` +
    datos.rutas.filter(visible).map((ruta) => {
      const r = datos.plan.rutas[ruta.id];
      const candidatos = datos.paquetes.filter((p) => ruta.puertos.includes(p.destino));
      return `<div class="tarjeta" style="border-left-color:${ruta.color}">
        <h3 style="color:${ruta.color}">${ruta.nombre}</h3>
        <p class="nota">Límite: ${ruta.max_paquetes} paquetes y ${numero(ruta.peso_max)} kg</p>
        <table><tr><th>Paquete</th><th>Peso</th><th>Flete</th><th>Decisión</th></tr>
          ${candidatos.map((p) => `<tr><td>${esc(p.nombre)}</td><td>${numero(p.peso)} kg</td><td>US$ ${numero(p.valor)}</td>
            <td>${r.a_bordo.includes(p.codigo) ? '<span class="si">✓ Sube</span>' : '<span class="no">✕ Espera</span>'}</td></tr>`).join('')}
        </table>
        <p>Mejor combinación: <b>${r.a_bordo.length} paquetes, ${numero(r.peso)} kg, US$ ${numero(r.valor)}</b></p>
      </div>`;
    }).join('');
}

function panelVecino() {
  return datos.rutas.filter(visible).map((ruta) => {
    const r = datos.plan.rutas[ruta.id];
    const pasos = r.pasos_vecino.map((paso) => `<li>Desde <b>${nombre(paso.desde)}</b> puede ir a:
        ${Object.entries(paso.opciones).map(([id, millas]) => `${nombre(id)} (${numero(millas)} mn)`).join(', ')}
        → va a <b>${nombre(paso.elegido)}</b>, el más cercano.</li>`).join('');
    return `<div class="tarjeta" style="border-left-color:${ruta.color}">
      <h3 style="color:${ruta.color}">${ruta.nombre}</h3>
      ${r.orden.length ? `<ol>${pasos}<li>No quedan puertos: regresa a Cartagena.</li></ol>
        <p>Orden final: <b>${textoCamino([datos.base, ...r.orden, datos.base])}</b> · ${numero(r.millas)} mn</p>`
        : '<p class="nota">No zarpa, no hay paradas que ordenar.</p>'}
    </div>`;
  }).join('');
}

function panelDijkstra() {
  const opciones = (elegido) => datos.puertos.map((p) => `<option value="${p.id}" ${p.id === elegido ? 'selected' : ''}>${p.nombre}</option>`).join('');
  const pasos = datos.plan.pasos_dijkstra[dijOrigen].map((paso, i) => `<tr>
      <td>${i + 1}</td><td>${nombre(paso.puerto)}</td><td>${numero(paso.distancia)} mn</td>
      <td>${paso.actualizados.map(([id, millas]) => `${nombre(id)} = ${numero(millas)}`).join(', ') || '—'}</td></tr>`).join('');
  return `<div class="tarjeta">
      <div class="campos">
        <label>Origen <select id="origen">${opciones(dijOrigen)}</select></label>
        <label>Destino <select id="destino">${opciones(dijDestino)}</select></label>
      </div>
      <p class="resultado">${numero(datos.plan.distancias[dijOrigen][dijDestino])} mn</p>
      <p>${textoCamino(datos.plan.caminos[dijOrigen][dijDestino])}</p>
      <p class="nota">Toca un puerto del mapa para elegirlo como destino.</p>
    </div>
    <h3>Paso a paso desde ${nombre(dijOrigen)}</h3>
    <table><tr><th>#</th><th>Puerto visitado</th><th>Distancia</th><th>Vecinos con nueva distancia (mn)</th></tr>${pasos}</table>`;
}

// ---------------------------------------------------------------- dibujar toda la página
function dibujar() {
  const rutas = Object.values(datos.plan.rutas);
  const suma = (campo) => rutas.reduce((total, r) => total + r[campo], 0);
  const cargados = rutas.reduce((total, r) => total + r.a_bordo.length, 0);
  $('#resumen').innerHTML = `
    <div class="dato"><span>A bordo</span><b>${cargados} / ${datos.paquetes.length}</b></div>
    <div class="dato"><span>Peso a bordo</span><b>${numero(suma('peso'))} kg</b></div>
    <div class="dato"><span>Fletes a bordo</span><b>US$ ${numero(suma('valor'))}</b></div>
    <div class="dato"><span>Navegación total</span><b>${numero(suma('millas'))} mn</b></div>`;

  $('#filtros').innerHTML = [{ id: 'todas', nombre: 'Todas las rutas' }, ...datos.rutas].map((r) =>
    `<button data-filtro="${r.id}" class="${rutaFiltro === r.id ? 'activo' : ''}">${r.nombre}</button>`).join('');
  document.querySelectorAll('[data-pestana]').forEach((b) => b.classList.toggle('activo', b.dataset.pestana === pestana));

  const paneles = { rutas: panelRutas, paquetes: panelPaquetes, mochila: panelMochila, vecino: panelVecino, dijkstra: panelDijkstra };
  $('#panel').innerHTML = paneles[pestana]();
  dibujarMapa();
  dibujarInfo();
}

// ---------------------------------------------------------------- eventos
document.addEventListener('click', (e) => {
  const boton = e.target.closest('[data-pestana], [data-filtro], [data-quitar], [data-puerto], [data-accion]');
  if (!boton) return;
  if (boton.dataset.pestana) pestana = boton.dataset.pestana;
  if (boton.dataset.filtro) rutaFiltro = boton.dataset.filtro;
  if (boton.dataset.accion === 'ejemplo') return pedirPlan();  // sin cambios: Python devuelve los datos de datos.py
  if (boton.dataset.quitar) {
    datos.paquetes = datos.paquetes.filter((p) => p.codigo !== boton.dataset.quitar);
    return recalcular();
  }
  if (boton.dataset.puerto) {
    if (pestana === 'dijkstra') dijDestino = boton.dataset.puerto;
    else puertoElegido = boton.dataset.puerto;
  }
  dibujar();
});

document.addEventListener('change', (e) => {
  const campo = e.target;
  if (campo.dataset.campo) {  // cambió la capacidad de un buque
    const ruta = datos.rutas.find((r) => r.id === campo.dataset.ruta);
    ruta[campo.dataset.campo] = Math.max(Number(campo.min), Math.round(Number(campo.value)) || Number(campo.min));
    recalcular();
  }
  if (campo.id === 'origen') { dijOrigen = campo.value; dibujar(); }
  if (campo.id === 'destino') { dijDestino = campo.value; dibujar(); }
});

document.addEventListener('submit', (e) => {  // agregar un paquete
  e.preventDefault();
  const f = new FormData(e.target);
  const ultimo = Math.max(500, ...datos.paquetes.map((p) => Number(p.codigo.replace('PK-', '')) || 0));
  datos.paquetes.push({
    codigo: `PK-${ultimo + 1}`,
    nombre: f.get('nombre').trim(),
    destino: f.get('destino'),
    peso: Math.round(Number(f.get('peso'))),
    valor: Math.round(Number(f.get('valor'))),
  });
  recalcular();
});

// ---------------------------------------------------------------- inicio: cargar la costa y pedir el plan a Python
fetch('costas.json')
  .then((respuesta) => respuesta.json())
  .then((json) => { costas = json.poligonos; pedirPlan(); })
  .catch(() => { $('#panel').innerHTML = '<p class="error">Abre la página ejecutando «python main.py».</p>'; });
