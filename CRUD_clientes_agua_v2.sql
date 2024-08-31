INSERT INTO PROMO ( Nombre_Promo, Valor_Promo, Cant_bidones, Alta_promo, Vencimiento_promo, Estado, Nota)
VALUES ( 'Promo DISPENSER + BIDONES * 10', 15000.00, 10, '2024-08-29', '2024-12-31', TRUE, 'Promoción válida para nuevos clientes.');

INSERT INTO PROMO ( Nombre_Promo, Valor_Promo, Cant_bidones, Alta_promo, Vencimiento_promo, Estado, Nota)
VALUES ( 'Promo DISPENSER + BIDONES * 6', 10000.00, 6, '2024-08-31', '2024-12-31', TRUE, 'Promoción válida para nuevos clientes.');

INSERT INTO PROMO ( Nombre_Promo, Valor_Promo, Cant_bidones, Alta_promo, Vencimiento_promo, Estado, Nota)
VALUES ( 'Promo DISPENSER', 10000.00, 0, '2024-08-29', '2024-12-28', TRUE, 'Promoción sin bidones.');

INSERT INTO CLIENTE (Tipo_Promo, Nombre, Apellido, Telefono, Direccion, Fecha_alta, Fecha_Cobro, Estado)
VALUES (1, 'Juan', 'Pérez', '123456789', 'Av. Siempre Viva 123', '2024-08-29', '2024-09-29', TRUE);
-- Nota: En este ejemplo, Tipo_Promo es 1, que corresponde a la primera promoción que insertamos en la tabla PROMO.

INSERT INTO CLIENTE (Tipo_Promo, Nombre, Apellido, Telefono, Direccion, Fecha_alta, Fecha_Cobro, Estado)
VALUES (2, 'Diego', 'Escobar', '987654321', 'Corrientes 2080', '2024-08-31', '2024-09-29', TRUE);
-- Nota: En este ejemplo, Tipo_Promo es 1, que corresponde a la primera promoción que insertamos en la tabla PROMO.

INSERT INTO PROMO_POR_CLIENTE (ID_Cliente, ID_Promo, Inicio_promo, Fin_promo, Bidones_disponibles, Codigo_dispenser, Estado, Nota)
VALUES (1, 1, '2024-08-29', '2025-02-28', 10, 'DISP001', TRUE, 'Cliente nuevo con promoción verano');
-- Nota: En este caso, ID_Cliente es 1 y ID_Promo es 1, que corresponden a los registros previamente insertados en las tablas CLIENTE y PROMO.

INSERT INTO PROMO_POR_CLIENTE (ID_Cliente, ID_Promo, Inicio_promo, Fin_promo, Bidones_disponibles, Codigo_dispenser, Estado, Nota)
VALUES (3, 2, '2024-08-31', '2025-02-28', 6, 'DISP002', TRUE, 'Cliente nuevo con promoción verano');
-- Nota: En este caso, ID_Cliente es 1 y ID_Promo es 1, que corresponden a los registros previamente insertados en las tablas CLIENTE y PROMO.

INSERT INTO VISITA (ID_Cliente, Fecha_visita, Nota)
VALUES (1, '2024-09-01', 'Primera visita de instalación de dispenser.');
-- Nota: ID_Cliente en ambas tablas se refiere al cliente con ID igual a 1, que es el primer cliente que insertamos.

INSERT INTO REGISTRO_PAGO (ID_Cliente, Fecha, Monto, Comprobante, Nota)
VALUES (1, '2024-09-01', 15000.00, 'COM001', 'Pago en efectivo.');
-- Nota: ID_Cliente en ambas tablas se refiere al cliente con ID igual a 1, que es el primer cliente que insertamos.




SELECT * FROM PROMO;
SELECT * FROM CLIENTE;
SELECT * FROM PROMO_POR_CLIENTE;
SELECT * FROM VISITA;
SELECT * FROM REGISTRO_PAGO;

-- BUSQUEDA PESADA
SELECT 
    c.Nombre,
    c.Apellido,
    c.Telefono,
    c.Direccion,
    c.Fecha_alta,
    c.Fecha_Cobro,
    c.Estado AS Estado_Cliente,
    p.Nombre_Promo,
    p.Valor_Promo,
    p.Cant_bidones,
    p.Alta_promo,
    p.Vencimiento_promo,
    -- p.Codigo_dispenser,
    p.Estado AS Estado_Promo,
    pc.Inicio_promo,
    pc.Fin_promo,
    pc.Codigo_dispenser,
    pc.Bidones_disponibles,
    v.Fecha_visita,
    v.Nota AS Nota_Visita,
    rp.Fecha AS Fecha_Pago,
    rp.Monto AS Monto_Pago,
    rp.Comprobante,
    rp.Nota AS Nota_Pago
