from django import forms
from apps.ventas.models import Venta, VentaProducto
from django.forms.models import inlineformset_factory
from django.forms import BaseInlineFormSet




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
        fields = ['metodo_pago','nota']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'total_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Venta'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Metodo Pago'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nota'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        # Validaciones adicionales si son necesarias
        return cleaned_data

class BaseVentaProductoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                cantidad = form.cleaned_data.get('cantidad', 0)
                if cantidad <= 0:
                    raise forms.ValidationError("La cantidad debe ser mayor a 0.")

VentaProductoFormSet = inlineformset_factory(
    Venta,
    VentaProducto,
    fields=['producto', 'cantidad', 'descuento', 'precio_unidad_venta'],
    extra=1,
    can_delete=True,
    formset=BaseVentaProductoFormSet  # Asocia el formset personalizado aquí
)