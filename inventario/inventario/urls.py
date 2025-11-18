
"""
URL configuration for inventario project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # 🔧 ahora las rutas de productos están en raíz
    path('', include('productos.urls')),

    path('ventas/', include('ventas.urls')),
    path('clientes/', include('clientes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
