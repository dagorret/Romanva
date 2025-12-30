#!/bin/bash

# Script de inicialización completa del sistema Romanova Platform

echo "=================================================="
echo "  Romanova Platform - Inicialización"
echo "=================================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Levantar servicios
echo -e "${YELLOW}[1/5] Levantando servicios Docker...${NC}"
docker compose down 2>/dev/null
docker compose up -d --build

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error al levantar servicios${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Servicios levantados${NC}"
echo ""

# 2. Esperar a PostgreSQL
echo -e "${YELLOW}[2/5] Esperando a PostgreSQL...${NC}"
sleep 5

MAX_TRIES=30
COUNT=0
until docker compose exec -T db pg_isready -U msp_user -d moodle_stats > /dev/null 2>&1; do
    COUNT=$((COUNT+1))
    if [ $COUNT -gt $MAX_TRIES ]; then
        echo -e "${RED}✗ PostgreSQL no responde después de $MAX_TRIES intentos${NC}"
        exit 1
    fi
    echo "Esperando... ($COUNT/$MAX_TRIES)"
    sleep 1
done

echo -e "${GREEN}✓ PostgreSQL listo${NC}"
echo ""

# 3. Ejecutar migraciones
echo -e "${YELLOW}[3/5] Ejecutando migraciones...${NC}"
docker compose exec -T web python manage.py makemigrations
docker compose exec -T web python manage.py migrate

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error en migraciones${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Migraciones completadas${NC}"
echo ""

# 4. Crear superusuario
echo -e "${YELLOW}[4/5] Creando superusuario...${NC}"
docker compose exec -T web python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('✓ Superusuario creado: admin / admin123')
else:
    print('✓ Superusuario ya existe')
END

echo -e "${GREEN}✓ Superusuario configurado${NC}"
echo ""

# 5. Cargar datos mock
echo -e "${YELLOW}[5/5] Cargando datos de prueba...${NC}"
docker compose exec -T web python manage.py load_mock_data --clear

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error al cargar datos${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Datos de prueba cargados${NC}"
echo ""

# Resumen final
echo "=================================================="
echo -e "${GREEN}   ✓ Inicialización completada exitosamente${NC}"
echo "=================================================="
echo ""
echo "El sistema está listo para usar:"
echo ""
echo "  🌐 Aplicación web:  http://localhost:8008"
echo "  🔧 Panel admin:     http://localhost:8008/admin"
echo ""
echo "  👤 Usuario:         admin"
echo "  🔑 Contraseña:      admin123"
echo ""
echo "=================================================="
echo ""
echo "Comandos útiles:"
echo "  Ver logs:           docker compose logs -f web"
echo "  Detener:            docker compose down"
echo "  Reiniciar:          docker compose restart"
echo ""
