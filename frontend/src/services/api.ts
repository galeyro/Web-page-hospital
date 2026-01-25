import axios from "axios";
import { Cita, Consultorio, SchedulerResponse, ReprogramarDatos } from "../types/scheduler";

//1. configurar la instancia base
const api = axios.create({
    baseURL: '/api'
});

//2. Funcion para obtener datos (Tipada)
export const getSchedulerData = (fecha: string) => {
    return api.get<SchedulerResponse>('/scheduler/', {
        params: {
            fecha,
            _t: Date.now() // Cache busting automático
        }
    });
};

//3. Funcion para reprogramar
export const reprogramarCita = (id: number, datos: ReprogramarDatos) => {
    return api.put(`/citas/${id}/reprogramar/`, datos);
};

export default api;