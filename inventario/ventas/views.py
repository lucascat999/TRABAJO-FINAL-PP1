from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Venta, ItemVenta
from .forms import VentaForm, ItemVentaFormSet
from productos.models import Producto

# ---------- CREAR VENTA ----------
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
                    # Descuenta stock
                    producto = item.producto
                    producto.stock -= item.cantidad
                    producto.save()
            venta.save()
            messages.success(request, "Venta registrada.")
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaForm()
        formset = ItemVentaFormSet()
    
    # Enviar productos al template para el form vacío
    productos = Producto.objects.all()
    
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Nueva Venta',
        'productos': productos,
    })

# ---------- EDITAR VENTA ----------
def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = ItemVentaFormSet(request.POST, instance=venta)
        if form.is_valid() and formset.is_valid():
            # Devuelve stock anterior
            for item in venta.items.all():
                prod = item.producto
                prod.stock += item.cantidad
                prod.save()
            venta.total = 0
            venta.save()
            form.save()
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                    item = item_form.save(commit=False)
                    item.venta = venta
                    item.save()
                    venta.total += item.subtotal
                    # Descuenta nuevo stock
                    prod = item.producto
                    prod.stock -= item.cantidad
                    prod.save()
            venta.save()
            messages.success(request, "Venta actualizada.")
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaForm(instance=venta)
        formset = ItemVentaFormSet(instance=venta)
    
    # Enviar productos al template
    productos = Producto.objects.all()
    
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Editar Venta',
        'productos': productos,
    })

# ---------- ANULAR VENTA ----------
def venta_anular(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if not venta.anulada:
        for item in venta.items.all():
            prod = item.producto
            prod.stock += item.cantidad
            prod.save()
        venta.anulada = True
        venta.save()
        messages.success(request, "Venta anulada y stock restaurado.")
    else:
        messages.warning(request, "La venta ya estaba anulada.")
    return redirect('venta_detail', pk=pk)

# ---------- LISTADO ----------
class VentaListView(ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
    ordering = ['-fecha']

# ---------- DETALLE ----------
class VentaDetailView(DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'
    context_object_name = 'venta'

# ---------- IMPRIMIR ----------
class VentaPrintView(DetailView):
    model = Venta
    template_name = 'ventas/venta_print.html'
    context_object_name = 'venta'