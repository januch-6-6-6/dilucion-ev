import { redondear } from './redondeo'
import { convertirMasa, type Cantidad, type UnidadMasa } from './unidades'

export type Resultado<T> = { ok: true; valor: T; pasos: string[] } | { ok: false; error: string }
export type DosisPorPeso = { valor: number; unidad: UnidadMasa; tiempo: 'min' | 'h' | null }

const GOTAS_MACRO_POR_ML = 20
const GOTAS_MICRO_POR_ML = 60

const positivo = (n: number) => Number.isFinite(n) && n > 0
const error = (mensaje: string): { ok: false; error: string } => ({ ok: false, error: mensaje })
const fmt = (n: number) => String(n).replace('.', ',')

/** Convierte con mensaje de error en vez de excepción. */
function aUnidad(c: Cantidad, unidad: UnidadMasa): number | { ok: false; error: string } {
  try {
    return convertirMasa(c.valor, c.unidad, unidad)
  } catch (e) {
    return error((e as Error).message)
  }
}

export function concentracion(cantidad: Cantidad, volumenFinalMl: number, unidadSalida: UnidadMasa): Resultado<number> {
  if (!positivo(cantidad.valor)) return error('Falta la dosis')
  if (!positivo(volumenFinalMl)) return error('Falta el volumen')
  const total = aUnidad(cantidad, unidadSalida)
  if (typeof total !== 'number') return total
  const valor = redondear(total / volumenFinalMl, 3)
  return {
    ok: true,
    valor,
    pasos: [
      'concentración = cantidad ÷ volumen final',
      `${fmt(total)} ${unidadSalida} ÷ ${fmt(volumenFinalMl)} ml = ${fmt(valor)} ${unidadSalida}/ml`,
    ],
  }
}

export function volumenACargar(
  dosis: Cantidad,
  presentacion: { cantidad: Cantidad; volumenMl: number },
): Resultado<{ ml: number; unidades: number }> {
  if (!positivo(dosis.valor)) return error('Falta la dosis')
  if (!positivo(presentacion.cantidad.valor) || !positivo(presentacion.volumenMl)) return error('Falta la concentración')
  const unidad = presentacion.cantidad.unidad
  const dosisEnUnidad = aUnidad(dosis, unidad)
  if (typeof dosisEnUnidad !== 'number') return dosisEnUnidad
  const porMl = presentacion.cantidad.valor / presentacion.volumenMl
  const ml = redondear(dosisEnUnidad / porMl, 2)
  const unidades = Math.ceil(redondear(ml / presentacion.volumenMl, 6))
  return {
    ok: true,
    valor: { ml, unidades },
    pasos: [
      'ml a cargar = dosis ÷ concentración de la presentación',
      `${fmt(dosisEnUnidad)} ${unidad} ÷ ${fmt(redondear(porMl, 4))} ${unidad}/ml = ${fmt(ml)} ml (${unidades} de ${fmt(presentacion.volumenMl)} ml)`,
    ],
  }
}

export function velocidadPorTiempo(
  volumenMl: number,
  tiempoMin: number,
): Resultado<{ mlh: number; gotasMacro: number; gotasMicro: number }> {
  if (!positivo(volumenMl)) return error('Falta el volumen')
  if (!positivo(tiempoMin)) return error('Falta el tiempo')
  const mlPorMin = volumenMl / tiempoMin
  const mlh = redondear(mlPorMin * 60, 1)
  const gotasMacro = redondear(mlPorMin * GOTAS_MACRO_POR_ML, 0)
  const gotasMicro = redondear(mlPorMin * GOTAS_MICRO_POR_ML, 0)
  return {
    ok: true,
    valor: { mlh, gotasMacro, gotasMicro },
    pasos: [
      'ml/h = volumen ÷ minutos × 60; gotas/min = volumen ÷ minutos × factor de goteo',
      `${fmt(volumenMl)} ml ÷ ${fmt(tiempoMin)} min × 60 = ${fmt(mlh)} ml/h`,
      `Macrogotero (20 gotas/ml): ${gotasMacro} gotas/min · Microgotero (60 gotas/ml): ${gotasMicro} gotas/min`,
    ],
  }
}

