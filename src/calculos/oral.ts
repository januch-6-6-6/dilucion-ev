import type { DosisOral, PresentacionOral } from '../esquema/ficha-oral'
import type { Alerta } from './alertas'
import type { Resultado } from './calculadoras'
import { masaAGotas, masaAMl, masaAUnidades } from './oralConversion'
import { redondear } from './redondeo'
import { convertirMasa, type Cantidad, type UnidadMasa } from './unidades'

export type SalidaPresentacion =
  | { tipo: 'ml'; ml: number }
  | { tipo: 'gotas'; gotas: number }
  | { tipo: 'unidades'; unidades: number; entregado: Cantidad; porcentaje: number }

export type ResultadoOral = {
  mgPorToma: Cantidad
  tomasPorDia: number | null
  totalDiario: Cantidad | null
  salida: SalidaPresentacion
  limitadaPor: string[]
  alertas: Alerta[]
}

type TopeAdulto = { porToma?: Cantidad; diario?: Cantidad }

const TOLERANCIA = 1e-6
const positivo = (n: number | undefined): n is number => typeof n === 'number' && Number.isFinite(n) && n > 0
const error = (mensaje: string): { ok: false; error: string } => ({ ok: false, error: mensaje })
const fmt = (n: number) => String(n).replace('.', ',')
const rojo = (mensaje: string): Alerta => ({ nivel: 'rojo', mensaje })
const excede = (valor: number, tope: number) => valor > tope + TOLERANCIA * Math.max(1, Math.abs(tope))

function aUnidad(c: Cantidad, unidad: UnidadMasa): number | { ok: false; error: string } {
  try {
    return convertirMasa(c.valor, c.unidad, unidad)
  } catch (e) {
    return error((e as Error).message)
  }
}

type Tope = { cantidad: Cantidad; etiqueta: string }

/** Núcleo común: recibe la toma ya calculada (en `unidad`), aplica topes y convierte a la presentación. */
function resolver(p: {
  toma: number
  unidad: UnidadMasa
  presentacion: PresentacionOral
  tomasPorDia: number | null
  topesToma: Tope[]
  topesDiarios: Tope[]
  pasos: string[]
  alertas: Alerta[]
}): Resultado<ResultadoOral> {
  const { unidad, tomasPorDia, presentacion } = p
  const pasos = [...p.pasos]
  const alertas = [...p.alertas]
  const limitadaPor: string[] = []
  let toma = redondear(p.toma, 3)

  for (const t of p.topesToma) {
    const tope = aUnidad(t.cantidad, unidad)
    if (typeof tope !== 'number') return tope
    if (excede(toma, tope)) {
      const nuevo = redondear(tope, 3)
      limitadaPor.push(t.etiqueta)
      alertas.push(rojo(`La dosis calculada (${fmt(toma)} ${unidad}) supera el ${t.etiqueta} (${fmt(nuevo)} ${unidad}); se limitó a ${fmt(nuevo)} ${unidad}.`))
      pasos.push(`Se limita por ${t.etiqueta}: ${fmt(toma)} ${unidad} → ${fmt(nuevo)} ${unidad}`)
      toma = nuevo
    }
  }

  if (tomasPorDia !== null) {
    for (const t of p.topesDiarios) {
      const tope = aUnidad(t.cantidad, unidad)
      if (typeof tope !== 'number') return tope
      const total = toma * tomasPorDia
      if (excede(total, tope)) {
        const nuevo = redondear(tope / tomasPorDia, 3)
        limitadaPor.push(t.etiqueta)
        alertas.push(
          rojo(`El total diario (${fmt(redondear(total, 3))} ${unidad}) supera el ${t.etiqueta} (${fmt(redondear(tope, 3))} ${unidad}); la toma se limitó a ${fmt(nuevo)} ${unidad}.`),
        )
        pasos.push(`Se limita por ${t.etiqueta}: toma = ${fmt(redondear(tope, 3))} ${unidad} ÷ ${fmt(tomasPorDia)} tomas = ${fmt(nuevo)} ${unidad}`)
        toma = nuevo
      }
    }
  }

  const mgPorToma: Cantidad = { valor: toma, unidad }
  const totalDiario: Cantidad | null = tomasPorDia === null ? null : { valor: redondear(toma * tomasPorDia, 3), unidad }

  let salida: SalidaPresentacion
  if (presentacion.forma === 'jarabe' || presentacion.forma === 'suspension') {
    const r = masaAMl(mgPorToma, presentacion)
    if (!r.ok) return r
    salida = { tipo: 'ml', ml: r.valor }
    pasos.push(...r.pasos)
  } else if (presentacion.forma === 'gotas') {
    const r = masaAGotas(mgPorToma, presentacion)
    if (!r.ok) return r
    if (r.valor === 0) return error('La dosis es menor a una gota')
    salida = { tipo: 'gotas', gotas: r.valor }
    pasos.push(...r.pasos)
  } else {
    const r = masaAUnidades(mgPorToma, presentacion)
    if (!r.ok) return r
    salida = { tipo: 'unidades', ...r.valor }
    pasos.push(...r.pasos)
    if (r.valor.porcentaje < 0.9) {
      const pct = fmt(redondear(r.valor.porcentaje * 100, 0))
      alertas.push(
        rojo(`La presentación entrega ${fmt(r.valor.entregado.valor)} ${r.valor.entregado.unidad}, solo el ${pct} % de la dosis calculada (${fmt(toma)} ${unidad}).`),
      )
    }
  }

  return { ok: true, valor: { mgPorToma, tomasPorDia, totalDiario, salida, limitadaPor, alertas }, pasos }
}

