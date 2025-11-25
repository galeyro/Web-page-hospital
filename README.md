# 🏥 Alfa Hospital - Sistema de Gestión Web

<div align="center">
  <img src="hospital/login/static/images/LOGO-COLOR.svg" alt="Alfa Hospital Logo" width="200"/>
  
  [![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org/)
  [![Render](https://img.shields.io/badge/Deployed-Render-46E3B7.svg)](https://render.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 Descripción

**Alfa Hospital** es un sistema web de gestión hospitalaria desarrollado con Django que permite administrar usuarios del hospital con operaciones CRUD y protección de URLs. La aplicación está completamente deployada en Render.

### 🌐 Link de la aplicación

🚀 **[Acceder a Alfa Hospital en Render](https://web-page-hospital.onrender.com/)**

**Credenciales de acceso:**
- Email: `admin@admin.com`
- Contraseña: `admin`

### ✨ Características Principales

- 🔐 **Sistema de autenticación seguro** con sesiones
- 👥 **Gestión completa de usuarios** (CRUD)
- 🛡️ **URLs protegidas** con decoradores personalizados
- 🎨 **Interfaz responsive** con HTML semántico
- 🔒 **Protección CSRF** en todos los formularios

## 🚀 Características Técnicas

### Funcionalidades Implementadas

- ✅ **Registro de usuarios** con validación de datos
- ✅ **Inicio de sesión** 
- ✅ **Gestión de sesiones** con middleware 
- ✅ **Listar usuarios**
- ✅ **Actualizar usuarios** con formularios pre-llenados
- ✅ **Eliminar usuarios** con confirmación de seguridad
- ✅ **Protección de rutas** mediante decoradores
- ✅ **Cierre de sesión** con limpieza completa
- ✅ **Validación de cédula ecuatoriana**
- ✅ **Sistema de roles** (Admin, Médico, Usuario)
- ✅ **Dashboard personalizado** por rol

### Seguridad

- 🔐 **Autenticación personalizada** basada en sesiones
- 🛡️ **Decorador @login_required** para proteger vistas
- 🔒 **Tokens CSRF** en todos los formularios POST
- ⚠️ **Validación de datos** en servidor y cliente
- 🚫 **Prevención de acceso no autorizado** a URLs sensibles

## 🛠️ Tecnologías Utilizadas

| Tecnología     | Versión | Propósito                          |
| -------------- | ------- | ---------------------------------- |
| **Python**     | 3.13    | Lenguaje de programación principal |
| **Django**     | 5.2.7   | Framework web backend              |
| **SQLite**     | 3       | Base de datos                      |
| **Gunicorn**   | 23.0.0  | Servidor WSGI                      |
| **WhiteNoise** | 6.6.0   | Servir archivos estáticos          |
| **Render**     | -       | Plataforma de hosting              |
| **HTML5**      | -       | Estructura semántica               |
| **CSS3**       | -       | Estilos y diseño responsive        |


## 📁 Estructura del Proyecto

```
Web-page-hospital/
├── hospital/                   # Proyecto Django principal
│   ├── manage.py               # Comando de gestión Django
│   ├── requirements.txt        # Dependencias Python
│   ├── Procfile                # Configuración para Render
│   ├── runtime.txt             # Versión de Python
│   ├── startup.sh              # Script de inicialización
│   ├── create_admin.py         # Script para crear admin
│   ├── hospital/               # Configuración del proyecto
│   │   ├── settings.py         # Configuraciones
│   │   ├── urls.py             # URLs principales
│   │   └── wsgi.py             # WSGI app
│   ├── login/                  # Aplicación principal
│   │   ├── models.py           # Modelos de datos
│   │   ├── views.py            # Lógica de las vistas
│   │   ├── forms.py            # Formularios
│   │   ├── validators.py       # Validadores personalizados
│   │   ├── admin.py            # Panel administrativo
│   │   ├── static/             # Archivos estáticos
│   │   │   ├── css/
│   │   │   └── images/
│   │   ├── templates/          # Plantillas HTML
│   │   │   ├── index.html
│   │   │   ├── login.html
│   │   │   ├── home.html
│   │   │   ├── control_users.html
│   │   │   ├── create_user.html
│   │   │   └── update_user.html
│   │   └── migrations/         # Migraciones de BD
│   └── citas/                  # Aplicación de citas
│       ├── models.py           # Modelos de citas
│       ├── views.py            # Vistas de citas
│       └── migrations/         # Migraciones
└── README.md                   # Este archivo
```

## ⚙️ Instalación y Configuración Local

### Prerrequisitos

- Python 3.11 o superior
- Git
- Pip (gestor de paquetes de Python)

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
cd hospital
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo

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
- Validación automática de cédula ecuatoriana
- Validación de teléfono (10 dígitos)
- Validación de edad (mayor de 18 años)
- Redirección automática al login

### 3. Inicio de Sesión

- Usa email y contraseña registrados
- Sesión persistente y segura
- Redireccionamiento según rol

### 4. Gestión de Usuarios (Admin)

- **Listar**: Ver todos los usuarios registrados
- **Actualizar**: Modificar datos de usuarios existentes
- **Eliminar**: Remover usuarios con confirmación
- **Cambiar rol**: Asignar roles (Admin, Médico, Usuario)


## 📊 Modelo de Datos

### Usuario

```python
class Usuario(models.Model):
    ROLES_CHOICES = [
        ('usuario', 'Usuario'),
        ('medico', 'Médico'),
        ('admin', 'Administrador')
    ]
    
    nombres = CharField(max_length=100)
    apellidos = CharField(max_length=100)
    cedula = CharField(max_length=20, unique=True)  # Validada
    telefono = CharField(max_length=15)  # 10 dígitos
    email = EmailField(unique=True)
    fecha_nacimiento = DateField()  # Mayor de 18 años
    genero = CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    password = CharField(max_length=128)  # Hasheada
    rol = CharField(max_length=10, choices=ROLES_CHOICES, default='usuario')
    fecha_registro = DateTimeField(auto_now_add=True)
```

## 🚀 Deployment en Render

### Configuración actual

- **Plataforma**: Render (plan Free)
- **URL**: https://web-page-hospital.onrender.com
- **Base de datos**: SQLite
- **Servidor**: Gunicorn
- **Archivos estáticos**: WhiteNoise

### Proceso de deployment

El deployment automático incluye:

1. **Build**: Instala dependencias y recoge archivos estáticos
2. **Startup**: Ejecuta migraciones y crea usuario admin
3. **Deploy**: Inicia Gunicorn en el puerto 10000

### Archivos de configuración

- `requirements.txt`: Dependencias de Python
- `Procfile`: Configuración de servicios
- `runtime.txt`: Versión de Python (3.11.7)
- `startup.sh`: Script de inicialización
- `create_admin.py`: Script para crear admin

### Variables de entorno en Render

```
DEBUG=False
SECRET_KEY=<clave_segura_generada>
ALLOWED_HOSTS=web-page-hospital.onrender.com
```

## 📋 Changelog

### [2.0.0] - 2025-11-16

**Nuevo:**
- ✅ Deployment en Render
- ✅ Configuración para producción
- ✅ Script de inicialización automática
- ✅ Sistema de roles mejorado
- ✅ Validación de cédula ecuatoriana
- ✅ Seguridad SSL/TLS en producción

**Mejorado:**
- 🔄 Settings.py configurado con variables de entorno
- 🔄 WhiteNoise para servir archivos estáticos
- 🔄 Decoradores de protección mejorados

### [1.0.0] - 2025-10-12

**Inicial:**
- CRUD completo de usuarios
- Sistema de autenticación
- Protección de URLs
- Validación de formularios

## 👥 Equipo de Desarrollo

- _Desarrollador Principal_ - [@galeyro](https://github.com/galeyro)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre un issue primero para discutir los cambios propuestos.

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio de GitHub.

---

<div align="center">
  <p>⭐ ¡Dale una estrella si te gusta el proyecto! ⭐</p>
  <p>Desarrollado con ❤️ usando Django</p>
  <p>Desplegado en 🚀 Render</p>
</div>
