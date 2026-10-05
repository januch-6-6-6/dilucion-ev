import { describe, expect, it } from 'vitest'
import type { DosisOral, PresentacionOral } from '../esquema/ficha-oral'
import { calcularFija, calcularPorPeso } from './oral'

const basePres = {
  liberacionProlongada: false,
  registroChile: 'sin_verificar',
  fuente: { id: 'x' },
} as unknown as Partial<PresentacionOral>
const pres = (p: Partial<PresentacionOral>) => ({ id: 'p', partible: 'no', ...basePres, ...p }) as PresentacionOral
const dosis = (d: Partial<DosisOral>) =>
  ({
    indicacion: 'x',
    poblacion: 'pediatrico',
    regimen: 'por_peso',
    base: 'toma',
    unidad: 'mg/kg',
    estatus: 'autorizada',
    fuente: { id: 'x' },
    ...d,
  }) as DosisOral

const jarabe100 = pres({ forma: 'jarabe', concentracion: { valor: 100, unidad: 'mg' } })
const comp = (valor: number, partible: PresentacionOral['partible'] = 'no') =>
  pres({ forma: 'comprimido', cantidad: { valor, unidad: 'mg' }, partible })

describe('calcularPorPeso', () => {
  it('paracetamol 15 mg/kg por toma, 10 kg, jarabe → 150 mg, 1,5 ml, 4 tomas, 600 mg', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 15, intervaloH: 6 }), presentacion: jarabe100 })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma).toEqual({ valor: 150, unidad: 'mg' })
    expect(r.valor.salida).toEqual({ tipo: 'ml', ml: 1.5 })
    expect(r.valor.tomasPorDia).toBe(4)
    expect(r.valor.totalDiario).toEqual({ valor: 600, unidad: 'mg' })
    expect(r.valor.limitadaPor).toEqual([])
    expect(r.valor.alertas).toEqual([])
    expect(r.pasos.length).toBeGreaterThan(0)
  })
  it('por día: 40 mg/kg/día en 3 tomas, 12 kg → 160 mg por toma', () => {
    const r = calcularPorPeso({ pesoKg: 12, dosis: dosis({ base: 'dia', max: 40, tomasPorDia: 3 }), presentacion: jarabe100 })
    expect(r.ok && r.valor.mgPorToma).toEqual({ valor: 160, unidad: 'mg' })
    expect(r.ok && r.valor.totalDiario).toEqual({ valor: 480, unidad: 'mg' })
  })
  it('usa min si no hay max', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ min: 10, tomasPorDia: 2 }), presentacion: jarabe100 })
    expect(r.ok && r.valor.mgPorToma.valor).toBe(100)
  })
  it('tope por toma: 15 mg/kg × 70 kg con tope 1000 mg → 1000 mg y alerta roja', () => {
    const r = calcularPorPeso({
      pesoKg: 70,
      dosis: dosis({ max: 15, tomasPorDia: 2, topePorToma: { valor: 1000, unidad: 'mg' } }),
      presentacion: comp(500),
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma.valor).toBe(1000)
    expect(r.valor.limitadaPor).toContain('tope por toma')
    expect(r.valor.alertas.some((a) => a.nivel === 'rojo' && a.mensaje.includes('1050'))).toBe(true)
  })
  it('tope diario: 4 tomas de 500 mg con tope 1500 mg → 375 mg y alerta', () => {
    const r = calcularPorPeso({
      pesoKg: 50,
      dosis: dosis({ max: 10, tomasPorDia: 4, topeDiario: { valor: 1500, unidad: 'mg' } }),
      presentacion: jarabe100,
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma.valor).toBe(375)
    expect(r.valor.totalDiario?.valor).toBe(1500)
    expect(r.valor.limitadaPor).toContain('tope diario')
    expect(r.valor.alertas).toHaveLength(1)
  })
  it('nunca supera el tope de adulto por toma', () => {
    const r = calcularPorPeso({
      pesoKg: 80,
      dosis: dosis({ max: 10, tomasPorDia: 3 }),
      presentacion: comp(250),
      topeAdulto: { porToma: { valor: 500, unidad: 'mg' } },
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma.valor).toBe(500)
    expect(r.valor.limitadaPor.some((s) => s.includes('tope de adulto'))).toBe(true)
    expect(r.valor.alertas.length).toBe(1)
  })
  it('tope de adulto diario reduce la toma', () => {
    const r = calcularPorPeso({
      pesoKg: 80,
      dosis: dosis({ max: 10, tomasPorDia: 4 }),
      presentacion: jarabe100,
      topeAdulto: { diario: { valor: 2 , unidad: 'g' } },
    })
    expect(r.ok && r.valor.mgPorToma.valor).toBe(500)
    expect(r.ok && r.valor.limitadaPor.some((s) => s.includes('tope de adulto'))).toBe(true)
  })
  it('un resultado exactamente igual al tope no se reporta como limitado', () => {
    const r = calcularPorPeso({
      pesoKg: 100,
      dosis: dosis({ max: 10, tomasPorDia: 2, topePorToma: { valor: 1000, unidad: 'mg' }, topeDiario: { valor: 2000, unidad: 'mg' } }),
      presentacion: jarabe100,
      topeAdulto: { porToma: { valor: 1, unidad: 'g' }, diario: { valor: 2, unidad: 'g' } },
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.limitadaPor).toEqual([])
    expect(r.valor.alertas).toEqual([])
  })
  it('base dia sin tomas → error', () => {
    const r = calcularPorPeso({ pesoKg: 12, dosis: dosis({ base: 'dia', max: 40 }), presentacion: jarabe100 })
    expect(r).toEqual({ ok: false, error: 'Falta el número de tomas por día' })
  })
  it.each([0, -5, NaN, Infinity])('peso %s → error', (pesoKg) => {
    const r = calcularPorPeso({ pesoKg, dosis: dosis({ max: 10, tomasPorDia: 2 }), presentacion: jarabe100 })
    expect(r).toEqual({ ok: false, error: 'Falta el peso' })
  })
  it('peso 400 → ok con alerta roja de rango', () => {
    const r = calcularPorPeso({ pesoKg: 400, dosis: dosis({ max: 1, tomasPorDia: 2 }), presentacion: jarabe100 })
    expect(r.ok).toBe(true)
    expect(r.ok && r.valor.alertas.some((a) => a.nivel === 'rojo' && a.mensaje === 'Peso fuera del rango habitual (1–150 kg)')).toBe(true)
  })
  it('ondansetrón 2 mg con comprimido de 4 mg no partible → error', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 0.2, tomasPorDia: 2 }), presentacion: comp(4, 'no') })
    expect(r).toEqual({ ok: false, error: 'Esta presentación no permite esa dosis' })
  })
  it('ondansetrón 2 mg con 4 mg partible en mitades → 0,5 unidades', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 0.2, tomasPorDia: 2 }), presentacion: comp(4, 'mitades') })
    expect(r.ok && r.valor.salida).toMatchObject({ tipo: 'unidades', unidades: 0.5, porcentaje: 1 })
    expect(r.ok && r.valor.alertas).toEqual([])
  })
  it('fracción que entrega < 90 %: 130 mg con comprimido de 100 mg en mitades → 100 mg (77 %) y alerta', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 13, tomasPorDia: 2 }), presentacion: comp(100, 'mitades') })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.salida).toMatchObject({ tipo: 'unidades', unidades: 1, entregado: { valor: 100, unidad: 'mg' } })
    expect(r.valor.alertas.some((a) => a.nivel === 'rojo' && a.mensaje.includes('77'))).toBe(true)
  })
  it('gotas: salida en gotas', () => {
    const g = pres({ forma: 'gotas', concentracion: { valor: 2, unidad: 'mg' }, gotasPorMl: 20 })
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 0.5, tomasPorDia: 2 }), presentacion: g })
    expect(r.ok && r.valor.salida).toEqual({ tipo: 'gotas', gotas: 50 })
  })
  it('dosis menor a una gota → error', () => {
    const g = pres({ forma: 'gotas', concentracion: { valor: 2, unidad: 'mg' }, gotasPorMl: 20 })
    const r = calcularPorPeso({ pesoKg: 1, dosis: dosis({ max: 0.05, tomasPorDia: 2 }), presentacion: g })
    expect(r).toEqual({ ok: false, error: 'La dosis es menor a una gota' })
  })
})

