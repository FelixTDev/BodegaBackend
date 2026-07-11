# BodegaBackend

Backend desarrollado con FastAPI para gestionar autenticacion, usuarios, categorias, productos, clientes, proveedores, compras, ventas, caja, inventario y cuentas por cobrar.

El proyecto fue revisado y ajustado con un enfoque conservador para una entrega academica: se mantuvieron los endpoints existentes, se reforzo la configuracion para produccion y se mejoro la documentacion sin cambiar la arquitectura funcional del sistema.

## Arquitectura de despliegue

- `Railway`: base de datos MySQL
- `Render`: backend FastAPI
- `Vercel`: frontend web

El backend queda preparado para ejecutarse localmente con MySQL, desplegarse en Render y conectarse a MySQL hospedado en Railway mediante variables de entorno.

## Tecnologias utilizadas

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic y Pydantic Settings
- PyMySQL
- JWT con `python-jose`
- `passlib` para hashing de contrasenas
- Pytest

## Estructura del proyecto

```text
BodegaBackend/
|-- app/
|   |-- core/                  # configuracion, base de datos, seguridad y excepciones
|   |-- modules/               # modulos por dominio
|   |   |-- autenticacion/
|   |   |-- usuarios/
|   |   |-- categorias/
|   |   |-- productos/
|   |   |-- clientes/
|   |   |-- proveedores/
|   |   |-- compras/
|   |   |-- ventas/
|   |   |-- caja/
|   |   |-- inventario/
|   |   |-- cuentas_por_cobrar/
|   |-- shared/                # respuestas y dependencias reutilizables
|   |-- tests/                 # pruebas automatizadas
|-- alembic/                   # base preparada para migraciones futuras
|-- docs/superpowers/          # especificacion y plan de auditoria aplicados
|-- .env.example               # ejemplo de variables de entorno
|-- requirements.txt
|-- runtime.txt
|-- README.md
```

## Requisitos previos

- Python 3.12 o superior
- MySQL disponible localmente o en Railway
- `pip`
- Git

## Instalacion local

1. Clona el repositorio:

```bash
git clone https://github.com/FelixTDev/BodegaBackend.git
cd BodegaBackend
```

2. Crea y activa un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Crea tu archivo `.env` a partir del ejemplo:

```bash
copy .env.example .env
```

5. Ajusta los valores de conexion MySQL y la clave secreta.

## Variables de entorno necesarias

El backend puede construirse con variables separadas de MySQL o usando `DATABASE_URL`.

Variables principales:

- `APP_NAME`
- `APP_VERSION`
- `APP_ENV`
- `DEBUG`
- `API_PREFIX`
- `PORT`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DATABASE_URL` (opcional si ya usas `DB_*`)
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `FRONTEND_URL`
- `ALLOWED_CORS_ORIGINS`
- `BACKEND_URL`

### Ejemplo para MySQL local

```env
APP_ENV=development
DEBUG=true
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bodega_backend
DB_USER=root
DB_PASSWORD=tu_password
SECRET_KEY=una-clave-larga-y-segura
FRONTEND_URL=http://localhost:3000
ALLOWED_CORS_ORIGINS=http://127.0.0.1:3000,http://localhost:5173
BACKEND_URL=http://127.0.0.1:8000
PORT=8000
```

### Ejemplo usando MySQL de Railway

```env
APP_ENV=production
DEBUG=false
DB_HOST=tu-host-railway
DB_PORT=3306
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
SECRET_KEY=una-clave-larga-y-segura
FRONTEND_URL=https://tu-frontend.vercel.app
ALLOWED_CORS_ORIGINS=https://tu-frontend.vercel.app
BACKEND_URL=https://tu-backend.onrender.com
PORT=10000
```

## Ejecucion local

Comando recomendado:

```bash
uvicorn app.main:app --reload
```

Tambien puedes especificar host y puerto:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Rutas esperadas en local:

- API base: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Swagger / OpenAPI

Swagger ya queda habilitado por FastAPI y documenta endpoints reales del proyecto.

Rutas:

- Local: `http://127.0.0.1:8000/docs`
- Produccion en Render: `https://tu-backend.onrender.com/docs`

