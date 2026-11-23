const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

if (!usuario || usuario.rol !== "EMPLEADO") {
  window.location.href = "index.html";
}

// Solo el empleado llega aquí, así que vuelve a su panel
document.getElementById("btn-volver").addEventListener("click", () => {
  window.location.href = "empleado.html";
});

function iconoProducto(nombre) {
  const n = nombre.toLowerCase();
  if (n.includes("combo")) return "🎟️";
  if (n.includes("crispeta")) return "🍿";
  if (n.includes("gaseosa")) return "🥤";
  if (n.includes("café")) return "☕";
  if (n.includes("chocolat")) return "🍫";
  if (n.includes("agua")) return "💧";
  if (n.includes("perro")) return "🌭";
  if (n.includes("nacho")) return "🧀";
  return "🍽️";
}

async function cargarProductos() {
  const respuesta = await fetch(`${API}/productos`);
  const productos = await respuesta.json();
  const lista = document.getElementById("lista-productos");
  lista.innerHTML = "";

  for (const p of productos) {
    lista.innerHTML += `
      <div class="producto">
        <div>
          <span>${iconoProducto(p.nombre)} ${p.nombre}</span>
          ${p.bajo_stock ? '<span class="alerta">Stock bajo</span>' : ''}<br>
          <small>Stock: ${p.existencias} | $${Number(p.precio).toLocaleString("es-CO")}</small>
        </div>
        <div class="producto-accion">
          <input type="number" id="cant-${p.id}" value="1" min="1">
          <button class="btn-principal" onclick="vender(${p.id})">Vender</button>
        </div>
      </div>`;
  }
}

async function vender(idProducto) {
  const resultado = document.getElementById("resultado");
  const cantidad = document.getElementById(`cant-${idProducto}`).value;

  const respuesta = await fetch(`${API}/productos/vender`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_producto: idProducto, cantidad, id_empleado: usuario.id }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    resultado.style.color = "#ff6b6b";
    resultado.textContent = datos.error;
    return;
  }
  resultado.style.color = "#6bd68a";
  resultado.textContent =
    `Vendido: ${datos.cantidad} x ${datos.producto}. Total $${datos.total}. Quedan ${datos.existencias}.`;
  cargarProductos();   // refresca el stock en pantalla
}

cargarProductos();