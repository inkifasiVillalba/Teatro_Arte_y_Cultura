const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

if (!usuario || usuario.rol !== "CLIENTE") {
  window.location.href = "index.html";
}

document.getElementById("btn-volver").addEventListener("click", () => {
  window.location.href = "cartelera.html";
});

async function cargarHistorial() {
  const datos = await fetch(`${API}/clientes/${usuario.id}/historial`).then((r) => r.json());

  const entradas = document.getElementById("lista-entradas");
  entradas.innerHTML = datos.entradas.length === 0 ? "Aún no tienes entradas." : "";
  for (const e of datos.entradas) {
    entradas.innerHTML += `
      <div class="obra">
        <span class="etiqueta">${e.estado} · ${e.codigo}</span>
        <h2>${e.titulo}</h2>
        <p>${e.fecha_hora} · ${e.sala}</p>
        <p>Asiento ${e.asiento} · $${e.precio}</p>
      </div>`;
  }

  const reservas = document.getElementById("lista-reservas");
  reservas.innerHTML = datos.reservas.length === 0 ? "Aún no tienes reservas." : "";
  for (const r of datos.reservas) {
    reservas.innerHTML += `
      <div class="obra">
        <span class="etiqueta">Reserva #${r.id} · ${r.estado}</span>
        <h2>${r.titulo}</h2>
        <p>${r.fecha_hora} · Asientos: ${r.asientos}</p>
        <p>Total: $${r.total}</p>
      </div>`;
  }
}

cargarHistorial();