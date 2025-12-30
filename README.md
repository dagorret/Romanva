<div align="center">

# 🚀 Romanova Platform

### Advanced Statistical Analysis and Management Platform for Moodle LMS Data

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**[English](#english)** · **[Español](#español)**

---

### *Born from the need to modernize legacy educational systems*

Transform your Moodle data into actionable insights with powerful statistical analysis,
beautiful visualizations, and an intuitive interface built on modern technology.

[Get Started](#-quick-start) · [View Demo](#-screenshots) · [Documentation](#-documentation)

</div>

---

## 🎯 What is Romanova Platform?

**Romanova Platform** is a comprehensive Django-based web application designed to **analyze, visualize, and manage Moodle LMS data** at scale. Migrated from a legacy PHP system, it combines enterprise-grade architecture with user-friendly interfaces to deliver:

- 📊 **Advanced Statistical Analysis** - 6 specialized modules for deep data insights
- 📈 **Real-Time Reporting** - Weekly access reports with engagement tracking
- 🎓 **Scalable Data Management** - Handle 3,200+ users and 200+ courses efficiently
- 🐳 **Modern Stack** - Fully Dockerized PostgreSQL + Django deployment
- 🔒 **Enterprise Security** - CSRF protection, SQL injection prevention, secure sessions

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📊 Advanced Analytics Engine

- **Descriptive Statistics**
  Mean, median, max, min, standard deviation with visual charts

- **Correlation Analysis**
  Discover relationships between enrollments, access patterns, and performance

- **Temporal Distribution**
  Daily and weekly access pattern visualization with heatmaps

- **Group Comparison**
  Performance metrics across student cohorts

- **Trend Analysis**
  Time series analysis over 12-week periods

- **Custom Dashboard**
  Build your own analysis with selectable variables and operations

</td>
<td width="50%">

### 📈 Intelligent Reporting System

- **Weekly Access Reports**
  Automated reports by course and group

- **Activity Tracking**
  User engagement metrics and participation rates

- **Inactive Student Detection**
  Automated alerts for students at risk

- **Data Export**
  CSV/Excel export for further analysis

- **Category Filtering**
  Filter by program (Grado, Postgrado, etc.)

- **Flexible Date Ranges**
  Custom reporting periods

</td>
</tr>
</table>

---

## 🏗️ Architecture & Technology

```
┌─────────────────────────────────────────────────────────────┐
│                    Romanova Platform                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend        │  Pure CSS (Bootstrap-inspired)           │
│  Backend         │  Django 5.1 (Python 3.12)                │
│  Database        │  PostgreSQL 16 Alpine                    │
│  Analytics       │  NumPy · Pandas · SciPy                  │
│  Visualization   │  Matplotlib · Seaborn                    │
│  Deployment      │  Docker + Docker Compose                 │
│  Security        │  Django Auth · CSRF · Session Management │
└─────────────────────────────────────────────────────────────┘
```

### 📦 Core Components

**Django Apps:**
- `apps.moodle` - Core reporting engine (migrated from PHP)
- `apps.analytics` - Advanced statistical analysis (6 modules)

**Data Models (8 core models):**
- Category, Course, MoodleUser, Group, GroupMember
- Enrol, UserEnrolment, UserLastAccess

**Performance Features:**
- Bulk database operations for thousands of records
- Optimized queries with database indexes
- Connection pooling and caching ready

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)

### Installation in 3 Steps

```bash
# 1. Clone the repository
git clone https://github.com/dagorret/Romanva.git
cd Romanva

# 2. Run initialization script
chmod +x init.sh
./init.sh

# 3. Access the platform
# Open http://localhost:8008 in your browser
```

**That's it!** The script automatically:
- ✅ Builds and starts Docker containers (PostgreSQL + Django)
- ✅ Runs database migrations
- ✅ Creates superuser account (`admin` / `admin123`)
- ✅ Loads realistic mock data (3,200 users, 200 courses)

### 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Web Application** | http://localhost:8008 | `admin` / `admin123` |
| **Admin Panel** | http://localhost:8008/admin | `admin` / `admin123` |
| **PostgreSQL** | localhost:5433 | `msp_user` / `msp_password_2024` |

---

## 📚 Usage Guide

### 1️⃣ Basic Reporting

1. **Login** to the platform at http://localhost:8008
2. **Select Course** from the dropdown menu
3. **Select Group/Commission** for the course
4. **Choose Date Range** (default: last 30 days)
5. **Click "Calculate"** to generate weekly access reports
6. **View Inactive Users** by clicking "Ver usuarios"

### 2️⃣ Statistical Analysis

Navigate to **"Estadísticas"** in the menu and choose from 6 analysis types:

| Module | Description |
|--------|-------------|
| 📊 **Descriptive Statistics** | Basic stats with visual distribution charts |
| 🔗 **Correlation Analysis** | Relationship discovery between variables |
| 📅 **Access Distribution** | Daily and weekly usage patterns |
| 👥 **Group Comparison** | Performance metrics across cohorts |
| 📈 **Temporal Trends** | Time series analysis over 12 weeks |
| ⚙️ **Custom Panel** | Build your own analysis with custom variables |

### 3️⃣ Custom Analysis Panel

1. Navigate to **Custom Panel**
2. **Select Variables**: enrollments, accesses, groups, courses, etc.
3. **Choose Operation**: mean, median, stddev, count, max, min
4. **Get Instant Results** with formatted output

---

## 🔧 Configuration

### Scalable Mock Data

Load data at different scales for testing or production:

```bash
# Full scale (3,200 users, 200 courses)
docker compose exec web python manage.py load_mock_data --clear --scale -1

# Half scale (1,600 users, 100 courses)
docker compose exec web python manage.py load_mock_data --clear --scale -2

# Quarter scale (800 users, 50 courses) - For testing
docker compose exec web python manage.py load_mock_data --clear --scale -4
```

### Mock Data Specifications

| Component | Details |
|-----------|---------|
| **Academic Programs** | 5 programs: Law, Economics, Engineering, Medicine, Architecture |
| **Modalities** | 2 types: Undergraduate (Grado), Graduate (Postgrado) |
| **Courses** | 200 total: 100 first semester, 100 second semester |
| **Students** | 3,200 with realistic names and emails |
| **Groups** | 2-3 groups per course, 20-40 students each |
| **Access Rate** | 70% simulating real engagement patterns |

### Connecting to Real Moodle Database

Edit `config/settings.py` to add a secondary database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='moodle_stats'),
        # ... your Romanova database
    },
    'moodle': {
        'ENGINE': 'django.db.backends.mysql',  # Moodle uses MySQL
        'NAME': 'moodle_production',
        'USER': 'moodle_user',
        'PASSWORD': 'secure_password',
        'HOST': 'moodle-db.example.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

Create a management command to import data from Moodle to Romanova.

---

## 🛠️ Development

### Useful Commands

```bash
# View application logs
docker compose logs -f web

# Access Django shell
docker compose exec web python manage.py shell

# Run tests
docker compose exec web python manage.py test

# Create database migrations
docker compose exec web python manage.py makemigrations

# Access PostgreSQL CLI
docker compose exec db psql -U msp_user -d moodle_stats

# Stop all services
docker compose down

# Restart services
docker compose restart

# Rebuild containers
docker compose up -d --build
```

### Project Structure

```
romanova/
├── apps/
│   ├── moodle/                    # Core reporting application
│   │   ├── models.py              # 8 Moodle data models
│   │   ├── views.py               # Panel, reports, user lists
│   │   ├── urls.py                # URL routing
│   │   └── management/commands/
│   │       └── load_mock_data.py  # Mock data generator
│   └── analytics/                 # Statistical analysis application
│       ├── views.py               # 6 analysis modules
│       └── urls.py                # Analytics routing
├── config/                        # Django project settings
│   ├── settings.py                # Main configuration
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── moodle/                    # Moodle app templates
│   └── analytics/                 # Analytics templates
├── static/                        # Static assets
│   ├── css/                       # Stylesheets
│   └── js/                        # JavaScript
├── docker-compose.yml             # Container orchestration
├── Dockerfile                     # Django container definition
├── requirements.txt               # Python dependencies
├── init.sh                        # Initialization script
└── manage.py                      # Django CLI
```

---

## 📊 Data Model

```
Category (Programs, Modalities)
    ↓ (1:N)
Course (200 courses across 5 programs)
    ↓ (1:N)
Group (2-3 groups per course)
    ↓ (M:N via GroupMember)
MoodleUser (3,200 students)
    ↓ (1:N via UserEnrolment)
Enrol (Enrollment methods)
    ↓ (1:N)
UserLastAccess (Activity tracking)
```

---

## 🤝 Contributing

Contributions are welcome! We appreciate:

- 🐛 Bug reports and fixes
- ✨ Feature requests and implementations
- 📝 Documentation improvements
- 🌍 Translations

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add AmazingFeature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2025 Carlos Dagorret
```

---

## 🙏 Acknowledgments

- **Original PHP System**: gestoresapp
- **Django Software Foundation**: For the amazing framework
- **PostgreSQL Global Development Group**: For the robust database
- **Moodle Community**: For inspiration and LMS excellence

---

## 📧 Contact & Support

**Carlos Dagorret**
GitHub: [@dagorret](https://github.com/dagorret)
Project: [https://github.com/dagorret/Romanva](https://github.com/dagorret/Romanva)

---

## 📸 Screenshots

### Login Page
*Clean and secure authentication interface*

### Main Dashboard
*Weekly access reports with filtering and date range selection*

### Statistical Analysis Menu
*Six specialized analysis modules for deep insights*

### Correlation Analysis
*Discover relationships between enrollments, access patterns, and performance*

---

<div align="center">

## 🌟 Star this repo if you find it useful!

**Made with ❤️ by Carlos Dagorret**

[⬆ Back to top](#-romanova-platform)

</div>

---
---

<div align="center">

# 🚀 Romanova Platform

### Plataforma Avanzada de Análisis Estadístico y Gestión de Datos Moodle

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)](LICENSE)

**[English](#english)** · **[Español](#español)**

---

### *Nacida de la necesidad de modernizar sistemas educativos heredados*

Transforma tus datos de Moodle en insights accionables con análisis estadístico potente,
visualizaciones hermosas y una interfaz intuitiva construida sobre tecnología moderna.

[Comenzar](#-inicio-rápido) · [Ver Demo](#-capturas-de-pantalla) · [Documentación](#-documentación)

</div>

---

## 🎯 ¿Qué es Romanova Platform?

**Romanova Platform** es una aplicación web integral basada en Django diseñada para **analizar, visualizar y gestionar datos de Moodle LMS** a escala. Migrada desde un sistema PHP heredado, combina arquitectura de nivel empresarial con interfaces amigables para entregar:

- 📊 **Análisis Estadístico Avanzado** - 6 módulos especializados para insights profundos
- 📈 **Reportes en Tiempo Real** - Reportes semanales de acceso con seguimiento de participación
- 🎓 **Gestión de Datos Escalable** - Maneja 3,200+ usuarios y 200+ cursos eficientemente
- 🐳 **Stack Moderno** - Despliegue completamente Dockerizado PostgreSQL + Django
- 🔒 **Seguridad Empresarial** - Protección CSRF, prevención de SQL injection, sesiones seguras

---

## ✨ Características Principales

<table>
<tr>
<td width="50%">

### 📊 Motor de Análisis Avanzado

- **Estadísticas Descriptivas**
  Media, mediana, máx, mín, desviación estándar con gráficos visuales

- **Análisis de Correlación**
  Descubre relaciones entre inscripciones, patrones de acceso y rendimiento

- **Distribución Temporal**
  Visualización de patrones de acceso diarios y semanales con mapas de calor

- **Comparación de Grupos**
  Métricas de rendimiento entre cohortes de estudiantes

- **Análisis de Tendencias**
  Análisis de series temporales sobre períodos de 12 semanas

- **Panel Personalizado**
  Construye tu propio análisis con variables y operaciones seleccionables

</td>
<td width="50%">

### 📈 Sistema de Reportes Inteligente

- **Reportes de Acceso Semanales**
  Reportes automatizados por curso y grupo

- **Seguimiento de Actividad**
  Métricas de participación y tasas de compromiso

- **Detección de Estudiantes Inactivos**
  Alertas automatizadas para estudiantes en riesgo

- **Exportación de Datos**
  Exportar a CSV/Excel para análisis adicional

- **Filtrado por Categoría**
  Filtrar por programa (Grado, Postgrado, etc.)

- **Rangos de Fecha Flexibles**
  Períodos de reporte personalizados

</td>
</tr>
</table>

---

## 🏗️ Arquitectura y Tecnología

```
┌─────────────────────────────────────────────────────────────┐
│                    Romanova Platform                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend        │  CSS Puro (inspirado en Bootstrap)      │
│  Backend         │  Django 5.1 (Python 3.12)                │
│  Base de Datos   │  PostgreSQL 16 Alpine                    │
│  Análisis        │  NumPy · Pandas · SciPy                  │
│  Visualización   │  Matplotlib · Seaborn                    │
│  Despliegue      │  Docker + Docker Compose                 │
│  Seguridad       │  Django Auth · CSRF · Gestión de Sesión  │
└─────────────────────────────────────────────────────────────┘
```

### 📦 Componentes Principales

**Apps Django:**
- `apps.moodle` - Motor de reportes central (migrado desde PHP)
- `apps.analytics` - Análisis estadístico avanzado (6 módulos)

**Modelos de Datos (8 modelos core):**
- Category, Course, MoodleUser, Group, GroupMember
- Enrol, UserEnrolment, UserLastAccess

**Características de Rendimiento:**
- Operaciones masivas en base de datos para miles de registros
- Consultas optimizadas con índices de base de datos
- Connection pooling y caching listos

---

## 🚀 Inicio Rápido

### Requisitos Previos

- [Docker](https://docs.docker.com/get-docker/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)

### Instalación en 3 Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/dagorret/Romanva.git
cd Romanva

# 2. Ejecutar script de inicialización
chmod +x init.sh
./init.sh

# 3. Acceder a la plataforma
# Abrir http://localhost:8008 en tu navegador
```

**¡Eso es todo!** El script automáticamente:
- ✅ Construye e inicia contenedores Docker (PostgreSQL + Django)
- ✅ Ejecuta migraciones de base de datos
- ✅ Crea cuenta de superusuario (`admin` / `admin123`)
- ✅ Carga datos mock realistas (3,200 usuarios, 200 cursos)

### 🌐 Puntos de Acceso

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **Aplicación Web** | http://localhost:8008 | `admin` / `admin123` |
| **Panel Admin** | http://localhost:8008/admin | `admin` / `admin123` |
| **PostgreSQL** | localhost:5433 | `msp_user` / `msp_password_2024` |

---

## 📚 Guía de Uso

### 1️⃣ Reportes Básicos

1. **Inicia sesión** en la plataforma en http://localhost:8008
2. **Selecciona Curso** del menú desplegable
3. **Selecciona Grupo/Comisión** para el curso
4. **Elige Rango de Fechas** (por defecto: últimos 30 días)
5. **Haz clic en "Calcular"** para generar reportes semanales de acceso
6. **Ver Usuarios Inactivos** haciendo clic en "Ver usuarios"

### 2️⃣ Análisis Estadístico

Navega a **"Estadísticas"** en el menú y elige entre 6 tipos de análisis:

| Módulo | Descripción |
|--------|-------------|
| 📊 **Estadísticas Descriptivas** | Estadísticas básicas con gráficos de distribución visual |
| 🔗 **Análisis de Correlación** | Descubrimiento de relaciones entre variables |
| 📅 **Distribución de Accesos** | Patrones de uso diarios y semanales |
| 👥 **Comparación de Grupos** | Métricas de rendimiento entre cohortes |
| 📈 **Tendencias Temporales** | Análisis de series temporales sobre 12 semanas |
| ⚙️ **Panel Personalizado** | Construye tu propio análisis con variables personalizadas |

### 3️⃣ Panel de Análisis Personalizado

1. Navega al **Panel Personalizado**
2. **Selecciona Variables**: inscripciones, accesos, grupos, cursos, etc.
3. **Elige Operación**: media, mediana, desv. estándar, cuenta, máx, mín
4. **Obtén Resultados Instantáneos** con salida formateada

---

## 🔧 Configuración

### Datos Mock Escalables

Carga datos en diferentes escalas para testing o producción:

```bash
# Escala completa (3,200 usuarios, 200 cursos)
docker compose exec web python manage.py load_mock_data --clear --scale -1

# Mitad (1,600 usuarios, 100 cursos)
docker compose exec web python manage.py load_mock_data --clear --scale -2

# Cuarto (800 usuarios, 50 cursos) - Para testing
docker compose exec web python manage.py load_mock_data --clear --scale -4
```

### Especificaciones de Datos Mock

| Componente | Detalles |
|------------|----------|
| **Programas Académicos** | 5 programas: Derecho, Economía, Ingeniería, Medicina, Arquitectura |
| **Modalidades** | 2 tipos: Grado, Postgrado |
| **Cursos** | 200 total: 100 primer cuatrimestre, 100 segundo cuatrimestre |
| **Estudiantes** | 3,200 con nombres y emails realistas |
| **Grupos** | 2-3 grupos por curso, 20-40 estudiantes cada uno |
| **Tasa de Acceso** | 70% simulando patrones de participación reales |

### Conectar a Base de Datos Moodle Real

Edita `config/settings.py` para agregar una base de datos secundaria:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='moodle_stats'),
        # ... tu base de datos Romanova
    },
    'moodle': {
        'ENGINE': 'django.db.backends.mysql',  # Moodle usa MySQL
        'NAME': 'moodle_produccion',
        'USER': 'moodle_user',
        'PASSWORD': 'password_seguro',
        'HOST': 'moodle-db.ejemplo.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

Crea un comando de management para importar datos desde Moodle a Romanova.

---

## 🛠️ Desarrollo

### Comandos Útiles

```bash
# Ver logs de la aplicación
docker compose logs -f web

# Acceder al shell de Django
docker compose exec web python manage.py shell

# Ejecutar tests
docker compose exec web python manage.py test

# Crear migraciones de base de datos
docker compose exec web python manage.py makemigrations

# Acceder al CLI de PostgreSQL
docker compose exec db psql -U msp_user -d moodle_stats

# Detener todos los servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Reconstruir contenedores
docker compose up -d --build
```

### Estructura del Proyecto

```
romanova/
├── apps/
│   ├── moodle/                    # Aplicación de reportes centrales
│   │   ├── models.py              # 8 modelos de datos Moodle
│   │   ├── views.py               # Panel, reportes, listas de usuarios
│   │   ├── urls.py                # Enrutamiento de URLs
│   │   └── management/commands/
│   │       └── load_mock_data.py  # Generador de datos mock
│   └── analytics/                 # Aplicación de análisis estadístico
│       ├── views.py               # 6 módulos de análisis
│       └── urls.py                # Enrutamiento de analytics
├── config/                        # Configuración del proyecto Django
│   ├── settings.py                # Configuración principal
│   ├── urls.py                    # Configuración de URLs raíz
│   ├── wsgi.py                    # Punto de entrada WSGI
│   └── asgi.py                    # Punto de entrada ASGI
├── templates/                     # Templates HTML
│   ├── base.html                  # Template base
│   ├── moodle/                    # Templates app moodle
│   └── analytics/                 # Templates analytics
├── static/                        # Archivos estáticos
│   ├── css/                       # Hojas de estilo
│   └── js/                        # JavaScript
├── docker-compose.yml             # Orquestación de contenedores
├── Dockerfile                     # Definición del contenedor Django
├── requirements.txt               # Dependencias Python
├── init.sh                        # Script de inicialización
└── manage.py                      # CLI de Django
```

---

## 📊 Modelo de Datos

```
Category (Programas, Modalidades)
    ↓ (1:N)
Course (200 cursos entre 5 programas)
    ↓ (1:N)
Group (2-3 grupos por curso)
    ↓ (M:N vía GroupMember)
MoodleUser (3,200 estudiantes)
    ↓ (1:N vía UserEnrolment)
Enrol (Métodos de inscripción)
    ↓ (1:N)
UserLastAccess (Seguimiento de actividad)
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Apreciamos:

- 🐛 Reportes y correcciones de bugs
- ✨ Solicitudes e implementaciones de características
- 📝 Mejoras en la documentación
- 🌍 Traducciones

### Cómo Contribuir

1. **Haz Fork** del repositorio
2. **Crea** una rama de feature
   ```bash
   git checkout -b feature/CaracteristicaIncreible
   ```
3. **Commitea** tus cambios
   ```bash
   git commit -m 'Agregar CaracteristicaIncreible'
   ```
4. **Pushea** a la rama
   ```bash
   git push origin feature/CaracteristicaIncreible
   ```
5. **Abre** un Pull Request

---

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para detalles.

```
Licencia MIT - Copyright (c) 2025 Carlos Dagorret
```

---

## 🙏 Agradecimientos

- **Sistema PHP Original**: gestoresapp
- **Django Software Foundation**: Por el increíble framework
- **PostgreSQL Global Development Group**: Por la robusta base de datos
- **Comunidad Moodle**: Por la inspiración y excelencia en LMS

---

## 📧 Contacto y Soporte

**Carlos Dagorret**
GitHub: [@dagorret](https://github.com/dagorret)
Proyecto: [https://github.com/dagorret/Romanva](https://github.com/dagorret/Romanva)

---

## 📸 Capturas de Pantalla

### Página de Login
*Interfaz de autenticación limpia y segura*

### Panel Principal
*Reportes semanales de acceso con filtrado y selección de rango de fechas*

### Menú de Análisis Estadístico
*Seis módulos especializados de análisis para insights profundos*

### Análisis de Correlación
*Descubre relaciones entre inscripciones, patrones de acceso y rendimiento*

---

<div align="center">

## 🌟 ¡Dale una estrella a este repo si te resulta útil!

**Hecho con ❤️ por Carlos Dagorret**

[⬆ Volver arriba](#-romanova-platform)

</div>

