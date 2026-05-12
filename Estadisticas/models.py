import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# 👤 Usuario Personalizado
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

# 🏆 Liga
class Liga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Ligas"

    def __str__(self):
        return self.nombre

# 🛡️ Equipo (Incluye Escudo y Precio)
class Equipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    liga = models.ForeignKey(Liga, on_delete=models.SET_NULL, null=True, related_name='equipos')
    escudo = models.ImageField(upload_to='escudos/', null=True, blank=True)
    # --- NUEVO CAMPO PARA EL CARRITO ---
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def __str__(self):
        return self.nombre

# 🏃 Jugador
class Jugador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    posicion = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

    def __str__(self):
        return self.nombre

# 📅 Partido
class Partido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField()
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)
    torneo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.equipo_local} {self.goles_local} - {self.goles_visitante} {self.equipo_visitante}"

# 📊 Estadísticas
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

# 🥇 Trofeo
class Trofeo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='trofeos')

    def __str__(self):
        return f"{self.nombre} ({self.anio})"

# ==========================================
# 🛒 NUEVOS MODELOS PARA EL CARRITO
# ==========================================

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'equipo')

    @property
    def subtotal(self):
        return self.equipo.precio * self.quantity

    def __str__(self):
        return f"{self.equipo.nombre} x {self.quantity}"