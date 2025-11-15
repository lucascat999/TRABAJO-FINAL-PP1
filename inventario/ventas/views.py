from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Venta
from .forms import VentaForm, ItemVentaFormSet

def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = ItemVentaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            venta = form.save(commit=False)
            venta.total = 0
            venta.save()
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                    item = item_form.save(commit=False)
                    item.venta = venta
                    item.save()
                    venta.total += item.subtotal
                    # Descontar stock
                    producto = item.producto
                    producto.stock -= item.cantidad
                    producto.save()
            venta.save()
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaForm()
        formset = ItemVentaFormSet()
    return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

class VentaListView(ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'

class VentaDetailView(DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'
    context_object_name = 'venta'