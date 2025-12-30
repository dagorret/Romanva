  # Para testing rápido (800 usuarios, 50 cursos)
  docker compose exec web python manage.py load_mock_data --clear --scale -4

  # Para mitad de datos (1600 usuarios, 100 cursos)
  docker compose exec web python manage.py load_mock_data --clear --scale -2

  # Para TODOS los datos (3200 usuarios, 200 cursos) - RECOMENDADO
  docker compose exec web python manage.py load_mock_data --clear --scale -1

  Características del nuevo comando:

  ✅ Constantes centralizadas en el archivo:
  - TOTAL_USERS = 3200
  - TOTAL_COURSES = 200
  - NUM_CAREERS = 5
  - NUM_MODALITIES = 2

  ✅ Escalas configurables:
  - --scale -1: Total (3200 usuarios, 200 cursos)
  - --scale -2: Mitad (1600 usuarios, 100 cursos)
  - --scale -4: Cuarto (800 usuarios, 50 cursos)

  ✅ Distribución realista:
  - 5 carreras: Derecho, Economía, Ingeniería, Medicina, Arquitectura
  - 2 modalidades: Grado y Postgrado
  - 200 cursos: 100 primer cuatrimestre (marzo-julio), 100 segundo cuatrimestre (agosto-diciembre)
  - 2-3 comisiones por curso
  - 70% de usuarios con accesos registrados

  ✅ Bulk operations para performance con miles de registros

  Ahora sí, ejecuta ./init.sh o los comandos manualmente para terminar la inicialización.

