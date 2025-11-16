from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={"placeholder":"correo@ejemplo.com"}))
    contraseña = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"placeholder":"contrasenaEjemplo1"}))

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        contraseña = cleaned.get("contraseña")
        if email and contraseña:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise ValidationError("Correo o contraseña incorrectos.")
            # authenticate espera username por defecto; podemos usar check_password
            if not user.check_password(contraseña):
                raise ValidationError("Correo o contraseña incorrectos.")
            if not user.is_active:
                raise ValidationError("Cuenta inactiva. Contacta al administrador.")
            cleaned["user"] = user
        return cleaned

class EmailRegisterForm(forms.ModelForm):
    contraseña = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username", "cedula", "telefono"]
        labels = {
            "email": "Correo electrónico",
            "username": "Nombre de usuario",
            "cedula": "Cédula",
            "telefono": "Teléfono",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder":"usuario (opcional)"}),
            "cedula": forms.TextInput(attrs={"placeholder":"Cédula/ID"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("contraseña")
        p2 = cleaned.get("confirmar_contraseña")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["contraseña"])
        # por defecto no damos permisos de admin
        user.is_active = True
        if commit:
            user.save()
        return user