from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, validar_cedula_ecuador, validar_telefono, validar_edad
from citas.models import Medico, Consultorio, Horario, Especialidad
from datetime import time


class CreateMedicoForm(forms.Form):
    """Formulario para crear un nuevo médico (usuario con rol médico)"""
    
    # Datos del usuario
    nombres = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres'
        })
    )
    apellidos = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos'
        })
    )
    cedula = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cédula (10 dígitos)'
        })
    )
    telefono = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono (10 dígitos)'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    genero = forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    
    # Datos del médico
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Especialidad'
    )
    tipo = forms.ChoiceField(
        choices=[('interno', 'Médico Interno'), ('externo', 'Médico Externo')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Médico'
    )
    numero_licencia = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de Licencia (opcional)'
        })
    )
    consultorio = forms.ModelChoiceField(
        queryset=Consultorio.objects.filter(activo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_consultorio'}),
        label='Consultorio (solo para internos)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el queryset dinámico para actualizar en cada instancia
        self.fields['consultorio'].queryset = Consultorio.objects.filter(activo=True)
    
    def clean(self):
        cleaned_data = super().clean()
        cedula = cleaned_data.get('cedula', '').strip()
        telefono = cleaned_data.get('telefono', '').strip()
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
        tipo = cleaned_data.get('tipo')
        consultorio = cleaned_data.get('consultorio')
        
        # Validar cédula
        if cedula:
            try:
                validar_cedula_ecuador(cedula)
            except ValidationError as e:
                self.add_error('cedula', e.message)
        
        # Validar teléfono
        if telefono:
            try:
                validar_telefono(telefono)
            except ValidationError as e:
                self.add_error('telefono', e.message)
        
        # Validar edad
        if fecha_nacimiento:
            try:
                validar_edad(fecha_nacimiento)
            except ValidationError as e:
                self.add_error('fecha_nacimiento', e.message)
        
        # Validar que no exista usuario con esa cédula
        if cedula and Usuario.objects.filter(cedula=cedula).exists():
            self.add_error('cedula', 'Ya existe un usuario con esta cédula')
        
        # Validar que no exista usuario con ese email
        email = cleaned_data.get('email', '').strip()
        if email and Usuario.objects.filter(email=email).exists():
            self.add_error('email', 'Ya existe un usuario con este email')
        
        # Validar médico interno debe tener consultorio
        if tipo == 'interno' and not consultorio:
            self.add_error('consultorio', 'Los médicos internos deben tener un consultorio asignado')
        
        # Validar médico externo no puede tener consultorio
        if tipo == 'externo' and consultorio:
            self.add_error('consultorio', 'Los médicos externos no pueden tener consultorio')
        
        # Validar que el consultorio sea del tipo correcto
        if consultorio:
            if tipo == 'interno' and consultorio.tipo != 'interno':
                self.add_error('consultorio', 'Debe seleccionar un consultorio de tipo interno')
            elif tipo == 'externo' and consultorio.tipo != 'externo':
                self.add_error('consultorio', 'Debe seleccionar un consultorio de tipo externo')
        
        return cleaned_data


class CreateConsultorioForm(forms.ModelForm):
    """Formulario para crear un nuevo consultorio"""
    
    class Meta:
        model = Consultorio
        fields = ['numero', 'tipo', 'descripcion', 'activo']
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número del consultorio'
            }),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción (opcional)',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero and Consultorio.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un consultorio con este número')
        return numero


class CreateHorarioForm(forms.ModelForm):
    """Formulario para crear un horario de médico"""
    
    class Meta:
        model = Horario
        fields = ['medico', 'dia_semana', 'hora_inicio', 'hora_fin']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        medico = cleaned_data.get('medico')
        dia_semana = cleaned_data.get('dia_semana')
        
        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise ValidationError('La hora de fin debe ser posterior a la hora de inicio')
        
        # Validar que no exista otro horario para el mismo médico el mismo día
        if medico and dia_semana is not None:
            existe = Horario.objects.filter(
                medico=medico,
                dia_semana=dia_semana
            ).exclude(pk=self.instance.pk).exists()
            
            if existe:
                raise ValidationError(
                    f'Este médico ya tiene un horario asignado para este día de la semana'
                )
        
        return cleaned_data


class CreateEspecialidadForm(forms.ModelForm):
    """Formulario para crear una nueva especialidad"""
    
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'duracion_cita']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la especialidad'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción (opcional)',
                'rows': 3
            }),
            'duracion_cita': forms.Select(attrs={'class': 'form-control'})
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and Especialidad.objects.filter(nombre=nombre).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe una especialidad con este nombre')
        return nombre
