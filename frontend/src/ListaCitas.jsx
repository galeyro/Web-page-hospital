import { useState, useEffect } from "react";

function ListaCitas(){
    const [citas, setCitas] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const obtenerDatos = async () => {
            try{
                const response = await fetch('/api/citas/');
                const datos = await response.json();
                setCitas(datos);
                setLoading(false);
            } catch (error){
                console.log(error);
            } finally {
                setLoading(false);
            }
            
        }

        obtenerDatos();

    }, []);


    return (
        <div>
            <h2>
                Mis Citas
            </h2>
            <div>
                {loading ? (
                    <p>Cargando...</p>
                ) : (
                    citas.map((cita)=>{
                        return (
                            <p key={cita.id}>{cita.fecha}</p>
                        )
                    })
                )}
            </div>
        </div>
    )
}

export default ListaCitas;
