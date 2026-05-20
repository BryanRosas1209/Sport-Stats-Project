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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'posicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Delantero'}),
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 120000000.00', 'step': '0.01'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

# 📋 JUGADORES (MASIVO)
class ImportarPlantillaForm(forms.Form):
    equipo = forms.ModelChoiceField(
        queryset=Equipo.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Equipo al que pertenecen"
    )
    datos_pegados = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 6, 
            'placeholder': 'Kylian Mbappé, Delantero, 180000000\nLuka Modric, Mediocampista, 15000000'
        }),
        label="Pega aquí los jugadores (Uno por línea)",
        help_text="Formato: Nombre, Posición, Precio (Separados por comas)"
    )

# 🛡️ EQUIPOS (INDIVIDUAL)
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'ciudad', 'liga', 'escudo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Club'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Madrid'}),
            'liga': forms.Select(attrs={'class': 'form-select'}),
            'escudo': forms.FileInput(attrs={'class': 'form-control'}),
        }

# 🛡️ EQUIPOS (MASIVO)
class ImportarEquiposForm(forms.Form):
    liga = forms.ModelChoiceField(
        queryset=Liga.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Liga a la que pertenecen"
    )
    equipos_pegados = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Real Madrid, Madrid\nFC Barcelona, Barcelona\nAtletico de Madrid, Madrid'
        }),
        label="Pega aquí los equipos (Uno por línea)",
        help_text="Formato: Nombre del Equipo, Ciudad (Separados por comas)"
    )