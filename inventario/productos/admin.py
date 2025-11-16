from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'precio', 'stock', 'stock_minimo', 'necesita_reposicion']
    search_fields = ['sku', 'nombre']
    list_filter = ['stock_minimo', 'fecha_creacion']
    ordering = ['sku']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']