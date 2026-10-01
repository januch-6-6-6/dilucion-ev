import { describe, expect, it } from 'vitest'
import { colorGrupo } from './colores'

describe('colorGrupo', () => {
  it('cada grupo conocido tiene su color', () => {
    expect(colorGrupo('vasoactivo')).toBe('naranjo')
    expect(colorGrupo('antiarritmico')).toBe('violeta')
    expect(colorGrupo('sedante')).toBe('indigo')
    expect(colorGrupo('analgesico-opioide')).toBe('azul')
    expect(colorGrupo('anestesico')).toBe('turquesa')
    expect(colorGrupo('electrolito')).toBe('verde')
    expect(colorGrupo('anticolinergico')).toBe('ambar')
  })
  it('un grupo nuevo sin color usa el neutro (nunca rojo, reservado a alertas)', () => expect(colorGrupo('antibiotico-x')).toBe('neutro'))
})
