import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba } from './escenario'

type Usuario = Awaited<ReturnType<typeof crearUsuario>>
const servicio = clienteServicio()
const SOLO_ADMIN = 'Solo el administrador puede hacer esto'
let X: string
let medicamento: string
let a: Usuario, b: Usuario, f: Usuario, g: Usuario, s: Usuario, admin: Usuario

const proponer = async (texto = 'nota de prueba') => {
  const r = await a.cliente.from('propuestas').insert({ medicamento, texto }).select('id').single()
  expect(r.error).toBeNull()
  return r.data!.id as string
}
const votarTodos = async (p: string, votantes: Usuario[]) => {
  for (const u of votantes) expect((await u.cliente.from('votos').insert({ propuesta: p, a_favor: true })).error).toBeNull()
}
const estado = async (p: string) => (await servicio.from('propuestas').select('estado').eq('id', p).single()).data?.estado
const bitacora = async (accion: string, objeto: string) =>
  (await servicio.from('bitacora').select('actor, detalle').eq('accion', accion).eq('objeto', objeto)).data

beforeAll(async () => {
  X = await crearHospital('admin-x')
  medicamento = await medicamentoDePrueba()
  a = await crearUsuario({ nombre: 'admin-a', establecimiento: X })
  b = await crearUsuario({ nombre: 'admin-b', establecimiento: X })
  f = await crearUsuario({ nombre: 'admin-f', establecimiento: X })
  g = await crearUsuario({ nombre: 'admin-g', establecimiento: X })
  s = await crearUsuario({ nombre: 'admin-s', establecimiento: X })
  admin = await crearUsuario({ nombre: 'admin-admin', admin: true })
})

afterAll(async () => {
  await admin.cliente.rpc('cambiar_umbral', { n: 3 })
})

describe('solo el administrador', () => {
  it('una invitada no puede usar ninguna función de administración', async () => {
    const p = await proponer()
    const intentos = [
      b.cliente.rpc('aprobar', { p }),
      b.cliente.rpc('rechazar', { p, comentario: 'no' }),
      b.cliente.rpc('retirar_nota', { p, motivo: 'no' }),
      b.cliente.rpc('suspender', { persona: f.id }),
      b.cliente.rpc('reactivar', { persona: f.id }),
      b.cliente.rpc('cambiar_umbral', { n: 1 }),
    ]
    for (const r of await Promise.all(intentos)) expect(r.error?.message).toContain(SOLO_ADMIN)
    expect(await estado(p)).toBe('en_votacion')
  })

  it('el público ni siquiera puede llamarlas', async () => {
    const r = await clientePublico().rpc('aprobar', { p: '00000000-0000-0000-0000-000000000000' })
    expect(r.error).not.toBeNull()
  })
})

describe('aprobar', () => {
  it('con el texto editado: el público la ve sin la autora y la bitácora guarda antes y después', async () => {
    const p = await proponer('texto original')
    await votarTodos(p, [b, f, g])
    expect(await estado(p)).toBe('en_bandeja')

    const r = await admin.cliente.rpc('aprobar', { p, texto_final: 'texto corregido' })
    expect(r.error).toBeNull()

    const { data } = await clientePublico().from('notas_publicadas').select('*').eq('id', p).single()
    expect(data).toMatchObject({ medicamento, establecimiento: X, texto_publicado: 'texto corregido', votos_a_favor: 3 })
    expect(Object.keys(data!)).not.toContain('autora')
    expect(await bitacora('edito_y_aprobo', p)).toEqual([
      { actor: admin.id, detalle: { antes: 'texto original', despues: 'texto corregido' } },
    ])
  })

  it('sin editar queda registrada como «aprobo»', async () => {
    const p = await proponer('tal cual')
    expect((await admin.cliente.rpc('aprobar', { p })).error).toBeNull()
    const { data } = await clientePublico().from('notas_publicadas').select('texto_publicado').eq('id', p).single()
    expect(data?.texto_publicado).toBe('tal cual')
    expect(await bitacora('aprobo', p)).toHaveLength(1)
  })

  it('no se aprueba dos veces ni con un texto de más de 500 caracteres', async () => {
    const p = await proponer()
    expect((await admin.cliente.rpc('aprobar', { p, texto_final: 'a'.repeat(501) })).error?.code).toBe('23514')
    expect((await admin.cliente.rpc('aprobar', { p })).error).toBeNull()
    expect((await admin.cliente.rpc('aprobar', { p })).error).not.toBeNull()
  })
})

