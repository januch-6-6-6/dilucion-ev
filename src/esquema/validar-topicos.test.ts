import { describe, expect, it } from 'vitest'
import { Fuente } from './ficha'
import { FichaTopica } from './ficha-topica'
import { fichaTopicaValida, fuentesTopicasPrueba } from './__fixtures__/topicos'
import { validarTopicos, verificacionTopica } from './validar-topicos'

const fuentes = fuentesTopicasPrueba.map((x) => Fuente.parse(x))

describe('verificacionTopica', () => {
  it('una pauta con segunda fuente de otra institución → contrastada', () => {
    expect(verificacionTopica(FichaTopica.parse(fichaTopicaValida()), fuentes)).toBe('contrastada')
  })
  it('segunda fuente de la misma institución → fuente_unica', () => {
    const f = fichaTopicaValida()
    f.dosis[1].tambien = [{ ref: 'CIMA2', detalle: 'x' }]
    expect(verificacionTopica(FichaTopica.parse(f), fuentes)).toBe('fuente_unica')
  })
  it('pautas distintas de instituciones distintas NO cuentan como contraste', () => {
    const f = fichaTopicaValida()
    delete f.dosis[1].tambien
    f.dosis[1].fuente = { ref: 'PED', detalle: 'pauta pediátrica' }
    expect(verificacionTopica(FichaTopica.parse(f), fuentes)).toBe('fuente_unica')
  })
  it('ficha sin pauta → sin_pauta', () => {
    const f = { ...fichaTopicaValida(), dosis: [], sinPauta: { motivo: 'x' }, pediatria: { estado: 'sin_datos', motivo: 'x' } }
    expect(verificacionTopica(FichaTopica.parse(f), fuentes)).toBe('sin_pauta')
  })
})

describe('validarTopicos', () => {
  const val = (ficha: unknown) => validarTopicos([ficha], fuentesTopicasPrueba)
  it('fixture válido → sin errores', () => {
    expect(val(fichaTopicaValida())).toEqual([])
  })
  it('detecta fuentes inexistentes en fuente, tambien y discrepancias', () => {
    const f = fichaTopicaValida()
    f.dosis[0].fuente.ref = 'NOPE1'
    f.dosis[1].tambien = [{ ref: 'NOPE2', detalle: 'x' }]
    ;(f.discrepancias as unknown[]) = [{ campo: 'c', valores: [{ fuente: 'NOPE3', valor: 'v' }], mostrado: 'm', motivo: 'm' }]
    const e = val(f).join('\n')
    expect(e).toContain('"NOPE1"')
    expect(e).toContain('"NOPE2"')
    expect(e).toContain('"NOPE3"')
  })
  it('detecta ids repetidos de ficha y de presentación', () => {
    const f = fichaTopicaValida()
    f.presentaciones.push({ ...f.presentaciones[0] })
    const e = validarTopicos([f, fichaTopicaValida()], fuentesTopicasPrueba)
    expect(e).toContain('colirio-x: id repetido')
    expect(e.some((x) => x.includes('id repetido "ojo-solucion-0-5"'))).toBe(true)
  })
  it('informa el error de esquema con su ruta', () => {
    const f = fichaTopicaValida()
    f.dosis[0].poblacion = 'anciano'
    expect(val(f)[0]).toMatch(/^colirio-x: dosis\[0\]\.poblacion/)
  })
})
