from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, MovimientoStock
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML, Row, Column

# -----------------------------------------------------------------------------
# Formulario para el modelo Producto
# -----------------------------------------------------------------------------
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["sku", "nombre", "descripcion", "precio", "stock", "stock_minimo", "imagen"]
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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("sku", placeholder="Ej: PROD-001"),
            Field("nombre", placeholder="Nombre del producto"),
            Field("descripcion", placeholder="Breve descripción"),
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

# -----------------------------------------------------------------------------
# Formulario para el modelo MovimientoStock
# -----------------------------------------------------------------------------
class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ["tipo", "cantidad", "motivo"]
        widgets = {
            "motivo": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "tipo": "Tipo de movimiento",
            "cantidad": "Cantidad",
            "motivo": "Motivo (opcional)"
        }

    def __init__(self, *args, **kwargs):
        self.producto = kwargs.pop("producto", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        stock_info = ""
        if self.producto:
            stock_info = f"""
            <div class="alert alert-info">
                <strong>Producto:</strong> {self.producto.nombre}<br>
                <strong>Stock actual:</strong> {self.producto.stock}
            </div>
            """

        self.helper.layout = Layout(
            HTML(stock_info),
            Field("tipo"),
            Field("cantidad"),
            Field("motivo"),
            ButtonHolder(
                Submit("submit", "Registrar movimiento", css_class="btn btn-success"),
                HTML('<a href="{{ request.META.HTTP_REFERER }}" class="btn btn-secondary">Cancelar</a>')
            )
        )

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero")

        if self.producto and self.cleaned_data.get("tipo") == "salida":
            if cantidad > self.producto.stock:
                raise ValidationError(f"No hay suficiente stock. Disponible: {self.producto.stock}")
        return cantidad

# -----------------------------------------------------------------------------
# Formulario para ajustar el stock a un valor específico
# -----------------------------------------------------------------------------
class AjusteStockForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=0,
        label="Nuevo Stock",
        help_text="Establece el nuevo valor de stock para el producto."
    )
    motivo = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Motivo del Ajuste",
        help_text="Explica por qué estás ajustando el stock (opcional)."
    )

    def __init__(self, *args, **kwargs):
        self.producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        stock_info = ""
        if self.producto:
            stock_info = f"""
            <div class="alert alert-info">
                <strong>Producto:</strong> {self.producto.nombre}<br>
                <strong>Stock actual:</strong> {self.producto.stock}
            </div>
            """
            self.fields['cantidad'].initial = self.producto.stock

        self.helper.layout = Layout(
            HTML(stock_info),
            Field('cantidad'),
            Field('motivo'),
            ButtonHolder(
                Submit('submit', 'Ajustar Stock', css_class='btn btn-warning'),
                HTML('<a href="{{ request.META.HTTP_REFERER }}" class="btn btn-secondary">Cancelar</a>')
            )
        )