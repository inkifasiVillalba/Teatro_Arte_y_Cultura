const API = "http://localhost:5000/api";
const usuario = JSON.parse(sessionStorage.getItem("usuario"));

let obras = [];
let generoActual = "TODOS";

// Si no hay sesión, vuelve al login
if (!usuario) {
  window.location.href = "index.html";
}

document.getElementById("saludo").textContent = `Bienvenido, ${usuario.nombre}`;

document.getElementById("btn-salir").addEventListener("click", () => {
  sessionStorage.removeItem("usuario");
  window.location.href = "index.html";
});

// Dibuja las obras que cumplan el texto y el género elegido
function mostrarObras() {
  const texto = document.getElementById("buscador").value.toLowerCase();
  const lista = document.getElementById("lista-obras");
  lista.innerHTML = "";

  for (const obra of obras) {
    const coincideTexto =
      obra.titulo.toLowerCase().includes(texto) ||
      obra.director.toLowerCase().includes(texto);
    const coincideGenero = generoActual === "TODOS" || obra.genero === generoActual;

    if (coincideTexto && coincideGenero) {
      lista.innerHTML += `
        <div class="obra" onclick="window.location.href='asientos.html?obra=${obra.id}'" style="cursor:pointer">
          <span class="etiqueta">${obra.genero} · ${obra.clasificacion}</span>
          <h2>${obra.titulo}</h2>
          <p>Dirección: ${obra.director}</p>
          <p>${obra.duracion_min} min</p>
        </div>`;
    }
  }
}

document.getElementById("buscador").addEventListener("input", mostrarObras);

document.querySelectorAll(".filtro").forEach((boton) => {
  boton.addEventListener("click", () => {
    document.querySelectorAll(".filtro").forEach((b) => b.classList.remove("activo"));
    boton.classList.add("activo");
    generoActual = boton.dataset.genero;
    mostrarObras();
  });
});

// Pide las obras a la API al cargar la página
async function cargarObras() {
  const respuesta = await fetch(`${API}/obras`);
  obras = await respuesta.json();
  mostrarObras();
}

cargarObras();