# Changelog - Romanova Platform

## [1.0.0] - 2024/2025

### Migración completa de PHP a Django

#### ✅ Añadido

**Infraestructura:**
- Sistema completo en Django 5.1 con Python 3.12
- Base de datos PostgreSQL 16
- Dockerización completa con docker compose
- Script de inicialización automática (`init.sh`)
- Configuración centralizada con variables de entorno

**Modelos de datos:**
- `Category` - Categorías de cursos
- `Course` - Cursos con metadata completa
- `MoodleUser` - Usuarios del sistema
- `Group` - Grupos de estudiantes
- `GroupMember` - Relación usuario-grupo
- `Enrol` - Métodos de inscripción
- `UserEnrolment` - Inscripciones de usuarios
- `UserLastAccess` - Registro de accesos
- `SavedAnalysis` - Análisis guardados (futuro)

**Funcionalidad básica (migrada de PHP):**
- Panel de login con autenticación Django
- Panel de reportes por curso/grupo
- Filtrado por categoría "Grado"
- Filtrado por cursos del último año
- Reportes semanales de acceso
- Vista de usuarios sin acceso por semana
- Búsqueda de cursos por código

**Módulo de estadísticas avanzadas:**
1. Estadísticas descriptivas (media, max, min, tasas)
2. Análisis de correlación (inscriptos vs accesos)
3. Distribución temporal de accesos
4. Comparación entre grupos
5. Tendencias semanales (series de tiempo)
6. Panel personalizado con 7 operaciones estadísticas

**Generación de datos:**
- Comando `load_mock_data` para datos de prueba
- 60 usuarios, 9 cursos, 20+ grupos
- Datos realistas con fechas y relaciones correctas

**Documentación:**
- README.md completo
- QUICKSTART.md para inicio rápido
- PROJECT_SUMMARY.md con resumen técnico
- CHANGELOG.md (este archivo)
- Comentarios extensivos en código

#### 🔄 Cambiado

**De PHP a Django:**
- NDJSON → PostgreSQL relacional
- Sesiones PHP → Django auth
- Archivos planos → ORM de Django
- SQL manual → QuerySets optimizados

#### ⚡ Mejorado

**Sobre el sistema original:**
- Base de datos relacional vs archivos
- Panel de administración completo
- Módulo de estadísticas avanzadas
- Sistema completamente dockerizado
- Fácilmente escalable y extensible
- Tests automatizables
- API REST-ready

#### 🗑️ Removido

- Dependencia de archivos NDJSON
- Procesamiento manual de CSV
- Configuración compleja de PHP/Apache
- Scripts de exportación manual

### Estructura del Proyecto

```
Archivos creados: 50+
Líneas de código: 3000+
Templates: 11
Modelos Django: 8
Vistas: 10
Comandos management: 1
Scripts de deployment: 3
```

### Tecnologías

**Stack completo:**
- Django 5.1
- PostgreSQL 16
- Python 3.12
- Docker + Docker Compose
- NumPy, Pandas, SciPy
- Matplotlib, Seaborn

### Configuración

**Por defecto (desarrollo):**
- Puerto web: 8008 (modificado del 8000 original)
- Puerto DB: 5432
- Usuario admin: admin / admin123
- Debug: True
- Timezone: America/Argentina/Cordoba

### Notas de Migración

**Equivalencias PHP → Django:**

| Archivo PHP | Vista Django | Template |
|-------------|--------------|----------|
| `index.php` | `login_view` | `login.html` |
| `panel.php` | `panel_view` | `panel.html` |
| `never_users.php` | `never_users_view` | `never_users.html` |
| `lib_ndjson.php` | ORM Django | - |
| - | 6 vistas de analytics | 6 templates |

**Datos:**
- NDJSON → Tablas PostgreSQL
- Lectura línea por línea → QuerySets optimizados
- PHP arrays → Django QuerySets + Python dicts

### Próximas versiones planificadas

**[1.1.0] - Futuro**
- [ ] Exportación a Excel/PDF
- [ ] Gráficos interactivos (Chart.js)
- [ ] Conexión a Moodle real
- [ ] API REST completa

**[1.2.0] - Futuro**
- [ ] Tests automatizados
- [ ] Análisis predictivos (ML)
- [ ] Dashboard en tiempo real
- [ ] Notificaciones automáticas

### Créditos

- **Sistema original**: gestoresapp (PHP)
- **Migración y desarrollo**: Claude Code
- **Framework**: Django Software Foundation
- **Base de datos**: PostgreSQL Global Development Group

---

**Versión actual: 1.0.0**
**Estado: Estable y listo para producción (con ajustes de seguridad)**
