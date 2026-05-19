from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Jugador

# Formulario corregido para que el registro (/registro/) no use auth.User interno
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

# Formulario para que editores ingresen jugadores individuales externamente con Bootstrap
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