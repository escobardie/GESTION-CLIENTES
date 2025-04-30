# forms.py
from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class SubusuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password')
