# coding: utf-8
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

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
        try:
            return str(self.username)
        except:
            return "Usuario Anonimo"

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
        try:
            # Blindaje contra bytes corruptos en la base de datos
            return self.nombre.encode('utf-8', errors='ignore').decode('utf-8')
        except:
            return "Liga"

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
        try:
            # Blindaje para evitar que falle al renderizar el string del Equipo
            return self.nombre.encode('utf-8', errors='ignore').decode('utf-8')
        except:
            return "Equipo"

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

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

    def __str__(self):
        try:
            return self.nombre.encode('utf-8', errors='ignore').decode('utf-8')
        except:
            return "Jugador"

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
    torneo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        try:
            return f"{self.equipo_local} - {self.equipo_visitante}"
        except:
            return "Partido"

# ==========================================
# 📊 RENDIMIENTO DE PARTIDOS
# ==========================================
class EstadisticaPartido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='rendimiento_partidos')
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='estadisticas')
    goles = models.PositiveIntegerField(default=0)
    asistencias = models.PositiveIntegerField(default=0)
    amarillas = models.PositiveIntegerField(default=0)
    rojas = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('jugador', 'partido')

    def __str__(self):
        try:
            return f"Stats - {self.jugador.nombre}"
        except:
            return "EstadisticaPartido"

# ==========================================
# 🏆 TROFEOS
# ==========================================
class Trofeo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='trofeos')

    def __str__(self):
        try:
            return self.nombre.encode('utf-8', errors='ignore').decode('utf-8')
        except:
            return "Trofeo"

# ==========================================
# 🛒 MODELOS DE CARRITO (CONSERVADOS)
# ==========================================
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.user.username}"

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'jugador')

    @property
    def subtotal(self):
        return self.jugador.precio * self.quantity

    def __str__(self):
        return f"{self.jugador.nombre} x {self.quantity}"