import { describe, expect, it } from 'vitest'
import { fichaValida } from '../esquema/__fixtures__/fichas'
import type { Ficha } from '../esquema/ficha'
import { buscar } from './buscar'

const lista = [
  { ...fichaValida('noradrenalina'), nombre: 'Noradrenalina', comerciales: ['Levophed'] },
  { ...fichaValida('adrenalina'), nombre: 'Adrenalina' },
  { ...fichaValida('amiodarona'), nombre: 'Amiodarona' },
] as Ficha[]

const ids = (texto: string) => buscar(texto, lista).map((f) => f.id)

describe('buscar', () => {
  it('por prefijo', () => expect(ids('nora')[0]).toBe('noradrenalina'))
  it('por nombre comercial, sin importar mayúsculas', () => expect(ids('LEVOPHED')[0]).toBe('noradrenalina'))
  it('sin importar tildes', () => expect(ids('adrenalína')[0]).toBe('adrenalina'))
  it('tolera errores de tipeo', () => expect(ids('noradrenalia')[0]).toBe('noradrenalina'))
  it('prefijo antes que substring', () => expect(ids('adrenalina')).toEqual(['adrenalina', 'noradrenalina']))
  it('texto vacío no devuelve nada', () => expect(ids('')).toEqual([]))
  it('sin coincidencias', () => expect(ids('xyz')).toEqual([]))
})
