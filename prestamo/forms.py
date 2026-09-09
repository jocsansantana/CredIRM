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
        exclude = ['total_interes', 'total_pagar']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }