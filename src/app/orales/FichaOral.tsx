import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fuentesOrales, obtenerOral, verificacion } from '../../datos/cargarOrales'
import { describirPresentacion } from '../../calculos/oral'
import type { DosisOral, FichaOral as TFichaOral, PresentacionOral } from '../../esquema/ficha-oral'
import Dato from '../componentes/Dato'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import AvisoFuenteUnica from './AvisoFuenteUnica'
import { alternarFavoritoOral, esFavoritoOral, registrarRecienteOral } from './guardadoOrales'
import TablaDiscrepancias from './TablaDiscrepancias'

const PESTANAS = ['Dosis', 'Presentaciones', 'Administración', 'Discrepancias', 'Fuentes'] as const
type Pestana = (typeof PESTANAS)[number]

const REGISTRO = { verificado: 'Verificado', sin_verificar: 'Sin verificar', no_registrado: 'No registrado' } as const
const PARTIBLE = { no: 'No partible', mitades: 'Partible en mitades', cuartos: 'Partible en cuartos' } as const
const COMIDA = { ayunas: 'En ayunas', con_comida: 'Con comida', indiferente: 'Indiferente', antes: 'Antes de comer', despues: 'Después de comer' } as const
const fmt = (n: number) => String(n).replace('.', ',')

function textoDosis(d: DosisOral, presentaciones: PresentacionOral[]): string {
  const rango = d.min !== undefined && d.max !== undefined && d.min !== d.max ? `${fmt(d.min)}–${fmt(d.max)}` : fmt((d.max ?? d.min) as number)
  const partes = d.min === undefined && d.max === undefined ? [d.texto ?? ''] : [`${rango} ${d.unidad}`, d.texto ?? '']
  if (d.base) partes.push(d.base === 'toma' ? 'por toma' : 'por día')
  if (d.tomasPorDia) partes.push(`${fmt(d.tomasPorDia)} veces al día`)
  if (d.intervaloH) partes.push(`cada ${fmt(d.intervaloH)} h`)
  if (d.topePorToma) partes.push(`tope por toma ${fmt(d.topePorToma.valor)} ${d.topePorToma.unidad}`)
  if (d.topeDiario) partes.push(`tope diario ${fmt(d.topeDiario.valor)} ${d.topeDiario.unidad}`)
  if (d.condicion) partes.push(d.condicion)
  if (d.presentaciones) {
    const solo = presentaciones.filter((p) => d.presentaciones?.includes(p.id)).map(describirPresentacion)
    if (solo.length === 0) partes.push('Sin presentación válida en la ficha')
    else partes.push(`Solo con ${solo.length === 1 ? 'la presentación' : 'estas presentaciones'}: ${solo.join('; ')}`)
  }
  return partes.filter(Boolean).join(', ')
}

