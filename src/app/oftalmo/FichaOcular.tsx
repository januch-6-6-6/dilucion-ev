import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { tieneVerificador } from '../../calculos/verificadorOcular'
import { fuentesOculares, obtenerOcular, verificacionDeOcular } from '../../datos/cargarOculares'
import type { DosisOcular, FichaOcular as TFicha } from '../../esquema/ficha-ocular'
import Dato from '../componentes/Dato'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import AvisoFuenteUnica from '../orales/AvisoFuenteUnica'
import TablaDiscrepancias from '../orales/TablaDiscrepancias'
import { alternarFavoritoOcular, esFavoritoOcular, registrarRecienteOcular } from './guardadoOculares'
import {
  AVISO_CIRUJANO,
  AVISO_FORMACION,
  AVISO_NO_REGISTRADO,
  AVISO_PABELLON,
  AVISO_SIN_PASOS,
  FAMILIA,
  PEDIATRIA,
  TEXTO_INFORMATIVA,
  TEXTO_SIN_PAUTA,
  VIA_OCULAR,
  describirPresentacion,
  finalTexto,
  pasoTexto,
} from './textos'

const PESTANAS = ['Dosis', 'Preparación', 'Conservación', 'Alertas', 'Discrepancias', 'Fuentes'] as const
type Pestana = (typeof PESTANAS)[number]

/** La ficha es de preparación pero la fuente no trae pasos y la presentación no viene lista para usar. */
const sinPasos = (f: TFicha): boolean =>
  f.modo === 'intraocular' && !f.sinPauta && f.protocolos.length === 0 && !f.presentaciones.every((p) => p.usoDirecto)

function textoDosis(d: DosisOcular, f: TFicha): string {
  const partes = [d.texto]
  if (d.final) partes.push(`Concentración de referencia: ${finalTexto(d.final)}`)
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
      {f.modo === 'informativa' && (
        <p role="note" className="aviso">
          {TEXTO_INFORMATIVA}
        </p>
      )}
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
                    key={`${d.indicacion}-${d.via}-${i}`}
                    etiqueta={`${d.indicacion} · ${VIA_OCULAR[d.via]}`}
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
      {f.alertas.length > 0 && <p className="sin-datos">Revisa la pestaña Alertas ({f.alertas.length}) antes de preparar.</p>}
    </>
  )
}

