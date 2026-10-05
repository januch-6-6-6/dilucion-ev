import { describe, expect, it } from 'vitest'
import { Fuente } from './ficha'
import { FichaOral } from './ficha-oral'
import { fichaOralValida, fuentesOralesPrueba } from './__fixtures__/orales'
import { validarOrales, verificacionDe } from './validar-orales'

const f = (ref: string) => ({ ref, detalle: 'p. 1' })
const fuentes2 = [
  { id: 'CIMA', titulo: 'CIMA', institucion: 'AEMPS', url: 'https://example.org/a', anio: 2026, consultado: '2026-10-01' },
  { id: 'PED', titulo: 'Pediamécum', institucion: 'AEP', url: 'https://example.org/b', anio: 2026, consultado: '2026-10-01' },
  { id: 'CIMA2', titulo: 'CIMA 2', institucion: 'AEMPS', url: 'https://example.org/c', anio: 2026, consultado: '2026-10-01' },
]
const fuentes = fuentes2.map((x) => Fuente.parse(x))

function conDosis(refs: string[]) {
  const base = fichaOralValida()
  return FichaOral.parse({ ...base, dosis: base.dosis.map((d, i) => ({ ...d, fuente: f(refs[i] ?? refs[0]) })) })
}

describe('verificacionDe', () => {
  it('dos dosis de la misma institución → fuente_unica', () => {
    expect(verificacionDe(conDosis(['CIMA', 'CIMA2']), fuentes)).toBe('fuente_unica')
  })
  it('CIMA + Pediamécum → dos_fuentes', () => {
    expect(verificacionDe(conDosis(['CIMA', 'PED']), fuentes)).toBe('dos_fuentes')
  })
  it('una ref inexistente no suma', () => {
    expect(verificacionDe(conDosis(['CIMA', 'NOPE']), fuentes)).toBe('fuente_unica')
  })
})

describe('validarOrales', () => {
  const val = (ficha: unknown) => validarOrales([ficha], fuentesOralesPrueba)

  it('lista vacía de errores para el fixture válido', () => {
    expect(val(fichaOralValida())).toEqual([])
  })

  it('una referencia de fuente inexistente da error con la ruta', () => {
    const base = fichaOralValida()
    const errores = val({ ...base, administracion: { ...base.administracion, fuente: f('ZZ') } })
    expect(errores.some((e) => e.includes('paracetamol.administracion.fuente') && e.includes('"ZZ"'))).toBe(true)
  })

  it('la dosis pediátrica por toma supera el tope de adulto de la misma ficha → error', () => {
    const base = fichaOralValida()
    const dosis = [base.dosis[0], { ...base.dosis[1], topePorToma: { valor: 2, unidad: 'g' } }]
    const errores = val({ ...base, dosis })
    expect(errores.some((e) => e.includes('dosis[1]') && e.includes('tope de adulto'))).toBe(true)
  })

  it('dosis pediátrica fija que supera el máximo adulto → error; igual o menor no', () => {
    const base = fichaOralValida()
    const fija = { ...base.dosis[1], regimen: 'fija', unidad: 'mg', min: 500, max: 1500 }
    expect(val({ ...base, dosis: [base.dosis[0], fija] }).some((e) => e.includes('tope de adulto'))).toBe(true)
    expect(val({ ...base, dosis: [base.dosis[0], { ...fija, max: 1000 }] })).toEqual([])
  })

  it('unidades no comparables (UI vs mg) no producen error', () => {
    const base = fichaOralValida()
    const fija = { ...base.dosis[1], regimen: 'fija', unidad: 'UI', min: 500, max: 5000 }
    expect(val({ ...base, dosis: [base.dosis[0], fija] })).toEqual([])
  })

  it('min mayor que max en una dosis → error', () => {
    const base = fichaOralValida()
    const errores = val({ ...base, dosis: [{ ...base.dosis[0], min: 2000, max: 1000 }, base.dosis[1]] })
    expect(errores.some((e) => e.includes('dosis[0]') && e.includes('min mayor que max'))).toBe(true)
  })

  it('una discrepancia cuyo mostrado no es el menor de sus valores numéricos → error', () => {
    const base = fichaOralValida()
    const disc = (mostrado: string) => [
      { campo: 'max diario', valores: [{ fuente: 'A', valor: '4 g' }, { fuente: 'B', valor: '3,5 g' }], mostrado, motivo: 'm' },
    ]
    expect(val({ ...base, discrepancias: disc('4 g') }).some((e) => e.includes('discrepancias[0]'))).toBe(true)
    expect(val({ ...base, discrepancias: disc('3,5 g') })).toEqual([])
  })

  it('discrepancia sin número extraíble no se valida', () => {
    const base = fichaOralValida()
    const d = [{ campo: 'x', valores: [{ fuente: 'A', valor: 'según peso' }, { fuente: 'B', valor: '3 g' }], mostrado: '9 g', motivo: 'm' }]
    expect(val({ ...base, discrepancias: d })).toEqual([])
  })

  it('una dosis que cita una presentación inexistente da error con la ruta', () => {
    const base = fichaOralValida()
    const dosis = [{ ...base.dosis[0], presentaciones: ['comp-500', 'fantasma'] }, base.dosis[1]]
    const errores = val({ ...base, dosis })
    expect(errores.some((e) => e.includes('dosis[0].presentaciones[1]') && e.includes('"fantasma"'))).toBe(true)
    expect(errores.some((e) => e.includes('presentaciones[0]'))).toBe(false)
  })

  it('una dosis con presentaciones existentes no da error', () => {
    const base = fichaOralValida()
    const dosis = [{ ...base.dosis[0], presentaciones: ['jarabe-32'] }, base.dosis[1]]
    expect(val({ ...base, dosis })).toEqual([])
  })

  it('id repetido', () => {
    const errores = validarOrales([fichaOralValida(), fichaOralValida()], fuentesOralesPrueba)
    expect(errores).toContain('paracetamol: id repetido')
  })

  it('presentación con id repetido dentro de la ficha', () => {
    const base = fichaOralValida()
    const errores = val({ ...base, presentaciones: [base.presentaciones[0], base.presentaciones[0]] })
    expect(errores.some((e) => e.includes('presentaciones[1]') && e.includes('id repetido'))).toBe(true)
  })

  it('errores de esquema llevan el id y la ruta', () => {
    const errores = val({ ...fichaOralValida(), grupo: '' })
    expect(errores.some((e) => e.startsWith('paracetamol: grupo — '))).toBe(true)
  })
})
