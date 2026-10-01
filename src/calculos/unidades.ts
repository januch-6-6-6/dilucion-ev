export type UnidadMasa = 'g' | 'mg' | 'mcg' | 'UI'
export type Cantidad = { valor: number; unidad: UnidadMasa }

const MCG_POR_UNIDAD: Record<Exclude<UnidadMasa, 'UI'>, number> = { g: 1_000_000, mg: 1000, mcg: 1 }

export function convertirMasa(valor: number, de: UnidadMasa, a: UnidadMasa): number {
  if (de === a) return valor
  if (de === 'UI' || a === 'UI') throw new Error('No se puede convertir UI a unidades de masa')
  return (valor * MCG_POR_UNIDAD[de]) / MCG_POR_UNIDAD[a]
}
