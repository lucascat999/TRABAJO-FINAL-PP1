from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib import messages
from .models import Producto, Categoria
from .forms import ProductoForm

# ---------- Listado con filtro por rubro ----------
def producto_list(request):
    qs = Producto.objects.all().order_by('nombre')
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        qs = qs.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.all()
    return render(request, 'productos/producto_list.html',
                  {'productos': qs, 'categorias': categorias})

# ---------- Alta ----------
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('productos:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/producto_form.html', {'form': form})

# ---------- Detalle ----------
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

# ---------- Edición ----------
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productos:producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/producto_form.html', {'form': form})

# ---------- Eliminación ----------
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('productos:producto_list')
    return render(request, 'productos/producto_confirm_delete.html', {'producto': producto})

# ---------- Stock bajo ----------
def stock_bajo_list(request):
    productos = Producto.objects.filter(stock__lte=10)
    return render(request, 'productos/stock_bajo_list.html', {'productos': productos})