import { randomBytes } from 'node:crypto'
import { beforeAll, describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba, sufijo } from './escenario'

const servicio = clienteServicio()
let hospital: string
let medicamento: string
let autora: string

beforeAll(async () => {
  hospital = await crearHospital('esquema')
  medicamento = await medicamentoDePrueba()
  autora = (await crearUsuario({ nombre: 'esquema-autora', establecimiento: hospital })).id
})

describe('restricciones del esquema', () => {
  it('una persona no puede tener hospital chileno y país extranjero a la vez', async () => {
    const { data, error } = await servicio.auth.admin.createUser({
      email: `prueba+${sufijo}-ambos@dilucion-ev.test`,
      password: randomBytes(18).toString('base64url'),
      email_confirm: true,
    })
    expect(error).toBeNull()
    const r = await servicio.from('personas').insert({
      id: data.user!.id,
      correo: `prueba+${sufijo}-ambos@dilucion-ev.test`,
      nombre: 'ambos',
      establecimiento: hospital,
      pais_extranjero: 'Perú',
    })
    expect(r.error?.code).toBe('23514')
  })

  it('una propuesta para un medicamento inexistente se rechaza', async () => {
    const r = await servicio
      .from('propuestas')
      .insert({ medicamento: `no-existe-${sufijo}`, establecimiento: hospital, texto: 'x', autora })
    expect(r.error?.code).toBe('23503')
  })

  it('no se puede borrar un medicamento que tiene propuestas', async () => {
    const ok = await servicio.from('propuestas').insert({ medicamento, establecimiento: hospital, texto: 'nota', autora })
    expect(ok.error).toBeNull()
    const r = await servicio.from('medicamentos').delete().eq('id', medicamento)
    expect(r.error?.code).toBe('23503')
  })
})

describe('el público no ve datos sensibles', () => {
  it('personas, administradores, historial, propuestas, votos, bitácora y ajustes salen vacíos', async () => {
    const otra = await crearUsuario({ nombre: 'esquema-votante', establecimiento: hospital })
    const { data: p } = await servicio.from('propuestas').select('id').eq('autora', autora).limit(1).single()
    await servicio.from('votos').insert({ propuesta: p!.id, persona: otra.id, a_favor: true, establecimiento_al_votar: hospital })
    await servicio.from('bitacora').insert({ accion: 'prueba', objeto: sufijo })

    // La prueba solo vale si las filas existen: el servicio sí las ve.
    for (const tabla of ['personas', 'propuestas', 'votos', 'bitacora']) {
      const { data } = await servicio.from(tabla).select('*').limit(1)
      expect(data?.length, `${tabla} debería tener filas para el servicio`).toBe(1)
    }

    const publico = clientePublico()
    for (const tabla of ['personas', 'administradores', 'historial_hospital', 'propuestas', 'votos', 'bitacora', 'ajustes']) {
      const { data, error } = await publico.from(tabla).select('*')
      expect(error, `${tabla} devolvió error`).toBeNull()
      expect(data, `${tabla} no debería mostrar filas al público`).toEqual([])
    }
  })
})
