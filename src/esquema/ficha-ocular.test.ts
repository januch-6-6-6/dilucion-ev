import { describe, expect, it } from 'vitest'
import { FichaOcular } from './ficha-ocular'
import { fichaOcularValida } from './__fixtures__/oculares'

const errores = (x: unknown) => {
  const r = FichaOcular.safeParse(x)
  return r.success ? [] : r.error.issues.map((i) => i.message)
}

describe('FichaOcular', () => {
  it('acepta la ficha mínima de cefuroxima', () => {
    expect(errores(fichaOcularValida())).toEqual([])
  })
  it('rechaza modo intraocular sin dosis con final', () => {
    const f = fichaOcularValida()
    delete f.dosis[0].final
    f.protocolos = []
    expect(errores(f)).toContain('una ficha intraocular exige al menos una dosis con final')
  })
  it('rechaza un protocolo cuyo resultado difiere más de 5 % de la dosis final', () => {
    const f = fichaOcularValida()
    f.protocolos[0].resultado.valor = 1.1
    expect(errores(f)).toContain('el resultado del protocolo difiere más de 5 % de la dosis final')
  })
  it('acepta un protocolo dentro del 5 % y en otra unidad de masa', () => {
    const f = fichaOcularValida()
    f.protocolos[0].resultado.valor = 1.04
    expect(errores(f)).toEqual([])
    f.protocolos[0].resultado = { valor: 1000, unidad: 'mcg', volumenMl: 0.1 }
    expect(errores(f)).toEqual([])
  })
  it('un resultado dentro de un rango es válido y fuera del rango es error', () => {
    const f = fichaOcularValida()
    f.dosis[0].final = { cantidad: { min: 6, max: 25, unidad: 'mcg' }, volumenMl: 0.1 }
    f.protocolos[0].resultado = { valor: 10, unidad: 'mcg', volumenMl: 0.1 }
    expect(errores(f)).toEqual([])
    f.protocolos[0].resultado.valor = 30
    expect(errores(f)).toContain('el resultado del protocolo queda fuera del rango de la dosis final')
  })
  it('unidades no comparables entre resultado y dosis final es error', () => {
    const f = fichaOcularValida()
    f.protocolos[0].resultado = { valor: 1, unidad: 'U', volumenMl: 0.1 }
    expect(errores(f)).toContain('el resultado del protocolo y la dosis final tienen unidades no comparables')
  })
  it('rechaza un protocolo con dosis o partida inexistente', () => {
    const f = fichaOcularValida()
    f.protocolos[0].dosis = 3
    expect(errores(f)).toContain('el protocolo apunta a una dosis que no existe')
    const g = fichaOcularValida()
    g.protocolos[0].partida = 'nada'
    expect(errores(g)).toContain('la presentación "nada" no existe en presentaciones de esta ficha')
  })
  it('rechaza usoDirecto sin volumenMl', () => {
    const f = fichaOcularValida()
    f.presentaciones[0].usoDirecto = true
    f.protocolos = []
    expect(errores(f)).toContain('usoDirecto exige volumenMl')
  })
  it('rechaza verificado sin registrosIsp', () => {
    const f = fichaOcularValida()
    f.presentaciones[0].registrosIsp = []
    expect(errores(f)).toContain('registroChile verificado exige registrosIsp en alguna presentación')
    f.registroChile = 'no_registrado'
    expect(errores(f)).toEqual([])
  })
  it('acepta una ficha informativa sin final ni protocolos y rechaza que tenga protocolos', () => {
    const f = fichaOcularValida()
    f.modo = 'informativa'
    delete f.dosis[0].final
    f.protocolos = []
    expect(errores(f)).toEqual([])
    const g = fichaOcularValida()
    g.modo = 'informativa'
    expect(errores(g)).toContain('una ficha informativa no tiene protocolos')
  })
  it('sinPauta prohíbe dosis y sin dosis exige sinPauta', () => {
    const f = fichaOcularValida()
    f.sinPauta = { motivo: 'x' }
    expect(errores(f)).toContain('una ficha sin pauta no puede tener dosis')
    const g = fichaOcularValida()
    g.dosis = []
    g.protocolos = []
    expect(errores(g)).toContain('sin dosis hay que declarar sinPauta con su motivo')
    g.sinPauta = { motivo: 'sin fuente' }
    expect(errores(g)).toEqual([])
  })
  it('rechaza altoRiesgo false', () => {
    const f = fichaOcularValida()
    f.altoRiesgo = false
    expect(errores(f).length).toBeGreaterThan(0)
  })
  it('pediatría con_dosis exige dosis pediátrica', () => {
    const f = fichaOcularValida()
    f.pediatria = { estado: 'con_dosis', motivo: 'x' }
    expect(errores(f)).toContain('con_dosis exige al menos una dosis pediátrica')
  })
  it('acepta la vía subretiniana (alteplasa en hemorragia submacular)', () => {
    const f = fichaOcularValida()
    f.dosis[0].via = 'subretiniana'
    expect(errores(f)).toEqual([])
  })
})
