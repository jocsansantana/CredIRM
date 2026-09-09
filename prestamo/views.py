from django.shortcuts import render, redirect
from .models import *
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


#DEFINE QUIEN ES EL ADMINISTRADOR
def es_admin(user):
    return user.is_staff


#CRUD DE CLIENTES
@login_required
def index(request):
    total_clientes = Cliente.objects.count()
    total_prestamos = Prestamo.objects.filter(estado='Activo').count()
    cuotas_atrasadas = Cuota.objects.filter(estado='Vencida').select_related('prestamo__cliente')
    pagos_recientes = Pago.objects.select_related('cuota__prestamo__cliente').order_by('-fecha_pago')[:5]
    cobrado_mes = Pago.objects.filter(
        fecha_pago__month=timezone.now().month
    ).aggregate(total=Sum('monto'))['total'] or 0

    return render(request, 'home.html', {
        'total_clientes': total_clientes,
        'total_prestamos': total_prestamos,
        'cuotas_atrasadas': cuotas_atrasadas,
        'pagos_recientes': pagos_recientes,
        'cobrado_mes': cobrado_mes,
    })

@login_required 
def clientes(request):
    clientes = Cliente.objects.all()
    template = loader.get_template('clientes/display_clientes.html')
    return HttpResponse(template.render({'clientes': clientes}, request))

@login_required
def cliente_detalle(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'clientes/details_clientes.html', {
        'cliente': cliente
    })

@login_required
def crear_cliente(request):
    if request.method=='POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Cliente creado exitosamente')
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request,'clientes/form_cliente.html',{'form':form})

@login_required
def editar_cliente(request,id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST,instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request,'clientes/form_cliente.html', {'form':form})

@login_required
@user_passes_test(es_admin, login_url='clientes')
def eliminar_cliente(request,id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('clientes')
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos')
        return super().form_invalid(form)


def cerrar_sesion(request):
    logout(request)
    return redirect('login')