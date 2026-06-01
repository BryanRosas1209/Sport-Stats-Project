# coding: utf-8
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Función auxiliar para desinfectar strings binarios corruptos de Excel
def limpiar_string_corrupto(valor):
    if isinstance(valor, str):
        try:
            valor.encode('utf-8')
            return valor
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Filtra caracteres no legibles (como bytes 0x90) de manera transparente
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

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if name in ['nombre', 'ciudad']:
            return limpiar_string_corrupto(attr)
        return attr

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
        return limpiar_string_corrupto(self.nombre)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if name in ['nombre', 'posicion']:
            return limpiar_string_corrupto(attr)
        return attr

# ==========================================
# ⚽ MODELO DE PARTIDO
# ==========================================
class Partido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField()
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='partidos', null=True, blank=True)

    def __str__(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre} ({self.liga.nombre if self.liga else 'Sin Liga'})"
    
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
        return f"Stats - {self.jugador}"

# ==========================================
# 🏆 TROFEOS
# ==========================================
class Trofeo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='trofeos')

    def __str__(self):
        return limpiar_string_corrupto(self.nombre)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if name == 'nombre':
            return limpiar_string_corrupto(attr)
        return attr

# ==========================================
# 🛒 MODELOS DE CARRITO
# ==========================================
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Carrito - {self.user.username}"

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
        return f"{self.jugador} x {self.quantity}"
    
class EquipoUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='equipo_ideal')
    jugadores = models.ManyToManyField('Jugador', blank=True)

    def __str__(self):
        return f"Equipo Ideal de {self.usuario.username}"
    