describe('rechazar y retirar', () => {
  it('rechazar exige comentario y la autora lo ve', async () => {
    const p = await proponer()
    expect((await admin.cliente.rpc('rechazar', { p, comentario: '   ' })).error).not.toBeNull()
    expect((await admin.cliente.rpc('rechazar', { p, comentario: 'Falta la fuente' })).error).toBeNull()
    const { data } = await a.cliente.from('propuestas').select('estado, comentario_admin').eq('id', p).single()
    expect(data).toEqual({ estado: 'rechazada', comentario_admin: 'Falta la fuente' })
    const { data: vista } = await a.cliente.from('propuestas_comunidad').select('estado').eq('id', p).single()
    expect(vista?.estado).toBe('rechazada')
  })

  it('retirar una nota la saca de las publicadas; solo se retira lo aprobado', async () => {
    const p = await proponer()
    expect((await admin.cliente.rpc('retirar_nota', { p, motivo: 'El hospital cambió su práctica' })).error).not.toBeNull()
    await admin.cliente.rpc('aprobar', { p })
    expect((await admin.cliente.rpc('retirar_nota', { p, motivo: 'El hospital cambió su práctica' })).error).toBeNull()
    const { data } = await clientePublico().from('notas_publicadas').select('id').eq('id', p)
    expect(data).toEqual([])
    expect(await estado(p)).toBe('retirada')
  })
})

describe('personas', () => {
  it('suspender impide votar y reactivar lo devuelve; el administrador no se suspende a sí mismo', async () => {
    const p = await proponer()
    expect((await admin.cliente.rpc('suspender', { persona: s.id })).error).toBeNull()
    expect((await s.cliente.from('votos').insert({ propuesta: p, a_favor: true })).error?.message).toContain('Tu acceso está suspendido')
    expect((await admin.cliente.rpc('reactivar', { persona: s.id })).error).toBeNull()
    expect((await s.cliente.from('votos').insert({ propuesta: p, a_favor: true })).error).toBeNull()
    expect((await admin.cliente.rpc('suspender', { persona: admin.id })).error).not.toBeNull()
    expect(await bitacora('suspendio', s.id)).toHaveLength(1)
    expect(await bitacora('reactivo', s.id)).toHaveLength(1)
  })
})

describe('umbral', () => {
  it('cambiarlo rige para las votaciones siguientes y no mueve las que ya tenían votos', async () => {
    const vieja = await proponer()
    await votarTodos(vieja, [b, f])
    expect((await admin.cliente.rpc('cambiar_umbral', { n: 2 })).error).toBeNull()
    expect(await estado(vieja)).toBe('en_votacion')

    const nueva = await proponer()
    await votarTodos(nueva, [b, f])
    expect(await estado(nueva)).toBe('en_bandeja')

    await votarTodos(vieja, [g])
    expect(await estado(vieja)).toBe('en_bandeja')
    expect((await bitacora('cambio_umbral', '1')).some((e) => (e.detalle as { despues?: number }).despues === 2)).toBe(true)
  })

  it('un umbral fuera de 1 a 50 se rechaza', async () => {
    expect((await admin.cliente.rpc('cambiar_umbral', { n: 0 })).error).not.toBeNull()
    expect((await admin.cliente.rpc('cambiar_umbral', { n: 51 })).error).not.toBeNull()
  })
})
