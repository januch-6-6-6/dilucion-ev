import { describe, expect, it } from 'vitest'
import { verificar, objetivosDe, type PasoNumerico } from '../calculos/verificadorOcular'
import { validarOculares } from '../esquema/validar-oculares'
import { fuentesOculares, obtenerOcular, oculares, verificacionDeOcular } from './cargarOculares'

describe('datos oculares reales', () => {
  it('todas las fichas y fuentes pasan el validador', () => {
    expect(validarOculares(oculares, fuentesOculares)).toEqual([])
  })
  it('cada protocolo, calculado con verificar(), coincide con su dosis de la fuente', () => {
    for (const f of oculares) {
      for (const p of f.protocolos) {
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
