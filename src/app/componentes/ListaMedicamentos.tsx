import { Link } from 'react-router-dom'
import type { Ficha } from '../../esquema/ficha'
import { etiquetaGrupo } from '../etiquetas'

export default function ListaMedicamentos({ fichas, titulo }: { fichas: Ficha[]; titulo: string }) {
  if (fichas.length === 0) return <p className="vacio">No hay medicamentos para mostrar.</p>
  return (
    <ul className="lista-medicamentos" aria-label={titulo}>
      {fichas.map((f) => (
        <li key={f.id}>
          <Link to={`/m/${f.id}`} className="item-medicamento">
            <span className="nombre">{f.nombre}</span>
            <span className="grupo">{etiquetaGrupo(f.grupo)}</span>
            {f.altoRiesgo && <span className="etiqueta alto-riesgo">Alto riesgo</span>}
          </Link>
        </li>
      ))}
    </ul>
  )
}
