from django import forms
from apps.productos.models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre_producto', 'precio_producto',
                  'proveedor', 'stock','imagen_url','descripcion_producto']

        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Producto'}),
            'precio_producto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio del Producto'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proveedor'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en stock'}),
            'imagen_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion_producto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del Producto'}),
            #'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }