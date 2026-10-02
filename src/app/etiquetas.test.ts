import { describe, expect, it } from 'vitest'
import { medicamentos } from '../datos/cargar'
import { GRUPOS, etiquetaGrupo } from './etiquetas'

describe('etiquetaGrupo', () => {
  it('cada grupo usado en las fichas tiene nombre legible', () => {
    const sinNombre = [...new Set(medicamentos.map((m) => m.grupo))].filter((g) => !(g in GRUPOS))
    expect(sinNombre).toEqual([])
  })

  it('grupo desconocido cae al id', () => expect(etiquetaGrupo('otro-grupo')).toBe('otro-grupo'))
})
