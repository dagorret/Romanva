#!/bin/bash
set -e

cd /code

echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "👤 Creando usuario admin..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
u, created = User.objects.get_or_create(
    username="admin",
    defaults={"email": "admin@admin.com", "is_staff": True, "is_superuser": True},
)
u.set_password("admin")
u.save()
if created:
    print("✓ Usuario admin creado")
else:
    print("✓ Usuario admin actualizado")
EOF

echo "🚀 Iniciando servidor Django..."
echo "📍 Admin disponible en: http://localhost:8008/admin/"
echo "👤 Usuario: admin / Contraseña: admin"
python manage.py runserver 0.0.0.0:8008
