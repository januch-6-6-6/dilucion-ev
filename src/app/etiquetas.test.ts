import { describe, expect, it } from 'vitest'
import { medicamentos } from '../datos/cargar'
import { GRUPOS, etiquetaGrupo } from './etiquetas'

const NUEVOS_ORALES: Record<string, string> = {
  aine: 'Antiinflamatorios (AINE)',
  'relajante-muscular': 'Relajantes musculares',
  antigotoso: 'Antigotosos',
  antiparasitario: 'Antiparasitarios',
  antianginoso: 'Antianginosos',
  hipolipemiante: 'Hipolipemiantes',
  digestivo: 'Digestivos',
  antidiabetico: 'Antidiabéticos',
  hormonal: 'Hormonales',
  antidepresivo: 'Antidepresivos',
  'hipnotico-ansiolitico': 'Hipnóticos y ansiolíticos',
  'vitamina-mineral': 'Vitaminas y minerales',
}

describe('etiquetaGrupo', () => {
  it('los grupos nuevos de orales tienen etiqueta propia distinta del id', () => {
    for (const [id, nombre] of Object.entries(NUEVOS_ORALES)) {
      expect(etiquetaGrupo(id)).toBe(nombre)
      expect(etiquetaGrupo(id)).not.toBe(id)
    }
  })

  it('cada grupo usado en las fichas tiene nombre legible', () => {
    const sinNombre = [...new Set(medicamentos.map((m) => m.grupo))].filter((g) => !(g in GRUPOS))
    expect(sinNombre).toEqual([])
  })

  it('grupo desconocido cae al id', () => expect(etiquetaGrupo('otro-grupo')).toBe('otro-grupo'))
})
