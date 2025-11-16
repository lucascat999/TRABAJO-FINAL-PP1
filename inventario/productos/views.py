from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView   # (opcional) si querés clases más adelante
from .models import Producto
from .forms import ProductoForm   # lo creamos después si no existe

# ---------- Listado de productos ----------
def producto_list(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'productos/producto_list.html', {'productos': productos})

# ---------- Alta de producto ----------
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/producto_form.html', {'form': form})

# ---------- Stock bajo ----------
def stock_bajo_list(request):
    """Muestra productos cuyo stock es menor o igual a 10."""
    productos = Producto.objects.filter(stock__lte=10)
    return render(request, 'productos/stock_bajo_list.html', {'productos': productos})
# ---------- agregar al final de productos/views.py ----------
from django.shortcuts import get_object_or_404

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/producto_form.html', {'form': form})

def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:producto_list')
    return render(request, 'productos/producto_confirm_delete.html', {'producto': producto})