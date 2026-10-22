const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

if (!usuario || usuario.rol !== "EMPLEADO") {
  window.location.href = "index.html";
}

// Solo el empleado llega aquí, así que vuelve a su panel
document.getElementById("btn-volver").addEventListener("click", () => {
  window.location.href = "empleado.html";
});


async function cargarProductos() {
  const respuesta = await fetch(`${API}/productos`);
  const productos = await respuesta.json();
  const lista = document.getElementById("lista-productos");
  lista.innerHTML = "";

  for (const p of productos) {
    lista.innerHTML += `
      <div class="obra">
        <span class="etiqueta">${p.categoria} · Stock: ${p.existencias}</span>
        <h2>${p.nombre}</h2>
        <p>$${p.precio}</p>
        <input type="number" id="cant-${p.id}" value="1" min="1">
        <button class="btn-principal" onclick="vender(${p.id})">Vender</button>
      </div>`;
  }
}

async function vender(idProducto) {
  const resultado = document.getElementById("resultado");
  const cantidad = document.getElementById(`cant-${idProducto}`).value;

  const respuesta = await fetch(`${API}/productos/vender`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_producto: idProducto, cantidad }),
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