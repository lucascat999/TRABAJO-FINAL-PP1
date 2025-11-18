from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stock-bajo/', views.stock_bajo_list, name='stock_bajo_list'),
    path('nuevo/', views.producto_create, name='producto_create'),
    path('categorias/', views.categoria_list, name='categoria_list'),

    # CRUD de productos
    path('', views.producto_list, name='producto_list'),  # listado en raíz
    path('<int:pk>/', views.producto_detail, name='producto_detail'),
    path('<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

    # CRUD de categorías
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
]