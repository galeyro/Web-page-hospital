export const TOTAL_MINUTES = 24 * 60; // 1440

/**
 * Convierte un string de hora "HH:MM:SS" o "HH:MM" a porcentaje (0-100)
 */
export const timeToPercent = (time: string): number => {
    if (!time) return 0;
    const [hours, minutes] = time.split(':').map(Number);
    const totalMinutes = hours * 60 + minutes;
    return (totalMinutes / TOTAL_MINUTES) * 100;
};

/**
 * Convierte un porcentaje (0-100) a hora "HH:MM" redondeada a 15 min
 */
export const percentToTime = (percent: number): string => {
    // Clamp entre 0 y 100
    const p = Math.max(0, Math.min(100, percent));

    let totalMinutes = (p / 100) * TOTAL_MINUTES;

    // Redondeo a 15 minutos
    const remainder = totalMinutes % 15;
    if (remainder >= 7.5) {
        totalMinutes += (15 - remainder);
    } else {
        totalMinutes -= remainder;
    }

    const h = Math.floor(totalMinutes / 60);
    const m = Math.floor(totalMinutes % 60);

    // Formatear HH:MM
    const hh = h.toString().padStart(2, '0');
    const mm = m.toString().padStart(2, '0');

    // Evitar 24:00 (que sea 23:45 como máximo inicio o manejarlo como fin de día)
    if (h === 24) return "24:00";

    return `${hh}:${mm}`;
};

/**
 * Calcula la duración en porcentaje basada en hora inicio y fin
 */
export const durationToPercent = (start: string, end: string): number => {
    const startP = timeToPercent(start);
    const endP = timeToPercent(end);
    return endP - startP;
};

/**
 * Verifica si hay solapamiento entre un rango nuevo y una lista de citas existentes.
 * Retorna true si hay colisión.
 */
export const checkOverlap = (
    newStart: string,
    newEnd: string,
    existingCitas: any[],
    excludeCitaId?: number
): boolean => {
    const newStartMin = timeToMinutes(newStart);
    const newEndMin = timeToMinutes(newEnd);

    return existingCitas.some(cita => {
        if (excludeCitaId && cita.id === excludeCitaId) return false;

        const citaStart = timeToMinutes(cita.hora_inicio);
        const citaEnd = timeToMinutes(cita.hora_fin);

        // Lógica de solapamiento: (StartA < EndB) y (EndA > StartB)
        return (newStartMin < citaEnd) && (newEndMin > citaStart);
    });
};

const timeToMinutes = (time: string): number => {
    const [h, m] = time.split(':').map(Number);
    return h * 60 + m;
};
