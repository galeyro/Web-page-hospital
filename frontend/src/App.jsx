import { useState } from 'react'
import './App.css'
import IntroAnimation from './components/IntroAnimation'
import BackgroundAnimation from './components/BackgroundAnimation'
import Scheduler from './components/SchedulerBoard'

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
            <Scheduler />
          </div>
        </>
      )}
    </>
  )
}
export default App
