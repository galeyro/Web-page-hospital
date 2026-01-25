import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ListaCitas from './ListaCitas'
import IntroAnimation from './components/IntroAnimation'
import BackgroundAnimation from './components/BackgroundAnimation'

function App() {
  const [showIntro, setShowIntro]=useState(true);

  return (
    <>
      {showIntro ? (
        <IntroAnimation onComplete={()=>setShowIntro(false)} />
      ) : (
        <>
          <BackgroundAnimation />
          <div>
            <a href="https://vite.dev" target="_blank">
              <img src={viteLogo} className="logo" alt="Vite logo" />
            </a>
            <a href="https://react.dev" target="_blank">
              <img src={reactLogo} className="logo react" alt="React logo" />
            </a>
          </div>
          <h1>Vite + React</h1>
          <ListaCitas />
        </>
      )}
    </>
  )
}
export default App
