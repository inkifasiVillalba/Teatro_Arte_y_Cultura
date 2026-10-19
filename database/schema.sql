CREATE DATABASE IF NOT EXISTS teatro_arte_cultura
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE teatro_arte_cultura;

-- ============ USUARIOS (herencia en una sola tabla) ============
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    clave_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    ultimo_acceso DATETIME NULL,
    rol ENUM('CLIENTE', 'EMPLEADO', 'ADMINISTRADOR') NOT NULL,
    telefono VARCHAR(20) NULL,
    cargo VARCHAR(50) NULL,
    nivel_acceso INT NULL
);

-- ============ PROGRAMACIÓN ============
CREATE TABLE obras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL UNIQUE,   -- regla R1: sin títulos duplicados
    genero VARCHAR(50) NOT NULL,
    clasificacion VARCHAR(10) NOT NULL,
    director VARCHAR(100) NOT NULL,
    descripcion TEXT,
    duracion_min INT NOT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    capacidad INT NOT NULL
);

CREATE TABLE asientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT NOT NULL,
    fila VARCHAR(2) NOT NULL,
    numero INT NOT NULL,
    ubicacion VARCHAR(50) NOT NULL DEFAULT 'Platea General',
    UNIQUE (id_sala, fila, numero),
    FOREIGN KEY (id_sala) REFERENCES salas(id)
);

CREATE TABLE funciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_obra INT NOT NULL,
    id_sala INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado ENUM('PROGRAMADA','EN_CURSO','FINALIZADA','CANCELADA')
        NOT NULL DEFAULT 'PROGRAMADA',
    FOREIGN KEY (id_obra) REFERENCES obras(id),
    FOREIGN KEY (id_sala) REFERENCES salas(id)
);

-- ============ CAFETERÍA ============
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    existencias INT NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CHECK (existencias >= 0)               -- regla R7: sin sobreventa
);

-- ============ RESERVAS ============
CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_funcion INT NOT NULL,
    fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('PENDIENTE','CONFIRMADA','CANCELADA','EXPIRADA')
        NOT NULL DEFAULT 'PENDIENTE',
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
    FOREIGN KEY (id_funcion) REFERENCES funciones(id)
);

CREATE TABLE detalle_reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_asiento INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    UNIQUE (id_reserva, id_asiento),
    FOREIGN KEY (id_reserva) REFERENCES reservas(id),
    FOREIGN KEY (id_asiento) REFERENCES asientos(id)
);

-- ============ VENTAS ============
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NULL,                   -- NULL si es venta de mostrador
    id_empleado INT NULL,
    id_reserva INT NULL UNIQUE,            -- si viene de una reserva
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
    FOREIGN KEY (id_empleado) REFERENCES usuarios(id),
    FOREIGN KEY (id_reserva) REFERENCES reservas(id)
);

CREATE TABLE entradas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_funcion INT NOT NULL,
    id_asiento INT NOT NULL,
    codigo VARCHAR(50) NOT NULL UNIQUE,    -- el código que se valida en la puerta
    precio DECIMAL(10,2) NOT NULL,
    estado ENUM('VENDIDA','USADA','ANULADA') NOT NULL DEFAULT 'VENDIDA',
    UNIQUE (id_funcion, id_asiento),       -- un asiento no se vende dos veces
    FOREIGN KEY (id_venta) REFERENCES ventas(id),
    FOREIGN KEY (id_funcion) REFERENCES funciones(id),
    FOREIGN KEY (id_asiento) REFERENCES asientos(id)
);

CREATE TABLE detalle_venta_producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);

CREATE TABLE pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL UNIQUE,
    monto DECIMAL(10,2) NOT NULL,
    metodo ENUM('EFECTIVO','TARJETA','TRANSFERENCIA') NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('PENDIENTE','APROBADO','RECHAZADO','ANULADO')
        NOT NULL DEFAULT 'PENDIENTE',
    FOREIGN KEY (id_venta) REFERENCES ventas(id)
);

-- ============ AUDITORÍA ============
CREATE TABLE registro_operacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    accion VARCHAR(50) NOT NULL,
    detalle TEXT,
    id_usuario INT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);




-- ============ DATOS DE PRUEBA ============

INSERT INTO salas (nombre, capacidad) VALUES
('Sala Principal Gabriel García Márquez', 48),
('Sala Experimental Débora Arango', 32),
('Palco VIP Porfirio Barba Jacob', 24);

INSERT INTO obras (titulo, genero, clasificacion, director, descripcion, duracion_min) VALUES
('El Fantasma de la Ópera', 'MUSICAL', '+12', 'Carlos Mario Restrepo', 'Historia de amor y misterio', 140),
('Hamlet: El Príncipe de Dinamarca', 'TRAGEDIA', '+16', 'Elena Montoya S.', 'La obra maestra de Shakespeare', 120),
('La Casa de Bernarda Alba', 'DRAMA', '+12', 'Marcela Betancur', 'Drama de Lorca', 95),
('El Principito: El Viaje de las Estrellas', 'INFANTIL', 'TP', 'Andrés Felipe Morales', 'Adaptación del clásico', 80),
('Crimen y Misterio en la Mansión Blackwood', 'SUSPENSO', '+16', 'Rodrigo Saldarriaga', 'Un misterio por resolver', 110);

INSERT INTO productos (nombre, categoria, precio, existencias) VALUES
('Palomitas Artesanales Caramelo & Sal Marina (Grande)', 'Snacks', 16000, 42),
('Copa de Vino Tinto Malbec Reserva', 'Bebidas', 24000, 28),
('Café Espresso Colombiano de Origen Especial', 'Bebidas', 8500, 65),
('Chocolates Finos de Autor (Caja 6 bombones)', 'Dulcería', 19000, 8),
('Agua de Manantial con Gas & Rodaja de Cítrico', 'Bebidas', 7000, 50),
('Combo Gala Teatral (2 Copas Vino + Tabla Quesos & Uvas)', 'Combos', 52000, 14);

INSERT INTO funciones (id_obra, id_sala, fecha_hora, precio) VALUES
(1, 1, '2026-10-18 19:00:00', 65000),
(2, 1, '2026-10-19 20:00:00', 55000),
(4, 2, '2026-10-18 16:00:00', 40000),
(3, 2, '2026-10-18 19:30:00', 50000);