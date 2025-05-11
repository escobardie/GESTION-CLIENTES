from django import forms
from .models import Suscripcion, SuscripcionPorUsuario, PagoSuscriptor
from apps.usuarios.models import Usuario

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = [
            'nombre_suscripcion',
            'valor_suscripcion',
            'fecha_vencimiento',
            'limite_clientes',
            'limite_empleados',
            'estado',
            'nota',
        ]
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'nota': forms.Textarea(attrs={'rows': 3}),
        }

    

class SuscripcionPorUsuarioForm(forms.ModelForm):
    class Meta:
        model = SuscripcionPorUsuario
        fields = [
            'usuario',
            'suscripcion',
            'fecha_cobro_suscrip',
            'fecha_fin_suscrip',
            'estado',
            'nota',
        ]
        widgets = {
            'fecha_cobro_suscrip': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin_suscrip': forms.DateInput(attrs={'type': 'date'}),
            'nota': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Solo incluir usuarios con rol 'cliente'
        self.fields['usuario'].queryset = Usuario.objects.filter(rol='cliente')

    def clean(self):
        cleaned_data = super().clean()
        fecha_cobro = cleaned_data.get('fecha_cobro_suscrip')
        fecha_fin = cleaned_data.get('fecha_fin_suscrip')

        if fecha_cobro and fecha_fin and fecha_fin < fecha_cobro:
            raise forms.ValidationError("La fecha de fin no puede ser anterior a la fecha de cobro.")

        return cleaned_data

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if self.instance.pk is None and SuscripcionPorUsuario.objects.filter(usuario=usuario).exists():
            raise forms.ValidationError("Este usuario ya tiene una suscripción asignada.")
        return usuario



class PagoSuscriptorForm(forms.ModelForm):
    class Meta:
        model = PagoSuscriptor
        fields = [
            'usuario',
            'suscripcion',
            'monto',
            'metodo_pago',
            'descripcion',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'monto': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(rol='cliente')
        self.fields['monto'].disabled = True  # protege también del POST

    def clean_monto(self):
        # Asegura que no se pierda el valor si es desactivado
        return self.cleaned_data.get('monto') or 0
