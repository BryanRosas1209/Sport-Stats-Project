from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Equipo, Partido, Jugador, Cart, CartItem, Liga
from .forms import JugadorForm

# =========================
# 🏠 Mercado de Fichajes (Home)
# =========================
def home(request):
    query = request.GET.get('q')
    liga_id = request.GET.get('liga')

    # Optimización: Cargar equipo y liga del jugador
    jugadores_list = Jugador.objects.select_related('equipo__liga').all()

    if query:
        jugadores_list = jugadores_list.filter(
            Q(nombre__icontains=query) | Q(posicion__icontains=query)
        )
    
    if liga_id:
        jugadores_list = jugadores_list.filter(equipo__liga__id=liga_id)

    paginator = Paginator(jugadores_list, 9) # 9 jugadores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    partidos = Partido.objects.all().order_by('-fecha')[:5]
    ligas = Liga.objects.all()
    
    return render(request, 'Estadisticas/home.html', {
        'page_obj': page_obj, 
        'partidos': partidos,
        'ligas': ligas,
        'query': query
    })

# =========================
# 🛒 Lógica de Fichajes
# =========================
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'Estadisticas/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, jugador_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    jugador = get_object_or_404(Jugador, id=jugador_id)
    
    item, created = CartItem.objects.get_or_create(cart=cart, jugador=jugador)
    if not created:
        item.quantity += 1
        item.save()
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
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()
    return redirect('cart_detail')

# =========================
# 📊 Panel y CRUD (Solo Editores)
# =========================
@login_required
def panel_editor(request):
    if not request.user.is_editor:
        return HttpResponseForbidden("Acceso denegado.")
    jugadores = Jugador.objects.all()
    return render(request, 'Estadisticas/panel.html', {'jugadores': jugadores})

@login_required
def jugador_crear(request):
    if not request.user.is_editor: return HttpResponseForbidden()
    form = JugadorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('panel_editor')
    return render(request, 'Estadisticas/jugador_form.html', {'form': form, 'titulo': 'Nuevo Fichaje'})

@login_required
def jugador_editar(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    if not request.user.is_editor: return HttpResponseForbidden()
    form = JugadorForm(request.POST or None, request.FILES or None, instance=jugador)
    if form.is_valid():
        form.save()
        return redirect('panel_editor')
    return render(request, 'Estadisticas/jugador_form.html', {'form': form, 'titulo': 'Editar Ficha'})

@login_required
def jugador_eliminar(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    if not request.user.is_editor: return HttpResponseForbidden()
    if request.method == 'POST':
        jugador.delete()
        return redirect('panel_editor')
    return render(request, 'Estadisticas/jugador_confirm_delete.html', {'jugador': jugador})

# =========================
# 🔐 Autenticación
# =========================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else: form = AuthenticationForm()
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
    else: form = UserCreationForm()
    return render(request, 'Estadisticas/register.html', {'form': form})