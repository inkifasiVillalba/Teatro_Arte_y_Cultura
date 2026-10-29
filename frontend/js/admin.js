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

// ---------- Obras ----------
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
        <button onclick="desactivarObra(${obra.id})">Desactivar</button>
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

async function desactivarObra(id) {
  const mensaje = document.getElementById("resultado");
  const respuesta = await fetch(`${API}/obras/${id}/desactivar`, { method: "POST" });
  const datos = await respuesta.json();
  mensaje.style.color = respuesta.ok ? "#6bd68a" : "#ff6b6b";
  mensaje.textContent = respuesta.ok ? datos.mensaje : datos.error;
  cargarObras();
}

// ---------- Pestañas ----------
document.querySelectorAll(".tab").forEach((boton) => {
  boton.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("activo"));
    boton.classList.add("activo");
    for (const nombre of ["dashboard", "obras", "programar", "inventario","usuarios"]) {
      document.getElementById(`seccion-${nombre}`).hidden = boton.dataset.seccion !== nombre;
    }
    if (boton.dataset.seccion === "dashboard") cargarDashboard();
    if (boton.dataset.seccion === "programar") cargarProgramacion();
    if (boton.dataset.seccion === "inventario") cargarInventario();
    if (boton.dataset.seccion === "usuarios") cargarUsuarios();
  });
});

// ---------- Programar funciones ----------
async function cargarProgramacion() {
  const [obras, salas, funciones] = await Promise.all([
    fetch(`${API}/obras`).then((r) => r.json()),
    fetch(`${API}/salas`).then((r) => r.json()),
    fetch(`${API}/funciones`).then((r) => r.json()),
  ]);

  document.getElementById("f-obra").innerHTML =
    obras.map((o) => `<option value="${o.id}">${o.titulo} (${o.duracion_min} min)</option>`).join("");
  document.getElementById("f-sala").innerHTML =
    salas.map((s) => `<option value="${s.id}">${s.nombre} (${s.capacidad} asientos)</option>`).join("");
  document.getElementById("tabla-funciones").innerHTML = funciones
    .map((f) => `
      <tr>
        <td>${f.obra}</td><td>${f.sala}</td><td>${f.fecha}</td>
        <td>${f.horario}</td><td>$${f.precio}</td>
        <td>${f.ocupacion}</td><td>${f.estado}</td>
      </tr>`)
    .join("");
}

document.getElementById("btn-programar").addEventListener("click", async () => {
  const mensaje = document.getElementById("resultado-funcion");
  const respuesta = await fetch(`${API}/funciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_obra: document.getElementById("f-obra").value,
      id_sala: document.getElementById("f-sala").value,
      fecha_hora: document.getElementById("f-fecha").value,
      precio: document.getElementById("f-precio").value,
    }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    mensaje.style.color = "#ff6b6b";
    mensaje.textContent = datos.error;
    return;
  }
  mensaje.style.color = "#6bd68a";
  mensaje.textContent = `Función de "${datos.obra}" programada en ${datos.sala}`;
  cargarProgramacion();
});

// ---------- Inventario ----------
async function cargarInventario() {
  const productos = await fetch(`${API}/productos`).then((r) => r.json());
  const lista = document.getElementById("lista-inventario");
  lista.innerHTML = "";
  for (const p of productos) {
    lista.innerHTML += `
      <div class="obra">
        <span class="etiqueta">${p.categoria}</span>
        <h2>${p.nombre}</h2>
        <p>Stock disponible: ${p.existencias} uds · Mínimo: ${p.stock_minimo}
          ${p.bajo_stock ? '<span class="alerta">Stock bajo</span>' : ''}</p>
        <button onclick="ajustarStock(${p.id}, -5)">-5</button>
        <button class="btn-principal" onclick="ajustarStock(${p.id}, 10)">+10</button>
      </div>`;
  }
}

async function ajustarStock(id, cambio) {
  const mensaje = document.getElementById("resultado-inventario");
  const respuesta = await fetch(`${API}/productos/ajustar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_producto: id, cambio }),
  });
  const datos = await respuesta.json();
  mensaje.style.color = respuesta.ok ? "#6bd68a" : "#ff6b6b";
  mensaje.textContent = respuesta.ok ? `Nuevo stock: ${datos.existencias}` : datos.error;
  cargarInventario();
}

