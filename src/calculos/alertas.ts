import { convertirMasa, type Cantidad } from './unidades'

export type Alerta = { nivel: 'rojo'; mensaje: string }

const fmt = (n: number) => String(n).replace('.', ',')
const rojo = (mensaje: string): Alerta => ({ nivel: 'rojo', mensaje })

export function alertaConcentracion(concPorMl: Cantidad, maxPorMl?: Cantidad): Alerta[] {
  if (!maxPorMl) return []
  const conc = convertirMasa(concPorMl.valor, concPorMl.unidad, maxPorMl.unidad)
  return conc > maxPorMl.valor
    ? [rojo(`La preparación (${fmt(conc)} ${maxPorMl.unidad}/ml) supera la concentración máxima de ${fmt(maxPorMl.valor)} ${maxPorMl.unidad}/ml.`)]
    : []
}

export function alertaDosis(
  dosis: number,
  unidad: string,
  rango: { min?: number; max?: number; maximaAbsoluta?: number },
): Alerta[] {
  const alertas: Alerta[] = []
  if (rango.max !== undefined && dosis > rango.max) {
    alertas.push(rojo(`${fmt(dosis)} ${unidad} supera la dosis máxima de ${fmt(rango.max)} ${unidad}.`))
  } else if (rango.maximaAbsoluta !== undefined && dosis > rango.maximaAbsoluta) {
    alertas.push(rojo(`${fmt(dosis)} ${unidad} supera la dosis máxima absoluta de ${fmt(rango.maximaAbsoluta)} ${unidad}.`))
  }
  if (rango.min !== undefined && dosis < rango.min) {
    alertas.push(rojo(`${fmt(dosis)} ${unidad} está bajo la dosis mínima de ${fmt(rango.min)} ${unidad}.`))
  }
  return alertas
}

export function alertaTiempo(tiempoMin: number, tiempoMinimoMin?: number): Alerta[] {
  if (tiempoMinimoMin === undefined || tiempoMin >= tiempoMinimoMin) return []
  return [rojo(`Pasar en ${fmt(tiempoMin)} min es más rápido que lo recomendado (mínimo ${fmt(tiempoMinimoMin)} min).`)]
}
