import { describe, expect, it } from 'vitest'
import { FichaOcular, type DosisFinal, type PresentacionOcular } from '../esquema/ficha-ocular'
import { fichaOcularValida } from '../esquema/__fixtures__/oculares'
import { objetivosDe, presentacionesVerificables, tieneVerificador, verificar, type PasoNumerico } from './verificadorOcular'

const fuente = { ref: 'ISP', detalle: 'x' }
const pres = (p: Partial<PresentacionOcular>): PresentacionOcular => ({
  id: 'p',
  forma: 'polvo',
  cantidad: { valor: 750, unidad: 'mg' },
  registrosIsp: ['F-1/26'],
  usoDirecto: false,
  fuente,
  ...p,
})
const puntual = (valor: number, unidad: 'mg' | 'mcg' | 'U', volumenMl = 0.1): DosisFinal => ({ cantidad: { valor, unidad }, volumenMl })
const rec = (volumenMl: number): PasoNumerico => ({ tipo: 'reconstituir', volumenMl })
const dil = (tomarMl: number, llevarAMl: number): PasoNumerico => ({ tipo: 'diluir', tomarMl, llevarAMl })

describe('verificar', () => {
  it('cefuroxima 750 mg + 7,5 ml → 100 mg/ml; diluir 1→10 → 10 mg/ml = 1 mg/0,1 ml, coincide', () => {
    const r = verificar({ presentacion: pres({}), pasos: [rec(7.5), dil(1, 10)], objetivos: [puntual(1, 'mg')] })
    expect(r).toMatchObject({ ok: true, algunaCoincide: true, volumenDisponibleMl: 10 })
    if (!r.ok) throw new Error()
    expect(r.porMl).toEqual({ valor: 10, unidad: 'mg' })
    expect(r.porVolumenObjetivo[0].valor).toBeCloseTo(1)
    expect(r.comparaciones[0]).toMatchObject({ estado: 'coincide', diferenciaPct: 0 })
  })
  it('Arshinoff: solución 5 mg/ml, diluir 3→10 → 150 mcg/0,1 ml; coincide con 150 y no con 500', () => {
    const vigamox = pres({ forma: 'solucion', cantidad: { valor: 15, unidad: 'mg' }, volumenMl: 3 })
    const r = verificar({ presentacion: vigamox, pasos: [dil(3, 10)], objetivos: [puntual(150, 'mcg'), puntual(500, 'mcg')] })
    if (!r.ok) throw new Error(r.error)
    expect(r.comparaciones.map((c) => c.estado)).toEqual(['coincide', 'no_coincide'])
    expect(r.algunaCoincide).toBe(true)
  })
  it('alteplasa en rango 6–25 mcg/0,1 ml: 50 mg + 50 ml, diluir 1→10 → 10 mcg, coincide', () => {
    const rango: DosisFinal = { cantidad: { min: 6, max: 25, unidad: 'mcg' }, volumenMl: 0.1 }
    const r = verificar({ presentacion: pres({ cantidad: { valor: 50, unidad: 'mg' } }), pasos: [rec(50), dil(1, 10)], objetivos: [rango] })
    if (!r.ok) throw new Error(r.error)
    expect(r.comparaciones[0]).toMatchObject({ estado: 'coincide', diferenciaPct: null })
  })
  it('fuera de rango (30 mcg) → no_coincide', () => {
    const rango: DosisFinal = { cantidad: { min: 6, max: 25, unidad: 'mcg' }, volumenMl: 0.1 }
    const r = verificar({ presentacion: pres({ cantidad: { valor: 50, unidad: 'mg' } }), pasos: [rec(50), dil(3, 10)], objetivos: [rango] })
    if (!r.ok) throw new Error(r.error)
    expect(r.comparaciones[0].estado).toBe('no_coincide')
    expect(r.algunaCoincide).toBe(false)
  })
  it('6 % de diferencia no coincide y 4 % sí', () => {
    // 750 mg / 7,5 ml = 100 mg/ml; tomar 1,06 ml → 106 mg en 10 ml = 1,06 mg/0,1 ml
    const seis = verificar({ presentacion: pres({}), pasos: [rec(7.5), dil(1.06, 10)], objetivos: [puntual(1, 'mg')] })
    const cuatro = verificar({ presentacion: pres({}), pasos: [rec(7.5), dil(1.04, 10)], objetivos: [puntual(1, 'mg')] })
    if (!seis.ok || !cuatro.ok) throw new Error()
    expect(seis.comparaciones[0].estado).toBe('no_coincide')
    expect(seis.comparaciones[0].diferenciaPct).toBeCloseTo(6)
    expect(cuatro.comparaciones[0].estado).toBe('coincide')
  })
  it('errores de pasos', () => {
    const base = { presentacion: pres({}), objetivos: [puntual(1, 'mg')] }
    expect(verificar({ ...base, pasos: [rec(7.5), dil(11, 12)] })).toEqual({ ok: false, error: 'No puedes tomar más volumen del que tienes (7,5 ml).' })
    expect(verificar({ ...base, pasos: [rec(7.5), dil(5, 3)] })).toEqual({ ok: false, error: 'El volumen final no puede ser menor que el que tomaste.' })
    expect(verificar({ ...base, pasos: [rec(0)] })).toEqual({ ok: false, error: 'Los volúmenes deben ser mayores que 0.' })
    expect(verificar({ ...base, pasos: [rec(7.5), dil(1, 2), dil(1, 2), dil(1, 2), dil(1, 2)] })).toEqual({ ok: false, error: 'Máximo 4 pasos.' })
    expect(verificar({ ...base, pasos: [dil(1, 10)] })).toEqual({ ok: false, error: 'Primero reconstituye el polvo.' })
    expect(verificar({ ...base, pasos: [] })).toEqual({ ok: false, error: 'Primero reconstituye el polvo.' })
  })
  it('una solución no se reconstituye', () => {
    const sol = pres({ forma: 'solucion', volumenMl: 3 })
    expect(verificar({ presentacion: sol, pasos: [rec(1)], objetivos: [puntual(1, 'mg')] })).toEqual({ ok: false, error: 'Esta presentación ya es una solución: no se reconstituye.' })
  })
  it('una solución sin volumen no se puede verificar', () => {
    const sol = pres({ forma: 'solucion' })
    expect(verificar({ presentacion: sol, pasos: [dil(1, 2)], objetivos: [puntual(1, 'mg')] })).toEqual({ ok: false, error: 'La presentación no informa su volumen.' })
  })
  it('U frente a mg → error de unidades no comparables, nunca un falso coincide', () => {
    const toxina = pres({ cantidad: { valor: 100, unidad: 'U' } })
    const r = verificar({ presentacion: toxina, pasos: [rec(1)], objetivos: [puntual(1, 'mg')] })
    expect(r).toEqual({ ok: false, error: 'Unidades no comparables: el frasco está en U y la dosis en mg.' })
  })
  it('U frente a U sí se compara', () => {
    const toxina = pres({ cantidad: { valor: 100, unidad: 'U' } })
    const r = verificar({ presentacion: toxina, pasos: [rec(1), dil(1, 10)], objetivos: [puntual(1, 'U', 0.1)] })
    if (!r.ok) throw new Error(r.error)
    expect(r.comparaciones[0].estado).toBe('coincide')
  })
  it('una presentación de uso directo no se verifica', () => {
    const r = verificar({ presentacion: pres({ usoDirecto: true, volumenMl: 0.05 }), pasos: [], objetivos: [puntual(1, 'mg')] })
    expect(r).toEqual({ ok: false, error: 'Esta presentación viene lista para usar: no hay nada que verificar.' })
  })
})