function Preparacion({ f }: { f: TFicha }) {
  return (
    <>
      <h3>Presentaciones</h3>
      <ul className="presentaciones">
        {f.presentaciones.map((p) => (
          <li key={p.id}>
            <dl>
              <Dato
                etiqueta={describirPresentacion(p)}
                valor={
                  <>
                    {p.registrosIsp.length > 0 ? `Registro ISP: ${p.registrosIsp.join(', ')}` : 'Sin registro ISP'}
                    {p.usoDirecto && ' · Viene lista para usar (no se prepara)'}
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
      <h3>Protocolos de preparación</h3>
      {f.protocolos.length === 0 ? (
        <p className="sin-datos">
          {f.modo === 'informativa'
            ? 'Ficha informativa: no hay protocolo de preparación.'
            : f.presentaciones.every((p) => p.usoDirecto)
              ? 'La presentación viene lista para usar: no hay pasos de preparación.'
              : 'Sin pasos de preparación publicados en las fuentes.'}
        </p>
      ) : (
        f.protocolos.map((p) => (
          <section key={p.id} className="protocolo">
            <h4>{p.titulo}</h4>
            <p>
              Parte de: {describirPresentacion(f.presentaciones.find((x) => x.id === p.partida) ?? f.presentaciones[0])}
            </p>
            <ol>
              {p.pasos.map((paso, i) => (
                <li key={i}>{pasoTexto(paso)}</li>
              ))}
            </ol>
            <p>
              Resultado: {finalTexto({ cantidad: { valor: p.resultado.valor, unidad: p.resultado.unidad }, volumenMl: p.resultado.volumenMl })}{' '}
              <cite className="fuente" title={p.fuente.detalle}>[{p.fuente.ref}]</cite>
            </p>
          </section>
        ))
      )}
    </>
  )
}

function Conservacion({ f }: { f: TFicha }) {
  if (f.conservacion.length === 0) return <p className="sin-datos">sin datos en las fuentes</p>
  return (
    <dl>
      {f.conservacion.map((c, i) => (
        <Dato key={i} etiqueta="Conservación" valor={`${c.texto}${c.horas ? ` (validez: ${String(c.horas).replace('.', ',')} h)` : ''}`} fuente={c.fuente} />
      ))}
    </dl>
  )
}

function Alertas({ f }: { f: TFicha }) {
  return (
    <>
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
      <h3>Alertas</h3>
      {f.alertas.length === 0 ? (
        <p className="sin-datos">sin datos en las fuentes</p>
      ) : (
        <ul className="alertas">
          {f.alertas.map((a) => (
            <li key={a}>{a}</li>
          ))}
        </ul>
      )}
      {f.componentes.length > 0 && (
        <dl>
          <Dato etiqueta="Componentes" valor={f.componentes.join(' + ')} />
        </dl>
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
        {fuentesOculares
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

export default function FichaOcular() {
  const { id = '' } = useParams()
  const f = obtenerOcular(id)
  const [activa, setActiva] = useState<Pestana>('Dosis')
  const [, refrescar] = useState(0)
  useEffect(() => {
    if (f) registrarRecienteOcular(f.id)
  }, [f])

  if (!f) return <p>Medicamento no encontrado</p>
  const favorito = esFavoritoOcular(f.id)
  const verificacion = verificacionDeOcular(f)

  return (
    <article className="ficha" data-color={colorGrupo(f.grupo)}>
      <p>
        <Link to="/oftalmologia">← Oftalmología</Link>
      </p>
      <header className="ficha-encabezado">
        <span className="chip-grupo">
          {etiquetaGrupo(f.grupo)} · {f.familias.map((x) => FAMILIA[x]).join(', ')}
        </span>
        <h2>
          {f.nombre} <span className="etiqueta alto-riesgo">Alto riesgo</span>
        </h2>
        <button
          type="button"
          className="estrella"
          aria-label="Favorito"
          aria-pressed={favorito}
          title={favorito ? 'Quitar de favoritos' : 'Agregar a favoritos'}
          onClick={() => {
            alternarFavoritoOcular(f.id)
            refrescar((n) => n + 1)
          }}
        >
          {favorito ? '★' : '☆'}
        </button>
        {tieneVerificador(f) && (
          <Link to={`/oftalmologia/m/${f.id}/verificar`} className="boton">
            Verificar mi preparación
          </Link>
        )}
      </header>
      <p role="note" className="aviso">
        {AVISO_FORMACION}
      </p>
      <p role="note" className="aviso">
        {AVISO_PABELLON}
      </p>
      {f.registroChile === 'no_registrado' && (
        <p role="note" className="aviso">
          {AVISO_NO_REGISTRADO}
        </p>
      )}
      {sinPasos(f) && (
        <p role="note" className="aviso">
          {AVISO_SIN_PASOS}
        </p>
      )}
      {f.familias.includes('antifibrotico') && (
        <p role="note" className="aviso">
          {AVISO_CIRUJANO}
        </p>
      )}
      {verificacion === 'fuente_unica' && <AvisoFuenteUnica />}
      {verificacion === 'sin_pauta' && (
        <p role="note" className="aviso aviso-fuente-unica">
          {TEXTO_SIN_PAUTA}
        </p>
      )}
      <div role="tablist" aria-label="Secciones de la ficha" className="pestanas">
        {PESTANAS.map((p) => (
          <button key={p} role="tab" type="button" aria-selected={activa === p} aria-controls={activa === p ? `panel-${p}` : undefined} id={`tab-${p}`} onClick={() => setActiva(p)}>
            {p}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`panel-${activa}`} aria-labelledby={`tab-${activa}`}>
        {activa === 'Dosis' && <Dosis f={f} />}
        {activa === 'Preparación' && <Preparacion f={f} />}
        {activa === 'Conservación' && <Conservacion f={f} />}
        {activa === 'Alertas' && <Alertas f={f} />}
        {activa === 'Discrepancias' && <TablaDiscrepancias discrepancias={f.discrepancias} />}
        {activa === 'Fuentes' && <Fuentes f={f} />}
      </div>
    </article>
  )
}
