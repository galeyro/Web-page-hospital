from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Especialidad, Medico, Paciente, Consultorio, HorarioMedico, Cita
from .forms import EspecialidadForm, MedicoForm, PacienteForm, ConsultorioForm, HorarioMedicoForm, CitaForm

# ---------- UTILIDADES ----------
def guardar_instancia(request, form, template):
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Guardado correctamente.")
                return redirect(request.path.rsplit("/", 2)[0] + "/")  # Redirigir a lista
            except Exception as e:
                messages.error(request, f"Error: {e}")
    return render(request, template, {"form": form})


# ---------- ESPECIALIDAD ----------
def especialidad_list(request):
    items = Especialidad.objects.all()
    return render(request, "citasmedicas/especialidad_list.html", {"items": items})

def especialidad_create(request):
    form = EspecialidadForm(request.POST or None)
    return guardar_instancia(request, form, "citasmedicas/especialidad_form.html")

def especialidad_edit(request, pk):
    obj = get_object_or_404(Especialidad, pk=pk)
    form = EspecialidadForm(request.POST or None, instance=obj)
    return guardar_instancia(request, form, "citasmedicas/especialidad_form.html")

def especialidad_delete(request, pk):
    obj = get_object_or_404(Especialidad, pk=pk)
    obj.delete()
    return redirect("especialidad_list")


# ---------- MÉDICO ----------
def medico_list(request):
    items = Medico.objects.all()
    return render(request, "citasmedicas/medico_list.html", {"items": items})

def medico_create(request):
    form = MedicoForm(request.POST or None)
    return guardar_instancia(request, form, "citasmedicas/medico_form.html")

def medico_edit(request, pk):
    obj = get_object_or_404(Medico, pk=pk)
    form = MedicoForm(request.POST or None, instance=obj)
    return guardar_instancia(request, form, "citasmedicas/medico_form.html")

def medico_delete(request, pk):
    obj = get_object_or_404(Medico, pk=pk)
    obj.delete()
    return redirect("medico_list")


# ---------- PACIENTE ----------
def paciente_list(request):
    items = Paciente.objects.all()
    return render(request, "citasmedicas/paciente_list.html", {"items": items})

def paciente_create(request):
    form = PacienteForm(request.POST or None)
    return guardar_instancia(request, form, "citasmedicas/paciente_form.html")

def paciente_edit(request, pk):
    obj = get_object_or_404(Paciente, pk=pk)
    form = PacienteForm(request.POST or None, instance=obj)
    return guardar_instancia(request, form, "citasmedicas/paciente_form.html")

def paciente_delete(request, pk):
    obj = get_object_or_404(Paciente, pk=pk)
    obj.delete()
    return redirect("paciente_list")


# ---------- CONSULTORIO ----------
def consultorio_list(request):
    items = Consultorio.objects.all()
    return render(request, "citasmedicas/consultorio_list.html", {"items": items})

def consultorio_create(request):
    form = ConsultorioForm(request.POST or None)
    return guardar_instancia(request, form, "citasmedicas/consultorio_form.html")

def consultorio_edit(request, pk):
    obj = get_object_or_404(Consultorio, pk=pk)
    form = ConsultorioForm(request.POST or None, instance=obj)
    return guardar_instancia(request, form, "citasmedicas/consultorio_form.html")

def consultorio_delete(request, pk):
    obj = get_object_or_404(Consultorio, pk=pk)
    obj.delete()
    return redirect("consultorio_list")


# ---------- HORARIO ----------
def horario_list(request):
    items = HorarioMedico.objects.all()
    return render(request, "citasmedicas/horario_list.html", {"items": items})

def horario_create(request):
    form = HorarioMedicoForm(request.POST or None)
    return guardar_instancia(request, form, "citasmedicas/horario_form.html")

def horario_edit(request, pk):
    obj = get_object_or_404(HorarioMedico, pk=pk)
    form = HorarioMedicoForm(request.POST or None, instance=obj)
    return guardar_instancia(request, form, "citasmedicas/horario_form.html")

def horario_delete(request, pk):
    obj = get_object_or_404(HorarioMedico, pk=pk)
    obj.delete()
    return redirect("horario_list")


# ---------- CITA ----------
def cita_list(request):
    items = Cita.objects.all()
    return render(request, "citasmedicas/cita_list.html", {"items": items})

def cita_create(request):
    form = CitaForm(request.POST or None)
    return guardar_instancia(request, form, "citasmedicas/cita_form.html")

def cita_edit(request, pk):
    obj = get_object_or_404(Cita, pk=pk)
    form = CitaForm(request.POST or None, instance=obj)
    return guardar_instancia(request, form, "citasmedicas/cita_form.html")

def cita_delete(request, pk):
    obj = get_object_or_404(Cita, pk=pk)
    obj.delete()
    return redirect("cita_list")
