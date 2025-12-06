# ✅ Checklist de Verificación - Moodle Stats

Use este checklist para verificar que todo funcione correctamente.

## 📋 Pre-instalación

- [ ] Docker está instalado (`docker --version`)
- [ ] Docker Compose está instalado (`docker-compose --version`)
- [ ] Tienes las credenciales de la BD de Moodle
- [ ] Tienes permisos de escritura en el directorio del proyecto

## 📋 Instalación

- [ ] Archivo extraído correctamente
- [ ] `docker-compose.yml` editado con credenciales de Moodle
- [ ] Directorio `data/` creado
- [ ] Directorio `staticfiles/` creado
- [ ] `install.sh` tiene permisos de ejecución
- [ ] `entrypoint.sh` tiene permisos de ejecución

## 📋 Primer Inicio

- [ ] Contenedor construido sin errores (`docker-compose build`)
- [ ] Contenedor iniciado correctamente (`docker-compose up -d`)
- [ ] No hay errores en los logs (`docker-compose logs`)
- [ ] Admin accesible en http://localhost:8008/admin/
- [ ] Puedes iniciar sesión con admin/admin

## 📋 Conexión a Moodle

- [ ] Script de prueba ejecutado (`test_connection.py`)
- [ ] Conexión a Moodle exitosa
- [ ] Se ven las tablas de Moodle
- [ ] Se puede contar usuarios y cursos

## 📋 Primera Importación

- [ ] Botón "Importar desde Moodle" visible en el admin
- [ ] Primera tabla importada sin errores (ej: courses)
- [ ] Registros visibles en el admin
- [ ] Log de importación creado
- [ ] Cuenta de registros correcta

## 📋 Funcionalidades del Admin

- [ ] Filtros funcionan correctamente
- [ ] Búsqueda funciona correctamente
- [ ] Paginación funciona (si hay >100 registros)
- [ ] Detalles de registro se pueden ver
- [ ] No hay errores 500 en ninguna página

## 📋 Exportación a Excel

- [ ] Acción "Exportar a Excel" visible
- [ ] Se pueden seleccionar registros
- [ ] Export se descarga correctamente
- [ ] Archivo Excel se abre sin errores
- [ ] Datos en Excel coinciden con BD

## 📋 Importación Masiva (CLI)

- [ ] Comando `import_moodle --list` funciona
- [ ] Comando `import_moodle` sin parámetros funciona
- [ ] Comando con `--tables` funciona
- [ ] Todas las tablas se importan correctamente
- [ ] Logs de importación actualizados

## 📋 Persistencia de Datos

- [ ] `data/db.sqlite3` existe en el host
- [ ] Contenedor se puede parar y reiniciar sin perder datos
- [ ] Archivos en `staticfiles/` persisten
- [ ] Datos importados permanecen después de reinicio

## 📋 Rendimiento

- [ ] Importación de tabla pequeña (<1k) toma <1 min
- [ ] Importación de tabla mediana (<50k) toma <10 min
- [ ] No hay timeouts en el admin
- [ ] Búsqueda responde en <2 segundos
- [ ] Exportación a Excel responde en <10 segundos

## 📋 Logs y Debugging

- [ ] Logs de Django son legibles
- [ ] Logs de importación muestran progreso
- [ ] Errores se muestran claramente
- [ ] Stack traces disponibles cuando hay errores
- [ ] Healthcheck de Docker funciona

## 📋 Seguridad (Producción)

Si vas a usar en producción:

- [ ] SECRET_KEY cambiada en settings.py
- [ ] DEBUG = False en settings.py
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] Contraseña del admin cambiada
- [ ] Puerto 8008 no expuesto directamente
- [ ] HTTPS configurado (nginx + Let's Encrypt)
- [ ] Firewall configurado
- [ ] Backups automáticos configurados
- [ ] PostgreSQL en lugar de SQLite
- [ ] Contraseñas en variables de entorno o secretos

## 📋 Documentación

- [ ] README.md leído
- [ ] ADMIN_API.md consultado
- [ ] PROJECT_SUMMARY.md revisado
- [ ] QUICKSTART.md entendido
- [ ] config.example.env usado como referencia

## 📋 Monitoreo

Para producción, considera:

- [ ] Logs centralizados (ELK, CloudWatch, etc.)
- [ ] Alertas por email cuando fallan importaciones
- [ ] Métricas de uso (cuántas importaciones, tiempos, etc.)
- [ ] Monitoreo de disco (data/ puede crecer)
- [ ] Backup automático de la BD
- [ ] Rotación de logs

## 📊 Resumen Final

### ✅ Todo OK
Si todos los items anteriores están marcados, ¡felicidades! Tu sistema está listo.

### ⚠️ Algunos items pendientes
Revisa los items no marcados y consulta la documentación o los logs.

### ❌ Muchos items fallando
Considera:
1. Verificar la instalación de Docker
2. Revisar las credenciales de Moodle
3. Consultar los logs: `docker-compose logs -f`
4. Probar la conexión: `test_connection.py`
5. Buscar errores específicos en la documentación

## 🆘 Soporte

Si necesitas ayuda:
1. Revisa los logs: `docker-compose logs`
2. Lee la documentación incluida
3. Verifica la configuración en `docker-compose.yml`
4. Prueba la conexión con `test_connection.py`

## 📝 Notas

```
Fecha de verificación: _____________
Persona: _____________
Resultado: ✅ OK / ⚠️ Con problemas / ❌ Falló
Notas adicionales:





```

---

**Versión del Checklist:** 1.0.0
**Fecha:** Diciembre 2024
