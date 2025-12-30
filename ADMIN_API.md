# Admin y API - Romanova Platform

## Panel de Administración de Django

El sistema incluye el panel de administración completo de Django con todos los modelos registrados.

### Acceso al Admin

**URL**: http://localhost:8008/admin

**Credenciales por defecto**:
- Usuario: `admin`
- Contraseña: `admin123`

### Modelos Disponibles en Admin

#### App: Moodle (Datos de Moodle)

1. **Categorías** (`Category`)
   - Campos: name, path, parent, depth
   - Búsqueda por: name, path
   - Filtros: depth

2. **Cursos** (`Course`)
   - Campos: shortname, fullname, category, startdate, enddate, visible
   - Búsqueda por: shortname, fullname
   - Filtros: category, visible, startdate
   - Jerarquía temporal: startdate

3. **Usuarios de Moodle** (`MoodleUser`)
   - Campos: username, firstname, lastname, email
   - Búsqueda por: username, firstname, lastname, email
   - Orden: lastname, firstname

4. **Grupos** (`Group`)
   - Campos: name, course, description
   - Búsqueda por: name, course__shortname, course__fullname
   - Filtros: course

5. **Miembros de Grupos** (`GroupMember`)
   - Campos: group, user, timeadded
   - Búsqueda por: user__username, user__lastname, group__name
   - Filtros: group__course, timeadded
   - Jerarquía temporal: timeadded

6. **Métodos de Inscripción** (`Enrol`)
   - Campos: course, enrol, status
   - Búsqueda por: course__shortname, course__fullname
   - Filtros: enrol, status

7. **Inscripciones de Usuarios** (`UserEnrolment`)
   - Campos: enrol, user, timestart, timeend, timecreated
   - Búsqueda por: user__username, user__lastname, enrol__course__shortname
   - Filtros: enrol__course, timestart
   - Jerarquía temporal: timecreated

8. **Últimos Accesos** (`UserLastAccess`)
   - Campos: user, course, timeaccess
   - Búsqueda por: user__username, user__lastname, course__shortname
   - Filtros: course, timeaccess
   - Jerarquía temporal: timeaccess
   - Índices optimizados para consultas rápidas

#### App: Analytics (Análisis Estadísticos)

1. **Análisis Guardados** (`SavedAnalysis`)
   - Campos: name, description, analysis_type, parameters, created_at, updated_at
   - Búsqueda por: name, description
   - Filtros: analysis_type, created_at
   - Jerarquía temporal: created_at

### Operaciones Comunes en Admin

#### Crear Curso Nuevo
1. Admin → Cursos → Añadir curso
2. Completar: shortname, fullname, category
3. Opcional: startdate, enddate
4. Guardar

#### Agregar Usuario a Grupo
1. Admin → Miembros de grupos → Añadir miembro de grupo
2. Seleccionar grupo
3. Seleccionar usuario
4. Guardar

#### Ver Accesos de un Usuario
1. Admin → Últimos accesos al curso
2. Buscar por username o apellido
3. Ver lista de accesos por curso

#### Filtrar Cursos por Categoría
1. Admin → Cursos
2. Panel derecho → Filtros → Seleccionar categoría
3. Ver cursos filtrados

## API REST (Preparado para implementación)

El sistema está listo para agregar Django REST Framework.

### Instalación de DRF (opcional)

```bash
# Agregar a requirements.txt
djangorestframework==3.14.0
django-filter==24.3

# Instalar
docker-compose exec web pip install djangorestframework django-filter

# Agregar a INSTALLED_APPS en settings.py
'rest_framework',
'django_filters',
```

### Endpoints Sugeridos

#### Cursos
```
GET    /api/courses/              # Listar cursos
GET    /api/courses/{id}/         # Detalle de curso
POST   /api/courses/              # Crear curso
PUT    /api/courses/{id}/         # Actualizar curso
DELETE /api/courses/{id}/         # Eliminar curso
GET    /api/courses/{id}/groups/  # Grupos del curso
GET    /api/courses/{id}/stats/   # Estadísticas del curso
```

