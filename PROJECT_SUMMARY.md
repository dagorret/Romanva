# Moodle Stats - Resumen Ejecutivo del Proyecto

## ✅ Estado: COMPLETADO

Sistema Django completo para importar, almacenar y analizar datos desde Moodle.

## 🎯 Objetivos Cumplidos

### 1. ✅ Docker con Volúmenes Persistentes
- Base de datos SQLite en `./data/` (host)
- Archivos estáticos en `./staticfiles/` (host)
- Código en contenedor pero modificable desde host
- Los datos persisten incluso si se elimina el contenedor

### 2. ✅ Importación desde Moodle
- 10 tablas soportadas de Moodle
- Importación individual o masiva
- Tres formas de importar:
  * Desde el admin de Django (UI)
  * Comando CLI (`import_moodle`)
  * Programáticamente desde Python

### 3. ✅ Interfaz Admin de Django
- Visualización de todas las tablas importadas
- Filtros y búsqueda en cada tabla
- Logs de importación con estado y errores
- Botón "Importar desde Moodle" en cada tabla
- Acción "Exportar a Excel" para datos seleccionados

### 4. ✅ Exportación a Excel
- Exportación selectiva (registros seleccionados)
- Formato profesional con encabezados
- Nombres de archivo con timestamp
- Ajuste automático de anchos de columna

## 📊 Tablas Importadas

| # | Tabla | Descripción |
|---|-------|-------------|
| 1 | courses | Cursos de Moodle |
| 2 | categories | Categorías de cursos |
| 3 | enrol | Métodos de inscripción |
| 4 | user_enrolments | Inscripciones de usuarios |
| 5 | users | Usuarios de Moodle |
| 6 | groups | Grupos de cursos |
| 7 | groups_members | Miembros de grupos |
| 8 | user_lastaccess | Último acceso de usuarios |
| 9 | role_assignments | Asignaciones de roles |
| 10 | context | Contextos de Moodle |

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│              Docker Container                    │
│  ┌───────────────────────────────────────────┐ │
│  │         Django Application                 │ │
│  │  ┌────────────┐      ┌─────────────┐     │ │
│  │  │   Admin    │◄────►│   Models    │     │ │
│  │  │    UI      │      │  (10 tablas)│     │ │
│  │  └────────────┘      └─────────────┘     │ │
│  │        ▲                     ▲            │ │
│  │        │                     │            │ │
│  │        │                     ▼            │ │
│  │        │              ┌─────────────┐    │ │
│  │        │              │  Import     │    │ │
│  │        │              │  Command    │    │ │
│  │        │              └─────────────┘    │ │
│  │        │                     ▲            │ │
│  └────────┼─────────────────────┼────────────┘ │
│           │                     │              │
│           ▼                     │              │
│   ┌───────────────┐            │              │
│   │ /staticfiles  │◄───────────┤              │
│   │   (Volume)    │            │              │
│   └───────────────┘            │              │
│           ▲                     │              │
│           │                     │              │
│   ┌───────────────┐            │              │
│   │    /data      │◄───────────┘              │
│   │  (db.sqlite3) │                           │
│   │   (Volume)    │                           │
│   └───────────────┘                           │
│           ▲                                    │
└───────────┼────────────────────────────────────┘
            │
     HOST FILESYSTEM
            │
            ▼
  ┌─────────────────┐
  │  Moodle MySQL   │
  │    Database     │
  └─────────────────┘
```

## 📁 Estructura de Archivos

```
moodle-stats/
├── 📄 README.md                    # Documentación principal
├── 📄 ADMIN_API.md                 # Documentación del admin
├── 📄 docker-compose.yml           # Configuración Docker
├── 📄 Dockerfile                   # Imagen Docker
├── 📄 requirements.txt             # Dependencias Python
├── 🔧 entrypoint.sh               # Script de inicio
├── 🔧 install.sh                  # Instalación rápida
├── 🔧 test_connection.py          # Prueba de conexión
├── 📄 config.example.env          # Ejemplo de configuración
├── 📄 .gitignore                  # Archivos ignorados por Git
├── 📄 manage.py                   # CLI de Django
│
├── moodlestats/                   # Proyecto Django
│   ├── __init__.py
│   ├── settings.py               # Configuración
│   ├── urls.py                   # URLs
│   ├── wsgi.py                   # WSGI
│   └── asgi.py                   # ASGI
│
├── moodledata/                    # App principal
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                 # 10 modelos + ImportLog
│   ├── admin.py                  # Admin personalizado
│   ├── management/
│   │   └── commands/
│   │       └── import_moodle.py  # Comando de importación
│   └── templates/
│       └── admin/
│           ├── moodle_changelist.html
│           └── import_moodle.html
│
├── data/                          # 🔒 PERSISTENTE (host)
│   └── db.sqlite3                # Base de datos
│
└── staticfiles/                   # 🔒 PERSISTENTE (host)
    └── admin/                    # Archivos estáticos de Django
