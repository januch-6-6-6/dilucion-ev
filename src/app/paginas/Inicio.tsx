import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { buscar } from '../../busqueda/buscar'
import { medicamentos, obtenerFicha } from '../../datos/cargar'
import type { Ficha } from '../../esquema/ficha'
import ListaMedicamentos from '../componentes/ListaMedicamentos'
import { AMBITOS, etiquetaGrupo } from '../etiquetas'
import { leerRecientes } from '../recientes'

export default function Inicio() {
  const [texto, setTexto] = useState('')
  const resultados = useMemo(() => buscar(texto, medicamentos), [texto])
  const recientes = useMemo(
    () => leerRecientes().map(obtenerFicha).filter((f): f is Ficha => f !== undefined),
    [],
  )
  const grupos = useMemo(() => [...new Set(medicamentos.map((m) => m.grupo))].sort(), [])

  return (
    <section className="inicio">
      <label className="buscador">
        <span className="visualmente-oculto">Buscar medicamento</span>
        <input
          type="search"
          placeholder="Buscar medicamento (genérico o comercial)"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          autoFocus
        />
      </label>

      {texto ? (
        <ListaMedicamentos fichas={resultados} titulo="Resultados de búsqueda de medicamentos" />
      ) : (
        <>
          <nav aria-label="Ámbitos" className="accesos">
            {Object.entries(AMBITOS).map(([id, nombre]) => (
              <Link key={id} to={`/ambito/${id}`} className="acceso">
                {nombre}
              </Link>
            ))}
          </nav>
          {recientes.length > 0 && (
            <>
              <h2>Últimos consultados</h2>
              <ListaMedicamentos fichas={recientes} titulo="Medicamentos consultados recientemente" />
            </>
          )}
          <h2>Por grupo</h2>
          <nav aria-label="Grupos" className="accesos">
            {grupos.map((g) => (
              <Link key={g} to={`/grupo/${g}`} className="acceso">
                {etiquetaGrupo(g)}
              </Link>
            ))}
          </nav>
          <p>
            <Link to="/calcular">Calculadora libre</Link> · <Link to="/acerca">Acerca de</Link>
          </p>
        </>
      )}
    </section>
  )
}
