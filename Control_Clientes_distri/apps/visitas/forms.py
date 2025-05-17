from django import forms
from apps.visitas.models import Visita, VisitaServis


class AddVisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['cliente', 'nota']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True

class VisitaServisForm(forms.ModelForm):
    class Meta:
        model = VisitaServis
        fields = [
            # 'usuario',
            'cliente',
            'nombre_promocion',
            'b_disponible',
            'b_entregado',
            'b_retirado',
            'b_en_poder_clte',
            'nota',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'nombre_promocion': forms.TextInput(attrs={'class': 'form-control'}),
            'b_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'b_entregado': forms.NumberInput(attrs={'class': 'form-control'}),
            'b_retirado': forms.NumberInput(attrs={'class': 'form-control'}),
            'b_en_poder_clte': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'usuario': forms.Select(attrs={'class': 'form-control'}),
            'nota': forms.Textarea(attrs={'class': 'form-control'}),
            # 'nota': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones del servicio (opcional)'})
        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo cliente para que no sea editable
        self.fields['cliente'].disabled = True

        # # Opcional: limitar usuarios por rol (solo quienes pueden registrar visitas)
        # self.fields['usuario'].queryset = self.fields['usuario'].queryset.filter(rol='subusuario')

        # # Opcional: mostrar solo clientes activos
        # self.fields['cliente'].queryset = self.fields['cliente'].queryset.filter(activo=True)