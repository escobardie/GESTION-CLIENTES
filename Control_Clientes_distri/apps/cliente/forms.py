from django import forms
from .models import Cliente,Visita,Promo,PromoPorCliente,Venta,Producto,VentaProducto, Pagos



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



class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono',
                  'direccion']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class AddVisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['cliente', 'nota']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            #'fecha_visita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True

class AddPromoPorClienteForm(forms.ModelForm):
    class Meta:
        model = PromoPorCliente
        fields = ['cliente', 'promo', 'fin_promo', 'fecha_pago_promo',
                'codigo_dispenser', 'estado', 'nota']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_pago_promo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fin_promo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # 'bidones_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_dispenser': forms.TextInput(attrs={'class': 'form-control'}),
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True
        
class ServisVisitaClienteForm(forms.ModelForm):
    class Meta:
        model = PromoPorCliente
        fields = ['cliente', 'promo','bidones_disponibles',
        'entrega_bidones', 'retorno_bidones', 'bidones_acumulados',
        'codigo_dispenser', 'nota']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            # 'cliente': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
            
            'bidones_disponibles': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'entrega_bidones': forms.NumberInput(attrs={'class': 'form-control'}),
            'retorno_bidones': forms.NumberInput(attrs={'class': 'form-control'}),
            'bidones_acumulados': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'codigo_dispenser': forms.TextInput(attrs={'class': 'form-control'}),
            #'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}, initial=True),  # Valor predeterminado en el formulario
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True
        # self.fields['bidones_disponibles'].disabled = True
        # self.fields['bidones_acumulados'].disabled = True
        self.fields['codigo_dispenser'].disabled = True
        self.fields['promo'].disabled = True

    # def clean(self):
    #     cleaned_data = super().clean()
    #     bidones_disponibles = cleaned_data.get('bidones_disponibles')
    #     entrega_bidones = cleaned_data.get('entrega_bidones')
        

    #     if bidones_disponibles is not None and entrega_bidones is not None:
    #         new_bidones_disponibles = bidones_disponibles - entrega_bidones
    #         cleaned_data['bidones_disponibles'] = new_bidones_disponibles
       
    #     ##################################
    #     bidones_acumulados = cleaned_data.get('bidones_acumulados')
    #     retorno_bidones = cleaned_data.get('retorno_bidones')
    #     cleaned_data['bidones_acumulados'] = bidones_acumulados + entrega_bidones - retorno_bidones
    #     ##################################

    #     return cleaned_data

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
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'total_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Venta'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nota'}),
        }

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
