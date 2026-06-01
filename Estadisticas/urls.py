# coding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Página Principal (Mercado de Fichajes / Panel General)
    path('', views.home, name='home'),

    #esperando a cargar
    path('api/equipos/<str:equipo_id>/jugadores/', views.api_jugadores_equipo, name='api_jugadores_equipo'),
    # Estadisticas/urls.py
    path('equipo/<uuid:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    # ⬇️ AGREGA ESTA NUEVA RUTA ⬇️
    path('agregar-ideal/<uuid:jugador_id>/', views.agregar_al_equipo_ideal, name='agregar_ideal'), 
    # Nota: Si tus IDs de jugador no usan UUID sino números, cambia <uuid:jugador_id> por <int:jugador_id>

    path('panel/rendimiento-masivo/', views.rendimiento_carga_masiva, name='rendimiento_carga_masiva'),

    path('panel/importar-rendimiento/', views.rendimiento_carga_masiva, name='rendimiento_carga_masiva'),

    path('eliminar-ideal/<uuid:jugador_id>/', views.eliminar_del_equipo_ideal, name='eliminar_ideal'),

    # ⚽ NUEVO: Explorador de Equipos Independiente (Rutas Limpias)
    path('equipos/', views.ver_equipos, name='ver_equipos'),
    path('equipos/<uuid:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),

    # 🛒 Carrito de Fichajes
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/agregar/<uuid:jugador_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/eliminar/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrito/actualizar/<uuid:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('carrito/finalizar/', views.checkout_cart, name='checkout_cart'),

    # 📊 Panel de Administración para Editores
    path('panel/', views.panel_editor, name='panel_editor'),
    
    # 🏃 CRUD de Jugadores
    path('jugador/crear/', views.jugador_crear, name='jugador_crear'),
    path('jugador/editar/<uuid:pk>/', views.jugador_editar, name='jugador_editar'),
    path('jugador/eliminar/<uuid:pk>/', views.jugador_eliminar, name='jugador_eliminar'),
    path('jugador/cargar-fotos/', views.cargar_fotos_masivo, name='cargar_fotos_masivo'),

    # 🛡️ CRUD de Equipos
    path('equipo/crear/', views.equipo_crear, name='equipo_crear'),

    # 🔐 Sistema de Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.register, name='register'),
]