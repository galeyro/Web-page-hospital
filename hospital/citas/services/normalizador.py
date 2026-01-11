from datetime import datetime

def normalizar_fecha_hora(fecha_str, hora_ini_str, hora_fin_str):
    # --- Fecha ---
    # Limpia puntos en meses tipo "Dec." -> "Dec"
    fecha_str = fecha_str.replace(".", "")
    
    # Convierte la fecha obtenida a datetime
    fecha = datetime.strptime(fecha_str, "%b %d, %Y")
    fecha_final = fecha.strftime("%Y-%m-%d")

    # --- Hora inicio ---
    hora_ini_str = hora_ini_str.replace(".", "").strip().lower()  # "9:30 am"
    hora_ini = datetime.strptime(hora_ini_str, "%I:%M %p")
    hora_ini_final = hora_ini.strftime("%H:%M")

    # --- Hora fin ---
    hora_fin_str = hora_fin_str.replace(".", "").strip().lower()  # "9:45 am"
    hora_fin = datetime.strptime(hora_fin_str, "%I:%M %p")
    hora_fin_final = hora_fin.strftime("%H:%M")

    return fecha_final, hora_ini_final, hora_fin_final