function tomas(d: DosisOral): number | null {
  if (positivo(d.tomasPorDia)) return d.tomasPorDia
  if (positivo(d.intervaloH)) return 24 / d.intervaloH
  return null
}

function unidadBase(d: DosisOral): UnidadMasa {
  return d.unidad.replace(/\/kg$/, '').replace(/\/(dia|día)$/, '') as UnidadMasa
}

export function calcularPorPeso(p: {
  pesoKg: number
  dosis: DosisOral
  presentacion: PresentacionOral
  topeAdulto?: TopeAdulto
}): Resultado<ResultadoOral> {
  if (!positivo(p.pesoKg)) return error('Falta el peso')
  const d = p.dosis
  const porKg = d.max ?? d.min
  if (!positivo(porKg)) return error('Falta la dosis')
  const unidad = unidadBase(d)
  const n = tomas(d)
  if (d.base === 'dia' && n === null) return error('Falta el número de tomas por día')

  const alertas: Alerta[] = []
  if (p.pesoKg < 1 || p.pesoKg > 150) alertas.push(rojo('Peso fuera del rango habitual (1–150 kg)'))

  const pasos = [`dosis = ${fmt(porKg)} ${d.unidad} × ${fmt(p.pesoKg)} kg = ${fmt(redondear(porKg * p.pesoKg, 3))} ${unidad}`]
  let toma = porKg * p.pesoKg
  if (d.base === 'dia' && n !== null) {
    pasos.push(`por toma = ${fmt(redondear(toma, 3))} ${unidad} ÷ ${fmt(redondear(n, 3))} tomas = ${fmt(redondear(toma / n, 3))} ${unidad}`)
    toma = toma / n
  }

  const topesToma: Tope[] = []
  const topesDiarios: Tope[] = []
  if (d.topePorToma) topesToma.push({ cantidad: d.topePorToma, etiqueta: 'tope por toma' })
  if (p.topeAdulto?.porToma) topesToma.push({ cantidad: p.topeAdulto.porToma, etiqueta: 'tope de adulto por toma' })
  if (d.topeDiario) topesDiarios.push({ cantidad: d.topeDiario, etiqueta: 'tope diario' })
  if (p.topeAdulto?.diario) topesDiarios.push({ cantidad: p.topeAdulto.diario, etiqueta: 'tope de adulto diario' })

  return resolver({ toma, unidad, presentacion: p.presentacion, tomasPorDia: n, topesToma, topesDiarios, pasos, alertas })
}

export function calcularFija(p: { dosis: DosisOral; presentacion: PresentacionOral }): Resultado<ResultadoOral> {
  const d = p.dosis
  const valor = d.max ?? d.min
  if (!positivo(valor)) return error('Falta la dosis')
  const unidad = unidadBase(d)
  const n = tomas(d)
  if (d.base === 'dia' && n === null) return error('Falta el número de tomas por día')

  const pasos = [`dosis = ${fmt(valor)} ${unidad}${d.base === 'dia' ? ' por día' : ' por toma'}`]
  let toma = valor
  if (d.base === 'dia' && n !== null) {
    toma = valor / n
    pasos.push(`por toma = ${fmt(valor)} ${unidad} ÷ ${fmt(redondear(n, 3))} tomas = ${fmt(redondear(toma, 3))} ${unidad}`)
  }

  const topesToma: Tope[] = d.topePorToma ? [{ cantidad: d.topePorToma, etiqueta: 'tope por toma' }] : []
  const topesDiarios: Tope[] = d.topeDiario ? [{ cantidad: d.topeDiario, etiqueta: 'tope diario' }] : []

  return resolver({ toma, unidad, presentacion: p.presentacion, tomasPorDia: n, topesToma, topesDiarios, pasos, alertas: [] })
}
