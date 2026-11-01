import type { DosisTopica, FichaTopica, PresentacionTopica } from '../esquema/ficha-topica'

/** Supuesto rotulado en la UI: tamaño de gota habitual de un gotero oftálmico. Editable. */
export const GOTAS_POR_ML_SUPUESTO = 20

export type MotivoNoCalculable = 'unguento' | 'unidosis' | 'sin_frecuencia' | 'no_aplica_presentacion'

/** Por qué una dosis no permite calcular la duración del envase; null = sí se puede. */
export function motivoNoCalculable(d: DosisTopica, p: PresentacionTopica): MotivoNoCalculable | null {
  if (d.presentaciones && !d.presentaciones.includes(p.id)) return 'no_aplica_presentacion'
  if (p.unidosis) return 'unidosis'
  if (p.forma === 'unguento' || p.forma === 'gel' || d.unidad === 'cm' || d.unidad === 'aplicacion') return 'unguento'
  if (d.cantidad === undefined || d.vecesAlDia === undefined || (d.unidad !== 'gota' && d.unidad !== 'pulverizacion')) return 'sin_frecuencia'
  return null
}

export const TEXTO_NO_CALCULABLE: Record<MotivoNoCalculable, string> = {
  unguento: 'Para ungüentos y geles no se calcula: la cantidad por aplicación (en cm) no se puede convertir con exactitud a contenido del tubo.',
  unidosis: 'Es unidosis: cada envase se usa una vez y se desecha. Necesitas un envase por aplicación.',
  sin_frecuencia: 'La fuente no da una cantidad y una frecuencia diaria fijas para esta pauta, así que no se puede calcular.',
  no_aplica_presentacion: 'Esta pauta no corresponde a la presentación elegida.',
}

/** Pares (dosis, presentación) con los que sí se puede calcular. */
export function combinacionesCalculables(f: FichaTopica): { dosis: DosisTopica; indice: number; presentacion: PresentacionTopica }[] {
  return f.dosis.flatMap((dosis, indice) =>
    f.presentaciones.filter((p) => motivoNoCalculable(dosis, p) === null).map((presentacion) => ({ dosis, indice, presentacion })),
  )
}

export type EntradaDuracion = {
  /** Unidades por aplicación (gotas o pulverizaciones) en cada sitio. */
  cantidad: number
  vecesAlDia: number
  /** 1 o 2 (un ojo / ambos, un oído / ambos, una fosa / ambas). */
  sitios: number
  unidad: 'gota' | 'pulverizacion'
  /** ml del frasco (gotas) o pulverizaciones por envase (spray). */
  contenido: number
  /** Solo para gotas. */
  gotasPorMl?: number
  /** Días que el envase se puede usar una vez abierto; undefined si la fuente no lo fija. */
  validezAbiertoDias?: number
}

export type ResultadoDuracion = {
  unidadesTotales: number
  consumoDiario: number
  diasPorContenido: number
  /** Días reales: el menor entre contenido y validez. */
  dias: number
  limita: 'contenido' | 'validez'
}

const valido = (n: number | undefined): n is number => n !== undefined && Number.isFinite(n) && n > 0

/** Cuántos días alcanza un envase. Lanza Error con mensaje legible si una entrada no es válida. */
export function duracionEnvase(e: EntradaDuracion): ResultadoDuracion {
  if (!valido(e.cantidad) || !valido(e.vecesAlDia)) throw new Error('La cantidad y las veces al día deben ser mayores que 0')
  if (e.sitios !== 1 && e.sitios !== 2) throw new Error('Los sitios deben ser 1 o 2')
  if (!valido(e.contenido)) throw new Error('El contenido del envase debe ser mayor que 0')
  let unidadesTotales = e.contenido
  if (e.unidad === 'gota') {
    const gpm = e.gotasPorMl ?? GOTAS_POR_ML_SUPUESTO
    if (!valido(gpm)) throw new Error('Las gotas por ml deben ser mayores que 0')
    unidadesTotales = e.contenido * gpm
  }
  const consumoDiario = e.cantidad * e.vecesAlDia * e.sitios
  const diasPorContenido = Math.floor(unidadesTotales / consumoDiario)
  if (valido(e.validezAbiertoDias) && e.validezAbiertoDias < diasPorContenido) {
    return { unidadesTotales, consumoDiario, diasPorContenido, dias: e.validezAbiertoDias, limita: 'validez' }
  }
  return { unidadesTotales, consumoDiario, diasPorContenido, dias: diasPorContenido, limita: 'contenido' }
}

/** Validez tras abrir que aplica a una presentación: la conservación específica, o la general. */
export function validezDe(f: FichaTopica, presentacionId: string): number | undefined {
  const especifica = f.conservacion.find((c) => c.presentaciones?.includes(presentacionId))
  if (especifica) return especifica.validezAbiertoDias
  return f.conservacion.find((c) => !c.presentaciones)?.validezAbiertoDias
}
