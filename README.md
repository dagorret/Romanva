<div align="center">

# 🚀 Romanova Platform

### Advanced Statistical Analysis and Management Platform for Moodle LMS Data

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**[English](#english)** · **[Español](#español)**

---

### *Transform your Moodle data into actionable insights*

Comprehensive Django-based platform for analyzing, visualizing, and managing Moodle LMS data with **12 statistical analysis modules** including **6 advanced Machine Learning algorithms**.

[Get Started](#-quick-start) · [Features](#-key-features) · [ML Modules](#-machine-learning-modules)

</div>

---

## 🎯 What is Romanova Platform?

**Romanova Platform** is a comprehensive Django-based web application designed to **analyze, visualize, and manage Moodle LMS data** at scale. Born from the need to migrate and modernize a legacy PHP system, it combines enterprise-grade architecture with cutting-edge machine learning to deliver:

- 📊 **12 Statistical Analysis Modules** - 6 basic + 6 advanced ML-powered
- 📈 **Real-Time Reporting** - Weekly access reports with engagement tracking
- 🎓 **Scalable Data Management** - Handle 3,200+ users and 200+ courses efficiently
- 🤖 **Machine Learning** - Predictive analytics, clustering, PCA, and more
- 🐳 **Modern Stack** - Fully Dockerized PostgreSQL + Django deployment
- 🔒 **Enterprise Security** - CSRF protection, SQL injection prevention, secure sessions

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📊 Basic Statistical Analysis

- **Descriptive Statistics**
  Mean, median, max, min, standard deviation with visual charts

- **Correlation Analysis**
  Discover relationships between enrollments, access patterns, and performance

- **Temporal Distribution**
  Daily and weekly access pattern visualization with histograms

- **Group Comparison**
  Performance metrics across student cohorts

- **Trend Analysis**
  Time series analysis over configurable periods

- **Custom Dashboard**
  Build your own analysis with selectable variables and operations

</td>
<td width="50%">

### 🤖 Machine Learning Modules

- **Role Analysis by Course**
  120-day access tracking by role with weekly averages

- **Regression & Prediction**
  Linear regression with 4-week trend forecasting

- **Student Clustering**
  K-Means algorithm for behavioral pattern analysis

- **Survival Analysis**
  Retention and churn analysis by enrollment cohorts

- **Activity Heatmap**
  Temporal patterns by day of week and hour

- **PCA Analysis**
  Principal Component Analysis for dimensional reduction

</td>
</tr>
</table>

### 📈 Intelligent Reporting System

- **Weekly Access Reports** - Automated reports by course and group
- **Activity Tracking** - User engagement metrics and participation rates
- **Inactive Student Detection** - Automated alerts for students at risk
- **Data Export** - CSV/Excel export for further analysis
- **Category Filtering** - Filter by program (Grado, Postgrado, etc.)
- **Flexible Date Ranges** - Custom reporting periods
- **Role-based Analysis** - Separate metrics for students, teachers, and managers

---

## 🏗️ Architecture & Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    Romanova Platform                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend        │  Pure CSS (Bootstrap-inspired)           │
│  Backend         │  Django 5.1 (Python 3.12)                │
│  Database        │  PostgreSQL 16 Alpine                    │
│  Analytics       │  NumPy · Pandas · SciPy                  │
│  ML Engine       │  scikit-learn 1.6.1                      │
│  Visualization   │  Matplotlib · Seaborn                    │
│  Deployment      │  Docker + Docker Compose                 │
│  Security        │  Django Auth · CSRF · Session Management │
└─────────────────────────────────────────────────────────────┘
```

### 📦 Core Components

**Django Apps:**
- `apps.moodle` - Core reporting engine (migrated from PHP)
- `apps.analytics` - Statistical analysis with 12 modules

**Data Models (10 core models):**
- Category, Course, MoodleUser, Group, GroupMember
- Enrol, UserEnrolment, UserLastAccess
- Role, RoleAssignment

**Performance Features:**
- Bulk database operations for thousands of records
- Optimized queries with database indexes
- Connection pooling and caching ready
- Scalable mock data generation

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
- ✅ Generates role assignments (95% students, 4% teachers, 1% editors)

### 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Web Application** | http://localhost:8008 | `admin` / `admin123` |
| **Admin Panel** | http://localhost:8008/admin | `admin` / `admin123` |
| **Analytics Menu** | http://localhost:8008/analytics | `admin` / `admin123` |
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

### 2️⃣ Statistical Analysis Menu

Navigate to **http://localhost:8008/analytics** to access all 12 analysis modules:

#### 📊 Basic Analysis (6 modules)

| Module | URL | Description |
|--------|-----|-------------|
| **Descriptive Statistics** | `/analytics/descriptive/` | Mean, median, stddev with distribution charts |
| **Correlation Analysis** | `/analytics/correlation/` | Relationship discovery between variables |
| **Access Distribution** | `/analytics/distribution/` | Daily and weekly usage patterns |
| **Group Comparison** | `/analytics/comparison/` | Performance metrics across cohorts |
| **Temporal Trends** | `/analytics/trends/` | Time series analysis over periods |
| **Custom Panel** | `/analytics/custom/` | Build custom analysis with variables |

#### 🤖 Advanced ML Analysis (6 modules)

| Module | URL | Description | ML Algorithm |
|--------|-----|-------------|--------------|
| **Role Analysis** | `/analytics/roles/` | 120-day access by role with weekly averages | Statistical Aggregation |
| **Regression & Prediction** | `/analytics/regression/` | 4-week trend forecasting | Linear Regression (SciPy) |
| **Student Clustering** | `/analytics/clustering/` | Behavioral pattern grouping | K-Means (scikit-learn) |
| **Survival Analysis** | `/analytics/survival/` | Retention and churn by cohorts | Cohort Analysis |
| **Activity Heatmap** | `/analytics/heatmap/` | Day/hour temporal patterns | Frequency Distribution |
| **PCA Analysis** | `/analytics/pca/` | Dimensional reduction | PCA (scikit-learn) |

---

## 🤖 Machine Learning Modules

### 1. 👥 Role Analysis by Course

**Algorithm:** Statistical Aggregation
**Period:** Last 120 days (~17 weeks)

Analyzes access patterns separated by user roles:
- Tracks unique users per role
- Calculates total accesses
- Computes weekly averages
- Shows access per user metrics

**Use Cases:**
- Identify which roles are most active
- Compare teacher vs student engagement
- Detect unusual role-based patterns

### 2. 📉 Regression & Prediction

**Algorithm:** Linear Regression (SciPy)
**Period:** Last 90 days, predicts next 4 weeks

Forecasts future access trends using linear regression:
- Analyzes weekly access data
- Computes slope and R² (goodness of fit)
- Classifies trends: Growing, Declining, Stable
- Predicts next 4 weeks of activity

**Use Cases:**
- Forecast course demand
- Identify declining engagement early
- Plan resource allocation

### 3. 🎯 Student Clustering

**Algorithm:** K-Means (scikit-learn)
**Features:** 4 dimensions (accesses, courses, groups, frequency)

Groups students by behavioral patterns:
- Normalizes data with StandardScaler
- Applies K-Means with 3 clusters
- Classifies: Very Active, Moderately Active, Low Activity
- Shows average metrics per cluster

**Use Cases:**
- Identify at-risk students
- Target interventions by cluster
- Understand student behavior patterns

### 4. 📊 Survival Analysis

**Algorithm:** Cohort Retention Analysis
**Period:** Last 12 months by enrollment cohort

Analyzes student retention and churn:
- Groups by enrollment month
- Tracks active vs inactive students
- Calculates retention and churn rates
- Shows trends over time

**Use Cases:**
- Measure course retention
- Identify high-churn periods
- Improve student success rates

### 5. 🔥 Activity Heatmap

**Algorithm:** Frequency Distribution Matrix
**Dimensions:** 7 days × 24 hours

Visualizes temporal activity patterns:
- Creates day-of-week × hour matrix
- Identifies peak activity times
- Shows usage patterns visually
- Highlights low-activity periods

**Use Cases:**
- Optimize support coverage
- Schedule maintenance windows
- Understand user behavior patterns

### 6. 🧬 PCA Analysis

**Algorithm:** Principal Component Analysis (scikit-learn)
**Features:** 5 dimensions (enrollment, accesses, groups, engagement, age)

Reduces dimensional complexity:
- Standardizes course data
- Computes principal components
- Shows variance explained
- Projects courses onto PC space

**Use Cases:**
- Identify most important metrics
- Simplify complex data
- Find hidden patterns

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
| **Roles** | 95% students, 4% teachers, 1% editing teachers |
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

# Apply migrations
docker compose exec web python manage.py migrate

# Access PostgreSQL CLI
docker compose exec db psql -U msp_user -d moodle_stats

# Rebuild containers (after changing requirements.txt)
docker compose down && docker compose up -d --build

# Stop all services
docker compose down

# Restart services
docker compose restart
```

### Project Structure

```
romanova/
├── apps/
│   ├── moodle/                    # Core reporting application
│   │   ├── models.py              # 10 Moodle data models
│   │   ├── views.py               # Panel, reports, user lists
│   │   ├── urls.py                # URL routing
│   │   ├── admin.py               # Admin interface
│   │   └── management/commands/
│   │       └── load_mock_data.py  # Mock data generator
│   └── analytics/                 # Statistical analysis application
│       ├── views.py               # 12 analysis modules (6 basic + 6 ML)
│       └── urls.py                # Analytics routing
├── config/                        # Django project settings
│   ├── settings.py                # Main configuration
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── moodle/                    # Moodle app templates
│   └── analytics/                 # Analytics templates (12 modules)
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

Role (Student, Teacher, Editor)
    ↓ (1:N via RoleAssignment)
MoodleUser ↔ Course (role assignments)
```

---

## 📦 Dependencies

### Core Framework
- **Django 5.1** - Web framework
- **psycopg2-binary 2.9.10** - PostgreSQL adapter
- **python-decouple 3.8** - Configuration management
- **django-extensions 3.2.3** - Django utilities

### Statistical Analysis
- **numpy 2.2.1** - Numerical computing
- **pandas 2.2.3** - Data analysis and manipulation
- **scipy 1.15.0** - Scientific computing (linear regression)

### Machine Learning
- **scikit-learn 1.6.1** - ML algorithms (K-Means, PCA, StandardScaler)

### Visualization
- **matplotlib 3.10.0** - Plotting library
- **seaborn 0.13.2** - Statistical visualizations

### Data Export
- **openpyxl 3.1.5** - Excel file generation

### Database
- **PostgreSQL 16 Alpine** - Production database

---

## 🤝 Contributing

Contributions are welcome! We appreciate:

- 🐛 Bug reports and fixes
- ✨ Feature requests and implementations
- 📝 Documentation improvements
- 🤖 New ML algorithms
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
- **scikit-learn Community**: For world-class ML tools
- **Moodle Community**: For inspiration and LMS excellence

---

## 📧 Contact & Support

**Carlos Dagorret**
- GitHub: [@dagorret](https://github.com/dagorret)
- Project: [https://github.com/dagorret/Romanva](https://github.com/dagorret/Romanva)

---

## 🔗 References & Documentation

### Machine Learning Libraries
- [scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html) - K-Means, PCA, StandardScaler
- [SciPy Documentation](https://docs.scipy.org/doc/scipy/) - Linear regression (stats.linregress)
- [NumPy Documentation](https://numpy.org/doc/stable/) - Numerical operations
- [Pandas Documentation](https://pandas.pydata.org/docs/) - Data manipulation

### Visualization
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html) - Plotting
- [Seaborn Documentation](https://seaborn.pydata.org/) - Statistical visualization

### Framework & Database
- [Django 5.1 Documentation](https://docs.djangoproject.com/en/5.1/) - Web framework
- [PostgreSQL 16 Documentation](https://www.postgresql.org/docs/16/) - Database

### Algorithms Used
- **K-Means Clustering**: [sklearn.cluster.KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- **Principal Component Analysis**: [sklearn.decomposition.PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- **Standard Scaler**: [sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- **Linear Regression**: [scipy.stats.linregress](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)

---

<div align="center">

## 🌟 Star this repo if you find it useful!

**12 Statistical Modules · 6 ML Algorithms · Enterprise Ready**

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
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)](LICENSE)

**[English](#english)** · **[Español](#español)**

---

### *Transforma tus datos de Moodle en insights accionables*

Plataforma integral basada en Django para analizar, visualizar y gestionar datos de Moodle LMS con **12 módulos de análisis estadístico** incluyendo **6 algoritmos avanzados de Machine Learning**.

[Comenzar](#-inicio-rápido) · [Características](#-características-principales) · [Módulos ML](#-módulos-de-machine-learning)

</div>

---

## 🎯 ¿Qué es Romanova Platform?

**Romanova Platform** es una aplicación web integral basada en Django diseñada para **analizar, visualizar y gestionar datos de Moodle LMS** a escala. Nacida de la necesidad de migrar y modernizar un sistema PHP heredado, combina arquitectura de nivel empresarial con machine learning de vanguardia para entregar:

- 📊 **12 Módulos de Análisis Estadístico** - 6 básicos + 6 avanzados con ML
- 📈 **Reportes en Tiempo Real** - Reportes semanales de acceso con seguimiento de participación
- 🎓 **Gestión de Datos Escalable** - Maneja 3,200+ usuarios y 200+ cursos eficientemente
- 🤖 **Machine Learning** - Análisis predictivo, clustering, PCA y más
- 🐳 **Stack Moderno** - Despliegue completamente Dockerizado PostgreSQL + Django
- 🔒 **Seguridad Empresarial** - Protección CSRF, prevención de SQL injection, sesiones seguras

---

## ✨ Características Principales

<table>
<tr>
<td width="50%">

### 📊 Análisis Estadístico Básico

- **Estadísticas Descriptivas**
  Media, mediana, máx, mín, desviación estándar con gráficos

- **Análisis de Correlación**
  Descubre relaciones entre inscripciones, patrones de acceso y rendimiento

- **Distribución Temporal**
  Visualización de patrones de acceso diarios y semanales

- **Comparación de Grupos**
  Métricas de rendimiento entre cohortes de estudiantes

- **Análisis de Tendencias**
  Análisis de series temporales en períodos configurables

- **Panel Personalizado**
  Construye tu análisis con variables y operaciones seleccionables

</td>
<td width="50%">

### 🤖 Módulos de Machine Learning

- **Análisis de Roles por Curso**
  Seguimiento de accesos de 120 días por rol con promedios semanales

- **Regresión y Predicción**
  Regresión lineal con pronóstico de tendencias a 4 semanas

- **Clustering de Estudiantes**
  Algoritmo K-Means para análisis de patrones de comportamiento

- **Análisis de Supervivencia**
  Análisis de retención y abandono por cohortes de inscripción

- **Mapa de Calor de Actividad**
  Patrones temporales por día de semana y hora

- **Análisis PCA**
  Análisis de Componentes Principales para reducción dimensional

</td>
</tr>
</table>

### 📈 Sistema de Reportes Inteligente

- **Reportes de Acceso Semanales** - Reportes automatizados por curso y grupo
- **Seguimiento de Actividad** - Métricas de participación y tasas de compromiso
- **Detección de Estudiantes Inactivos** - Alertas automatizadas para estudiantes en riesgo
- **Exportación de Datos** - Exportación a CSV/Excel para análisis adicional
- **Filtrado por Categoría** - Filtrar por programa (Grado, Postgrado, etc.)
- **Rangos de Fecha Flexibles** - Períodos de reporte personalizados
- **Análisis Basado en Roles** - Métricas separadas para estudiantes, profesores y gestores

---

## 🏗️ Arquitectura y Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    Romanova Platform                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend        │  CSS Puro (inspirado en Bootstrap)      │
│  Backend         │  Django 5.1 (Python 3.12)                │
│  Base de Datos   │  PostgreSQL 16 Alpine                    │
│  Análisis        │  NumPy · Pandas · SciPy                  │
│  Motor ML        │  scikit-learn 1.6.1                      │
│  Visualización   │  Matplotlib · Seaborn                    │
│  Despliegue      │  Docker + Docker Compose                 │
│  Seguridad       │  Django Auth · CSRF · Gestión de Sesión  │
└─────────────────────────────────────────────────────────────┘
```

### 📦 Componentes Principales

**Apps Django:**
- `apps.moodle` - Motor de reportes central (migrado desde PHP)
- `apps.analytics` - Análisis estadístico con 12 módulos

**Modelos de Datos (10 modelos core):**
- Category, Course, MoodleUser, Group, GroupMember
- Enrol, UserEnrolment, UserLastAccess
- Role, RoleAssignment

**Características de Rendimiento:**
- Operaciones masivas en base de datos para miles de registros
- Consultas optimizadas con índices de base de datos
- Connection pooling y caching listos
- Generación de datos mock escalable

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
- ✅ Genera asignaciones de roles (95% estudiantes, 4% profesores, 1% editores)

### 🌐 Puntos de Acceso

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **Aplicación Web** | http://localhost:8008 | `admin` / `admin123` |
| **Panel Admin** | http://localhost:8008/admin | `admin` / `admin123` |
| **Menú Analytics** | http://localhost:8008/analytics | `admin` / `admin123` |
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

### 2️⃣ Menú de Análisis Estadístico

Navega a **http://localhost:8008/analytics** para acceder a los 12 módulos de análisis:

#### 📊 Análisis Básicos (6 módulos)

| Módulo | URL | Descripción |
|--------|-----|-------------|
| **Estadísticas Descriptivas** | `/analytics/descriptive/` | Media, mediana, desv. est. con gráficos |
| **Análisis de Correlación** | `/analytics/correlation/` | Descubrimiento de relaciones entre variables |
| **Distribución de Accesos** | `/analytics/distribution/` | Patrones de uso diarios y semanales |
| **Comparación de Grupos** | `/analytics/comparison/` | Métricas de rendimiento entre cohortes |
| **Tendencias Temporales** | `/analytics/trends/` | Análisis de series temporales |
| **Panel Personalizado** | `/analytics/custom/` | Construye análisis personalizados |

#### 🤖 Análisis Avanzados ML (6 módulos)

| Módulo | URL | Descripción | Algoritmo ML |
|--------|-----|-------------|--------------|
| **Análisis de Roles** | `/analytics/roles/` | Accesos de 120 días por rol con promedios | Agregación Estadística |
| **Regresión y Predicción** | `/analytics/regression/` | Pronóstico de tendencias a 4 semanas | Regresión Lineal (SciPy) |
| **Clustering Estudiantes** | `/analytics/clustering/` | Agrupamiento por patrones de comportamiento | K-Means (scikit-learn) |
| **Análisis Supervivencia** | `/analytics/survival/` | Retención y abandono por cohortes | Análisis de Cohortes |
| **Mapa de Calor** | `/analytics/heatmap/` | Patrones temporales día/hora | Distribución de Frecuencia |
| **Análisis PCA** | `/analytics/pca/` | Reducción dimensional | PCA (scikit-learn) |

---

## 🤖 Módulos de Machine Learning

### 1. 👥 Análisis de Roles por Curso

**Algoritmo:** Agregación Estadística
**Período:** Últimos 120 días (~17 semanas)

Analiza patrones de acceso separados por roles de usuario:
- Rastrea usuarios únicos por rol
- Calcula accesos totales
- Computa promedios semanales
- Muestra métricas de acceso por usuario

**Casos de Uso:**
- Identificar qué roles son más activos
- Comparar participación profesor vs estudiante
- Detectar patrones inusuales basados en roles

### 2. 📉 Regresión y Predicción

**Algoritmo:** Regresión Lineal (SciPy)
**Período:** Últimos 90 días, predice próximas 4 semanas

Pronostica tendencias futuras de acceso usando regresión lineal:
- Analiza datos de acceso semanales
- Calcula pendiente y R² (bondad de ajuste)
- Clasifica tendencias: Creciente, Decreciente, Estable
- Predice próximas 4 semanas de actividad

**Casos de Uso:**
- Pronosticar demanda de cursos
- Identificar participación decreciente temprano
- Planificar asignación de recursos

### 3. 🎯 Clustering de Estudiantes

**Algoritmo:** K-Means (scikit-learn)
**Características:** 4 dimensiones (accesos, cursos, grupos, frecuencia)

Agrupa estudiantes por patrones de comportamiento:
- Normaliza datos con StandardScaler
- Aplica K-Means con 3 clusters
- Clasifica: Muy Activos, Moderadamente Activos, Baja Actividad
- Muestra métricas promedio por cluster

**Casos de Uso:**
- Identificar estudiantes en riesgo
- Dirigir intervenciones por cluster
- Entender patrones de comportamiento estudiantil

### 4. 📊 Análisis de Supervivencia

**Algoritmo:** Análisis de Retención por Cohortes
**Período:** Últimos 12 meses por cohorte de inscripción

Analiza retención y abandono de estudiantes:
- Agrupa por mes de inscripción
- Rastrea estudiantes activos vs inactivos
- Calcula tasas de retención y abandono
- Muestra tendencias en el tiempo

**Casos de Uso:**
- Medir retención de cursos
- Identificar períodos de alto abandono
- Mejorar tasas de éxito estudiantil

### 5. 🔥 Mapa de Calor de Actividad

**Algoritmo:** Matriz de Distribución de Frecuencia
**Dimensiones:** 7 días × 24 horas

Visualiza patrones de actividad temporal:
- Crea matriz día de semana × hora
- Identifica picos de actividad
- Muestra patrones de uso visualmente
- Resalta períodos de baja actividad

**Casos de Uso:**
- Optimizar cobertura de soporte
- Programar ventanas de mantenimiento
- Entender patrones de comportamiento de usuarios

### 6. 🧬 Análisis PCA

**Algoritmo:** Análisis de Componentes Principales (scikit-learn)
**Características:** 5 dimensiones (inscripción, accesos, grupos, engagement, edad)

Reduce complejidad dimensional:
- Estandariza datos de cursos
- Calcula componentes principales
- Muestra varianza explicada
- Proyecta cursos en espacio PC

**Casos de Uso:**
- Identificar métricas más importantes
- Simplificar datos complejos
- Encontrar patrones ocultos

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
| **Roles** | 95% estudiantes, 4% profesores, 1% editores |
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

# Aplicar migraciones
docker compose exec web python manage.py migrate

# Acceder al CLI de PostgreSQL
docker compose exec db psql -U msp_user -d moodle_stats

# Reconstruir contenedores (después de cambiar requirements.txt)
docker compose down && docker compose up -d --build

# Detener todos los servicios
docker compose down

# Reiniciar servicios
docker compose restart
```

### Estructura del Proyecto

```
romanova/
├── apps/
│   ├── moodle/                    # Aplicación de reportes centrales
│   │   ├── models.py              # 10 modelos de datos Moodle
│   │   ├── views.py               # Panel, reportes, listas de usuarios
│   │   ├── urls.py                # Enrutamiento de URLs
│   │   ├── admin.py               # Interfaz admin
│   │   └── management/commands/
│   │       └── load_mock_data.py  # Generador de datos mock
│   └── analytics/                 # Aplicación de análisis estadístico
│       ├── views.py               # 12 módulos (6 básicos + 6 ML)
│       └── urls.py                # Enrutamiento analytics
├── config/                        # Configuración del proyecto Django
│   ├── settings.py                # Configuración principal
│   ├── urls.py                    # Configuración de URLs raíz
│   ├── wsgi.py                    # Punto de entrada WSGI
│   └── asgi.py                    # Punto de entrada ASGI
├── templates/                     # Templates HTML
│   ├── base.html                  # Template base
│   ├── moodle/                    # Templates app moodle
│   └── analytics/                 # Templates analytics (12 módulos)
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

Role (Estudiante, Profesor, Editor)
    ↓ (1:N vía RoleAssignment)
MoodleUser ↔ Course (asignaciones de roles)
```

---

## 📦 Dependencias

### Framework Core
- **Django 5.1** - Framework web
- **psycopg2-binary 2.9.10** - Adaptador PostgreSQL
- **python-decouple 3.8** - Gestión de configuración
- **django-extensions 3.2.3** - Utilidades Django

### Análisis Estadístico
- **numpy 2.2.1** - Computación numérica
- **pandas 2.2.3** - Análisis y manipulación de datos
- **scipy 1.15.0** - Computación científica (regresión lineal)

### Machine Learning
- **scikit-learn 1.6.1** - Algoritmos ML (K-Means, PCA, StandardScaler)

### Visualización
- **matplotlib 3.10.0** - Biblioteca de gráficos
- **seaborn 0.13.2** - Visualizaciones estadísticas

### Exportación de Datos
- **openpyxl 3.1.5** - Generación de archivos Excel

### Base de Datos
- **PostgreSQL 16 Alpine** - Base de datos de producción

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Apreciamos:

- 🐛 Reportes y correcciones de bugs
- ✨ Solicitudes e implementaciones de características
- 📝 Mejoras en la documentación
- 🤖 Nuevos algoritmos de ML
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
- **Comunidad scikit-learn**: Por herramientas ML de clase mundial
- **Comunidad Moodle**: Por la inspiración y excelencia en LMS

---

## 📧 Contacto y Soporte

**Carlos Dagorret**
- GitHub: [@dagorret](https://github.com/dagorret)
- Proyecto: [https://github.com/dagorret/Romanva](https://github.com/dagorret/Romanva)

---

## 🔗 Referencias y Documentación

### Bibliotecas de Machine Learning
- [Documentación scikit-learn](https://scikit-learn.org/stable/documentation.html) - K-Means, PCA, StandardScaler
- [Documentación SciPy](https://docs.scipy.org/doc/scipy/) - Regresión lineal (stats.linregress)
- [Documentación NumPy](https://numpy.org/doc/stable/) - Operaciones numéricas
- [Documentación Pandas](https://pandas.pydata.org/docs/) - Manipulación de datos

### Visualización
- [Documentación Matplotlib](https://matplotlib.org/stable/contents.html) - Gráficos
- [Documentación Seaborn](https://seaborn.pydata.org/) - Visualización estadística

### Framework y Base de Datos
- [Documentación Django 5.1](https://docs.djangoproject.com/en/5.1/) - Framework web
- [Documentación PostgreSQL 16](https://www.postgresql.org/docs/16/) - Base de datos

### Algoritmos Utilizados
- **Clustering K-Means**: [sklearn.cluster.KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- **Análisis de Componentes Principales**: [sklearn.decomposition.PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- **Escalador Estándar**: [sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- **Regresión Lineal**: [scipy.stats.linregress](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)

---

<div align="center">

## 🌟 ¡Dale una estrella a este repo si te resulta útil!

**12 Módulos Estadísticos · 6 Algoritmos ML · Listo para Producción**

**Hecho con ❤️ por Carlos Dagorret**

[⬆ Volver arriba](#-romanova-platform)

</div>
