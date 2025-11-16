# ---------- productos/urls.py ----------
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('nuevo/', views.producto_create, name='producto_create'),
    path('stock-bajo/', views.stock_bajo_list, name='stock_bajo_list'),

    # nuevas (las que faltaban)
    path('<int:pk>/', views.producto_detail, name='producto_detail'),
    path('<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
]