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