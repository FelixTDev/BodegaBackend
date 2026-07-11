-- Limpieza manual de tablas legacy no usadas por el backend actual.
-- Ejecuta este archivo solo despues de correr:
-- 1) 01_backup_canonic_tables.sql
-- 2) 02_diagnose_legacy_tables.sql
-- y de confirmar que no necesitas migrar datos desde las tablas antiguas.

USE camuchita_db;

DROP TABLE IF EXISTS abonos;
DROP TABLE IF EXISTS cuentas_por_cobrar;
DROP TABLE IF EXISTS venta_detalles;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS compra_detalles;
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS caja_movimientos;
DROP TABLE IF EXISTS sesiones_caja;
DROP TABLE IF EXISTS cajas;
DROP TABLE IF EXISTS proveedores;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS movimientos_inventario;
