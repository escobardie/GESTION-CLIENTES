-- Tabla CLIENTE
CREATE TABLE CLIENTE (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Telefono VARCHAR(15),
    Direccion VARCHAR(255),
    Fecha_alta DATE,
    Tipo_Promo VARCHAR(50),
    Fecha_Cobro DATE,
    Estado BOOLEAN
);

-- Tabla PRECIO
CREATE TABLE PRECIO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Monto DECIMAL(10, 2),
    Nota TEXT
);

-- Tabla PROMO
CREATE TABLE PROMO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    ID_Precio INT,
    Tipo_Promo VARCHAR(50),
    Cant_bidones INT,
    Alta_promo DATE,
    Codigo_dispenser VARCHAR(50),
    Estado BOOLEAN,
    Nota TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID),
    FOREIGN KEY (ID_Precio) REFERENCES PRECIO(ID)
);

-- Tabla VISITA
CREATE TABLE VISITA (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Fecha_visita DATE,
    Nota TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID)
);

-- Tabla REGISTRO PAGO
CREATE TABLE REGISTRO_PAGO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Fecha DATE,
    Monto DECIMAL(10, 2),
    Comprobante VARCHAR(255),
    Nota TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID)
);