describe('calcularFija', () => {
  const fija = (d: Partial<DosisOral>) => dosis({ poblacion: 'adulto', regimen: 'fija', base: undefined, unidad: 'mg', ...d })
  it('adulto 500 mg c/8 h con comprimidos de 500 mg → 1 unidad, 3 tomas, 1500 mg', () => {
    const r = calcularFija({ dosis: fija({ max: 500, intervaloH: 8 }), presentacion: comp(500) })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.salida).toMatchObject({ tipo: 'unidades', unidades: 1 })
    expect(r.valor.tomasPorDia).toBe(3)
    expect(r.valor.totalDiario).toEqual({ valor: 1500, unidad: 'mg' })
    expect(r.valor.alertas).toEqual([])
  })
  it('superar topeDiario da alerta', () => {
    const r = calcularFija({
      dosis: fija({ max: 500, intervaloH: 8, topeDiario: { valor: 1000, unidad: 'mg' } }),
      presentacion: jarabe100,
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.limitadaPor).toContain('tope diario')
    expect(r.valor.alertas.some((a) => a.nivel === 'rojo')).toBe(true)
    expect(r.valor.mgPorToma).toEqual({ valor: 333.333, unidad: 'mg' })
    expect(r.valor.totalDiario?.valor).toBe(999.999)
  })
  it('un tope que hace imposible la presentación lo declara como causa', () => {
    const r = calcularFija({
      dosis: fija({ max: 500, intervaloH: 8, topeDiario: { valor: 1000, unidad: 'mg' } }),
      presentacion: comp(500),
    })
    expect(r.ok).toBe(false)
    if (r.ok) return
    expect(r.error).toContain('Esta presentación no permite esa dosis')
    expect(r.error).toContain('La dosis se limitó a 333,333 mg por el tope diario')
  })
  it('sin tomas conocidas, el tope diario limita la toma igualmente', () => {
    const r = calcularFija({ dosis: fija({ max: 5000, topeDiario: { valor: 4, unidad: 'g' } }), presentacion: jarabe100 })
    expect(r.ok && r.valor.mgPorToma.valor).toBe(4000)
    expect(r.ok && r.valor.limitadaPor).toContain('tope diario')
    expect(r.ok && r.valor.alertas).toHaveLength(1)
  })
  it('rechaza dosis por peso y por edad', () => {
    expect(calcularFija({ dosis: dosis({ max: 15 }), presentacion: jarabe100 })).toMatchObject({ ok: false })
    const e = calcularFija({ dosis: fija({ regimen: 'por_edad', max: 250, texto: 't' }), presentacion: jarabe100 })
    expect(e).toEqual({ ok: false, error: 'Esta dosis es por edad: se muestra como pauta, no se calcula' })
  })
  it('sin tomas conocidas: tomasPorDia y total nulos', () => {
    const r = calcularFija({ dosis: fija({ max: 500 }), presentacion: comp(500) })
    expect(r.ok && r.valor.tomasPorDia).toBeNull()
    expect(r.ok && r.valor.totalDiario).toBeNull()
  })
  it('dosis menor a una gota → error', () => {
    const g = pres({ forma: 'gotas', concentracion: { valor: 2, unidad: 'mg' }, gotasPorMl: 20 })
    expect(calcularFija({ dosis: fija({ max: 0.05 }), presentacion: g })).toEqual({ ok: false, error: 'La dosis es menor a una gota' })
  })
})

