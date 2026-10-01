import { describe, expect, it } from 'vitest'
import { medicamentos } from './cargar'

describe('compatibilidad en Y global', () => {
  it('todo par de medicamentos de la app tiene entrada de compatibilidad en ambas fichas', () => {
    const faltan: string[] = []
    for (const a of medicamentos) {
      const con = new Set(a.compatibilidad.map((c) => c.con))
      for (const b of medicamentos) if (b.id !== a.id && !con.has(b.id)) faltan.push(`${a.id}→${b.id}`)
    }
    expect(faltan.slice(0, 5)).toEqual([])
    expect(faltan.length).toBe(0)
  })

  it('cada ficha registra compatibilidad con SF y SG5', () => {
    for (const a of medicamentos) {
      const con = a.compatibilidad.map((c) => c.con)
      expect(con, a.id).toEqual(expect.arrayContaining(['SF', 'SG5']))
    }
  })
})
