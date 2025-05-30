# forms.py
from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class SubusuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repetir contraseña")

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'codigo_area', 'telefono')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Las contraseñas no coinciden")
        return cleaned_data


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repetir contraseña")

    class Meta:
        model = Usuario
        fields = (
            'username', 'first_name', 'last_name', 'empresa_nombre', 'codigo_area',
            'telefono', 'direccion', 'localidad', 'provincia', 'email', 'password',
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Las contraseñas no coinciden")
        return cleaned_data
