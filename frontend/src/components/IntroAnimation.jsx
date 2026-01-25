import { useEffect, useState } from "react";
import Lottie from "lottie-react";


const IntroAnimation = ({onComplete}) => {
    const [animationData, setAnimationData] = useState(null);

    useEffect(()=>{
        fetch(`${import.meta.env.BASE_URL}Business%20Analysis.json`) 
        .then((response) => response.json())
        .then((data) => setAnimationData(data))
        .catch((error) => console.error("Error cargando la animación", error))
    },[]);

    if (!animationData) {
        return null;
    }
  
    return (
    <div style={styles.container}>
      <Lottie
        animationData={animationData}
        loop={false}
        onComplete={onComplete} 
        style={styles.animation}
      />
    </div>
  );
};

const styles = {
  container: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    backgroundColor: "#a4d3f8", 
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 9999, 
  },
  animation: {
    width: "80%", 
    maxWidth: "500px",
  },
};

export default IntroAnimation;