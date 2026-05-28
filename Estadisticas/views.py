from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q, Sum  # Se agrega Sum para calcular estadísticas acumuladas
from decimal import Decimal
from datetime import datetime
import uuid
from .models import Jugador, EquipoUsuario

from .models import Equipo, Partido, Cart, CartItem, Liga
from .forms import (
    JugadorForm, CustomUserCreationForm, ImportarPlantillaForm, 
    EquipoForm, ImportarEquiposForm, ImportarPartidosForm
)

# ==============================================================================
# 🏠 Menú de Bienvenida & Enrutador de Estadísticas Avanzadas
# ==============================================================================
def home(request):
    # 1. Capturar parámetros de la URL
    seccion = request.GET.get('ver', '') 
    query = request.GET.get('q', '')
    liga_id = request.GET.get('liga', '')
    equipo_id = request.GET.get('equipo', '').strip() # Limpiamos espacios

    # 2. FORZAR SECCIÓN: Si hay un ID de equipo en la URL, obligamos a que la sección sea de equipos
    if equipo_id:
        seccion = 'detalle_equipo'
        # Esto reescribe temporalmente la sección para el HTML si 'ver' venía vacío o mal escrito

    # 3. Cargar datos base para pintar la interfaz
    ligas = Liga.objects.all()
    equipos = Equipo.objects.all()
    jugadores_list = Jugador.objects.all()

    # Separar equipos por liga
    equipos_premier = Equipo.objects.filter(liga__nombre__icontains='premier')
    equipos_laliga = Equipo.objects.filter(liga__nombre__icontains='liga')

    # 4. Lógica del Equipo Seleccionado (Extremadamente tolerante)
    equipo_seleccionado = None
    jugadores_equipo_seleccionado = []
    
    if equipo_id:
        # Intentar buscarlo primero como objeto UUID puro
        try:
            uuid_obj = uuid.UUID(equipo_id)
            equipo_seleccionado = Equipo.objects.filter(id=uuid_obj).first()
        except ValueError:
            # Si falla, intentar buscarlo como texto directo (depende de la base de datos)
            equipo_seleccionado = Equipo.objects.filter(id=equipo_id).first()
        
        # Si encontramos el equipo, traemos sus jugadores
        if equipo_seleccionado:
            jugadores_equipo_seleccionado = Jugador.objects.filter(equipo=equipo_seleccionado)
        else:
            # SI NO LO ENCUENTRA: Creamos un objeto ficticio para que el HTML no se rompa y muestre algo
            class EquipoFicticio:
                id = equipo_id
                nombre = "Equipo (ID No encontrado en BD)"
            equipo_seleccionado = EquipoFicticio()

   # # 5. LÓGICA DE ESTADÍSTICAS DE LA LIGA (CORREGIDA SIN ERROR DE 'PUNTOS')
    liga_seleccionada = None
    tabla_posiciones = []
    goleadores = []
    asistidores = []
    partidos_equipo = []

    if liga_id:
        # Intentamos buscar la liga seleccionada controlando formatos UUID
        try:
            try:
                uuid_liga = uuid.UUID(liga_id)
                liga_seleccionada = Liga.objects.filter(id=uuid_liga).first()
            except ValueError:
                liga_seleccionada = Liga.objects.filter(id=liga_id).first()
        except Exception:
            liga_seleccionada = Liga.objects.filter(id=liga_id).first()

        if liga_seleccionada:
            # CORRECCIÓN: Filtrar por liga y ordenar por 'nombre' ya que tu base de datos no tiene la columna 'puntos'
            tabla_posiciones = Equipo.objects.filter(liga=liga_seleccionada).order_by('nombre')
            
            # CORRECCIÓN: Calcular la suma de goles acumulados usando la relación rendimiento_partidos
            goleadores = Jugador.objects.filter(equipo__liga=liga_seleccionada).annotate(
                total_goles=Sum('rendimiento_partidos__goles')
            ).filter(total_goles__gt=0).order_by('-total_goles')[:10]
            
            # CORRECCIÓN: Calcular la suma de asistencias acumuladas usando la relación rendimiento_partidos
            asistidores = Jugador.objects.filter(equipo__liga=liga_seleccionada).annotate(
                total_asistencias=Sum('rendimiento_partidos__asistencias')
            ).filter(total_asistencias__gt=0).order_by('-total_asistencias')[:10]
            
            # CORRECCIÓN: Forzar el nombre exacto de la sección que espera tu HTML
            seccion = 'liga_detalle'

    # ==========================================================
    # 🎮 LÓGICA CORREGIDA: JUEGO "EQUIPO IDEAL" (LEYENDO DE EQUIPOUSUARIO)
    # ==========================================================
    presupuesto_total = 1100000000  # $1,100,000,000
    valor_equipo = 0
    jugadores_fichados = []

    if request.user.is_authenticated:
        try:
            # LEEMOS DIRECTAMENTE DESDE EL NUEVO MODELO DE EQUIPOUSUARIO
            from .models import EquipoUsuario
            equipo_usuario = EquipoUsuario.objects.filter(usuario=request.user).first()
            
            if equipo_usuario:
                # Traemos todos los jugadores guardados de forma fija para este usuario
                jugadores_fichados = equipo_usuario.jugadores.all()
        except Exception as e:
            jugadores_fichados = []

        # Calculamos la inversión total sumando el valor de cada jugador fichado fijo
        for jugador in jugadores_fichados:
            if jugador.precio:  
                valor_equipo += jugador.precio
    
    # Restamos los costos totales de la plantilla al presupuesto de 1,100 millones
    presupuesto_restante = presupuesto_total - valor_equipo

    # 6. Enviar datos exactos a la plantilla (Incluyendo las nuevas variables)
    return render(request, 'Estadisticas/home.html', {
        'page_obj': jugadores_list, 
        'ligas': ligas,
        'equipos': equipos,
        'query': query,
        'seccion': seccion,  # Enviamos la sección corregida o forzada
        'liga_seleccionada': liga_seleccionada,
        'tabla_posiciones': tabla_posiciones,
        'goleadores': goleadores,
        'asistidores': asistidores,
        'equipo_seleccionado': equipo_seleccionado,
        'partidos_equipo': partidos_equipo,
        'equipos_premier': equipos_premier,
        'equipos_laliga': equipos_laliga,
        'jugadores_equipo_seleccionado': jugadores_equipo_seleccionado,
        
        # NUEVAS VARIABLES INYECTADAS PARA "EQUIPO IDEAL":
        'jugadores_fichados': jugadores_fichados,
        'valor_equipo': valor_equipo,
        'presupuesto_restante': presupuesto_restante,
        'presupuesto_total': presupuesto_total,
    })

