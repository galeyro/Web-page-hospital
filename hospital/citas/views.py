from django.shortcuts import render
from datetime import datetime, timedelta
# Create your views here.

# Hace la suma de los minutos por los bloques
def sumar_minutos(hora, minutos):
    dt = datetime.combine(datetime.today(), hora)
    return (dt + timedelta(minutes=minutos)).time()

# Permite verificar que no existan 2 citas al misma hora sobrelapadas
def hay_conflicto(inicio, fin, citas):
    for c in citas:
        if not (fin <= c.hora_inicio or inicio >= c.hora_fin):
            return True
    return False

