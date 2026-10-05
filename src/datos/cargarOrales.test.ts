import { describe, expect, it } from 'vitest'
import { FichaOral } from '../esquema/ficha-oral'
import { fichaOralValida } from '../esquema/__fixtures__/orales'
import { fuentesOrales, obtenerOral, orales, verificacion } from './cargarOrales'

describe('cargarOrales', () => {
  it('id inexistente da undefined', () => expect(obtenerOral('inexistente')).toBeUndefined())
  it('las orales están ordenadas por nombre', () => {
    const nombres = orales.map((o) => o.nombre)
    expect([...nombres].sort((a, b) => a.localeCompare(b, 'es'))).toEqual(nombres)
  })
  it('fuentesOrales es una lista', () => expect(Array.isArray(fuentesOrales)).toBe(true))
  it('verificacion: fuente_unica para una ficha con una sola institución', () => {
    expect(verificacion(FichaOral.parse(fichaOralValida()))).toBe('fuente_unica')
  })
})
