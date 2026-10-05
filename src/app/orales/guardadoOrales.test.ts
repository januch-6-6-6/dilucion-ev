import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { alternarFavorito, esFavorito } from '../favoritos'
import { registrarReciente, leerRecientes } from '../recientes'
import {
  alternarFavoritoOral,
  esFavoritoOral,
  leerFavoritosOrales,
  leerRecientesOrales,
  registrarRecienteOral,
} from './guardadoOrales'

beforeEach(() => localStorage.clear())
afterEach(() => vi.restoreAllMocks())

describe('guardadoOrales', () => {
  it('favorito oral no marca el EV con el mismo id, y viceversa', () => {
    alternarFavoritoOral('ketorolaco')
    expect(esFavoritoOral('ketorolaco')).toBe(true)
    expect(esFavorito('ketorolaco')).toBe(false)
    expect(leerFavoritosOrales()).toEqual(['ketorolaco'])
    localStorage.clear()
    alternarFavorito('ketorolaco')
    expect(esFavorito('ketorolaco')).toBe(true)
    expect(esFavoritoOral('ketorolaco')).toBe(false)
    expect(leerFavoritosOrales()).toEqual([])
  })
  it('alternar dos veces desmarca y conserva los EV', () => {
    alternarFavorito('adrenalina')
    alternarFavoritoOral('x')
    alternarFavoritoOral('x')
    expect(leerFavoritosOrales()).toEqual([])
    expect(esFavorito('adrenalina')).toBe(true)
  })
  it('recientes orales y EV no se pisan', () => {
    registrarReciente('adrenalina')
    registrarRecienteOral('paracetamol')
    registrarRecienteOral('ibuprofeno')
    registrarRecienteOral('paracetamol')
    expect(leerRecientesOrales()).toEqual(['paracetamol', 'ibuprofeno'])
    expect(leerRecientes()).toContain('adrenalina')
    expect(leerRecientes().filter((x) => !x.startsWith('oral:'))).toEqual(['adrenalina'])
  })
  it('con localStorage bloqueado no lanza y devuelve []', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('bloqueado')
    })
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('bloqueado')
    })
    expect(leerFavoritosOrales()).toEqual([])
    expect(leerRecientesOrales()).toEqual([])
    expect(() => alternarFavoritoOral('a')).not.toThrow()
    expect(() => registrarRecienteOral('a')).not.toThrow()
  })
})
