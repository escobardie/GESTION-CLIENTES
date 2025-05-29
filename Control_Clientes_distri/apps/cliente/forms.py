from django import forms
from .models import Cliente, PromoPorCliente, Promo

# class AddClienteForm(forms.ModelForm):

#     class Meta:
#         model = Cliente
#         fields = ['nombre', 'apellido', 'telefono',
#                   'direccion']

#         widgets = {
#             'nombre': forms.TextInput(attrs={'class': 'form-control'}),
#             'apellido': forms.TextInput(attrs={'class': 'form-control'}),
#             'telefono': forms.TextInput(attrs={'class': 'form-control'}),
#             'direccion': forms.TextInput(attrs={'class': 'form-control'}),
#         }

class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'codigo_area',
            'telefono',
            'direccion',
            'localidad',
            'provincia',
            'latitud',
            'longitud',
            'email',
            'observacion',
            'ubicacion',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_area': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ubicacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

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
            'codigo_dispenser': forms.TextInput(attrs={'class': 'form-control'}),
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args,user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True
        if user is not None:
            print("ENTRO POR ACA")
            print(user.usuario_padre)
            # Filtrar las promos asociadas al usuario (dueño)
            # "SOLO EL USUARIO TIENE ACCERO A CARGAR PROMOS Y CLIENTES"
            self.fields['promo'].queryset = Promo.objects.filter(usuario=user)

class ServisVisitaClienteForm(forms.ModelForm):
    class Meta:
        model = PromoPorCliente
        fields = ['cliente', 'promo','bidones_disponibles',
        'entrega_bidones', 'retorno_bidones', 'bidones_acumulados']
        # ,'codigo_dispenser', 'nota']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
            'bidones_disponibles': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'entrega_bidones': forms.NumberInput(attrs={'class': 'form-control'}),
            'retorno_bidones': forms.NumberInput(attrs={'class': 'form-control'}),
            'bidones_acumulados': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            # 'codigo_dispenser': forms.TextInput(attrs={'class': 'form-control'}),
            # 'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True
        # self.fields['codigo_dispenser'].disabled = True
        # self.fields['nota'].disabled = True
        self.fields['promo'].disabled = True
