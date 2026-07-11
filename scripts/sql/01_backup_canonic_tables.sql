-- Respaldo manual de las tablas canonicas usadas por el backend actual.
-- Ajusta el nombre de la base de respaldo antes de ejecutar en MySQL.

CREATE DATABASE IF NOT EXISTS camuchita_db_backup_20260708;

CREATE TABLE camuchita_db_backup_20260708.users AS
SELECT * FROM camuchita_db.users;

CREATE TABLE camuchita_db_backup_20260708.categories AS
SELECT * FROM camuchita_db.categories;

CREATE TABLE camuchita_db_backup_20260708.products AS
SELECT * FROM camuchita_db.products;

CREATE TABLE camuchita_db_backup_20260708.clients AS
SELECT * FROM camuchita_db.clients;

CREATE TABLE camuchita_db_backup_20260708.suppliers AS
SELECT * FROM camuchita_db.suppliers;

CREATE TABLE camuchita_db_backup_20260708.caja_boxes AS
SELECT * FROM camuchita_db.caja_boxes;

CREATE TABLE camuchita_db_backup_20260708.caja_sessions AS
SELECT * FROM camuchita_db.caja_sessions;

CREATE TABLE camuchita_db_backup_20260708.caja_movements AS
SELECT * FROM camuchita_db.caja_movements;

CREATE TABLE camuchita_db_backup_20260708.purchases AS
SELECT * FROM camuchita_db.purchases;

CREATE TABLE camuchita_db_backup_20260708.compra_details AS
SELECT * FROM camuchita_db.compra_details;

CREATE TABLE camuchita_db_backup_20260708.sales AS
SELECT * FROM camuchita_db.sales;

CREATE TABLE camuchita_db_backup_20260708.venta_details AS
SELECT * FROM camuchita_db.venta_details;

CREATE TABLE camuchita_db_backup_20260708.accounts_receivable AS
SELECT * FROM camuchita_db.accounts_receivable;

CREATE TABLE camuchita_db_backup_20260708.payments AS
SELECT * FROM camuchita_db.payments;

CREATE TABLE camuchita_db_backup_20260708.inventory_movements AS
SELECT * FROM camuchita_db.inventory_movements;
