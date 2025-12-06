# API del Admin de Moodle Stats

Este documento describe las funcionalidades disponibles en el admin de Django.

## Tablas Disponibles

### 1. Logs de Importación
**URL:** `/admin/moodledata/importlog/`

Muestra el historial de todas las importaciones realizadas:
- Tabla importada
- Fecha/hora de inicio y fin
- Estado (En progreso, Completada, Fallida)
- Número de registros importados
- Mensajes de error (si los hay)

**Permisos:** Solo lectura

### 2. Cursos
**URL:** `/admin/moodledata/course/`

Gestión de cursos de Moodle.

**Campos:**
- ID Moodle
- Nombre corto
- Nombre completo
- Categoría
- Fecha inicio/fin (timestamp)
- Visible

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Filtrar por visibilidad y categoría
- Buscar por nombre

### 3. Categorías
**URL:** `/admin/moodledata/category/`

Gestión de categorías de cursos.

**Campos:**
- ID Moodle
- Nombre
- Categoría padre
- Ruta
- Visible

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Filtrar por visibilidad
- Buscar por nombre

### 4. Métodos de Inscripción
**URL:** `/admin/moodledata/enrol/`

Gestión de métodos de inscripción en cursos.

**Campos:**
- ID Moodle
- ID Curso
- Método (manual, self, etc.)
- Estado

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Filtrar por método y estado
- Buscar por ID de curso

### 5. Inscripciones de Usuarios
**URL:** `/admin/moodledata/userenrolment/`

Gestión de inscripciones de usuarios en cursos.

**Campos:**
- ID Moodle
- ID Usuario
- ID Inscripción
- Tiempo inicio/fin (timestamp)
- Estado

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Filtrar por estado
- Buscar por ID de usuario o inscripción

### 6. Usuarios
**URL:** `/admin/moodledata/user/`

Gestión de usuarios de Moodle.

**Campos:**
- ID Moodle
- Nombre de usuario
- Nombre
- Apellido
- Email
- Ciudad
- País
- Suspendido
- Eliminado

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Filtrar por suspendido y país
- Buscar por nombre de usuario, nombre, apellido o email

### 7. Grupos
**URL:** `/admin/moodledata/group/`

Gestión de grupos de cursos.

**Campos:**
- ID Moodle
- ID Curso
- Nombre
- Número ID

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Buscar por nombre o número ID

### 8. Miembros de Grupos
**URL:** `/admin/moodledata/groupmember/`

Gestión de miembros de grupos.

**Campos:**
- ID Moodle
- ID Grupo
- ID Usuario

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Buscar por ID de grupo o usuario

### 9. Último Acceso de Usuarios
**URL:** `/admin/moodledata/userlastaccess/`

Registro de último acceso de usuarios a cursos.

**Campos:**
- ID Moodle
- ID Usuario
- ID Curso
- Tiempo de acceso (timestamp)

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Buscar por ID de usuario o curso

### 10. Asignaciones de Roles
**URL:** `/admin/moodledata/roleassignment/`

Gestión de asignaciones de roles a usuarios.

**Campos:**
- ID Moodle
- ID Rol
- ID Contexto
- ID Usuario
- Tiempo modificado (timestamp)
- ID Modificador

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Buscar por ID de usuario o rol

### 11. Contextos
**URL:** `/admin/moodledata/context/`

Gestión de contextos de Moodle.

**Campos:**
- ID Moodle
- Nivel de contexto
- ID Instancia
- Ruta
- Profundidad

**Acciones disponibles:**
- Importar desde Moodle
- Exportar a Excel
- Filtrar por nivel de contexto
- Buscar por ID de instancia

## Flujo de Trabajo Típico

### 1. Primera Importación

1. Accede al admin: http://localhost:8008/admin/
2. Entra a "Usuarios" (o la tabla que quieras importar)
3. Haz clic en "Importar desde Moodle" (botón verde arriba a la derecha)
4. Confirma la importación
5. Espera a que termine (se mostrará un mensaje de éxito)
6. Repite para otras tablas

### 2. Ver Datos Importados

1. En el admin, entra a cualquier tabla
2. Verás la lista de registros importados
3. Usa los filtros y búsqueda para encontrar lo que necesitas
4. Haz clic en un registro para ver sus detalles

### 3. Exportar a Excel

1. En la lista de registros, selecciona los que quieres exportar (checkboxes)
2. En el menú desplegable "Acción", selecciona "Exportar seleccionados a Excel"
3. Haz clic en "Go"
4. Se descargará un archivo Excel

### 4. Verificar Importaciones

1. Ve a "Logs de Importación"
2. Verás todas las importaciones realizadas
3. Revisa el estado y número de registros
4. Si algo falló, verás el mensaje de error

## Automatización

### Importar Todas las Tablas desde CLI

```bash
docker-compose exec web python manage.py import_moodle
```

### Importar Tablas Específicas

```bash
docker-compose exec web python manage.py import_moodle --tables users,courses,groups
```

### Programar Importaciones Automáticas

Puedes usar cron para programar importaciones automáticas:

```bash
# Editar crontab
crontab -e

# Importar todos los días a las 2 AM
0 2 * * * cd /ruta/a/moodle-stats && docker-compose exec -T web python manage.py import_moodle >> /var/log/moodle-import.log 2>&1
```

## Personalización del Admin

### Cambiar Campos Mostrados

Edita `moodledata/admin.py` y modifica `list_display`:

```python
@admin.register(User)
class UserAdmin(MoodleImportMixin, ExportToExcelMixin, admin.ModelAdmin):
    list_display = ('moodle_id', 'username', 'email', 'imported_at')  # Agregar/quitar campos
```

### Agregar Filtros

Edita `list_filter`:

```python
list_filter = ('suspended', 'country', 'city')  # Agregar más filtros
```

### Cambiar Campos de Búsqueda

Edita `search_fields`:

```python
search_fields = ('username', 'email', 'firstname', 'lastname', 'city')  # Más campos
```

## Consideraciones de Rendimiento

### Importación de Tablas Grandes

Las tablas con muchos registros (100k+) pueden tardar varios minutos:
- `users`: ~5-10 minutos
- `user_enrolments`: ~10-15 minutos
- `role_assignments`: ~5-10 minutos

**Recomendación:** Usa el comando CLI en lugar del admin para tablas grandes.

### Exportación a Excel

Excel tiene un límite de ~1 millón de filas. Si necesitas exportar más:
1. Usa filtros para reducir el conjunto de datos
2. Exporta en múltiples archivos
3. O considera usar CSV en lugar de Excel

## Seguridad

### Permisos

Por defecto, solo los superusuarios pueden:
- Importar datos desde Moodle
- Ver logs de importación
- Exportar a Excel

Para dar permisos a otros usuarios:
1. En el admin, ve a "Usuarios"
2. Edita el usuario
3. Marca "Es staff" para darle acceso al admin
4. Asigna permisos específicos según necesidad

### Datos Sensibles

Ten cuidado con:
- Emails de usuarios
- Información personal
- No compartas exportaciones con personas no autorizadas