Endpoints documentados principales:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/me`
- `GET /api/users`
- `GET /api/users/{usuario_id}`
- `PUT /api/users/{usuario_id}`
- `DELETE /api/users/{usuario_id}`
- `POST /api/categories`
- `GET /api/categories`
- `POST /api/products`
- `GET /api/products`
- `POST /api/products/{producto_id}/ajustes`
- `POST /api/clients`
- `GET /api/clients`
- `POST /api/suppliers`
- `GET /api/suppliers`
- `POST /api/cash/boxes`
- `GET /api/cash/boxes`
- `GET /api/cash/sessions`
- `POST /api/cash/sessions/open`
- `POST /api/cash/sessions/{session_id}/close`
- `GET /api/purchases`
- `POST /api/purchases`
- `GET /api/sales`
- `POST /api/sales`
- `GET /api/receivables`
- `POST /api/receivables/payments`
- `GET /api/inventory/movements`

Como probar desde Swagger:

1. Abre `/docs`.
2. Ejecuta `POST /api/auth/login` o `POST /api/auth/register`.
3. Copia el `access_token`.
4. Usa el boton `Authorize` de Swagger con `Bearer <token>`.
5. Prueba los endpoints protegidos.

## Endpoints principales

Ademas de Swagger, estos son los grupos funcionales del backend:

- Autenticacion y perfil de usuario
- Gestion de usuarios
- Catalogo: categorias y productos
- Maestros: clientes y proveedores
- Operaciones: compras y ventas
- Caja y sesiones
- Inventario
- Cuentas por cobrar y abonos

## Limpieza manual de base de datos

El backend actual usa como tablas canonicas:

- `users`
- `categories`
- `products`
- `clients`
- `suppliers`
- `caja_boxes`
- `caja_sessions`
- `caja_movements`
- `purchases`
- `compra_details`
- `sales`
- `venta_details`
- `accounts_receivable`
- `payments`
- `inventory_movements`

Si tu base tiene tablas duplicadas en espanol y en ingles, usa estos scripts manuales antes de pasar a produccion:

- [scripts/sql/01_backup_canonic_tables.sql](C:/Users/felix/Downloads/BodegaBackend/scripts/sql/01_backup_canonic_tables.sql)
- [scripts/sql/02_diagnose_legacy_tables.sql](C:/Users/felix/Downloads/BodegaBackend/scripts/sql/02_diagnose_legacy_tables.sql)
- [scripts/sql/03_drop_legacy_tables.sql](C:/Users/felix/Downloads/BodegaBackend/scripts/sql/03_drop_legacy_tables.sql)

Orden recomendado:

1. Ejecutar respaldo de tablas canonicas.
2. Ejecutar diagnostico para revisar conteos y claves foraneas.
3. Confirmar manualmente que las tablas legacy no tienen datos que deban migrarse.
4. Ejecutar el script de eliminacion de tablas legacy.

## Base de datos en Railway

La base de datos objetivo es MySQL en Railway.

### Que hacer en Railway

1. Crea un nuevo servicio MySQL.
2. Espera a que Railway aprovisione la instancia.
3. Copia los datos de conexion del panel:
   - host
   - puerto
   - nombre de base de datos
   - usuario
   - password
4. Registra esas credenciales en Render como variables de entorno del backend.

### Variables que debes copiar hacia Render

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

### Como validar la conexion

- Ejecuta el backend con esas variables.
- Revisa que el arranque no falle.
- Abre `/docs`.
- Prueba `GET /` y un endpoint real autenticado.
- Revisa logs de Render si aparece un error de base de datos.

## Backend en Render

### Tipo de servicio

- Crear un `Web Service`
- Alternativa recomendada: desplegar usando el blueprint incluido en [render.yaml](C:/Users/felix/Downloads/BodegaBackend/render.yaml)

### Runtime recomendado

- Python 3.12
- Archivo incluido: `runtime.txt`

### Build command

```bash
pip install -r requirements.txt
```

### Start command recomendado

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Variables de entorno en Render

- `APP_NAME=Camuchita Backend`
- `APP_VERSION=1.0.0`
- `APP_ENV=production`
- `DEBUG=false`
- `API_PREFIX=/api`
- `PORT` = valor asignado por Render o definido por el servicio
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SECRET_KEY`
- `ALGORITHM=HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`
- `REFRESH_TOKEN_EXPIRE_DAYS=7`
- `FRONTEND_URL=https://tu-frontend.vercel.app`
- `ALLOWED_CORS_ORIGINS=https://tu-frontend.vercel.app`
- `BACKEND_URL=https://tu-backend.onrender.com`

El archivo `render.yaml` ya deja preconfigurados los valores no secretos. Las credenciales y URLs reales deben completarse desde el panel de Render.

### Verificacion del despliegue en Render

1. Confirmar que el build termina sin errores.
2. Confirmar que el servicio inicia correctamente.
3. Abrir `https://tu-backend.onrender.com/`.
4. Abrir `https://tu-backend.onrender.com/docs`.
5. Revisar logs para confirmar que no hay errores de conexion a MySQL.
6. Probar login y al menos un endpoint protegido.

