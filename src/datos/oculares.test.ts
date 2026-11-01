import { describe, expect, it } from 'vitest'
import { verificar, objetivosDe, type PasoNumerico } from '../calculos/verificadorOcular'
import { validarOculares } from '../esquema/validar-oculares'
import { colorGrupo } from '../app/colores'
import { etiquetaGrupo } from '../app/etiquetas'
import { orales } from './cargarOrales'
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

const INTRAVITREAS = [
  'bevacizumab', 'ranibizumab', 'aflibercept', 'faricimab', 'brolucizumab', 'dexametasona-implante', 'vancomicina', 'ceftazidima',
  'amikacina', 'anfotericina-b', 'voriconazol', 'ganciclovir', 'foscarnet', 'clindamicina', 'metotrexato', 'ocriplasmina',
]

describe('lote 2: intravítreas', () => {
  it('hay exactamente las 16 intravítreas del listado', () => {
    const ids = oculares.filter((f) => f.familias[0] === 'intravitreo').map((f) => f.id).sort()
    expect(ids).toEqual([...INTRAVITREAS].sort())
  })
  it('las no registradas del lote son brolucizumab, anfotericina B y ocriplasmina', () => {
    const ids = oculares.filter((f) => f.familias[0] === 'intravitreo' && f.registroChile === 'no_registrado').map((f) => f.id).sort()
    expect(ids).toEqual(['anfotericina-b', 'brolucizumab', 'ocriplasmina'])
  })
  it('anti-VEGF listos para usar: usoDirecto y alerta de eliminar el exceso de volumen', () => {
    for (const id of ['ranibizumab', 'aflibercept', 'faricimab', 'brolucizumab']) {
      const f = obtenerOcular(id)!
      expect(f.presentaciones.every((p) => p.usoDirecto), id).toBe(true)
      expect(f.protocolos, id).toEqual([])
      expect(f.alertas.join(' '), id).toContain('elimina el exceso')
    }
  })
  it('Lucentis trae la dosis pediátrica de 0,2 mg/0,02 ml (retinopatía del prematuro)', () => {
    const f = obtenerOcular('ranibizumab')!
    expect(f.pediatria.estado).toBe('con_dosis')
    expect(f.dosis.map((d) => [d.poblacion, d.final!.cantidad, d.final!.volumenMl])).toEqual([
      ['adulto', { valor: 0.5, unidad: 'mg' }, 0.05],
      ['pediatrico', { valor: 0.2, unidad: 'mg' }, 0.02],
    ])
  })
  it('bevacizumab: 1,25 mg/0,05 ml off-label y el protocolo del PNT cuadra sin diluir', () => {
    const f = obtenerOcular('bevacizumab')!
    expect(f.dosis).toHaveLength(1)
    expect(f.dosis[0].estatus).toBe('off_label')
    expect(f.dosis[0].final).toEqual({ cantidad: { valor: 1.25, unidad: 'mg' }, volumenMl: 0.05 })
    const r = verificar({ presentacion: f.presentaciones[0], pasos: [], objetivos: [f.dosis[0].final!] })
    expect(r.ok && r.algunaCoincide).toBe(true)
  })
  it('dexametasona en implante es informativa: sin protocolo ni cifra de concentración', () => {
    const f = obtenerOcular('dexametasona-implante')!
    expect(f.modo).toBe('informativa')
    expect(f.protocolos).toEqual([])
    expect(f.dosis[0].final).toBeUndefined()
  })
  it('ceftazidima muestra 2 mg/0,1 ml y registra la discrepancia con 2,25 mg', () => {
    const f = obtenerOcular('ceftazidima')!
    expect(f.dosis[0].final).toEqual({ cantidad: { valor: 2, unidad: 'mg' }, volumenMl: 0.1 })
    const d = f.discrepancias[0]
    expect(d.valores.map((v) => v.valor).join(' | ')).toContain('2,25 mg/0,1 ml')
    expect(d.valores.length).toBeGreaterThanOrEqual(3)
  })
  it('vancomicina: el verificador acepta 10 ml → 2 ml → 10 ml y rechaza 10 ml → 1 ml → 10 ml', () => {
    const f = obtenerOcular('vancomicina')!
    const presentacion = f.presentaciones[0]
    const objetivos = objetivosDe(f, presentacion.id)
    const bien = verificar({ presentacion, pasos: [{ tipo: 'reconstituir', volumenMl: 10 }, { tipo: 'diluir', tomarMl: 2, llevarAMl: 10 }], objetivos })
    const mal = verificar({ presentacion, pasos: [{ tipo: 'reconstituir', volumenMl: 10 }, { tipo: 'diluir', tomarMl: 1, llevarAMl: 10 }], objetivos })
    expect(bien.ok && bien.algunaCoincide).toBe(true)
    expect(mal.ok && mal.algunaCoincide).toBe(false)
  })
  it('vancomicina lleva la alerta roja HORV y amikacina la de infarto macular', () => {
    expect(obtenerOcular('vancomicina')!.alertas.join(' ')).toContain('HORV')
    expect(obtenerOcular('amikacina')!.alertas.join(' ')).toContain('INFARTO MACULAR')
  })
  it('amikacina, anfotericina B, clindamicina, foscarnet y metotrexato no traen protocolo', () => {
    for (const id of ['amikacina', 'anfotericina-b', 'clindamicina', 'foscarnet', 'metotrexato']) {
      expect(obtenerOcular(id)!.protocolos, id).toEqual([])
    }
  })
  it('voriconazol (200 mg → 20 ml → 1 mg/ml) y ganciclovir (500 mg → 10 ml → 2 ml a 5 ml) cuadran con el verificador', () => {
    const v = obtenerOcular('voriconazol')!
    const rv = verificar({ presentacion: v.presentaciones[0], pasos: [{ tipo: 'reconstituir', volumenMl: 20 }, { tipo: 'diluir', tomarMl: 1, llevarAMl: 10 }], objetivos: [v.dosis[0].final!] })
    expect(rv.ok && rv.algunaCoincide).toBe(true)
    const g = obtenerOcular('ganciclovir')!
    const rg = verificar({ presentacion: g.presentaciones[0], pasos: [{ tipo: 'reconstituir', volumenMl: 10 }, { tipo: 'diluir', tomarMl: 2, llevarAMl: 5 }], objetivos: [g.dosis[0].final!] })
    expect(rg.ok && rg.algunaCoincide).toBe(true)
  })
  it('discrepancias registradas: ganciclovir (PNT vs consenso), anfotericina (5 vs 10 µg) y foscarnet (frecuencia)', () => {
    expect(obtenerOcular('ganciclovir')!.discrepancias).toHaveLength(1)
    expect(obtenerOcular('anfotericina-b')!.dosis[0].final!.cantidad).toEqual({ min: 5, max: 10, unidad: 'mcg' })
    expect(obtenerOcular('foscarnet')!.discrepancias[0].campo).toContain('Frecuencia')
  })
  it('solo brolucizumab, el implante de dexametasona y ocriplasmina quedan con una sola fuente (la ficha CIMA); el resto está contrastado', () => {
    const unica = INTRAVITREAS.filter((id) => verificacionDeOcular(obtenerOcular(id)!) === 'fuente_unica').sort()
    expect(unica).toEqual(['brolucizumab', 'dexametasona-implante', 'ocriplasmina'])
    for (const id of INTRAVITREAS.filter((x) => !unica.includes(x))) expect(verificacionDeOcular(obtenerOcular(id)!), id).toBe('contrastada')
  })
})

