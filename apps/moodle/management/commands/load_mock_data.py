"""
Comando para cargar datos mock que simulan una base de datos de Moodle
Genera datos realistas para testing y desarrollo con escala configurable
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from apps.moodle.models import (
    Category, Course, MoodleUser, Group, GroupMember,
    Enrol, UserEnrolment, UserLastAccess
)

# CONSTANTES DE CONFIGURACIÓN
TOTAL_USERS = 3200
TOTAL_COURSES = 200
NUM_CAREERS = 5
NUM_MODALITIES = 2
COURSES_PER_SEMESTER = TOTAL_COURSES // 2  # Mitad primer cuatri, mitad segundo


class Command(BaseCommand):
    help = 'Carga datos mock simulando una base de datos Moodle con escala configurable'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpia todos los datos antes de cargar',
        )
        parser.add_argument(
            '--scale',
            type=str,
            default='-1',
            choices=['-1', '-2', '-4'],
            help='Escala de datos: -1 (total=3200), -2 (mitad=1600), -4 (cuarto=800)',
        )

    def handle(self, *args, **options):
        # Determinar escala
        scale_factor = {
            '-1': 1,      # Total
            '-2': 2,      # Mitad
            '-4': 4,      # Cuarto
        }[options['scale']]

        users_to_create = TOTAL_USERS // scale_factor
        courses_to_create = TOTAL_COURSES // scale_factor

        self.stdout.write(self.style.WARNING(f'\nEscala seleccionada: {options["scale"]}'))
        self.stdout.write(f'  Usuarios a crear: {users_to_create}')
        self.stdout.write(f'  Cursos a crear: {courses_to_create}\n')

        if options['clear']:
            self.stdout.write('Limpiando datos existentes...')
            UserLastAccess.objects.all().delete()
            UserEnrolment.objects.all().delete()
            Enrol.objects.all().delete()
            GroupMember.objects.all().delete()
            Group.objects.all().delete()
            MoodleUser.objects.all().delete()
            Course.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Datos eliminados'))

        self.stdout.write('Generando datos mock de Moodle...')

        # 1. Categorías (Grado y Postgrado como modalidades, carreras dentro)
        self.stdout.write('Creando categorías...')

        # Modalidades principales
        cat_grado = Category.objects.create(
            name='Grado',
            path='/1',
            depth=1
        )

        cat_postgrado = Category.objects.create(
            name='Postgrado',
            path='/2',
            depth=1
        )

        # 5 Carreras en Grado
        careers_grado = [
            'Derecho',
            'Economía',
            'Ingeniería',
            'Medicina',
            'Arquitectura',
        ]

        career_categories = []
        for i, career_name in enumerate(careers_grado):
            cat = Category.objects.create(
                name=career_name,
                path=f'/1/{3+i}',
                parent=cat_grado,
                depth=2
            )
            career_categories.append(cat)

        self.stdout.write(self.style.SUCCESS(f'✓ {Category.objects.count()} categorías creadas'))

        # 2. Cursos (200 cursos: mitad primer cuatri, mitad segundo cuatri)
        self.stdout.write('Creando cursos...')

        current_year = timezone.now().year
        now = timezone.now()

        courses = []
        courses_per_career = courses_to_create // NUM_CAREERS

        # Nombres de materias por carrera
        subjects_by_career = {
            'Derecho': ['Derecho Civil', 'Derecho Penal', 'Derecho Constitucional', 'Derecho Laboral',
                       'Derecho Internacional', 'Derecho Comercial', 'Filosofía del Derecho',
                       'Derecho Procesal', 'Derecho Administrativo', 'Derecho Tributario'],
            'Economía': ['Microeconomía', 'Macroeconomía', 'Econometría', 'Finanzas',
                        'Contabilidad', 'Estadística', 'Matemática Financiera',
                        'Análisis Económico', 'Economía Internacional', 'Política Económica'],
            'Ingeniería': ['Cálculo', 'Física', 'Álgebra', 'Programación',
                          'Estructuras', 'Electrónica', 'Termodinámica',
                          'Mecánica', 'Materiales', 'Proyecto Final'],
            'Medicina': ['Anatomía', 'Fisiología', 'Bioquímica', 'Farmacología',
                        'Patología', 'Clínica Médica', 'Cirugía', 'Pediatría',
                        'Ginecología', 'Medicina Interna'],
            'Arquitectura': ['Diseño Arquitectónico', 'Historia de la Arquitectura', 'Estructuras',
                            'Construcciones', 'Urbanismo', 'Instalaciones',
                            'Proyecto Arquitectónico', 'Morfología', 'Materialidad', 'Taller'],
        }

        for idx, category in enumerate(career_categories):
            career_name = category.name
            subjects = subjects_by_career.get(career_name, ['Materia'])

            for i in range(courses_per_career):
                # Determinar si es primer o segundo cuatrimestre
                is_first_semester = i < (courses_per_career // 2)

                if is_first_semester:
                    # Primer cuatrimestre: marzo a julio
                    start = timezone.datetime(current_year, 3, random.randint(1, 15), tzinfo=timezone.get_current_timezone())
                    end = start + timedelta(days=120)
                    semester = '1C'
                else:
                    # Segundo cuatrimestre: agosto a diciembre
                    start = timezone.datetime(current_year, 8, random.randint(1, 15), tzinfo=timezone.get_current_timezone())
                    end = start + timedelta(days=120)
                    semester = '2C'

                # Seleccionar materia
                subject = random.choice(subjects)
                year_level = random.randint(1, 5)

                course_code = f'{career_name[:3].upper()}-{year_level}{i:02d}-{semester}-{current_year}'
                course_name = f'{subject} - Año {year_level} ({semester} {current_year})'

                course = Course.objects.create(
                    shortname=course_code,
                    fullname=course_name,
                    category=category,
                    startdate=start,
                    enddate=end,
                    visible=True
                )
                courses.append(course)

        self.stdout.write(self.style.SUCCESS(f'✓ {Course.objects.count()} cursos creados'))

        # 3. Usuarios (3200, 1600 o 800 según escala)
        self.stdout.write(f'Creando {users_to_create} usuarios...')

        nombres = [
            'Juan', 'María', 'Carlos', 'Ana', 'Pedro', 'Laura', 'Diego', 'Sofia',
            'Miguel', 'Valentina', 'Lucas', 'Camila', 'Mateo', 'Isabella', 'Santiago',
            'Martina', 'Nicolás', 'Catalina', 'Sebastián', 'Emilia', 'Tomás', 'Agustina',
            'Felipe', 'Josefina', 'Joaquín', 'Victoria', 'Manuel', 'Antonella', 'Pablo',
            'Carolina', 'Andrés', 'Francisca', 'Gabriel', 'Mercedes', 'Rodrigo'
        ]

        apellidos = [
            'García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez',
            'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
            'Fernández', 'Díaz', 'Morales', 'Jiménez', 'Álvarez', 'Romero',
            'Herrera', 'Medina', 'Castro', 'Vargas', 'Ortiz', 'Silva'
        ]

        users = []
        batch_size = 1000

        for i in range(users_to_create):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)

            user = MoodleUser(
                username=f'user{i:05d}',
                firstname=nombre,
                lastname=apellido,
                email=f'{nombre.lower()}.{apellido.lower()}{i}@universidad.edu.ar'
            )
            users.append(user)

            # Bulk create cada 1000 usuarios
            if len(users) >= batch_size:
                MoodleUser.objects.bulk_create(users)
                self.stdout.write(f'  Creados {i+1}/{users_to_create} usuarios...')
                users = []

        # Crear los restantes
        if users:
            MoodleUser.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS(f'✓ {MoodleUser.objects.count()} usuarios creados'))

        # 4. Grupos (2-3 por curso)
        self.stdout.write('Creando grupos...')

        all_users = list(MoodleUser.objects.all())
        groups = []

        for course in courses:
            num_groups = random.randint(2, 3)
            for grupo_num in range(1, num_groups + 1):
                group = Group.objects.create(
                    name=f'Comisión {grupo_num}',
                    course=course,
                    description=f'Comisión {grupo_num} de {course.shortname}'
                )
                groups.append(group)

        self.stdout.write(self.style.SUCCESS(f'✓ {Group.objects.count()} grupos creados'))

        # 5. Inscripciones de usuarios a grupos
        self.stdout.write('Inscribiendo usuarios a grupos...')

        group_members = []
        students_per_group = max(20, users_to_create // len(groups))

        for group in groups:
            # Entre 20 y students_per_group estudiantes por grupo
            num_students = random.randint(20, min(students_per_group, len(all_users)))
            selected_users = random.sample(all_users, num_students)

            for user in selected_users:
                group_members.append(
                    GroupMember(group=group, user=user)
                )

            # Bulk create cada 2000 registros
            if len(group_members) >= 2000:
                GroupMember.objects.bulk_create(group_members, ignore_conflicts=True)
                self.stdout.write(f'  Creados {len(group_members)} miembros de grupos...')
                group_members = []

        if group_members:
            GroupMember.objects.bulk_create(group_members, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'✓ {GroupMember.objects.count()} miembros de grupos creados'))

        # 6. Métodos de inscripción
        self.stdout.write('Creando métodos de inscripción...')

        enrols = []
        for course in courses:
            enrol = Enrol.objects.create(
                course=course,
                enrol='manual',
                status=True
            )
            enrols.append(enrol)

        self.stdout.write(self.style.SUCCESS(f'✓ {Enrol.objects.count()} métodos de inscripción creados'))

        # 7. Inscripciones de usuarios a cursos
        self.stdout.write('Inscribiendo usuarios a cursos...')

        user_enrolments = []

        for enrol in enrols:
            # Obtener todos los usuarios que están en grupos de este curso
            course_users = set()
            for group in enrol.course.groups.all():
                for member in group.members.all():
                    course_users.add(member.user)

            for user in course_users:
                user_enrolments.append(
                    UserEnrolment(
                        enrol=enrol,
                        user=user,
                        timestart=enrol.course.startdate,
                        timeend=enrol.course.enddate
                    )
                )

            # Bulk create cada 2000
            if len(user_enrolments) >= 2000:
                UserEnrolment.objects.bulk_create(user_enrolments, ignore_conflicts=True)
                self.stdout.write(f'  Creadas {len(user_enrolments)} inscripciones...')
                user_enrolments = []

        if user_enrolments:
            UserEnrolment.objects.bulk_create(user_enrolments, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'✓ {UserEnrolment.objects.count()} inscripciones creadas'))

        # 8. Últimos accesos (70% de usuarios con acceso)
        self.stdout.write('Generando datos de accesos (70% de usuarios)...')

        accesses = []

        for course in courses:
            enrolled_users = set()
            for ue in UserEnrolment.objects.filter(enrol__course=course):
                enrolled_users.add(ue.user)

            for user in enrolled_users:
                # 70% de probabilidad de tener acceso
                if random.random() < 0.7:
                    # Acceso en los últimos 60 días
                    days_ago = random.randint(0, 60)
                    access_time = now - timedelta(days=days_ago, hours=random.randint(0, 23))

                    accesses.append(
                        UserLastAccess(
                            user=user,
                            course=course,
                            timeaccess=access_time
                        )
                    )

            # Bulk create cada 5000
            if len(accesses) >= 5000:
                UserLastAccess.objects.bulk_create(accesses, ignore_conflicts=True)
                self.stdout.write(f'  Creados {len(accesses)} registros de acceso...')
                accesses = []

        if accesses:
            UserLastAccess.objects.bulk_create(accesses, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'✓ {UserLastAccess.objects.count()} registros de acceso creados'))

        # Resumen final
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS GENERADOS:'))
        self.stdout.write(f'  Escala: {options["scale"]} (factor {scale_factor}x)')
        self.stdout.write(f'  Categorías: {Category.objects.count()}')
        self.stdout.write(f'  Cursos: {Course.objects.count()} ({courses_to_create // 2} por cuatrimestre)')
        self.stdout.write(f'  Usuarios: {MoodleUser.objects.count()}')
        self.stdout.write(f'  Grupos: {Group.objects.count()}')
        self.stdout.write(f'  Miembros de grupos: {GroupMember.objects.count()}')
        self.stdout.write(f'  Métodos de inscripción: {Enrol.objects.count()}')
        self.stdout.write(f'  Inscripciones: {UserEnrolment.objects.count()}')
        self.stdout.write(f'  Registros de acceso: {UserLastAccess.objects.count()}')
        self.stdout.write('='*70)
        self.stdout.write(self.style.SUCCESS('\n✓ Datos mock cargados exitosamente'))
