from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from decimal import Decimal
import uuid

from .models import Equipo, Partido, Jugador, Cart, CartItem, Liga
from .forms import JugadorForm, CustomUserCreationForm, ImportarPlantillaForm, EquipoForm, ImportarEquiposForm

# ==============================================================================
# 🏠 Mercado de Fichajes (Home) - Con Desinfectador Automático de Base de Datos
# ==============================================================================
def home(request):
    # 🛡️ LIMPIADOR ULTRA-DEFENSIVO AUTOMÁTICO
    # Revisa todos los equipos y si sus nombres tienen caracteres binarios corruptos, los repara.
    try:
        for equipo in Equipo.objects.all():
            try:
                # Intentamos codificar y decodificar el nombre y la ciudad.
                # Si contiene bytes binarios puros (como el 0x90), saltará al except.
                equipo.nombre.encode('utf-8')
                equipo.ciudad.encode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                # Si saltó el error, desinfectamos el registro de inmediato
                equipo.nombre = f"Equipo Recuperado ({str(equipo.id)[:4]})"
                equipo.ciudad = "Ciudad Limpia"
                equipo.escudo = None
                equipo.save()
    except Exception:
        pass

    # 📊 LÓGICA DE LA INTERFAZ HOME (Muestra todos los jugadores juntos)
    query = request.GET.get('q')
    liga_id = request.GET.get('liga')

    jugadores_list = Jugador.objects.select_related('equipo__liga').all()

    if query:
        jugadores_list = jugadores_list.filter(
            Q(nombre__icontains=query) | 
            Q(posicion__icontains=query) |
            Q(equipo__nombre__icontains=query)
        )
    
    if liga_id:
        jugadores_list = jugadores_list.filter(equipo__liga__id=liga_id)

    partidos = Partido.objects.all().order_by('-fecha')[:5]
    ligas = Liga.objects.all()
    
    return render(request, 'Estadisticas/home.html', {
        'page_obj': jugadores_list, 
        'partidos': partidos,
        'ligas': ligas,
        'query': query
    })

# ==============================================================================
# 🛒 Lógica de Fichajes
# ==============================================================================
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

# ==============================================================================
# 📊 Panel y CRUD (Solo Editores)
# ==============================================================================
@login_required
def panel_editor(request):
    if not request.user.is_editor:
        return HttpResponseForbidden("Acceso denegado.")
    jugadores = Jugador.objects.all()
    return render(request, 'Estadisticas/panel.html', {'jugadores': jugadores})

# 🏃 VISTA UNIFICADA: JUGADORES (INDIVIDUAL O MASIVO)
@login_required
def jugador_crear(request):
    if not request.user.is_editor: return HttpResponseForbidden()
    
    form_individual = JugadorForm(request.POST or None, request.FILES or None)
    form_masivo = ImportarPlantillaForm(request.POST or None)
    
    if request.method == 'POST':
        if 'btn_individual' in request.POST and form_individual.is_valid():
            form_individual.save()
            return redirect('panel_editor')
            
        elif 'btn_masivo' in request.POST and form_masivo.is_valid():
            equipo_sel = form_masivo.cleaned_data['equipo']
            lineas = form_masivo.cleaned_data['datos_pegados'].strip().split('\n')
            for linea in lineas:
                if not linea.strip(): continue
                partes = linea.split('\t')
                if len(partes) >= 3:
                    try: precio = Decimal(partes[2].strip())
                    except: precio = Decimal('0.00')
                    
                    Jugador.objects.create(
                        nombre=partes[0].strip(),
                        posicion=partes[1].strip(),
                        equipo=equipo_sel,
                        precio=precio
                    )
            return redirect('cargar_fotos_masivo')

    return render(request, 'Estadisticas/jugador_form.html', {
        'form_individual': form_individual,
        'form_masivo': form_masivo,
        'titulo': 'Registrar Fichajes'
    })

@login_required
def jugador_editar(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    if not request.user.is_editor: return HttpResponseForbidden()
    form = JugadorForm(request.POST or None, request.FILES or None, instance=jugador)
    if form.is_valid():
        form.save()
        return redirect('panel_editor')
    return render(request, 'Estadisticas/jugador_form.html', {'form_individual': form, 'form_masivo': None, 'titulo': 'Editar Ficha'})

@login_required
def jugador_eliminar(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    if not request.user.is_editor: return HttpResponseForbidden()
    if request.method == 'POST':
        jugador.delete()
        return redirect('panel_editor')
    return render(request, 'Estadisticas/jugador_confirm_delete.html', {'jugador': jugador})

# 🛡️ VISTA UNIFICADA: EQUIPOS (INDIVIDUAL O MASIVO)
@login_required
def equipo_crear(request):
    if not request.user.is_editor: return HttpResponseForbidden()
    
    form_individual = EquipoForm(request.POST or None, request.FILES or None)
    form_masivo = ImportarEquiposForm(request.POST or None)
    
    if request.method == 'POST':
        if 'btn_individual' in request.POST and form_individual.is_valid():
            form_individual.save()
            return redirect('panel_editor')
            
        elif 'btn_masivo' in request.POST and form_masivo.is_valid():
            liga_sel = form_masivo.cleaned_data['liga']
            lineas = form_masivo.cleaned_data['equipos_pegados'].strip().split('\n')
            for linea in lineas:
                if not linea.strip(): continue
                partes = linea.split(',')
                if len(partes) >= 2:
                    Equipo.objects.create(
                        nombre=partes[0].strip(),
                        ciudad=partes[1].strip(),
                        liga=liga_sel
                    )
            return redirect('panel_editor')

    return render(request, 'Estadisticas/equipo_form.html', {
        'form_individual': form_individual,
        'form_masivo': form_masivo,
        'titulo': 'Registrar Equipos'
    })

# 📸 CARGA DE FOTOS AUTOMÁTICA POST-PEGADO
@login_required
def cargar_fotos_masivo(request):
    if not request.user.is_editor: return HttpResponseForbidden()
    jugadores_sin_foto = Jugador.objects.filter(foto='')
    
    if request.method == 'POST':
        for jugador in jugadores_sin_foto:
            campo_foto_id = f"foto_{jugador.id}"
            if campo_foto_id in request.FILES:
                jugador.foto = request.FILES[campo_foto_id]
                jugador.save()
        return redirect('panel_editor')
        
    return render(request, 'Estadisticas/cargar_fotos_masivo.html', {'jugadores': jugadores_sin_foto})

# ==============================================================================
# 🔐 Autenticación
# ==============================================================================
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else: 
        form = CustomUserCreationForm()
    return render(request, 'Estadisticas/register.html', {'form': form})