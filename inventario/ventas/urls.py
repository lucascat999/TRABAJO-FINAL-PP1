from django.urls import path
from . import views

urlpatterns = [
    path('', views.VentaListView.as_view(), name='venta_list'),
    path('nueva/', views.venta_create, name='venta_create'),
    path('<int:pk>/', views.VentaDetailView.as_view(), name='venta_detail'),
    path('<int:pk>/editar/', views.venta_update, name='venta_update'),
    path('<int:pk>/anular/', views.venta_anular, name='venta_anular'),
        path('<int:pk>/imprimir/', views.VentaPrintView.as_view(), name='venta_print'),
]