// ---------- Dashboard ----------
const pesos = (n) => "$ " + Number(n).toLocaleString("es-CO");

async function cargarDashboard() {
  const d = await fetch(`${API}/dashboard`).then((r) => r.json());

  document.getElementById("kpis").innerHTML = `
    <div class="kpi"><span class="etiqueta">Ventas totales</span><strong>${pesos(d.ventas_totales)}</strong><small>${d.transacciones} transacciones validadas</small></div>
    <div class="kpi"><span class="etiqueta">Boletas vendidas</span><strong>${d.boletas}</strong><small>${d.funciones_activas} funciones activas</small></div>
    <div class="kpi"><span class="etiqueta">Ventas cafetería</span><strong>${d.cafeteria_uds} uds</strong><small>Inventario descontado en tiempo real</small></div>`;

  document.getElementById("ocupacion-salas").innerHTML = d.salas
    .map((s) => `
      <div class="obra">
        <h2>${s.nombre}</h2>
        <div class="barra"><div class="barra-llena" style="width: ${s.porcentaje}%"></div></div>
        <p>${s.porcentaje}% ocupada · ${s.vendidos} asientos vendidos de ${s.cupos}
           (capacidad ${s.capacidad}, ${s.funciones} funciones)</p>
      </div>`)
    .join("");

  document.getElementById("tabla-alertas").innerHTML = d.inventario
    .map((p) => `
      <tr>
        <td>${p.nombre}</td><td>${p.existencias} uds</td><td>${p.stock_minimo} uds</td>
        <td>${p.bajo_stock ? '<span class="alerta">Stock bajo</span>' : '<span class="ok">En stock</span>'}</td>
      </tr>`)
    .join("");
}


// ---------- Usuarios (empleados y administradores) ----------
async function cargarUsuarios() {
  const respuesta = await fetch(`${API}/usuarios?id_admin=${usuario.id}`);
  const usuarios = await respuesta.json();
  if (!respuesta.ok) return;
  document.getElementById("tabla-usuarios").innerHTML = usuarios
    .map((u) => `
      <tr>
        <td>${u.nombre}</td><td>${u.correo}</td><td>${u.rol}</td>
        <td>${u.detalle}</td><td>${u.ultimo_acceso}</td>
        <td>${u.activo ? '<span class="ok">ACTIVO</span>' : '<span class="error">INACTIVO</span>'}</td>
      </tr>`)
    .join("");
}


function ajustarCampoCargo() {
  const esEmpleado = document.getElementById("u-rol").value === "EMPLEADO";
  document.getElementById("u-cargo").hidden = !esEmpleado;
}
document.getElementById("u-rol").addEventListener("change", ajustarCampoCargo);
ajustarCampoCargo();

document.getElementById("btn-crear-usuario").addEventListener("click", async () => {
  const mensaje = document.getElementById("resultado-usuario");
  const respuesta = await fetch(`${API}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_admin: usuario.id,
      nombre: document.getElementById("u-nombre").value,
      correo: document.getElementById("u-correo").value,
      rol: document.getElementById("u-rol").value,
      cargo: document.getElementById("u-cargo").value,
      clave: document.getElementById("u-clave").value,
      confirmar: document.getElementById("u-confirmar").value,
    }),
  });
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    mensaje.style.color = "#ff6b6b";
    mensaje.textContent = datos.error;
    return;
  }
  mensaje.style.color = "#6bd68a";
  mensaje.textContent = `${datos.rol} "${datos.nombre}" registrado`;
  for (const id of ["u-nombre", "u-correo", "u-cargo", "u-clave", "u-confirmar"]) {
    document.getElementById(id).value = "";
  }
  cargarUsuarios();
});

cargarObras();
cargarDashboard();