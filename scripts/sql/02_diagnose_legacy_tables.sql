-- Diagnostico previo a limpieza manual.
-- Ejecuta estas consultas antes de eliminar tablas legacy.

USE camuchita_db;

SELECT 'users' AS table_name, COUNT(*) AS total_rows FROM users
UNION ALL
SELECT 'usuarios', COUNT(*) FROM usuarios
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'categorias', COUNT(*) FROM categorias
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'productos', COUNT(*) FROM productos
UNION ALL
SELECT 'clients', COUNT(*) FROM clients
UNION ALL
SELECT 'clientes', COUNT(*) FROM clientes
UNION ALL
SELECT 'suppliers', COUNT(*) FROM suppliers
UNION ALL
SELECT 'proveedores', COUNT(*) FROM proveedores
UNION ALL
SELECT 'caja_boxes', COUNT(*) FROM caja_boxes
UNION ALL
SELECT 'cajas', COUNT(*) FROM cajas
UNION ALL
SELECT 'caja_sessions', COUNT(*) FROM caja_sessions
UNION ALL
SELECT 'sesiones_caja', COUNT(*) FROM sesiones_caja
UNION ALL
SELECT 'caja_movements', COUNT(*) FROM caja_movements
UNION ALL
SELECT 'caja_movimientos', COUNT(*) FROM caja_movimientos
UNION ALL
SELECT 'purchases', COUNT(*) FROM purchases
UNION ALL
SELECT 'compras', COUNT(*) FROM compras
UNION ALL
SELECT 'compra_details', COUNT(*) FROM compra_details
UNION ALL
SELECT 'compra_detalles', COUNT(*) FROM compra_detalles
UNION ALL
SELECT 'sales', COUNT(*) FROM sales
UNION ALL
SELECT 'ventas', COUNT(*) FROM ventas
UNION ALL
SELECT 'venta_details', COUNT(*) FROM venta_details
UNION ALL
SELECT 'accounts_receivable', COUNT(*) FROM accounts_receivable
UNION ALL
SELECT 'cuentas_por_cobrar', COUNT(*) FROM cuentas_por_cobrar
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'abonos', COUNT(*) FROM abonos
UNION ALL
SELECT 'inventory_movements', COUNT(*) FROM inventory_movements
UNION ALL
SELECT 'movimientos_inventario', COUNT(*) FROM movimientos_inventario;

-- Revisa tambien claves foraneas existentes antes de borrar tablas legacy.
SELECT
    table_name,
    constraint_name,
    referenced_table_name
FROM information_schema.key_column_usage
WHERE table_schema = 'camuchita_db'
  AND referenced_table_name IS NOT NULL
ORDER BY table_name, constraint_name;
