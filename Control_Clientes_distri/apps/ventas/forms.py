from django import forms
from apps.ventas.models import Venta, VentaProducto


class VentaProductoForm(forms.ModelForm):
    class Meta:
        model = VentaProducto
        fields = ['producto', 'cantidad', 'descuento', 'precio_unidad_venta', 'precio_total_venta']
        widgets = {
            #'venta': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad', 'min': 1}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Descuento', 'min': 0}),
            'precio_unidad_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio por Unidad'}),
            'precio_total_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Venta'}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'metodo_pago']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'total_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Venta'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Metodo Pago'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nota'}),
        }
