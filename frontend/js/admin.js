const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

// Solo el administrador puede entrar aquí
if (!usuario || usuario.rol !== "ADMINISTRADOR") {
  window.location.href = "index.html";
}

document.getElementById("saludo").textContent = `Administrador: ${usuario.nombre}`;

document.getElementById("btn-salir").addEventListener("click", () => {
  sessionStorage.removeItem("usuario");
  window.location.href = "index.html";
});

async function cargarObras() {
  const respuesta = await fetch(`${API}/obras`);
  const obras = await respuesta.json();
  const lista = document.getElementById("lista-obras");
  lista.innerHTML = "";
  for (const obra of obras) {
    lista.innerHTML += `
      <div class="obra">
        <span class="etiqueta">${obra.genero} · ${obra.clasificacion}</span>
        <h2>${obra.titulo}</h2>
        <p>Dirección: ${obra.director} · ${obra.duracion_min} min</p>
      </div>`;
  }
}

document.getElementById("btn-crear").addEventListener("click", async () => {
  const resultado = document.getElementById("resultado");

  const respuesta = await fetch(`${API}/obras`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      titulo: document.getElementById("titulo").value,
      genero: document.getElementById("genero").value,
      clasificacion: document.getElementById("clasificacion").value,
      director: document.getElementById("director").value,
      descripcion: document.getElementById("descripcion").value,
      duracion_min: document.getElementById("duracion").value,
    }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    resultado.style.color = "#ff6b6b";
    resultado.textContent = datos.error;
    return;
  }
  resultado.style.color = "#6bd68a";
  resultado.textContent = `Obra "${datos.titulo}" registrada`;
  cargarObras();
});

cargarObras();