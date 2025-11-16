# ---------- productos/urls.py ----------
from django.urls import path
from . import views

app_name = 'productos'   # namespace que usa la plantilla

urlpatterns = [
    # ya tendrás más paths aquí; agregá el último
    path('', views.producto_list, name='producto_list'),
    path('nuevo/', views.producto_create, name='producto_create'),
    path('stock-bajo/', views.stock_bajo_list, name='stock_bajo_list'),  # <-- nuevo
]