```

## 🚀 Inicio Rápido

### Opción 1: Instalación Automática
```bash
./install.sh
```

### Opción 2: Manual
```bash
# 1. Configurar conexión a Moodle en docker-compose.yml
# 2. Iniciar el sistema
docker-compose up -d --build

# 3. Acceder al admin
# http://localhost:8008/admin/
# Usuario: admin / Contraseña: admin
```

### Probar Conexión
```bash
docker-compose exec web python test_connection.py
```

### Importar Datos
```bash
# Todas las tablas
docker-compose exec web python manage.py import_moodle

# Tablas específicas
docker-compose exec web python manage.py import_moodle --tables users,courses
```

## 🔑 Características Clave

### Admin de Django
- ✅ UI intuitiva para gestión de datos
- ✅ Botón "Importar desde Moodle" en cada tabla
- ✅ Acción "Exportar a Excel" para registros seleccionados
- ✅ Filtros y búsqueda en todas las tablas
- ✅ Logs de importación con estado y errores

### Importación
- ✅ Importación por tabla o masiva
- ✅ Limpieza automática antes de importar
- ✅ Inserción en lotes (batch) para rendimiento
- ✅ Logs detallados de cada importación
- ✅ Manejo de errores con rollback

### Exportación
- ✅ Excel con formato profesional
- ✅ Encabezados con colores
- ✅ Ajuste automático de columnas
- ✅ Nombre de archivo con timestamp

### Docker
- ✅ Contenedor aislado
- ✅ Volúmenes persistentes para datos
- ✅ Hot-reload en desarrollo
- ✅ Fácil de desplegar

## 📊 Rendimiento

### Tiempos de Importación (estimados)

| Tabla | Registros | Tiempo |
|-------|-----------|--------|
| courses | ~500 | < 1 min |
| categories | ~100 | < 1 min |
| users | ~50k | 5-10 min |
| user_enrolments | ~100k | 10-15 min |
| groups | ~1k | < 1 min |
| role_assignments | ~50k | 5-10 min |

### Optimizaciones Implementadas
- Inserción en lotes de 1000 registros
- Transacciones atómicas
- Índices en campos `moodle_id`
- Queries optimizadas sin JOINs innecesarios

## 🔒 Seguridad

### En Desarrollo
- ✅ DEBUG = True
- ✅ ALLOWED_HOSTS = ['*']
- ✅ Credenciales en variables de entorno

### Para Producción (TODO)
- ⚠️ Cambiar SECRET_KEY
- ⚠️ DEBUG = False
- ⚠️ Configurar ALLOWED_HOSTS
- ⚠️ Usar PostgreSQL en lugar de SQLite
- ⚠️ Cambiar credenciales del admin
- ⚠️ Usar HTTPS
- ⚠️ Configurar nginx/reverse proxy

## 📝 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f web

# Parar sistema
docker-compose down

# Reiniciar
docker-compose restart

# Entrar al contenedor
docker-compose exec web bash

# Ver BD
docker-compose exec web python manage.py dbshell

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Hacer migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## 🐛 Solución de Problemas

### Error de conexión a Moodle
```bash
# Probar conexión
docker-compose exec web python test_connection.py

# Verificar configuración
docker-compose exec web env | grep MOODLE
```

### BD bloqueada
```bash
docker-compose down
docker-compose up -d
```

### Permisos en volúmenes
```bash
sudo chown -R $USER:$USER ./data ./staticfiles
```

## 📚 Documentación

- **README.md** - Guía completa de instalación y uso
- **ADMIN_API.md** - Documentación del admin y API
- **config.example.env** - Ejemplo de configuración

## ✨ Extensibilidad

### Agregar Nuevas Tablas
1. Agregar modelo en `models.py`
2. Agregar query en `admin.py` (MOODLE_QUERIES)
3. Agregar mapeo en `admin.py` (FIELD_MAPPING)
4. Registrar admin con decorador `@admin.register`
5. Hacer migraciones

### Agregar Acciones Personalizadas
```python
def mi_accion(self, request, queryset):
    # Tu código aquí
    pass
mi_accion.short_description = "Mi acción personalizada"

class MiAdmin(admin.ModelAdmin):
    actions = [mi_accion]
```

## 🎓 Tecnologías Utilizadas

- **Backend:** Django 5.1
- **Base de datos:** SQLite (dev), MySQL (Moodle)
- **Contenedor:** Docker + Docker Compose
- **Export:** openpyxl
- **DB Connector:** mysql-connector-python
- **Server:** Gunicorn (production ready)

## 👤 Autor

Carlos Dagorret
- Blog: https://dagorret.com.ar
- Proyecto: Lucy (Sistema de gestión académica)

## 📅 Fecha de Creación

Diciembre 2024

## 🎉 Estado Final

**✅ PROYECTO COMPLETADO Y FUNCIONAL**

Todas las funcionalidades requeridas han sido implementadas:
- ✅ Docker con volúmenes persistentes
- ✅ Importación desde Moodle (UI + CLI)
- ✅ Admin de Django con 10 tablas
- ✅ Exportación a Excel
- ✅ Logs de importación
- ✅ Documentación completa
- ✅ Scripts de instalación y prueba
