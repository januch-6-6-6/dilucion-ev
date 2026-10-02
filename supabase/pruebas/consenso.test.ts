import { beforeAll, describe, expect, it } from 'vitest'
import { clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba } from './escenario'

type Usuario = Awaited<ReturnType<typeof crearUsuario>>
const servicio = clienteServicio()
let X: string
let Y: string
let medicamento: string
let a: Usuario // autora, hospital X
let b: Usuario, f: Usuario, g: Usuario // hospital X
let c: Usuario, h: Usuario // hospital Y
let d: Usuario, i: Usuario // fuera de Chile
let s: Usuario // hospital X, se suspende dentro de una prueba
let e: Usuario // sin hospital

const proponer = async (autora: Usuario, texto = 'nota de prueba') => {
  const r = await autora.cliente.from('propuestas').insert({ medicamento, texto }).select('id').single()
  expect(r.error).toBeNull()
  return r.data!.id as string
}
const votar = (u: Usuario, propuesta: string, a_favor: boolean, extra: Record<string, unknown> = {}) =>
  u.cliente.from('votos').insert({ propuesta, a_favor, ...extra })
const estado = async (propuesta: string) =>
  (await servicio.from('propuestas').select('estado').eq('id', propuesta).single()).data?.estado

beforeAll(async () => {
  X = await crearHospital('consenso-x')
  Y = await crearHospital('consenso-y')
  medicamento = await medicamentoDePrueba()
  a = await crearUsuario({ nombre: 'consenso-a', establecimiento: X })
  b = await crearUsuario({ nombre: 'consenso-b', establecimiento: X })
  f = await crearUsuario({ nombre: 'consenso-f', establecimiento: X })
  g = await crearUsuario({ nombre: 'consenso-g', establecimiento: X })
  c = await crearUsuario({ nombre: 'consenso-c', establecimiento: Y })
  h = await crearUsuario({ nombre: 'consenso-h', establecimiento: Y })
  d = await crearUsuario({ nombre: 'consenso-d', pais: 'Perú' })
  i = await crearUsuario({ nombre: 'consenso-i', pais: 'Argentina' })
  s = await crearUsuario({ nombre: 'consenso-s', establecimiento: X })
  e = await crearUsuario({ nombre: 'consenso-e' })
})

describe('umbral de 3 votos locales', () => {
  let p: string

  it('con 2 votos del mismo hospital sigue en votación', async () => {
    p = await proponer(a)
    expect((await votar(b, p, true)).error).toBeNull()
    expect((await votar(f, p, true)).error).toBeNull()
    expect(await estado(p)).toBe('en_votacion')
  })

  it('los votos de otro hospital o de fuera de Chile no cuentan para el umbral', async () => {
    expect((await votar(c, p, true)).error).toBeNull()
    expect((await votar(d, p, true)).error).toBeNull()
    expect(await estado(p)).toBe('en_votacion')
  })

  it('el 3.er voto del mismo hospital la pasa a la bandeja, y queda registrado', async () => {
    expect((await votar(g, p, true)).error).toBeNull()
    expect(await estado(p)).toBe('en_bandeja')
    const { data } = await servicio.from('bitacora').select('actor, detalle').eq('accion', 'paso_a_bandeja').eq('objeto', p)
    expect(data).toEqual([{ actor: null, detalle: { a_favor_local: 3, a_favor: 5, en_contra: 0 } }])
  })

  it('en la bandeja la votación está cerrada y el estado no retrocede', async () => {
    const cerrado = await b.cliente.from('votos').update({ a_favor: false }).eq('propuesta', p)
    expect(cerrado.error?.message).toContain('La votación de esta propuesta está cerrada')
    const nuevo = await votar(h, p, true)
    expect(nuevo.error?.message).toContain('La votación de esta propuesta está cerrada')
    // Aunque un voto cambie por fuera de la app, una propuesta ya evaluada no vuelve atrás.
    await servicio.from('votos').update({ a_favor: false }).eq('propuesta', p)
    expect(await estado(p)).toBe('en_bandeja')
  })
})

