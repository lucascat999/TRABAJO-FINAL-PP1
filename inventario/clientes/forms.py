from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'documento', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'documento': forms.TextInput(attrs={'placeholder': 'Ej: 12345678'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '11-1234-5678'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle 123, Ciudad'}),
        }

    def clean_documento(self):
        documento = self.cleaned_data['documento']
        if Cliente.objects.exclude(pk=self.instance.pk).filter(documento=documento).exists():
            raise forms.ValidationError("Ya existe un cliente con este número de documento.")
        return documento