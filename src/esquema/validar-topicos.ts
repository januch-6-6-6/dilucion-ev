import { Fuente } from './ficha'
import { FichaTopica } from './ficha-topica'

export type Verificacion = 'contrastada' | 'fuente_unica' | 'sin_pauta'

/**
 * 'contrastada' si al menos una pauta trae en `tambien` una fuente de otra institución
 * que su `fuente` (la misma pauta respaldada dos veces). Una pauta adulta de una institución
 * y otra pediátrica de otra NO cuentan: son pautas distintas.
 */
export function verificacionTopica(ficha: FichaTopica, fuentes: Fuente[]): Verificacion {
  if (ficha.sinPauta) return 'sin_pauta'
  const inst = new Map(fuentes.map((f) => [f.id, f.institucion]))
  const contrastada = ficha.dosis.some((d) => {
    const propia = inst.get(d.fuente.ref)
    return (d.tambien ?? []).some((t) => {
      const otra = inst.get(t.ref)
      return otra !== undefined && propia !== undefined && otra !== propia
    })
  })
  return contrastada ? 'contrastada' : 'fuente_unica'
}

export function refsDeFuente(valor: unknown, ruta: string, salida: { ruta: string; ref: string }[]) {
  if (Array.isArray(valor)) {
    valor.forEach((v, i) => refsDeFuente(v, `${ruta}[${i}]`, salida))
  } else if (valor && typeof valor === 'object') {
    for (const [k, v] of Object.entries(valor)) {
      if ((k === 'fuente' || k === 'tambien') && Array.isArray(v)) {
        v.forEach((x, i) => x && typeof x === 'object' && 'ref' in x && salida.push({ ruta: `${ruta}.${k}[${i}]`, ref: String(x.ref) }))
      } else if (k === 'fuente' && v && typeof v === 'object' && 'ref' in v) {
        salida.push({ ruta: `${ruta}.fuente`, ref: String(v.ref) })
      } else if (k === 'fuente' && typeof v === 'string') {
        // discrepancias[].valores[].fuente es el id de la fuente, no un FuenteRef
        salida.push({ ruta: `${ruta}.fuente`, ref: v })
      } else {
        refsDeFuente(v, `${ruta}.${k}`, salida)
      }
    }
  }
}

export const rutaLegible = (ruta: PropertyKey[]): string =>
  ruta.reduce<string>((acc, seg) => (typeof seg === 'number' ? `${acc}[${seg}]` : acc ? `${acc}.${String(seg)}` : String(seg)), '')

/** Valida fichas tópicas y sus fuentes. Devuelve errores legibles; lista vacía = todo OK. */
export function validarTopicos(fichasCrudas: unknown[], fuentesCrudas: unknown[]): string[] {
  const errores: string[] = []
  const idsFuente = new Set<string>()
  fuentesCrudas.forEach((f, i) => {
    const r = Fuente.safeParse(f)
    if (!r.success) errores.push(`fuentes-topicos.yaml[${i}]: ${r.error.issues.map((x) => `${x.path.join('.')} ${x.message}`).join('; ')}`)
    else if (idsFuente.has(r.data.id)) errores.push(`fuentes-topicos.yaml: id repetido "${r.data.id}"`)
    else idsFuente.add(r.data.id)
  })

  const vistos = new Set<string>()
  fichasCrudas.forEach((crudo, i) => {
    const etiqueta = (crudo as { id?: string })?.id ?? `ficha[${i}]`
    const r = FichaTopica.safeParse(crudo)
    if (!r.success) {
      for (const x of r.error.issues) errores.push(`${etiqueta}: ${rutaLegible(x.path)} — ${x.message}`)
      return
    }
    const ficha = r.data
    if (vistos.has(ficha.id)) errores.push(`${ficha.id}: id repetido`)
    vistos.add(ficha.id)

    const idsPres = new Set<string>()
    ficha.presentaciones.forEach((p, j) => {
      if (idsPres.has(p.id)) errores.push(`${ficha.id}: presentaciones[${j}] id repetido "${p.id}"`)
      idsPres.add(p.id)
    })

    const refs: { ruta: string; ref: string }[] = []
    refsDeFuente(ficha, ficha.id, refs)
    for (const { ruta, ref } of refs) {
      if (!idsFuente.has(ref)) errores.push(`${ruta}: la fuente "${ref}" no existe en fuentes-topicos.yaml`)
    }
  })
  return errores
}
