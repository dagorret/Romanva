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
    Group, GroupMember, Category, Role, RoleAssignment
)


@login_required
def analytics_menu(request):
    """Menú principal de estadísticas"""
    context = {
        'stats_options': [
            # Análisis Básicos
            {
                'name': 'Estadísticas Descriptivas',
                'description': 'Media, mediana, moda, desviación estándar, varianza',
                'url': 'descriptive_stats',
                'icon': '📊',
                'category': 'basic'
            },
            {
                'name': 'Análisis de Correlación',
                'description': 'Correlación entre variables de acceso y rendimiento',
                'url': 'correlation_analysis',
                'icon': '🔗',
                'category': 'basic'
            },
            {
                'name': 'Distribución de Accesos',
                'description': 'Histogramas y distribución temporal de accesos',
                'url': 'access_distribution',
                'icon': '📈',
                'category': 'basic'
            },
            {
                'name': 'Comparación entre Grupos',
                'description': 'Comparar métricas entre diferentes grupos',
                'url': 'group_comparison',
                'icon': '⚖️',
                'category': 'basic'
            },
            {
                'name': 'Tendencias Temporales',
                'description': 'Análisis de series de tiempo y tendencias',
                'url': 'temporal_trends',
                'icon': '📉',
                'category': 'basic'
            },
            {
                'name': 'Panel Personalizado',
                'description': 'Selecciona variables y operaciones estadísticas',
                'url': 'custom_panel',
                'icon': '🎛️',
                'category': 'basic'
            },
            # Análisis Avanzados
            {
                'name': 'Análisis de Roles por Curso',
                'description': 'Últimos 120 días: accesos por rol, cantidad y promedio semanal',
                'url': 'role_analysis',
                'icon': '👥',
                'category': 'advanced'
            },
            {
                'name': 'Regresión y Predicción',
                'description': 'Predicción de tendencias futuras con regresión lineal',
                'url': 'regression_analysis',
                'icon': '📉',
                'category': 'advanced'
            },
            {
                'name': 'Clustering de Estudiantes',
                'description': 'Agrupamiento por patrones de comportamiento (K-Means)',
                'url': 'clustering_analysis',
                'icon': '🎯',
                'category': 'advanced'
            },
            {
                'name': 'Análisis de Supervivencia',
                'description': 'Retención y abandono de estudiantes por cohortes',
                'url': 'survival_analysis',
                'icon': '📊',
                'category': 'advanced'
            },
            {
                'name': 'Heatmap de Actividad',
                'description': 'Patrones temporales: día de semana y hora del día',
                'url': 'heatmap_activity',
                'icon': '🔥',
                'category': 'advanced'
            },
            {
                'name': 'Análisis PCA',
                'description': 'Componentes Principales: reducción dimensional de datos',
                'url': 'pca_analysis',
                'icon': '🧬',
                'category': 'advanced'
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


# ============================================================================
# MÓDULOS ESTADÍSTICOS AVANZADOS
# ============================================================================

@login_required
def role_analysis(request):
    """Análisis de roles por curso - Últimos 120 días con promedios semanales"""
    from collections import defaultdict

    # Fecha límite: últimos 120 días
    date_limit = timezone.now() - timedelta(days=120)

    # Obtener cursos con actividad reciente
    courses = Course.objects.filter(
        visible=True,
        user_accesses__timeaccess__gte=date_limit
    ).distinct()[:20]

    course_stats = []
    for course in courses:
        # Estadísticas por rol
        role_stats = defaultdict(lambda: {'total_accesses': 0, 'unique_users': set()})

        # Obtener accesos de los últimos 120 días para este curso
        accesses = UserLastAccess.objects.filter(
            course=course,
            timeaccess__gte=date_limit
        ).select_related('user')

        for access in accesses:
            # Obtener rol del usuario en este curso
            role_assignment = RoleAssignment.objects.filter(
                user=access.user,
                course=course
            ).select_related('role').first()

            if role_assignment:
                role_name = role_assignment.role.get_shortname_display()
            else:
                role_name = 'Sin rol'

            role_stats[role_name]['total_accesses'] += 1
            role_stats[role_name]['unique_users'].add(access.user.id)

        # Calcular promedios semanales (120 días = ~17 semanas)
        weeks = 17
        for role_name in role_stats:
            total_accesses = role_stats[role_name]['total_accesses']
            unique_users = len(role_stats[role_name]['unique_users'])

            role_stats[role_name] = {
                'total_accesses': total_accesses,
                'unique_users': unique_users,
                'avg_weekly_accesses': round(total_accesses / weeks, 2),
                'avg_accesses_per_user': round(total_accesses / unique_users, 2) if unique_users > 0 else 0,
            }

        course_stats.append({
            'course': course,
            'role_stats': dict(role_stats),
            'total_accesses': sum(s['total_accesses'] for s in role_stats.values()),
        })

    # Ordenar por total de accesos
    course_stats.sort(key=lambda x: x['total_accesses'], reverse=True)

    context = {
        'course_stats': course_stats,
        'days': 120,
        'weeks': 17,
        'date_from': date_limit.strftime('%Y-%m-%d'),
        'date_to': timezone.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'analytics/role_analysis.html', context)


@login_required
def regression_analysis(request):
    """Análisis de regresión y predicción de tendencias"""
    import numpy as np
    from scipy import stats

    # Obtener cursos activos
    courses = Course.objects.filter(visible=True)[:10]

    predictions = []
    for course in courses:
        # Obtener accesos de los últimos 90 días
        days = 90
        date_limit = timezone.now() - timedelta(days=days)

        # Agrupar accesos por semana
        weekly_data = []
        for week in range(int(days/7)):
            week_start = date_limit + timedelta(weeks=week)
            week_end = week_start + timedelta(days=7)

            count = UserLastAccess.objects.filter(
                course=course,
                timeaccess__gte=week_start,
                timeaccess__lt=week_end
            ).count()

            weekly_data.append(count)

        if len(weekly_data) > 2 and sum(weekly_data) > 0:
            # Regresión lineal
            x = np.array(range(len(weekly_data)))
            y = np.array(weekly_data)

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            # Predecir próximas 4 semanas
            future_weeks = []
            for i in range(4):
                prediction = slope * (len(weekly_data) + i) + intercept
                future_weeks.append(max(0, round(prediction, 2)))  # No negativos

            predictions.append({
                'course': course,
                'weekly_data': weekly_data,
                'slope': round(slope, 3),
                'r_squared': round(r_value ** 2, 3),
                'trend': 'Creciente' if slope > 0.5 else 'Decreciente' if slope < -0.5 else 'Estable',
                'future_predictions': future_weeks,
                'avg_current': round(sum(weekly_data) / len(weekly_data), 2),
                'avg_predicted': round(sum(future_weeks) / len(future_weeks), 2),
            })

    context = {
        'predictions': predictions,
        'days_analyzed': 90,
        'weeks_predicted': 4,
    }
    return render(request, 'analytics/regression_analysis.html', context)


@login_required
def clustering_analysis(request):
    """Análisis de clustering - Agrupamiento de estudiantes por patrones"""
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    import numpy as np

    # Obtener estudiantes con actividad
    date_limit = timezone.now() - timedelta(days=90)

    # Construir matriz de características
    students_data = []
    students_info = []

    for user in MoodleUser.objects.all()[:200]:  # Limitar para performance
        # Características del estudiante
        total_accesses = UserLastAccess.objects.filter(
            user=user,
            timeaccess__gte=date_limit
        ).count()

        courses_enrolled = UserEnrolment.objects.filter(user=user).count()
        groups_count = GroupMember.objects.filter(user=user).count()

        # Calcular días promedio entre accesos
        accesses = UserLastAccess.objects.filter(
            user=user,
            timeaccess__gte=date_limit
        ).order_by('timeaccess')

        if accesses.count() > 1:
            time_deltas = []
            for i in range(1, len(accesses)):
                delta = (accesses[i].timeaccess - accesses[i-1].timeaccess).days
                time_deltas.append(delta)
            avg_days_between = sum(time_deltas) / len(time_deltas) if time_deltas else 0
        else:
            avg_days_between = 0

        if total_accesses > 0:  # Solo estudiantes activos
            students_data.append([
                total_accesses,
                courses_enrolled,
                groups_count,
                avg_days_between
            ])
            students_info.append({
                'user': user,
                'total_accesses': total_accesses,
                'courses_enrolled': courses_enrolled,
                'groups_count': groups_count,
            })

    clusters_result = []
    if len(students_data) >= 3:  # Mínimo 3 estudiantes para clustering
        # Normalizar datos
        scaler = StandardScaler()
        X = scaler.fit_transform(np.array(students_data))

        # Aplicar K-Means con 3 clusters
        n_clusters = min(3, len(students_data))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)

        # Agrupar resultados por cluster
        for cluster_id in range(n_clusters):
            cluster_members = [
                students_info[i] for i in range(len(labels)) if labels[i] == cluster_id
            ]

            if cluster_members:
                avg_accesses = sum(s['total_accesses'] for s in cluster_members) / len(cluster_members)
                avg_courses = sum(s['courses_enrolled'] for s in cluster_members) / len(cluster_members)

                # Clasificar cluster
                if avg_accesses > 20:
                    cluster_type = 'Muy Activos'
                elif avg_accesses > 10:
                    cluster_type = 'Moderadamente Activos'
                else:
                    cluster_type = 'Poco Activos'

                clusters_result.append({
                    'id': cluster_id + 1,
                    'type': cluster_type,
                    'size': len(cluster_members),
                    'avg_accesses': round(avg_accesses, 2),
                    'avg_courses': round(avg_courses, 2),
                    'members': cluster_members[:10],  # Mostrar primeros 10
                })

    context = {
        'clusters': clusters_result,
        'total_students': len(students_data),
        'days_analyzed': 90,
    }
    return render(request, 'analytics/clustering_analysis.html', context)


@login_required
def survival_analysis(request):
    """Análisis de supervivencia - Retención y abandono de estudiantes"""
    # Analizar retención por cohorte (mes de inscripción)
    from collections import defaultdict

    cohorts = defaultdict(lambda: {'enrolled': 0, 'active': 0, 'inactive': 0})

    # Definir "activo" como acceso en últimos 30 días
    activity_threshold = timezone.now() - timedelta(days=30)

    # Agrupar por mes de inscripción
    enrollments = UserEnrolment.objects.all().select_related('user', 'enrol__course')

    for enrollment in enrollments:
        cohort_month = enrollment.timecreated.strftime('%Y-%m')
        cohorts[cohort_month]['enrolled'] += 1

        # Verificar si el usuario ha accedido recientemente
        recent_access = UserLastAccess.objects.filter(
            user=enrollment.user,
            timeaccess__gte=activity_threshold
        ).exists()

        if recent_access:
            cohorts[cohort_month]['active'] += 1
        else:
            cohorts[cohort_month]['inactive'] += 1

    # Calcular tasas de retención
    cohort_stats = []
    for month, data in sorted(cohorts.items(), reverse=True)[:12]:  # Últimos 12 meses
        retention_rate = (data['active'] / data['enrolled'] * 100) if data['enrolled'] > 0 else 0
        churn_rate = 100 - retention_rate

        cohort_stats.append({
            'month': month,
            'enrolled': data['enrolled'],
            'active': data['active'],
            'inactive': data['inactive'],
            'retention_rate': round(retention_rate, 2),
            'churn_rate': round(churn_rate, 2),
        })

    # Estadísticas globales
    total_enrolled = sum(c['enrolled'] for c in cohort_stats)
    total_active = sum(c['active'] for c in cohort_stats)
    global_retention = (total_active / total_enrolled * 100) if total_enrolled > 0 else 0

    context = {
        'cohorts': cohort_stats,
        'total_enrolled': total_enrolled,
        'total_active': total_active,
        'total_inactive': total_enrolled - total_active,
        'global_retention_rate': round(global_retention, 2),
        'activity_threshold_days': 30,
    }
    return render(request, 'analytics/survival_analysis.html', context)


@login_required
def heatmap_activity(request):
    """Heatmap de actividad temporal - Patrones por día de semana y hora"""
    from collections import defaultdict

    # Obtener accesos de los últimos 60 días
    date_limit = timezone.now() - timedelta(days=60)
    accesses = UserLastAccess.objects.filter(timeaccess__gte=date_limit)

    # Matriz: día de semana (0-6) x hora (0-23)
    heatmap_data = defaultdict(lambda: defaultdict(int))

    for access in accesses:
        day_of_week = access.timeaccess.weekday()  # 0=Lunes, 6=Domingo
        hour = access.timeaccess.hour
        heatmap_data[day_of_week][hour] += 1

    # Convertir a formato para template
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    hours = list(range(24))

    heatmap_matrix = []
    for day_idx in range(7):
        row = {
            'day': days[day_idx],
            'hours': [heatmap_data[day_idx][hour] for hour in hours]
        }
        heatmap_matrix.append(row)

    # Encontrar picos de actividad
    max_activity = 0
    peak_times = []
    for day_idx, day_data in heatmap_data.items():
        for hour, count in day_data.items():
            if count > max_activity:
                max_activity = count
            if count > 10:  # Umbral arbitrario
                peak_times.append({
                    'day': days[day_idx],
                    'hour': f"{hour:02d}:00",
                    'count': count
                })

    peak_times.sort(key=lambda x: x['count'], reverse=True)

    context = {
        'heatmap_matrix': heatmap_matrix,
        'hours': hours,
        'max_activity': max_activity,
        'peak_times': peak_times[:10],  # Top 10
        'days_analyzed': 60,
    }
    return render(request, 'analytics/heatmap_activity.html', context)


@login_required
def pca_analysis(request):
    """Análisis de Componentes Principales - Reducción dimensional"""
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    import numpy as np

    # Construir matriz de características de cursos
    courses_data = []
    courses_info = []

    for course in Course.objects.filter(visible=True)[:50]:
        # Características del curso
        total_enrolled = UserEnrolment.objects.filter(enrol__course=course).count()
        total_accesses = UserLastAccess.objects.filter(course=course).count()
        groups_count = Group.objects.filter(course=course).count()

        # Calcular engagement rate
        unique_accessors = UserLastAccess.objects.filter(course=course).values('user').distinct().count()
        engagement_rate = (unique_accessors / total_enrolled * 100) if total_enrolled > 0 else 0

        # Días desde inicio
        if course.startdate:
            days_active = (timezone.now() - course.startdate).days
        else:
            days_active = 0

        if total_enrolled > 0:  # Solo cursos con estudiantes
            courses_data.append([
                total_enrolled,
                total_accesses,
                groups_count,
                engagement_rate,
                days_active
            ])
            courses_info.append({
                'course': course,
                'total_enrolled': total_enrolled,
                'total_accesses': total_accesses,
                'engagement_rate': round(engagement_rate, 2),
            })

    pca_results = []
    if len(courses_data) >= 3:
        # Normalizar datos
        scaler = StandardScaler()
        X = scaler.fit_transform(np.array(courses_data))

        # Aplicar PCA
        n_components = min(3, len(courses_data))
        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X)

        # Varianza explicada
        variance_explained = pca.explained_variance_ratio_ * 100

        # Componentes principales
        for i, course_info in enumerate(courses_info):
            pca_results.append({
                'course': course_info['course'],
                'pc1': round(X_pca[i][0], 3) if n_components > 0 else 0,
                'pc2': round(X_pca[i][1], 3) if n_components > 1 else 0,
                'pc3': round(X_pca[i][2], 3) if n_components > 2 else 0,
                'total_enrolled': course_info['total_enrolled'],
                'total_accesses': course_info['total_accesses'],
            })

        variance_info = [
            {'component': f'PC{i+1}', 'variance': round(var, 2)}
            for i, var in enumerate(variance_explained)
        ]
    else:
        variance_info = []

    context = {
        'pca_results': pca_results[:20],  # Top 20 para visualización
        'variance_explained': variance_info,
        'total_courses': len(courses_data),
        'n_components': len(variance_info),
    }
    return render(request, 'analytics/pca_analysis.html', context)
