import { useState } from 'react'
import { AVISO } from '../aviso'

const CLAVE = 'dilucion-ev:aviso-aceptado'

function aceptado(): boolean {
  try {
    return localStorage.getItem(CLAVE) === '1'
  } catch {
    return false
  }
}

export default function AvisoInicial() {
  const [visible, setVisible] = useState(() => !aceptado())
  if (!visible) return null
  const aceptar = () => {
    try {
      localStorage.setItem(CLAVE, '1')
    } catch {
      /* sin almacenamiento: se mostrará de nuevo la próxima vez */
    }
    setVisible(false)
  }
  return (
    <div className="fondo-modal">
      <div role="dialog" aria-modal="true" aria-labelledby="aviso-titulo" className="modal">
        <h2 id="aviso-titulo">Antes de usar</h2>
        <p>{AVISO}</p>
        <button type="button" onClick={aceptar} autoFocus>
          Entendido
        </button>
      </div>
    </div>
  )
}
