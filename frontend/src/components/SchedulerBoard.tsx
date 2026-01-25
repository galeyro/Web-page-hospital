import { useState, useEffect } from "react";
import { getSchedulerData, reprogramarCita } from "../services/api";
import { SchedulerResponse, Cita } from "../types/scheduler";
import {
    DndContext,
    DragEndEvent,
    DragStartEvent,
    PointerSensor,
    useSensor,
    useSensors,
    DragOverlay,
    defaultDropAnimationSideEffects,
    DropAnimation
} from "@dnd-kit/core";
import { createPortal } from "react-dom";

import TimeRuler from "./Scheduler/TimeRuler";
import TimelineRow from "./Scheduler/TimelineRow";
import CitaBlock from "./Scheduler/CitaBlock";
import { percentToTime, checkOverlap } from "./Scheduler/utils/timeUtils";

const dropAnimation: DropAnimation = {
    sideEffects: defaultDropAnimationSideEffects({
        styles: {
            active: {
                opacity: '0.4',
            },
        },
    }),
};

export default function SchedulerBoard() {
    const [data, setData] = useState<SchedulerResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]);
    const [activeCita, setActiveCita] = useState<Cita | null>(null);
    const [totalCitas, setTotalCitas] = useState(0);

    // Sensor de puntero universal para máxima compatibilidad
    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 3, // Solo 3px de movimiento para arrancar
            },
        })
    );

    useEffect(() => {
        cargarDatos();
    }, [fecha]);

    useEffect(() => {
        if (data) {
            const total = data.consultorios.reduce((acc, c) => acc + c.citas.length, 0);
            setTotalCitas(total);
        }
    }, [data]);

    const cargarDatos = async () => {
        try {
            setLoading(true);
            const response = await getSchedulerData(fecha);
            setData(response.data);
        } catch (error) {
            console.error("Error cargando datos: ", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDragStart = (event: DragStartEvent) => {
        const { active } = event;
        if (active.data.current && active.data.current.type === 'CITA') {
            setActiveCita(active.data.current.cita);
        }
    };

    const handleDragEnd = async (event: DragEndEvent) => {
        const { active, over } = event;
        setActiveCita(null);

        if (!over || !active.data.current || !data) return;

        const currentCita = active.data.current.cita as Cita;
        const consultorioIdStr = String(over.id).replace('consultorio-', '');
        const targetConsultorioId = parseInt(consultorioIdStr);
        const targetConsultorio = data.consultorios.find(c => c.id === targetConsultorioId);

        if (!targetConsultorio) return;

        // Validaciones Médicas
        const isInterna = currentCita.tipo_medico?.toLowerCase().includes('interno') ||
            currentCita.tipo_medico?.toLowerCase().includes('general');

        if (isInterna) {
            const origin = data.consultorios.find(c => c.citas.some(cita => cita.id === currentCita.id));
            if (origin && targetConsultorio.id !== origin.id) {
                alert("⚠️ Las citas internas no pueden cambiar de consultorio.");
                return;
            }
        } else {
            if (targetConsultorio.tipo?.toLowerCase() !== 'externo') {
                alert("⚠️ Las citas externas solo van a consultorios externos.");
                return;
            }
        }

        const dropRect = active.rect.current.translated;
        const rect = over.rect;

        if (!dropRect || !rect) return;

        const relativeX = dropRect.left - rect.left;
        let percent = (relativeX / rect.width) * 100;
        const newStartTime = percentToTime(percent);

        const [h1, m1] = currentCita.hora_inicio.split(':').map(Number);
        const [h2, m2] = currentCita.hora_fin.split(':').map(Number);
        const durationMin = (h2 * 60 + m2) - (h1 * 60 + m1);

        const [newH, newM] = newStartTime.split(':').map(Number);
        let endTotalMin = newH * 60 + newM + durationMin;
        const newEndTime = `${String(Math.floor(endTotalMin / 60)).padStart(2, '0')}:${String(endTotalMin % 60).padStart(2, '0')}`;

        if (checkOverlap(newStartTime, newEndTime, targetConsultorio.citas, currentCita.id)) {
            alert(`❌ Horario ocupado (${newStartTime} - ${newEndTime}).`);
            return;
        }

        if (window.confirm(`¿Reprogramar cita a las ${newStartTime}?`)) {
            try {
                await reprogramarCita(currentCita.id, {
                    consultorio_id: targetConsultorio.id,
                    fecha: fecha,
                    hora_inicio: newStartTime,
                    hora_fin: newEndTime
                });
                cargarDatos();
            } catch (err: any) {
                const msg = err.response?.data?.error || "Error al actualizar la cita.";
                alert(`Error: ${msg}`);
            }
        }
    };

    if (loading) return (
        <div style={{
            height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'linear-gradient(to bottom, #f8fafc, #f1f5f9)'
        }}>
            <div style={{ color: '#2563eb', fontWeight: 'bold' }}>🔄 Sincronizando Agenda...</div>
        </div>
    );

    return (
        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
            <div style={{
                padding: '20px', width: '100%', minHeight: '100vh', display: 'flex', flexDirection: 'column',
                backgroundColor: 'transparent', position: 'relative', zIndex: 10
            }}>
                <header style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <h1 style={{ color: '#0f172a', margin: 0, fontSize: '1.5rem', fontWeight: '900' }}>Hospital Scheduler</h1>
                    <input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} style={{ padding: '8px', borderRadius: '8px', border: '1px solid #e2e8f0', fontWeight: 'bold' }} />
                </header>

                <div style={{ flex: 1, border: '1px solid #e2e8f0', borderRadius: '20px', backgroundColor: 'white', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                    <div style={{ width: '100%', flex: 1, display: 'flex', flexDirection: 'column' }}>
                        <TimeRuler />
                        <div style={{ overflowY: 'auto', flex: 1 }}>
                            {data?.consultorios.map(c => {
                                const horariosActivos = activeCita ?
                                    data.horarios_disponibles.filter(h =>
                                        h.nombre_medico?.toLowerCase().trim() === activeCita.nombre_medico?.toLowerCase().trim()
                                    ) : [];
                                return <TimelineRow key={c.id} consultorio={c} activeCita={activeCita} horariosMedico={horariosActivos} />;
                            })}
                        </div>
                    </div>
                </div>
            </div>

            {createPortal(
                <DragOverlay dropAnimation={dropAnimation} style={{ zIndex: 99999 }}>
                    {activeCita ? <CitaBlock cita={activeCita} isOverlay /> : null}
                </DragOverlay>,
                document.body
            )}
        </DndContext>
    );
}