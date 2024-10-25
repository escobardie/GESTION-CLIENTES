from django import forms
from apps.promociones.models import Promo  

class AddPromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        fields = ['nombre_promo', 'valor_promo', 'cant_bidones', 'vencimiento_promo', 'estado', 'nota']
        widgets = {
            'nombre_promo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Promoción'}),
            'valor_promo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de la Promoción'}),
            'cant_bidones': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad de Bidones'}),
            'vencimiento_promo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas sobre la promoción'}),
        }
