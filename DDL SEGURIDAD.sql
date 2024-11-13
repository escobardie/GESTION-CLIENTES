
CREATE DATABASE gestion_cliente_agua_v2;
USE gestion_cliente_agua_v2;
SHOW TABLES;


/* DDL CON ENFOQUE EN SEGURIDAD*/
/* creamos un usuario con persimos solo para acceder a la base de datos db_blog*/
/* usuario: user1,  password: user-1 */
CREATE USER 'usuario_agua'@'localhost' identified by 'usuario_agua-1';

GRANT ALL PRIVILEGES ON gestion_cliente_agua_v2.* TO usuario_agua@localhost;
FLUSH PRIVILEGES;

DROP USER 'usuario_agua'@'localhost';

SELECT * FROM cliente_cliente;
SELECT * FROM cliente_promo;
SELECT * FROM cliente_promoporcliente;
SELECT * FROM cliente_visita;
SELECT * FROM cliente_registropago;


SELECT * FROM visitas_visita;

SELECT @@global.time_zone, @@session.time_zone;
SET GLOBAL time_zone = 'America/Argentina/Buenos_Aires';