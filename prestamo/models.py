from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class Cliente(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=50)
    fecha_registro = models.DateField(default=timezone.now)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Prestamo(models.Model):
    
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ACTIVO', 'Activo'),
        ('PAGADO', 'Pagado'),
        ('VENCIDO', 'Vencido'),
        ('CANCELADO', 'Cancelado'),
    ]

    FRECUENCIAS = [
        ('SEMANAL', 'Semanal'),
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="prestamos")
    monto = models.DecimalField( max_digits=10, decimal_places=2)
    tasa_interes = models.DecimalField( max_digits=5, decimal_places=2)
    numero_cuotas = models.PositiveIntegerField()
    frecuencia_pago = models.CharField(max_length=20, choices=FRECUENCIAS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_interes = models.DecimalField( max_digits=10, decimal_places=2)
    total_pagar = models.DecimalField( max_digits=10, decimal_places=2)
    estado = models.CharField( max_length=20, choices=ESTADOS, default='PENDIENTE')
    observaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_interes = self.monto * (self.tasa_interes / 100)
        self.total_pagar = self.monto + self.total_interes

        # Calcular fecha_fin según frecuencia y número de cuotas
        if self.frecuencia_pago == 'SEMANAL':
            self.fecha_fin = self.fecha_inicio + timedelta(weeks=self.numero_cuotas)
        elif self.frecuencia_pago == 'QUINCENAL':
            self.fecha_fin = self.fecha_inicio + timedelta(days=15 * self.numero_cuotas)
        else:  # MENSUAL
            self.fecha_fin = self.fecha_inicio + relativedelta(months=self.numero_cuotas)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Préstamo #{self.id} - {self.cliente}"

class Cuota(models.Model):
    
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Pago parcial'),
        ('PAGADA', 'Pagada'),
        ('VENCIDA', 'Vencida'),
    ]

    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='cuotas')
    numero = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField()
    capital = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Cuota {self.numero} - Préstamo #{self.prestamo.id}"

    @property
    def total_pagado(self):
        return self.pagos.aggregate(total=models.Sum('monto'))['total'] or 0

    @property
    def saldo_pendiente(self):
        return self.monto - self.total_pagado

    def actualizar_estado(self):
        """Recalcula el estado de la cuota según lo que se ha pagado."""
        pagado = self.total_pagado
        if pagado >= self.monto:
            self.estado = 'PAGADA'
        elif pagado > 0:
            self.estado = 'PARCIAL'
        else:
            self.estado = 'PENDIENTE'
        self.save()
    @property
    def ultimo_pago(self):
        return self.pagos.order_by('-fecha_pago').first()
    

class Pago(models.Model):
    
    METODOS = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('DEPOSITO','Depósito')
    ]
    
    cuota = models.ForeignKey(Cuota,on_delete=models.CASCADE,related_name='pagos')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10,decimal_places=2)
    metodo_pago = models.CharField(max_length=20,choices=METODOS)
    referencia = models.CharField(max_length=100,blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Pago #{self.id} - ${self.monto}"
    
class Actividad(models.Model):
    
    TIPOS = [
        ('cliente', 'Cliente nuevo'),
        ('prestamo', 'Préstamo nuevo'),
        ('pago', 'Pago registrado'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descripcion}"
    
    