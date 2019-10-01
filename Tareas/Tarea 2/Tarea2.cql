CREATE TABLE productos_disponibles(
    nombre TEXT,
    precioU DECIMAL,
    PRIMARY KEY (nombre)
);

CREATE TABLE compras_supermercado(
    idSucursal INT,
    nombre TEXT,
    productos map<TEXT, INT>,
    total DECIMAL,
    fecha TIMESTAMP,
    total_productos INT,
    PRIMARY KEY ((fecha, idSucursal), nombre)
);

INSERT INTO productos_disponibles(nombre, precioU) 
VALUES ('pan', 10.0);
INSERT INTO productos_disponibles(nombre, precioU)
VALUES ('limon', 2.0);
INSERT INTO productos_disponibles(nombre, precioU)
VALUES ('cafe', 53.8);
INSERT INTO productos_disponibles(nombre, precioU)
VALUES ('agua', 6.0);
INSERT INTO productos_disponibles(nombre, precioU)
VALUES ('huevo', 25.9);

INSERT INTO compras_supermercado(idSucursal, nombre, productos, total, fecha)
VALUES (1, 'Laura', {'pan':1, 'limon':2}, 14.0, '2019-01-01', 2);
INSERT INTO compras_supermercado(idSucursal, nombre, productos, total, fecha)
VALUES (1, 'Pedro', {'cafe':1, 'agua':2}, 65.8, '2019-01-02', 2);
INSERT INTO compras_supermercado(idSucursal, nombre, productos, total, fecha)
VALUES (2, 'Juan', {'pan':1, 'limon':2}, 14.0, '2019-01-05', 2);
INSERT INTO compras_supermercado(idSucursal, nombre, productos, total, fecha)
VALUES (2, 'Minerva', {'huevo':1, 'limon':2}, 29.9, '2019-02-01', 2);

SELECT * FROM productos_disponibles;
SELECT * FROM compras_supermercado;

CREATE INDEX ON compras_supermercado(fecha);

SELECT COUNT(*) FROM compras_supermercado WHERE fecha='';
SELECT COUNT(*) FROM compras_supermercado WHERE fecha='' AND idSucursal = ;
SELECT productos FROM compras_supermercado WHERE nombre = '' AND fecha = '' ALLOW FILTERING
SELECT nombre FROM compras_supermercado WHERE fecha = dateof(now()) - 2m; // Apache Cassandra
SELECT total_productos FROM compras_supermercado WHERE fecha = ''
SELECT productos FROM compras_supermercado WHERE fecha = dateof(now()) - 7d // Apache Cassandra

// Documentacion de Apache Cassandra para las operaciones artmeticas de fechas: http://cassandra.apache.org/doc/latest/cql/operators.html


CREATE TABLE clientes(
    tipo_producto TEXT,
    nombre TEXT,
    movimiento TEXT,
    monto DECIMAL,
    medio TEXT,
    fecha TIMESTAMP,
    PRIMARY KEY (tipo_producto, nombre)
);

INSERT INTO clientes(tipo_producto, nombre, movimiento, monto, medio, fecha)
VALUES ('che','Juan','dep',100,'eff','2019-01-05')
INSERT INTO clientes(tipo_producto, nombre, movimiento, monto, medio, fecha)
VALUES ('inv','Maria','ret',2000,'eff','2019-02-10')
INSERT INTO clientes(tipo_producto, nombre, movimiento, monto, medio, fecha)
VALUES ('cre','Tomas','ret',50,'eff','2019-05-11')
INSERT INTO clientes(tipo_producto, nombre, movimiento, monto, medio, fecha)
VALUES ('cre','Maria','dep',5000,'eff','2019-06-15')

SELECT tipo_producto FROM clientes WHERE nombre = '';
SELECT COUNT(*) FROM clientes WHERE tipo_producto = "inv";
SELECT nombre FROM clientes WHERE movimiento IN ('dep', 'ret') AND monto >= ;
SELECT nombre, fecha FROM clientes WHERE monto >= ;
SELECT monto, movimiento FROM clientes WHERE fecha <= '' AND fecha >= '';
SELECT tipo_producto, medio FROM clientes WHERE fecha = '' AND monto >=;