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
const abajo3 = (n: number) => Math.floor(redondear(n * 1000, 6)) / 1000
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
  const original = toma
  const motivos: string[] = []

  for (const t of p.topesToma) {
    const tope = aUnidad(t.cantidad, unidad)
    if (typeof tope !== 'number') return tope
    if (excede(toma, tope)) {
      const nuevo = redondear(tope, 3)
      limitadaPor.push(t.etiqueta)
      const previo = limitadaPor.length === 1 ? `La dosis calculada (${fmt(toma)} ${unidad})` : `La dosis ya limitada (${fmt(toma)} ${unidad}, calculada ${fmt(original)} ${unidad})`
      alertas.push(rojo(`${previo} supera el ${t.etiqueta} (${fmt(nuevo)} ${unidad}); se limitó a ${fmt(nuevo)} ${unidad}.`))
      pasos.push(`Se limita por ${t.etiqueta}: ${fmt(toma)} ${unidad} → ${fmt(nuevo)} ${unidad}`)
      motivos.push(`La dosis se limitó a ${fmt(nuevo)} ${unidad} por el ${t.etiqueta}`)
      toma = nuevo
    }
  }

  for (const t of p.topesDiarios) {
    const tope = aUnidad(t.cantidad, unidad)
    if (typeof tope !== 'number') return tope
    const total = toma * (tomasPorDia ?? 1)
    if (!excede(total, tope)) continue
    const nuevo = tomasPorDia === null ? redondear(tope, 3) : abajo3(tope / tomasPorDia)
    limitadaPor.push(t.etiqueta)
    if (tomasPorDia === null) {
      alertas.push(
        rojo(`Una sola toma (${fmt(toma)} ${unidad}) supera el ${t.etiqueta} (${fmt(redondear(tope, 3))} ${unidad}); se limitó a ${fmt(nuevo)} ${unidad} (tomas por día desconocidas).`),
      )
      pasos.push(`Se limita por ${t.etiqueta}: toma = ${fmt(nuevo)} ${unidad} (tomas por día desconocidas)`)
    } else {
      alertas.push(
        rojo(`El total diario (${fmt(redondear(total, 3))} ${unidad}) supera el ${t.etiqueta} (${fmt(redondear(tope, 3))} ${unidad}); la toma se limitó a ${fmt(nuevo)} ${unidad}.`),
      )
      pasos.push(`Se limita por ${t.etiqueta}: toma = ${fmt(redondear(tope, 3))} ${unidad} ÷ ${fmt(tomasPorDia)} tomas = ${fmt(nuevo)} ${unidad} (hacia abajo)`)
    }
    motivos.push(`La dosis se limitó a ${fmt(nuevo)} ${unidad} por el ${t.etiqueta}`)
    toma = nuevo
  }

  const conCausa = <T extends { ok: false; error: string }>(r: T): T =>
    motivos.length === 0 ? r : { ...r, error: `${r.error}. ${motivos[motivos.length - 1]}` }

  const mgPorToma: Cantidad = { valor: toma, unidad }
  const totalDiario: Cantidad | null = tomasPorDia === null ? null : { valor: redondear(toma * tomasPorDia, 3), unidad }

  let salida: SalidaPresentacion
  if (presentacion.forma === 'jarabe' || presentacion.forma === 'suspension') {
    const r = masaAMl(mgPorToma, presentacion)
    if (!r.ok) return conCausa(r)
    salida = { tipo: 'ml', ml: r.valor }
    pasos.push(...r.pasos)
  } else if (presentacion.forma === 'gotas') {
    const r = masaAGotas(mgPorToma, presentacion)
    if (!r.ok) return r
    if (r.valor === 0) return conCausa(error('La dosis es menor a una gota'))
    salida = { tipo: 'gotas', gotas: r.valor }
    pasos.push(...r.pasos)
  } else {
    const r = masaAUnidades(mgPorToma, presentacion)
    if (!r.ok) return conCausa(r)
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
  if (positivo(d.intervaloH)) return Math.ceil(24 / d.intervaloH)
  return null
}

function unidadBase(d: DosisOral): UnidadMasa {
  return d.unidad.replace(/\/kg$/, '').replace(/\/(dia|día)$/, '') as UnidadMasa
}

const NOMBRE_REGIMEN: Record<DosisOral['regimen'], string> = {
  fija: 'fija',
  por_peso: 'por peso',
  por_edad: 'por edad',
  por_superficie: 'por superficie corporal',
}

function validarRegimen(d: DosisOral, esperado: 'fija' | 'por_peso'): string | null {
  const porKg = d.unidad.endsWith('/kg')
  if (d.regimen !== esperado || porKg !== (esperado === 'por_peso')) {
    const pauta = d.regimen === 'por_edad' || d.regimen === 'por_superficie' ? ': se muestra como pauta, no se calcula' : ''
    const aviso = d.regimen === esperado ? ` con unidad ${d.unidad}, que no corresponde` : ''
    return `Esta dosis es ${NOMBRE_REGIMEN[d.regimen]}${aviso}${pauta}`
  }
  return null
}

/** Forma y concentración de una presentación, p. ej. «comprimido 100 mg de liberación prolongada», «jarabe 100 mg/ml». */
export function describirPresentacion(p: PresentacionOral): string {
  const forma = p.forma.replace(/_/g, ' ')
  const cifra = p.cantidad
    ? `${String(p.cantidad.valor).replace('.', ',')} ${p.cantidad.unidad}`
    : p.concentracion
      ? `${String(p.concentracion.valor).replace('.', ',')} ${p.concentracion.unidad}/ml`
      : ''
  return [forma, cifra, p.liberacionProlongada ? 'de liberación prolongada' : ''].filter(Boolean).join(' ')
}

/** Si la dosis no aplica a la presentación elegida, el mensaje de error; si aplica, null. */
function noAplica(d: DosisOral, presentacion: PresentacionOral, presentacionesDeFicha?: PresentacionOral[]): string | null {
  if (!d.presentaciones || d.presentaciones.includes(presentacion.id)) return null
  const aplicables = presentacionesDeFicha?.filter((x) => d.presentaciones?.includes(x.id)) ?? []
  const lista = aplicables.length > 0 ? aplicables.map(describirPresentacion).join(' o ') : d.presentaciones.join(' o ')
  return `Esta dosis no aplica a esta presentación: usa ${lista}`
}

export function calcularPorPeso(p: {
  pesoKg: number
  dosis: DosisOral
  presentacion: PresentacionOral
  /** Todas las presentaciones de la ficha; sirven para nombrar las aplicables en el error. */
  presentacionesDeFicha?: PresentacionOral[]
  topeAdulto?: TopeAdulto
}): Resultado<ResultadoOral> {
  if (!positivo(p.pesoKg)) return error('Falta el peso')
  const d = p.dosis
  const inv = validarRegimen(d, 'por_peso')
  if (inv) return error(inv)
  const noApl = noAplica(d, p.presentacion, p.presentacionesDeFicha)
  if (noApl) return error(noApl)
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

export function calcularFija(p: {
  dosis: DosisOral
  presentacion: PresentacionOral
  presentacionesDeFicha?: PresentacionOral[]
}): Resultado<ResultadoOral> {
  const d = p.dosis
  const inv = validarRegimen(d, 'fija')
  if (inv) return error(inv)
  const noApl = noAplica(d, p.presentacion, p.presentacionesDeFicha)
  if (noApl) return error(noApl)
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
