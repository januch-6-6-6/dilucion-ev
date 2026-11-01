import { describe, expect, it } from 'vitest'
import { Fuente } from './ficha'
import { FichaOcular } from './ficha-ocular'
import { fichaOcularValida, fuentesOcularesPrueba } from './__fixtures__/oculares'
import { validarOculares, verificacionOcular } from './validar-oculares'

const fuentes = fuentesOcularesPrueba.map((x) => Fuente.parse(x))
const val = (ficha: unknown) => validarOculares([ficha], fuentesOcularesPrueba)

describe('verificacionOcular', () => {
  it('tambien de otra institución → contrastada', () => {
    const f = fichaOcularValida()
    f.dosis[0].tambien = [{ ref: 'EYEWIKI', detalle: 'x' }]
    expect(verificacionOcular(FichaOcular.parse(f), fuentes)).toBe('contrastada')
  })
  it('tambien de la misma institución → fuente_unica', () => {
    const f = fichaOcularValida()
    f.dosis[0].tambien = [{ ref: 'PNT2', detalle: 'x' }]
    expect(verificacionOcular(FichaOcular.parse(f), fuentes)).toBe('fuente_unica')
  })
  it('ficha sin pauta → sin_pauta', () => {
    const f = { ...fichaOcularValida(), dosis: [], protocolos: [], sinPauta: { motivo: 'x' } }
    expect(verificacionOcular(FichaOcular.parse(f), fuentes)).toBe('sin_pauta')
  })
})

describe('validarOculares', () => {
  it('fixture válido → sin errores', () => {
    expect(val(fichaOcularValida())).toEqual([])
  })
  it('detecta fuentes inexistentes en dosis, tambien, protocolo y discrepancia', () => {
    const f = fichaOcularValida()
    f.dosis[0].fuente.ref = 'NOPE1'
    f.dosis[0].tambien = [{ ref: 'NOPE2', detalle: 'x' }]
    f.protocolos[0].fuente.ref = 'NOPE3'
    f.discrepancias = [{ campo: 'c', valores: [{ fuente: 'NOPE4', valor: 'v' }], mostrado: 'm', motivo: 'm' }]
    const e = val(f).join('\n')
    for (const n of ['NOPE1', 'NOPE2', 'NOPE3', 'NOPE4']) expect(e).toContain(`"${n}"`)
    expect(e).toContain('fuentes-oftalmo.yaml')
  })
  it('detecta ids repetidos de ficha y de presentación', () => {
    const f = fichaOcularValida()
    f.presentaciones.push({ ...f.presentaciones[0] })
    const e = validarOculares([f, fichaOcularValida()], fuentesOcularesPrueba)
    expect(e).toContain('cefuroxima: id repetido')
    expect(e.some((x) => x.includes('id repetido "polvo-750"'))).toBe(true)
  })
  it('informa el error de esquema con su ruta', () => {
    const f = fichaOcularValida()
    f.dosis[0].via = 'oral'
    expect(val(f)[0]).toMatch(/^cefuroxima: dosis\[0\]\.via/)
  })
})
