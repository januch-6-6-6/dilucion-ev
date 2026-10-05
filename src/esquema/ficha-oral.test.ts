import { describe, expect, it } from 'vitest'
import { FichaOral } from './ficha-oral'
import { fichaOralValida } from './__fixtures__/orales'

const f = { ref: 'F1', detalle: 'p. 1' }
const base = fichaOralValida()
const pres = base.presentaciones[0]
const dosisAdulto = base.dosis[0]
const dosisPed = base.dosis[1]

function rutas(r: ReturnType<typeof FichaOral.safeParse>) {
  return r.success ? [] : r.error.issues.map((i) => i.path.join('.'))
}

describe('FichaOral', () => {
  it('acepta una ficha válida', () => {
    expect(FichaOral.safeParse(fichaOralValida()).success).toBe(true)
  })

  it('rechaza un campo desconocido', () => {
    expect(FichaOral.safeParse(fichaOralValida('x', { extra: 1 })).success).toBe(false)
  })

  it('una presentación líquida sin concentración falla', () => {
    const { concentracion: _c, ...sinConc } = base.presentaciones[1] as Record<string, unknown>
    const r = FichaOral.safeParse(fichaOralValida('x', { presentaciones: [sinConc] }))
    expect(r.success).toBe(false)
    expect(rutas(r).some((p) => p.startsWith('presentaciones.0'))).toBe(true)
  })

  it('una presentación sólida sin cantidad falla', () => {
    const { cantidad: _c, ...sinCant } = pres as Record<string, unknown>
    const r = FichaOral.safeParse(fichaOralValida('x', { presentaciones: [sinCant] }))
    expect(rutas(r).some((p) => p.startsWith('presentaciones.0'))).toBe(true)
  })

  it('gotas exige gotasPorMl', () => {
    const gotas = { ...base.presentaciones[1], id: 'gotas', forma: 'gotas' }
    const r = FichaOral.safeParse(fichaOralValida('x', { presentaciones: [gotas] }))
    expect(r.success).toBe(false)
    expect(rutas(r).some((p) => p.startsWith('presentaciones.0'))).toBe(true)
    const ok = FichaOral.safeParse(fichaOralValida('x', { presentaciones: [{ ...gotas, gotasPorMl: 20 }] }))
    expect(ok.success).toBe(true)
  })

  it('por_edad y por_superficie exigen texto', () => {
    for (const regimen of ['por_edad', 'por_superficie']) {
      const d = { ...dosisAdulto, regimen }
      expect(FichaOral.safeParse(fichaOralValida('x', { dosis: [d, dosisPed] })).success).toBe(false)
      expect(FichaOral.safeParse(fichaOralValida('x', { dosis: [{ ...d, texto: 'según tabla' }, dosisPed] })).success).toBe(true)
    }
  })

  it('por_peso exige base y unidad por kg', () => {
    const { base: _b, ...sinBase } = dosisPed as Record<string, unknown>
    expect(FichaOral.safeParse(fichaOralValida('x', { dosis: [dosisAdulto, sinBase] })).success).toBe(false)
    expect(FichaOral.safeParse(fichaOralValida('x', { dosis: [dosisAdulto, { ...dosisPed, unidad: 'mg' }] })).success).toBe(false)
  })

  it('solo_adulto exige motivo', () => {
    const r = FichaOral.safeParse(fichaOralValida('x', { dosis: [dosisAdulto], pediatria: { estado: 'solo_adulto' } }))
    expect(r.success).toBe(false)
    expect(FichaOral.safeParse(fichaOralValida('x', { dosis: [dosisAdulto], pediatria: { estado: 'solo_adulto', motivo: 'No autorizado' } })).success).toBe(true)
  })

  it('la dosis pediátrica con pediatria solo_adulto falla', () => {
    const r = FichaOral.safeParse(fichaOralValida('x', { pediatria: { estado: 'solo_adulto', motivo: 'No autorizado' } }))
    expect(r.success).toBe(false)
  })

  it('con_dosis exige al menos una dosis pediátrica', () => {
    expect(FichaOral.safeParse(fichaOralValida('x', { dosis: [dosisAdulto] })).success).toBe(false)
  })

  it('id con prefijo oral: falla', () => {
    expect(FichaOral.safeParse(fichaOralValida('oral:paracetamol')).success).toBe(false)
  })

  it('ajusteRenalHepatico acepta un objeto con fuente', () => {
    expect(FichaOral.safeParse(fichaOralValida('x', { ajusteRenalHepatico: { renal: 'Reducir', fuente: f } })).success).toBe(true)
  })
})
