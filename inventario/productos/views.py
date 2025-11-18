from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models   # Para usar F()
from .models import Producto, Categoria
from .forms import ProductoForm

# ---------- Listado con filtro + paginación ----------
@login_required
def producto_list(request):
    qs = Producto.objects.all().order_by('nombre')
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        qs = qs.filter(categoria_id=categoria_id)

    paginator = Paginator(qs, 10)  # 10 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    categorias = Categoria.objects.all()
    return render(request, 'productos/producto_list.html', {
        'productos': productos,
        'categorias': categorias
    })

# ---------- Alta ----------
@login_required
@permission_required('productos.add_producto', raise_exception=True)
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('productos:producto_list')
        else:
            messages.error(request, "Error al crear el producto. Verifique los datos.")
    else:
        form = ProductoForm()
    return render(request, 'productos/producto_form.html', {'form': form})

# ---------- Detalle ----------
@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

# ---------- Edición ----------
@login_required
@permission_required('productos.change_producto', raise_exception=True)
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productos:producto_list')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/producto_form.html', {'form': form})

# ---------- Eliminación ----------
@login_required
@permission_required('productos.delete_producto', raise_exception=True)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('productos:producto_list')
    return render(request, 'productos/producto_confirm_delete.html', {'producto': producto})

# ---------- Stock bajo ----------
@login_required
def stock_bajo_list(request):
    productos = Producto.objects.filter(stock__lt=models.F('stock_minimo'))
    return render(request, 'productos/stock_bajo_list.html', {'productos': productos})

# ---------- Dashboard ----------
@login_required
def dashboard(request):
    total_productos = Producto.objects.count()
    productos_stock_bajo = Producto.objects.filter(stock__lt=models.F('stock_minimo')).count()
    total_categorias = Categoria.objects.count()

    return render(request, 'productos/dashboard.html', {
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo,
        'total_categorias': total_categorias,
    })
# ---------- Listado de categorías ----------
@login_required
def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'productos/categoria_list.html', {'categorias': categorias})

# ---------- Alta de categoría ----------
@login_required
@permission_required('productos.add_categoria', raise_exception=True)
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        if nombre:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, "Categoría creada correctamente.")
            return redirect('productos:categoria_list')
        else:
            messages.error(request, "El nombre es obligatorio.")
    return render(request, 'productos/categoria_form.html')

# ---------- Edición de categoría ----------
@login_required
@permission_required('productos.change_categoria', raise_exception=True)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        if categoria.nombre:
            categoria.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('productos:categoria_list')
        else:
            messages.error(request, "El nombre es obligatorio.")
    return render(request, 'productos/categoria_form.html', {'categoria': categoria})

# ---------- Eliminación de categoría ----------
@login_required
@permission_required('productos.delete_categoria', raise_exception=True)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('productos:categoria_list')
    return render(request, 'productos/categoria_confirm_delete.html', {'categoria': categoria})
