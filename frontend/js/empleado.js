const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

if (!usuario || usuario.rol !== "EMPLEADO") {
  window.location.href = "index.html";
}

document.getElementById("saludo").textContent = `Empleado: ${usuario.nombre}`;

document.getElementById("btn-salir").addEventListener("click", () => {
  sessionStorage.removeItem("usuario");
  window.location.href = "index.html";
});

document.getElementById("btn-validar").addEventListener("click", async () => {
  const resultado = document.getElementById("resultado");
  const codigo = document.getElementById("codigo").value;

  const respuesta = await fetch(`${API}/entradas/validar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ codigo }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    resultado.style.color = "#ff6b6b";
    resultado.textContent = datos.error;
    return;
  }
  resultado.style.color = "#6bd68a";
  resultado.textContent = `Entrada ${datos.codigo} válida. Ahora está: ${datos.estado}`;
});


async function cargarReservas() {
  const respuesta = await fetch(`${API}/reservas/pendientes`);
  const reservas = await respuesta.json();
  const lista = document.getElementById("lista-reservas");
  lista.innerHTML = "";

  if (reservas.length === 0) {
    lista.textContent = "No hay reservas pendientes.";
    return;
  }

  for (const r of reservas) {
    lista.innerHTML += `
      <div class="obra">
        <span class="etiqueta">Reserva #${r.id}</span>
        <h2>${r.titulo}</h2>
        <p>${r.cliente} · ${r.telefono || "sin teléfono"}</p>
        <p>${r.fecha_hora} · Asientos: ${r.asientos}</p>
        <p>Total: $${r.total}</p>
        <button class="btn-principal" onclick="cobrarReserva(${r.id})">Cobrar y emitir</button>
        <button onclick="cancelarReserva(${r.id})">Cancelar</button>
      </div>`;
  }
}

async function cobrarReserva(id) {
  const mensaje = document.getElementById("resultado-reservas");
  const respuesta = await fetch(`${API}/reservas/${id}/cobrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_empleado: usuario.id,
      metodo: document.getElementById("metodo-cobro").value,
    }),
  });
  const datos = await respuesta.json();
  mensaje.style.color = respuesta.ok ? "#6bd68a" : "#ff6b6b";
  mensaje.textContent = respuesta.ok
    ? `Cobrado $${datos.total}. Códigos: ${datos.codigos.join(", ")}`
    : datos.error;
  cargarReservas();
}

async function cancelarReserva(id) {
  const mensaje = document.getElementById("resultado-reservas");
  const respuesta = await fetch(`${API}/reservas/${id}/cancelar`, { method: "POST" });
  const datos = await respuesta.json();
  mensaje.style.color = respuesta.ok ? "#6bd68a" : "#ff6b6b";
  mensaje.textContent = respuesta.ok ? datos.mensaje : datos.error;
  cargarReservas();
}

cargarReservas();