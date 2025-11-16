from django.core.exceptions import ValidationError


def validar_cedula_ecuador(cedula: str):
    """
    Valida una cédula ecuatoriana usando el algoritmo oficial.
    
    La cédula ecuatoriana tiene 10 dígitos:
    - Primeros 2 dígitos: provincia (01-24)
    - Dígito 3: tipo de identificación (0-5 para personas naturales)
    - Últimos 6 dígitos: número secuencial
    - Dígito 10: dígito verificador (calculado con algoritmo)
    """
    cedula = str(cedula).strip()

    # Verificar que sea numérica y de 10 dígitos
    if not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError("La cédula debe tener 10 dígitos numéricos.")

    # Validar código de provincia (01 a 24)
    provincia = int(cedula[0:2])
    if provincia < 1 or provincia > 24:
        raise ValidationError("El código de provincia es inválido en la cédula.")

    # Validar tercer dígito (menor a 6 para personas naturales)
    if int(cedula[2]) >= 6:
        raise ValidationError("La cédula no corresponde a una persona natural válida.")

    # Algoritmo del dígito verificador
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9
        suma += valor

    digito_verificador = 10 - (suma % 10)
    if digito_verificador == 10:
        digito_verificador = 0

    if digito_verificador != int(cedula[9]):
        raise ValidationError("La cédula no es válida.")
