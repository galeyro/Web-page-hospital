# 🏥 Alfa Hospital – Sistema Web de Gestión Hospitalaria

📋 **Descripción**  
Alfa Hospital es un sistema web desarrollado con **Django** para la gestión hospitalaria, incluyendo autenticación de usuarios, control de accesos y administración de citas médicas. El proyecto está organizado siguiendo las mejores prácticas de Django, separando la lógica en **apps independientes** para mayor mantenibilidad y escalabilidad.

---

## ✨ Características Principales

### 🔐 Autenticación y Control de Sesiones
- Sistema de login seguro basado en sesiones.
- Protección CSRF en todos los formularios.
- Decoradores personalizados para restringir acceso.

### 👥 Gestión de Usuarios
- CRUD de usuarios del hospital.
- Formularios validados en servidor y cliente.
- Vistas protegidas para evitar accesos no autorizados.

### 🗓️ Gestión de Citas Médicas
- Módulo independiente para manejar citas.
- Contiene la información y la lógica core del negocio.
- Integración con el sistema de autenticación.
- Rutas incluidas en las rutas del proyecto.

### 🎨 Interfaz
- HTML con estructura semántica y organizada.
- Archivos estáticos separados en cada app.
    - Permite que el estilo de cada app sea manejado por separado en caso de ser necesario.
- Plantillas integradas con el sistema de vistas.

---

## 🚀 Características Técnicas

### Funcionalidades Implementadas
- ✅ Registro de usuarios  
- ✅ Inicio de sesión y cierre seguro  
- ✅ Protección de rutas con decoradores  
- ✅ CRUD de usuarios (crear, listar, editar, eliminar)  
- ✅ Gestión de citas médicas en app independiente.
- ✅ Uso de la logica core en la app de citas médicas.
- ✅ Templates organizados por aplicación  
- ✅ Migraciones automáticas por app  
- ✅ Manejo de archivos estáticos por módulo  

---

## 🔒 Seguridad
- 🔐 Autenticación mediante sesiones  
- 🛡️ Decoradores personalizados (`@login_required`)  
- 🔒 Tokens CSRF en todos los formularios  
- ⚠️ Validación de datos en servidor y cliente  
- 🚫 Bloqueo de acceso a URLs privadas sin autenticación  

---

## 🗂️ Estructura del Proyecto

La estructura del proyecto está organizada en un **proyecto Django principal** llamado `alfahospital` y dos aplicaciones internas: **login** y **citasmedicas**.

```
Web-page-hospital/
│── manage.py # Comando principal de Django
│── requirements.txt # Dependencias del proyecto
│── sonar-project.properties # Configuración de análisis de Sonar
│
├── alfahospital/ # Proyecto Django principal
│ ├── settings.py # Configuraciones globales del proyecto
│ ├── urls.py # Rutas principales del sistema
│ ├── wsgi.py # Configuración para despliegue WSGI
│ └── asgi.py # Configuración para ASGI
│
├── login/ # App de autenticación y gestión de usuarios
│ ├── models.py # Modelos de usuario
│ ├── views.py # Lógica del login y CRUD
│ ├── urls.py # Rutas específicas de la app
│ ├── admin.py # Registro para el panel admin
│ ├── static/ # Archivos CSS, JS e imágenes
│ └── templates/ # Plantillas HTML del login y usuarios
│
├── citasmedicas/ # App para gestión de citas médicas
│ ├── models.py # Modelos de citas
│ ├── views.py # Lógica de citas
│ ├── urls.py # Rutas de la app
│ ├── admin.py # Configuración en el admin
│ ├── static/ # Archivos estáticos de la app
│ └── templates/ # Plantillas HTML para citas médicas
│
└── venv/ # Entorno virtual
```

---

## 🧩 Explicación de las Carpetas

### 📁 `alfahospital/`
Proyecto principal de Django. Contiene:
- Configuración global del sistema.
- Rutas principales.

---

### 📁 `login/`
App destinada a:
- Autenticación de usuarios.
- Manejo de login/logout y control de acceso.
- Templates y archivos estáticos relacionados.

---

### 📁 `citasmedicas/`
App que gestiona:
- Modelos de citas médicas y relacionados.
- Lógica de creación, listado y actualización (CRUD de citas médicas).
- Lógica propia de negocio, el Core propiamente dicho.
- Templates y recursos propios de la app.

---

## 📦 Instalación y Ejecución

```bash
# Clonar repositorio
git clone https://github.com/galeyro/Web-page-hospital.git
cd Web-page-hospital
```

```bash
# Inicializar proyecto:
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias -> Solo utilizamos Django de momento
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver