from django.contrib import admin
from .models import User, Liga, Equipo, Jugador, Partido, EstadisticaPartido, Trofeo

# Inline para ver jugadores dentro de un equipo
class JugadorInline(admin.TabularInline):
    model = Jugador
    extra = 1

# Inline para registrar estadísticas dentro de un partido (Estilo CartItem)
class EstadisticaPartidoInline(admin.TabularInline):
    model = EstadisticaPartido
    extra = 2 # Espacios vacíos para llenar rápido

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'liga', 'ciudad')
    list_filter = ('liga',)
    inlines = [JugadorInline]

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('equipo_local', 'equipo_visitante', 'fecha')
    inlines = [EstadisticaPartidoInline] # Aquí llenas los goles del partido

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equipo', 'posicion')
    search_fields = ('nombre',)

@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais')

@admin.register(Trofeo)
class TrofeoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'anio', 'equipo')
    list_filter = ('equipo',)

admin.site.register(User)