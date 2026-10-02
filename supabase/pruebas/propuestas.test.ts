import { beforeAll, describe, expect, it } from 'vitest'
import { clientePublico, clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba } from './escenario'

const servicio = clienteServicio()
let X: string
let Y: string
let medicamento: string
let a: Awaited<ReturnType<typeof crearUsuario>>
let b: Awaited<ReturnType<typeof crearUsuario>>
let fuera: Awaited<ReturnType<typeof crearUsuario>>
let sinHospital: Awaited<ReturnType<typeof crearUsuario>>
let suspendida: Awaited<ReturnType<typeof crearUsuario>>

const proponer = (u: typeof a, texto: string, extra: Record<string, unknown> = {}) =>
  u.cliente.from('propuestas').insert({ medicamento, texto, ...extra }).select('id, autora, establecimiento, estado').single()

beforeAll(async () => {
  X = await crearHospital('propuestas-x')
  Y = await crearHospital('propuestas-y')
  medicamento = await medicamentoDePrueba()
  a = await crearUsuario({ nombre: 'propuestas-a', establecimiento: X })
  b = await crearUsuario({ nombre: 'propuestas-b', establecimiento: X })
  fuera = await crearUsuario({ nombre: 'propuestas-fuera', pais: 'Perú' })
  sinHospital = await crearUsuario({ nombre: 'propuestas-sin' })
  suspendida = await crearUsuario({ nombre: 'propuestas-s', establecimiento: X, suspendida: true })
})

describe('proponer', () => {
  it('el servidor fija autora, hospital y estado aunque la app mande otros valores', async () => {
    const r = await proponer(a, 'En este hospital se diluye en 100 ml', { establecimiento: Y, estado: 'aprobada', autora: b.id })
    expect(r.error).toBeNull()
    expect(r.data).toMatchObject({ autora: a.id, establecimiento: X, estado: 'en_votacion' })
  })

  it('quien trabaja fuera de Chile o aún no elige hospital no puede proponer', async () => {
    for (const u of [fuera, sinHospital]) {
      const r = await proponer(u, 'nota')
      expect(r.error?.message).toContain('Las prácticas locales se proponen desde hospitales chilenos')
    }
  })

  it('una persona suspendida no puede proponer', async () => {
    const r = await proponer(suspendida, 'nota')
    expect(r.error?.message).toContain('Tu acceso está suspendido')
  })

  it('el texto vacío, solo de espacios o de 501 caracteres se rechaza; 500 caracteres es válido', async () => {
    for (const texto of ['', '   ', 'a'.repeat(501)]) {
      const r = await proponer(a, texto)
      expect(r.error?.code, `texto de ${texto.length} caracteres`).toBe('23514')
    }
    const ok = await proponer(a, 'a'.repeat(500))
    expect(ok.error).toBeNull()
  })
})

describe('ver propuestas', () => {
  it('otra invitada la ve sin la autora, el público y la suspendida no ven nada', async () => {
    const { data: creada } = await proponer(a, 'visible para la comunidad')
    const { data: vista, error } = await b.cliente.from('propuestas_comunidad').select('*').eq('id', creada!.id).single()
    expect(error).toBeNull()
    expect(vista).toMatchObject({ medicamento, establecimiento: X, a_favor: 0, en_contra: 0, es_mia: false, mi_voto: null })
    expect(Object.keys(vista!)).not.toContain('autora')

    const propia = await a.cliente.from('propuestas_comunidad').select('es_mia').eq('id', creada!.id).single()
    expect(propia.data?.es_mia).toBe(true)

    const publico = await clientePublico().from('propuestas_comunidad').select('*').eq('id', creada!.id)
    if (publico.error) expect(publico.error.code).toBe('42501')
    expect(publico.data ?? []).toEqual([])
    const susp = await suspendida.cliente.from('propuestas_comunidad').select('*').eq('id', creada!.id)
    expect(susp.data ?? []).toEqual([])
  })
})

describe('retirar y editar', () => {
  it('la autora retira la suya mientras está en votación; otra persona no puede', async () => {
    const { data: creada } = await proponer(a, 'la voy a retirar')
    const ajena = await b.cliente.rpc('retirar_propuesta', { p: creada!.id })
    expect(ajena.error).not.toBeNull()
    const propia = await a.cliente.rpc('retirar_propuesta', { p: creada!.id })
    expect(propia.error).toBeNull()
    const { data } = await servicio.from('propuestas').select('estado').eq('id', creada!.id).single()
    expect(data?.estado).toBe('retirada')
    const otraVez = await a.cliente.rpc('retirar_propuesta', { p: creada!.id })
    expect(otraVez.error).not.toBeNull()
  })

  it('nadie edita una propuesta directamente desde la app', async () => {
    const { data: creada } = await proponer(a, 'texto original')
    const upd = await a.cliente.from('propuestas').update({ texto: 'cambiado' }).eq('id', creada!.id)
    expect(upd.error).not.toBeNull()
    const del = await a.cliente.from('propuestas').delete().eq('id', creada!.id)
    expect(del.error).not.toBeNull()
    const { data } = await servicio.from('propuestas').select('texto').eq('id', creada!.id).single()
    expect(data?.texto).toBe('texto original')
  })
})
