from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'documento', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'documento')
    list_filter = ('apellido',)
    ordering = ('apellido', 'nombre')