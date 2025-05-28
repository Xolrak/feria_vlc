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
CREATE TABLE Hacen (
    id_user INT,
    id_encuesta INT,
    realizada BOOLEAN DEFAULT FALSE,
    correo_enviado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_user, id_encuesta),
    FOREIGN KEY (id_user) REFERENCES Usuarios(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_encuesta) REFERENCES Encuesta(id_encuesta) ON DELETE CASCADE
);