@login_required
def agregar_al_equipo_ideal(request, jugador_id):
    # 1. Buscamos al jugador que se quiere fichar
    jugador = get_object_or_404(Jugador, id=jugador_id)
    
    # 2. Obtenemos el Equipo Ideal del usuario o lo creamos si no tiene uno todavía
    equipo_usuario, created = EquipoUsuario.objects.get_or_create(usuario=request.user)
    
    # 3. Agregamos el jugador a la lista del usuario (ManyToManyField evita duplicados automáticamente)
    equipo_usuario.jugadores.add(jugador)
    
    # 4. Redirigimos al usuario de vuelta a la pantalla del juego
    return redirect('/?ver=mi_dream_team')

@login_required
def eliminar_del_equipo_ideal(request, jugador_id):
    # 1. Buscamos al jugador que se quiere eliminar
    jugador = get_object_or_404(Jugador, id=jugador_id)
    
    # 2. Obtenemos el Equipo Ideal del usuario
    equipo_usuario = EquipoUsuario.objects.filter(usuario=request.user).first()
    
    # 3. Si el equipo existe, removemos al jugador de la lista
    if equipo_usuario:
        equipo_usuario.jugadores.remove(jugador)
        
    # 4. Redirigimos de vuelta a la pantalla del juego
    return redirect('/?ver=mi_dream_team')

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

@login_required
def checkout_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        cart.items.all().delete()
        return redirect('home')
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
                partes = linea.split(',') if ',' in linea else linea.split('\t')
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
                partes = linea.split(',') if ',' in linea else linea.split('\t')
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

