/** Redondeo half-up a `decimales`, sin ruido de coma flotante. */
export function redondear(valor: number, decimales: number): number {
  const [mantisa, exponente = '0'] = String(valor).split('e')
  const desplazado = Math.round(Number(`${mantisa}e${Number(exponente) + decimales}`))
  const resultado = Number(`${desplazado}e-${decimales}`)
  return resultado === 0 ? 0 : resultado
}
