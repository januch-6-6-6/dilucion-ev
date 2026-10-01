import { describe, expect, it } from 'vitest'
import { convertirMasa } from './unidades'

describe('convertirMasa', () => {
  it('convierte mg a mcg', () => expect(convertirMasa(1, 'mg', 'mcg')).toBe(1000))
  it('convierte mcg a mg', () => expect(convertirMasa(2500, 'mcg', 'mg')).toBe(2.5))
  it('convierte g a mg', () => expect(convertirMasa(1, 'g', 'mg')).toBe(1000))
  it('deja UI igual', () => expect(convertirMasa(5, 'UI', 'UI')).toBe(5))
  it('no mezcla UI con masa', () =>
    expect(() => convertirMasa(1, 'UI', 'mg')).toThrow('No se puede convertir UI a unidades de masa'))
})
