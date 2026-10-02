const CLAVE = 'dilucion-ev:favoritos'

/** Ids de medicamentos marcados con estrella, en el orden en que se marcaron. Solo en este dispositivo. */
export function leerFavoritos(): string[] {
  try {
    const crudo = localStorage.getItem(CLAVE)
    const lista: unknown = crudo ? JSON.parse(crudo) : []
    return Array.isArray(lista) ? lista.filter((x): x is string => typeof x === 'string') : []
  } catch {
    return []
  }
}

export const esFavorito = (id: string): boolean => leerFavoritos().includes(id)

/** Marca o desmarca un medicamento. Tolera localStorage bloqueado. */
export function alternarFavorito(id: string): void {
  try {
    const lista = leerFavoritos()
    const nueva = lista.includes(id) ? lista.filter((x) => x !== id) : [...lista, id]
    localStorage.setItem(CLAVE, JSON.stringify(nueva))
  } catch {
    /* sin almacenamiento: se ignora */
  }
}
