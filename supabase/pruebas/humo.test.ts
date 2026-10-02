import { describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio } from './escenario'

describe('arnés de pruebas', () => {
  it('el público no lee ajustes y el servicio sí', async () => {
    const { data: publico } = await clientePublico().from('ajustes').select('*')
    expect(publico).toEqual([])
    const { data } = await clienteServicio().from('ajustes').select('umbral_votos').single()
    expect(data?.umbral_votos).toBe(3)
  })
})
