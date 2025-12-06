# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2024-12-06

### Añadido
- Sistema completo de importación desde Moodle
- 10 modelos Django para tablas de Moodle:
  - courses (Cursos)
  - categories (Categorías)
  - enrol (Métodos de inscripción)
  - user_enrolments (Inscripciones de usuarios)
  - users (Usuarios)
  - groups (Grupos)
  - groups_members (Miembros de grupos)
  - user_lastaccess (Último acceso)
  - role_assignments (Asignaciones de roles)
  - context (Contextos)
- Admin de Django personalizado con:
  - Botón "Importar desde Moodle" en cada tabla
  - Acción "Exportar a Excel" para registros seleccionados
  - Filtros y búsqueda en todas las tablas
  - Modelo ImportLog para tracking de importaciones
- Management command `import_moodle` para CLI
- Docker + Docker Compose con volúmenes persistentes
- Script de instalación automática (`install.sh`)
- Script de prueba de conexión (`test_connection.py`)
- Documentación completa:
  - README.md (guía de usuario)
  - ADMIN_API.md (documentación del admin)
  - PROJECT_SUMMARY.md (resumen ejecutivo)
  - config.example.env (ejemplo de configuración)

### Características Técnicas
- Importación en lotes (batch insert) para rendimiento
- Transacciones atómicas para integridad de datos
- Logs detallados de importaciones con estado y errores
- Exportación a Excel con formato profesional
- Hot-reload en desarrollo
- Healthcheck en Docker

## [Próximas Versiones]

### Planeado para [1.1.0]
- [ ] Importación incremental (solo nuevos registros)
- [ ] Programación de importaciones automáticas (cron)
- [ ] Dashboard con estadísticas y gráficos
- [ ] Soporte para PostgreSQL
- [ ] API REST para consultas
- [ ] Exportación a CSV
- [ ] Filtros avanzados en el admin

### Planeado para [1.2.0]
- [ ] Sistema de reportes personalizables
- [ ] Comparación entre importaciones
- [ ] Alertas por email cuando termine importación
- [ ] Soporte para más tablas de Moodle
- [ ] Importación parcial (rangos de IDs)
- [ ] Compresión de exports grandes

### Planeado para [2.0.0]
- [ ] Interfaz web (no solo admin)
- [ ] Visualizaciones interactivas
- [ ] Sistema de permisos granular
- [ ] Multi-tenancy (múltiples Moodles)
- [ ] Cache de queries frecuentes
- [ ] Integración con APIs de análisis

## Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Versionado

Usamos [SemVer](http://semver.org/) para versionado. Para las versiones disponibles, 
mira los [tags en este repositorio](https://github.com/tu-usuario/moodle-stats/tags).

[1.0.0]: https://github.com/tu-usuario/moodle-stats/releases/tag/v1.0.0
