from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Autenticación
    path('registro/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard de Gestión
    path('panel/', views.panel_editor, name='panel_editor'),

    # CRUD de Jugadores
    path('jugadores/nuevo/', views.jugador_crear, name='jugador_crear'),
    path('jugadores/<uuid:pk>/editar/', views.jugador_editar, name='jugador_editar'),
    path('jugadores/<uuid:pk>/eliminar/', views.jugador_eliminar, name='jugador_eliminar'),
]