## Frontend en Vercel

El frontend debe apuntar a la URL publica del backend desplegado en Render.

### Configuracion esperada

1. Conecta el proyecto frontend a GitHub en Vercel.
2. Registra una variable con la URL del backend de Render.
3. Usa esa URL en las llamadas HTTP del frontend.
4. Configura `FRONTEND_URL` y `ALLOWED_CORS_ORIGINS` en el backend para permitir ese dominio.

### Verificacion esperada

- El frontend carga sin errores de CORS.
- El frontend consume correctamente los endpoints del backend.
- Las solicitudes autenticadas funcionan con la URL publica de Render.

## Buenas practicas aplicadas

- Configuracion centralizada por variables de entorno
- Soporte para MySQL local y MySQL en Railway
- CORS configurable para Vercel y entornos locales
- Manejo consistente de errores JWT
- Swagger con descripciones y respuestas comunes
- `.env.example` sin credenciales reales
- `runtime.txt` preparado para Render
- Pruebas automatizadas para configuracion y autenticacion
- Listados backend reales para cajas, sesiones, compras, ventas y cuentas por cobrar
- Scripts SQL manuales para depuracion de tablas duplicadas

## Auditoria realizada

### Hallazgos de impacto alto

- `SECRET_KEY` inseguro por defecto en configuracion.
- Falta de CORS para el frontend desplegado en Vercel.
- Error de token JWT no normalizado, con riesgo de respuesta 500.

### Hallazgos de impacto medio

- Swagger existente pero con metadata limitada.
- README incompleto para la arquitectura real Railway/Render/Vercel.
- Dependencia de configuracion poco clara para despliegue en produccion.

### Hallazgos de impacto bajo

- Tags y textos de rutas poco consistentes.
- Faltaban docstrings puntuales en configuracion y base de datos.
- `runtime.txt` no estaba presente.

## Cambios implementados

- Soporte para `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD`
- Validacion de `SECRET_KEY` fuera de desarrollo
- Propiedad calculada para origenes CORS
- Middleware CORS en FastAPI
- Verificacion basica de conexion a base de datos al iniciar
- Manejo consistente de errores de token
- Mejora de metadata OpenAPI en endpoints reales
- Endpoints GET reales para cajas, sesiones, compras, ventas y cuentas por cobrar
- `.env.example` actualizado
- `.gitignore` reforzado
- `runtime.txt` agregado
- README reescrito para instalacion, ejecucion y despliegue

## Estado del proyecto

El backend queda funcional para desarrollo local y preparado para despliegue con:

- MySQL en Railway
- Backend en Render
- Frontend en Vercel

No se realizaron cambios agresivos de arquitectura ni se modificaron endpoints existentes.

## Despliegue en Render

Resumen operativo:

1. Sube los cambios a GitHub.
2. Crea un `Web Service` en Render apuntando al repositorio o usa el blueprint de [render.yaml](C:/Users/felix/Downloads/BodegaBackend/render.yaml).
3. Configura el `Build Command`:

```bash
pip install -r requirements.txt
```

4. Configura el `Start Command`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Carga las variables de entorno con las credenciales del MySQL de Railway.
6. Despliega.
7. Valida `GET /`, `GET /docs` y los endpoints principales.

## Checklist final para produccion

### Antes del despliegue

- `requirements.txt` actualizado
- `.env.example` creado y revisado
- `.gitignore` correcto
- `README.md` actualizado
- Swagger funcionando localmente
- Backend probado con MySQL
- No hay credenciales reales en el repositorio
- CORS preparado para Vercel
- Variables necesarias identificadas

### Railway - MySQL

- Servicio MySQL creado
- Base de datos configurada
- Host, puerto, usuario, password y nombre de BD identificados
- Conexion probada desde el backend

### Render - Backend

- Servicio web creado desde GitHub
- `Build Command` configurado
- `Start Command` configurado
- Variables de entorno cargadas
- Backend desplegado correctamente
- Swagger accesible en produccion
- Logs sin errores de conexion

### Vercel - Frontend

- Proyecto conectado a GitHub
- Variable con URL del backend configurada
- Frontend desplegado correctamente
- Consumo de API validado
- CORS funcionando

## Pruebas automatizadas

Comando recomendado:

```bash
.venv\Scripts\python.exe -m pytest app/tests -q
```

## Nota de alcance

Esta revision priorizo cambios seguros y trazables para cumplir la rubrica academica y acercar el backend a un despliegue real sin romper endpoints existentes ni modificar la base de datos de forma agresiva.
