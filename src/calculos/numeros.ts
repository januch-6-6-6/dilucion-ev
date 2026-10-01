/** Lee un número escrito por el usuario (acepta coma decimal). Devuelve null si no es un número > 0. */
export function parsearNumero(texto: string): number | null {
  const limpio = texto.trim().replace(',', '.')
  if (limpio === '' || !/^[0-9]*\.?[0-9]+$/.test(limpio)) return null
  const n = Number(limpio)
  return Number.isFinite(n) && n > 0 ? n : null
}
