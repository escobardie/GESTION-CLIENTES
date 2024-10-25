from django import forms
from apps.visitas.models import Visita


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
