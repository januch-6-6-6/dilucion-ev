import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { buscar } from '../../busqueda/buscar'
import { obtenerOral, orales, verificacion } from '../../datos/cargarOrales'
import type { FichaOral } from '../../esquema/ficha-oral'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import { leerFavoritosOrales, leerRecientesOrales } from './guardadoOrales'

function ListaItems({ fichas, titulo }: { fichas: FichaOral[]; titulo: string }) {
  if (fichas.length === 0) return <p className="vacio">No hay medicamentos para mostrar.</p>
  return (
    <ul className="lista-medicamentos" aria-label={titulo}>
      {fichas.map((f) => (
        <li key={f.id}>
          <Link to={`/orales/m/${f.id}`} className="item-medicamento" data-color={colorGrupo(f.grupo)}>
            <span className="nombre">{f.nombre}</span>
            <span className="grupo chip-grupo">{etiquetaGrupo(f.grupo)}</span>
            {f.altoRiesgo && <span className="etiqueta alto-riesgo">Alto riesgo</span>}
            {verificacion(f) === 'fuente_unica' && <span className="etiqueta fuente-unica">Una sola fuente</span>}
          </Link>
        </li>
      ))}
    </ul>
  )
}

const aFichas = (ids: string[]) => ids.map(obtenerOral).filter((f): f is FichaOral => f !== undefined)

export default function ListaOrales() {
  const [texto, setTexto] = useState('')
  const resultados = useMemo(() => buscar(texto, orales), [texto])
  const favoritos = useMemo(() => aFichas(leerFavoritosOrales()), [])
  const recientes = useMemo(() => aFichas(leerRecientesOrales()), [])
  const porGrupo = useMemo(() => {
    const mapa = new Map<string, FichaOral[]>()
    for (const f of orales) mapa.set(f.grupo, [...(mapa.get(f.grupo) ?? []), f])
    return [...mapa.entries()]
      .sort((a, b) => etiquetaGrupo(a[0]).localeCompare(etiquetaGrupo(b[0]), 'es'))
      .map(([g, fs]) => [g, [...fs].sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))] as const)
  }, [])

  return (
    <section className="inicio">
      <label className="buscador">
        <svg className="lupa" viewBox="0 0 24 24" aria-hidden="true" width="22" height="22">
          <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2.2" />
          <path d="M16.5 16.5 21 21" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
        </svg>
        <span className="visualmente-oculto">Buscar medicamento oral</span>
        <input
          type="search"
          placeholder="Buscar medicamento oral (genérico o comercial)"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
        />
      </label>

      {texto ? (
        <ListaItems fichas={resultados} titulo="Resultados de búsqueda de orales" />
      ) : (
        <>
          {favoritos.length > 0 && (
            <>
              <h2 className="titulo-seccion">Mis favoritos</h2>
              <ListaItems fichas={favoritos} titulo="Medicamentos favoritos" />
            </>
          )}
          {recientes.length > 0 && (
            <>
              <h2 className="titulo-seccion">Últimos consultados</h2>
              <ListaItems fichas={recientes} titulo="Medicamentos consultados recientemente" />
            </>
          )}
          {orales.length === 0 && <p className="vacio">No hay medicamentos para mostrar.</p>}
          {porGrupo.map(([g, fichas]) => (
            <div key={g}>
              <h2 className="titulo-seccion">{etiquetaGrupo(g)}</h2>
              <ListaItems fichas={fichas} titulo={`Orales: ${etiquetaGrupo(g)}`} />
            </div>
          ))}
        </>
      )}
    </section>
  )
}
