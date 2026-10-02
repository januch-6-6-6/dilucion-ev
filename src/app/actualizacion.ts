/** Cada cuánto, como mínimo, se busca una versión nueva al volver a la app (un par de veces al día). */
export const INTERVALO_MS = 6 * 60 * 60 * 1000

export const debeRevisar = (ahora: number, ultima: number | null, intervalo = INTERVALO_MS): boolean =>
  ultima === null || ahora - ultima >= intervalo

/**
 * Una app instalada en Android suele quedar en segundo plano y no se recarga al reabrirla,
 * así que no busca versiones nuevas. Al volver a primer plano, si pasaron 6 h desde la última
 * búsqueda (o desde que se cargó), se le pide al service worker que revise. Devuelve cómo dejar de vigilar.
 */
export function vigilarActualizaciones(registro: { update: () => Promise<unknown> }, reloj: () => number = Date.now): () => void {
  let ultima = reloj() // al cargar, el navegador ya revisa por su cuenta
  const alVolver = () => {
    if (document.visibilityState !== 'visible' || !navigator.onLine) return
    if (!debeRevisar(reloj(), ultima)) return
    ultima = reloj()
    registro.update().catch(() => {
      /* sin red o servidor caído: se reintenta en la próxima ventana */
    })
  }
  document.addEventListener('visibilitychange', alVolver)
  return () => document.removeEventListener('visibilitychange', alVolver)
}