export function velocidadPorDosis(dosisPorHora: Cantidad, concentracionPorMl: Cantidad): Resultado<number> {
  if (!positivo(dosisPorHora.valor)) return error('Falta la dosis')
  if (!positivo(concentracionPorMl.valor)) return error('Falta la concentración')
  const dosis = aUnidad(dosisPorHora, concentracionPorMl.unidad)
  if (typeof dosis !== 'number') return dosis
  const mlh = redondear(dosis / concentracionPorMl.valor, 1)
  return {
    ok: true,
    valor: mlh,
    pasos: [
      'ml/h = dosis por hora ÷ concentración',
      `${fmt(dosis)} ${concentracionPorMl.unidad}/h ÷ ${fmt(concentracionPorMl.valor)} ${concentracionPorMl.unidad}/ml = ${fmt(mlh)} ml/h`,
    ],
  }
}

export function dosisAVelocidad(p: { pesoKg: number; dosis: DosisPorPeso; concentracionPorMl: Cantidad }): Resultado<number> {
  if (!positivo(p.pesoKg)) return error('Falta el peso')
  if (!positivo(p.dosis.valor) || p.dosis.tiempo === null) return error('Falta la dosis')
  if (!positivo(p.concentracionPorMl.valor)) return error('Falta la concentración')
  const dosis = aUnidad({ valor: p.dosis.valor, unidad: p.dosis.unidad }, p.concentracionPorMl.unidad)
  if (typeof dosis !== 'number') return dosis
  const factorHora = p.dosis.tiempo === 'min' ? 60 : 1
  const mlh = redondear((dosis * p.pesoKg * factorHora) / p.concentracionPorMl.valor, 1)
  const u = p.concentracionPorMl.unidad
  return {
    ok: true,
    valor: mlh,
    pasos: [
      p.dosis.tiempo === 'min' ? 'ml/h = dosis × peso × 60 ÷ concentración' : 'ml/h = dosis × peso ÷ concentración',
      `${fmt(dosis)} ${u}/kg/${p.dosis.tiempo} × ${fmt(p.pesoKg)} kg${factorHora === 60 ? ' × 60' : ''} ÷ ${fmt(p.concentracionPorMl.valor)} ${u}/ml = ${fmt(mlh)} ml/h`,
    ],
  }
}

export function velocidadADosis(p: {
  pesoKg: number
  mlh: number
  concentracionPorMl: Cantidad
  unidadSalida: UnidadMasa
  tiempo: 'min' | 'h'
}): Resultado<number> {
  if (!positivo(p.pesoKg)) return error('Falta el peso')
  if (!positivo(p.mlh)) return error('Falta la velocidad')
  if (!positivo(p.concentracionPorMl.valor)) return error('Falta la concentración')
  const concentracionSalida = aUnidad(p.concentracionPorMl, p.unidadSalida)
  if (typeof concentracionSalida !== 'number') return concentracionSalida
  const divisorTiempo = p.tiempo === 'min' ? 60 : 1
  const dosis = redondear((p.mlh * concentracionSalida) / p.pesoKg / divisorTiempo, 3)
  return {
    ok: true,
    valor: dosis,
    pasos: [
      p.tiempo === 'min' ? 'dosis = ml/h × concentración ÷ peso ÷ 60' : 'dosis = ml/h × concentración ÷ peso',
      `${fmt(p.mlh)} ml/h × ${fmt(concentracionSalida)} ${p.unidadSalida}/ml ÷ ${fmt(p.pesoKg)} kg${divisorTiempo === 60 ? ' ÷ 60' : ''} = ${fmt(dosis)} ${p.unidadSalida}/kg/${p.tiempo}`,
    ],
  }
}

export function dosisPediatrica(p: {
  pesoKg: number
  dosisPorKg: Cantidad
  topeAdulto: Cantidad
}): Resultado<{ dosis: Cantidad; limitada: boolean }> {
  if (!positivo(p.pesoKg)) return error('Falta el peso')
  if (!positivo(p.dosisPorKg.valor)) return error('Falta la dosis')
  const unidad = p.dosisPorKg.unidad
  const tope = aUnidad(p.topeAdulto, unidad)
  if (typeof tope !== 'number') return tope
  const calculada = redondear(p.dosisPorKg.valor * p.pesoKg, 3)
  const limitada = calculada > tope
  const final = limitada ? tope : calculada
  return {
    ok: true,
    valor: { dosis: { valor: final, unidad }, limitada },
    pasos: [
      'dosis = dosis por kg × peso (con tope de dosis de adulto)',
      `${fmt(p.dosisPorKg.valor)} ${unidad}/kg × ${fmt(p.pesoKg)} kg = ${fmt(calculada)} ${unidad}${limitada ? ` → limitada a ${fmt(tope)} ${unidad}` : ''}`,
    ],
  }
}