describe('calcularPorPeso: régimen, topes y redondeo (ronda de correcciones)', () => {
  it.each([
    ['por_edad', 'Esta dosis es por edad: se muestra como pauta, no se calcula'],
    ['por_superficie', 'Esta dosis es por superficie corporal: se muestra como pauta, no se calcula'],
  ] as const)('régimen %s → error', (regimen, error) => {
    const r = calcularPorPeso({ pesoKg: 20, dosis: dosis({ regimen, unidad: 'mg', max: 250, tomasPorDia: 3, texto: 't' }), presentacion: jarabe100 })
    expect(r).toEqual({ ok: false, error })
  })
  it('dosis fija pasada a calcularPorPeso → error', () => {
    const r = calcularPorPeso({ pesoKg: 20, dosis: dosis({ regimen: 'fija', unidad: 'mg', max: 250, tomasPorDia: 3 }), presentacion: jarabe100 })
    expect(r).toMatchObject({ ok: false })
  })
  it('por_peso con unidad sin /kg → error', () => {
    const r = calcularPorPeso({ pesoKg: 20, dosis: dosis({ unidad: 'mg', max: 250, tomasPorDia: 3 }), presentacion: jarabe100 })
    expect(r).toMatchObject({ ok: false })
  })
  it('tope diario con tomas desconocidas limita la toma, con alerta', () => {
    const r = calcularPorPeso({
      pesoKg: 80,
      dosis: dosis({ max: 60, topeDiario: { valor: 4000, unidad: 'mg' } }),
      presentacion: jarabe100,
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma.valor).toBe(4000)
    expect(r.valor.limitadaPor).toContain('tope diario')
    expect(r.valor.alertas).toHaveLength(1)
  })
  it('tope de adulto diario con tomas desconocidas limita la toma', () => {
    const r = calcularPorPeso({
      pesoKg: 80,
      dosis: dosis({ max: 60 }),
      presentacion: jarabe100,
      topeAdulto: { diario: { valor: 4, unidad: 'g' } },
    })
    expect(r.ok && r.valor.mgPorToma.valor).toBe(4000)
    expect(r.ok && r.valor.limitadaPor.some((s) => s.includes('tope de adulto'))).toBe(true)
  })
  it('el tope por peso con presentación imposible declara el tope como causa', () => {
    const r = calcularPorPeso({
      pesoKg: 70,
      dosis: dosis({ max: 15, tomasPorDia: 2, topePorToma: { valor: 1000, unidad: 'mg' } }),
      presentacion: comp(1500),
    })
    expect(r.ok).toBe(false)
    expect(!r.ok && r.error).toContain('La dosis se limitó a 1000 mg por el tope por toma')
  })
  it('al limitar por tope diario redondea hacia abajo: 300 mg × 6 con tope 1000 → 166,666 (total 999,996)', () => {
    const r = calcularPorPeso({
      pesoKg: 10,
      dosis: dosis({ max: 30, tomasPorDia: 6, topeDiario: { valor: 1000, unidad: 'mg' } }),
      presentacion: jarabe100,
    })
    expect(r.ok && r.valor.mgPorToma.valor).toBe(166.666)
    expect(r.ok && r.valor.totalDiario?.valor).toBe(999.996)
  })
  it.each([
    [5, 5],
    [6, 4],
    [8, 3],
    [12, 2],
  ])('intervalo c/%s h → %s tomas por día (hacia arriba)', (intervaloH, n) => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 10, intervaloH }), presentacion: jarabe100 })
    expect(r.ok && r.valor.tomasPorDia).toBe(n)
  })
  it('820 mg c/5 h contra tope diario de 4000 mg se limita', () => {
    const r = calcularPorPeso({
      pesoKg: 82,
      dosis: dosis({ max: 10, intervaloH: 5, topeDiario: { valor: 4000, unidad: 'mg' } }),
      presentacion: jarabe100,
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma.valor).toBe(800)
    expect(r.valor.limitadaPor).toContain('tope diario')
  })
  it('dos topes por toma: la segunda alerta no llama "calculada" a la dosis ya limitada', () => {
    const r = calcularPorPeso({
      pesoKg: 100,
      dosis: dosis({ max: 15, tomasPorDia: 2, topePorToma: { valor: 1000, unidad: 'mg' } }),
      presentacion: jarabe100,
      topeAdulto: { porToma: { valor: 500, unidad: 'mg' } },
    })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.mgPorToma.valor).toBe(500)
    expect(r.valor.alertas).toHaveLength(2)
    expect(r.valor.alertas[0].mensaje).toContain('calculada (1500 mg)')
    expect(r.valor.alertas[1].mensaje).not.toContain('La dosis calculada (1000')
    expect(r.valor.alertas[1].mensaje).toContain('calculada 1500 mg')
  })
})

