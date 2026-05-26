# Alembic

This folder is ready for migration scripts.

## Init (first time)

```bash
alembic init alembic
```

## Create migration

```bash
alembic revision --autogenerate -m "init"
```

## Apply migration

```bash
alembic upgrade head
```
