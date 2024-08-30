CREATE DATABASE gestion_cliente_agua;
USE gestion_cliente_agua;
SHOW TABLES;
-- DROP DATABASE gestion_cliente_agua;

-- 1RO: Crear tabla PROMO
CREATE TABLE PROMO (
    ID INT PRIMARY KEY AUTO_INCREMENT,
	Nombre_Promo VARCHAR(50),
    Valor_Promo DECIMAL(10, 2),
    Cant_bidones INT,
    Alta_promo DATE,
    Vencimiento_promo DATE,
    -- Codigo_dispenser VARCHAR(20),
    Estado BOOLEAN,
    Nota TEXT
);

-- 2DO: Crear tabla CLIENTE
CREATE TABLE CLIENTE (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Tipo_Promo INT,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Telefono VARCHAR(15),
    Direccion VARCHAR(100),
    Fecha_alta DATE,
    Fecha_Cobro DATE,
    Estado BOOLEAN,
    FOREIGN KEY (Tipo_Promo) REFERENCES PROMO(ID)
);

-- 3RO: Crear la tabla PROMO_POR_CLIENTE
CREATE TABLE PROMO_POR_CLIENTE (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ID_Cliente INT,
    ID_Promo INT,
    Inicio_promo DATE,
    Fin_promo DATE,
    Bidones_disponibles INT,
    Codigo_dispenser VARCHAR(20),
    Estado BOOLEAN,
    Nota TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID),
    FOREIGN KEY (ID_Promo) REFERENCES PROMO(ID)
);



-- 4TO: Crear tabla VISITA
CREATE TABLE VISITA (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Fecha_visita DATE,
    Nota TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID)
);


-- 5TO: Crear tabla REGISTRO_PAGO
CREATE TABLE REGISTRO_PAGO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Fecha DATE,
    Monto DECIMAL(10, 2),
    Comprobante VARCHAR(100),
    Nota TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID)
);

