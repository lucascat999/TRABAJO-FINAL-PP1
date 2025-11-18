from django.contrib import admin
from django.utils.html import format_html
from .models import Venta, ItemVenta

# ── Item en línea (para edición dentro de Venta) ──
class ItemVentaInline(admin.TabularInline):
    model = ItemVenta
    extra = 0
    fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')
    readonly_fields = ('subtotal',)
    can_delete = True

# ── Admin de Venta ──
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'cliente',
        'fecha',
        'total',
        'anulada',
        'acciones_rapidas',
    )
    list_filter = ('anulada', 'fecha', 'cliente')
    search_fields = ('codigo', 'cliente__nombre', 'cliente__apellido', 'cliente__documento')
    ordering = ('-fecha',)
    readonly_fields = ('codigo', 'fecha', 'total')
    inlines = [ItemVentaInline]

    def acciones_rapidas(self, obj):
        if obj.anulada:
            return format_html('<span style="color:grey;">Anulada</span>')
        return format_html(
            '<a class="button" href="{}">Anular</a>',
            f'/admin/ventas/venta/{obj.pk}/anular/'
        )
    acciones_rapidas.short_description = 'Acciones'
    acciones_rapidas.allow_tags = True

    # ── Acción masiva: anular ventas seleccionadas ──
    @admin.action(description='Anular ventas seleccionadas')
    def anular_ventas(self, request, queryset):
        for venta in queryset:
            if not venta.anulada:
                venta.anulada = True
                venta.save()
                # devolver stock
                for item in venta.items.all():
                    prod = item.producto
                    prod.stock += item.cantidad
                    prod.save()
        self.message_user(request, f'Se anularon {queryset.count()} ventas y se restauró el stock.')

    actions = [anular_ventas]


# ── Admin de ItemVenta (opcional) ──
@admin.register(ItemVenta)
class ItemVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('venta__fecha', 'producto')
    search_fields = ('venta__codigo', 'producto__nombre')
    readonly_fields = ('subtotal',)