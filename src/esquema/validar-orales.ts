import { convertirMasa } from '../calculos/unidades'
import { Fuente } from './ficha'
import { DosisOral, FichaOral } from './ficha-oral'

const UNIDADES_MASA = ['g', 'mg', 'mcg', 'UI', 'mEq', 'mmol'] as const
type Masa = (typeof UNIDADES_MASA)[number]
const esMasa = (u: string): u is Masa => (UNIDADES_MASA as readonly string[]).includes(u)

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

/** 'dos_fuentes' si las dosis citan al menos 2 instituciones distintas; si no, 'fuente_unica'. */
export function verificacionDe(ficha: FichaOral, fuentes: Fuente[]): 'dos_fuentes' | 'fuente_unica' {
  const institucionPorRef = new Map(fuentes.map((f) => [f.id, f.institucion]))
  const instituciones = new Set<string>()
  for (const d of ficha.dosis) {
    const inst = institucionPorRef.get(d.fuente.ref)
    if (inst !== undefined) instituciones.add(inst)
  }
  return instituciones.size >= 2 ? 'dos_fuentes' : 'fuente_unica'
}

const NUMERO = /-?\d+([.,]\d+)?/
const primerNumero = (s: string): number | null => {
  const m = NUMERO.exec(s)
  return m ? Number(m[0].replace(',', '.')) : null
}

/** Cifra por toma de una dosis en mg, o null si no es comparable. */
function porTomaMg(d: DosisOral, comoTope: boolean): number | null {
  try {
    if (d.regimen === 'por_peso') {
      const t = d.topePorToma
      return t && t.unidad !== 'UI' ? convertirMasa(t.valor, t.unidad, 'mg') : null
    }
    if (d.regimen !== 'fija' || d.base === 'dia' || !esMasa(d.unidad) || d.unidad === 'UI') return null
    const v = comoTope ? (d.topePorToma ? convertirMasa(d.topePorToma.valor, d.topePorToma.unidad, 'mg') : null) : null
    if (v !== null) return v
    const cifra = d.max ?? d.min
    return cifra === undefined ? null : convertirMasa(cifra, d.unidad, 'mg')
  } catch {
    return null
  }
}

/** Valida fichas orales y sus fuentes. Devuelve errores legibles; lista vacía = todo OK. */
export function validarOrales(fichasCrudas: unknown[], fuentesCrudas: unknown[]): string[] {
  const errores: string[] = []

  const idsFuente = new Set<string>()
  fuentesCrudas.forEach((f, i) => {
    const r = Fuente.safeParse(f)
    if (!r.success) errores.push(`fuentes-orales.yaml[${i}]: ${r.error.issues.map((x) => `${x.path.join('.')} ${x.message}`).join('; ')}`)
    else idsFuente.add(r.data.id)
  })

  const vistos = new Set<string>()
  fichasCrudas.forEach((crudo, i) => {
    const etiqueta = (crudo as { id?: string })?.id ?? `ficha[${i}]`
    const r = FichaOral.safeParse(crudo)
    if (!r.success) {
      for (const x of r.error.issues) errores.push(`${etiqueta}: ${x.path.join('.')} — ${x.message}`)
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
      if (!idsFuente.has(ref)) errores.push(`${ruta}: la fuente "${ref}" no existe en fuentes-orales.yaml`)
    }

    ficha.dosis.forEach((d, j) => {
      if (d.min !== undefined && d.max !== undefined && d.min > d.max) errores.push(`${ficha.id}: dosis[${j}] min mayor que max`)
    })

    const topesAdulto = ficha.dosis.flatMap((d) => (d.poblacion === 'adulto' ? [porTomaMg(d, true)] : [])).filter((x): x is number => x !== null)
    if (topesAdulto.length) {
      const tope = Math.max(...topesAdulto)
      ficha.dosis.forEach((d, j) => {
        if (d.poblacion !== 'pediatrico') return
        const v = porTomaMg(d, false)
        if (v !== null && v > tope) {
          errores.push(`${ficha.id}: dosis[${j}] la dosis pediátrica por toma (${v} mg) supera el tope de adulto (${tope} mg)`)
        }
      })
    }

    ficha.discrepancias.forEach((dc, j) => {
      const mostrado = primerNumero(dc.mostrado)
      const valores = dc.valores.map((v) => primerNumero(v.valor))
      if (mostrado === null || valores.length === 0 || valores.some((v) => v === null)) return
      const menor = Math.min(...(valores as number[]))
      if (mostrado > menor) {
        errores.push(`${ficha.id}: discrepancias[${j}] — el valor mostrado (${mostrado}) no es el menor de los valores de las fuentes (${menor})`)
      }
    })
  })

  return errores
}
