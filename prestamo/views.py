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
from .utils import *

#DEFINE QUIEN ES EL ADMINISTRADOR
def es_admin(user):
    return user.is_staff

#CERRAR SESION
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos')
        return super().form_invalid(form)


def cerrar_sesion(request):
    logout(request)
    return redirect('login')

#DASHBOARD
@login_required
def index(request):
    total_clientes = Cliente.objects.count()
    total_prestamos = Prestamo.objects.filter(estado='ACTIVO').count() 
    cuotas_atrasadas = Cuota.objects.filter(estado='VENCIDA').select_related('prestamo__cliente') 
    actividades_recientes = Actividad.objects.select_related('usuario')[:5]
    cobrado_mes = Pago.objects.filter(
        fecha_pago__month=timezone.now().month
    ).aggregate(total=Sum('monto'))['total'] or 0

    return render(request, 'home.html', {
        'total_clientes': total_clientes,
        'total_prestamos': total_prestamos,
        'cuotas_atrasadas': cuotas_atrasadas,
        'actividades_recientes': actividades_recientes,
        'cobrado_mes': cobrado_mes,
    })

#CRUD DE CLIENTES
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
            cliente = form.save()
            registrar_actividad(
                tipo='cliente',
                descripcion=f'Nuevo cliente registrado: {cliente.nombres} {cliente.apellidos}',
                usuario=request.user
            )
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
            registrar_actividad(
                tipo='cliente',
                descripcion=f'Cliente actualizado: {cliente.nombres} {cliente.apellidos}',
                usuario=request.user
            )
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
        nombre_completo = f'{cliente.nombres} {cliente.apellidos}'
        cliente.delete()
        registrar_actividad(
            tipo='cliente',
            descripcion=f'Cliente eliminado: {nombre_completo}',
            usuario=request.user
        )
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('clientes')
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})



#CRUD PARA PRESTAMOS
@login_required
def prestamos(request):
    prestamos = Prestamo.objects.select_related('cliente').all().order_by('-fecha_inicio')
    template = loader.get_template('prestamos/display_prestamos.html')
    return HttpResponse(template.render({'prestamos': prestamos}, request))

@login_required
def prestamo_detalle(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    cuotas = prestamo.cuotas.select_related().prefetch_related('pagos').order_by('numero')

    total_pagado = Pago.objects.filter(cuota__prestamo=prestamo).aggregate(
        total=Sum('monto')
    )['total'] or 0

    saldo_pendiente = prestamo.total_pagar - total_pagado

    return render(request, 'prestamos/details_prestamos.html', {
        'prestamo': prestamo,
        'cuotas': cuotas,
        'total_pagado': total_pagado,
        'saldo_pendiente': saldo_pendiente,
    })

@login_required
def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()
            generar_cuotas(prestamo)
            registrar_actividad(
                tipo='prestamo',
                descripcion=f'Préstamo de ${prestamo.monto} otorgado a {prestamo.cliente}',
                usuario=request.user
            )
            messages.success(request, 'Préstamo creado exitosamente')
            return redirect('prestamos')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/form_prestamos.html', {'form': form})

@login_required
def editar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    tiene_pagos = Pago.objects.filter(cuota__prestamo=prestamo).exists()

    if tiene_pagos:
        messages.error(request, 'No se puede editar un préstamo con pagos registrados')
        return redirect('prestamos')

    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            prestamo.cuotas.all().delete()
            generar_cuotas(prestamo)
            registrar_actividad(
                tipo='prestamo',
                descripcion=f'Préstamo #{prestamo.id} actualizado ({prestamo.cliente})',
                usuario=request.user
            )
            messages.success(request, 'Préstamo actualizado exitosamente')
            return redirect('prestamos')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'prestamos/form_prestamos.html', {'form': form})

@login_required
def prestamos_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    prestamos = Prestamo.objects.filter(cliente=cliente).order_by('-fecha_inicio')
    return render(request, 'prestamos/prestamos_cliente.html', {
        'cliente': cliente,
        'prestamos': prestamos
    })

@login_required
@user_passes_test(es_admin, login_url='prestamos')
def eliminar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    tiene_pagos = Pago.objects.filter(cuota__prestamo=prestamo).exists()

    if request.method == 'POST':
        if tiene_pagos:
            prestamo.estado = 'CANCELADO'
            prestamo.save()
            registrar_actividad(
                tipo='prestamo',
                descripcion=f'Préstamo #{prestamo.id} cancelado ({prestamo.cliente})',
                usuario=request.user
            )
            messages.success(request, 'Préstamo cancelado exitosamente (tenía pagos registrados)')
        else:
            descripcion = f'Préstamo #{prestamo.id} eliminado ({prestamo.cliente})'
            prestamo.delete()
            registrar_actividad(
                tipo='prestamo',
                descripcion=descripcion,
                usuario=request.user
            )
            messages.success(request, 'Préstamo eliminado exitosamente')
        return redirect('prestamos')

    return render(request, 'prestamos/confirmar_eliminar.html', {'prestamo': prestamo})