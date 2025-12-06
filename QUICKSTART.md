# 🚀 Guía de Despliegue Rápido - Moodle Stats

## ¿Qué es esto?

Sistema Django completo para **importar, almacenar y analizar datos desde Moodle**.

## ✨ Características

- ✅ Importa 10 tablas de Moodle (usuarios, cursos, inscripciones, etc.)
- ✅ Admin de Django para gestionar datos
- ✅ Exportación a Excel
- ✅ Docker con datos persistentes en el host
- ✅ Tres formas de importar: UI, CLI, o programáticamente

## 📦 Contenido del Paquete

```
moodle-stats/
├── README.md              ← LEE ESTO PRIMERO
├── ADMIN_API.md           ← Documentación del admin
├── PROJECT_SUMMARY.md     ← Resumen ejecutivo
├── docker-compose.yml     ← Configuración Docker
├── Dockerfile
├── requirements.txt
├── install.sh             ← Script de instalación automática
├── test_connection.py     ← Prueba de conexión a Moodle
├── manage.py
├── moodlestats/          ← Proyecto Django
├── moodledata/           ← App con modelos y admin
└── data/                 ← BD SQLite (creada al iniciar)
```

## 🎬 Inicio en 3 Pasos

### 1. Extraer el archivo

```bash
tar -xzf moodle-stats-v1.0.tar.gz
cd moodle-stats/
```

### 2. Configurar conexión a Moodle

Edita `docker-compose.yml` y cambia estas líneas:

```yaml
environment:
  - MOODLE_DB_HOST=localhost        # ← Cambia esto
  - MOODLE_DB_NAME=moodle           # ← Cambia esto
  - MOODLE_DB_USER=moodle_user      # ← Cambia esto
  - MOODLE_DB_PASSWORD=tu_password  # ← Cambia esto
```

### 3. Iniciar

**Opción A - Instalación automática:**
```bash
./install.sh
```

**Opción B - Manual:**
```bash
docker-compose up -d --build
```

¡Listo! Accede a: **http://localhost:8008/admin/**
- Usuario: `admin`
- Contraseña: `admin`

## 🔍 Probar Conexión a Moodle

Antes de importar, prueba que la conexión funcione:

```bash
docker-compose exec web python test_connection.py
```

Si ves ✅, todo está bien. Si ves ❌, revisa la configuración.

## 📥 Importar Datos

### Desde el Admin (Recomendado)
1. Ve a http://localhost:8008/admin/
2. Click en cualquier tabla (ej: "Usuarios")
3. Click en "Importar desde Moodle" (botón verde)
4. Confirma

### Desde la Terminal
```bash
# Todas las tablas
docker-compose exec web python manage.py import_moodle

# Solo algunas
docker-compose exec web python manage.py import_moodle --tables users,courses

# Ver tablas disponibles
docker-compose exec web python manage.py import_moodle --list
```

## 📊 Ver Datos

1. En el admin, entra a cualquier tabla
2. Usa filtros y búsqueda para encontrar datos
3. Selecciona registros y exporta a Excel

## 📚 Documentación Completa

- **README.md** - Guía completa de instalación y uso
- **ADMIN_API.md** - Documentación del admin y API
- **PROJECT_SUMMARY.md** - Resumen técnico del proyecto

## 🔧 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Reiniciar
docker-compose restart

# Entrar al contenedor
docker-compose exec web bash

# Crear superusuario adicional
docker-compose exec web python manage.py createsuperuser
```

## 🐛 Problemas Comunes

### "No se puede conectar a Moodle"
1. Verifica que el host sea accesible desde Docker
2. Revisa que las credenciales sean correctas
3. Asegúrate que MySQL acepte conexiones remotas

### "BD bloqueada"
```bash
docker-compose down
docker-compose up -d
```

### "Permisos denegados"
```bash
sudo chown -R $USER:$USER ./data ./staticfiles
```

## 🔒 Seguridad

⚠️ **En producción:**
1. Cambia la SECRET_KEY en `settings.py`
2. Establece DEBUG=False
3. Configura ALLOWED_HOSTS
4. Cambia las credenciales del admin
5. Usa HTTPS (nginx + Let's Encrypt)

## 💡 Tips

- Los datos en `./data/` y `./staticfiles/` persisten incluso si eliminas el contenedor
- Puedes modificar el código y se actualizará automáticamente (hot-reload)
- Para tablas grandes (>100k registros), usa el comando CLI en lugar del admin
- Revisa los logs de importación en el admin para ver errores

## 📞 Soporte

Para más información, lee los archivos de documentación incluidos:
- README.md (guía completa)
- ADMIN_API.md (documentación del admin)
- PROJECT_SUMMARY.md (resumen técnico)

## 🎓 Tecnologías

- Django 5.1
- Docker + Docker Compose
- SQLite (dev) / MySQL (Moodle)
- openpyxl (exportación Excel)
- mysql-connector-python

## ✅ Checklist de Despliegue

- [ ] Extraer archivo
- [ ] Editar docker-compose.yml con datos de Moodle
- [ ] Ejecutar `docker-compose up -d --build`
- [ ] Probar conexión con `test_connection.py`
- [ ] Acceder al admin (http://localhost:8008/admin/)
- [ ] Importar primera tabla de prueba
- [ ] Verificar datos importados
- [ ] Importar resto de tablas

## 🎉 ¡Éxito!

Si llegaste hasta aquí, tu sistema está listo para usar.

Siguiente paso: Lee **README.md** para entender todas las capacidades del sistema.

---

**Autor:** Carlos Dagorret
**Versión:** 1.0.0
**Fecha:** Diciembre 2024
