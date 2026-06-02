# ⚽ Sport Stats Project
### CBTIS 116 — General Vicente Guerrero
### Implementa Base De Datos Relacionales En Sistema de Información
### Proyecto Final — Equipo 9

**Docente:** Jose Christian Romero Hernandez

**Integrantes:**
- Rosas Varela Bryan Irvin
- Ríos Flores Alan Samuel
- Jovani Rojas Huerta
- Corona Larrinaga Marco Antonio
- Vinalay López Romina Cristal

**4AVPG — Tijuana, B.C., 28 de marzo del 2026**

---

# 📋 Índice

1. Introducción
2. Desarrollo
   - 2.1 Arquitectura General del Sistema
   - 2.2 Explicación del Archivo settings.py
   - 2.3 Explicación del Archivo urls.py
   - 2.4 Diseño de la Base de Datos
   - 2.5 Explicación de los Models
   - 2.6 Relaciones entre los Models
   - 2.7 Funcionamiento del Django Admin
   - 2.8 Entrada, Actualización y Eliminación de Datos
   - 2.9 Explicación de las Views
   - 2.10 Interacción entre URLs, Views y Templates
   - 2.11 Templates e Interfaz de Usuario
3. Conclusiones Finales

---

# 📖 Introducción

El presente proyecto consiste en el desarrollo de una aplicación web deportiva llamada **Sport Stats Project**, creada utilizando el framework Django de Python. La finalidad principal del sistema es administrar información relacionada con ligas, equipos, jugadores, partidos, estadísticas deportivas y un sistema de fichajes mediante un carrito de compras interactivo.

La aplicación fue diseñada para funcionar como una plataforma dinámica y organizada donde los usuarios pueden consultar información deportiva de manera sencilla, mientras que los administradores y usuarios editores tienen la capacidad de gestionar y modificar los datos desde el panel administrativo del sistema.

El proyecto implementa el patrón de arquitectura **MVT (Model - View - Template)** utilizado por Django, permitiendo separar la lógica del sistema, la estructura de la base de datos y la interfaz visual para mantener un desarrollo más limpio, seguro y fácil de mantener.

Dentro del sistema se pueden realizar diferentes funciones como registrar jugadores, crear equipos, administrar ligas deportivas, registrar partidos, actualizar estadísticas, cargar imágenes de jugadores y escudos de equipos, además de permitir la autenticación de usuarios mediante inicio de sesión y registro personalizado.

La base de datos fue desarrollada utilizando **SQLite3**, permitiendo almacenar toda la información del sistema de manera estructurada mediante relaciones entre modelos. Además, se implementó un modelo de usuario personalizado para controlar permisos especiales dentro de la plataforma, diferenciando usuarios normales de usuarios editores.

Por otra parte, el proyecto incorpora el uso del panel administrativo de Django, facilitando operaciones **CRUD (Create, Read, Update y Delete)** para administrar toda la información sin necesidad de manipular directamente la base de datos.

---

# 🛠 Tecnologías Utilizadas

- Python
- Django
- SQLite3
- HTML5
- CSS3
- JavaScript
- Bootstrap

---

# 📌 Características Principales

- Registro de usuarios y autenticación
- Sistema de permisos para editores
- Administración de jugadores y equipos
- Gestión de ligas y partidos
- Sistema de estadísticas deportivas
- Carrito de fichajes
- Importación masiva de jugadores y equipos
- Subida de imágenes de jugadores y escudos
- Panel administrativo de Django
- Sistema automático de limpieza de datos corruptos

---

# 💻 Desarrollo

El presente proyecto fue desarrollado utilizando Django, un framework web basado en Python que permite crear aplicaciones dinámicas, organizadas y seguras mediante el patrón de arquitectura MVT (Model - View - Template).

El sistema desarrollado corresponde a una plataforma deportiva llamada **Sport Stats Project**, cuya finalidad principal es administrar información relacionada con equipos, jugadores, partidos, ligas deportivas, estadísticas individuales, trofeos y un sistema de fichajes mediante un mercado de compras.

La aplicación principal del sistema recibe el nombre de **Estadisticas**, mientras que el proyecto general se llama **Sport_Stats_Project**.

El sistema fue diseñado para que diferentes usuarios puedan interactuar con la plataforma dependiendo de sus permisos:

- **Usuarios editores:** tienen permisos especiales para registrar jugadores, equipos, modificar información y administrar contenido desde el panel del sistema.
- **Usuarios normales:** solo tienen acceso a la plataforma para buscar o seleccionar jugadores.

---

## 2.1 Arquitectura General del Sistema

El proyecto trabaja utilizando el patrón MVT de Django, dividido en tres partes principales:

| Componente | Función |
|---|---|
| **Models** | Maneja la base de datos |
| **Views** | Contiene la lógica del sistema |
| **Templates** | Muestra la interfaz gráfica |

