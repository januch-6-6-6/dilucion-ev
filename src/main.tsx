import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { registerSW } from 'virtual:pwa-register'
import App from './app/App.tsx'
import { vigilarActualizaciones } from './app/actualizacion'
import { aplicarTema, leerTema } from './app/tema'
import './index.css'

aplicarTema(leerTema())

registerSW({
  immediate: true,
  onRegisteredSW(_url, registro) {
    if (registro) vigilarActualizaciones(registro)
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
