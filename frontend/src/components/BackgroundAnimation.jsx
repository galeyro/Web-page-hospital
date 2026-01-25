import { useEffect, useState } from "react";
import Lottie from "lottie-react";

const BackgroundAnimation = () => {
    const [animationData, setAnimationData] = useState(null);

    useEffect(()=>{
        fetch(`${import.meta.env.BASE_URL}Fog%20Background%20Decoration.json`)
        .then((response)=>response.json()) 
        .then((data)=>setAnimationData(data))
        .catch((error)=>console.error("Error cargando la animación", error))
    },[]);

    if (!animationData) {
        return null;
    }

    return (
        <div style={styles.container}>
            <Lottie animationData={animationData} loop style={styles.animation}/>
        </div>
    )
};

const styles = {
  container: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundColor: "#ffffffff", 
    zIndex: -1,
    overflow: "hidden",
    pointerEvents: "none",
  },
  animation: {
    width: "100%",
    height: "100%",
    opacity: 0.5,
  },
};
export default BackgroundAnimation;