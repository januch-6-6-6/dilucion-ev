import { beforeAll, describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba, sufijo } from './escenario'

// Vías directas de escalada: lo que una invitada intentaría saltándose la app.
const servicio = clienteServicio()
let a: Awaited<ReturnType<typeof crearUsuario>>
let b: Awaited<ReturnType<typeof crearUsuario>>
let propuestaDeA: string

beforeAll(async () => {
  const hospital = await crearHospital('permisos')
  const medicamento = await medicamentoDePrueba()
  a = await crearUsuario({ nombre: 'permisos-a', establecimiento: hospital })
  b = await crearUsuario({ nombre: 'permisos-b', establecimiento: hospital })
  const r = await a.cliente.from('propuestas').insert({ medicamento, texto: 'de A' }).select('id').single()
  propuestaDeA = r.data!.id
})

describe('escalada directa', () => {
  it('una invitada no puede hacerse administradora', async () => {
    const r = await b.cliente.from('administradores').insert({ persona: b.id })
    expect(r.error).not.toBeNull()
    const { data } = await servicio.from('administradores').select('persona').eq('persona', b.id)
    expect(data).toEqual([])
  })

  it('una invitada no puede crear personas ni cambiar los ajustes', async () => {
    const persona = await b.cliente.from('personas').insert({ id: b.id, correo: `x+${sufijo}@dilucion-ev.test`, nombre: 'x' })
    expect(persona.error).not.toBeNull()
    await b.cliente.from('ajustes').update({ umbral_votos: 1 }).eq('id', 1)
    const { data } = await servicio.from('ajustes').select('umbral_votos').single()
    expect(data?.umbral_votos).toBe(3)
    const lectura = await b.cliente.from('ajustes').select('*')
    expect(lectura.data ?? []).toEqual([])
  })

  it('una invitada no lee la autoría de las propuestas ajenas en la tabla', async () => {
    const { data } = await b.cliente.from('propuestas').select('autora').eq('id', propuestaDeA)
    expect(data).toEqual([])
    const { data: propia } = await a.cliente.from('propuestas').select('autora').eq('id', propuestaDeA)
    expect(propia).toEqual([{ autora: a.id }])
  })

  it('el público no puede ejecutar las funciones de administración: se le niega el permiso antes de entrar', async () => {
    const r = await clientePublico().rpc('aprobar', { p: '00000000-0000-0000-0000-000000000000' })
    expect(r.error?.code).toBe('42501')
  })

  it('el registro público de cuentas está desactivado', async () => {
    const r = await clientePublico().auth.signUp({ email: `intruso+${sufijo}@dilucion-ev.test`, password: 'Clave-larga-123456' })
    expect(r.error).not.toBeNull()
    expect(r.data.user).toBeNull()
  })
})
