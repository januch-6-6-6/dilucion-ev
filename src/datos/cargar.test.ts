import { describe, expect, it } from 'vitest'
import { fuentes, medicamentos, obtenerFicha } from './cargar'

describe('cargar', () => {
  it('carga las fichas validadas, ordenadas por nombre', () => {
    expect(medicamentos.length).toBeGreaterThanOrEqual(10)
    const nombres = medicamentos.map((m) => m.nombre)
    expect([...nombres].sort((a, b) => a.localeCompare(b, 'es'))).toEqual(nombres)
  })
  it('obtiene una ficha por id', () => expect(obtenerFicha('noradrenalina')?.presentaciones[0].volumenMl).toBe(4))
  it('id inexistente da undefined', () => expect(obtenerFicha('no-existe')).toBeUndefined())
  it('carga las fuentes', () => expect(fuentes.find((f) => f.id === 'PUCON-2022')).toBeTruthy())
})
