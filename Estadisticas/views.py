from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Equipo, Partido, Jugador, Cart, CartItem
from .forms import JugadorForm

# =========================
# 🏠 Home con Búsqueda y Paginación
# =========================
def home(request):
    query = request.GET.get('q')
    equipos_list = Equipo.objects.all()

    if query:
        equipos_list = equipos_list.filter(
            Q(nombre__icontains=query) | 
            Q(ciudad__icontains=query)
        )

    paginator = Paginator(equipos_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    partidos = Partido.objects.all().order_by('-fecha')[:5]
    
    return render(request, 'Estadisticas/home.html', {
        'page_obj': page_obj, 
        'partidos': partidos,
        'query': query
    })

# =========================
# 🛒 Gestión del Carrito
# =========================
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'Estadisticas/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, equipo_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, equipo=equipo)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
        except (ValueError, TypeError):
            pass
    return redirect('cart_detail')

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

# =========================
# 🔐 Vistas de Auth
# =========================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'Estadisticas/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Estadisticas/register.html', {'form': form})