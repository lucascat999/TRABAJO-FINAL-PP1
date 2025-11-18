from django.db import models
import os
import uuid
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils import timezone
from django.db.models import F

def validate_image_size(image):
    filesize = image.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"El tamaño máximo permitido es de {megabyte_limit} MB")

def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("productos", filename)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=20, unique=True, verbose_name="SKU")
    nombre = models.CharField("Nombre", max_length=50)
    descripcion = models.CharField("Descripcion", max_length=200)
    categoria = models.ForeignKey(
    Categoria,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name="Rubro / Categoría"
)
    precio = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Mínimo")
    imagen = models.ImageField(
        "Imagen",
        upload_to=get_image_path,
        validators=[validate_image_size],
        blank=True,
        null=True,
        help_text="Formatos permitidos: jpg, png, gif. Tamaño máximo: 5MB"
    )
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagen:
            try:
                img = Image.open(self.imagen.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.imagen.path)
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")

    @property
    def necesita_reposicion(self):
        return self.stock < self.stock_minimo