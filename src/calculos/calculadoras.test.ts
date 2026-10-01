import { describe, expect, it } from 'vitest'
import {
  concentracion,
  dosisAVelocidad,
  dosisPediatrica,
  velocidadADosis,
  velocidadPorDosis,
  velocidadPorTiempo,
  volumenACargar,
  type Resultado,
} from './calculadoras'

function valor<T>(r: Resultado<T>): T {
  if (!r.ok) throw new Error(`se esperaba ok, vino error: ${r.error}`)
  expect(r.pasos[0]).toBeTruthy()
  return r.valor
}

describe('concentracion', () => {
  it('noradrenalina 4 mg en 250 ml = 16 mcg/ml', () =>
    expect(valor(concentracion({ valor: 4, unidad: 'mg' }, 250, 'mcg'))).toBe(16))
})

describe('volumenACargar', () => {
  it('amiodarona 300 mg con ampollas 150 mg/3 ml = 6 ml, 2 ampollas', () =>
    expect(valor(volumenACargar({ valor: 300, unidad: 'mg' }, { cantidad: { valor: 150, unidad: 'mg' }, volumenMl: 3 }))).toEqual({ ml: 6, unidades: 2 }))
  it('adrenalina 1 mg con ampolla 1 mg/1 ml = 1 ml, 1 ampolla', () =>
    expect(valor(volumenACargar({ valor: 1, unidad: 'mg' }, { cantidad: { valor: 1, unidad: 'mg' }, volumenMl: 1 }))).toEqual({ ml: 1, unidades: 1 }))
})

describe('velocidadPorTiempo', () => {
  it('100 ml en 30 min', () => expect(valor(velocidadPorTiempo(100, 30))).toEqual({ mlh: 200, gotasMacro: 67, gotasMicro: 200 }))
  it('500 ml en 8 h', () => expect(valor(velocidadPorTiempo(500, 480))).toEqual({ mlh: 62.5, gotasMacro: 21, gotasMicro: 63 }))
})

describe('velocidadPorDosis', () => {
  it('fentanilo 100 mcg/h a 10 mcg/ml = 10 ml/h', () =>
    expect(valor(velocidadPorDosis({ valor: 100, unidad: 'mcg' }, { valor: 10, unidad: 'mcg' }))).toBe(10))
  it('no mezcla UI con mg', () =>
    expect(velocidadPorDosis({ valor: 2, unidad: 'UI' }, { valor: 1, unidad: 'mg' })).toEqual({ ok: false, error: 'No se puede convertir UI a unidades de masa' }))
})

describe('dosisAVelocidad', () => {
  it('noradrenalina 0,1 mcg/kg/min, 70 kg, 16 mcg/ml = 26,3 ml/h', () =>
    expect(valor(dosisAVelocidad({ pesoKg: 70, dosis: { valor: 0.1, unidad: 'mcg', tiempo: 'min' }, concentracionPorMl: { valor: 16, unidad: 'mcg' } }))).toBe(26.3))
  it('redondeo half-up sin ruido acumulado: 0,15 mcg/kg/min, 46 kg, 40 mcg/ml = 10,4 ml/h', () =>
    expect(valor(dosisAVelocidad({ pesoKg: 46, dosis: { valor: 0.15, unidad: 'mcg', tiempo: 'min' }, concentracionPorMl: { valor: 40, unidad: 'mcg' } }))).toBe(10.4))
  it('midazolam 0,05 mg/kg/h, 80 kg, 1 mg/ml = 4 ml/h', () =>
    expect(valor(dosisAVelocidad({ pesoKg: 80, dosis: { valor: 0.05, unidad: 'mg', tiempo: 'h' }, concentracionPorMl: { valor: 1, unidad: 'mg' } }))).toBe(4))
  it('sin peso dice qué falta', () =>
    expect(dosisAVelocidad({ pesoKg: 0, dosis: { valor: 0.1, unidad: 'mcg', tiempo: 'min' }, concentracionPorMl: { valor: 16, unidad: 'mcg' } })).toEqual({ ok: false, error: 'Falta el peso' }))
})

describe('unidades no convertibles', () => {
  it('heparina 18 UI/kg/h, 70 kg, 100 UI/ml = 12,6 ml/h', () =>
    expect(valor(dosisAVelocidad({ pesoKg: 70, dosis: { valor: 18, unidad: 'UI', tiempo: 'h' }, concentracionPorMl: { valor: 100, unidad: 'UI' } }))).toBe(12.6))
  it('potasio 10 mEq/h a 0,2 mEq/ml = 50 ml/h', () =>
    expect(valor(velocidadPorDosis({ valor: 10, unidad: 'mEq' }, { valor: 0.2, unidad: 'mEq' }))).toBe(50))
  it('mEq contra mg da error explícito', () =>
    expect(velocidadPorDosis({ valor: 10, unidad: 'mEq' }, { valor: 1, unidad: 'mg' })).toMatchObject({ ok: false }))
})

describe('velocidadADosis', () => {
  it('26,25 ml/h de 16 mcg/ml en 70 kg = 0,1 mcg/kg/min', () =>
    expect(valor(velocidadADosis({ pesoKg: 70, mlh: 26.25, concentracionPorMl: { valor: 16, unidad: 'mcg' }, unidadSalida: 'mcg', tiempo: 'min' }))).toBe(0.1))
})

describe('dosisPediatrica', () => {
  it('0,01 mg/kg en 20 kg = 0,2 mg', () =>
    expect(valor(dosisPediatrica({ pesoKg: 20, dosisPorKg: { valor: 0.01, unidad: 'mg' }, topeAdulto: { valor: 1, unidad: 'mg' } }))).toEqual({ dosis: { valor: 0.2, unidad: 'mg' }, limitada: false }))
  it('sobre el tope se limita a la dosis de adulto', () =>
    expect(valor(dosisPediatrica({ pesoKg: 150, dosisPorKg: { valor: 0.01, unidad: 'mg' }, topeAdulto: { valor: 1, unidad: 'mg' } }))).toEqual({ dosis: { valor: 1, unidad: 'mg' }, limitada: true }))
})
