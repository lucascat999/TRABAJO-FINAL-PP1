from django.contrib.auth.models import User, Group

def crear_usuarios_demo():
    # Grupos ya deben existir (los creamos antes)
    admin_group = Group.objects.get(name='administradores')
    stock_group   = Group.objects.get(name='stock')
    ventas_group  = Group.objects.get(name='ventas')

    # 1. Usuario administrador
    admin, created = User.objects.get_or_create(
        username='admin', defaults={'email': 'admin@demo.com'}
    )
    if created:
        admin.set_password('admin123')
        admin.save()
    admin.groups.set([admin_group])

    # 2. Usuario stock
    stock_user, created = User.objects.get_or_create(
        username='stock', defaults={'email': 'stock@demo.com'}
    )
    if created:
        stock_user.set_password('stock123')
        stock_user.save()
    stock_user.groups.set([stock_group])

    # 3. Usuario ventas
    ventas_user, created = User.objects.get_or_create(
        username='ventas', defaults={'email': 'ventas@demo.com'}
    )
    if created:
        ventas_user.set_password('ventas123')
        ventas_user.save()
    ventas_user.groups.set([ventas_group])

    print("✅ Usuarios demo creados")
    print("   admin   / admin123  → todo")
    print("   stock   / stock123  → productos")
    print("   ventas  / ventas123 → clientes+ventas")