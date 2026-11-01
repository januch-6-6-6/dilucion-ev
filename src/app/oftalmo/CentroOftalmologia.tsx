import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { buscar } from '../../busqueda/buscar'
import { obtenerOcular, oculares, verificacionDeOcular } from '../../datos/cargarOculares'
import { orales, verificacion as verificacionOral } from '../../datos/cargarOrales'
import { topicos, verificacionDeTopico } from '../../datos/cargarTopicos'
import type { FamiliaOcular, FichaOcular } from '../../esquema/ficha-ocular'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import { leerFavoritosOculares } from './guardadoOculares'
import { AVISO_FORMACION, AVISO_PABELLON, FAMILIA } from './textos'

const PESTANAS = ['Pabellón', 'Orales', 'Colirios'] as const
type Pestana = (typeof PESTANAS)[number]
const FAMILIAS: FamiliaOcular[] = ['intracameral', 'intravitreo', 'bloqueo', 'periocular', 'antifibrotico']

type Item = { id: string; nombre: string; comerciales: string[]; grupo: string; ruta: string; etiquetas: { texto: string; clase: string }[] }

const porNombre = (a: { nombre: string }, b: { nombre: string }) => a.nombre.localeCompare(b.nombre, 'es')

function aItemPabellon(f: FichaOcular): Item {
  const v = verificacionDeOcular(f)
  return {
    id: f.id,
    nombre: f.nombre,
    comerciales: f.comerciales,
    grupo: f.grupo,
    ruta: `/oftalmologia/m/${f.id}`,
    etiquetas: [
      ...(f.registroChile === 'no_registrado' ? [{ texto: 'No registrado en Chile', clase: 'fuente-unica' }] : []),
      ...(v === 'fuente_unica' ? [{ texto: 'Una sola fuente', clase: 'fuente-unica' }] : []),
      ...(v === 'sin_pauta' ? [{ texto: 'Sin pauta', clase: 'fuente-unica' }] : []),
    ],
  }
}

function ListaItems({ items, titulo }: { items: Item[]; titulo: string }) {
  if (items.length === 0) return <p className="vacio">No hay medicamentos para mostrar.</p>
  return (
    <ul className="lista-medicamentos" aria-label={titulo}>
      {items.map((i) => (
        <li key={i.id}>
          <Link to={i.ruta} className="item-medicamento" data-color={colorGrupo(i.grupo)}>
            <span className="nombre">{i.nombre}</span>
            <span className="grupo chip-grupo">{etiquetaGrupo(i.grupo)}</span>
            {i.etiquetas.map((e) => (
              <span key={e.texto} className={`etiqueta ${e.clase}`}>
                {e.texto}
              </span>
            ))}
          </Link>
        </li>
      ))}
    </ul>
  )
}

