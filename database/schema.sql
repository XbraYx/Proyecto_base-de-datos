CREATE DATABASE IF NOT EXISTS rastreador_drones
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE rastreador_drones;

CREATE TABLE IF NOT EXISTS drones (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  drone_code VARCHAR(30) NOT NULL UNIQUE,
  status ENUM('available', 'delivering', 'maintenance') NOT NULL DEFAULT 'available',
  battery_level TINYINT UNSIGNED NOT NULL DEFAULT 100,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (battery_level <= 100)
);