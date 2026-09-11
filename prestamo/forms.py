from .models import *
from django import forms

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombres': forms.Textarea(attrs={'rows':1,'class': 'form-control'}),
            'apellidos': forms.Textarea(attrs={'rows':1,'class':'form-control'}),
            'cedula': forms.Textarea(attrs={'rows':1,'class':'form-control'}),
            'telefono': forms.Textarea(attrs={'rows':1,'class':'form-control'}),
            'fecha_registro': forms.DateInput(format= '%Y-%m-%d', attrs={'type':'date','class':'form-control'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        exclude = ['total_interes', 'total_pagar', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
        
class PrestamoEditForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['estado', 'observaciones']
        
class PagoForm(forms.ModelForm):
    cuota = forms.ModelChoiceField(
        queryset=Cuota.objects.none(),
        label='Cuota'
    )

    class Meta:
        model = Pago
        fields = ['cuota', 'monto', 'metodo_pago', 'referencia', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuota'].queryset = Cuota.objects.exclude(
            estado='PAGADA'
        ).select_related('prestamo__cliente').order_by('fecha_vencimiento')

        self.fields['cuota'].label_from_instance = self.label_cuota

    @staticmethod
    def label_cuota(cuota):
        cliente = f"{cuota.prestamo.cliente.nombres} {cuota.prestamo.cliente.apellidos}"
        saldo = cuota.saldo_pendiente
        return f"Préstamo #{cuota.prestamo.id} - {cliente} - Cuota {cuota.numero} - Saldo: ${saldo}"