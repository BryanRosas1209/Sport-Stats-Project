from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Jugador, Equipo, Liga

# 👤 USUARIOS
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

# 🏃 JUGADORES (INDIVIDUAL)
class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'posicion', 'equipo', 'precio', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-txt', 'placeholder': 'Nombre completo'}),
            'posicion': forms.TextInput(attrs={'class': 'input-txt', 'placeholder': 'Ej: Delantero'}),
            'equipo': forms.Select(attrs={'class': 'select-box'}),
            'precio': forms.NumberInput(attrs={'class': 'input-txt', 'placeholder': 'Ej: 120000000.00', 'step': '0.01'}),
            'foto': forms.FileInput(attrs={'class': 'input-txt'}),
        }

# 📋 JUGADORES (MASIVO)
class ImportarPlantillaForm(forms.Form):
    equipo = forms.ModelChoiceField(
        queryset=Equipo.objects.all(), 
        widget=forms.Select(attrs={'class': 'select-box'}),
        label="Equipo al que pertenecen"
    )
    datos_pegados = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6, 
            'placeholder': 'Kylian Mbappé, Delantero, 180000000\nLuka Modric, Mediocampista, 15000000',
            'style': 'width:100%; background-color:#1f2833; color:#fff; border:1px solid #2f3b4c; padding:12px; border-radius:4px; font-family:monospace; box-sizing: border-box;'
        }),
        label="Pega aquí los jugadores (Uno por línea)",
        help_text="Formato: Nombre, Posición, Precio (Separados por comas o tabulaciones de Excel)"
    )

# 🛡️ EQUIPOS (INDIVIDUAL)
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'ciudad', 'liga', 'escudo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-txt', 'placeholder': 'Nombre del Club'}),
            'ciudad': forms.TextInput(attrs={'class': 'input-txt', 'placeholder': 'Ej: Madrid'}),
            'liga': forms.Select(attrs={'class': 'select-box'}),
            'escudo': forms.FileInput(attrs={'class': 'input-txt'}),
        }

# 🛡️ EQUIPOS (MASIVO)
class ImportarEquiposForm(forms.Form):
    liga = forms.ModelChoiceField(
        queryset=Liga.objects.all(),
        widget=forms.Select(attrs={'class': 'select-box'}),
        label="Liga a la que pertenecen"
    )
    equipos_pegados = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Real Madrid, Madrid\nFC Barcelona, Barcelona\nAtletico de Madrid, Madrid',
            'style': 'width:100%; background-color:#1f2833; color:#fff; border:1px solid #2f3b4c; padding:12px; border-radius:4px; font-family:monospace; box-sizing: border-box;'
        }),
        label="Pega aquí los equipos (Uno por línea)",
        help_text="Formato: Nombre del Equipo, Ciudad (Separados por comas)"
    )

# 📅 PARTIDOS (MASIVO)
class ImportarPartidosForm(forms.Form):
    liga = forms.ModelChoiceField(
        queryset=Liga.objects.all(), 
        label="Seleccionar Liga para estos partidos",
        widget=forms.Select(attrs={'class': 'select-box'})
    )
    partidos_pegados = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10, 
            'placeholder': "Formato: Fecha (AAAA-MM-DD), Equipo Local, Goles Local, Equipo Visitante, Goles Visitante\nEjemplo:\n2026-05-28, Real Madrid, 2, Barcelona, 1\n2026-05-29, Manchester City, 3, Liverpool, 3",
            'style': 'width:100%; background-color:#1f2833; color:#fff; border:1px solid #2f3b4c; padding:12px; border-radius:4px; font-family:monospace; box-sizing: border-box;'
        }),
        label="Datos de los partidos (puedes pegar filas desde Excel o usar comas)"
    )