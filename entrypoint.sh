#!/bin/bash
set -e

echo "Esperando a que PostgreSQL esté listo..."
while ! pg_isready -h db -p 5432 -U msp_user > /dev/null 2>&1; do
    sleep 1
done

echo "PostgreSQL está listo!"

echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate

echo "Creando superusuario si no existe..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('Superusuario creado: admin / admin123')
else:
    print('Superusuario ya existe')
END

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || true

echo "Sistema listo!"
exec "$@"
