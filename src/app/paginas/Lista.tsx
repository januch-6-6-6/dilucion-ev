import { Link, useParams } from 'react-router-dom'
import { medicamentos } from '../../datos/cargar'
import ListaMedicamentos from '../componentes/ListaMedicamentos'
import { AMBITOS, etiquetaGrupo } from '../etiquetas'

export default function Lista() {
  const { ambito, grupo } = useParams()
  const fichas = medicamentos.filter((m) =>
    ambito ? (m.ambitos as string[]).includes(ambito) : grupo ? m.grupo === grupo : false,
  )
  const titulo = ambito ? (AMBITOS[ambito] ?? ambito) : etiquetaGrupo(grupo ?? '')
  return (
    <section>
      <p>
        <Link to="/">← Inicio</Link>
      </p>
      <h2>{titulo}</h2>
      <ListaMedicamentos fichas={fichas} titulo={`Medicamentos: ${titulo}`} />
    </section>
  )
}