El funcionamiento general del sistema es el siguiente:

'''plaintext
1. El usuario entra a una URL.
2. Django revisa el archivo urls.py.
3. La URL llama una view.
4. La view obtiene datos desde los models.
5. Los datos se envían a un template.
6. El template muestra la información en pantalla.
'''

---

## 2.2 Explicación del Archivo settings.py

El archivo `settings.py` es uno de los archivos más importantes del proyecto porque contiene toda la configuración global del sistema. Desde este archivo se controla prácticamente todo el comportamiento interno de Django.

Dentro de `settings.py` se configuran:

- Aplicaciones instaladas
- Seguridad
- Conexión a la base de datos
- Templates
- Archivos estáticos
- Archivos multimedia
- Autenticación
- Middleware
- Idioma y zona horaria

### BASE_DIR

'''python
BASE_DIR = Path(__file__).resolve().parent.parent
'''

Esta línea define la ruta principal del proyecto. Django utiliza `BASE_DIR` para localizar automáticamente carpetas importantes como templates, imágenes, archivos estáticos y la base de datos principal.

### SECRET_KEY

'''python
SECRET_KEY = 'django-insecure-tu-llave-secreta-aqui'
'''

Funciona como una clave privada utilizada internamente por Django para proteger sesiones, formularios, autenticación y cifrado interno.

### DEBUG

'''python
DEBUG = True
'''

Cuando `DEBUG` está activado, Django muestra errores detallados y facilita el desarrollo. Sin embargo, al publicar el proyecto en internet debe cambiarse a `False` para proteger información sensible.

### ALLOWED_HOSTS

'''python
ALLOWED_HOSTS = ['10.20.7.79', 'localhost', '127.0.0.1', '*']
'''

### INSTALLED_APPS

'''python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Estadisticas',
    'django.contrib.humanize',
]
'''

Cada aplicación cumple una función específica:

- **django.contrib.admin:** Activa el panel administrativo de Django.
- **django.contrib.auth:** Controla usuarios, permisos, autenticación y contraseñas.
- **django.contrib.messages:** Permite mostrar mensajes automáticos.
- **django.contrib.staticfiles:** Administra archivos CSS, JavaScript e imágenes estáticas.
- **django.contrib.humanize:** Convierte números y fechas a formatos legibles para los usuarios.
- **Estadisticas:** Contiene la lógica desarrollada para el proyecto.

### Configuración de archivos multimedia

'''python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
'''

### Base de Datos

'''python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

---

## 2.3 Explicación del Archivo urls.py

El archivo `urls.py` funciona como el sistema principal de navegación del proyecto. Aquí se conectan las rutas del navegador con las views correspondientes.

'''python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Estadisticas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

Esto permite acceder a:

- Página principal
- Login y registro
- Panel de administración (`/admin/`)
- Gestión de jugadores y equipos

---

## 2.4 Diseño de la Base de Datos

La base de datos fue diseñada cuidadosamente para soportar toda la información deportiva manejada por la plataforma. El sistema utiliza **SQLite3** como motor principal debido a que es ligero, rápido, fácil de configurar y muy útil para proyectos académicos.

Toda la información se almacena dentro del archivo:

'''plaintext
db.sqlite3
'''

La estructura relacional permite mantener organizada toda la información evitando duplicaciones innecesarias. Por ejemplo, cuando el sistema consulta un jugador, también puede recuperar:

- El equipo al que pertenece
- La liga donde juega
- Estadísticas relacionadas
- Imágenes asociadas

Django utiliza migraciones para crear automáticamente las tablas dentro de SQLite:

'''bash
python manage.py makemigrations
python manage.py migrate
'''

---

## 2.5 Explicación de los Models

Los Models son uno de los componentes más importantes del proyecto porque representan toda la estructura de la base de datos. En Django, cada modelo creado mediante Python se convierte automáticamente en una tabla dentro de SQLite.

Todos los modelos fueron desarrollados dentro del archivo `Estadisticas/models.py`.

Entre los modelos principales se encuentran: **User, Liga, Equipo, Jugador, Partido, Estadistica, Trofeo, Carrito y MercadoDeFichajes.**

