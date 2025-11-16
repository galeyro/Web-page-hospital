from django import forms
from .models import Especialidad, Medico, Paciente, Consultorio, HorarioMedico, Cita
from .validators import validar_cedula_ecuador


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ["nombre"]


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            "cedula",
            "nombre",
            "apellido",
            "correo",
            "telefono",
            "especialidad",
            "numero_licencia",
            "estatus"
        ]

    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"]
        if not validar_cedula_ecuador(cedula):
            raise forms.ValidationError("La cédula ingresada no es válida.")
        return cedula


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "cedula",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "correo",
            "sexo",
            "provincia",
        ]

    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"]
        if not validar_cedula_ecuador(cedula):
            raise forms.ValidationError("La cédula ingresada no es válida.")
        return cedula


class ConsultorioForm(forms.ModelForm):
    class Meta:
        model = Consultorio
        fields = ["codigo", "medico"]


class HorarioMedicoForm(forms.ModelForm):
    class Meta:
        model = HorarioMedico
        fields = ["medico", "dia_semana", "hora_inicio", "hora_fin"]


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            "paciente",
            "medico",
            "consultorio",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "estado"
        ]
