// Define la forma de una Cita
export interface Cita {
    id: number;
    fecha: string;       // "YYYY-MM-DD"
    hora_inicio: string; // "HH:MM:SS"
    hora_fin: string;
    nombre_medico: string;
    tipo_medico: string;
    nombre_paciente: string;
    nombre_especialidad: string;
}

// Define la forma de un Consultorio (ConsultorioSchedulerSerializer)
export interface Consultorio {
    id: number;
    numero: string;
    tipo: string;
    citas: Cita[]; // ¡Importante! Un consultorio tiene una lista de citas
}

// Define la forma de un Horario de disponibilidad de un médico
export interface HorarioMedico {
    id: number;
    id_medico: number;
    nombre_medico: string;
    dia_semana: number;
    hora_inicio: string;
    hora_fin: string;
}

// Define la respuesta completa del Scheduler (SchedulerDataView)
export interface SchedulerResponse {
    consultorios: Consultorio[];
    horarios_disponibles: HorarioMedico[]; // Por ahora ponle any o define la interfaz Horario si quieres
    huerfanos?: Cita[]; // Citas sin consultorio asignado
}

export interface ReprogramarDatos {
    consultorio_id?: number;
    fecha?: string;
    hora_inicio?: string;
    hora_fin?: string;
}