const BLOQUEOS = ['bupivacaina', 'ropivacaina', 'mepivacaina', 'hialuronidasa']
const PERIOCULARES = ['cefazolina', 'gentamicina', 'metilprednisolona', 'betametasona', 'dexametasona']
const ANTIFIBROTICOS = ['mitomicina', 'fluorouracilo', 'toxina-botulinica']

describe('lote 3: bloqueos, perioculares y antifibróticos', () => {
  it('hay 4 bloqueos, 5 perioculares y 3 antifibróticos con toxina, y las 41 fichas suman', () => {
    const por = (fam: string) => oculares.filter((f) => f.familias[0] === fam).map((f) => f.id).sort()
    expect(por('bloqueo')).toEqual([...BLOQUEOS].sort())
    expect(por('periocular')).toEqual([...PERIOCULARES].sort())
    expect(por('antifibrotico')).toEqual([...ANTIFIBROTICOS].sort())
    expect(oculares).toHaveLength(41)
  })
  it('bloqueos y perioculares son informativos: sin protocolos y sin dosis final de concentración', () => {
    for (const id of [...BLOQUEOS, ...PERIOCULARES]) {
      const f = obtenerOcular(id)!
      expect(f.modo, id).toBe('informativa')
      expect(f.protocolos, id).toEqual([])
      expect(f.dosis.every((d) => d.final === undefined), id).toBe(true)
    }
  })
  it('los volúmenes de bloqueo de la ficha técnica y de EyeWiki quedan como texto', () => {
    const b = obtenerOcular('bupivacaina')!
    const texto = (via: string) => b.dosis.find((d) => d.via === via)!.texto
    expect(texto('retrobulbar')).toContain('2 a 4 ml')
    expect(texto('peribulbar')).toContain('6 a 10 ml')
    expect(texto('subtenoniana')).toContain('2 a 5 ml')
  })
  it('ropivacaína es la única no registrada del lote y mepivacaína queda sin pauta', () => {
    const noReg = oculares.filter((f) => [...BLOQUEOS, ...PERIOCULARES, ...ANTIFIBROTICOS].includes(f.id) && f.registroChile === 'no_registrado').map((f) => f.id)
    expect(noReg).toEqual(['ropivacaina'])
    const m = obtenerOcular('mepivacaina')!
    expect(m.sinPauta).not.toBeNull()
    expect(m.dosis).toEqual([])
  })
  it('mitomicina, 5-FU y toxina llevan la alerta «La dosis y el tiempo de aplicación los define el cirujano»', () => {
    for (const id of ANTIFIBROTICOS) {
      const f = obtenerOcular(id)!
      expect(f.altoRiesgo, id).toBe(true)
      expect(f.alertas.join(' '), id).toContain('La dosis y el tiempo de aplicación los define el cirujano')
    }
  })
  it('mitomicina no trae protocolo de reconstitución, pero el verificador acepta 20 mg en 40 ml (0,5 mg/ml) y rechaza 20 mg en 10 ml', () => {
    const f = obtenerOcular('mitomicina')!
    expect(f.protocolos).toEqual([])
    const presentacion = f.presentaciones[0]
    const objetivos = objetivosDe(f, presentacion.id)
    const bien = verificar({ presentacion, pasos: [{ tipo: 'reconstituir', volumenMl: 40 }], objetivos })
    const mal = verificar({ presentacion, pasos: [{ tipo: 'reconstituir', volumenMl: 10 }], objetivos })
    expect(bien.ok && bien.algunaCoincide).toBe(true)
    expect(mal.ok && mal.algunaCoincide).toBe(false)
  })
  it('toxina botulínica: unidades U, alerta de no intercambiables y diluciones de 8, 4 y 2 ml', () => {
    const f = obtenerOcular('toxina-botulinica')!
    expect(f.presentaciones[0].cantidad.unidad).toBe('U')
    expect(f.alertas.join(' ')).toContain('NO son intercambiables')
    expect(f.protocolos.map((p) => p.id)).toEqual(['botox-100-8ml', 'botox-100-4ml', 'botox-100-2ml'])
    const presentacion = f.presentaciones[0]
    const objetivos = objetivosDe(f, presentacion.id)
    const bien = verificar({ presentacion, pasos: [{ tipo: 'reconstituir', volumenMl: 4 }], objetivos })
    const mal = verificar({ presentacion, pasos: [{ tipo: 'reconstituir', volumenMl: 10 }], objetivos })
    expect(bien.ok && bien.algunaCoincide).toBe(true)
    expect(mal.ok && mal.algunaCoincide).toBe(false)
  })
  it('5-FU: el vial de 50 mg/ml sin diluir da 5 mg en 0,1 ml, y 1 ml → 5 ml da la solución de 10 mg/ml', () => {
    const f = obtenerOcular('fluorouracilo')!
    const presentacion = f.presentaciones[0]
    const sinDiluir = verificar({ presentacion, pasos: [], objetivos: [f.dosis[0].final!] })
    expect(sinDiluir.ok && sinDiluir.algunaCoincide).toBe(true)
    const diluido = verificar({ presentacion, pasos: [{ tipo: 'diluir', tomarMl: 1, llevarAMl: 5 }], objetivos: [f.dosis[1].final!] })
    expect(diluido.ok && diluido.algunaCoincide).toBe(true)
  })
  it('gentamicina lleva la alerta de infarto macular y betametasona la discrepancia de 2 mg frente a 5,7 mg', () => {
    expect(obtenerOcular('gentamicina')!.alertas.join(' ')).toContain('INFARTO MACULAR')
    const d = obtenerOcular('betametasona')!.discrepancias[0]
    expect(d.valores.map((v) => v.valor).join(' | ')).toContain('5,7 mg')
  })
  it('estados de verificación: las de una sola fuente son dexametasona, gentamicina, metilprednisolona y toxina', () => {
    const ids = [...BLOQUEOS, ...PERIOCULARES, ...ANTIFIBROTICOS]
    const unica = ids.filter((id) => verificacionDeOcular(obtenerOcular(id)!) === 'fuente_unica').sort()
    expect(unica).toEqual(['dexametasona', 'gentamicina', 'metilprednisolona', 'toxina-botulinica'])
  })
})

