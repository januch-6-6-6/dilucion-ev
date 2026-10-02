import { beforeAll, describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba } from './escenario'

// Requiere haber corrido: python3 scripts/supabase/cargar_catalogos.py --destino prueba
const servicio = clienteServicio()

describe('catálogos cargados', () => {
  it('el público lee los medicamentos de las fichas', async () => {
    const { count, error } = await clientePublico().from('medicamentos').select('id', { count: 'exact', head: true })
    expect(error).toBeNull()
    expect(count).toBeGreaterThanOrEqual(89)
    const { data } = await clientePublico().from('medicamentos').select('id').eq('id', 'ceftriaxona')
    expect(data).toEqual([{ id: 'ceftriaxona' }])
  })

  it('el público lee el catálogo DEIS completo, con los hospitales conocidos', async () => {
    const { count } = await clientePublico().from('establecimientos').select('codigo', { count: 'exact', head: true })
    expect(count).toBeGreaterThan(5000)
    const { data } = await clientePublico().from('establecimientos').select('nombre, tipo, comuna, vigente').eq('codigo', '114101').single()
    expect(data).toMatchObject({ tipo: 'Hospital', comuna: 'Puente Alto', vigente: true })
    expect(data?.nombre).toContain('Sótero del Río')
  })
})

describe('los catálogos no se tocan desde la app', () => {
  let a: Awaited<ReturnType<typeof crearUsuario>>
  beforeAll(async () => {
    a = await crearUsuario({ nombre: 'catalogos-a', establecimiento: '114101' })
  })

  it('ni el público ni una invitada pueden agregar, cambiar o borrar establecimientos y medicamentos', async () => {
    for (const cliente of [clientePublico(), a.cliente]) {
      expect((await cliente.from('establecimientos').insert({ codigo: 'X-1', nombre: 'falso' })).error).not.toBeNull()
      expect((await cliente.from('medicamentos').insert({ id: 'falso' })).error).not.toBeNull()
      await cliente.from('establecimientos').update({ nombre: 'cambiado' }).eq('codigo', '114101')
      await cliente.from('establecimientos').delete().eq('codigo', '114101')
    }
    const { data } = await servicio.from('establecimientos').select('nombre').eq('codigo', '114101').single()
    expect(data?.nombre).toContain('Sótero del Río')
  })

  it('un establecimiento con propuestas no se puede borrar, así una recarga del catálogo nunca las deja huérfanas', async () => {
    const hospital = await crearHospital('catalogos')
    const autora = await crearUsuario({ nombre: 'catalogos-autora', establecimiento: hospital })
    const medicamento = await medicamentoDePrueba()
    expect((await autora.cliente.from('propuestas').insert({ medicamento, texto: 'nota' })).error).toBeNull()
    const r = await servicio.from('establecimientos').delete().eq('codigo', hospital)
    expect(r.error?.code).toBe('23503')
  })
})
