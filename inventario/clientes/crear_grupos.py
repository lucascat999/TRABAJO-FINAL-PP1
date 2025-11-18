from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def crear_grupos():
    # 1. Crear o recuperar grupos
    admin_group, _ = Group.objects.get_or_create(name='administradores')
    stock_group, _   = Group.objects.get_or_create(name='stock')
    ventas_group, _  = Group.objects.get_or_create(name='ventas')

    # 2. Permisos de productos/categorías → grupo "stock"
    producto_ct   = ContentType.objects.get(app_label='productos', model='producto')
    categoria_ct  = ContentType.objects.get(app_label='productos', model='categoria')
    stock_perms   = Permission.objects.filter(content_type__in=[producto_ct, categoria_ct])
    stock_group.permissions.set(stock_perms)

    # 3. Permisos de clientes + ventas → grupo "ventas"
    cliente_ct  = ContentType.objects.get(app_label='clientes', model='cliente')
    venta_ct    = ContentType.objects.get(app_label='ventas', model='venta')
    item_ct     = ContentType.objects.get(app_label='ventas', model='itemventa')
    ventas_perms = Permission.objects.filter(content_type__in=[cliente_ct, venta_ct, item_ct])
    ventas_group.permissions.set(ventas_perms)

    # 4. Administradores → todos los permisos
    admin_group.permissions.set(Permission.objects.all())

    print("✅ Grupos y permisos creados")