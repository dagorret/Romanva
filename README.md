# Romanova Platform

Sistema de análisis estadístico y gestión de datos Moodle desarrollado en Django con PostgreSQL.

## Características

### 📊 Panel de Reportes Básicos
- Migración completa del sistema PHP original
- Reportes semanales de acceso por curso y grupo
- Filtrado por categoría "Grado" y cursos del último año
- Búsqueda por código de curso
- Lista detallada de usuarios sin acceso

### 📈 Análisis Estadísticos Avanzados
1. **Estadísticas Descriptivas**: Media, máximos, mínimos, tasas de acceso
2. **Análisis de Correlación**: Relación entre variables (inscriptos, accesos, grupos)
3. **Distribución de Accesos**: Histogramas y distribución temporal
4. **Comparación entre Grupos**: Métricas comparativas de rendimiento
5. **Tendencias Temporales**: Análisis de series de tiempo semanales
6. **Panel Personalizado**: Selección libre de variables y operaciones estadísticas

### 🐳 Arquitectura
- **Backend**: Django 5.1 con Python 3.12
- **Base de datos**: PostgreSQL 16
- **Containerización**: Docker y Docker Compose
- **Librerías estadísticas**: NumPy, Pandas, SciPy, Matplotlib, Seaborn

## Instalación y Configuración

### Requisitos previos
- Docker
- Docker Compose

### 1. Clonar y configurar

```bash
cd /home/carlos/work/msp
cp .env.example .env
```

Edita `.env` si necesitas cambiar configuraciones (opcional para desarrollo).

### 2. Construir y levantar servicios

```bash
docker compose up --build -d
```

Esto iniciará:
- PostgreSQL en puerto 5432
- Django en puerto 8008

### 3. Ejecutar migraciones

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### 4. Crear superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

Credenciales sugeridas:
- Usuario: `admin`
- Email: `admin@localhost`
- Contraseña: `admin123` (cambiar en producción)

### 5. Cargar datos de prueba (mock)

```bash
docker compose exec web python manage.py load_mock_data --clear
```

Esto generará:
- 5 categorías (Grado, Postgrado, Derecho, Economía, Ingeniería)
- 9 cursos con datos del año actual
- 60 usuarios de prueba
- Grupos por curso (2-3 por curso)
- Inscripciones y accesos realistas

## Uso del Sistema

### Acceso al sistema

1. **Aplicación web**: http://localhost:8008
2. **Panel de administración**: http://localhost:8008/admin

### Credenciales por defecto
- Usuario: `admin`
- Contraseña: `admin123`

### Navegación

#### Panel de Reportes (migrado de PHP)
1. Ingresa al sistema
2. Selecciona un curso
3. Selecciona un grupo
4. Define rango de fechas (por defecto: últimos 30 días)
5. Haz clic en "Calcular"
6. Visualiza reportes semanales de acceso
7. Haz clic en "Ver usuarios" para ver quiénes no accedieron

#### Estadísticas Avanzadas
1. Haz clic en "Estadísticas" en el menú
2. Selecciona el tipo de análisis:
   - **Estadísticas Descriptivas**: Resumen general por curso
   - **Correlación**: Relaciones entre variables
   - **Distribución**: Accesos por día
   - **Comparación**: Rendimiento entre grupos
   - **Tendencias**: Evolución semanal
   - **Panel Personalizado**: Análisis a medida

#### Panel Personalizado
1. Selecciona variables a analizar (accesos, inscripciones, etc.)
2. Elige operación estadística (media, mediana, desviación estándar, etc.)
3. Haz clic en "Calcular estadísticas"
4. Visualiza resultados

## Comandos Útiles

### Ver logs
```bash
docker compose logs -f web
```

### Acceder a shell de Django
```bash
docker compose exec web python manage.py shell
```

### Acceder a PostgreSQL
```bash
docker compose exec db psql -U msp_user -d moodle_stats
```

### Recargar datos mock
```bash
docker compose exec web python manage.py load_mock_data --clear
```

### Detener servicios
```bash
docker compose down
```

### Detener y eliminar volúmenes (CUIDADO: elimina la BD)
```bash
docker compose down -v
```