'''python
# coding: utf-8
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Función auxiliar para desinfectar strings binarios corruptos de Excel
def limpiar_string_corrupto(valor):
    if isinstance(valor, str):
        try:
            valor.encode('utf-8')
            return valor
        except (UnicodeDecodeError, UnicodeEncodeError):
            return "".join([c for c in valor if c.isprintable()]).strip() or "Dato Sanado"
    return valor

# ==========================================
# 👤 MODELO DE USUARIO CUSTOM
# ==========================================
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_editor = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='estadisticas_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='estadisticas_user_permissions',
        blank=True
    )
    def __str__(self):
        return str(self.username)

# ==========================================
# 🏆 MODELO DE LIGA
# ==========================================
class Liga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=100, blank=True)
    class Meta:
        verbose_name_plural = "Ligas"
    def __str__(self):
        return limpiar_string_corrupto(self.nombre)

# ==========================================
# 👑 MODELO DE EQUIPO
# ==========================================
class Equipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    liga = models.ForeignKey(Liga, on_delete=models.SET_NULL, null=True, related_name='equipos')
    escudo = models.ImageField(upload_to='escudos/', null=True, blank=True)
    def __str__(self):
        return limpiar_string_corrupto(self.nombre)

# ==========================================
# 🏃 MODELO DE JUGADOR
# ==========================================
class Jugador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    posicion = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    foto = models.ImageField(upload_to='jugadores/', null=True, blank=True)

# ==========================================
# ⚽ MODELO DE PARTIDO
# ==========================================
class Partido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField()
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)

# ==========================================
# 📊 ESTADÍSTICAS DE PARTIDOS
# ==========================================
class EstadisticaPartido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    goles = models.PositiveIntegerField(default=0)
    asistencias = models.PositiveIntegerField(default=0)

# ==========================================
# 🏆 TROFEOS
# ==========================================
class Trofeo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

# ==========================================
# 🛒 CARRITO DE COMPRAS
# ==========================================
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
'''

---

## 2.6 Relaciones entre los Models

### Uno a Muchos (ForeignKey)

'''python
equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
'''

Esto construye una estructura jerárquica organizada: **Liga → Equipo → Jugador → Estadística**.

### Muchos a Muchos (ManyToManyField)

Utilizada en el Carrito y el Mercado de Fichajes:

- Un usuario puede agregar muchos jugadores a su carrito.
- Un mismo jugador puede estar en el carrito de muchos usuarios simultáneamente.

### Identificadores Únicos (UUIDField)

'''python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
'''

El uso de UUID protege el sistema contra ataques de enumeración y manipulación de URLs.

---

## 2.7 Funcionamiento del Django Admin

El panel administrativo de Django permite administrar toda la información deportiva desde una interfaz gráfica, realizando operaciones CRUD:

| Operación | Descripción |
|---|---|
| **Create** | Crear nuevos registros |
| **Read** | Visualizar información |
| **Update** | Modificar datos existentes |
| **Delete** | Eliminar elementos |

---

## 2.8 Entrada, Actualización y Eliminación de Datos

**Entrada de datos (Create):** Al añadir un jugador, Django detecta la ForeignKey hacia Equipo y genera automáticamente un menú de selección. Al guardar ejecuta internamente:

'''sql
INSERT INTO Estadisticas_jugador (...)
'''

**Actualización de datos (Update):** Al modificar un registro, Django lo busca mediante su UUID y ejecuta:

'''sql
UPDATE Estadisticas_jugador SET precio = X WHERE id = UUID
'''

**Eliminación de datos (Delete):** Django analiza las relaciones existentes antes de eliminar. Gracias a `CASCADE`, si un equipo es eliminado, también se eliminan automáticamente sus jugadores relacionados:

'''python
on_delete=models.CASCADE
'''

---

## 2.9 Explicación de las Views

Las views son el intermediario entre URLs, Models y Templates. Cuando un usuario entra a una página:

'''plaintext
1. Django detecta la URL.
2. La URL ejecuta una view.
3. La view procesa la solicitud.
4. La view consulta modelos.
5. Los datos son enviados al template.
6. El template genera HTML dinámico.
'''

Ejemplo de la vista principal:

'''python
@login_required
def rendimiento_carga_masiva(request):
    if not request.user.is_editor:
        return HttpResponseForbidden("Acceso denegado.")

    form_rendimiento = ImportarRendimientoForm(request.POST or None)
    mensaje_error = None

    if request.method == 'POST' and form_rendimiento.is_valid():
        partido_sel = form_rendimiento.cleaned_data['partido']
        lineas = form_rendimiento.cleaned_data['rendimiento_pegado'].strip().split('\n')

        for num_linea, linea in enumerate(lineas, 1):
            partes = linea.strip().split(',')
            if len(partes) >= 5:
                jugador_obj = Jugador.objects.filter(nombre__iexact=partes[0]).first()
                if jugador_obj:
                    EstadisticaPartido.objects.update_or_create(
                        partido=partido_sel,
                        jugador=jugador_obj,
                        defaults={
                            'goles': int(partes[1]),
                            'asistencias': int(partes[2]),
                            'amarillas': int(partes[3]),
                            'rojas': int(partes[4])
                        }
                    )

    return render(request, 'Estadisticas/rendimiento_masivo_form.html', {
        'form_rendimiento': form_rendimiento,
        'mensaje_error': mensaje_error,
        'titulo': 'Carga Masiva de Estadísticas'
    })
'''

