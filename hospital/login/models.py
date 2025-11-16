from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

# Validador de cédula ecuatoriana
def validar_cedula_ecuador(cedula):
    """
    Valida una cédula ecuatoriana usando el algoritmo oficial.
    
    La cédula ecuatoriana tiene 10 dígitos:
    - Primeros 2 dígitos: provincia (01-24)
    - Dígito 3: tipo de identificación (0-9)
    - Últimos 6 dígitos: número secuencial
    - Dígito 10: dígito verificador (calculado con algoritmo)
    """
    
    # Verificar que sea string de 10 dígitos
    if not isinstance(cedula, str) or not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError('La cédula debe tener 10 dígitos')
    
    # Verificar que la provincia sea válida (01-24)
    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        raise ValidationError('La provincia indicada en la cédula no existe')
    
    # Algoritmo de validación del dígito verificador
    multiplicadores = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    
    for i in range(9):
        digito = int(cedula[i])
        resultado = digito * multiplicadores[i]
        
        # Si el resultado es mayor a 9, restar 9
        if resultado > 9:
            resultado -= 9
        
        suma += resultado
    
    # Calcular el dígito verificador
    digito_verificador_calculado = (10 - (suma % 10)) % 10
    digito_verificador_real = int(cedula[9])
    
    # Comparar el dígito calculado con el proporcionado
    if digito_verificador_calculado != digito_verificador_real:
        raise ValidationError('La cédula no es válida (dígito verificador incorrecto)')

# Validador de telefono valido
def validar_telefono(telefono):
    """
    Valida que el teléfono tenga exactamente 10 dígitos
    """
    if not telefono.isdigit() or len(telefono) != 10:
        raise ValidationError('Número de teléfono invalido')

# Validador de edad para crear usuario
def validar_edad(fecha_nacimiento):
    """
    Valida que el usuario sea mayor de 18 años
    """
    hoy = date.today()
    edad = relativedelta(hoy, fecha_nacimiento).years
    
    if edad < 18:
        raise ValidationError('El usuario debe ser mayor de 18 años')

# Create your models here.
class Usuario(models.Model):
    ROLES_CHOICES = [
        ('usuario', 'Usuario'),
        ('medico', 'Médico'),
        ('admin', 'Administrador')
    ]
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=20, 
        unique=True,
        validators=[validar_cedula_ecuador]
    )
    telefono = models.CharField(
        max_length=15,
        validators=[validar_telefono]
        )
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(
        validators=[validar_edad]
    )
    genero = models.CharField(max_length=1, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ])
    password = models.CharField(max_length=128)
    rol = models.CharField(
        max_length=10,
        choices=ROLES_CHOICES,
        default='usuario'  # Por defecto, nuevo usuario es 'usuario'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"