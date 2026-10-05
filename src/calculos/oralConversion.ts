import type { PresentacionOral } from '../esquema/ficha-oral'
import type { Resultado } from './calculadoras'
import { redondear } from './redondeo'
import { convertirMasa, type Cantidad, type UnidadMasa } from './unidades'

const positivo = (n: number | undefined): n is number => typeof n === 'number' && Number.isFinite(n) && n > 0
const error = (mensaje: string): { ok: false; error: string } => ({ ok: false, error: mensaje })
const fmt = (n: number) => String(n).replace('.', ',')

function aUnidad(c: Cantidad, unidad: UnidadMasa): number | { ok: false; error: string } {
  try {
    return convertirMasa(c.valor, c.unidad, unidad)
  } catch (e) {
    return error((e as Error).message)
  }
}

const PASO: Record<PresentacionOral['partible'], number> = { no: 1, mitades: 0.5, cuartos: 0.25 }

/** Masa pedida expresada en la unidad de la concentración y esa concentración (por ml). */
function enConcentracion(masa: Cantidad, p: PresentacionOral) {
  const c = p.concentracion
  if (!c || !positivo(c.valor)) return error('Falta la concentración')
  if (!positivo(masa.valor)) return error('Falta la dosis')
  const m = aUnidad(masa, c.unidad)
  if (typeof m !== 'number') return m
  return { ok: true as const, m, c }
}

export function masaAMl(masa: Cantidad, p: PresentacionOral): Resultado<number> {
  const r = enConcentracion(masa, p)
  if (!r.ok) return r
  const ml = redondear(r.m / r.c.valor, 2)
  return {
    ok: true,
    valor: ml,
    pasos: [
      'ml = dosis ÷ concentración',
      `${fmt(redondear(r.m, 4))} ${r.c.unidad} ÷ ${fmt(r.c.valor)} ${r.c.unidad}/ml = ${fmt(ml)} ml`,
    ],
  }
}

export function mlAMasa(ml: number, p: PresentacionOral): Resultado<Cantidad> {
  const c = p.concentracion
  if (!c || !positivo(c.valor)) return error('Falta la concentración')
  if (!positivo(ml)) return error('Falta el volumen')
  const valor = redondear(ml * c.valor, 4)
  return {
    ok: true,
    valor: { valor, unidad: c.unidad },
    pasos: ['dosis = ml × concentración', `${fmt(ml)} ml × ${fmt(c.valor)} ${c.unidad}/ml = ${fmt(valor)} ${c.unidad}`],
  }
}

export function masaAGotas(masa: Cantidad, p: PresentacionOral): Resultado<number> {
  const r = enConcentracion(masa, p)
  if (!r.ok) return r
  if (!positivo(p.gotasPorMl)) return error('Falta el dato de gotas por ml de esta presentación')
  const ml = r.m / r.c.valor
  const gotas = Math.floor(redondear(ml * p.gotasPorMl, 6))
  return {
    ok: true,
    valor: gotas,
    pasos: [
      'gotas = dosis ÷ concentración × gotas por ml (hacia abajo)',
      `${fmt(redondear(r.m, 4))} ${r.c.unidad} ÷ ${fmt(r.c.valor)} ${r.c.unidad}/ml × ${fmt(p.gotasPorMl)} gotas/ml = ${gotas} gotas`,
    ],
  }
}

export function masaAUnidades(
  masa: Cantidad,
  p: PresentacionOral,
): Resultado<{ unidades: number; entregado: Cantidad; porcentaje: number }> {
  const c = p.cantidad
  if (!c || !positivo(c.valor)) return error('Falta la cantidad por unidad')
  if (!positivo(masa.valor)) return error('Falta la dosis')
  const m = aUnidad(masa, c.unidad)
  if (typeof m !== 'number') return m
  const paso = PASO[p.partible]
  const unidades = Math.floor(redondear(m / c.valor / paso, 6)) * paso
  if (unidades <= 0) return error('Esta presentación no permite esa dosis')
  const entregado = redondear(unidades * c.valor, 4)
  const porcentaje = redondear(entregado / m, 4)
  return {
    ok: true,
    valor: { unidades, entregado: { valor: entregado, unidad: c.unidad }, porcentaje },
    pasos: [
      `unidades = dosis ÷ cantidad por unidad, hacia abajo a ${fmt(paso)}`,
      `${fmt(redondear(m, 4))} ${c.unidad} ÷ ${fmt(c.valor)} ${c.unidad} = ${fmt(unidades)} unidades (${fmt(entregado)} ${c.unidad}, ${fmt(redondear(porcentaje * 100, 1))} % de lo pedido)`,
    ],
  }
}
