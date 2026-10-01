export type UnidadMasa = 'g' | 'mg' | 'mcg' | 'UI'
export type Cantidad = { valor: number; unidad: UnidadMasa }

const MCG_POR_UNIDAD: Record<Exclude<UnidadMasa, 'UI'>, number> = { g: 1_000_000, mg: 1000, mcg: 1 }

export function convertirMasa(valor: number, de: UnidadMasa, a: UnidadMasa): number {
  if (de === a) return valor
  if (de === 'UI' || a === 'UI') throw new Error('No se puede convertir UI a unidades de masa')
  return (valor * MCG_POR_UNIDAD[de]) / MCG_POR_UNIDAD[a]
}

export type UnidadDosis = { masa: UnidadMasa; porKg: boolean; tiempo: 'min' | 'h' | null }

/** Interpreta unidades de dosis como "mcg/kg/min", "mg/kg", "g/h" o "mg". Devuelve null si no la reconoce. */
export function parsearUnidadDosis(unidad: string): UnidadDosis | null {
  const m = /^(g|mg|mcg|UI)(\/kg)?(?:\/(min|h))?$/.exec(unidad.replace(/\s+/g, ''))
  if (!m) return null
  return { masa: m[1] as UnidadMasa, porKg: Boolean(m[2]), tiempo: (m[3] as 'min' | 'h' | undefined) ?? null }
}
