from django.contrib import admin
from django.urls import path, include # Importante agregar 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Estadisticas.urls')), # Conecta con las URLs de tu app
]

# Esto permite ver las fotos de escudos/jugadores en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)