describe('tieneVerificador y objetivosDe', () => {
  it('cefuroxima: sí; informativa: no; solo uso directo: no', () => {
    expect(tieneVerificador(FichaOcular.parse(fichaOcularValida()))).toBe(true)
    const inf = fichaOcularValida()
    inf.modo = 'informativa'
    delete inf.dosis[0].final
    inf.protocolos = []
    expect(tieneVerificador(FichaOcular.parse(inf))).toBe(false)
    const directa = fichaOcularValida()
    directa.presentaciones[0].usoDirecto = true
    directa.presentaciones[0].volumenMl = 0.05
    directa.protocolos = []
    expect(tieneVerificador(FichaOcular.parse(directa))).toBe(false)
  })
  it('objetivosDe respeta las presentaciones de cada dosis', () => {
    const f = fichaOcularValida()
    f.presentaciones.push({ ...f.presentaciones[0], id: 'otra' })
    f.dosis[0].presentaciones = ['otra']
    const ficha = FichaOcular.parse(f)
    expect(objetivosDe(ficha, 'polvo-750')).toEqual([])
    expect(objetivosDe(ficha, 'otra')).toHaveLength(1)
  })
})

describe('volumen disponible frente al volumen de la dosis', () => {
  const jeringa = pres({ forma: 'solucion', cantidad: { valor: 1, unidad: 'mg' }, volumenMl: 0.05 })
  it('la concentración coincide pero queda menos volumen del que pide la dosis: no alcanza y no cuenta como coincidencia', () => {
    const r = verificar({ presentacion: jeringa, pasos: [], objetivos: [puntual(2, 'mg', 0.1)] })
    if (!r.ok) throw new Error(r.error)
    expect(r.comparaciones[0]).toMatchObject({ estado: 'coincide', volumenAlcanza: false })
    expect(r.algunaCoincide).toBe(false)
  })
  it('si el volumen alcanza (diluyendo a 0,1 ml o más) sí coincide', () => {
    const r = verificar({ presentacion: jeringa, pasos: [dil(0.05, 0.1)], objetivos: [puntual(1, 'mg', 0.1)] })
    if (!r.ok) throw new Error(r.error)
    expect(r.comparaciones[0]).toMatchObject({ estado: 'coincide', volumenAlcanza: true })
    expect(r.algunaCoincide).toBe(true)
  })
})

describe('presentacionesVerificables', () => {
  it('excluye las presentaciones sin dosis aplicable y tieneVerificador lo respeta', () => {
    const f = fichaOcularValida()
    f.presentaciones.push({ ...f.presentaciones[0], id: 'otra' })
    f.dosis[0].presentaciones = ['otra']
    const ficha = FichaOcular.parse(f)
    expect(presentacionesVerificables(ficha).map((p) => p.id)).toEqual(['otra'])
    const sola = fichaOcularValida()
    sola.presentaciones.push({ ...sola.presentaciones[0], id: 'directa', usoDirecto: true, volumenMl: 0.05 })
    sola.dosis[0].presentaciones = ['directa']
    sola.protocolos = []
    expect(tieneVerificador(FichaOcular.parse(sola))).toBe(false)
  })
})
