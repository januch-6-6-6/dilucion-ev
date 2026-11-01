import { describe, expect, it } from 'vitest'
import { verificar, objetivosDe, type PasoNumerico } from '../calculos/verificadorOcular'
import { validarOculares } from '../esquema/validar-oculares'
import { fuentesOculares, obtenerOcular, oculares, verificacionDeOcular } from './cargarOculares'

// Recetas de mezcla que no caben en el verificador de una presentación (usan varias ampollas y otros fármacos).
const PROTOCOLOS_DE_MEZCLA = ['adrenalina/shugar-epi-shugarcaine']

describe('datos oculares reales', () => {
  it('todas las fichas y fuentes pasan el validador', () => {
    expect(validarOculares(oculares, fuentesOculares)).toEqual([])
  })
  it('cada protocolo, calculado con verificar(), coincide con su dosis de la fuente', () => {
    for (const f of oculares) {
      for (const p of f.protocolos) {
        if (PROTOCOLOS_DE_MEZCLA.includes(`${f.id}/${p.id}`)) continue
        const presentacion = f.presentaciones.find((x) => x.id === p.partida)!
        const pasos: PasoNumerico[] = p.pasos.flatMap((s): PasoNumerico[] =>
          s.tipo === 'reconstituir' ? [{ tipo: 'reconstituir', volumenMl: s.volumenMl }] : s.tipo === 'diluir' ? [{ tipo: 'diluir', tomarMl: s.tomarMl, llevarAMl: s.llevarAMl }] : [],
        )
        const r = verificar({ presentacion, pasos, objetivos: [f.dosis[p.dosis].final!] })
        expect(r.ok && r.algunaCoincide, `${f.id}/${p.id}`).toBe(true)
      }
    }
  })
})

describe('lote piloto: cefuroxima y moxifloxacino', () => {
  it('cefuroxima: Aprokam registrado, dos protocolos y contrastada (CIMA + SEFH)', () => {
    const f = obtenerOcular('cefuroxima')!
    expect(f.registroChile).toBe('verificado')
    expect(f.presentaciones.find((p) => p.id === 'aprokam-50')?.registrosIsp).toEqual(['F-25555/25'])
    expect(f.protocolos.map((p) => p.id)).toEqual(['aprokam-ficha-tecnica', 'pnt-sefh-750'])
    expect(verificacionDeOcular(f)).toBe('contrastada')
  })
  it('moxifloxacino: dos protocolos off-label y una discrepancia con las cinco posturas', () => {
    const f = obtenerOcular('moxifloxacino')!
    expect(f.dosis.map((d) => d.estatus)).toEqual(['off_label', 'off_label'])
    expect(objetivosDe(f, 'oftalmica-0-5').map((o) => o.cantidad)).toEqual([
      { valor: 0.5, unidad: 'mg' },
      { valor: 150, unidad: 'mcg' },
    ])
    expect(f.discrepancias[0].valores).toHaveLength(5)
  })
  it('moxifloxacino: el verificador acepta Arshinoff (3→10) y rechaza 1→10 frente a las dos dosis', () => {
    const f = obtenerOcular('moxifloxacino')!
    const presentacion = f.presentaciones[0]
    const objetivos = objetivosDe(f, presentacion.id)
    const bien = verificar({ presentacion, pasos: [{ tipo: 'diluir', tomarMl: 3, llevarAMl: 10 }], objetivos })
    const mal = verificar({ presentacion, pasos: [{ tipo: 'diluir', tomarMl: 1, llevarAMl: 10 }], objetivos })
    expect(bien.ok && bien.algunaCoincide).toBe(true)
    expect(mal.ok && mal.algunaCoincide).toBe(false)
  })
})

const INTRACAMERALES = [
  'carbacol', 'acetilcolina', 'cefuroxima', 'moxifloxacino', 'adrenalina', 'lidocaina', 'fenilefrina-tropicamida-lidocaina',
  'fenilefrina-ketorolaco', 'azul-tripano', 'alteplasa', 'triamcinolona', 'verde-indocianina', 'azul-brillante',
]

describe('lote 1: las 13 intracamerales', () => {
  it('están las 13 y todas son de alto riesgo', () => {
    const ids = oculares.filter((f) => f.familias[0] === 'intracameral').map((f) => f.id)
    expect(ids.sort()).toEqual([...INTRACAMERALES].sort())
    expect(oculares.every((f) => f.altoRiesgo)).toBe(true)
  })
  it('sin registro en Chile: carbacol, acetilcolina, Omidria, azul tripano y azul brillante, con ficha FDA o CIMA', () => {
    const sin = oculares.filter((f) => f.registroChile === 'no_registrado' && INTRACAMERALES.includes(f.id)).map((f) => f.id)
    expect(sin.sort()).toEqual(['acetilcolina', 'azul-brillante', 'azul-tripano', 'carbacol', 'fenilefrina-ketorolaco'])
  })
  it('Mydrane: uso directo, 0,2 ml y la alerta de no dar dosis adicionales; registrado F-25730/25', () => {
    const f = obtenerOcular('fenilefrina-tropicamida-lidocaina')!
    expect(f.presentaciones[0]).toMatchObject({ usoDirecto: true, registrosIsp: ['F-25730/25'] })
    expect(f.dosis[0].final?.volumenMl).toBe(0.2)
    expect(f.alertas.join(' ')).toContain('No inyectar dosis adicionales')
  })
  it('alteplasa: rango 6–25 µg/0,1 ml off-label, alerta de hipema y sin protocolos', () => {
    const f = obtenerOcular('alteplasa')!
    expect(f.dosis[0].final).toEqual({ cantidad: { min: 6, max: 25, unidad: 'mcg' }, volumenMl: 0.1 })
    expect(f.dosis.every((d) => d.estatus === 'off_label')).toBe(true)
    expect(f.alertas.join(' ')).toContain('hipema')
    expect(f.protocolos).toEqual([])
  })
  it('lidocaína y triamcinolona reúnen varias vías en una sola ficha', () => {
    const vias = (id: string) => new Set(obtenerOcular(id)!.dosis.map((d) => d.via))
    expect([...vias('lidocaina')].sort()).toEqual(['intracameral', 'peribulbar', 'retrobulbar', 'subtenoniana'])
    expect(vias('triamcinolona')).toEqual(new Set(['intravitrea']))
  })
  it('frascos elegidos a mano: adrenalina 1 mg/1 mL y lidocaína 1 % (no los dentales)', () => {
    expect(obtenerOcular('adrenalina')!.presentaciones[0].registrosIsp).toEqual(['F-28164/24'])
    expect(obtenerOcular('lidocaina')!.presentaciones.find((p) => p.id === 'lidocaina-1')?.registrosIsp).toEqual(['F-28110/24'])
  })
  it('verde de indocianina queda sin pauta por falta de fuente ocular', () => {
    expect(obtenerOcular('verde-indocianina')!.sinPauta).not.toBeNull()
  })
  it('adrenalina: la receta de 0,015 % cuadra con el verificador (0,3 ml → 2 ml)', () => {
    const f = obtenerOcular('adrenalina')!
    const r = verificar({ presentacion: f.presentaciones[0], pasos: [{ tipo: 'diluir', tomarMl: 0.3, llevarAMl: 2 }], objetivos: [f.dosis[1].final!] })
    expect(r.ok && r.algunaCoincide).toBe(true)
  })
})
