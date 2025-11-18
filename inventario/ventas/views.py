from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db import transaction
from .models import Venta, ItemVenta
from .forms import VentaForm, ItemVentaFormSet
from productos.models import Producto


# ---------- CREAR VENTA ----------
@login_required
@transaction.atomic
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = ItemVentaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            # =====  DEBUG  =====
            print("DEBUG form válido")
            print("DEBUG formset válido")
            print("DEBUG cantidad de forms en formset:", len(formset.forms))
            for f in formset.forms:
                print("  form data:", f.cleaned_data)
            # ===================

            venta = form.save(commit=False)
            venta.save()

            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                    item = item_form.save(commit=False)
                    item.venta = venta
                    item.subtotal = item.cantidad * item.precio_unitario
                    item.save()

                    producto = item.producto
                    if producto.stock < item.cantidad:
                        messages.error(request, f"Stock insuficiente para {producto.nombre} (disponible: {producto.stock})")
                        raise ValueError("Stock insuficiente")
                    producto.stock -= item.cantidad
                    producto.save()

            venta.total = sum(it.subtotal for it in venta.items.all())
            venta.save()
            messages.success(request, "Venta registrada.")
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaForm()
        formset = ItemVentaFormSet()

    productos = Producto.objects.all()
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Nueva Venta',
        'productos': productos,
    })


# ---------- EDITAR VENTA ----------
@login_required
@transaction.atomic
def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = ItemVentaFormSet(request.POST, instance=venta)
        if form.is_valid() and formset.is_valid():
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
                    item.subtotal = item.cantidad * item.precio_unitario
                    item.save()

                    prod = item.producto
                    if prod.stock < item.cantidad:
                        messages.error(request, f"Stock insuficiente para {prod.nombre} (disponible: {prod.stock})")
                        raise ValueError("Stock insuficiente")
                    prod.stock -= item.cantidad
                    prod.save()

            venta.total = sum(it.subtotal for it in venta.items.all())
            venta.save()
            messages.success(request, "Venta actualizada.")
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaForm(instance=venta)
        formset = ItemVentaFormSet(instance=venta)

    productos = Producto.objects.all()
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Editar Venta',
        'productos': productos,
    })


# ---------- ANULAR VENTA ----------
@login_required
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
class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
    ordering = ['-fecha']


# ---------- DETALLE ----------
class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'
    context_object_name = 'venta'


# ---------- IMPRIMIR ----------
class VentaPrintView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_print.html'
    context_object_name = 'venta'