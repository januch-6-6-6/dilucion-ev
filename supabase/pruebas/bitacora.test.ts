import { beforeAll, describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio, crearHospital, crearUsuario, sufijo } from './escenario'

const servicio = clienteServicio()
let a: Awaited<ReturnType<typeof crearUsuario>>
let admin: Awaited<ReturnType<typeof crearUsuario>>
let filaId: number

beforeAll(async () => {
  const hospital = await crearHospital('bitacora')
  a = await crearUsuario({ nombre: 'bitacora-a', establecimiento: hospital })
  admin = await crearUsuario({ nombre: 'bitacora-admin', admin: true })
  const { data, error } = await servicio.from('bitacora').insert({ accion: 'prueba', objeto: `bitacora-${sufijo}`, detalle: { original: true } }).select('id').single()
  expect(error).toBeNull()
  filaId = data!.id
})

describe('lectura', () => {
  it('una invitada no lee la bitácora y el administrador sí', async () => {
    const { data: de } = await a.cliente.from('bitacora').select('id').eq('id', filaId)
    expect(de).toEqual([])
    const { data: admin_ } = await admin.cliente.from('bitacora').select('id').eq('id', filaId)
    expect(admin_).toEqual([{ id: filaId }])
  })

  it('nadie puede escribir en la bitácora ni llamar a registrar() desde la app', async () => {
    const directo = await a.cliente.from('bitacora').insert({ accion: 'falsa' })
    expect(directo.error).not.toBeNull()
    const funcion = await a.cliente.rpc('registrar', { accion: 'falsa', objeto: 'x', detalle: {} })
    expect(funcion.error).not.toBeNull()
    const publico = await clientePublico().rpc('registrar', { accion: 'falsa', objeto: 'x', detalle: {} })
    expect(publico.error).not.toBeNull()
  })
})

describe('inmutabilidad', () => {
  it('el administrador no puede modificar ni borrar una entrada', async () => {
    const upd = await admin.cliente.from('bitacora').update({ accion: 'cambiada' }).eq('id', filaId)
    expect(upd.error).not.toBeNull()
    const del = await admin.cliente.from('bitacora').delete().eq('id', filaId)
    expect(del.error).not.toBeNull()
    const { data } = await servicio.from('bitacora').select('accion').eq('id', filaId).single()
    expect(data?.accion).toBe('prueba')
  })

  it('ni siquiera la clave de servicio puede modificarla o borrarla', async () => {
    const upd = await servicio.from('bitacora').update({ accion: 'cambiada' }).eq('id', filaId)
    expect(upd.error?.message).toContain('La bitácora no se puede modificar')
    const del = await servicio.from('bitacora').delete().eq('id', filaId)
    expect(del.error?.message).toContain('La bitácora no se puede modificar')
  })
})
