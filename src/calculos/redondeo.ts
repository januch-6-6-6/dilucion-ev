/** Redondeo half-up a `decimales`, sin ruido de coma flotante (incluido el acumulado en un cálculo). */
export function redondear(valor: number, decimales: number): number {
  const limpio = Number(valor.toPrecision(12))
  const [mantisa, exponente = '0'] = String(limpio).split('e')
  const desplazado = Math.round(Number(`${mantisa}e${Number(exponente) + decimales}`))
  const resultado = Number(`${desplazado}e-${decimales}`)
  return resultado === 0 ? 0 : resultado
}
