# Inicio Rápido - Romanova Platform

## Pasos para ejecutar el sistema

### 1. Levantar servicios

```bash
docker compose up --build -d
```

Espera unos segundos hasta que PostgreSQL esté listo.

### 2. Ejecutar migraciones e inicialización

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### 3. Crear superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

O usa el script automático:

```bash
docker compose exec web bash -c "
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('✓ Superusuario creado: admin / admin123')
else:
    print('✓ Superusuario ya existe')
END
"
```

### 4. Cargar datos de prueba

```bash
docker compose exec web python manage.py load_mock_data --clear
```

Esto generará:
- ✅ 5 categorías
- ✅ 9 cursos (año actual)
- ✅ 60 usuarios
- ✅ 20+ grupos
- ✅ Inscripciones y accesos realistas

### 5. Acceder al sistema

- **Web**: http://localhost:8008
- **Admin**: http://localhost:8008/admin

**Credenciales**: `admin` / `admin123`

## Comandos útiles

### Ver logs en tiempo real
```bash
docker compose logs -f web
```

### Reiniciar el sistema
```bash
docker compose restart
```

### Detener el sistema
```bash
docker compose down
```

### Resetear completamente (CUIDADO: elimina datos)
```bash
docker compose down -v
docker compose up --build -d
# Luego repetir pasos 2-4
```

### Acceder a shell de Python/Django
```bash
docker compose exec web python manage.py shell
```

### Acceder a base de datos
```bash
docker compose exec db psql -U msp_user -d moodle_stats
```

## Verificación

Si todo funciona correctamente:

1. ✅ Puedes hacer login en http://localhost:8000
2. ✅ Ves cursos en el selector del panel
3. ✅ Puedes generar reportes semanales
4. ✅ El menú de "Estadísticas" tiene 6 opciones
5. ✅ El admin muestra todos los modelos

## Problemas comunes

### Error: "port 5432 already in use"
PostgreSQL ya está corriendo en tu sistema.

**Solución**: Cambia el puerto en `docker compose.yml`:
```yaml
ports:
  - "5433:5432"  # Usar 5433 en vez de 5432
```

### Error: "port 8008 already in use"
Otro servicio usa el puerto 8008.

**Solución**: Cambia el puerto en `docker compose.yml`:
```yaml
ports:
  - "8009:8000"  # Usar 8009 en vez de 8008
```

### No se cargan datos mock
**Solución**: Verifica que las migraciones estén aplicadas:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py load_mock_data --clear
```

### Error de permisos
**Solución**: Asegúrate de tener permisos:
```bash
sudo chown -R $USER:$USER .
```

## Próximos pasos

1. Explora el panel de reportes básicos
2. Prueba los diferentes tipos de estadísticas
3. Revisa el código en `apps/moodle/` y `apps/analytics/`
4. Personaliza según tus necesidades
5. Conecta a una base de datos real de Moodle (opcional)

---

**¿Todo listo?** Abre http://localhost:8008 y comienza a usar el sistema.
