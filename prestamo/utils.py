from datetime import timedelta
from dateutil.relativedelta import relativedelta
from .models import *

def registrar_actividad(tipo, descripcion, usuario=None):
    Actividad.objects.create(tipo=tipo, descripcion=descripcion, usuario=usuario)


def generar_cuotas(prestamo):
    capital_por_cuota = prestamo.monto / prestamo.numero_cuotas
    interes_por_cuota = prestamo.total_interes / prestamo.numero_cuotas
    monto_por_cuota = prestamo.total_pagar / prestamo.numero_cuotas

    fecha = prestamo.fecha_inicio

    for i in range(1, prestamo.numero_cuotas + 1):
        if prestamo.frecuencia_pago == 'SEMANAL':
            fecha = fecha + timedelta(weeks=1)
        elif prestamo.frecuencia_pago == 'QUINCENAL':
            fecha = fecha + timedelta(days=15)
        else:  # MENSUAL
            fecha = fecha + relativedelta(months=1)

        Cuota.objects.create(
            prestamo=prestamo,
            numero=i,
            fecha_vencimiento=fecha,
            capital=round(capital_por_cuota, 2),
            interes=round(interes_por_cuota, 2),
            monto=round(monto_por_cuota, 2),
            estado='PENDIENTE'
        )