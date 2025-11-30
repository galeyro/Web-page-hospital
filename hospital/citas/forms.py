from django import forms
from .models import Cita, Especialidad

class CitaCreateForm(forms.Form):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha"
    )
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        label="Especialidad"
    )