# 🏥 Alfa Hospital - Sistema de Gestión Web

<div align="center">
  <img src="hospital/login/static/images/LOGO-COLOR.svg" alt="Alfa Hospital Logo" width="200"/>
  
  [![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org/)
  [![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red.svg)](https://www.microsoft.com/sql-server)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 Descripción

**Alfa Hospital** es un sistema web de gestión hospitalaria desarrollado con Django que permite administrar usuarios del hospital de manera segura y eficiente. El sistema incluye autenticación, autorización y operaciones CRUD completas para la gestión de personal médico y administrativo.

### ✨ Características Principales

- 🔐 **Sistema de autenticación seguro** con sesiones
- 👥 **Gestión completa de usuarios** (CRUD)
- 🛡️ **URLs protegidas** con decoradores personalizados
- 🎨 **Interfaz responsive** con HTML semántico
- 🔒 **Protección CSRF** en todos los formularios
- 📱 **Diseño mobile-first** con CSS moderno

## 🚀 Características Técnicas

### Funcionalidades Implementadas

- ✅ **Registro de usuarios** con validación de datos
- ✅ **Inicio de sesión** con verificación de credenciales
- ✅ **Gestión de sesiones** con middleware personalizado
- ✅ **Listar usuarios** con información detallada
- ✅ **Actualizar usuarios** con formularios pre-llenados
- ✅ **Eliminar usuarios** con confirmación de seguridad
- ✅ **Protección de rutas** mediante decoradores
- ✅ **Cierre de sesión** con limpieza completa

### Seguridad

- 🔐 **Autenticación personalizada** basada en sesiones
- 🛡️ **Decorador @login_required** para proteger vistas
- 🔒 **Tokens CSRF** en todos los formularios POST
- ⚠️ **Validación de datos** en servidor y cliente
- 🚫 **Prevención de acceso no autorizado** a URLs sensibles

## 🛠️ Tecnologías Utilizadas

| Tecnología     | Versión | Propósito                          |
| -------------- | ------- | ---------------------------------- |
| **Python**     | 3.x     | Lenguaje de programación principal |
| **Django**     | 5.2.7   | Framework web backend              |
| **SQL Server** | 2019+   | Base de datos principal            |
| **HTML5**      | -       | Estructura semántica               |
| **CSS3**       | -       | Estilos y diseño responsive        |
| **JavaScript** | ES6+    | Interactividad del frontend        |

## 📁 Estructura del Proyecto

```
Web-page-hospital/
├── hospital/                    # Proyecto Django principal
│   ├── manage.py               # Comando de gestión Django
│   ├── hospital/               # Configuración del proyecto
│   │   ├── settings.py         # Configuraciones
│   │   ├── urls.py            # URLs principales
│   │   └── wsgi.py            # Configuración WSGI
│   └── login/                  # Aplicación principal
│       ├── models.py           # Modelos de datos
│       ├── views.py            # Lógica de las vistas
│       ├── admin.py            # Panel administrativo
│       ├── static/             # Archivos estáticos
│       │   ├── css/
│       │   └── images/
│       ├── templates/          # Plantillas HTML
│       │   ├── index.html
│       │   ├── login.html
│       │   ├── home.html
│       │   ├── control_users.html
│       │   ├── create_user.html
│       │   └── update_user.html
│       └── migrations/         # Migraciones de BD
└── README.md                   # Este archivo
```

## ⚙️ Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- SQL Server 2019 o superior
- ODBC Driver 17 for SQL Server
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/galeyro/Web-page-hospital.git
cd Web-page-hospital
```

### 2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install django
pip install mssql-cli
pip install pyodbc
```

### 4. Configurar base de datos

1. Crear base de datos en SQL Server:

```sql
CREATE DATABASE DJANGO_HOSPITAL;
```

2. Crear usuario Django:

```sql
CREATE LOGIN django WITH PASSWORD = 'SqlUser!2025';
USE DJANGO_HOSPITAL;
CREATE USER django FOR LOGIN django;
ALTER ROLE db_owner ADD MEMBER django;
```

### 5. Ejecutar migraciones

```bash
cd hospital
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## 🖥️ Uso del Sistema

### 1. Página Principal

- Accede a `http://127.0.0.1:8000/`
- Navegación a login y registro

### 2. Registro de Usuario

- Completa el formulario con datos válidos
- Validación automática de campos
- Redirección automática al login

### 3. Inicio de Sesión

- Usa email y contraseña registrados
- Sesión persistente y segura
- Acceso a área protegida

### 4. Gestión de Usuarios

- **Listar**: Ver todos los usuarios registrados
- **Actualizar**: Modificar datos de usuarios existentes
- **Eliminar**: Remover usuarios con confirmación

## 🔧 Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` para configuraciones sensibles:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
DATABASE_NAME=DJANGO_HOSPITAL
DATABASE_USER=django
DATABASE_PASSWORD=SqlUser!2025
DATABASE_HOST=localhost
DATABASE_PORT=1433
```

### Configuración de Producción

Para despliegue en producción, modifica `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas específicas
python manage.py test login.tests
```

## 📊 Modelo de Datos

### Usuario

```python
class Usuario(models.Model):
    nombres = CharField(max_length=100)
    apellidos = CharField(max_length=100)
    cedula = CharField(max_length=20, unique=True)
    telefono = CharField(max_length=15)
    email = EmailField(unique=True)
    fecha_nacimiento = DateField()
    genero = CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    password = CharField(max_length=128)
    fecha_registro = DateTimeField(auto_now_add=True)
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Roadmap

### 🎯 Próximas Funcionalidades

- [ ] Sistema de roles y permisos
- [ ] Historial médico de pacientes
- [ ] Agenda de citas médicas
- [ ] Reportes y estadísticas
- [ ] API REST para integración
- [ ] Notificaciones en tiempo real
- [ ] Sistema de backup automático

### 🔧 Mejoras Técnicas

- [ ] Implementar Django REST Framework
- [ ] Agregar tests unitarios completos
- [ ] Documentación con Sphinx
- [ ] Integración continua con GitHub Actions
- [ ] Containerización con Docker
- [ ] Monitoreo con logging avanzado

## 📋 Changelog

### [1.0.0] - 2025-10-12

#### Agregado

- Sistema de autenticación completo
- CRUD de usuarios funcional
- Protección de URLs con decoradores
- Interfaz responsive con HTML semántico
- Validación de formularios
- Protección CSRF
- Gestión de sesiones

#### Seguridad

- Implementación de @login_required
- Validación de datos en servidor
- Prevención de ataques CSRF
- Limpieza segura de sesiones

## 👥 Equipo de Desarrollo

- **Galo Alejandro** - _Desarrollador Principal_ - [@galeyro](https://github.com/galeyro)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

¿Tienes preguntas o problemas?

- 📧 Email: soporte@alfahospital.com
- 🐛 Issues: [GitHub Issues](https://github.com/galeyro/Web-page-hospital/issues)
- 📖 Documentación: [Wiki del proyecto](https://github.com/galeyro/Web-page-hospital/wiki)

---

<div align="center">
  <p>⭐ ¡Dale una estrella si te gusta el proyecto! ⭐</p>
  <p>Desarrollado con ❤️ para la gestión hospitalaria moderna</p>
</div>
