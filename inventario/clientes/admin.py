from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'documento', 'email', 'telefono')
    list_display_links = ('nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'documento', 'email')
    list_per_page = 20
    ordering = ('apellido', 'nombre')