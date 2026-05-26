# Camuchita Backend

Backend FastAPI modular construido a partir de la lógica real del documento `/Users/sankef/PROYECTO FELIX NOVIA/02_logica_negocio_bd_camuchita.md` y del modelo SQL de Camuchita.

## Resumen técnico previo (fuente funcional)

### Entidades detectadas
- usuarios
- categorias
- productos
- clientes
- proveedores
- compras y compra_detalles
- ventas y venta_detalles
- cuentas_por_cobrar y abonos
- sesiones_caja y caja_movimientos
- movimientos_inventario

### Relaciones principales
- `products.category_id -> categories.id`
- `purchases.supplier_id -> suppliers.id`
- `purchase_details.purchase_id -> purchases.id`, `purchase_details.product_id -> products.id`
- `sales.client_id -> clients.id`, `sales.cash_session_id -> cash_sessions.id`, `sales.user_id -> users.id`
- `sale_details.sale_id -> sales.id`, `sale_details.product_id -> products.id`
- `accounts_receivable.sale_id -> sales.id`, `accounts_receivable.client_id -> clients.id`
- `payments.account_id -> accounts_receivable.id`, `payments.cash_session_id -> cash_sessions.id`, `payments.user_id -> users.id`
- `cash_movements.cash_session_id -> cash_sessions.id`
- `inventory_movements.product_id -> products.id`

### Módulos definidos desde la lógica del negocio
- `auth`
- `users`
- `categories`
- `products`
- `clients`
- `suppliers`
- `cash`
- `purchases`
- `sales`
- `receivables`
- `inventory`

### Reglas de negocio implementadas en services
- RN-01: venta bloqueada si stock insuficiente.
- RN-03: endpoints críticos protegidos con rol `ADMIN`.
- RN-04: `CONTADO` sin cliente y `FIADO` con cliente obligatorio.
- RN-05: cliente `MOROSO`/`BLOQUEADO` no puede comprar al fiado.
- RN-06: fiado no excede límite de crédito.
- RN-07: venta fiado crea cuenta por cobrar y actualiza saldo cliente.
- RN-08: abono > 0 y no puede exceder saldo actual.
- RN-09: abono actualiza CxC, saldo cliente y caja.
- RN-11: no más de una sesión abierta por caja+fecha.
- RN-12: cierre de caja calcula teórico y diferencia contra físico.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración `.env`

```bash
cp .env.example .env
```

Variables clave:
- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`

## Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Endpoints principales

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/me`

### Users
- `GET /api/users`
- `GET /api/users/{id}`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`

### Catálogo y maestros
- `POST/GET /api/categories`
- `POST/GET /api/products`
- `POST/GET /api/clients`
- `POST/GET /api/suppliers`

### Caja
- `POST /api/cash/boxes`
- `POST /api/cash/sessions/open`
- `POST /api/cash/sessions/{session_id}/close`

### Operaciones
- `POST /api/purchases`
- `POST /api/sales`
- `POST /api/receivables/payments`
- `GET /api/inventory/movements`

## Pruebas

```bash
pytest app/tests -q
```

## Nota de supuestos
- Se usó SQLAlchemy síncrono y `Base.metadata.create_all()` para arranque rápido.
- Se dejó carpeta `alembic/` preparada; falta cablear `alembic.ini` y `env.py` para migraciones versionadas formales.
- Se mantiene `sqlite` como valor por defecto para desarrollo local rápido, pero el diseño apunta a MySQL vía `DATABASE_URL` en `.env`.
