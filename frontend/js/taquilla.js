const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

if (!usuario || usuario.rol !== "EMPLEADO") {
  window.location.href = "index.html";
}

let funciones = [];
let funcionActual = null;
let elegidos = [];

document.getElementById("btn-volver").addEventListener("click", () => {
  window.location.href = "empleado.html";
});

async function cargarFunciones() {
  funciones = await fetch(`${API}/funciones`).then((r) => r.json());
  const select = document.getElementById("funcion");
  select.innerHTML = funciones
    .filter((f) => f.estado === "PROGRAMADA" && new Date(`${f.fecha}T${f.horario.split(" - ")[0]}`) >= new Date())
    .map((f) => {
      const hora = f.horario.split(" - ")[0];
      const sala = f.sala.split(" ")[0] + " " + f.sala.split(" ")[1];
      return `<option value="${f.id}">${f.fecha} ${hora} · ${f.obra} · ${sala}</option>`;
    })
    .join("");
  select.addEventListener("change", elegirFuncion);
  elegirFuncion();
}

async function elegirFuncion() {
  const id = Number(document.getElementById("funcion").value);
  funcionActual = funciones.find((f) => f.id === id);
  elegidos = [];
  actualizarResumen();

  const asientos = await fetch(`${API}/funciones/${id}/asientos`).then((r) => r.json());
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
    boton.addEventListener("click", () => {
      const pos = elegidos.findIndex((e) => e.id === a.id);
      if (pos >= 0) { elegidos.splice(pos, 1); boton.classList.remove("elegido"); }
      else { elegidos.push(a); boton.classList.add("elegido"); }
      actualizarResumen();
    });
    mapa.appendChild(boton);
  }
}

function actualizarResumen() {
  const resumen = document.getElementById("resumen");
  if (!funcionActual || elegidos.length === 0) {
    resumen.textContent = "Asientos: ninguno";
    return;
  }
  const total = elegidos.length * funcionActual.precio;
  resumen.textContent = `Asientos: ${elegidos.map((e) => e.codigo).join(", ")} · Total: $${total}`;
}

document.getElementById("btn-cobrar").addEventListener("click", async () => {
  const resultado = document.getElementById("resultado");
  if (!funcionActual || elegidos.length === 0) {
    resultado.style.color = "#ff6b6b";
    resultado.textContent = "Elige al menos un asiento";
    return;
  }
  const respuesta = await fetch(`${API}/comprar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_cliente: null,
      id_empleado: usuario.id,
      id_funcion: funcionActual.id,
      asientos: elegidos.map((e) => e.id),
      precio: funcionActual.precio,
      metodo: document.getElementById("metodo").value,
    }),
  });
  const datos = await respuesta.json();
  resultado.style.color = respuesta.ok ? "#6bd68a" : "#ff6b6b";
  resultado.textContent = respuesta.ok
    ? `Cobrado $${datos.total}. Códigos: ${datos.codigos.join(", ")}`
    : datos.error;
  if (respuesta.ok) elegirFuncion();
});

cargarFunciones();