import { describe, expect, it } from 'vitest'
import { FichaTopica } from './ficha-topica'
import { fichaTopicaValida } from './__fixtures__/topicos'

const errores = (x: unknown) => {
  const r = FichaTopica.safeParse(x)
  return r.success ? [] : r.error.issues.map((i) => i.message)
}

describe('FichaTopica', () => {
  it('acepta el fixture válido', () => {
    expect(errores(fichaTopicaValida())).toEqual([])
  })
  it('con_dosis sin dosis pediátrica es error', () => {
    const f = fichaTopicaValida()
    f.dosis = f.dosis.filter((d) => d.poblacion === 'adulto')
    expect(errores(f)).toContain('con_dosis exige al menos una dosis pediátrica')
  })
  it('contraindicada con dosis pediátrica es error', () => {
    const f = fichaTopicaValida()
    f.pediatria = { estado: 'contraindicada', motivo: 'menores de 2 años' }
    expect(errores(f)).toContain('con pediatría contraindicada no puede haber dosis pediátricas')
  })
  it('sin dosis exige sinPauta, y sinPauta prohíbe dosis', () => {
    const vacia = { ...fichaTopicaValida(), dosis: [], pediatria: { estado: 'sin_datos', motivo: 'x' } }
    expect(errores(vacia)).toContain('sin dosis hay que declarar sinPauta con su motivo')
    expect(errores({ ...vacia, sinPauta: { motivo: 'otra concentración' } })).toEqual([])
    expect(errores({ ...fichaTopicaValida(), sinPauta: { motivo: 'x' } })).toContain('una ficha sin pauta no puede tener dosis')
  })
  it('una presentación inexistente en dosis o conservación es error', () => {
    const f = fichaTopicaValida()
    ;(f.dosis as unknown[])[0] = { ...f.dosis[0], presentaciones: ['nope'] }
    ;(f.conservacion as unknown[])[0] = { ...f.conservacion[0], presentaciones: ['nope2'] }
    const e = errores(f)
    expect(e).toContain('la presentación "nope" no existe en presentaciones de esta ficha')
    expect(e).toContain('la presentación "nope2" no existe en presentaciones de esta ficha')
  })
  it('una presentación de una vía no declarada es error', () => {
    const f = fichaTopicaValida()
    f.presentaciones[0].via = 'oido'
    expect(errores(f)).toContain('la vía "oido" no está en vias')
  })
  it('cantidad sin unidad es error', () => {
    const f = fichaTopicaValida()
    delete (f.dosis[0] as { unidad?: string }).unidad
    expect(errores(f)).toContain('cantidad exige unidad')
  })
  it('rechaza campos desconocidos y formas fuera del enum', () => {
    expect(errores({ ...fichaTopicaValida(), extra: 1 }).length).toBeGreaterThan(0)
    const f = fichaTopicaValida()
    f.presentaciones[0].forma = 'comprimido'
    expect(errores(f).length).toBeGreaterThan(0)
  })
})
