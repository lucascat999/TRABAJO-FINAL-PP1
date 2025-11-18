# ventas/models.py
from django.db import models
from django.db.models import Max
from productos.models import Producto
from clientes.models import Cliente


class Venta(models.Model):
    codigo = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    anulada = models.BooleanField(default=False)

    def __str__(self):
        return f"Venta {self.codigo} - {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.codigo:                       # primera vez
            last = Venta.objects.aggregate(max=Max('id'))['max'] or 0
            self.codigo = f'V{last + 1:05d}'      # V00001, V00002, ...
        super().save(*args, **kwargs)


class ItemVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)