## Estructura del Proyecto

```
msp/
├── config/              # Configuración Django
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── moodle/         # App principal (reportes básicos)
│   │   ├── models.py   # Modelos de datos Moodle
│   │   ├── views.py    # Vistas del panel
│   │   ├── admin.py    # Admin de Django
│   │   └── management/
│   │       └── commands/
│   │           └── load_mock_data.py  # Generador de datos
│   └── analytics/      # App de estadísticas avanzadas
│       ├── models.py
│       ├── views.py    # 6 tipos de análisis
│       └── admin.py
├── templates/
│   ├── base.html
│   ├── moodle/         # Templates del panel básico
│   └── analytics/      # Templates de estadísticas
├── static/             # CSS, JS, imágenes
├── docker compose.yml  # Orquestación de servicios
├── Dockerfile          # Imagen de Django
├── requirements.txt    # Dependencias Python
└── manage.py
```

## Modelos de Datos

El sistema replica la estructura de Moodle:

- **Category**: Categorías de cursos
- **Course**: Cursos con código, nombre, fechas
- **MoodleUser**: Usuarios (estudiantes, docentes)
- **Group**: Grupos dentro de cursos
- **GroupMember**: Relación usuario-grupo
- **Enrol**: Métodos de inscripción
- **UserEnrolment**: Inscripciones de usuarios
- **UserLastAccess**: Último acceso al curso

## Migración desde el sistema PHP

El sistema Django implementa la misma funcionalidad que el script PHP original:

### Equivalencias

| PHP Original | Django |
|-------------|--------|
| `gestoresapp/index.php` | `apps/moodle/views.py::login_view` |
| `gestoresapp/panel.php` | `apps/moodle/views.py::panel_view` |
| `gestoresapp/never_users.php` | `apps/moodle/views.py::never_users_view` |
| Archivos NDJSON | Modelos Django + PostgreSQL |
| `lib_ndjson.php` | ORM de Django |

### Mejoras sobre el original

1. ✅ Base de datos relacional en vez de archivos NDJSON
2. ✅ Autenticación integrada con Django
3. ✅ Panel de administración completo
4. ✅ Módulo de estadísticas avanzadas
5. ✅ Containerización con Docker
6. ✅ API REST-ready (fácil de extender)
7. ✅ Tests automatizables

## Estadísticas Disponibles

### Descriptivas
- Media (promedio)
- Mediana
- Máximo y mínimo
- Desviación estándar
- Tasas de acceso

### Correlativas
- Inscriptos vs Accesos
- Grupos vs Rendimiento
- Variables personalizadas

### Temporales
- Distribución diaria
- Tendencias semanales
- Evolución histórica

## Desarrollo

### Agregar nuevos análisis estadísticos

1. Edita `apps/analytics/views.py`
2. Agrega nueva función de vista
3. Crea template en `templates/analytics/`
4. Registra URL en `apps/analytics/urls.py`
5. Agrega al menú en `analytics_menu()`

### Extender modelos

1. Edita `apps/moodle/models.py`
2. Crea migración: `python manage.py makemigrations`
3. Aplica: `python manage.py migrate`
4. Actualiza `load_mock_data.py` para generar datos

## Producción

Para deployment en producción:

1. Cambia `DJANGO_DEBUG=False` en `.env`
2. Genera SECRET_KEY segura
3. Configura ALLOWED_HOSTS
4. Usa servidor WSGI (Gunicorn/uWSGI)
5. Configura nginx como reverse proxy
6. Habilita HTTPS
7. Configura backups de PostgreSQL

## Soporte y Contribuciones

Este proyecto migra el sistema PHP original a Django con mejoras significativas en arquitectura, escalabilidad y funcionalidades estadísticas.

### Autor
Sistema desarrollado por Claude Code basado en el script PHP original de gestoresapp.

### Licencia
[Especificar licencia]

---

**Notas importantes:**
- Los datos mock son para testing/desarrollo
- En producción, conectar a BD real de Moodle o implementar sincronización
- El sistema es extensible: fácil agregar nuevos tipos de análisis
- Compatible con Django REST Framework para crear API
