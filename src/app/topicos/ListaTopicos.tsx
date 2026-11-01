import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { buscar } from '../../busqueda/buscar'
import { obtenerTopico, topicos, verificacionDeTopico } from '../../datos/cargarTopicos'
import type { FichaTopica, Via } from '../../esquema/ficha-topica'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import { leerFavoritosTopicos, leerRecientesTopicos } from './guardadoTopicos'
import { VIA } from './textos'

function ListaItems({ fichas, titulo }: { fichas: FichaTopica[]; titulo: string }) {
  if (fichas.length === 0) return <p className="vacio">No hay medicamentos para mostrar.</p>
  return (
    <ul className="lista-medicamentos" aria-label={titulo}>
      {fichas.map((f) => {
        const v = verificacionDeTopico(f)
        return (
          <li key={f.id}>
            <Link to={`/topicos/m/${f.id}`} className="item-medicamento" data-color={colorGrupo(f.grupo)}>
              <span className="nombre">{f.nombre}</span>
              <span className="grupo chip-grupo">
                {etiquetaGrupo(f.grupo)} · {f.vias.map((x) => VIA[x]).join(', ')}
              </span>
              {f.altoRiesgo && <span className="etiqueta alto-riesgo">Alto riesgo</span>}
              {v === 'fuente_unica' && <span className="etiqueta fuente-unica">Una sola fuente</span>}
              {v === 'sin_pauta' && <span className="etiqueta fuente-unica">Sin pauta</span>}
            </Link>
          </li>
        )
      })}
    </ul>
  )
}

const aFichas = (ids: string[]) => ids.map(obtenerTopico).filter((f): f is FichaTopica => f !== undefined)
const VIAS: (Via | 'todas')[] = ['todas', 'ojo', 'oido', 'nariz']

export default function ListaTopicos() {
  const [texto, setTexto] = useState('')
  const [via, setVia] = useState<Via | 'todas'>('todas')
  const visibles = useMemo(() => (via === 'todas' ? topicos : topicos.filter((t) => t.vias.includes(via))), [via])
  const resultados = useMemo(() => buscar(texto, visibles), [texto, visibles])
  const favoritos = useMemo(() => aFichas(leerFavoritosTopicos()), [])
  const recientes = useMemo(() => aFichas(leerRecientesTopicos()), [])
  const porGrupo = useMemo(() => {
    const mapa = new Map<string, FichaTopica[]>()
    for (const f of visibles) mapa.set(f.grupo, [...(mapa.get(f.grupo) ?? []), f])
    return [...mapa.entries()]
      .sort((a, b) => etiquetaGrupo(a[0]).localeCompare(etiquetaGrupo(b[0]), 'es'))
      .map(([g, fs]) => [g, [...fs].sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))] as const)
  }, [visibles])

  return (
    <section className="inicio">
      <label className="buscador">
        <svg className="lupa" viewBox="0 0 24 24" aria-hidden="true" width="22" height="22">
          <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2.2" />
          <path d="M16.5 16.5 21 21" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
        </svg>
        <span className="visualmente-oculto">Buscar tópico de ojo, oído o nariz</span>
        <input type="search" placeholder="Buscar colirio, gota ótica o spray nasal" value={texto} onChange={(e) => setTexto(e.target.value)} />
      </label>
      <div role="group" aria-label="Filtrar por vía" className="pestanas">
        {VIAS.map((v) => (
          <button key={v} type="button" aria-pressed={via === v} onClick={() => setVia(v)}>
            {v === 'todas' ? 'Todas' : VIA[v]}
          </button>
        ))}
      </div>

      {texto ? (
        <ListaItems fichas={resultados} titulo="Resultados de búsqueda de tópicos" />
      ) : (
        <>
          {favoritos.length > 0 && (
            <>
              <h2 className="titulo-seccion">Mis favoritos</h2>
              <ListaItems fichas={favoritos} titulo="Tópicos favoritos" />
            </>
          )}
          {recientes.length > 0 && (
            <>
              <h2 className="titulo-seccion">Últimos consultados</h2>
              <ListaItems fichas={recientes} titulo="Tópicos consultados recientemente" />
            </>
          )}
          {visibles.length === 0 && <p className="vacio">No hay medicamentos para mostrar.</p>}
          {porGrupo.map(([g, fichas]) => (
            <div key={g}>
              <h2 className="titulo-seccion">{etiquetaGrupo(g)}</h2>
              <ListaItems fichas={fichas} titulo={`Tópicos: ${etiquetaGrupo(g)}`} />
            </div>
          ))}
        </>
      )}
    </section>
  )
}