export default function CentroOftalmologia() {
  const [activa, setActiva] = useState<Pestana>('Pabellón')
  const [texto, setTexto] = useState('')

  const pabellon = useMemo(() => oculares.map(aItemPabellon), [])
  const oralesOft = useMemo<Item[]>(
    () =>
      orales
        .filter((o) => o.usos?.includes('oftalmologia'))
        .map((o) => ({
          id: o.id,
          nombre: o.nombre,
          comerciales: o.comerciales,
          grupo: o.grupo,
          ruta: `/orales/m/${o.id}`,
          etiquetas: [
            ...(o.presentaciones.some((p) => p.registroChile === 'no_registrado') ? [{ texto: 'No registrado en Chile', clase: 'fuente-unica' }] : []),
            ...(verificacionOral(o) === 'fuente_unica' ? [{ texto: 'Una sola fuente', clase: 'fuente-unica' }] : []),
          ],
        }))
        .sort(porNombre),
    [],
  )
  const colirios = useMemo<Item[]>(
    () =>
      topicos
        .filter((t) => t.vias.includes('ojo'))
        .map((t) => ({
          id: t.id,
          nombre: t.nombre,
          comerciales: t.comerciales,
          grupo: t.grupo,
          ruta: `/topicos/m/${t.id}`,
          etiquetas: [
            ...(t.altoRiesgo ? [{ texto: 'Alto riesgo', clase: 'alto-riesgo' }] : []),
            ...(verificacionDeTopico(t) === 'fuente_unica' ? [{ texto: 'Una sola fuente', clase: 'fuente-unica' }] : []),
          ],
        }))
        .sort(porNombre),
    [],
  )
  const favoritos = useMemo(
    () => leerFavoritosOculares().map(obtenerOcular).filter((f): f is FichaOcular => f !== undefined).map(aItemPabellon),
    [],
  )

  const lista = activa === 'Pabellón' ? pabellon : activa === 'Orales' ? oralesOft : colirios
  const resultados = useMemo(() => buscar(texto, lista), [texto, lista])
  const porFamilia = useMemo(
    () =>
      FAMILIAS.map((fam) => {
        const ids = new Set(oculares.filter((o) => o.familias[0] === fam).map((o) => o.id))
        return [fam, pabellon.filter((i) => ids.has(i.id)).sort(porNombre)] as const
      }).filter(([, items]) => items.length > 0),
    [pabellon],
  )
  const porGrupo = useMemo(() => {
    const mapa = new Map<string, Item[]>()
    for (const i of lista) mapa.set(i.grupo, [...(mapa.get(i.grupo) ?? []), i])
    return [...mapa.entries()].sort((a, b) => etiquetaGrupo(a[0]).localeCompare(etiquetaGrupo(b[0]), 'es'))
  }, [lista])

  return (
    <section className="inicio">
      <p role="note" className="aviso">
        {AVISO_FORMACION}
      </p>
      <p role="note" className="aviso">
        {AVISO_PABELLON}
      </p>
      <p className="sin-datos">Las preparaciones intraoculares de Pabellón son todas de alto riesgo: cada ficha muestra su fuente.</p>
      <label className="buscador">
        <svg className="lupa" viewBox="0 0 24 24" aria-hidden="true" width="22" height="22">
          <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2.2" />
          <path d="M16.5 16.5 21 21" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
        </svg>
        <span className="visualmente-oculto">Buscar medicamento de uso oftalmológico</span>
        <input type="search" placeholder="Buscar por nombre o marca" value={texto} onChange={(e) => setTexto(e.target.value)} />
      </label>
      <div role="tablist" aria-label="Secciones de Oftalmología" className="pestanas">
        {PESTANAS.map((p) => (
          <button key={p} role="tab" type="button" aria-selected={activa === p} aria-controls={activa === p ? `panel-${p}` : undefined} id={`tab-${p}`} onClick={() => setActiva(p)}>
            {p}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`panel-${activa}`} aria-labelledby={`tab-${activa}`}>
        {texto ? (
          <ListaItems items={resultados} titulo="Resultados de búsqueda de Oftalmología" />
        ) : activa === 'Pabellón' ? (
          <>
            {favoritos.length > 0 && (
              <>
                <h3 className="titulo-seccion">Mis favoritos</h3>
                <ListaItems items={favoritos} titulo="Favoritos de pabellón" />
              </>
            )}
            {porFamilia.map(([fam, items]) => (
              <div key={fam}>
                <h2 className="titulo-seccion">{FAMILIA[fam]}</h2>
                <ListaItems items={items} titulo={`Pabellón: ${FAMILIA[fam]}`} />
              </div>
            ))}
          </>
        ) : (
          <>
            <p className="sin-datos">
              {activa === 'Orales'
                ? 'Medicamentos orales con indicación oftalmológica; la ficha abre en la sección Orales.'
                : 'Colirios, ungüentos y otros tópicos de vía oftálmica; la ficha abre en la sección Tópicos.'}
            </p>
            {porGrupo.map(([g, items]) => (
              <div key={g}>
                <h3 className="titulo-seccion">{etiquetaGrupo(g)}</h3>
                <ListaItems items={items.sort(porNombre)} titulo={`${activa}: ${etiquetaGrupo(g)}`} />
              </div>
            ))}
          </>
        )}
      </div>
    </section>
  )
}
