from django import forms
from .models import Cliente,Visita,Promo,PromoPorCliente,RegistroPago


class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono',
                  'direccion', 'fecha_cobro','tipo_promo']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_cobro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_promo': forms.Select(attrs={'class': 'form-control'}),
            # tipo_promo es una relación de clave foránea (ForeignKey) y solo se puede 
            # seleccionar una promoción, se debería usar forms.Select. 
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

# class AddPromoForm(forms.ModelForm):
#     class Meta:
#         model = Promo
#         fields = ['nombre_promo', 'valor_promo', 'cant_bidones',
#                 'vencimiento_promo', 'estado', 'nota']

#         widgets = {
#             'nombre_promo': forms.TextInput(attrs={'class': 'form-control'}),
#             'valor_promo': forms.NumberInput(attrs={'class': 'form-control'}),
#             'cant_bidones': forms.NumberInput(attrs={'class': 'form-control'}),
#             'vencimiento_promo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             #'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}, initial=True),  # Valor predeterminado en el formulario
#             'nota': forms.Textarea(attrs={'class': 'form-control'}),
#         }

class AddPromoPorClienteForm(forms.ModelForm):
    class Meta:
        model = PromoPorCliente
        fields = ['cliente', 'promo', 'inicio_promo', 'fin_promo',
                'bidones_disponibles', 'codigo_dispenser', 'estado', 'nota']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            # 'cliente': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
            'inicio_promo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fin_promo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bidones_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_dispenser': forms.TextInput(attrs={'class': 'form-control'}),
            #'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}, initial=True),  # Valor predeterminado en el formulario
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True
        self.fields['inicio_promo'].disabled = True

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

# class AddRegistroPagoForm(forms.ModelForm):
#     class Meta:
#         model = RegistroPago
#         fields = ['cliente', 'fecha', 'monto', 'comprobante', 'nota']

#         widgets = {
#             'cliente': forms.Select(attrs={'class': 'form-control'}),
#             'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'monto': forms.NumberInput(attrs={'class': 'form-control'}),
#             'comprobante': forms.FileInput(attrs={'class': 'form-control'}),
#             'nota': forms.Textarea(attrs={'class': 'form-control'}),
#         }

## Clases CSS: Se usó class='form-control' para aplicar estilos de Bootstrap a los campos, 
## y class='form-check-input' para los campos de tipo checkbox (como estado).

