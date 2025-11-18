#!/bin/sh
set -e

# Crear migraciones y aplicarlas
python inventario/manage.py makemigrations
python inventario/manage.py migrate

# (Opcional) recolectar archivos estáticos si lo usás en producción
# python inventario/manage.py collectstatic --noinput

# Levantar el servidor en 0.0.0.0:8000
python inventario/manage.py runserver 0.0.0.0:8000
