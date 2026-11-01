import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { combinacionesCalculables } from '../../calculos/duracionEnvase'
import { fuentesTopicos, obtenerTopico, verificacionDeTopico } from '../../datos/cargarTopicos'
import type { DosisTopica, FichaTopica as TFicha } from '../../esquema/ficha-topica'
import Dato from '../componentes/Dato'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import AvisoFuenteUnica from '../orales/AvisoFuenteUnica'
import TablaDiscrepancias from '../orales/TablaDiscrepancias'
import { alternarFavoritoTopico, esFavoritoTopico, registrarRecienteTopico } from './guardadoTopicos'
import { describirPresentacion, PEDIATRIA, TEXTO_SIN_PAUTA, VIA } from './textos'

const PESTANAS = ['Dosis', 'Presentaciones', 'Conservación', 'Administración', 'Discrepancias', 'Fuentes'] as const
type Pestana = (typeof PESTANAS)[number]

function textoDosis(d: DosisTopica, f: TFicha): string {
  const partes = [d.texto]
  if (d.duracion) partes.push(d.duracion)
  if (d.condicion) partes.push(d.condicion)
  if (d.presentaciones) {
    const solo = f.presentaciones.filter((p) => d.presentaciones?.includes(p.id)).map(describirPresentacion)
    partes.push(`Solo para: ${solo.join('; ')}`)
  }
  return partes.join('. ')
}

function Dosis({ f }: { f: TFicha }) {
  if (f.sinPauta) {
    return (
      <div role="note" className="aviso">
        <p>
          <strong>{TEXTO_SIN_PAUTA}</strong>
        </p>
        <p>{f.sinPauta.motivo}</p>
        <p>Consulta la indicación médica y la ficha del producto que tienes en la mano.</p>
      </div>
    )
  }
  return (
    <>
      {(['adulto', 'pediatrico'] as const).map((pob) => {
        const dosis = f.dosis.filter((d) => d.poblacion === pob)
        return (
          <section key={pob}>
            <h3>{pob === 'adulto' ? 'Dosis adulto' : 'Dosis pediátrica'}</h3>
            {pob === 'pediatrico' && (
              <p className={f.pediatria.estado === 'contraindicada' ? 'alerta-roja' : 'sin-datos'}>
                {PEDIATRIA[f.pediatria.estado]}: {f.pediatria.motivo}
              </p>
            )}
            {dosis.length === 0 ? (
              pob === 'adulto' && <p className="sin-datos">sin datos en las fuentes</p>
            ) : (
              <dl>
                {dosis.map((d, i) => (
                  <Dato
                    key={`${d.indicacion}-${i}`}
                    etiqueta={d.indicacion}
                    valor={
                      <>
                        {textoDosis(d, f)}{' '}
                        <span className={`etiqueta ${d.estatus === 'autorizada' ? 'autorizada' : 'off-label'}`}>
                          {d.estatus === 'autorizada' ? 'Autorizada' : 'Off-label'}
                        </span>
                        {d.tambien?.map((t) => (
                          <span key={t.ref} className="tambien">
                            {' '}
                            Concuerda: <cite className="fuente" title={t.detalle}>[{t.ref}]</cite>
                          </span>
                        ))}
                      </>
                    }
                    fuente={d.fuente}
                  />
                ))}
              </dl>
            )}
          </section>
        )
      })}
    </>
  )
}

function Presentaciones({ f }: { f: TFicha }) {
  return (
    <ul className="presentaciones">
      {f.presentaciones.map((p) => (
        <li key={p.id}>
          <dl>
            <Dato
              etiqueta={describirPresentacion(p)}
              valor={
                <>
                  Registro ISP: {p.registrosIsp.join(', ')}
                  {p.sinConservantes && ' · Sin conservantes'}
                  {p.nota && ` · ${p.nota}`}
                </>
              }
              fuente={p.fuente}
            />
          </dl>
        </li>
      ))}
    </ul>
  )
}

function Conservacion({ f }: { f: TFicha }) {
  if (f.conservacion.length === 0) return <p className="sin-datos">sin datos en las fuentes</p>
  return (
    <dl>
      {f.conservacion.map((c, i) => (
        <Dato
          key={i}
          etiqueta={
            c.presentaciones
              ? f.presentaciones.filter((p) => c.presentaciones?.includes(p.id)).map(describirPresentacion).join('; ')
              : 'Todas las presentaciones'
          }
          valor={`${c.texto}${c.validezAbiertoDias ? ` (validez abierto: ${c.validezAbiertoDias} días)` : ''}`}
          fuente={c.fuente}
        />
      ))}
    </dl>
  )
}

