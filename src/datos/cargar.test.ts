import { describe, expect, it } from 'vitest'
import { volumenACargar } from '../calculos/calculadoras'
import { fuentes, medicamentos, obtenerFicha } from './cargar'

describe('cargar', () => {
  it('carga las fichas validadas, ordenadas por nombre', () => {
    expect(medicamentos.length).toBeGreaterThanOrEqual(10)
    const nombres = medicamentos.map((m) => m.nombre)
    expect([...nombres].sort((a, b) => a.localeCompare(b, 'es'))).toEqual(nombres)
  })
  it('obtiene una ficha por id', () => expect(obtenerFicha('noradrenalina')?.presentaciones[0].volumenMl).toBe(4))
  it('id inexistente da undefined', () => expect(obtenerFicha('no-existe')).toBeUndefined())
  it('carga las fuentes', () => expect(fuentes.find((f) => f.id === 'PUCON-2022')).toBeTruthy())
  it('cloruro de potasio: alto riesgo y volumen a cargar con la ampolla real (10 ml al 10 % = 13,41 mEq)', () => {
    const kcl = obtenerFicha('cloruro-de-potasio')
    expect(kcl?.altoRiesgo).toBe(true)
    const amp = kcl!.presentaciones[0]
    expect(amp.cantidad).toEqual({ valor: 13.41, unidad: 'mEq' })
    const r = volumenACargar({ valor: 20, unidad: 'mEq' }, { cantidad: amp.cantidad, volumenMl: amp.volumenMl })
    expect(r).toMatchObject({ ok: true, valor: { ml: 14.91, unidades: 2 } })
  })
  it('cefazolina: el volumen a cargar usa la concentración reconstituida (1 g en 10 ml = 100 mg/ml)', () => {
    const cef = obtenerFicha('cefazolina')
    expect(cef?.reconstitucion?.volumenMl).toBe(10)
    const fa = cef!.presentaciones[0]
    expect(fa.volumenMl).toBe(cef!.reconstitucion!.volumenMl)
    const r = volumenACargar({ valor: 2, unidad: 'g' }, { cantidad: fa.cantidad, volumenMl: fa.volumenMl })
    expect(r).toMatchObject({ ok: true, valor: { ml: 20, unidades: 2 } })
  })
})
