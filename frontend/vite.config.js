import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Base path para que los assets carguen bien desde Django
  base: '/static/', 
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: 'app.html'
    }
  }
})