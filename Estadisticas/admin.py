# coding: utf-8
from django.contrib import admin
from django import forms
from decimal import Decimal
import re
from .models import User, Liga, Equipo, Jugador, Partido, EstadisticaPartido, Trofeo

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

@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais']

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

admin.site.register(User)
admin.site.register(Jugador)
admin.site.register(Partido)
admin.site.register(EstadisticaPartido)
admin.site.register(Trofeo)