import { describe, expect, it } from 'vitest'
import { fichaValida, fuentesPrueba } from './__fixtures__/fichas'
import { validarDatos } from './validar'

const f = { ref: 'F1', detalle: 'p. 1' }

describe('validarDatos', () => {
  it('ficha válida no tiene errores', () => expect(validarDatos([fichaValida()], fuentesPrueba)).toEqual([]))

  it('exige fuente en los datos', () => {
    const ficha = fichaValida()
    const { fuente: _omitida, ...sinFuente } = ficha.administracion
    void _omitida
    const errores = validarDatos([{ ...ficha, administracion: sinFuente }], fuentesPrueba)
    expect(errores.join('\n')).toContain('fuente')
  })

  it('la ref debe existir en fuentes.yaml', () => {
    const ficha = fichaValida('droga-a', { estabilidad: { ambienteH: 24, protegerLuz: true, fuente: { ref: 'NOEXISTE', detalle: 'x' } } })
    expect(validarDatos([ficha], fuentesPrueba).join('\n')).toContain('no existe en fuentes.yaml')
  })

  it('min no puede ser mayor que max', () => {
    const ficha = fichaValida('droga-a', { dosis: [{ indicacion: 'X', poblacion: 'adulto', unidad: 'mg', min: 5, max: 1, fuente: f }] })
    expect(validarDatos([ficha], fuentesPrueba).join('\n')).toContain('min mayor que max')
  })

  it('valores numéricos deben ser positivos', () => {
    const ficha = fichaValida('droga-a', { presentaciones: [{ id: 'amp', forma: 'ampolla', cantidad: { valor: -4, unidad: 'mg' }, volumenMl: 4, fuente: f }] })
    expect(validarDatos([ficha], fuentesPrueba).length).toBeGreaterThan(0)
  })

  it('detecta compatibilidad asimétrica', () => {
    const a = fichaValida('droga-a', { compatibilidad: [{ con: 'droga-b', estado: 'incompatible', fuente: f }] })
    const b = fichaValida('droga-b', { compatibilidad: [{ con: 'droga-a', estado: 'compatible', fuente: f }] })
    expect(validarDatos([a, b], fuentesPrueba).join('\n')).toContain('compatibilidad asimétrica')
  })

  it('sinDosisPediatrica debe ser coherente con las dosis', () => {
    const ficha = fichaValida('droga-a', {
      sinDosisPediatrica: true,
      dosis: [{ indicacion: 'X', poblacion: 'pediatrico', unidad: 'mg/kg', max: 1, topeAdulto: { valor: 1, unidad: 'mg' }, fuente: f }],
    })
    expect(validarDatos([ficha], fuentesPrueba).join('\n')).toContain('sinDosisPediatrica')
  })

  it('ids repetidos son error', () => {
    expect(validarDatos([fichaValida(), fichaValida()], fuentesPrueba).join('\n')).toContain('repetido')
  })
})
