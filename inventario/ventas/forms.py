from django import forms
from django.forms import inlineformset_factory
from .models import Venta, ItemVenta
from productos.models import Producto
from clientes.models import Cliente


class VentaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Venta
        fields = ['cliente']   # ← sacamos 'codigo' para que lo genere auto


class ItemVentaForm(forms.ModelForm):
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        producto = self.cleaned_data.get('producto')
        if producto and cantidad > producto.stock:
            raise forms.ValidationError(f"Stock insuficiente. Disponible: {producto.stock}")
        return cantidad


ItemVentaFormSet = inlineformset_factory(
    Venta, ItemVenta, form=ItemVentaForm, extra=0, can_delete=True
)