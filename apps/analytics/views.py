"""
Vistas para análisis estadísticos avanzados
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Max, Min, StdDev, Q
from django.utils import timezone
from datetime import timedelta
import json

from apps.moodle.models import (
    Course, MoodleUser, UserLastAccess, UserEnrolment,
    Group, GroupMember, Category
)


@login_required
def analytics_menu(request):
    """Menú principal de estadísticas"""
    context = {
        'stats_options': [
            {
                'name': 'Estadísticas Descriptivas',
                'description': 'Media, mediana, moda, desviación estándar, varianza',
                'url': 'descriptive_stats',
                'icon': '📊'
            },
            {
                'name': 'Análisis de Correlación',
                'description': 'Correlación entre variables de acceso y rendimiento',
                'url': 'correlation_analysis',
                'icon': '🔗'
            },
            {
                'name': 'Distribución de Accesos',
                'description': 'Histogramas y distribución temporal de accesos',
                'url': 'access_distribution',
                'icon': '📈'
            },
            {
                'name': 'Comparación entre Grupos',
                'description': 'Comparar métricas entre diferentes grupos',
                'url': 'group_comparison',
                'icon': '⚖️'
            },
            {
                'name': 'Tendencias Temporales',
                'description': 'Análisis de series de tiempo y tendencias',
                'url': 'temporal_trends',
                'icon': '📉'
            },
            {
                'name': 'Panel Personalizado',
                'description': 'Selecciona variables y operaciones estadísticas',
                'url': 'custom_panel',
                'icon': '🎛️'
            },
        ]
    }
    return render(request, 'analytics/menu.html', context)


@login_required
def descriptive_stats(request):
    """Estadísticas descriptivas de accesos"""
    # Obtener datos de acceso por curso
    courses = Course.objects.filter(visible=True)[:20]  # Limitar para performance

    stats = []
    for course in courses:
        accesses = UserLastAccess.objects.filter(course=course)
        access_count = accesses.count()

        if access_count > 0:
            enrolled_count = UserEnrolment.objects.filter(enrol__course=course).count()

            # Calcular días desde el inicio del curso
            now = timezone.now()
            if course.startdate:
                days_active = (now - course.startdate).days
            else:
                days_active = None

            stats.append({
                'course': course,
                'access_count': access_count,
                'enrolled_count': enrolled_count,
                'access_rate': round((access_count / enrolled_count * 100), 2) if enrolled_count > 0 else 0,
                'days_active': days_active,
            })

    # Calcular estadísticas globales
    if stats:
        access_rates = [s['access_rate'] for s in stats]
        avg_rate = sum(access_rates) / len(access_rates)
        max_rate = max(access_rates)
        min_rate = min(access_rates)

        global_stats = {
            'avg_access_rate': round(avg_rate, 2),
            'max_access_rate': round(max_rate, 2),
            'min_access_rate': round(min_rate, 2),
            'total_courses': len(stats),
        }
    else:
        global_stats = None

    context = {
        'stats': stats,
        'global_stats': global_stats,
    }

    return render(request, 'analytics/descriptive_stats.html', context)


@login_required
def correlation_analysis(request):
    """Análisis de correlación entre variables"""
    # Variables: accesos vs inscriptos, grupos vs accesos, etc.

    courses = Course.objects.filter(visible=True)

    data_points = []
    for course in courses:
        enrolled = UserEnrolment.objects.filter(enrol__course=course).count()
        accesses = UserLastAccess.objects.filter(course=course).count()
        groups_count = Group.objects.filter(course=course).count()

        if enrolled > 0:
            data_points.append({
                'course_name': course.shortname,
                'enrolled': enrolled,
                'accesses': accesses,
                'groups': groups_count,
                'access_rate': round((accesses / enrolled * 100), 2),
            })

    context = {
        'data_points': data_points,
        'data_json': json.dumps(data_points),
    }

    return render(request, 'analytics/correlation_analysis.html', context)


@login_required
def access_distribution(request):
    """Distribución temporal de accesos"""
    now = timezone.now()
    last_30_days = now - timedelta(days=30)

    # Accesos por día (últimos 30 días)
    daily_accesses = []
    for i in range(30):
        day_start = last_30_days + timedelta(days=i)
        day_end = day_start + timedelta(days=1)

        count = UserLastAccess.objects.filter(
            timeaccess__gte=day_start,
            timeaccess__lt=day_end
        ).count()

        daily_accesses.append({
            'date': day_start.strftime('%Y-%m-%d'),
            'count': count
        })

    context = {
        'daily_accesses': daily_accesses,
        'daily_accesses_json': json.dumps(daily_accesses),
    }

    return render(request, 'analytics/access_distribution.html', context)


@login_required
def group_comparison(request):
    """Comparación entre grupos"""
    groups = Group.objects.all()[:20]

    group_stats = []
    for group in groups:
        members = GroupMember.objects.filter(group=group).count()
        course = group.course

        # Accesos de miembros del grupo
        member_ids = GroupMember.objects.filter(group=group).values_list('user_id', flat=True)
        accesses = UserLastAccess.objects.filter(
            course=course,
            user_id__in=member_ids
        ).count()

        group_stats.append({
            'group': group,
            'members': members,
            'accesses': accesses,
            'access_rate': round((accesses / members * 100), 2) if members > 0 else 0,
        })

    context = {
        'group_stats': group_stats,
    }

    return render(request, 'analytics/group_comparison.html', context)


@login_required
def temporal_trends(request):
    """Análisis de tendencias temporales"""
    now = timezone.now()
    last_90_days = now - timedelta(days=90)

    # Accesos por semana (últimas 12 semanas)
    weekly_data = []
    for i in range(12):
        week_start = last_90_days + timedelta(weeks=i)
        week_end = week_start + timedelta(weeks=1)

        count = UserLastAccess.objects.filter(
            timeaccess__gte=week_start,
            timeaccess__lt=week_end
        ).count()

        weekly_data.append({
            'week': f'Semana {i+1}',
            'date': week_start.strftime('%Y-%m-%d'),
            'count': count
        })

    context = {
        'weekly_data': weekly_data,
        'weekly_data_json': json.dumps(weekly_data),
    }

    return render(request, 'analytics/temporal_trends.html', context)


@login_required
def custom_panel(request):
    """Panel personalizado para seleccionar variables y operaciones"""

    if request.method == 'POST':
        # Procesar selección de variables
        selected_vars = request.POST.getlist('variables')
        operation = request.POST.get('operation')

        results = calculate_custom_stats(selected_vars, operation)

        context = {
            'variables': get_available_variables(),
            'operations': get_available_operations(),
            'selected_vars': selected_vars,
            'selected_operation': operation,
            'results': results,
        }
    else:
        context = {
            'variables': get_available_variables(),
            'operations': get_available_operations(),
        }

    return render(request, 'analytics/custom_panel.html', context)


def get_available_variables():
    """Variables disponibles para análisis"""
    return [
        {'id': 'course_accesses', 'name': 'Accesos por curso', 'type': 'numeric'},
        {'id': 'user_enrollments', 'name': 'Inscripciones por curso', 'type': 'numeric'},
        {'id': 'group_members', 'name': 'Miembros por grupo', 'type': 'numeric'},
        {'id': 'access_rate', 'name': 'Tasa de acceso (%)', 'type': 'numeric'},
        {'id': 'days_since_access', 'name': 'Días desde último acceso', 'type': 'numeric'},
    ]


def get_available_operations():
    """Operaciones estadísticas disponibles"""
    return [
        {'id': 'mean', 'name': 'Media (promedio)'},
        {'id': 'median', 'name': 'Mediana'},
        {'id': 'max', 'name': 'Máximo'},
        {'id': 'min', 'name': 'Mínimo'},
        {'id': 'sum', 'name': 'Suma total'},
        {'id': 'count', 'name': 'Conteo'},
        {'id': 'stddev', 'name': 'Desviación estándar'},
    ]


def calculate_custom_stats(variables, operation):
    """Calcula estadísticas personalizadas"""
    results = {}

    for var in variables:
        if var == 'course_accesses':
            values = [
                UserLastAccess.objects.filter(course=c).count()
                for c in Course.objects.filter(visible=True)
            ]
        elif var == 'user_enrollments':
            values = [
                UserEnrolment.objects.filter(enrol__course=c).count()
                for c in Course.objects.filter(visible=True)
            ]
        elif var == 'group_members':
            values = [
                GroupMember.objects.filter(group=g).count()
                for g in Group.objects.all()
            ]
        else:
            values = []

        if values:
            if operation == 'mean':
                results[var] = round(sum(values) / len(values), 2)
            elif operation == 'median':
                sorted_vals = sorted(values)
                n = len(sorted_vals)
                results[var] = sorted_vals[n//2] if n % 2 else (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2
            elif operation == 'max':
                results[var] = max(values)
            elif operation == 'min':
                results[var] = min(values)
            elif operation == 'sum':
                results[var] = sum(values)
            elif operation == 'count':
                results[var] = len(values)
            elif operation == 'stddev':
                mean = sum(values) / len(values)
                variance = sum((x - mean) ** 2 for x in values) / len(values)
                results[var] = round(variance ** 0.5, 2)

    return results