FROM 
    CLIENTE c
LEFT JOIN 
    PROMO_POR_CLIENTE pc ON c.ID = pc.ID_Cliente
LEFT JOIN 
    PROMO p ON pc.ID_Promo = p.ID
LEFT JOIN 
    VISITA v ON c.ID = v.ID_Cliente
LEFT JOIN 
    REGISTRO_PAGO rp ON c.ID = rp.ID_Cliente
WHERE 
    c.Nombre = 'Juan' AND c.Apellido = 'Pérez';
-- Joins: La consulta usa LEFT JOIN para asegurarse de que, incluso si el cliente no tiene visitas o registros de pago, la información del cliente y su promoción aún se muestre.


SELECT 
    c.Nombre,
    c.Apellido,
    c.Direccion,
    c.Fecha_Cobro,
    c.Estado AS Estado_Cliente,
    p.Nombre_Promo,
    p.Valor_Promo,
    -- p.Codigo_dispenser,
    pc.Inicio_promo,
    pc.Fin_promo,
    pc.Codigo_dispenser,
    pc.Bidones_disponibles,
    v.Fecha_visita,
    rp.Fecha AS Fecha_Pago,
    rp.Monto AS Monto_Pago,
    rp.Comprobante,
    rp.Nota AS Nota_Pago
FROM 
    CLIENTE c
LEFT JOIN 
    PROMO_POR_CLIENTE pc ON c.ID = pc.ID_Cliente
LEFT JOIN 
    PROMO p ON pc.ID_Promo = p.ID
LEFT JOIN 
    VISITA v ON c.ID = v.ID_Cliente
LEFT JOIN 
    REGISTRO_PAGO rp ON c.ID = rp.ID_Cliente
WHERE 
    c.Nombre = 'diego' AND c.Apellido = 'escobar';
-- Joins: La consulta usa LEFT JOIN para asegurarse de que, incluso si el cliente no tiene visitas o registros de pago, la información del cliente y su promoción aún se muestre.

SELECT 
    c.Nombre,
    c.Apellido,
    c.Direccion,
    c.Fecha_Cobro,
    p.Nombre_Promo,
    p.Valor_Promo,
    pc.Inicio_promo,
    pc.Fin_promo,
    pc.Bidones_disponibles,
    v.Fecha_visita,
    rp.Fecha AS Fecha_Pago,
    rp.Monto AS Monto_Pago,
    rp.Comprobante,
    rp.Nota AS Nota_Pago
FROM 
    CLIENTE c
LEFT JOIN 
    PROMO_POR_CLIENTE pc ON c.ID = pc.ID_Cliente
LEFT JOIN 
    PROMO p ON pc.ID_Promo = p.ID
LEFT JOIN 
    VISITA v ON c.ID = v.ID_Cliente
LEFT JOIN 
    REGISTRO_PAGO rp ON c.ID = rp.ID_Cliente
WHERE 
    c.Nombre = 'Juan' AND c.Apellido = 'Pérez';
-- Joins: La consulta usa LEFT JOIN para asegurarse de que, incluso si el cliente no tiene visitas o registros de pago, la información del cliente y su promoción aún se muestre.


SELECT 
    c.Nombre,
    c.Apellido,
    c.Direccion,
    p.Nombre_Promo,
    p.Valor_Promo,
    pc.Bidones_disponibles,
    v.Fecha_visita
FROM 
    CLIENTE c
LEFT JOIN 
    PROMO_POR_CLIENTE pc ON c.ID = pc.ID_Cliente
LEFT JOIN 
    PROMO p ON pc.ID_Promo = p.ID
LEFT JOIN 
    VISITA v ON c.ID = v.ID_Cliente
WHERE 
    c.Nombre = 'Juan' AND c.Apellido = 'Pérez';
-- Joins: La consulta usa LEFT JOIN para asegurarse de que, incluso si el cliente no tiene visitas o registros de pago, la información del cliente y su promoción aún se muestre.



DELETE FROM CLIENTE 
WHERE Apellido = 'escobar';