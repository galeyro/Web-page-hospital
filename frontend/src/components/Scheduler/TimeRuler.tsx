import React from 'react';

// Reducimos el ancho para que quepa mejor en pantallas sin scroll
export const SIDEBAR_WIDTH = '140px';

const TimeRuler = () => {
    const hours = Array.from({ length: 24 }, (_, i) => i);

    return (
        <div style={{
            display: 'flex',
            height: '40px',
            borderBottom: '1px solid #d1d5db',
            background: '#f8fafc',
            position: 'sticky',
            top: 0,
            zIndex: 60,
            boxSizing: 'border-box',
            width: '100%'
        }}>
            <div style={{
                minWidth: SIDEBAR_WIDTH,
                width: SIDEBAR_WIDTH,
                borderRight: '1px solid #cbd5e1',
                background: '#f1f5f9',
                flexShrink: 0,
                boxSizing: 'border-box'
            }} />

            <div style={{
                flex: 1,
                display: 'grid',
                gridTemplateColumns: 'repeat(24, 1fr)',
                position: 'relative',
                boxSizing: 'border-box'
            }}>
                {hours.map(h => (
                    <div key={h} style={{
                        borderLeft: '1px solid #e2e8f0',
                        fontSize: '0.65rem', // Un poco más pequeño
                        fontWeight: '700',
                        color: '#64748b',
                        paddingLeft: '2px',
                        display: 'flex',
                        alignItems: 'center',
                        boxSizing: 'border-box'
                    }}>
                        {h}:00
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TimeRuler;
