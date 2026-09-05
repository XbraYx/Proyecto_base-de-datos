-- =========================================================
-- DroneTrack - Database Schema
-- =========================================================

CREATE DATABASE IF NOT EXISTS rastreador_drones
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE rastreador_drones;


-- =========================================================
-- TABLE: drones
-- =========================================================

CREATE TABLE IF NOT EXISTS drones (
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
-- TABLE: clientes
-- =========================================================

CREATE TABLE IF NOT EXISTS clientes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    phone VARCHAR(20),

    address VARCHAR(255),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- TABLE: estados_paquete
-- =========================================================

CREATE TABLE IF NOT EXISTS estados_paquete (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(50) NOT NULL UNIQUE,

    description VARCHAR(200)
);


-- =========================================================
-- TABLE: paquetes
-- =========================================================

CREATE TABLE IF NOT EXISTS paquetes (
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
-- TABLE: historial_paquete
-- =========================================================

CREATE TABLE IF NOT EXISTS historial_paquete (
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