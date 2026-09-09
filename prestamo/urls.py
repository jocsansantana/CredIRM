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
    
] 