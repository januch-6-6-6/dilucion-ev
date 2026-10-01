import { describe, expect, it } from 'vitest'
import { medicamentos } from '../datos/cargar'
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
  it('grupos de v0.2', () => {
    const tabla: Record<string, string> = {
      vasoactivo: 'naranjo', antiarritmico: 'violeta', antihipertensivo: 'violeta', diuretico: 'violeta', sedante: 'indigo',
      anticonvulsivante: 'indigo', antipsicotico: 'indigo', 'analgesico-opioide': 'azul', 'analgesico-no-opioide': 'azul',
      anestesico: 'turquesa', 'bloqueador-neuromuscular': 'turquesa', antiemetico: 'lima', 'protector-gastrico': 'lima',
      corticoide: 'lima', electrolito: 'verde', metabolico: 'verde', hematologico: 'neutro', antiinfeccioso: 'cian',
      antidoto: 'ambar', antihistaminico: 'ambar', anticolinergico: 'ambar',
    }
    for (const [g, c] of Object.entries(tabla)) expect(colorGrupo(g)).toBe(c)
  })
  it('todo grupo usado en los datos tiene color (salvo hematológico)', () => {
    for (const m of medicamentos) if (m.grupo !== 'hematologico') expect(colorGrupo(m.grupo), m.id).not.toBe('neutro')
  })
  it('un grupo nuevo sin color usa el neutro (nunca rojo, reservado a alertas)', () => expect(colorGrupo('antibiotico-x')).toBe('neutro'))
})
