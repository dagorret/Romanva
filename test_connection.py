#!/usr/bin/env python3
"""
Script de prueba de conexión a Moodle
Verifica que la configuración sea correcta antes de importar datos
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moodlestats.settings')
import django
django.setup()

from django.conf import settings
import mysql.connector
from mysql.connector import Error


def test_connection():
    """Prueba la conexión a la base de datos de Moodle"""
    config = settings.MOODLE_DB_CONFIG
    
    print("=" * 60)
    print("  Prueba de Conexión a Moodle")
    print("=" * 60)
    print()
    print(f"Host:     {config['host']}")
    print(f"Puerto:   {config['port']}")
    print(f"Base de datos: {config['database']}")
    print(f"Usuario:  {config['user']}")
    print(f"Prefijo:  {config['prefix']}")
    print()
    print("Intentando conectar...")
    
    try:
        # Intentar conectar
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            charset='utf8mb4',
            use_unicode=True,
            connect_timeout=10
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Conexión exitosa a MySQL Server versión {db_info}")
            
            # Probar una query simple
            cursor = connection.cursor()
            
            # Contar cursos
            cursor.execute(f"SELECT COUNT(*) FROM {config['prefix']}course WHERE id > 1")
            course_count = cursor.fetchone()[0]
            print(f"✓ Encontrados {course_count} cursos en Moodle")
            
            # Contar usuarios
            cursor.execute(f"SELECT COUNT(*) FROM {config['prefix']}user WHERE deleted = 0")
            user_count = cursor.fetchone()[0]
            print(f"✓ Encontrados {user_count} usuarios activos")
            
            # Listar algunas tablas
            cursor.execute(f"""
                SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = '{config['database']}' 
                AND TABLE_NAME LIKE '{config['prefix']}%'
                LIMIT 10
            """)
            tables = cursor.fetchall()
            print(f"\n✓ Tablas encontradas (primeras 10):")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            connection.close()
            
            print()
            print("=" * 60)
            print("✅ PRUEBA EXITOSA - La configuración es correcta")
            print("=" * 60)
            print()
            print("Siguiente paso: Importar datos con:")
            print("  docker-compose exec web python manage.py import_moodle")
            print()
            return True
            
    except Error as e:
        print()
        print("=" * 60)
        print("❌ ERROR DE CONEXIÓN")
        print("=" * 60)
        print(f"\nError: {e}")
        print()
        print("Posibles causas:")
        print("  1. El host de Moodle no es accesible desde el contenedor")
        print("  2. Las credenciales son incorrectas")
        print("  3. El puerto MySQL está cerrado o filtrado")
        print("  4. El nombre de la base de datos es incorrecto")
        print()
        print("Soluciones:")
        print("  1. Verifica la configuración en docker-compose.yml")
        print("  2. Asegúrate que MySQL acepte conexiones remotas")
        print("  3. Verifica que no haya un firewall bloqueando")
        print()
        return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
