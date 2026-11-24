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