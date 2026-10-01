import { describe, expect, it } from 'vitest'
import { alertaConcentracion, alertaDosis, alertaTiempo } from './alertas'

describe('alertaConcentracion', () => {
  it('avisa si supera la máxima', () => {
    const a = alertaConcentracion({ valor: 64, unidad: 'mcg' }, { valor: 32, unidad: 'mcg' })
    expect(a).toHaveLength(1)
    expect(a[0].mensaje).toContain('supera la concentración máxima')
  })
  it('no avisa dentro del rango', () => expect(alertaConcentracion({ valor: 16, unidad: 'mcg' }, { valor: 32, unidad: 'mcg' })).toEqual([]))
  it('compara en la misma unidad', () => expect(alertaConcentracion({ valor: 0.064, unidad: 'mg' }, { valor: 32, unidad: 'mcg' })).toHaveLength(1))
  it('sin máximo no avisa', () => expect(alertaConcentracion({ valor: 64, unidad: 'mcg' })).toEqual([]))
})

describe('alertaDosis', () => {
  it('sobre la máxima', () => expect(alertaDosis(3, 'mcg/kg/min', { max: 1 })[0].mensaje).toContain('supera la dosis máxima'))
  it('bajo la mínima', () => expect(alertaDosis(0.01, 'mcg/kg/min', { min: 0.05 })[0].mensaje).toContain('bajo la dosis mínima'))
  it('sobre la máxima absoluta', () => expect(alertaDosis(500, 'mg', { maximaAbsoluta: 450 })[0].mensaje).toContain('supera la dosis máxima'))
  it('sin rango no avisa', () => expect(alertaDosis(3, 'mg', {})).toEqual([]))
})

describe('alertaTiempo', () => {
  it('más rápido que lo recomendado', () => expect(alertaTiempo(10, 30)[0].mensaje).toContain('más rápido que lo recomendado'))
  it('igual al mínimo no avisa', () => expect(alertaTiempo(30, 30)).toEqual([]))
  it('sin mínimo no avisa', () => expect(alertaTiempo(1)).toEqual([]))
})
