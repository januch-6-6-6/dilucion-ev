import { afterEach, describe, expect, it, vi } from 'vitest'
import { alternarFavorito, esFavorito, leerFavoritos } from './favoritos'

afterEach(() => vi.restoreAllMocks())

describe('favoritos', () => {
  it('sin favoritos devuelve lista vacía', () => expect(leerFavoritos()).toEqual([]))

  it('alternar agrega y quita, sin repetir', () => {
    alternarFavorito('atropina')
    alternarFavorito('adrenalina')
    expect(leerFavoritos()).toEqual(['atropina', 'adrenalina'])
    expect(esFavorito('atropina')).toBe(true)
    alternarFavorito('atropina')
    expect(leerFavoritos()).toEqual(['adrenalina'])
    expect(esFavorito('atropina')).toBe(false)
  })

  it('ignora datos corruptos en el almacenamiento', () => {
    localStorage.setItem('dilucion-ev:favoritos', '{"no":"lista"}')
    expect(leerFavoritos()).toEqual([])
    localStorage.setItem('dilucion-ev:favoritos', '[1, "atropina", null]')
    expect(leerFavoritos()).toEqual(['atropina'])
  })

  it('con el almacenamiento bloqueado no falla', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('bloqueado')
    })
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('bloqueado')
    })
    expect(leerFavoritos()).toEqual([])
    expect(() => alternarFavorito('atropina')).not.toThrow()
  })
})
