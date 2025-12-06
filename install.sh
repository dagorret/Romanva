#!/bin/bash
# Script de instalación y configuración rápida de Moodle Stats

set -e

echo "======================================"
echo "  Moodle Stats - Instalación Rápida"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    echo "Por favor instala Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    echo "Por favor instala Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker y Docker Compose detectados${NC}"
echo ""

# Crear directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p data staticfiles
echo -e "${GREEN}✓ Directorios creados${NC}"
echo ""

# Solicitar configuración de Moodle (opcional)
echo "¿Deseas configurar la conexión a Moodle ahora? (s/n)"
read -r configure_now

if [[ "$configure_now" == "s" || "$configure_now" == "S" ]]; then
    echo ""
    echo "Configuración de Conexión a Moodle:"
    echo "-----------------------------------"
    
    read -p "Host de Moodle [localhost]: " MOODLE_HOST
    MOODLE_HOST=${MOODLE_HOST:-localhost}
    
    read -p "Puerto MySQL [3306]: " MOODLE_PORT
    MOODLE_PORT=${MOODLE_PORT:-3306}
    
    read -p "Nombre de la BD: " MOODLE_DB
    read -p "Usuario de la BD: " MOODLE_USER
    read -sp "Contraseña de la BD: " MOODLE_PASS
    echo ""
    
    read -p "Prefijo de tablas [mdl_]: " MOODLE_PREFIX
    MOODLE_PREFIX=${MOODLE_PREFIX:-mdl_}
    
    # Actualizar docker-compose.yml
    echo ""
    echo "📝 Actualizando configuración..."
    
    # Backup del archivo original
    cp docker-compose.yml docker-compose.yml.backup
    
    # Actualizar variables de entorno
    sed -i "s/MOODLE_DB_HOST=.*/MOODLE_DB_HOST=$MOODLE_HOST/" docker-compose.yml
    sed -i "s/MOODLE_DB_PORT=.*/MOODLE_DB_PORT=$MOODLE_PORT/" docker-compose.yml
    sed -i "s/MOODLE_DB_NAME=.*/MOODLE_DB_NAME=$MOODLE_DB/" docker-compose.yml
    sed -i "s/MOODLE_DB_USER=.*/MOODLE_DB_USER=$MOODLE_USER/" docker-compose.yml
    sed -i "s/MOODLE_DB_PASSWORD=.*/MOODLE_DB_PASSWORD=$MOODLE_PASS/" docker-compose.yml
    sed -i "s/MOODLE_DB_PREFIX=.*/MOODLE_DB_PREFIX=$MOODLE_PREFIX/" docker-compose.yml
    
    echo -e "${GREEN}✓ Configuración actualizada${NC}"
else
    echo -e "${YELLOW}⚠ Recuerda editar docker-compose.yml antes de importar datos${NC}"
fi

echo ""
echo "🐳 Construyendo e iniciando contenedores..."
docker-compose up -d --build

echo ""
echo "⏳ Esperando a que el servidor esté listo..."
sleep 5

# Verificar que el contenedor esté corriendo
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Contenedor iniciado correctamente${NC}"
else
    echo -e "${RED}❌ Error al iniciar el contenedor${NC}"
    echo "Ejecuta 'docker-compose logs' para ver los errores"
    exit 1
fi

echo ""
echo "======================================"
echo -e "${GREEN}✅ Instalación completada!${NC}"
echo "======================================"
echo ""
echo "🌐 URL del Admin: http://localhost:8008/admin/"
echo "👤 Usuario: admin"
echo "🔑 Contraseña: admin"
echo ""
echo "📋 Comandos útiles:"
echo "  - Ver logs:           docker-compose logs -f"
echo "  - Parar sistema:      docker-compose down"
echo "  - Reiniciar:          docker-compose restart"
echo "  - Importar datos:     docker-compose exec web python manage.py import_moodle"
echo ""
echo "📖 Lee el README.md para más información"
echo ""
