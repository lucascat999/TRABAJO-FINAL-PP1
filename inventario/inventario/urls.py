"""
URL configuration for inventario project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('admin/', admin.site.urls),
    path("", include("productos.urls")),            # ← SÓLO ESTA (raíz)
    path("ventas/", include("ventas.urls")),
    path("clientes/", include("clientes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)