function Administracion({ f }: { f: TFicha }) {
  return (
    <>
      <dl>
        <Dato etiqueta="Cómo aplicar" valor={f.administracion?.texto} fuente={f.administracion?.fuente} />
        {f.componentes.length > 0 && <Dato etiqueta="Componentes" valor={f.componentes.join(' + ')} />}
      </dl>
      {f.contraindicaciones.length > 0 && (
        <>
          <h3>Contraindicaciones</h3>
          <ul className="alertas">
            {f.contraindicaciones.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
        </>
      )}
      {f.alertas.length > 0 && (
        <>
          <h3>Alertas</h3>
          <ul className="alertas">
            {f.alertas.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        </>
      )}
    </>
  )
}

function Fuentes({ f }: { f: TFicha }) {
  const usadas = new Set<string>()
  JSON.stringify(f, (k, v) => {
    if ((k === 'ref' || k === 'fuente') && typeof v === 'string') usadas.add(v)
    return v
  })
  return (
    <>
      <ul>
        {fuentesTopicos
          .filter((x) => usadas.has(x.id))
          .map((x) => (
            <li key={x.id}>
              <strong>{x.id}</strong>: <a href={x.url} target="_blank" rel="noreferrer">{x.titulo}</a> — {x.institucion} ({x.anio}), consultada el {x.consultado}.
            </li>
          ))}
      </ul>
      <p>Revisión clínica: {f.meta.revisadoPor ? `${f.meta.revisadoPor} (${f.meta.fechaRevision ?? 's/f'})` : 'pendiente'}.</p>
    </>
  )
}

export default function FichaTopica() {
  const { id = '' } = useParams()
  const f = obtenerTopico(id)
  const [activa, setActiva] = useState<Pestana>('Dosis')
  const [, refrescar] = useState(0)
  useEffect(() => {
    if (f) registrarRecienteTopico(f.id)
  }, [f])

  if (!f) return <p>Medicamento no encontrado</p>
  const favorito = esFavoritoTopico(f.id)
  const verificacion = verificacionDeTopico(f)

  return (
    <article className="ficha" data-color={colorGrupo(f.grupo)}>
      <p>
        <Link to="/topicos">← Tópicos</Link>
      </p>
      <header className="ficha-encabezado">
        <span className="chip-grupo">
          {etiquetaGrupo(f.grupo)} · {f.vias.map((v) => VIA[v]).join(', ')}
        </span>
        <h2>
          {f.nombre} {f.altoRiesgo && <span className="etiqueta alto-riesgo">Alto riesgo</span>}
        </h2>
        <button
          type="button"
          className="estrella"
          aria-label="Favorito"
          aria-pressed={favorito}
          title={favorito ? 'Quitar de favoritos' : 'Agregar a favoritos'}
          onClick={() => {
            alternarFavoritoTopico(f.id)
            refrescar((n) => n + 1)
          }}
        >
          {favorito ? '★' : '☆'}
        </button>
        {combinacionesCalculables(f).length > 0 && (
          <Link to={`/topicos/m/${f.id}/calcular`} className="boton">
            ¿Cuánto dura el frasco?
          </Link>
        )}
      </header>
      {verificacion === 'fuente_unica' && <AvisoFuenteUnica />}
      {verificacion === 'sin_pauta' && (
        <p role="note" className="aviso aviso-fuente-unica">
          {TEXTO_SIN_PAUTA}
        </p>
      )}
      <div role="tablist" aria-label="Secciones de la ficha" className="pestanas">
        {PESTANAS.map((p) => (
          <button key={p} role="tab" type="button" aria-selected={activa === p} aria-controls={`panel-${p}`} id={`tab-${p}`} onClick={() => setActiva(p)}>
            {p}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`panel-${activa}`} aria-labelledby={`tab-${activa}`}>
        {activa === 'Dosis' && <Dosis f={f} />}
        {activa === 'Presentaciones' && <Presentaciones f={f} />}
        {activa === 'Conservación' && <Conservacion f={f} />}
        {activa === 'Administración' && <Administracion f={f} />}
        {activa === 'Discrepancias' && <TablaDiscrepancias discrepancias={f.discrepancias} />}
        {activa === 'Fuentes' && <Fuentes f={f} />}
      </div>
    </article>
  )
}
