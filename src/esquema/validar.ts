import { Ficha, Fuente } from './ficha'

/** Recorre un objeto y devuelve todas las referencias `fuente.ref` con su ruta. */
function refsDeFuente(valor: unknown, ruta: string, salida: { ruta: string; ref: string }[]) {
  if (Array.isArray(valor)) {
    valor.forEach((v, i) => refsDeFuente(v, `${ruta}[${i}]`, salida))
  } else if (valor && typeof valor === 'object') {
    for (const [k, v] of Object.entries(valor)) {
      if (k === 'fuente' && v && typeof v === 'object' && 'ref' in v) salida.push({ ruta: `${ruta}.fuente`, ref: String(v.ref) })
      else refsDeFuente(v, `${ruta}.${k}`, salida)
    }
  }
}

/** Valida fichas y fuentes. Devuelve errores legibles; lista vacía = todo OK. */
export function validarDatos(fichasCrudas: unknown[], fuentesCrudas: unknown[]): string[] {
  const errores: string[] = []

  const idsFuente = new Set<string>()
  fuentesCrudas.forEach((f, i) => {
    const r = Fuente.safeParse(f)
    if (!r.success) errores.push(`fuentes.yaml[${i}]: ${r.error.issues.map((x) => `${x.path.join('.')} ${x.message}`).join('; ')}`)
    else idsFuente.add(r.data.id)
  })

  const fichas: Ficha[] = []
  const vistos = new Set<string>()
  fichasCrudas.forEach((crudo, i) => {
    const etiqueta = (crudo as { id?: string })?.id ?? `ficha[${i}]`
    const r = Ficha.safeParse(crudo)
    if (!r.success) {
      for (const x of r.error.issues) errores.push(`${etiqueta}: ${x.path.join('.')} — ${x.message}`)
      return
    }
    const ficha = r.data
    if (vistos.has(ficha.id)) errores.push(`${ficha.id}: id repetido`)
    vistos.add(ficha.id)
    fichas.push(ficha)

    const refs: { ruta: string; ref: string }[] = []
    refsDeFuente(ficha, ficha.id, refs)
    for (const { ruta, ref } of refs) {
      if (!idsFuente.has(ref)) errores.push(`${ruta}: la fuente "${ref}" no existe en fuentes.yaml`)
    }

    ficha.dosis.forEach((d, j) => {
      if (d.min !== undefined && d.max !== undefined && d.min > d.max) errores.push(`${ficha.id}: dosis[${j}] min mayor que max`)
    })
    const { concentracionMin: cmin, concentracionMax: cmax } = ficha.dilucion
    if (cmin && cmax && cmin.unidad === cmax.unidad && cmin.valor > cmax.valor) {
      errores.push(`${ficha.id}: dilucion concentracionMin mayor que concentracionMax (min mayor que max)`)
    }

    const tienePediatrica = ficha.dosis.some((d) => d.poblacion === 'pediatrico')
    if (ficha.sinDosisPediatrica === tienePediatrica) {
      errores.push(`${ficha.id}: sinDosisPediatrica=${ficha.sinDosisPediatrica} no calza con las dosis pediátricas registradas`)
    }
  })

  const porId = new Map(fichas.map((f) => [f.id, f]))
  for (const a of fichas) {
    for (const c of a.compatibilidad) {
      const b = porId.get(c.con)
      if (!b) continue
      const inversa = b.compatibilidad.find((x) => x.con === a.id)
      if (inversa && inversa.estado !== c.estado && a.id < b.id) {
        errores.push(`compatibilidad asimétrica: ${a.id}→${b.id} = ${c.estado}, ${b.id}→${a.id} = ${inversa.estado}`)
      }
      if (!inversa && c.estado === 'incompatible') {
        errores.push(`compatibilidad asimétrica: ${a.id} es incompatible con ${b.id}, pero ${b.id} no lo registra`)
      }
    }
  }

  return errores
}
