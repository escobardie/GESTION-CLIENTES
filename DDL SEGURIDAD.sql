
CREATE DATABASE gestion_cliente_agua_django;
USE gestion_cliente_agua_django;
SHOW TABLES;


/* DDL CON ENFOQUE EN SEGURIDAD*/
/* creamos un usuario con persimos solo para acceder a la base de datos db_blog*/
/* usuario: user1,  password: user-1 */
CREATE USER 'usuario_agua'@'localhost' identified by 'usuario_agua-1';

GRANT ALL PRIVILEGES ON gestion_cliente_agua_django.* TO usuario_agua@localhost;
FLUSH PRIVILEGES;

DROP USER 'usuario_agua'@'localhost';

SELECT * FROM cliente_cliente;
SELECT * FROM cliente_promo;
SELECT * FROM cliente_promoporcliente;
SELECT * FROM cliente_visita;
SELECT * FROM cliente_registropago;