describe('más en contra que a favor', () => {
  it('3 votos locales a favor no bastan si hay más en contra', async () => {
    const p = await proponer(a)
    for (const u of [c, h, d, i]) expect((await votar(u, p, false)).error).toBeNull()
    for (const u of [b, f, g]) expect((await votar(u, p, true)).error).toBeNull()
    expect(await estado(p)).toBe('en_votacion')
    const { data } = await b.cliente.from('propuestas_comunidad').select('a_favor, en_contra, mi_voto').eq('id', p).single()
    expect(data).toEqual({ a_favor: 3, en_contra: 4, mi_voto: true })
  })
})

describe('personas suspendidas', () => {
  it('sus votos se conservan pero dejan de contar', async () => {
    const p = await proponer(a)
    expect((await votar(s, p, true)).error).toBeNull()
    await servicio.from('personas').update({ estado: 'suspendida' }).eq('id', s.id)
    expect((await votar(b, p, true)).error).toBeNull()
    expect((await votar(f, p, true)).error).toBeNull()
    expect(await estado(p)).toBe('en_votacion')
    const { data } = await servicio.from('votos').select('persona').eq('propuesta', p).eq('persona', s.id)
    expect(data).toHaveLength(1)
    const { data: vista } = await b.cliente.from('propuestas_comunidad').select('a_favor').eq('id', p).single()
    expect(vista?.a_favor).toBe(2)
  })

  it('una persona suspendida no puede votar', async () => {
    const p = await proponer(a)
    const r = await votar(s, p, true)
    expect(r.error?.message).toContain('Tu acceso está suspendido')
  })
})

describe('reglas de cada voto', () => {
  it('nadie vota su propia propuesta ni dos veces, pero puede cambiar su voto', async () => {
    const p = await proponer(a)
    expect((await votar(a, p, true)).error?.message).toContain('No puedes votar tu propia propuesta')
    expect((await votar(b, p, true)).error).toBeNull()
    expect((await votar(b, p, false)).error?.code).toBe('23505')
    const cambio = await b.cliente.from('votos').update({ a_favor: false }).eq('propuesta', p).select()
    expect(cambio.error).toBeNull()
    expect(cambio.data).toHaveLength(1)
    const { data } = await servicio.from('bitacora').select('actor').eq('accion', 'cambio_voto').eq('objeto', p)
    expect(data).toEqual([{ actor: b.id }])
  })

  it('sin elegir hospital no se puede votar', async () => {
    const p = await proponer(a)
    expect((await votar(e, p, true)).error?.message).toContain('Elige tu hospital antes de votar')
  })

  it('el hospital del voto lo fija el servidor, no la app', async () => {
    const p = await proponer(a)
    expect((await votar(b, p, true, { establecimiento_al_votar: Y, pais_al_votar: 'Chile', persona: c.id })).error).toBeNull()
    const { data } = await servicio.from('votos').select('persona, establecimiento_al_votar, pais_al_votar').eq('propuesta', p).single()
    expect(data).toEqual({ persona: b.id, establecimiento_al_votar: X, pais_al_votar: null })
  })

  it('quien vota desde fuera de Chile guarda su país', async () => {
    const p = await proponer(a)
    expect((await votar(d, p, true)).error).toBeNull()
    const { data } = await servicio.from('votos').select('establecimiento_al_votar, pais_al_votar').eq('propuesta', p).single()
    expect(data).toEqual({ establecimiento_al_votar: null, pais_al_votar: 'Perú' })
  })

  it('cada persona ve solo su propio voto', async () => {
    const p = await proponer(a)
    await votar(b, p, true)
    await votar(f, p, false)
    const { data } = await b.cliente.from('votos').select('persona').eq('propuesta', p)
    expect(data).toEqual([{ persona: b.id }])
  })
})
