SELECT * FROM cliente_cliente;
SELECT * FROM cliente_promo;
SELECT * FROM cliente_promoporcliente;
SELECT * FROM cliente_visita;
SELECT * FROM cliente_registropago;


-- Borrar los datos de la tabla
DELETE FROM cliente_promo;

-- Reiniciar el contador de AUTO_INCREMENT a 1
ALTER TABLE cliente_registropago AUTO_INCREMENT = 1;


-- Inserta un nuevo registro en la tabla cliente_promo
INSERT INTO cliente_promo (nombre_promo, valor_promo, cant_bidones, alta_promo, vencimiento_promo, estado, nota)
VALUES ('DISPENSER CON 6 BIDONES', 21000.00, 6, '2024-09-01', '2024-12-31', 1, 'Promoción válida para compras durante el verano.');

INSERT INTO cliente_promo (nombre_promo, valor_promo, cant_bidones, alta_promo, vencimiento_promo, estado, nota)
VALUES ('DISPENSER CON 10 BIDONES', 22000.00, 10, '2024-09-01', '2024-12-31', 1, 'Promoción válida para compras durante el verano.');

INSERT INTO cliente_promo (nombre_promo, valor_promo, cant_bidones, alta_promo, vencimiento_promo, estado, nota)
VALUES ('DISPENSER CON 4 BIDONES', 20000.00, 4, '2024-09-01', '2024-12-31', 1, 'Promoción válida para compras durante el verano.');

INSERT INTO cliente_promo (nombre_promo, valor_promo, cant_bidones, alta_promo, vencimiento_promo, estado, nota)
VALUES ('DISPENSER SIN BIDONES', 15000.00, 0, '2024-09-01', '2024-12-31', 1, 'Promoción válida para compras durante el verano.');


SELECT * FROM cliente_ventaproducto;
SELECT * FROM cliente_venta;
SELECT * FROM cliente_producto;


SELECT V.id AS venta_id, C.nombre AS cliente, P.nombre_producto AS producto, VP.cantidad, VP.precio_unidad_venta, VP.precio_total_venta, V.fecha_venta
FROM cliente_ventaproducto VP
JOIN cliente_venta V ON VP.venta_id = V.id
LEFT JOIN cliente_cliente C ON V.cliente_id = C.id
JOIN cliente_producto P ON VP.producto_id = P.id;