function Dosis({ f }: { f: TFichaOral }) {
  return (
    <>
      {/* DosisOral.poblacion es un enum cerrado (adulto | pediatrico): si se amplía, hay que actualizar este render. */}
      {(['adulto', 'pediatrico'] as const).map((pob) => {
        const dosis = f.dosis.filter((d) => d.poblacion === pob)
        return (
          <section key={pob}>
            <h3>{pob === 'adulto' ? 'Dosis adulto' : 'Dosis pediátrica'}</h3>
            {dosis.length === 0 ? (
              <p className="sin-datos">
                {pob === 'pediatrico' && f.pediatria.estado === 'solo_adulto' ? `Solo adulto: ${f.pediatria.motivo}` : 'sin datos en las fuentes'}
              </p>
            ) : (
              <dl>
                {dosis.map((d, i) => (
                  <Dato
                    key={`${d.indicacion}-${i}`}
                    etiqueta={d.indicacion}
                    valor={
                      <>
                        {textoDosis(d, f.presentaciones)}{' '}
                        <span className={`etiqueta ${d.estatus === 'autorizada' ? 'autorizada' : 'off-label'}`}>
                          {d.estatus === 'autorizada' ? 'Autorizada' : 'Off-label'}
                        </span>
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

function descripcionPresentacion(p: PresentacionOral): string {
  const base = p.cantidad ? `${fmt(p.cantidad.valor)} ${p.cantidad.unidad} por unidad` : p.concentracion ? `${fmt(p.concentracion.valor)} ${p.concentracion.unidad} por ml` : ''
  const forma = p.forma.replace(/_/g, ' ')
  return `${forma.charAt(0).toUpperCase()}${forma.slice(1)} ${base}`.trim()
}

function Presentaciones({ f }: { f: TFichaOral }) {
  return (
    <ul className="presentaciones">
      {f.presentaciones.map((p) => (
        <li key={p.id}>
          <dl>
            <Dato
              etiqueta={descripcionPresentacion(p)}
              valor={
                <>
                  {PARTIBLE[p.partible]}
                  {p.liberacionProlongada && <span className="etiqueta"> Liberación prolongada</span>}
                  {p.gotasPorMl !== undefined && ` · ${fmt(p.gotasPorMl)} gotas/ml`}
                  {p.elemental && ` · equivale a ${fmt(p.elemental.valor)} ${p.elemental.unidad} de ${p.elemental.de}`}
                </>
              }
              fuente={p.fuente}
            />
            <Dato etiqueta="Registro en Chile" valor={REGISTRO[p.registroChile]} />
          </dl>
        </li>
      ))}
    </ul>
  )
}

function Administracion({ f }: { f: TFichaOral }) {
  const a = f.administracion
  const r = f.ajusteRenalHepatico
  return (
    <>
      <dl>
        <Dato etiqueta="Con las comidas" valor={COMIDA[a.comida]} fuente={a.fuente} />
        <Dato etiqueta="Indicaciones" valor={a.texto} fuente={a.fuente} />
        {a.noTriturar && <Dato etiqueta="No triturar" valor="Sí" fuente={a.fuente} />}
        <Dato etiqueta="Ajuste renal" valor={r?.renal} fuente={r?.fuente} />
        <Dato etiqueta="Ajuste hepático" valor={r?.hepatico} fuente={r?.fuente} />
      </dl>
      {f.alertas.length > 0 && (
        <ul className="alertas">
          {f.alertas.map((al) => (
            <li key={al}>{al}</li>
          ))}
        </ul>
      )}
    </>
  )
}

function Fuentes({ f }: { f: TFichaOral }) {
  const usadas = new Set<string>()
  JSON.stringify(f, (k, v) => {
    if (k === 'ref' && typeof v === 'string') usadas.add(v)
    return v
  })
  return (
    <>
      <ul>
        {fuentesOrales
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

export default function FichaOral() {
  const { id = '' } = useParams()
  const f = obtenerOral(id)
  const [activa, setActiva] = useState<Pestana>('Dosis')
  const [, refrescar] = useState(0)
  useEffect(() => {
    if (f) registrarRecienteOral(f.id)
  }, [f])

  if (!f) return <p>Medicamento no encontrado</p>
  const favorito = esFavoritoOral(f.id)

  return (
    <article className="ficha" data-color={colorGrupo(f.grupo)}>
      <p>
        <Link to="/orales">← Orales</Link>
      </p>
      <header className="ficha-encabezado">
        <span className="chip-grupo">{etiquetaGrupo(f.grupo)}</span>
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
            alternarFavoritoOral(f.id)
            refrescar((n) => n + 1)
          }}
        >
          {favorito ? '★' : '☆'}
        </button>
        {f.pediatria.estado === 'con_dosis' && (
          <Link to={`/orales/m/${f.id}/calcular`} className="boton">
            Calculadora
          </Link>
        )}
      </header>
      {verificacion(f) === 'fuente_unica' && <AvisoFuenteUnica />}
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
        {activa === 'Administración' && <Administracion f={f} />}
        {activa === 'Discrepancias' && <TablaDiscrepancias discrepancias={f.discrepancias} />}
        {activa === 'Fuentes' && <Fuentes f={f} />}
      </div>
    </article>
  )
}
