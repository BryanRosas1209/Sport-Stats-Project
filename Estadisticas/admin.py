# coding: utf-8
from django.contrib import admin
from django import forms
from django.db import models
from django.forms import ClearableFileInput
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal
from datetime import datetime
import re
from .models import User, Liga, Equipo, Jugador, Partido, EstadisticaPartido, Trofeo

# ==========================================
# CONFIGURACIÓN PARA EQUIPOS MASIVOS
# ==========================================
class EquipoAdminForm(forms.ModelForm):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    ciudad = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    # RESTAURADO: Volvemos a habilitar la subida de imágenes nativa de Django
    escudo = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'class': 'vFileField'}))

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
    
    # RESTAURADO: Subida de fotos original sin bloqueos binarios
    foto = forms.ImageField(required=False, widget=ClearableFileInput(attrs={'class': 'vFileField'}))
    
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
# CONFIGURACIÓN PARA PARTIDOS MASIVOS (Opción 1: Por Comas)
# ==========================================
class PartidoAdminForm(forms.ModelForm):
    # Forzamos a que en el FORMULARIO no sean requeridos para que Django no truene antes de procesar
    fecha = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'vTextField', 'placeholder': 'AAAA-MM-DD (Opcional si usas carga masiva)'})
    )
    equipo_local = forms.ModelChoiceField(queryset=Equipo.objects.all(), required=False)
    equipo_visitante = forms.ModelChoiceField(queryset=Equipo.objects.all(), required=False)
    goles_local = forms.IntegerField(required=False)
    goles_visitante = forms.IntegerField(required=False)
    
    partidos_masivos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 6}),
        required=False,
        label="💥 Carga Masiva de Partidos (Por Comas)",
        help_text="Estructura: Fecha, Equipo Local, Goles Local, Equipo Visitante, Goles Visitante.<br>Ejemplo:<br>2026-05-28, Real Madrid, 2, Barcelona, 1"
    )
    class Meta:
        model = Partido
        fields = '__all__'

    # Validación del formulario para asegurar que al menos uno de los dos métodos tenga datos
    def clean(self):
        cleaned_data = super().clean()
        texto_masivo = cleaned_data.get('partidos_masivos')
        
        # Si NO se usó la carga masiva, obligamos a que se hayan llenado los campos tradicionales
        if not texto_masivo:
            if not cleaned_data.get('fecha') or not cleaned_data.get('equipo_local') or not cleaned_data.get('equipo_visitante'):
                raise forms.ValidationError("Debes rellenar los datos del partido individual o usar el cuadro de Carga Masiva.")
        return cleaned_data


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    form = PartidoAdminForm
    list_display = ['fecha', 'equipo_local', 'goles_local', 'goles_visitante', 'equipo_visitante', 'liga']
    list_filter = ['liga', 'fecha']
    change_list_template = "admin/partido_changelist.html"

    def save_model(self, request, obj, form, change):
        texto_masivo = form.cleaned_data.get('partidos_masivos')
        liga_seleccionada = form.cleaned_data.get('liga')

        if texto_masivo:
            # Bandera temporal para evitar ejecuciones posteriores
            request._is_masivo = True
            
            lineas = texto_masivo.strip().split('\n')
            for linea in lineas:
                linea_limpia = linea.strip()
                if not linea_limpia: 
                    continue
                
                partes = [p.strip() for p in linea_limpia.split(',')]
                
                if len(partes) >= 5:
                    try:
                        fecha_str = partes[0]
                        local_nombre = partes[1]
                        g_local = int(partes[2])
                        visitante_nombre = partes[3]
                        g_visitante = int(partes[4])
                        
                        fecha_obj = None
                        for formato in ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"]:
                            try:
                                fecha_obj = datetime.strptime(fecha_str, formato)
                                break
                            except ValueError:
                                continue
                        
                        if not fecha_obj:
                            continue
                        
                        # Buscar equipos en la base de datos
                        eq_local = Equipo.objects.filter(nombre__iexact=local_nombre, liga=liga_seleccionada).first()
                        if not eq_local:
                            eq_local = Equipo.objects.filter(nombre__icontains=local_nombre, liga=liga_seleccionada).first()
                            
                        eq_visitante = Equipo.objects.filter(nombre__iexact=visitante_nombre, liga=liga_seleccionada).first()
                        if not eq_visitante:
                            eq_visitante = Equipo.objects.filter(nombre__icontains=visitante_nombre, liga=liga_seleccionada).first()
                        
                        if eq_local and eq_visitante:
                            Partido.objects.create(
                                fecha=fecha_obj,
                                equipo_local=eq_local,
                                equipo_visitante=eq_visitante,
                                goles_local=g_local,
                                goles_visitante=g_visitante,
                                liga=liga_seleccionada
                            )
                    except Exception:
                        continue
            
            # Construimos un objeto simulado válido temporal únicamente para cumplir con el flujo del Admin 
            # sin que altere nada real (ya que retornamos inmediatamente después)
            obj.fecha = datetime.now()
            obj.equipo_local = Equipo.objects.filter(liga=liga_seleccionada).first()
            obj.equipo_visitante = Equipo.objects.filter(liga=liga_seleccionada).first()
            return

        # Si es un guardado normal unitario, procesamos la fecha manual de texto a datetime real
        fecha_data = form.cleaned_data.get('fecha')
        if fecha_data and isinstance(fecha_data, str):
            for formato in ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"]:
                try:
                    obj.fecha = datetime.strptime(fecha_data.strip(), formato)
                    break
                except ValueError:
                    continue
                    
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Cancelamos por completo la verificación si se usó la carga masiva
        if getattr(request, '_is_masivo', False):
            return
        super().save_related(request, form, formsets, change)

    def response_add(self, request, obj, post_url_continue=None):
        # Redirigir limpiamente a la tabla general de partidos después de la carga masiva
        if getattr(request, '_is_masivo', False):
            return redirect('../')
        return super().response_add(request, obj, post_url_continue)

# ==========================================
# REGISTRO DE MODELOS SIMPLES
# ==========================================
@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais']

admin.site.register(User)
admin.site.register(EstadisticaPartido)
admin.site.register(Trofeo)