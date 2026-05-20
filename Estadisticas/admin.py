# coding: utf-8
from django.contrib import admin
from django import forms
from decimal import Decimal
import re
from .models import User, Liga, Equipo, Jugador, Partido, EstadisticaPartido, Trofeo

# ==========================================
# CONFIGURACIÓN PARA EQUIPOS MASIVOS
# ==========================================
class EquipoAdminForm(forms.ModelForm):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    ciudad = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    equipos_masivos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 5}),
        required=False,
        label="Carga Masiva de Equipos"
    )
    class Meta:
        model = Equipo
        fields = '__all__'

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    form = EquipoAdminForm
    list_display = ['nombre', 'ciudad', 'liga']
    list_filter = ['liga']

    def save_model(self, request, obj, form, change):
        texto = form.cleaned_data.get('equipos_masivos')
        liga_sel = form.cleaned_data.get('liga')
        if texto:
            for linea in texto.strip().split('\n'):
                if not linea.strip(): continue
                partes = re.split(r',\s*|\t|\s{2,}', linea.strip())
                if len(partes) >= 2:
                    Equipo.objects.create(
                        nombre=partes[0].strip(),
                        ciudad=partes[1].strip(),
                        liga=liga_sel
                    )
            return
        if obj.nombre:
            super().save_model(request, obj, form, change)


# ==========================================
# CONFIGURACIÓN PARA JUGADORES MASIVOS
# ==========================================
class JugadorAdminForm(forms.ModelForm):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    posicion = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    jugadores_masivos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 5}),
        required=False,
        label="Carga Masiva de Jugadores",
        help_text="Pega las columnas de Excel: Nombre [Tab] Posición [Tab] Precio"
    )
    class Meta:
        model = Jugador
        fields = '__all__'

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    form = JugadorAdminForm
    list_display = ['nombre', 'posicion', 'equipo', 'precio']
    list_filter = ['equipo', 'posicion']

    def save_model(self, request, obj, form, change):
        texto_masivo = form.cleaned_data.get('jugadores_masivos')
        equipo_seleccionado = form.cleaned_data.get('equipo')

        if texto_masivo:
            for linea in texto_masivo.strip().split('\n'):
                if not linea.strip(): continue
                partes = re.split(r',\s*|\t|\s{2,}', linea.strip())
                if len(partes) >= 2:
                    nombre = partes[0].strip()
                    posicion = partes[1].strip()
                    precio = Decimal('0.00')
                    
                    # Si viene el precio en la tercera columna, lo procesamos
                    if len(partes) >= 3:
                        try:
                            precio_limpio = partes[2].replace('$', '').replace('.', '').replace(',', '.').strip()
                            precio = Decimal(precio_limpio)
                        except:
                            precio = Decimal('0.00')
                            
                    Jugador.objects.create(
                        nombre=nombre,
                        posicion=posicion,
                        equipo=equipo_seleccionado,
                        precio=precio
                    )
            return
            
        if obj.nombre:
            super().save_model(request, obj, form, change)


# ==========================================
# REGISTRO DE MODELOS SIMPLES
# ==========================================
@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais']

admin.site.register(User)
admin.site.register(Partido)
admin.site.register(EstadisticaPartido)
admin.site.register(Trofeo)