import { describe, expect, it } from 'vitest'
import { parsearNumero } from './numeros'

describe('parsearNumero', () => {
  it('acepta coma decimal', () => expect(parsearNumero('70,5')).toBe(70.5))
  it('ignora espacios', () => expect(parsearNumero(' 70 ')).toBe(70))
  it('vacío es null', () => expect(parsearNumero('')).toBeNull())
  it('texto es null', () => expect(parsearNumero('abc')).toBeNull())
  it('cero es null', () => expect(parsearNumero('0')).toBeNull())
  it('negativo es null', () => expect(parsearNumero('-3')).toBeNull())
})
