import React, { useState, useRef } from 'react';
import { useDraggable } from '@dnd-kit/core';
import { Cita } from '../../types/scheduler';
import { timeToPercent, durationToPercent } from './utils/timeUtils';
import { createPortal } from 'react-dom';

interface Props {
    cita: Cita;
    isOverlay?: boolean;
}

const CitaBlock = ({ cita, isOverlay = false }: Props) => {
    const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
        id: `cita-${cita.id}`,
        data: {
            type: 'CITA',
            cita: cita,
        },
        disabled: isOverlay
    });

    const [showTooltip, setShowTooltip] = useState(false);
    const [tooltipPos, setTooltipPos] = useState({ top: 0, left: 0 });
    const blockRef = useRef<HTMLDivElement>(null);

    const left = timeToPercent(cita.hora_inicio);
    const width = durationToPercent(cita.hora_inicio, cita.hora_fin);

    const handleMouseEnter = () => {
        if (blockRef.current) {
            const rect = blockRef.current.getBoundingClientRect();
            setTooltipPos({
                top: rect.bottom + window.scrollY + 8,
                left: rect.left + window.scrollX + rect.width / 2
            });
        }
        setShowTooltip(true);
    };

    const containerStyle: React.CSSProperties = {
        position: 'absolute',
        left: isOverlay ? undefined : `${left}%`,
        width: isOverlay ? '160px' : `${width}%`,
        maxWidth: isOverlay ? '160px' : `${width}%`,
        height: '80%',
        top: '10%',
        zIndex: isOverlay ? 9999 : 20,
        pointerEvents: 'auto',
        boxSizing: 'border-box',
        overflow: 'hidden',
        touchAction: 'none', // IMPORTANTE: Evita scroll del navegador al arrastrar
    };

    const cardStyle: React.CSSProperties = {
        width: '100%',
        height: '100%',
        backgroundColor: isDragging && !isOverlay ? '#dbeafe' : '#2563eb',
        opacity: isDragging && !isOverlay ? 0.3 : 1,
        color: 'white',
        borderRadius: '4px',
        padding: '2px 4px',
        cursor: isOverlay ? 'grabbing' : 'grab',
        boxShadow: isOverlay ? '0 10px 15px rgba(0,0,0,0.3)' : '0 1px 2px rgba(0,0,0,0.1)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        border: '1px solid rgba(255,255,255,0.2)',
        boxSizing: 'border-box',
        overflow: 'hidden',
        userSelect: 'none'
    };

    return (
        <div
            ref={(node) => {
                setNodeRef(node);
                // @ts-ignore
                blockRef.current = node;
            }}
            style={containerStyle}
            {...listeners}
            {...attributes}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={() => setShowTooltip(false)}
        >
            <div style={cardStyle}>
                <div style={{
                    fontWeight: 'bold',
                    fontSize: '0.6rem',
                    width: '100%',
                    whiteSpace: 'nowrap',
                    textOverflow: 'ellipsis',
                    overflow: 'hidden',
                    display: 'block'
                }}>
                    {width > 2 ? cita.nombre_paciente : '...'}
                </div>
            </div>

            {showTooltip && !isDragging && !isOverlay && createPortal(
                <div style={{
                    position: 'absolute',
                    top: `${tooltipPos.top}px`,
                    left: `${tooltipPos.left}px`,
                    transform: 'translateX(-50%)',
                    backgroundColor: '#1e293b',
                    color: 'white',
                    padding: '12px',
                    borderRadius: '8px',
                    fontSize: '0.8rem',
                    zIndex: 10001,
                    minWidth: '220px',
                    boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
                    border: '1px solid #334155',
                    textAlign: 'left',
                    pointerEvents: 'none'
                }}>
                    <div style={{ borderBottom: '1px solid #475569', marginBottom: '8px', paddingBottom: '4px', fontWeight: 'bold', color: '#38bdf8' }}>
                        Detalles de la Cita
                    </div>
                    <div><strong>Paciente:</strong> {cita.nombre_paciente}</div>
                    <div><strong>Especialidad:</strong> {cita.nombre_especialidad}</div>
                    <div><strong>Médico:</strong> {cita.nombre_medico}</div>
                    <div style={{ marginTop: '8px', paddingTop: '4px', borderTop: '1px dashed #475569', color: '#94a3b8', fontSize: '0.75rem' }}>
                        📅 {cita.hora_inicio.substring(0, 5)} - {cita.hora_fin.substring(0, 5)}
                    </div>
                </div>,
                document.body
            )}
        </div>
    );
};

export default CitaBlock;
