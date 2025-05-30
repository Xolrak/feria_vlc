CREATE DATABASE IF NOT EXISTS FeriaEncuestas
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE Feria;

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    correo_electronico VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(20) NOT NULL,
    apellido_1 VARCHAR(20) NOT NULL,
    apellido_2 VARCHAR(20)
);

-- Tabla de Encuesta
CREATE TABLE Encuesta (
    id_encuesta INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activa BOOLEAN DEFAULT TRUE
);

-- Tabla intermedia Hacen (relación muchos a muchos con estado)
CREATE TABLE IF NOT EXISTS Hacen (
    id_usuario INT,
    id_encuesta INT,
    realizada BOOLEAN DEFAULT FALSE,
    correo_enviado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_usuario, id_encuesta),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_encuesta) REFERENCES Encuesta(id_encuesta) ON DELETE CASCADE
);
