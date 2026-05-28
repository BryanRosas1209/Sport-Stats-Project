# ⚽ Sport Stats Project

Proyecto web desarrollado con Django para la administración de estadísticas deportivas, equipos, jugadores y fichajes.

El sistema permite gestionar información relacionada con ligas deportivas, jugadores, equipos, partidos, estadísticas individuales y un sistema de carrito de fichajes, utilizando una interfaz dinámica y organizada.

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

# 🛠 Tecnologías Utilizadas

- Python
- Django
- SQLite3
- HTML5
- CSS3
- JavaScript
- Bootstrap

---

# 📂 Estructura General del Proyecto

```plaintext
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
```

---

# ⚙️ Configuración del Proyecto

El archivo `settings.py` contiene toda la configuración principal del sistema:

- configuración de base de datos,
- aplicaciones instaladas,
- archivos multimedia,
- autenticación,
- archivos estáticos,
- templates,
- permisos.

## Base de Datos

El proyecto utiliza SQLite3:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

# 🔗 Sistema de URLs

El archivo `urls.py` controla la navegación del sistema y conecta las rutas con las views correspondientes.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Estadisticas.urls')),
]
```

Esto permite acceder a:

- página principal,
- login,
- registro,
- panel de administración,
- gestión de jugadores y equipos.

---

# 🧠 Models Principales

## 👤 User


 Su función es definir la estructura principal de la base de datos utilizando modelos de Django. Aquí se crean los modelos para usuarios, ligas, equipos, jugadores, partidos, estadísticas, trofeos y carrito de compras.
```
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
```

Modelo de usuario personalizado con permisos especiales para editores.

Campos principales:

- username
- password
- is_editor

---

## 🏆 Liga

Representa ligas deportivas registradas en el sistema.

Campos:

- nombre
- pais

---

## 👑 Equipo

Representa equipos deportivos.

Campos:

- nombre
- ciudad
- liga
- escudo

Relación:

- Una liga puede tener muchos equipos.

---

## 🏃 Jugador

Representa jugadores registrados.

Campos:

- nombre
- posicion
- equipo
- precio
- foto

Relación:

- Un equipo puede tener muchos jugadores.

---

## ⚽ Partido

Representa encuentros deportivos entre equipos.

Campos:

- equipo_local
- equipo_visitante
- goles
- fecha
- torneo

---

## 📊 EstadisticaPartido

Guarda estadísticas individuales de jugadores por partido.

Campos:

- goles
- asistencias
- tarjetas amarillas
- tarjetas rojas

---

## 🛒 Cart y CartItem

Implementan el sistema de carrito de fichajes deportivos.

---

# 🔄 Funcionamiento de las Views

Las views contienen toda la lógica funcional del sistema.

Las views:

- reciben solicitudes desde las URLs,
- consultan datos desde los models,
- procesan información,
- envían datos a los templates.

Ejemplo:

```python
def home(request):
    jugadores_list = Jugador.objects.all()

    return render(request, 'Estadisticas/home.html', {
        'page_obj': jugadores_list
    })
```

---

# 🌐 Interacción entre URLs, Views y Templates

El sistema trabaja siguiendo el patrón MVT de Django:

```plaintext
Usuario
   ↓
URL
   ↓
View
   ↓
Model
   ↓
Base de Datos
   ↓
Template
   ↓
Interfaz Web
```

Las URLs llaman las views, las views consultan los models y los templates muestran la información visualmente.

---

# 🛡️ Panel Administrativo

Django incluye un panel administrativo para gestionar toda la base de datos.

Ruta:

```plaintext
/admin/
```

Desde el admin se pueden:

- crear jugadores,
- editar equipos,
- eliminar registros,
- administrar usuarios,
- modificar estadísticas.

---

# 📸 Archivos Multimedia

El sistema permite subir:

- fotos de jugadores,
- escudos de equipos.

Configuración:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

# 🚀 Instalación del Proyecto

## 1. Clonar repositorio

```bash
git clone <url-del-repositorio>
```

---

## 2. Crear entorno virtual

```bash
python -m venv env
```

---

## 3. Activar entorno virtual

### Windows

```bash
env\Scripts\activate
```

### Linux/Mac

```bash
source env/bin/activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Ejecutar migraciones

```bash
python manage.py migrate
```

---

## 6. Ejecutar servidor

```bash
python manage.py runserver
```

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

# 📖 Conclusión

Sport Stats Project es una aplicación web desarrollada en Django que permite administrar información deportiva de manera organizada, dinámica y segura. El sistema integra autenticación, administración de estadísticas, relaciones entre modelos, carga de imágenes y gestión de fichajes mediante una arquitectura basada en el patrón MVT.


