SELECT * FROM cliente_cliente;
SELECT * FROM cliente_promo;
SELECT * FROM cliente_promoporcliente;
SELECT * FROM cliente_visita;
SELECT * FROM cliente_registropago;


INSERT INTO cliente_promo ( Nombre_Promo, Valor_Promo, Cant_bidones, Alta_promo, Vencimiento_promo, Estado, Nota)
VALUES ( 'Dispenser (SIN BIDONES)', 21000.00, 0, '2024-09-01', '2025-12-31', TRUE, 'Promoción válida para nuevos clientes.');

INSERT INTO cliente_cliente (Tipo_Promo_id, Nombre, Apellido, Telefono, Direccion, Fecha_alta, Fecha_Cobro, Estado)
VALUES (2, 'Diego', 'Escobar', '154078790', 'Corrientes 2080', '2024-09-01', '2024-09-29', TRUE);
-- Nota: En este ejemplo, Tipo_Promo es 1, que corresponde a la primera promoción que insertamos en la tabla PROMO.

INSERT INTO cliente_promoporcliente (cliente_id, promo_id, Inicio_promo, Fin_promo, Bidones_disponibles, Codigo_dispenser, Estado, Nota)
VALUES (2, 2, '2024-08-29', '2025-02-28', 10, 'DISP001', TRUE, 'Cliente nuevo con promoción verano');
-- Nota: En este caso, ID_Cliente es 1 y ID_Promo es 1, que corresponden a los registros previamente insertados en las tablas CLIENTE y PROMO.

INSERT INTO cliente_visita (cliente_id, Fecha_visita, Nota)
VALUES (1, '2024-09-01', 'Primera visita de instalación de dispenser.');
-- Nota: ID_Cliente en ambas tablas se refiere al cliente con ID igual a 1, que es el primer cliente que insertamos.

INSERT INTO cliente_registropago (cliente_id, Fecha, Monto, Comprobante, Nota)
VALUES (1, '2024-09-01', 15000.00, 'COM001', 'Pago en efectivo.');
-- Nota: ID_Cliente en ambas tablas se refiere al cliente con ID igual a 1, que es el primer cliente que insertamos.