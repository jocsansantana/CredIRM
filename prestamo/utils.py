from .models import Actividad

def registrar_actividad(tipo, descripcion, usuario=None):
    Actividad.objects.create(tipo=tipo, descripcion=descripcion, usuario=usuario)