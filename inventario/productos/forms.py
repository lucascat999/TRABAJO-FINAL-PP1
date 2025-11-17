from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Categoria
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["sku", "nombre", "descripcion", "categoria", "precio", "stock", "stock_minimo", "imagen"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "stock_minimo": "Stock Mínimo (alerta)",
        }
        help_texts = {
            "stock_minimo": "Se mostrará una alerta cuando el stock esté por debajo de este valor"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("sku", placeholder="Ej: FER-001"),
            Field("nombre", placeholder="Nombre del producto"),
            Field("descripcion", placeholder="Breve descripción"),
            Field("categoria", placeholder="Seleccione rubro"),
            Field("precio", placeholder="0.00"),
            Field("stock", placeholder="Cantidad actual"),
            Field("stock_minimo", placeholder="Mínimo antes de alerta"),
            Field("imagen"),
            ButtonHolder(
                Submit("submit", "Guardar", css_class="btn btn-success"),
                HTML('<a href="{% url \'productos:producto_list\' %}" class="btn btn-secondary">Cancelar</a>')
            )
        )

    def clean_sku(self):
        sku = self.cleaned_data.get("sku")
        if Producto.objects.exclude(pk=self.instance.pk).filter(sku=sku).exists():
            raise ValidationError("Ya existe un producto con este SKU.")
        return sku

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio and precio <= 0:
            raise ValidationError("El precio debe ser mayor a cero.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is not None and stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        return stock

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get("stock_minimo")
        if stock_minimo is not None and stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo.")
        return stock_minimo