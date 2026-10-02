import { describe, expect, it } from 'vitest'
import { convertirMasa, parsearUnidadDosis } from '../calculos/unidades'
import { medicamentos, obtenerFicha } from './cargar'

const porMl = (c: { valor: number; unidad: string }, ml: number, a: string) =>
  convertirMasa(c.valor, c.unidad as never, a as never) / ml

describe('coherencia interna de las fichas', () => {
  it('cada dilución estándar respeta la concentración mínima y máxima de su propia ficha', () => {
    const fuera: string[] = []
    for (const f of medicamentos) {
      const { concentracionMin: min, concentracionMax: max, estandar } = f.dilucion
      for (const e of estandar) {
        if (max && porMl(e.cantidad, e.volumenFinalMl, max.unidad) > max.valor + 1e-9) fuera.push(`${f.id}: ${e.descripcion} > máx`)
        if (min && porMl(e.cantidad, e.volumenFinalMl, min.unidad) < min.valor - 1e-9) fuera.push(`${f.id}: ${e.descripcion} < mín`)
      }
    }
    expect(fuera).toEqual([])
  })

  it('ningún suero indicado para diluir figura como incompatible en la tabla de compatibilidad', () => {
    const malos: string[] = []
    for (const f of medicamentos)
      for (const s of f.dilucion.sueros)
        if (f.compatibilidad.find((c) => c.con === s)?.estado === 'incompatible') malos.push(`${f.id}–${s}`)
    expect(malos).toEqual([])
  })

  it('las dosis con unidad de masa usan una unidad convertible con la presentación', () => {
    const malos: string[] = []
    for (const f of medicamentos) {
      const base = f.presentaciones[0].cantidad.unidad
      for (const d of f.dosis) {
        const m = parsearUnidadDosis(d.unidad)?.masa ?? /^(g|mg|mcg|UI|mEq|mmol)/.exec(d.unidad)?.[1]
        if (!m) continue
        try { convertirMasa(1, m as never, base) } catch { malos.push(`${f.id}: ${d.unidad} vs ${base}`) }
      }
    }
    expect(malos).toEqual([])
  })

  it('octreótido: la dosis en várices es la de CIMA 4.2 (25 mcg/h)', () => {
    const d = obtenerFicha('octreotido')!.dosis[0]
    expect(d.min).toBe(25)
    expect(d.fuente.detalle).toContain('4.2')
  })

  it('meropenem pediátrico separa la pauta habitual de la de meningitis', () => {
    const ped = obtenerFicha('meropenem')!.dosis.filter((d) => d.poblacion === 'pediatrico')
    expect(ped[0].max).toBe(20)
    expect(ped.some((d) => /meningitis/i.test(d.indicacion) && d.max === 40)).toBe(true)
  })
})
