import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { buscar } from '../../busqueda/buscar'
import { medicamentos, obtenerFicha } from '../../datos/cargar'
import type { Ficha } from '../../esquema/ficha'
import ListaMedicamentos from '../componentes/ListaMedicamentos'
import { colorGrupo } from '../colores'
import { AMBITOS, etiquetaGrupo } from '../etiquetas'
import { leerRecientes } from '../recientes'

export default function Inicio() {
  const [texto, setTexto] = useState('')
  const resultados = useMemo(() => buscar(texto, medicamentos), [texto])
  const recientes = useMemo(
    () => leerRecientes().map(obtenerFicha).filter((f): f is Ficha => f !== undefined),
    [],
  )
  const grupos = useMemo(() => [...new Set(medicamentos.map((m) => m.grupo))].sort((a, b) => etiquetaGrupo(a).localeCompare(etiquetaGrupo(b), 'es')), [])

  return (
    <section className="inicio">
      <label className="buscador">
        <svg className="lupa" viewBox="0 0 24 24" aria-hidden="true" width="22" height="22">
          <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2.2" />
          <path d="M16.5 16.5 21 21" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
        </svg>
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
              <Link key={id} to={`/ambito/${id}`} className="acceso acceso-ambito" data-ambito={id}>
                {nombre}
              </Link>
            ))}
          </nav>
          {recientes.length > 0 && (
            <>
              <h2 className="titulo-seccion">Últimos consultados</h2>
              <ListaMedicamentos fichas={recientes} titulo="Medicamentos consultados recientemente" />
            </>
          )}
          <h2 className="titulo-seccion">Por grupo</h2>
          <nav aria-label="Grupos" className="accesos">
            {grupos.map((g) => (
              <Link key={g} to={`/grupo/${g}`} className="acceso acceso-grupo" data-color={colorGrupo(g)}>
                {etiquetaGrupo(g)}
              </Link>
            ))}
          </nav>
          <div className="accesos-pie">
            <Link to="/calcular" className="boton boton-secundario">Calculadora libre</Link>
            <Link to="/acerca" className="boton boton-secundario">Acerca de</Link>
          </div>
        </>
      )}
    </section>
  )
}