El sistema también implementa búsquedas dinámicas:

'''python
Jugador.objects.select_related('equipo__liga').all()
Q(nombre__icontains=query)
'''

---

## 2.10 Interacción entre URLs, Views y Templates

El correcto funcionamiento del sistema depende de la interacción entre sus tres componentes principales:

'''plaintext
Usuario entra al navegador
        ↓
Django recibe solicitud HTTP
        ↓
urls.py identifica la ruta
        ↓
Se ejecuta una view
        ↓
La view procesa la lógica
        ↓
La view consulta models
        ↓
SQLite devuelve información
        ↓
La view envía datos al template
        ↓
El template genera HTML dinámico
        ↓
El navegador muestra resultados
'''

Ejemplo del sistema de URLs:

'''python
urlpatterns = [
    path('', views.home, name='home'),
    path('equipo/<uuid:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('agregar-ideal/<uuid:jugador_id>/', views.agregar_al_equipo_ideal, name='agregar_ideal'),
    path('eliminar-ideal/<uuid:jugador_id>/', views.eliminar_del_equipo_ideal, name='eliminar_ideal'),
    path('panel/rendimiento-masivo/', views.rendimiento_carga_masiva, name='rendimiento_carga_masiva'),
]
'''

---

## 2.11 Templates e Interfaz de Usuario

Los templates utilizan HTML junto con Django Template Language para generar interfaces visuales dinámicas:

'''html
<h1>{{ jugador.nombre }}</h1>
<img src="{{ jugador.foto.url }}">
'''

Ejemplo de template personalizado para el admin:

'''html
{% extends "admin/change_list.html" %}
{% load i18n %}
{% block object-tools-items %}
  <li>
    <a href="add/" style="background-color: #e67e22 !important; color: white !important;
    font-weight: bold; border-radius: 4px; padding: 10px 15px; display: inline-block;">
      🚀 Ir a Carga Masiva (Por Comas)
    </a>
  </li>
  {{ block.super }}
{% endblock %}
'''

---

# 📂 Estructura General del Proyecto

'''plaintext
Sport_Stats_Project/
│
├── Estadisticas/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── templates/
│   └── static/
│
├── media/
├── static/
├── db.sqlite3
├── manage.py
└── README.md
'''

---

# 🚀 Instalación del Proyecto

## 1. Clonar repositorio

'''bash
git clone <url-del-repositorio>
'''

## 2. Crear entorno virtual

'''bash
python -m venv venv
'''

## 3. Activar entorno virtual

### Windows

'''bash
venv\Scripts\activate
'''

### Linux/Mac

'''bash
source venv/bin/activate
'''

## 4. Instalar librerias

'''bash
pip install pillow
pip install django==5.2
'''

## 5. Ejecutar migraciones

'''bash
python manage.py makemigrations
python manage.py migrate
'''

## 6. Crear superusuario

'''bash
python manage.py createsuperuser
'''

## 7. Ejecutar servidor

'''bash
python manage.py runserver
'''

Accede al sistema en: `http://127.0.0.1:8000/`
Panel administrativo en: `http://127.0.0.1:8000/admin/`

---

# 👨‍💻 Funcionalidades del Sistema

✔ Registro de usuarios  
✔ Inicio y cierre de sesión  
✔ Gestión de jugadores  
✔ Gestión de equipos  
✔ Gestión de ligas  
✔ Sistema de estadísticas  
✔ Sistema de fichajes  
✔ Importación masiva  
✔ Subida de imágenes  
✔ Panel administrativo  

---

# 📖 Conclusión Final

El desarrollo del proyecto Sport Stats Project permitió comprender de manera práctica el funcionamiento del framework Django y la forma en que interactúan sus principales componentes dentro de una aplicación web dinámica. A lo largo del proyecto fue posible implementar correctamente el patrón de arquitectura MVT (Model - View - Template), logrando separar la lógica del sistema, la base de datos y la interfaz gráfica de usuario para mantener una estructura organizada y funcional.

Mediante el uso de models se diseñó una base de datos capaz de administrar información relacionada con jugadores, equipos, ligas, partidos, estadísticas y usuarios. Las views permitieron controlar toda la lógica del proyecto, procesando solicitudes de los usuarios, realizando consultas a la base de datos y enviando información hacia los templates.

El panel administrativo de Django facilitó enormemente la gestión de información mediante operaciones CRUD, permitiendo crear, modificar y eliminar registros de manera rápida y segura sin necesidad de trabajar directamente sobre la base de datos.

Finalmente, este proyecto ayudó a fortalecer conocimientos sobre desarrollo web, bases de datos, organización de proyectos en Django y funcionamiento interno de aplicaciones dinámicas, demostrando cómo un framework puede facilitar la creación de sistemas modernos, seguros y escalables.

---

**CBTIS 116 — Tijuana, B.C. — 2026**
