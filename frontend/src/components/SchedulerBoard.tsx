import { useState, useEffect } from "react";
import { getSchedulerData } from "../services/api";
import { SchedulerResponse } from "../types/scheduler";
import { 
    DndContext, 
    DragEndEvent, 
    PointerSensor, 
    useSensor, 
    useSensors 
} from "@dnd-kit/core";

export default function SchedulerBoard(){
    const [data, setData] = useState<SchedulerResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]);

    // CONFIGURACIÓN DE SENSORES
    // Esto es crucial para evitar errores. Usamos PointerSensor para que funcione con mouse y touch.
    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8, // Hay que mover el mouse 8px para empezar a arrastrar (evita clicks accidentales)
            },
        })
    );

    useEffect(()=>{
        const load = async() => {
            try{
                setLoading(true);
                const response = await getSchedulerData(fecha);
                setData(response.data);
            }catch(error){
                console.log("Error cargando datos: ", error);
            }finally{
                setLoading(false);
            }
        };

        load();
    }, [fecha]);

    const handleDragEnd = (event: DragEndEvent) => {
        console.log("Terminó drag: ", event);
    };

    if (loading) {
        return <p style={{color:'black', padding: 20}}>Cargando...</p>;
    };

    return (
        <div className="p-4" style={{padding: 20}}> 
            <div style={{ marginBottom: 20, display: 'flex', alignItems: 'center', gap: 10 }}>
                <h2 style={{color: '#333', margin: 0}}>Agenda del día:</h2>
                <input 
                    type="date" 
                    value={fecha} 
                    onChange={(e) => setFecha(e.target.value)}
                    style={{
                        padding: '8px 12px',
                        fontSize: '16px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        cursor: 'pointer'
                    }}
                />
            </div>
            
            {/* Pasa los sensores al contexto */}
            <DndContext sensors={sensors} onDragEnd={handleDragEnd}>
                <div style={{ display: 'flex', gap: '20px', overflowX: 'auto', padding: '20px 0' }}>
                    {data?.consultorios.map(c => (
                        <div key={c.id} style={{ minWidth: 250, background:'white', border: '1px solid #ccc', borderRadius: 8, padding: 10, boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                            <h3 style={{color: '#444', borderBottom: '1px solid #eee'}}>{c.numero}</h3>
                            {/* Mostramos las citas bonito en lugar de JSON crudo */}
                            <div style={{marginTop: 10}}>
                                {c.citas.length > 0 ? c.citas.map(cita => (
                                    <div key={cita.id} style={{background: '#f0f9ff', padding: 8, marginBottom: 5, borderRadius: 4, borderLeft: '3px solid #007bff'}}>
                                        <div style={{fontWeight: 'bold', fontSize: 12}}>{cita.hora_inicio}</div>
                                        <div style={{color: '#555'}}>{cita.nombre_paciente}</div>
                                    </div>
                                )) : <div style={{color: '#999', fontStyle: 'italic'}}>Sin citas</div>}
                            </div>
                        </div>
                    ))}
                </div>
            </DndContext>
        </div>
    );
}