export type Tema = 'claro' | 'oscuro' | 'sistema'
const CLAVE = 'dilucion-ev:tema'

export function aplicarTema(tema: Tema): void {
  if (tema === 'sistema') document.documentElement.removeAttribute('data-theme')
  else document.documentElement.setAttribute('data-theme', tema)
  try {
    localStorage.setItem(CLAVE, tema)
  } catch {
    /* ignorar */
  }
}

export function leerTema(): Tema {
  try {
    const t = localStorage.getItem(CLAVE)
    return t === 'claro' || t === 'oscuro' ? t : 'sistema'
  } catch {
    return 'sistema'
  }
}
