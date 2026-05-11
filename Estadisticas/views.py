from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Equipo, Partido, Jugador
from .forms import JugadorForm

def home(request):
    equipos = Equipo.objects.all()
    partidos = Partido.objects.all().order_by('-fecha')[:5]
    return render(request, 'Estadisticas/home.html', {'equipos': equipos, 'partidos': partidos})

# =========================
# 📊 Panel de Control
# =========================
@login_required
def panel_editor(request):
    if not request.user.is_editor:
        return HttpResponseForbidden("No tienes permisos de editor.")
    
    jugadores = Jugador.objects.all()
    return render(request, 'Estadisticas/panel.html', {'jugadores': jugadores})

# =========================
# 🏃 CRUD Jugadores
# =========================
@login_required
def jugador_crear(request):
    if not request.user.is_editor:
        return HttpResponseForbidden()
    
    form = JugadorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('panel_editor')
    
    return render(request, 'Estadisticas/jugador_form.html', {'form': form, 'titulo': 'Inscribir Jugador'})

@login_required
def jugador_editar(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    if not request.user.is_editor:
        return HttpResponseForbidden()
    
    form = JugadorForm(request.POST or None, instance=jugador)
    if form.is_valid():
        form.save()
        return redirect('panel_editor')
    
    return render(request, 'Estadisticas/jugador_form.html', {'form': form, 'titulo': 'Editar Jugador'})

@login_required
def jugador_eliminar(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    if not request.user.is_editor:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        jugador.delete()
        return redirect('panel_editor')
    
    return render(request, 'Estadisticas/jugador_confirm_delete.html', {'jugador': jugador})

# Vistas de Auth (Mantenlas o actualízalas si las tenías vacías)
def login_view(request):
    # ... tu lógica de login actual ...
    return render(request, 'Estadisticas/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    # ... tu lógica de registro actual ...
    return render(request, 'Estadisticas/register.html')