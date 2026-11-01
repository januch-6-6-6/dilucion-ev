import { Fuente } from './ficha'
import { FichaOcular } from './ficha-ocular'
import { refsDeFuente, rutaLegible, type Verificacion } from './validar-topicos'

/** Igual que en tópicos: 'contrastada' si una dosis trae en `tambien` una fuente de otra institución que su `fuente`. */
export function verificacionOcular(ficha: FichaOcular, fuentes: Fuente[]): Verificacion {
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

/** Valida fichas oculares y sus fuentes. Devuelve errores legibles; lista vacía = todo OK. */
export function validarOculares(fichasCrudas: unknown[], fuentesCrudas: unknown[]): string[] {
  const errores: string[] = []
  const idsFuente = new Set<string>()
  fuentesCrudas.forEach((f, i) => {
    const r = Fuente.safeParse(f)
    if (!r.success) errores.push(`fuentes-oftalmo.yaml[${i}]: ${r.error.issues.map((x) => `${x.path.join('.')} ${x.message}`).join('; ')}`)
    else if (idsFuente.has(r.data.id)) errores.push(`fuentes-oftalmo.yaml: id repetido "${r.data.id}"`)
    else idsFuente.add(r.data.id)
  })

  const vistos = new Set<string>()
  fichasCrudas.forEach((crudo, i) => {
    const etiqueta = (crudo as { id?: string })?.id ?? `ficha[${i}]`
    const r = FichaOcular.safeParse(crudo)
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
      if (!idsFuente.has(ref)) errores.push(`${ruta}: la fuente "${ref}" no existe en fuentes-oftalmo.yaml`)
    }
  })
  return errores
}
