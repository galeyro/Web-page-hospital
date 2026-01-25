import React from 'react';
import { useDroppable } from '@dnd-kit/core';
import { Consultorio, Cita } from '../../types/scheduler';
import CitaBlock from './CitaBlock';
import { timeToPercent, durationToPercent } from './utils/timeUtils';
import { SIDEBAR_WIDTH } from './TimeRuler';

interface Props {
    consultorio: Consultorio;
    activeCita?: Cita | null;
    horariosMedico?: any[];
}

const TimelineRow = ({ consultorio, activeCita, horariosMedico }: Props) => {
    const { setNodeRef, isOver } = useDroppable({
        id: `consultorio-${consultorio.id}`,
        data: { consultorio }
    });

    let isCompatible = true;
    let backgroundColor = 'white';

    if (activeCita) {
        const isCitaInterna = activeCita.tipo_medico?.toLowerCase().includes('interno') ||
            activeCita.tipo_medico?.toLowerCase().includes('general');

        if (isCitaInterna) {
            const belongsToThisRow = consultorio.citas.some(c => c.id === activeCita.id);
            if (!belongsToThisRow) isCompatible = false;
        } else {
            if (consultorio.tipo !== 'externo') isCompatible = false;
        }

        if (!isCompatible) {
            backgroundColor = '#f8fafc';
        } else if (isOver) {
            backgroundColor = '#f0fdf4';
        }
    }

    return (
        <div style={{ display: 'flex', borderBottom: `1px solid #e2e8f0`, height: '80px', boxSizing: 'border-box' }}>
            {/* Header Consultorio */}
            <div style={{
                minWidth: SIDEBAR_WIDTH,
                width: SIDEBAR_WIDTH,
                borderRight: '1px solid #cbd5e1',
                backgroundColor: '#ffffff',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                position: 'sticky',
                left: 0,
                zIndex: 30,
                flexShrink: 0,
                boxSizing: 'border-box'
            }}>
                <div style={{ fontSize: '1.2rem', fontWeight: '900', color: '#1e293b' }}>{consultorio.numero}</div>
                <div style={{
                    marginTop: '2px',
                    fontSize: '0.6rem',
                    fontWeight: '800',
                    textTransform: 'uppercase',
                    padding: '2px 8px',
                    borderRadius: '10px',
                    backgroundColor: consultorio.tipo === 'interno' ? '#eff6ff' : '#fdf2f8',
                    color: consultorio.tipo === 'interno' ? '#3b82f6' : '#db2777',
                    border: `1px solid ${consultorio.tipo === 'interno' ? '#dbeafe' : '#fbcfe8'}`
                }}>
                    {consultorio.tipo}
                </div>
            </div>

            {/* Track temporal */}
            <div
                ref={setNodeRef}
                style={{
                    flex: 1,
                    position: 'relative',
                    backgroundColor: backgroundColor,
                    transition: 'background-color 0.2s',
                    overflow: 'visible',
                    boxSizing: 'border-box'
                }}
            >
                {/* 1. GRID DE FONDO (HORAS) */}
                <div style={{
                    position: 'absolute',
                    top: 0, left: 0, right: 0, bottom: 0,
                    display: 'grid',
                    gridTemplateColumns: 'repeat(24, 1fr)',
                    pointerEvents: 'none',
                    zIndex: 0,
                    boxSizing: 'border-box'
                }}>
                    {Array.from({ length: 24 }).map((_, i) => (
                        <div key={i} style={{
                            borderLeft: '1px solid #f1f5f9',
                            height: '100%',
                            boxSizing: 'border-box'
                        }} />
                    ))}
                </div>

                {/* 2. SUBGRID DE 15 MINUTOS (Solo si hay drag activo) */}
                {activeCita && (
                    <div style={{
                        position: 'absolute',
                        top: 0, left: 0, right: 0, bottom: 0,
                        display: 'grid',
                        gridTemplateColumns: `repeat(${24 * 4}, 1fr)`, // 96 columnas de 15m
                        pointerEvents: 'none',
                        zIndex: 0,
                        boxSizing: 'border-box'
                    }}>
                        {Array.from({ length: 24 * 4 }).map((_, i) => (
                            <div key={i} style={{
                                borderLeft: '1px solid rgba(226, 232, 240, 0.4)',
                                height: '100%',
                                boxSizing: 'border-box'
                            }} />
                        ))}
                    </div>
                )}

                {/* 3. RESALTADO DE DISPONIBILIDAD (Sombra Verde) */}
                {activeCita && isCompatible && horariosMedico && horariosMedico.map((horario, index) => {
                    const leftPos = timeToPercent(horario.hora_inicio);
                    const widthPos = durationToPercent(horario.hora_inicio, horario.hora_fin);
                    return (
                        <div key={`avail-${index}`} style={{
                            position: 'absolute',
                            left: `${leftPos}%`,
                            width: `${widthPos}%`,
                            top: 0,
                            bottom: 0,
                            backgroundColor: 'rgba(34, 197, 94, 0.12)', // Un poco más intenso
                            borderLeft: '2px solid #22c55e',
                            borderRight: '2px solid #22c55e',
                            pointerEvents: 'none',
                            zIndex: 1,
                            boxSizing: 'border-box',
                            display: 'flex',
                            alignItems: 'flex-start',
                            padding: '4px'
                        }}>
                            <span style={{ fontSize: '0.6rem', color: '#166534', fontWeight: 'bold' }}>✓ DISPONIBLE</span>
                        </div>
                    );
                })}

                {/* 4. RENDERIZADO DE CITAS */}
                {consultorio.citas.map(cita => (
                    <CitaBlock key={cita.id} cita={cita} />
                ))}
            </div>
        </div>
    );
};

export default TimelineRow;
