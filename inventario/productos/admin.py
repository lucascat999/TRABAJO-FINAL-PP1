from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'precio', 'stock', 'stock_minimo', 'necesita_reposicion']
    list_filter = ['categoria', 'stock_minimo', 'fecha_creacion']
    search_fields = ['sku', 'nombre', 'categoria__nombre']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']