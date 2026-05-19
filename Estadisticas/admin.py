from django.contrib import admin
from .models import User, Liga, Equipo, Jugador, Partido, EstadisticaPartido, Trofeo

# Registrar modelos secundarios estándar
admin.site.register(User)
admin.site.register(Liga)
admin.site.register(Partido)
admin.site.register(EstadisticaPartido)
admin.site.register(Trofeo)

# 🚀 REGISTRO MASIVO DE JUGADORES DENTRO DEL FORMULARIO DEL EQUIPO
class JugadorInline(admin.TabularInline):
    model = Jugador
    extra = 5  # Cantidad de filas vacías listas para rellenar de golpe
    fields = ['nombre', 'posicion', 'precio', 'foto']

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'liga']
    inlines = [JugadorInline] # Inserta la cuadrícula masiva

# Registro individual clásico (para búsquedas rápidas)
@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'posicion', 'equipo', 'precio']
    list_filter = ['equipo', 'posicion']
    search_fields = ['nombre']