import { beforeAll, describe, expect, it } from 'vitest'
import { clienteServicio, crearHospital, crearUsuario } from './escenario'

const servicio = clienteServicio()
let X: string
let Y: string
let a: Awaited<ReturnType<typeof crearUsuario>>
let b: Awaited<ReturnType<typeof crearUsuario>>
let suspendida: Awaited<ReturnType<typeof crearUsuario>>
let admin: Awaited<ReturnType<typeof crearUsuario>>

beforeAll(async () => {
  X = await crearHospital('personas-x')
  Y = await crearHospital('personas-y')
  a = await crearUsuario({ nombre: 'personas-a', establecimiento: X })
  b = await crearUsuario({ nombre: 'personas-b', establecimiento: Y })
  suspendida = await crearUsuario({ nombre: 'personas-s', establecimiento: X, suspendida: true })
  admin = await crearUsuario({ nombre: 'personas-admin', admin: true })
})

describe('cambio de hospital', () => {
  it('queda en el historial de la persona y en la bitácora que lee el administrador', async () => {
    const r = await a.cliente.from('personas').update({ establecimiento: Y }).eq('id', a.id).select()
    expect(r.error).toBeNull()
    expect(r.data).toHaveLength(1)

    const { data: historial } = await a.cliente.from('historial_hospital').select('desde, hacia').eq('persona', a.id)
    expect(historial).toEqual([{ desde: X, hacia: Y }])

    const { data: bitacora } = await admin.cliente.from('bitacora').select('actor, detalle').eq('accion', 'cambio_hospital').eq('objeto', a.id)
    expect(bitacora).toEqual([{ actor: a.id, detalle: { desde: X, hacia: Y } }])
  })

  it('pasar a «fuera de Chile» registra el país', async () => {
    const r = await a.cliente.from('personas').update({ establecimiento: null, pais_extranjero: 'Perú' }).eq('id', a.id).select()
    expect(r.error).toBeNull()
    const { data } = await a.cliente.from('historial_hospital').select('desde, hacia').eq('persona', a.id).order('fecha', { ascending: false }).limit(1)
    expect(data).toEqual([{ desde: Y, hacia: 'extranjero: Perú' }])
  })

  it('una persona no puede cambiar su estado ni su nombre', async () => {
    const estado = await a.cliente.from('personas').update({ estado: 'activa' }).eq('id', a.id)
    expect(estado.error).not.toBeNull()
    const nombre = await a.cliente.from('personas').update({ nombre: 'otro' }).eq('id', a.id)
    expect(nombre.error).not.toBeNull()
  })

  it('una persona suspendida no puede cambiar su hospital', async () => {
    const r = await suspendida.cliente.from('personas').update({ establecimiento: Y }).eq('id', suspendida.id).select()
    expect(r.data ?? []).toEqual([])
    const { data } = await servicio.from('personas').select('establecimiento').eq('id', suspendida.id).single()
    expect(data?.establecimiento).toBe(X)
  })
})

describe('quién lee qué', () => {
  it('una persona solo ve su propia fila; el administrador ve todas', async () => {
    const { data: propias } = await b.cliente.from('personas').select('id')
    expect(propias).toEqual([{ id: b.id }])
    const { data: todas } = await admin.cliente.from('personas').select('id')
    expect(todas!.length).toBeGreaterThanOrEqual(4)
  })

  it('una persona no ve el historial de otra', async () => {
    const { data } = await b.cliente.from('historial_hospital').select('persona').eq('persona', a.id)
    expect(data).toEqual([])
  })
})
