from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)        # ← nullable
    documento = models.CharField(max_length=20, unique=True, blank=True, null=True)  # ← nullable
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.apellido or ''}, {self.nombre}".strip()

    class Meta:
        ordering = ['apellido', 'nombre']