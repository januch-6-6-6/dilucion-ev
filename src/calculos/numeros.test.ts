import { describe, expect, it } from 'vitest'
import { parsearNumero } from './numeros'

describe('parsearNumero', () => {
  it('acepta coma decimal', () => expect(parsearNumero('70,5')).toBe(70.5))
  it('ignora espacios', () => expect(parsearNumero(' 70 ')).toBe(70))
  it('vacío es null', () => expect(parsearNumero('')).toBeNull())
  it('texto es null', () => expect(parsearNumero('abc')).toBeNull())
  it('cero es null', () => expect(parsearNumero('0')).toBeNull())
  it('punto como separador de miles (1.000)', () => expect(parsearNumero('1.000')).toBe(1000))
  it('miles y decimales a la chilena (1.000,5)', () => expect(parsearNumero('1.000,5')).toBe(1000.5))
  it('punto decimal simple sigue funcionando (1.5)', () => expect(parsearNumero('1.5')).toBe(1.5))
  it('negativo es null', () => expect(parsearNumero('-3')).toBeNull())
})
