from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(Pago)
admin.site.register(Prestamo)
admin.site.register(Cuota)