#### Usuarios
```
GET    /api/users/                # Listar usuarios
GET    /api/users/{id}/           # Detalle de usuario
GET    /api/users/{id}/courses/   # Cursos del usuario
GET    /api/users/{id}/groups/    # Grupos del usuario
GET    /api/users/{id}/accesses/  # Accesos del usuario
```

#### Grupos
```
GET    /api/groups/               # Listar grupos
GET    /api/groups/{id}/          # Detalle de grupo
GET    /api/groups/{id}/members/  # Miembros del grupo
GET    /api/groups/{id}/stats/    # Estadísticas del grupo
```

#### Estadísticas
```
GET    /api/stats/descriptive/    # Estadísticas descriptivas
GET    /api/stats/correlation/    # Análisis de correlación
GET    /api/stats/distribution/   # Distribución de accesos
GET    /api/stats/trends/         # Tendencias temporales
POST   /api/stats/custom/         # Análisis personalizado
```

#### Reportes
```
POST   /api/reports/weekly/       # Generar reporte semanal
GET    /api/reports/{id}/         # Obtener reporte guardado
GET    /api/reports/{id}/export/  # Exportar reporte (CSV/Excel)
```

### Ejemplo de Serializer

```python
# apps/moodle/serializers.py
from rest_framework import serializers
from .models import Course, MoodleUser, Group

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'shortname', 'fullname', 'category',
                  'startdate', 'enddate', 'visible']

class MoodleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodleUser
        fields = ['id', 'username', 'firstname', 'lastname', 'email']

class GroupSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.shortname', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'course_name',
                  'description', 'member_count']

    def get_member_count(self, obj):
        return obj.members.count()
```

### Ejemplo de ViewSet

```python
# apps/moodle/viewsets.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, MoodleUser, Group
from .serializers import CourseSerializer, MoodleUserSerializer, GroupSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'visible']
    search_fields = ['shortname', 'fullname']

class MoodleUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MoodleUser.objects.all()
    serializer_class = MoodleUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'firstname', 'lastname', 'email']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']
```

### Registrar URLs de API

```python
# config/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.moodle.viewsets import CourseViewSet, MoodleUserViewSet, GroupViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('users', MoodleUserViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [
    # ... URLs existentes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
```

## Permisos y Seguridad

### Configuración de Permisos en Admin

Django admin usa el sistema de permisos integrado:

- `add_<model>`: Permiso para crear
- `change_<model>`: Permiso para editar
- `delete_<model>`: Permiso para eliminar
- `view_<model>`: Permiso para ver

### Crear Usuario Staff

```python
from django.contrib.auth.models import User
user = User.objects.create_user('gestor', 'gestor@example.com', 'password123')
user.is_staff = True  # Puede acceder al admin
user.save()

# Dar permisos específicos
from django.contrib.auth.models import Permission
perm = Permission.objects.get(codename='view_course')
user.user_permissions.add(perm)
```

### Configurar Permisos en DRF

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## Exportación de Datos desde Admin

### Exportar a CSV (Nativo de Django)

1. Crear action en admin:

```python
# apps/moodle/admin.py
import csv
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Email'])  # Headers

    for obj in queryset:
        writer.writerow([obj.id, obj.username, obj.email])

    return response

export_to_csv.short_description = "Exportar a CSV"

@admin.register(MoodleUser)
class MoodleUserAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    # ... resto de la configuración
```

### Exportar a Excel

```python
from openpyxl import Workbook
from django.http import HttpResponse

def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Nombre', 'Email'])  # Headers

    for obj in queryset:
        ws.append([obj.id, obj.username, obj.email])

    wb.save(response)
    return response

export_to_excel.short_description = "Exportar a Excel"
```

## Conclusión

El sistema incluye:
- ✅ Admin completo de Django con todos los modelos
- ✅ Búsqueda, filtros y jerarquía temporal
- ✅ Preparado para implementar API REST
- ✅ Ejemplos de serializers y viewsets
- ✅ Sistema de permisos integrado
- ✅ Exportación a CSV/Excel

Para más información sobre Django Admin: https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
Para Django REST Framework: https://www.django-rest-framework.org/
