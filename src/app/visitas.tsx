import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'

declare global {
  interface Window {
    goatcounter?: { count?: (datos: { path: string }) => void; path?: () => string; no_onload?: boolean }
  }
}

/**
 * Cuenta visitas anónimas con GoatCounter (sin cookies ni datos personales).
 * El script de index.html cuenta la primera pantalla al cargar; la app usa HashRouter,
 * así que cada navegación posterior se informa aquí con la ruta del hash.
 */
export default function ContadorVisitas() {
  const { pathname } = useLocation()
  const primera = useRef(true)
  useEffect(() => {
    if (primera.current) {
      primera.current = false
      return
    }
    window.goatcounter?.count?.({ path: pathname })
  }, [pathname])
  return null
}
