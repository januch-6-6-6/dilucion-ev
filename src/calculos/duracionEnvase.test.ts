import { describe, expect, it } from 'vitest'
import { FichaTopica } from '../esquema/ficha-topica'
import { fichaTopicaValida } from '../esquema/__fixtures__/topicos'
import { combinacionesCalculables, duracionEnvase, motivoNoCalculable, validezDe } from './duracionEnvase'

describe('duracionEnvase', () => {
  it('colirio 5 ml, 20 gotas/ml, 1 gota 3 veces al día en ambos ojos → 16 días', () => {
    const r = duracionEnvase({ cantidad: 1, vecesAlDia: 3, sitios: 2, unidad: 'gota', contenido: 5 })
    expect(r).toEqual({ unidadesTotales: 100, consumoDiario: 6, diasPorContenido: 16, dias: 16, limita: 'contenido' })
  })
  it('la validez tras abrir limita cuando es menor', () => {
    const r = duracionEnvase({ cantidad: 1, vecesAlDia: 1, sitios: 1, unidad: 'gota', contenido: 5, validezAbiertoDias: 28 })
    expect(r.diasPorContenido).toBe(100)
    expect(r.dias).toBe(28)
    expect(r.limita).toBe('validez')
  })
  it('spray: el contenido son pulverizaciones; gotasPorMl no se usa', () => {
    const r = duracionEnvase({ cantidad: 2, vecesAlDia: 1, sitios: 2, unidad: 'pulverizacion', contenido: 120, gotasPorMl: 99, validezAbiertoDias: 60 })
    expect(r.unidadesTotales).toBe(120)
    expect(r.dias).toBe(30)
    expect(r.limita).toBe('contenido')
  })
  it('respeta gotas por ml editadas', () => {
    expect(duracionEnvase({ cantidad: 1, vecesAlDia: 2, sitios: 1, unidad: 'gota', contenido: 3, gotasPorMl: 30 }).dias).toBe(45)
  })
  it('rechaza entradas inválidas', () => {
    const base = { cantidad: 1, vecesAlDia: 2, sitios: 1, unidad: 'gota' as const, contenido: 5 }
    expect(() => duracionEnvase({ ...base, contenido: 0 })).toThrow('contenido')
    expect(() => duracionEnvase({ ...base, sitios: 3 })).toThrow('sitios')
    expect(() => duracionEnvase({ ...base, vecesAlDia: Number.NaN })).toThrow()
    expect(() => duracionEnvase({ ...base, gotasPorMl: -1 })).toThrow('gotas por ml')
  })
})

describe('motivoNoCalculable y combinaciones', () => {
  const f = FichaTopica.parse(fichaTopicaValida())
  it('gotas con frecuencia → calculable', () => {
    expect(motivoNoCalculable(f.dosis[0], f.presentaciones[0])).toBeNull()
    expect(combinacionesCalculables(f)).toHaveLength(2)
  })
  it('ungüento, unidosis, sin frecuencia y presentación ajena no son calculables', () => {
    const p = f.presentaciones[0]
    expect(motivoNoCalculable(f.dosis[0], { ...p, forma: 'unguento' })).toBe('unguento')
    expect(motivoNoCalculable({ ...f.dosis[0], unidad: 'cm' }, p)).toBe('unguento')
    expect(motivoNoCalculable(f.dosis[0], { ...p, unidosis: true })).toBe('unidosis')
    expect(motivoNoCalculable({ ...f.dosis[0], vecesAlDia: undefined }, p)).toBe('sin_frecuencia')
    expect(motivoNoCalculable({ ...f.dosis[0], presentaciones: ['otra'] }, p)).toBe('no_aplica_presentacion')
  })
  it('validezDe prefiere la conservación específica de la presentación', () => {
    const g = FichaTopica.parse({
      ...fichaTopicaValida(),
      conservacion: [
        { validezAbiertoDias: 28, texto: 'general', fuente: { ref: 'CIMA', detalle: 'x' } },
        { presentaciones: ['ojo-solucion-0-5'], validezAbiertoDias: 7, texto: 'específica', fuente: { ref: 'CIMA', detalle: 'x' } },
      ],
    })
    expect(validezDe(g, 'ojo-solucion-0-5')).toBe(7)
    expect(validezDe(g, 'otra')).toBe(28)
  })
})
