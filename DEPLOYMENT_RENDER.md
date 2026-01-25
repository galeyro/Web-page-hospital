# 📋 CHECKLIST PARA DEPLOY EN RENDER

## ✅ Archivos Creados

- [x] `requirements.txt` - Dependencias de Python
- [x] `Procfile` - Instrucciones de ejecución
- [x] `runtime.txt` - Versión de Python
- [x] `.env.example` - Ejemplo de variables de entorno
- [x] `build.sh` - Script de construcción
- [x] `settings.py` actualizado - Configuración para producción

## 🔧 PRÓXIMOS PASOS EN RENDER

### 1. **Commit y Push a GitHub**

```bash
git add .
git commit -m "Add deployment files for Render"
git push origin dev/crud/galo
```

### 2. **Configurar en Render**

En la pantalla de creación del Web Service, asegúrate de:

- **Name**: `web-page-hospital` (o el que prefieras)
- **Source**: `galeyro/Web-page-hospital`
- **Branch**: `main` (o la rama que uses)
- **Language**: Python 3 (Render intentará detectar tb Node para el frontend)
- **Build Command**: `./build.sh`
- **Start Command**: `cd hospital && gunicorn hospital.wsgi:application`
- **Root Directory**: `.` (Déjalo vacío o pon . para usar la raíz del repo)

> **Nota**: Al usar `./build.sh`, Render instalará las dependencias de Node.js y compilará el frontend automáticamente antes de preparar el backend.

### 3. **Configurar Variables de Entorno**

En Render, añade estas variables en **Environment Variables**:

```
SECRET_KEY=tu_clave_secreta_super_segura_aqui
DEBUG=False
ALLOWED_HOSTS=web-page-hospital.onrender.com,localhost
DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
```

**Para generar una SECRET_KEY segura**, usa en terminal:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. **Base de Datos (IMPORTANTE)**

Por defecto SQLite, pero Render NO lo soporta bien.

**Opción A: Usar PostgreSQL (Recomendado)**

- Crea una PostgreSQL database en Render
- Usa la DATABASE_URL que te genera
- Render la conectará automáticamente

**Opción B: Mantener SQLite** (Solo para pruebas)

- Requiere disco persistente (requiere plan pagado)
- No recomendado para producción

### 5. **Archivos Estáticos**

Los archivos CSS e imágenes se servirán automáticamente desde `/staticfiles`

## ⚠️ IMPORTANTE - ANTES DE HACER DEPLOY

1. **Cambia `DEBUG = False` en variables de entorno**
2. **Genera una nueva SECRET_KEY** (la actual está expuesta)
3. **Configura ALLOWED_HOSTS** con tu dominio de Render
4. **Revisa que no haya datos sensibles** en los archivos
5. **Test local**: `python manage.py runserver --insecure` con DEBUG=False

## 🚀 DEPLOY

Una vez configurado todo en Render, simplemente haz click en "Deploy" y Render:

1. Clonará tu repositorio
2. Instalará dependencias (`requirements.txt`)
3. Ejecutará el comando de build
4. Ejecutará migraciones
5. Iniciará la aplicación con Gunicorn

## 📊 Monitoreo Post-Deploy

- Ve a tu dashboard de Render
- Revisa los logs en la sección "Logs"
- Si hay errores, aparecerán allí

## ⚡ Troubleshooting

Si los estáticos no carga (CSS/imágenes rotos):

```
En Render, ejecuta: python manage.py collectstatic --no-input
```

Si la BD tiene errores:

```
En Render: python manage.py migrate
```

Si necesitas creador un superusuario:

```
En Render: python manage.py createsuperuser
```

---

**¡Listo para despegar! 🚀**
