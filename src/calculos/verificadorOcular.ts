import { convertirOcular, TOLERANCIA_OCULAR, type CantidadOcular, type DosisFinal, type FichaOcular, type PresentacionOcular } from '../esquema/ficha-ocular'

/** Un paso de preparación ya con números (los que escribe el usuario en el verificador). */
export type PasoNumerico = { tipo: 'reconstituir'; volumenMl: number } | { tipo: 'diluir'; tomarMl: number; llevarAMl: number }

export type Comparacion = {
  dosis: DosisFinal
  estado: 'coincide' | 'no_coincide'
  diferenciaPct: number | null
  /** El volumen que queda tras los pasos alcanza para el volumen de esta dosis. */
  volumenAlcanza: boolean
}

export type ResultadoVerificacion =
  | {
      ok: true
      /** Concentración final por ml, en la unidad del frasco. */
      porMl: CantidadOcular
      /** Cantidad que habría en el volumen de cada dosis objetivo, en la unidad de esa dosis (mismo orden que `objetivos`). */
      porVolumenObjetivo: CantidadOcular[]
      volumenDisponibleMl: number
      comparaciones: Comparacion[]
      algunaCoincide: boolean
    }
  | { ok: false; error: string }

export const MAX_PASOS = 4
const EPS = 1e-9
const coma = (n: number) => String(n).replace('.', ',')
const fallo = (error: string): ResultadoVerificacion => ({ ok: false, error })

/**
 * Calcula la concentración que resulta de los pasos y la compara con las dosis de la fuente.
 * Solo compara: nunca propone cómo preparar. El volumen de una reconstitución es el volumen total que queda tras disolver el polvo (el que indica la fuente), no el diluyente agregado: el polvo puede ocupar volumen.
 */
export function verificar(e: { presentacion: PresentacionOcular; pasos: PasoNumerico[]; objetivos: DosisFinal[] }): ResultadoVerificacion {
  const { presentacion: p, pasos, objetivos } = e
  if (p.usoDirecto) return fallo('Esta presentación viene lista para usar: no hay nada que verificar.')
  if (pasos.length > MAX_PASOS) return fallo(`Máximo ${MAX_PASOS} pasos.`)
  const valores = pasos.flatMap((s) => (s.tipo === 'reconstituir' ? [s.volumenMl] : [s.tomarMl, s.llevarAMl]))
  if (valores.some((v) => !Number.isFinite(v) || v <= 0)) return fallo('Los volúmenes deben ser mayores que 0.')

  const esPolvo = p.forma === 'polvo'
  if (!esPolvo && p.volumenMl === undefined) return fallo('La presentación no informa su volumen.')
  const masa = p.cantidad.valor
  let cantidad = masa
  let volumen = esPolvo ? 0 : (p.volumenMl as number)
  for (const s of pasos) {
    if (s.tipo === 'reconstituir') {
      if (!esPolvo) return fallo('Esta presentación ya es una solución: no se reconstituye.')
      if (volumen > 0) return fallo('El polvo ya está reconstituido.')
      volumen = s.volumenMl
    } else {
      if (volumen === 0) return fallo('Primero reconstituye el polvo.')
      if (s.tomarMl > volumen + EPS) return fallo(`No puedes tomar más volumen del que tienes (${coma(volumen)} ml).`)
      if (s.llevarAMl < s.tomarMl - EPS) return fallo('El volumen final no puede ser menor que el que tomaste.')
      cantidad = (cantidad * s.tomarMl) / volumen
      volumen = s.llevarAMl
    }
  }
  if (volumen === 0) return fallo('Primero reconstituye el polvo.')

  const porMl: CantidadOcular = { valor: cantidad / volumen, unidad: p.cantidad.unidad }
  const porVolumenObjetivo: CantidadOcular[] = []
  const comparaciones: Comparacion[] = []
  for (const o of objetivos) {
    const unidadObj = o.cantidad.unidad
    const enUnidadObj = convertirOcular(porMl.valor, porMl.unidad, unidadObj)
    if (enUnidadObj === null) return fallo(`Unidades no comparables: el frasco está en ${porMl.unidad} y la dosis en ${unidadObj}.`)
    const obtenido = enUnidadObj * o.volumenMl
    porVolumenObjetivo.push({ valor: obtenido, unidad: unidadObj })
    const volumenAlcanza = volumen >= o.volumenMl - EPS
    if ('min' in o.cantidad) {
      const dentro = obtenido >= o.cantidad.min * (1 - EPS) && obtenido <= o.cantidad.max * (1 + EPS)
      comparaciones.push({ dosis: o, estado: dentro ? 'coincide' : 'no_coincide', diferenciaPct: null, volumenAlcanza })
    } else {
      const pct = ((obtenido - o.cantidad.valor) / o.cantidad.valor) * 100
      comparaciones.push({ dosis: o, estado: Math.abs(pct) <= TOLERANCIA_OCULAR * 100 + EPS ? 'coincide' : 'no_coincide', diferenciaPct: pct, volumenAlcanza })
    }
  }
  return {
    ok: true,
    porMl,
    porVolumenObjetivo,
    volumenDisponibleMl: volumen,
    comparaciones,
    /** Coincide solo si la concentración es la de la fuente Y queda volumen para una dosis. */
    algunaCoincide: comparaciones.some((c) => c.estado === 'coincide' && c.volumenAlcanza),
  }
}

/** El verificador existe solo en fichas intraoculares con alguna presentación que se prepara y tiene una dosis de la fuente con la que comparar. */
export function tieneVerificador(f: FichaOcular): boolean {
  return f.modo === 'intraocular' && presentacionesVerificables(f).length > 0
}

/** Presentaciones que se preparan y tienen al menos una dosis final de la fuente contra la que comparar. */
export function presentacionesVerificables(f: FichaOcular): PresentacionOcular[] {
  return f.presentaciones.filter((p) => !p.usoDirecto && objetivosDe(f, p.id).length > 0)
}

/** Dosis finales de la fuente que aplican a esa presentación (una dosis sin `presentaciones` aplica a todas). */
export function objetivosDe(f: FichaOcular, presentacionId: string): DosisFinal[] {
  return f.dosis.flatMap((d) => (d.final && (!d.presentaciones || d.presentaciones.includes(presentacionId)) ? [d.final] : []))
}
