"""
Vistas para el panel de gestores (migrado de PHP)
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from .models import (
    Course, Group, MoodleUser, Category,
    GroupMember, UserEnrolment, UserLastAccess
)


def login_view(request):
    """Vista de login"""
    if request.user.is_authenticated:
        return redirect('panel')

    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            error = 'Completá usuario y contraseña.'
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('panel')
            else:
                error = 'Usuario o contraseña inválidos.'

    return render(request, 'moodle/login.html', {'error': error})


def logout_view(request):
    """Vista de logout"""
    auth_logout(request)
    return redirect('login')


@login_required
def panel_view(request):
    """Panel principal de reportes (migrado de panel.php)"""

    # Obtener categorías "Grado" y sus descendientes
    grado_categories = Category.objects.filter(name__iexact='Grado')
    allowed_category_ids = set()

    if grado_categories.exists():
        for cat in grado_categories:
            # Incluir la categoría principal
            allowed_category_ids.add(cat.id)
            # Buscar todos los descendientes (categorías que tienen a esta en su path)
            # Si cat.path es "/1", buscamos categorías cuyo path empiece con "/1/"
            descendants = Category.objects.filter(path__startswith=cat.path + '/')
            allowed_category_ids.update(descendants.values_list('id', flat=True))

    # Filtro de búsqueda por código
    course_search = request.GET.get('q', '').strip()

    # Filtrar cursos (solo categoría Grado del año actual)
    now = timezone.now()
    current_year = now.year

    courses = Course.objects.filter(visible=True)

    if allowed_category_ids:
        courses = courses.filter(category_id__in=allowed_category_ids)

    if course_search:
        courses = courses.filter(
            Q(shortname__icontains=course_search) |
            Q(fullname__icontains=course_search)
        )

    # Filtrar por año actual en el nombre del curso (más permisivo)
    import re
    filtered_courses = []
    for course in courses:
        # Buscar año en el nombre
        year_match = re.search(r'\b(20\d{2})\b', course.fullname or course.shortname)

        if year_match:
            course_year = int(year_match.group(1))
            # Aceptar año actual y siguiente
            if course_year == current_year or course_year == current_year + 1:
                filtered_courses.append(course)
        elif course.startdate:
            # Si no hay año en el nombre, usar startdate del año actual
            if course.startdate.year == current_year:
                filtered_courses.append(course)
        else:
            # Si no tiene ni año ni fecha, incluirlo igual
            filtered_courses.append(course)

    # Ordenar por shortname
    filtered_courses.sort(key=lambda c: c.shortname)

    # Parámetros del formulario
    courseid = int(request.GET.get('courseid') or 0)
    groupid = int(request.GET.get('groupid') or 0)
    from_str = request.GET.get('from', '')
    to_str = request.GET.get('to', '')

    # Rango por defecto: últimos 30 días
    if not from_str and not to_str:
        to_date = now
        from_date = now - timedelta(days=30)
        from_str = from_date.strftime('%Y-%m-%d')
        to_str = to_date.strftime('%Y-%m-%d')
    else:
        # Convertir strings a datetime con timezone
        if from_str:
            from_date = timezone.make_aware(
                timezone.datetime.strptime(from_str, '%Y-%m-%d')
            )
        else:
            from_date = None

        if to_str:
            to_date = timezone.make_aware(
                timezone.datetime.strptime(to_str, '%Y-%m-%d')
            )
        else:
            to_date = None

    # Validaciones
    errors = []
    selected_course = None
    groups = []

    if courseid:
        try:
            selected_course = Course.objects.get(id=courseid)
            groups = Group.objects.filter(course=selected_course).order_by('name')
        except Course.DoesNotExist:
            errors.append('Curso inválido.')
            courseid = 0
            groupid = 0

    selected_group = None
    if courseid and groupid:
        try:
            selected_group = Group.objects.get(id=groupid, course_id=courseid)
        except Group.DoesNotExist:
            errors.append('El grupo no pertenece al curso.')
            groupid = 0

    # Calcular reporte
    report = None
    if selected_course and selected_group and from_date and to_date:
        report = calculate_weekly_report(selected_course, selected_group, from_date, to_date)

    context = {
        'courses': filtered_courses,
        'course_search': course_search,
        'selected_course': selected_course,
        'groups': groups,
        'selected_group': selected_group,
        'from_str': from_str,
        'to_str': to_str,
        'errors': errors,
        'report': report,
    }

    return render(request, 'moodle/panel.html', context)


def calculate_weekly_report(course, group, from_date, to_date):
    """Calcula el reporte semanal de usuarios sin acceso"""

    # A) Usuarios del grupo
    group_user_ids = set(GroupMember.objects.filter(group=group).values_list('user_id', flat=True))

    # B) Usuarios inscritos al curso
    course_user_ids = set(
        UserEnrolment.objects.filter(enrol__course=course).values_list('user_id', flat=True)
    )

    # C) Intersección
    target_user_ids = group_user_ids & course_user_ids

    # D) Últimos accesos
    last_accesses = {}
    for access in UserLastAccess.objects.filter(course=course, user_id__in=target_user_ids):
        user_id = access.user_id
        if user_id not in last_accesses or access.timeaccess > last_accesses[user_id]:
            last_accesses[user_id] = access.timeaccess

    # E) Serie semanal
    series = []
    current_date = from_date

    # Encontrar el lunes de la semana
    while current_date.weekday() != 0:  # 0 = lunes
        current_date -= timedelta(days=1)

    while current_date <= to_date:
        week_end = current_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

        still_never = 0
        for user_id in target_user_ids:
            if user_id not in last_accesses or last_accesses[user_id] > week_end:
                still_never += 1

        week_label = f"{current_date.strftime('%Y-%m-%d')} → {week_end.strftime('%Y-%m-%d')}"

        series.append({
            'week': week_label,
            'never': still_never,
            'end_ts': int(week_end.timestamp())
        })

        current_date += timedelta(days=7)

    return {
        'series': series,
        'total_group': len(target_user_ids)
    }


@login_required
def never_users_view(request):
    """Lista de usuarios que no accedieron en una semana específica"""
    courseid = int(request.GET.get('courseid') or 0)
    groupid = int(request.GET.get('groupid') or 0)
    week_end_ts = int(request.GET.get('end') or 0)

    if not all([courseid, groupid, week_end_ts]):
        return render(request, 'moodle/error.html', {'message': 'Parámetros inválidos'})

    course = Course.objects.get(id=courseid)
    group = Group.objects.get(id=groupid)
    week_end = timezone.datetime.fromtimestamp(week_end_ts, tz=timezone.get_current_timezone())

    # Usuarios del grupo
    group_user_ids = set(GroupMember.objects.filter(group=group).values_list('user_id', flat=True))

    # Usuarios inscritos
    course_user_ids = set(
        UserEnrolment.objects.filter(enrol__course=course).values_list('user_id', flat=True)
    )

    # Intersección
    target_user_ids = group_user_ids & course_user_ids

    # Últimos accesos
    last_accesses = {}
    for access in UserLastAccess.objects.filter(course=course, user_id__in=target_user_ids):
        user_id = access.user_id
        if user_id not in last_accesses or access.timeaccess > last_accesses[user_id]:
            last_accesses[user_id] = access.timeaccess

    # Faltantes
    missing_user_ids = []
    for user_id in target_user_ids:
        if user_id not in last_accesses or last_accesses[user_id] > week_end:
            missing_user_ids.append(user_id)

    # Datos de usuarios
    users = MoodleUser.objects.filter(id__in=missing_user_ids).order_by('lastname', 'firstname')

    week_start = week_end - timedelta(days=6)
    week_label = f"{week_start.strftime('%Y-%m-%d')} → {week_end.strftime('%Y-%m-%d')}"

    context = {
        'users': users,
        'week_label': week_label,
        'course': course,
        'group': group,
    }

    return render(request, 'moodle/never_users.html', context)
