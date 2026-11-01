import { describe, expect, it } from 'vitest'
import { GRUPOS } from '../app/etiquetas'
import { combinacionesCalculables } from '../calculos/duracionEnvase'
import { fuentesTopicos, obtenerTopico, topicos, verificacionDeTopico } from './cargarTopicos'

const SIN_PAUTA = [
  'antazolina-bacitracina-neomicina-xilometazolina', 'betametasona', 'betametasona-gentamicina', 'betametasona-neomicina',
  'betametasona-neomicina-polimixina-b', 'betaxolol', 'bimatoprost-brimonidina-timolol', 'brimonidina-dorzolamida-timolol',
  'cromoglicato', 'dexametasona-moxifloxacino', 'dextrano-hipromelosa-nafazolina', 'fenazona-lidocaina',
  'gatifloxacino-prednisolona', 'ketorolaco', 'levofloxacino', 'lidocaina-sulfatiazol',
]

describe('datos tópicos reales', () => {
  it('son las 80 moléculas del ISP, con 99 fuentes', () => {
    expect(topicos).toHaveLength(80)
    expect(fuentesTopicos).toHaveLength(99)
  })
  it('las 16 sin pauta son exactamente las del informe', () => {
    expect(topicos.filter((t) => t.sinPauta).map((t) => t.id).sort()).toEqual([...SIN_PAUTA].sort())
  })
  it('13 contrastadas y 51 de fuente única', () => {
    const v = topicos.map(verificacionDeTopico)
    expect(v.filter((x) => x === 'contrastada')).toHaveLength(13)
    expect(v.filter((x) => x === 'fuente_unica')).toHaveLength(51)
  })
  it('todo grupo usado tiene etiqueta', () => {
    for (const t of topicos) expect(GRUPOS[t.grupo], t.grupo).toBeDefined()
  })
  it('regla de concentración: betaxolol 0,5 % sin pauta; bimatoprost solo 0,01 %', () => {
    expect(obtenerTopico('betaxolol')?.sinPauta).not.toBeNull()
    const b = obtenerTopico('bimatoprost')
    expect(b?.dosis.every((d) => d.presentaciones?.join() === 'ojo-solucion-0-01')).toBe(true)
  })
  it('atropina: pauta pediátrica de Pediamécum marcada off-label', () => {
    const a = obtenerTopico('atropina')
    expect(a?.altoRiesgo).toBe(true)
    expect(a?.dosis.some((d) => d.poblacion === 'pediatrico' && d.estatus === 'off_label' && d.fuente.ref.startsWith('PEDIAMECUM'))).toBe(true)
  })
  it('ningún ungüento ni unidosis queda como calculable', () => {
    for (const t of topicos) {
      for (const c of combinacionesCalculables(t)) {
        expect(c.presentacion.forma, t.id).not.toBe('unguento')
        expect(c.presentacion.unidosis, t.id).not.toBe(true)
      }
    }
  })
})

describe('grupos tópicos en la UI', () => {
  it('todo grupo tópico tiene color propio (nunca neutro)', async () => {
    const { colorGrupo } = await import('../app/colores')
    for (const t of topicos) expect(colorGrupo(t.grupo), t.grupo).not.toBe('neutro')
  })
})
