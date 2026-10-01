const CLAVE = 'dilucion-ev:recientes'
const MAXIMO = 8

/** Solo guarda ids de medicamentos (nunca datos de pacientes). Tolera localStorage bloqueado. */
export function leerRecientes(): string[] {
  try {
    const crudo = localStorage.getItem(CLAVE)
    const lista: unknown = crudo ? JSON.parse(crudo) : []
    return Array.isArray(lista) ? lista.filter((x): x is string => typeof x === 'string') : []
  } catch {
    return []
  }
}

export function registrarReciente(id: string): void {
  try {
    const lista = [id, ...leerRecientes().filter((x) => x !== id)].slice(0, MAXIMO)
    localStorage.setItem(CLAVE, JSON.stringify(lista))
  } catch {
    /* sin almacenamiento: se ignora */
  }
}
