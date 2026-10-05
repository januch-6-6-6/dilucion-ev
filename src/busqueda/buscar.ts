type Buscable = { nombre: string; comerciales: string[] }

export const normalizar = (s: string) =>
  s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim()

function levenshtein(a: string, b: string): number {
  const fila = Array.from({ length: b.length + 1 }, (_, j) => j)
  for (let i = 1; i <= a.length; i++) {
    let previo = fila[0]
    fila[0] = i
    for (let j = 1; j <= b.length; j++) {
      const temp = fila[j]
      fila[j] = Math.min(fila[j] + 1, fila[j - 1] + 1, previo + (a[i - 1] === b[j - 1] ? 0 : 1))
      previo = temp
    }
  }
  return fila[b.length]
}

/** Puntaje: 0 = prefijo, 1 = substring, 2 = tolerancia a errores; null = no coincide. */
function puntaje(q: string, ficha: Buscable): number | null {
  const textos = [ficha.nombre, ...ficha.comerciales].map(normalizar)
  if (textos.some((t) => t.startsWith(q) || t.split(/[\s()/-]+/).some((p) => p.startsWith(q)))) {
    return textos.some((t) => t.startsWith(q)) ? 0 : 1
  }
  if (textos.some((t) => t.includes(q))) return 1
  if (q.length >= 5) {
    const palabras = textos.flatMap((t) => t.split(/[\s()/-]+/)).filter(Boolean)
    if (palabras.some((p) => levenshtein(q, p) <= 2)) return 2
  }
  return null
}

export function buscar<T extends Buscable>(texto: string, lista: T[]): T[] {
  const q = normalizar(texto)
  if (!q) return []
  return lista
    .map((f) => ({ f, p: puntaje(q, f) }))
    .filter((x): x is { f: T; p: number } => x.p !== null)
    .sort((a, b) => a.p - b.p || a.f.nombre.localeCompare(b.f.nombre, 'es'))
    .map((x) => x.f)
}
