from django.urls import path
from . import views
#SECCIÓN DE CLIENTES
urlpatterns = [
    path("", views.index, name="index"),
    path("clientes/", views.clientes, name="clientes"),
    path("cliente_detalle/<int:id>", views.cliente_detalle, name="cliente_detalle"),
    path("cliente_editar/<int:id>", views.editar_cliente, name ="editar_cliente"),
    path("cliente_eliminar/<int:id>", views.eliminar_cliente, name ="eliminar_cliente"),
    path("formulario_cliente/", views.crear_cliente, name="crear_cliente"),
    
    #SECCIÓN DE LOGIN PARA CLIENTES
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    
    #SECCIÓN PARA PRESTAMOS
    
    path('prestamos/', views.prestamos, name='prestamos'),
    path('prestamos/nuevo/', views.crear_prestamo, name='crear_prestamo'),
    path('prestamos/<int:id>/', views.prestamo_detalle, name='prestamo_detalle'),
    path('prestamos/editar/<int:id>/', views.editar_prestamo, name='editar_prestamo'),
    path('prestamos/eliminar/<int:id>/', views.eliminar_prestamo, name='eliminar_prestamo'),
    path('clientes/<int:cliente_id>/prestamos/', views.prestamos_cliente, name='prestamos_cliente'),
    
    #SECCIÓN DE CUOTA
    path('cuotas/', views.cuotas, name='cuotas'),
    
    #SECCIÓN DE PAGO
    path('pagos/nuevo/', views.registrar_pago, name='registrar_pago'),
    path('pagos/comprobante/<int:id>/', views.comprobante_pago, name='comprobante_pago'),
] 