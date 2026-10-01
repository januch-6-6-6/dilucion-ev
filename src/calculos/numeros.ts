/**
 * Lee un número escrito por el usuario a la chilena: coma decimal y punto como separador
 * de miles ("1.000" = mil, "1.000,5" = mil coma cinco). Un punto seguido de 1–2 o 4+ dígitos
 * se acepta como decimal ("1.5"). Devuelve null si no es un número > 0.
 */
export function parsearNumero(texto: string): number | null {
  let limpio = texto.trim()
  if (/^\d{1,3}(\.\d{3})+(,\d+)?$/.test(limpio)) limpio = limpio.replace(/\./g, '')
  limpio = limpio.replace(',', '.')
  if (limpio === '' || !/^[0-9]*\.?[0-9]+$/.test(limpio)) return null
  const n = Number(limpio)
  return Number.isFinite(n) && n > 0 ? n : null
}
