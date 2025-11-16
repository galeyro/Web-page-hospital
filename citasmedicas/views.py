from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Especialidad, Medico, Paciente, Consultorio, HorarioMedico, Cita
from .forms import EspecialidadForm, MedicoForm, PacienteForm, ConsultorioForm, HorarioMedicoForm, CitaForm

# ---------- ESPECIALIDAD ----------
@login_required
def especialidad_list(request):
    especialidades = Especialidad.objects.all()
    return render(request, "citasmedicas/especialidad_list.html", {"especialidades": especialidades})

@login_required
def especialidad_create(request):
    if request.method == "POST":
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidad creada correctamente.")
            return redirect("especialidad_list")
    else:
        form = EspecialidadForm()
    return render(request, "citasmedicas/especialidad_form.html", {"form": form})

@login_required
def especialidad_edit(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == "POST":
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, "Especialidad actualizada.")
            return redirect("especialidad_list")
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, "citasmedicas/especialidad_form.html", {"form": form})

@login_required
def especialidad_delete(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    especialidad.delete()
    messages.success(request, "Especialidad eliminada.")
    return redirect("especialidad_list")


# ---------- MÉDICO ----------
@login_required
def medico_list(request):
    medicos = Medico.objects.all()
    return render(request, "citasmedicas/medico_list.html", {"medicos": medicos})

@login_required
def medico_create(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado.")
            return redirect("medico_list")
    else:
        form = MedicoForm()
    return render(request, "citasmedicas/medico_form.html", {"form": form})

@login_required
def medico_edit(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == "POST":
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico actualizado.")
            return redirect("medico_list")
    else:
        form = MedicoForm(instance=medico)
    return render(request, "citasmedicas/medico_form.html", {"form": form})

@login_required
def medico_delete(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    medico.delete()
    messages.success(request, "Médico eliminado.")
    return redirect("medico_list")


# ---------- PACIENTE ----------
@login_required
def paciente_list(request):
    pacientes = Paciente.objects.all()
    return render(request, "citasmedicas/paciente_list.html", {"pacientes": pacientes})

@login_required
def paciente_create(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente registrado.")
            return redirect("paciente_list")
        else:
            print(form.errors)
    else:
        form = PacienteForm()
    return render(request, "citasmedicas/paciente_form.html", {"form": form})

@login_required
def paciente_edit(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente actualizado.")
            return redirect("paciente_list")
    else:
        form = PacienteForm(instance=paciente)
    return render(request, "citasmedicas/paciente_form.html", {"form": form})

@login_required
def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.delete()
    messages.success(request, "Paciente eliminado.")
    return redirect("paciente_list")

# ---------- CONSULTORIO ----------
@login_required
def consultorio_list(request):
    consultorios = Consultorio.objects.all()
    return render(request, "citasmedicas/consultorio_list.html", {"consultorios": consultorios})

@login_required
def consultorio_create(request):
    if request.method == "POST":
        form = ConsultorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultorio registrado.")
            return redirect("consultorio_list")
    else:
        form = ConsultorioForm()
    return render(request, "citasmedicas/consultorio_form.html", {"form": form})

@login_required
def consultorio_edit(request, pk):
    consultorio = get_object_or_404(Consultorio, pk=pk)
    if request.method == "POST":
        form = ConsultorioForm(request.POST, instance=consultorio)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultorio actualizado.")
            return redirect("consultorio_list")
    else:
        form = ConsultorioForm(instance=consultorio)
    return render(request, "citasmedicas/consultorio_form.html", {"form": form})

@login_required
def consultorio_delete(request, pk):
    consultorio = get_object_or_404(Consultorio, pk=pk)
    consultorio.delete()
    messages.success(request, "Consultorio eliminado.")
    return redirect("consultorio_list")

# ---------- HORARIO ----------
@login_required
def horario_list(request):
    horarios = HorarioMedico.objects.all()
    return render(request, "citasmedicas/horario_list.html", {"horarios": horarios})

@login_required
def horario_create(request):
    if request.method == "POST":
        form = HorarioMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Horario registrado.")
            return redirect("horario_list")
    else:
        form = HorarioMedicoForm()
    return render(request, "citasmedicas/horario_form.html", {"form": form})

@login_required
def horario_edit(request, pk):
    horario = get_object_or_404(HorarioMedico, pk=pk)
    if request.method == "POST":
        form = HorarioMedicoForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, "Horario actualizado.")
            return redirect("horario_list")
    else:
        form = HorarioMedicoForm(instance=horario)
    return render(request, "citasmedicas/horario_form.html", {"form": form})

@login_required
def horario_delete(request, pk):
    horario = get_object_or_404(HorarioMedico, pk=pk)
    horario.delete()
    messages.success(request, "Horario eliminado.")
    return redirect("horario_list")

# ---------- CITA ----------
@login_required
def cita_list(request):
    citas = Cita.objects.all()
    return render(request, "citasmedicas/cita_list.html", {"citas": citas})

@login_required
def cita_create(request):
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita registrada.")
            return redirect("cita_list")
    else:
        form = CitaForm()
    return render(request, "citasmedicas/cita_form.html", {"form": form})

@login_required
def cita_edit(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita actualizada.")
            return redirect("cita_list")
    else:
        form = CitaForm(instance=cita)
    return render(request, "citasmedicas/cita_form.html", {"form": form})

@login_required
def cita_delete(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == "POST":
        cita.delete()
        messages.success(request, "Cita eliminada.")
        return redirect("cita_list")
    return render(request, "citasmedicas/confirm_delete.html", {"obj": cita})
