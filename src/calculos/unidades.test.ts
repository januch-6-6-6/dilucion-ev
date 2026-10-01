import { describe, expect, it } from 'vitest'
import { convertirMasa, parsearUnidadDosis } from './unidades'

describe('convertirMasa', () => {
  it('convierte mg a mcg', () => expect(convertirMasa(1, 'mg', 'mcg')).toBe(1000))
  it('convierte mcg a mg', () => expect(convertirMasa(2500, 'mcg', 'mg')).toBe(2.5))
  it('convierte g a mg', () => expect(convertirMasa(1, 'g', 'mg')).toBe(1000))
  it('deja UI igual', () => expect(convertirMasa(5, 'UI', 'UI')).toBe(5))
  it('deja mEq igual', () => expect(convertirMasa(10, 'mEq', 'mEq')).toBe(10))
  it('no mezcla mEq con masa', () => expect(() => convertirMasa(1, 'mEq', 'mg')).toThrow())
  it('no mezcla mmol con mEq', () => expect(() => convertirMasa(1, 'mmol', 'mEq')).toThrow())
  it('no mezcla UI con masa', () =>
    expect(() => convertirMasa(1, 'UI', 'mg')).toThrow('No se puede convertir UI a unidades de masa'))
})


describe('parsearUnidadDosis', () => {
  it('mcg/kg/min', () => expect(parsearUnidadDosis('mcg/kg/min')).toEqual({ masa: 'mcg', porKg: true, tiempo: 'min' }))
  it('mg/kg/h', () => expect(parsearUnidadDosis('mg/kg/h')).toEqual({ masa: 'mg', porKg: true, tiempo: 'h' }))
  it('mg/kg', () => expect(parsearUnidadDosis('mg/kg')).toEqual({ masa: 'mg', porKg: true, tiempo: null }))
  it('mcg/min', () => expect(parsearUnidadDosis('mcg/min')).toEqual({ masa: 'mcg', porKg: false, tiempo: 'min' }))
  it('g/h', () => expect(parsearUnidadDosis('g/h')).toEqual({ masa: 'g', porKg: false, tiempo: 'h' }))
  it('mg', () => expect(parsearUnidadDosis('mg')).toEqual({ masa: 'mg', porKg: false, tiempo: null }))
  it('mEq/h', () => expect(parsearUnidadDosis('mEq/h')).toEqual({ masa: 'mEq', porKg: false, tiempo: 'h' }))
  it('mEq/kg', () => expect(parsearUnidadDosis('mEq/kg')).toEqual({ masa: 'mEq', porKg: true, tiempo: null }))
  it('mmol/kg/h', () => expect(parsearUnidadDosis('mmol/kg/h')).toEqual({ masa: 'mmol', porKg: true, tiempo: 'h' }))
  it('mg/24 h no se interpreta', () => expect(parsearUnidadDosis('mg/24 h')).toBeNull())
})