describe('dosis restringida a presentaciones (presentaciones)', () => {
  const tramadolRetard = pres({ id: 'ret-100', forma: 'comprimido', cantidad: { valor: 100, unidad: 'mg' }, partible: 'no', liberacionProlongada: true })
  const tramadolIr = pres({ id: 'ir-50', forma: 'capsula', cantidad: { valor: 50, unidad: 'mg' }, partible: 'no', liberacionProlongada: false })
  const ficha = [tramadolRetard, tramadolIr]
  const soloIr = { presentaciones: ['ir-50'] }

  it('presentación aplicable: calcula igual que sin restricción', () => {
    const r = calcularFija({ dosis: fijaAdulto({ max: 50, intervaloH: 6, ...soloIr }), presentacion: tramadolIr, presentacionesDeFicha: ficha })
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.valor.salida).toMatchObject({ tipo: 'unidades', unidades: 1 })
  })

  it('presentación no aplicable: error que nombra las aplicables, sin calcular', () => {
    const r = calcularFija({ dosis: fijaAdulto({ max: 50, intervaloH: 6, ...soloIr }), presentacion: tramadolRetard, presentacionesDeFicha: ficha })
    expect(r).toEqual({ ok: false, error: 'Esta dosis no aplica a esta presentación: usa capsula 50 mg' })
  })

  it('por peso: presentación no aplicable devuelve el error, sin calcular', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 10, tomasPorDia: 2, ...soloIr }), presentacion: tramadolRetard, presentacionesDeFicha: ficha })
    expect(r).toEqual({ ok: false, error: 'Esta dosis no aplica a esta presentación: usa capsula 50 mg' })
  })

  it('sin lista de la ficha, el error usa los ids aplicables', () => {
    const r = calcularFija({ dosis: fijaAdulto({ max: 50, ...soloIr }), presentacion: tramadolRetard })
    expect(r).toEqual({ ok: false, error: 'Esta dosis no aplica a esta presentación: usa ir-50' })
  })

  it('sin presentaciones en la dosis, calcula con cualquier presentación (como antes)', () => {
    const r = calcularPorPeso({ pesoKg: 10, dosis: dosis({ max: 10, tomasPorDia: 2 }), presentacion: tramadolRetard, presentacionesDeFicha: ficha })
    expect(r.ok).toBe(true)
    const f = calcularFija({ dosis: fijaAdulto({ max: 100 }), presentacion: tramadolRetard })
    expect(f.ok).toBe(true)
  })
})

const fijaAdulto = (d: Partial<DosisOral>) => dosis({ poblacion: 'adulto', regimen: 'fija', base: undefined, unidad: 'mg', ...d })
