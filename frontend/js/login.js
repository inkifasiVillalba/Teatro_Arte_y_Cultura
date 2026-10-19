const API = "http://localhost:5000/api";
let rolSeleccionado = "CLIENTE";
let modo = "login";

const mensaje = document.getElementById("mensaje");
const pestanas = document.getElementById("pestanas");
const formLogin = document.getElementById("form-login");
const formRegistro = document.getElementById("form-registro");

function mostrar(texto, tipo) {
  mensaje.textContent = texto;
  mensaje.className = tipo;
}

// El registro solo existe para clientes
function actualizarVista() {
  const esCliente = rolSeleccionado === "CLIENTE";
  pestanas.hidden = !esCliente;
  if (!esCliente) modo = "login";
  formLogin.hidden = modo !== "login";
  formRegistro.hidden = modo !== "registro";
  mostrar("", "");
}

document.querySelectorAll(".rol").forEach((boton) => {
  boton.addEventListener("click", () => {
    document.querySelectorAll(".rol").forEach((b) => b.classList.remove("activo"));
    boton.classList.add("activo");
    rolSeleccionado = boton.dataset.rol;
    actualizarVista();
  });
});

document.querySelectorAll(".pestana").forEach((boton) => {
  boton.addEventListener("click", () => {
    document.querySelectorAll(".pestana").forEach((b) => b.classList.remove("activo"));
    boton.classList.add("activo");
    modo = boton.dataset.modo;
    actualizarVista();
  });
});

async function enviar(ruta, cuerpo) {
  try {
    const respuesta = await fetch(`${API}/${ruta}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cuerpo),
    });
    const datos = await respuesta.json();
    return { ok: respuesta.ok, datos };
  } catch (error) {
    return { ok: false, datos: { error: "No se pudo conectar con el servidor" } };
  }
}

document.getElementById("btn-entrar").addEventListener("click", async () => {
  const { ok, datos } = await enviar("login", {
    correo: document.getElementById("correo").value,
    clave: document.getElementById("clave").value,
    rol: rolSeleccionado,
  });
  if (!ok) return mostrar(datos.error, "error");
    sessionStorage.setItem("usuario", JSON.stringify(datos.usuario));
      if (datos.usuario.rol === "EMPLEADO") {
    window.location.href = "empleado.html";
    } else if (datos.usuario.rol === "ADMINISTRADOR") {
    window.location.href = "admin.html";
  } else {
    window.location.href = "cartelera.html";
  }
});

document.getElementById("btn-registrar").addEventListener("click", async () => {
  const correo = document.getElementById("reg-correo").value;
  const clave = document.getElementById("reg-clave").value;

  const { ok, datos } = await enviar("registro", {
    nombre: document.getElementById("reg-nombre").value,
    correo,
    telefono: document.getElementById("reg-telefono").value,
    clave,
    confirmar: document.getElementById("reg-confirmar").value,
  });
  if (!ok) return mostrar(datos.error, "error");

  // Registro exitoso: pasamos al login con el correo ya escrito
  modo = "login";
  document.querySelectorAll(".pestana").forEach((b) =>
    b.classList.toggle("activo", b.dataset.modo === "login"));
  actualizarVista();
  document.getElementById("correo").value = correo;
  mostrar(`Cuenta creada, ${datos.usuario.nombre}. Ya puedes iniciar sesión.`, "ok");
});