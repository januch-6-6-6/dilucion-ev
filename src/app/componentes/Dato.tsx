import type { ReactNode } from 'react'

export const SIN_DATOS = 'sin datos en las fuentes'

type Props = {
  etiqueta: string
  valor?: ReactNode
  unidad?: string
  fuente?: { ref: string; detalle: string }
}

/** Muestra un dato con su unidad y su fuente; si no hay valor, lo dice explícitamente. */
export default function Dato({ etiqueta, valor, unidad, fuente }: Props) {
  const vacio = valor === undefined || valor === null || valor === ''
  return (
    <div className="dato">
      <dt>{etiqueta}</dt>
      <dd>
        {vacio ? (
          <span className="sin-datos">{SIN_DATOS}</span>
        ) : (
          <>
            {typeof valor === 'number' ? String(valor).replace('.', ',') : valor}
            {unidad ? ` ${unidad}` : ''}
          </>
        )}
        {fuente && !vacio && (
          <cite className="fuente" title={fuente.detalle}>
            {' '}
            [{fuente.ref}]
          </cite>
        )}
      </dd>
    </div>
  )
}
