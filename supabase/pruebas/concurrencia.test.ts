import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import { clienteServicio, crearHospital, crearUsuario, medicamentoDePrueba } from './escenario'

type Usuario = Awaited<ReturnType<typeof crearUsuario>>
const servicio = clienteServicio()
let X: string
let medicamento: string
let autora: Usuario
let votantes: Usuario[]
let admin: Usuario

beforeAll(async () => {
  X = await crearHospital('concurrencia')
  medicamento = await medicamentoDePrueba()
  autora = await crearUsuario({ nombre: 'conc-autora', establecimiento: X })
  admin = await crearUsuario({ nombre: 'conc-admin', admin: true })
  votantes = []
  for (const n of ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']) votantes.push(await crearUsuario({ nombre: `conc-v${n}`, establecimiento: X }))
})

afterAll(async () => {
  await admin.cliente.rpc('cambiar_umbral', { n: 3 })
})

const proponer = async () =>
  (await autora.cliente.from('propuestas').insert({ medicamento, texto: 'concurrente' }).select('id').single()).data!.id as string

describe('votos simultáneos', () => {
  it('10 votos a la vez sobre la misma propuesta (umbral alto, sin cierre) no dan deadlock y se cuentan todos', async () => {
    expect((await admin.cliente.rpc('cambiar_umbral', { n: 50 })).error).toBeNull()
    for (let ronda = 0; ronda < 6; ronda++) {
      const p = await proponer()
      const resultados = await Promise.all(votantes.map((v) => v.cliente.from('votos').insert({ propuesta: p, a_favor: ronda % 2 === 0 })))
      for (const r of resultados) expect(r.error, `ronda ${ronda}: ${r.error?.message}`).toBeNull()
      const { count } = await servicio.from('votos').select('persona', { count: 'exact', head: true }).eq('propuesta', p)
      expect(count).toBe(10)
    }
    expect((await admin.cliente.rpc('cambiar_umbral', { n: 3 })).error).toBeNull()
  })

  it('3 votos a la vez sobre la misma propuesta no se bloquean entre sí (sin deadlock) y se cuentan todos', async () => {
    expect((await admin.cliente.rpc('cambiar_umbral', { n: 3 })).error).toBeNull()
    for (let ronda = 0; ronda < 8; ronda++) {
      const p = await proponer()
      const resultados = await Promise.all(votantes.slice(0, 3).map((v) => v.cliente.from('votos').insert({ propuesta: p, a_favor: true })))
      for (const r of resultados) expect(r.error, `ronda ${ronda}: ${r.error?.message}`).toBeNull()
      const { data } = await servicio.from('propuestas').select('estado').eq('id', p).single()
      expect(data?.estado).toBe('en_bandeja')
      const { count } = await servicio.from('votos').select('persona', { count: 'exact', head: true }).eq('propuesta', p)
      expect(count).toBe(3)
    }
  })

  it('un voto que llega mientras se aprueba la propuesta no queda guardado sobre una propuesta cerrada', async () => {
    for (let ronda = 0; ronda < 4; ronda++) {
      const p = await proponer()
      const [aprobar, voto] = await Promise.all([
        admin.cliente.rpc('aprobar', { p }),
        votantes[0].cliente.from('votos').insert({ propuesta: p, a_favor: true }),
      ])
      expect(aprobar.error).toBeNull()
      const { data: estado } = await servicio.from('propuestas').select('estado').eq('id', p).single()
      expect(estado?.estado).toBe('aprobada')
      // O el voto entró antes de aprobar (cuenta) o se rechazó por cerrada: nunca un error distinto ni un voto huérfano.
      const { count } = await servicio.from('votos').select('persona', { count: 'exact', head: true }).eq('propuesta', p)
      if (voto.error) {
        expect(voto.error.message).toContain('La votación de esta propuesta está cerrada')
        expect(count).toBe(0)
      } else {
        expect(count).toBe(1)
      }
    }
  })
})
