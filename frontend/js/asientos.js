const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));
const idObra = new URLSearchParams(window.location.search).get("obra");

let funcionActual = null;
let elegidos = [];

if (!usuario) window.location.href = "index.html";

document.getElementById("btn-volver").addEventListener("click", () => {
  window.location.href = "cartelera.html";
});



document.getElementById("btn-reservar").addEventListener("click", async () => {
  const resultado = document.getElementById("resultado");

  if (!funcionActual || elegidos.length === 0) {
    resultado.textContent = "Elige una función y al menos un asiento";
    return;
  }

  const respuesta = await fetch(`${API}/reservar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_cliente: usuario.id,
      id_funcion: funcionActual.id,
      asientos: elegidos.map((e) => e.id),
      precio: funcionActual.precio,
    }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    resultado.style.color = "#ff6b6b";
    resultado.textContent = datos.error;
    return;
  }
  resultado.style.color = "#6bd68a";
  resultado.textContent =
    `Reserva #${datos.id_reserva} creada. Total a pagar en taquilla: $${datos.total}`;
  elegirFuncion(funcionActual);   // los reservados quedan grises
});


async function cargarHorarios() {
  const respuesta = await fetch(`${API}/obras/${idObra}/funciones`);
  const funciones = await respuesta.json();
  const contenedor = document.getElementById("horarios");

  if (funciones.length === 0) {
    contenedor.textContent = "Esta obra no tiene funciones programadas.";
    return;
  }

  for (const f of funciones) {
    const boton = document.createElement("button");
    boton.className = "horario";
    boton.textContent = `${f.fecha_hora} · ${f.sala} · $${f.precio}`;
    boton.addEventListener("click", () => elegirFuncion(f));
    contenedor.appendChild(boton);
  }
}

async function elegirFuncion(funcion) {
  funcionActual = funcion;
  elegidos = [];
  actualizarResumen();

  const respuesta = await fetch(`${API}/funciones/${funcion.id}/asientos`);
  const asientos = await respuesta.json();
  const mapa = document.getElementById("mapa");
  mapa.innerHTML = "";

  let filaAnterior = "";
  for (const a of asientos) {
    if (a.fila !== filaAnterior) {
      mapa.appendChild(document.createElement("br"));
      filaAnterior = a.fila;
    }
    const boton = document.createElement("button");
    boton.className = "asiento" + (a.ocupado ? " ocupado" : "");
    boton.textContent = a.codigo;
    boton.disabled = a.ocupado;
    boton.addEventListener("click", () => alternarAsiento(a, boton));
    mapa.appendChild(boton);
  }
}

function alternarAsiento(asiento, boton) {
  const posicion = elegidos.findIndex((e) => e.id === asiento.id);
  if (posicion >= 0) {
    elegidos.splice(posicion, 1);
    boton.classList.remove("elegido");
  } else {
    elegidos.push(asiento);
    boton.classList.add("elegido");
  }
  actualizarResumen();
}

function actualizarResumen() {
  const resumen = document.getElementById("resumen");
  if (elegidos.length === 0) {
    resumen.textContent = "Asientos elegidos: ninguno";
    return;
  }
  const codigos = elegidos.map((e) => e.codigo).join(", ");
  const total = elegidos.length * funcionActual.precio;
  resumen.textContent = `Asientos: ${codigos} · Total: $${total}`;
}


document.getElementById("btn-comprar").addEventListener("click", async () => {
  const resultado = document.getElementById("resultado");

  if (!funcionActual || elegidos.length === 0) {
    resultado.textContent = "Elige una función y al menos un asiento";
    return;
  }

  const respuesta = await fetch(`${API}/comprar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_cliente: usuario.id,
      id_funcion: funcionActual.id,
      asientos: elegidos.map((e) => e.id),
      precio: funcionActual.precio,
      metodo: document.getElementById("metodo").value,
    }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    resultado.textContent = datos.error;
    return;
  }

  resultado.textContent =
    `¡Compra exitosa! Total $${datos.total}. Tus códigos: ${datos.codigos.join(", ")}`;
  elegirFuncion(funcionActual);   // recarga el mapa: los comprados quedan ocupados
});

cargarHorarios();