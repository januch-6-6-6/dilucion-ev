import { describe, expect, it } from 'vitest'
import type { PresentacionOral } from '../esquema/ficha-oral'
import { masaAGotas, masaAMl, masaAUnidades, mlAMasa } from './oralConversion'

const base = {
  liberacionProlongada: false,
  registroChile: 'sin_verificar',
  fuente: { id: 'x' },
} as unknown as Partial<PresentacionOral>
const pres = (p: Partial<PresentacionOral>) => ({ id: 'p', partible: 'no', ...base, ...p }) as PresentacionOral

const lactulosa = pres({ forma: 'jarabe', concentracion: { valor: 667, unidad: 'mg' } })
const paracetamol = pres({ forma: 'jarabe', concentracion: { valor: 100, unidad: 'mg' } })
const haloperidol = pres({ forma: 'gotas', concentracion: { valor: 2, unidad: 'mg' }, gotasPorMl: 20 })
const comp = (valor: number, partible: PresentacionOral['partible']) =>
  pres({ forma: 'comprimido', cantidad: { valor, unidad: 'mg' }, partible })

describe('masaAMl', () => {
  it('lactulosa: 10 g con 667 mg/ml → 15 ml', () => {
    const r = masaAMl({ valor: 10, unidad: 'g' }, lactulosa)
    expect(r.ok && r.valor).toBeCloseTo(15, 1)
  })
  it('paracetamol infantil: 150 mg con 100 mg/ml → 1,5 ml', () => {
    const r = masaAMl({ valor: 150, unidad: 'mg' }, paracetamol)
    expect(r).toMatchObject({ ok: true, valor: 1.5 })
  })
  it.each([undefined, 0, NaN])('concentración %s → error', (v) => {
    const p = pres({ forma: 'jarabe', concentracion: v === undefined ? undefined : { valor: v, unidad: 'mg' } })
    expect(masaAMl({ valor: 1, unidad: 'mg' }, p)).toEqual({ ok: false, error: 'Falta la concentración' })
  })
})

describe('mlAMasa', () => {
  it('1,5 ml de 100 mg/ml → 150 mg', () => {
    expect(mlAMasa(1.5, paracetamol)).toMatchObject({ ok: true, valor: { valor: 150, unidad: 'mg' } })
  })
  it('sin concentración → error', () => {
    expect(mlAMasa(1, pres({ forma: 'jarabe' }))).toEqual({ ok: false, error: 'Falta la concentración' })
  })
})

describe('masaAGotas', () => {
  it('haloperidol: 0,5 mg con 2 mg/ml y 20 gotas/ml → 5 gotas', () => {
    expect(masaAGotas({ valor: 0.5, unidad: 'mg' }, haloperidol)).toMatchObject({ ok: true, valor: 5 })
  })
  it('redondea hacia abajo', () => {
    expect(masaAGotas({ valor: 0.59, unidad: 'mg' }, haloperidol)).toMatchObject({ ok: true, valor: 5 })
  })
  it('sin gotasPorMl → error', () => {
    const r = masaAGotas({ valor: 1, unidad: 'mg' }, paracetamol)
    expect(r.ok).toBe(false)
    if (!r.ok) expect(r.error).toMatch(/gotas por ml/i)
  })
})

describe('masaAUnidades', () => {
  it('2 mg con comprimido de 4 mg no partible → error', () => {
    expect(masaAUnidades({ valor: 2, unidad: 'mg' }, comp(4, 'no'))).toEqual({
      ok: false,
      error: 'Esta presentación no permite esa dosis',
    })
  })
  it('2 mg con comprimido de 4 mg en mitades → 0,5 unidades, 100 %', () => {
    const r = masaAUnidades({ valor: 2, unidad: 'mg' }, comp(4, 'mitades'))
    expect(r).toMatchObject({ ok: true, valor: { unidades: 0.5, entregado: { valor: 2, unidad: 'mg' }, porcentaje: 1 } })
  })
  it('2 g con comprimidos de 500 mg → 4 unidades', () => {
    const r = masaAUnidades({ valor: 2, unidad: 'g' }, comp(500, 'no'))
    expect(r).toMatchObject({ ok: true, valor: { unidades: 4, porcentaje: 1 } })
  })
  it('nunca excede la dosis y informa el porcentaje', () => {
    const r = masaAUnidades({ valor: 3, unidad: 'mg' }, comp(4, 'mitades'))
    expect(r).toMatchObject({ ok: true, valor: { unidades: 0.5, porcentaje: 0.6667 } })
  })
})
