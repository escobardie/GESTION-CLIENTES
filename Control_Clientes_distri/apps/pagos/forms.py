from django import forms
from apps.pagos.models import Pagos


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = [ 'monto','metodo_pago', 'descripcion']
        widgets = {
            #'cliente': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
        }
