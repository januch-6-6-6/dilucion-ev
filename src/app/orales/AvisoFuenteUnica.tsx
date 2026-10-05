export const TEXTO_FUENTE_UNICA = 'Esta ficha se apoya en una sola fuente y no se pudo contrastar con otra.'

export default function AvisoFuenteUnica() {
  return (
    <p role="note" className="aviso aviso-fuente-unica">
      {TEXTO_FUENTE_UNICA}
    </p>
  )
}
