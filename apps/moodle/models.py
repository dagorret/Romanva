"""
Modelos Django que replican la estructura de Moodle
Basados en el análisis del script PHP original
"""
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Categorías de cursos en Moodle"""
    name = models.CharField(max_length=255, verbose_name='Nombre')
    path = models.CharField(max_length=500, blank=True, verbose_name='Ruta')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='Categoría padre')
    depth = models.IntegerField(default=0, verbose_name='Profundidad')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['path', 'name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """Cursos de Moodle"""
    shortname = models.CharField(max_length=255, unique=True, verbose_name='Código')
    fullname = models.CharField(max_length=500, verbose_name='Nombre completo')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='courses', verbose_name='Categoría')
    startdate = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de inicio')
    enddate = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de fin')
    visible = models.BooleanField(default=True, verbose_name='Visible')

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['shortname']

    def __str__(self):
        return f"{self.shortname} - {self.fullname}"


class MoodleUser(models.Model):
    """Usuarios de Moodle"""
    username = models.CharField(max_length=100, unique=True, verbose_name='Usuario')
    firstname = models.CharField(max_length=100, verbose_name='Nombre')
    lastname = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name = 'Usuario de Moodle'
        verbose_name_plural = 'Usuarios de Moodle'
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f"{self.lastname}, {self.firstname} ({self.username})"

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"


class Group(models.Model):
    """Grupos dentro de cursos"""
    name = models.CharField(max_length=255, verbose_name='Nombre')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='groups', verbose_name='Curso')
    description = models.TextField(blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['course', 'name']

    def __str__(self):
        return f"{self.name} ({self.course.shortname})"


class GroupMember(models.Model):
    """Relación usuarios-grupos"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='members', verbose_name='Grupo')
    user = models.ForeignKey(MoodleUser, on_delete=models.CASCADE,
                             related_name='groups', verbose_name='Usuario')
    timeadded = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de incorporación')

    class Meta:
        verbose_name = 'Miembro de grupo'
        verbose_name_plural = 'Miembros de grupos'
        unique_together = ['group', 'user']

    def __str__(self):
        return f"{self.user} en {self.group.name}"


class Enrol(models.Model):
    """Métodos de inscripción de cursos"""
    ENROL_METHODS = [
        ('manual', 'Manual'),
        ('self', 'Auto-inscripción'),
        ('cohort', 'Cohorte'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='enrol_methods', verbose_name='Curso')
    enrol = models.CharField(max_length=50, choices=ENROL_METHODS,
                             default='manual', verbose_name='Método')
    status = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Método de inscripción'
        verbose_name_plural = 'Métodos de inscripción'

    def __str__(self):
        return f"{self.course.shortname} - {self.get_enrol_display()}"


class UserEnrolment(models.Model):
    """Inscripciones de usuarios a cursos"""
    enrol = models.ForeignKey(Enrol, on_delete=models.CASCADE,
                              related_name='user_enrolments', verbose_name='Método de inscripción')
    user = models.ForeignKey(MoodleUser, on_delete=models.CASCADE,
                             related_name='enrolments', verbose_name='Usuario')
    timestart = models.DateTimeField(null=True, blank=True, verbose_name='Inicio')
    timeend = models.DateTimeField(null=True, blank=True, verbose_name='Fin')
    timecreated = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    class Meta:
        verbose_name = 'Inscripción de usuario'
        verbose_name_plural = 'Inscripciones de usuarios'
        unique_together = ['enrol', 'user']

    def __str__(self):
        return f"{self.user} inscrito en {self.enrol.course.shortname}"


class Role(models.Model):
    """Roles de Moodle (estudiante, profesor, etc.)"""
    ROLE_TYPES = [
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
        ('editingteacher', 'Profesor editor'),
        ('manager', 'Gestor'),
    ]

    name = models.CharField(max_length=255, verbose_name='Nombre')
    shortname = models.CharField(max_length=100, choices=ROLE_TYPES,
                                  default='student', verbose_name='Código')

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class RoleAssignment(models.Model):
    """Asignación de roles a usuarios en cursos"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name='assignments', verbose_name='Rol')
    user = models.ForeignKey(MoodleUser, on_delete=models.CASCADE,
                             related_name='role_assignments', verbose_name='Usuario')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='role_assignments', verbose_name='Curso')
    timecreated = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    class Meta:
        verbose_name = 'Asignación de rol'
        verbose_name_plural = 'Asignaciones de roles'
        unique_together = ['role', 'user', 'course']

    def __str__(self):
        course_str = f" en {self.course.shortname}" if self.course else ""
        return f"{self.user} - {self.role.name}{course_str}"


class UserLastAccess(models.Model):
    """Último acceso de usuarios a cursos"""
    user = models.ForeignKey(MoodleUser, on_delete=models.CASCADE,
                             related_name='last_accesses', verbose_name='Usuario')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='user_accesses', verbose_name='Curso')
    timeaccess = models.DateTimeField(verbose_name='Último acceso')

    class Meta:
        verbose_name = 'Último acceso al curso'
        verbose_name_plural = 'Últimos accesos a cursos'
        unique_together = ['user', 'course']
        indexes = [
            models.Index(fields=['course', 'timeaccess']),
            models.Index(fields=['user', 'timeaccess']),
        ]

    def __str__(self):
        return f"{self.user} - {self.course.shortname} - {self.timeaccess}"