@login_required
def partido_carga_masiva(request):
    if not request.user.is_editor: 
        return HttpResponseForbidden("Acceso denegado. Solo editores.")
    
    form_masivo = ImportarPartidosForm(request.POST or None)
    mensaje_error = None
    partidos_creados = 0
    
    if request.method == 'POST' and form_masivo.is_valid():
        liga_sel = form_masivo.cleaned_data['liga']
        lineas = form_masivo.cleaned_data['partidos_pegados'].strip().split('\n')
        
        for num_linea, linea in enumerate(lineas, 1):
            linea_limpia = linea.strip()
            if not linea_limpia: 
                continue 
            
            partes = linea_limpia.split(',')
            partes = [p.strip() for p in partes]
            
            if len(partes) >= 5:
                try:
                    fecha_str = partes[0]
                    local_nombre = partes[1]
                    g_local = int(partes[2])
                    visitante_nombre = partes[3]
                    g_visitante = int(partes[4])
                    
                    fecha_obj = None
                    formatos_fecha = ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"]
                    
                    for formato in formatos_fecha:
                        try:
                            fecha_obj = datetime.strptime(fecha_str, formato)
                            break
                        except ValueError:
                            continue
                    
                    if not fecha_obj:
                        mensaje_error = f"Error en línea {num_linea}: El formato de la fecha '{fecha_str}' no es correcto."
                        break
                    
                    eq_local = Equipo.objects.filter(nombre__iexact=local_nombre, liga=liga_sel).first()
                    if not eq_local:
                        eq_local = Equipo.objects.filter(nombre__icontains=local_nombre, liga=liga_sel).first()
                        
                    eq_visitante = Equipo.objects.filter(nombre__iexact=visitante_nombre, liga=liga_sel).first()
                    if not eq_visitante:
                        eq_visitante = Equipo.objects.filter(nombre__icontains=visitante_nombre, liga=liga_sel).first()
                    
                    if eq_local and eq_visitante:
                        Partido.objects.create(
                            fecha=fecha_obj,
                            equipo_local=eq_local,
                            equipo_visitante=eq_visitante,
                            goles_local=g_local,
                            goles_visitante=g_visitante,
                            liga=liga_sel
                        )
                        partidos_creados += 1
                    else:
                        faltante = local_nombre if not eq_local else visitante_nombre
                        mensaje_error = f"Error en línea {num_linea}: El equipo '{faltante}' no se encuentra registrado."
                        break
                        
                except ValueError:
                    mensaje_error = f"Error en línea {num_linea}: Los goles deben ser números enteros."
                    break
                except Exception as e:
                    mensaje_error = f"Error inesperado en línea {num_linea}: {str(e)}"
                    break
            else:
                mensaje_error = f"Error en línea {num_linea}: Faltan datos."
                break
                    
        if not mensaje_error and partidos_creados > 0:
            return redirect('panel_editor')

    return render(request, 'Estadisticas/partido_masivo_form.html', {
        'form_masivo': form_masivo,
        'mensaje_error': mensaje_error,
        'titulo': 'Importar Calendario Masivo (Por comas)'
    })

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

# ==============================================================================
# ⚽ Listado de Equipos en 2 Columnas y Detalle de Plantilla (Jugadores)
# ==============================================================================
def ver_equipos(request):
    liga_premier = Liga.objects.filter(nombre__icontains='premier').first()
    liga_espana = Liga.objects.filter(nombre__icontains='liga').first()

    equipos_premier = Equipo.objects.filter(liga=liga_premier) if liga_premier else []
    equipos_laliga = Equipo.objects.filter(liga=liga_espana) if liga_espana else []

    context = {
        'equipos_premier': equipos_premier,
        'equipos_laliga': equipos_laliga,
        'equipo_seleccionado': None,
        'jugadores_equipo_seleccionado': []
    }
    return render(request, 'Estadisticas/ver_equipos.html', context)


def detalle_equipo(request, equipo_id):
    # 1. Buscamos el equipo por su ID (UUID)
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    # 2. Filtramos los jugadores que pertenecen a este equipo
    jugadores = Jugador.objects.filter(equipo=equipo)
    
    # 3. Mandamos a la plantilla independiente
    return render(request, 'Estadisticas/detalle_equipo.html', {
        'equipo': equipo,
        'jugadores': jugadores
    })

# ==============================================================================
# ⚡ ENDPOINT ASÍNCRONO PARA CARGAR JUGADORES (SIN RECARGAR PÁGINA)
# ==============================================================================
def api_jugadores_equipo(request, equipo_id):
    # Buscamos el equipo sin importar si su ID es numérico o un UUID string
    equipo = get_object_or_404(Equipo, id=equipo_id)
    jugadores = Jugador.objects.filter(equipo=equipo)
    
    # Renderizamos únicamente un fragmento de HTML (la tabla suelta)
    return render(request, 'Estadisticas/partials/tabla_jugadores.html', {
        'equipo_seleccionado': equipo,
        'jugadores_equipo_seleccionado': jugadores
    })