describe('conteos finales y grupos de la sección Oftalmología', () => {
  it('hay 41 fichas oculares: 13 intracamerales, 16 intravítreas, 4 bloqueos, 5 perioculares y 3 antifibróticos', () => {
    expect(oculares).toHaveLength(41)
    const porFamilia = (f: string) => oculares.filter((o) => o.familias[0] === f).length
    expect([porFamilia('intracameral'), porFamilia('intravitreo'), porFamilia('bloqueo'), porFamilia('periocular'), porFamilia('antifibrotico')])
      .toEqual([13, 16, 4, 5, 3])
  })

  it('9 fichas no registradas en Chile, todas con ficha FDA o CIMA como fuente', () => {
    const ids = oculares.filter((o) => o.registroChile === 'no_registrado').map((o) => o.id).sort()
    expect(ids).toEqual(['acetilcolina', 'anfotericina-b', 'azul-brillante', 'azul-tripano', 'brolucizumab', 'carbacol', 'fenilefrina-ketorolaco', 'ocriplasmina', 'ropivacaina'])
  })

  it('toda ficha ocular es de alto riesgo', () => {
    expect(oculares.filter((o) => !o.altoRiesgo).map((o) => o.id)).toEqual([])
  })

  it('todo grupo de las fichas oculares y de los orales oftalmológicos tiene etiqueta legible y color propio (nunca neutro)', () => {
    const grupos = new Set([...oculares.map((o) => o.grupo), ...orales.filter((o) => o.usos?.includes('oftalmologia')).map((o) => o.grupo)])
    for (const g of grupos) {
      expect(etiquetaGrupo(g), `etiqueta de ${g}`).not.toBe(g)
      expect(colorGrupo(g), `color de ${g}`).not.toBe('neutro')
    }
  })
})
