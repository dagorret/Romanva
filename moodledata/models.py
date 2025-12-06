"""
Modelos Django para almacenar datos importados desde Moodle
"""
from django.db import models
from django.utils import timezone


class ImportLog(models.Model):
    """Log de importaciones realizadas"""
    table_name = models.CharField(max_length=100, verbose_name='Tabla')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Inicio')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Fin')
    records_imported = models.IntegerField(default=0, verbose_name='Registros importados')
    status = models.CharField(
        max_length=20,
        choices=[
            ('running', 'En progreso'),
            ('completed', 'Completada'),
            ('failed', 'Fallida'),
        ],
        default='running',
        verbose_name='Estado'
    )
    error_message = models.TextField(blank=True, verbose_name='Mensaje de error')

    class Meta:
        verbose_name = 'Log de Importación'
        verbose_name_plural = 'Logs de Importación'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.table_name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"


class Course(models.Model):
    """Cursos de Moodle"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    shortname = models.CharField(max_length=255, verbose_name='Nombre corto')
    fullname = models.CharField(max_length=255, verbose_name='Nombre completo')
    category = models.IntegerField(verbose_name='Categoría')
    startdate = models.IntegerField(verbose_name='Fecha inicio (timestamp)')
    enddate = models.IntegerField(verbose_name='Fecha fin (timestamp)')
    visible = models.BooleanField(default=True, verbose_name='Visible')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['shortname']

    def __str__(self):
        return f"{self.shortname} - {self.fullname}"


class Category(models.Model):
    """Categorías de cursos"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    parent = models.IntegerField(verbose_name='Categoría padre')
    path = models.CharField(max_length=255, verbose_name='Ruta')
    visible = models.BooleanField(default=True, verbose_name='Visible')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name


class Enrol(models.Model):
    """Métodos de inscripción"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    courseid = models.IntegerField(verbose_name='ID Curso')
    enrol = models.CharField(max_length=50, verbose_name='Método')
    status = models.IntegerField(verbose_name='Estado')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Método de Inscripción'
        verbose_name_plural = 'Métodos de Inscripción'
        ordering = ['courseid', 'enrol']

    def __str__(self):
        return f"Curso {self.courseid} - {self.enrol}"


class UserEnrolment(models.Model):
    """Inscripciones de usuarios"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    userid = models.IntegerField(verbose_name='ID Usuario')
    enrolid = models.IntegerField(verbose_name='ID Inscripción')
    timestart = models.IntegerField(verbose_name='Inicio (timestamp)')
    timeend = models.IntegerField(verbose_name='Fin (timestamp)')
    status = models.IntegerField(verbose_name='Estado')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Inscripción de Usuario'
        verbose_name_plural = 'Inscripciones de Usuarios'
        ordering = ['userid', 'enrolid']

    def __str__(self):
        return f"Usuario {self.userid} - Inscripción {self.enrolid}"


class User(models.Model):
    """Usuarios de Moodle"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    username = models.CharField(max_length=100, verbose_name='Nombre de usuario')
    firstname = models.CharField(max_length=100, verbose_name='Nombre')
    lastname = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(verbose_name='Email')
    city = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    country = models.CharField(max_length=2, blank=True, verbose_name='País')
    suspended = models.BooleanField(default=False, verbose_name='Suspendido')
    deleted = models.BooleanField(default=False, verbose_name='Eliminado')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f"{self.lastname}, {self.firstname} ({self.username})"


class Group(models.Model):
    """Grupos de Moodle"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    courseid = models.IntegerField(verbose_name='ID Curso')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    idnumber = models.CharField(max_length=100, blank=True, verbose_name='Número ID')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['courseid', 'name']

    def __str__(self):
        return f"{self.name} (Curso {self.courseid})"


class GroupMember(models.Model):
    """Miembros de grupos"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    groupid = models.IntegerField(verbose_name='ID Grupo')
    userid = models.IntegerField(verbose_name='ID Usuario')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Miembro de Grupo'
        verbose_name_plural = 'Miembros de Grupos'
        ordering = ['groupid', 'userid']

    def __str__(self):
        return f"Usuario {self.userid} en Grupo {self.groupid}"


class UserLastAccess(models.Model):
    """Último acceso de usuarios a cursos"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    userid = models.IntegerField(verbose_name='ID Usuario')
    courseid = models.IntegerField(verbose_name='ID Curso')
    timeaccess = models.IntegerField(verbose_name='Tiempo acceso (timestamp)')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Último Acceso de Usuario'
        verbose_name_plural = 'Últimos Accesos de Usuarios'
        ordering = ['-timeaccess']

    def __str__(self):
        return f"Usuario {self.userid} - Curso {self.courseid}"


class RoleAssignment(models.Model):
    """Asignaciones de roles"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    roleid = models.IntegerField(verbose_name='ID Rol')
    contextid = models.IntegerField(verbose_name='ID Contexto')
    userid = models.IntegerField(verbose_name='ID Usuario')
    timemodified = models.IntegerField(verbose_name='Modificado (timestamp)')
    modifierid = models.IntegerField(verbose_name='ID Modificador')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Asignación de Rol'
        verbose_name_plural = 'Asignaciones de Roles'
        ordering = ['userid', 'roleid']

    def __str__(self):
        return f"Usuario {self.userid} - Rol {self.roleid}"


class Context(models.Model):
    """Contextos de Moodle"""
    moodle_id = models.IntegerField(unique=True, verbose_name='ID Moodle')
    contextlevel = models.IntegerField(verbose_name='Nivel de contexto')
    instanceid = models.IntegerField(verbose_name='ID Instancia')
    path = models.CharField(max_length=255, verbose_name='Ruta')
    depth = models.IntegerField(verbose_name='Profundidad')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Importado el')

    class Meta:
        verbose_name = 'Contexto'
        verbose_name_plural = 'Contextos'
        ordering = ['contextlevel', 'instanceid']

    def __str__(self):
        return f"Contexto {self.moodle_id} - Nivel {self.contextlevel}"

# Diccionario de mapeo entre nombres de tabla y modelos
TABLE_MODEL_MAP = {
    'courses': Course,
    'categories': Category,
    'enrol': Enrol,
    'user_enrolments': UserEnrolment,
    'users': User,
    'groups': Group,
    'groups_members': GroupMember,
    'user_lastaccess': UserLastAccess,
    'role_assignments': RoleAssignment,
    'context': Context,
}
