-- =========================================================
-- DroneTrack - Database Schema
-- =========================================================

DROP DATABASE IF EXISTS rastreador_drones;

CREATE DATABASE rastreador_drones
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE rastreador_drones;


-- =========================================================
-- USUARIOS
-- =========================================================

CREATE TABLE usuarios (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    email VARCHAR(150) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- CLIENTES
-- =========================================================

CREATE TABLE clientes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    user_id INT UNSIGNED NOT NULL UNIQUE,

    name VARCHAR(100) NOT NULL,

    phone VARCHAR(20),

    address VARCHAR(255),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);


-- =========================================================
-- DRONES
-- =========================================================

CREATE TABLE drones (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    drone_code VARCHAR(30) NOT NULL UNIQUE,

    status ENUM(
        'available',
        'delivering',
        'maintenance'
    ) NOT NULL DEFAULT 'available',

    battery_level TINYINT UNSIGNED NOT NULL DEFAULT 100,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (battery_level <= 100)
);


-- =========================================================
-- ESTADOS DE PAQUETE
-- =========================================================

CREATE TABLE estados_paquete (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(50) NOT NULL UNIQUE,

    description VARCHAR(200)
);


-- =========================================================
-- PAQUETES
-- =========================================================

CREATE TABLE paquetes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    tracking_number VARCHAR(50) NOT NULL UNIQUE,

    client_id INT UNSIGNED NOT NULL,

    origin VARCHAR(255) NOT NULL,

    destination VARCHAR(255) NOT NULL,

    weight_kg DECIMAL(6,2) NOT NULL,

    status_id INT UNSIGNED NOT NULL,

    drone_id INT UNSIGNED NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    estimated_delivery DATETIME NULL,

    delivered_at DATETIME NULL,

    FOREIGN KEY (client_id)
        REFERENCES clientes(id),

    FOREIGN KEY (status_id)
        REFERENCES estados_paquete(id),

    FOREIGN KEY (drone_id)
        REFERENCES drones(id)
);


-- =========================================================
-- HISTORIAL DE PAQUETE
-- =========================================================

CREATE TABLE historial_paquete (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    package_id INT UNSIGNED NOT NULL,

    status_id INT UNSIGNED NOT NULL,

    location VARCHAR(255),

    comment VARCHAR(255),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (package_id)
        REFERENCES paquetes(id),

    FOREIGN KEY (status_id)
        REFERENCES estados_paquete(id)
);


-- =========================================================
-- ESTADOS INICIALES
-- =========================================================

INSERT INTO estados_paquete (name, description)
VALUES
    ('registered', 'El paquete ha sido registrado'),
    ('preparing', 'El paquete se encuentra en preparación'),
    ('delivering', 'El paquete está siendo transportado'),
    ('delivered', 'El paquete fue entregado'),
    ('cancelled', 'El paquete fue cancelado');


-- =========================================================
-- DRONES DE PRUEBA
-- =========================================================

INSERT INTO drones (drone_code, status, battery_level)
VALUES
    ('DRN-001', 'available', 100),
    ('DRN-002', 'available', 95),
    ('DRN-003', 'maintenance', 60);
