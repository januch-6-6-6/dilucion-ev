import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fuentes, obtenerFicha } from '../../datos/cargar'
import type { Ficha as TFicha } from '../../esquema/ficha'
import Dato from '../componentes/Dato'
import { colorGrupo } from '../colores'
import { etiquetaGrupo } from '../etiquetas'
import { registrarReciente } from '../recientes'

const PESTANAS = ['Preparar', 'Administrar', 'Compatibilidad', 'Seguridad', 'Fuentes'] as const
type Pestana = (typeof PESTANAS)[number]

const VIAS: Record<string, string> = { bolo: 'Bolo', infusion_intermitente: 'Infusión intermitente', infusion_continua: 'Infusión continua' }
const ESTADO: Record<string, string> = { compatible: 'Compatible', incompatible: 'Incompatible', sin_datos: 'Sin datos' }
const siNo = (v?: boolean) => (v === undefined ? undefined : v ? 'Sí' : 'No')
const fmt = (n: number) => String(n).replace('.', ',')

function Preparar({ f }: { f: TFicha }) {
  const { dilucion, estabilidad } = f
  return (
    <>
      <h3>Presentaciones</h3>
      <dl>
        {f.presentaciones.map((p) => (
          <Dato key={p.id} etiqueta={p.forma} valor={`${fmt(p.cantidad.valor)} ${p.cantidad.unidad} / ${fmt(p.volumenMl)} ml`} fuente={p.fuente} />
        ))}
      </dl>
      <h3>Reconstitución</h3>
      <dl>
        {f.reconstitucion ? (
          <Dato etiqueta="Diluyente" valor={`${f.reconstitucion.diluyente}, ${fmt(f.reconstitucion.volumenMl)} ml`} fuente={f.reconstitucion.fuente} />
        ) : (
          <Dato etiqueta="Reconstitución" valor="No requiere (viene en solución)" />
        )}
      </dl>
      <h3>Dilución</h3>
      <dl>
        <Dato etiqueta="Sueros" valor={dilucion.sueros.length ? dilucion.sueros.join(', ') : undefined} />
        <Dato etiqueta="Concentración mínima" valor={dilucion.concentracionMin?.valor} unidad={dilucion.concentracionMin && `${dilucion.concentracionMin.unidad}/ml`} fuente={dilucion.concentracionMin?.fuente} />
        <Dato etiqueta="Concentración máxima" valor={dilucion.concentracionMax?.valor} unidad={dilucion.concentracionMax && `${dilucion.concentracionMax.unidad}/ml`} fuente={dilucion.concentracionMax?.fuente} />
      </dl>
      {dilucion.estandar.length > 0 && (
        <ul className="diluciones">
          {dilucion.estandar.map((d) => (
            <li key={d.descripcion}>
              {d.descripcion} <cite title={d.fuente.detalle}>[{d.fuente.ref}]</cite>
            </li>
          ))}
        </ul>
      )}
      <h3>Estabilidad</h3>
      <dl>
        <Dato etiqueta="Temperatura ambiente" valor={estabilidad.ambienteH} unidad="h" fuente={estabilidad.fuente} />
        <Dato etiqueta="Refrigerado" valor={estabilidad.refrigeradoH} unidad="h" fuente={estabilidad.fuente} />
        <Dato etiqueta="Proteger de la luz" valor={siNo(estabilidad.protegerLuz)} fuente={estabilidad.fuente} />
      </dl>
    </>
  )
}

function Administrar({ f }: { f: TFicha }) {
  const a = f.administracion
  return (
    <>
      <dl>
        <Dato etiqueta="Vías" valor={a.vias.map((v) => VIAS[v]).join(', ')} fuente={a.fuente} />
        <Dato etiqueta="Indicaciones" valor={a.texto} fuente={a.fuente} />
        <Dato etiqueta="Tiempo mínimo de administración" valor={a.tiempoMinimoMin} unidad="min" fuente={a.fuente} />
        <Dato etiqueta="Requiere vía central" valor={siNo(a.requiereViaCentral)} />
        <Dato etiqueta="Requiere bomba" valor={siNo(a.requiereBomba)} />
      </dl>
      {(['adulto', 'pediatrico'] as const).map((pob) => {
        const dosis = f.dosis.filter((d) => d.poblacion === pob)
        return (
          <section key={pob}>
            <h3>{pob === 'adulto' ? 'Dosis adulto' : 'Dosis pediátrica'}</h3>
            {dosis.length === 0 ? (
              <p className="sin-datos">{pob === 'pediatrico' ? 'sin dosis pediátrica en la fuente' : 'sin datos en las fuentes'}</p>
            ) : (
              <dl>
                {dosis.map((d) => (
                  <Dato
                    key={d.indicacion}
                    etiqueta={d.indicacion}
                    valor={[d.min !== undefined && d.max !== undefined && d.min !== d.max ? `${fmt(d.min)}–${fmt(d.max)}` : fmt(d.max ?? d.min ?? NaN), d.unidad].join(' ') +
                      (d.maximaAbsoluta ? ` (máximo ${fmt(d.maximaAbsoluta)})` : '') +
                      (d.topeAdulto ? ` (tope ${fmt(d.topeAdulto.valor)} ${d.topeAdulto.unidad})` : '')}
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

function Compatibilidad({ f }: { f: TFicha }) {
  if (f.compatibilidad.length === 0) return <p className="sin-datos">sin datos en las fuentes</p>
  return (
    <table className="compatibilidad">
      <thead>
        <tr>
          <th>Con</th>
          <th>Estado</th>
          <th>Fuente</th>
        </tr>
      </thead>
      <tbody>
        {f.compatibilidad.map((c) => (
          <tr key={c.con} className={`estado-${c.estado}`}>
            <td>{obtenerFicha(c.con)?.nombre ?? c.con}</td>
            <td>
              <span className={`pildora pildora-${c.estado}`}>{ESTADO[c.estado]}</span>
            </td>
            <td>
              <cite title={c.fuente.detalle}>{c.fuente.ref}</cite>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

function Seguridad({ f }: { f: TFicha }) {
  const e = f.efectosAdversos
  const lista = (titulo: string, items: string[]) => (
    <>
      <h3>{titulo}</h3>
      {items.length ? <ul>{items.map((i) => <li key={i}>{i}</li>)}</ul> : <p className="sin-datos">sin datos en las fuentes</p>}
    </>
  )
  return (
    <>
      {f.alertas.length > 0 && (
        <ul className="alertas">
          {f.alertas.map((a) => (
            <li key={a}>{a}</li>
          ))}
        </ul>
      )}
      <h3>Interacciones graves</h3>
      {f.interaccionesGraves.length ? (
        <ul>
          {f.interaccionesGraves.map((i) => (
            <li key={i.con}>
              <strong>{i.con}:</strong> {i.efecto} <cite title={i.fuente.detalle}>[{i.fuente.ref}]</cite>
            </li>
          ))}
        </ul>
      ) : (
        <p className="sin-datos">sin datos en las fuentes</p>
      )}
      {lista('Efectos adversos frecuentes', e.frecuentes)}
      {lista('Efectos adversos graves', e.graves)}
      {lista('Qué vigilar', e.vigilar)}
      <p>
        <cite title={e.fuente.detalle}>Fuente: {e.fuente.ref}</cite>
      </p>
    </>
  )
}

function Fuentes({ f }: { f: TFicha }) {
  const usadas = new Set<string>()
  JSON.stringify(f, (k, v) => {
    if (k === 'ref' && typeof v === 'string') usadas.add(v)
    return v
  })
  return (
    <>
      <ul>
        {fuentes
          .filter((x) => usadas.has(x.id))
          .map((x) => (
            <li key={x.id}>
              <strong>{x.id}</strong>: <a href={x.url} target="_blank" rel="noreferrer">{x.titulo}</a> — {x.institucion} ({x.anio}), consultada el {x.consultado}.
            </li>
          ))}
      </ul>
      <h3>Discrepancias</h3>
      {f.meta.discrepancias.length ? (
        <ul>
          {f.meta.discrepancias.map((d) => (
            <li key={d.campo}>
              <strong>{d.campo}:</strong> {d.valores.join(' / ')}. <em>Decisión:</em> {d.decision}
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay discrepancias registradas.</p>
      )}
      <p>
        Revisión clínica: {f.meta.revisadoPor ? `${f.meta.revisadoPor} (${f.meta.fechaRevision ?? 's/f'})` : 'pendiente'}.
      </p>
    </>
  )
}

export default function Ficha() {
  const { id = '' } = useParams()
  const f = obtenerFicha(id)
  const [activa, setActiva] = useState<Pestana>('Preparar')
  useEffect(() => {
    if (f) registrarReciente(f.id)
  }, [f])

  if (!f) return <p>Medicamento no encontrado</p>

  return (
    <article className="ficha" data-color={colorGrupo(f.grupo)}>
      <p>
        <Link to="/">← Inicio</Link>
      </p>
      <header className="ficha-encabezado">
        <span className="chip-grupo">{etiquetaGrupo(f.grupo)}</span>
        <h2>
          {f.nombre} {f.altoRiesgo && <span className="etiqueta alto-riesgo">Alto riesgo</span>}
        </h2>
        <Link to={`/m/${f.id}/calcular`} className="boton">
          Calcular
        </Link>
      </header>
      <div role="tablist" aria-label="Secciones de la ficha" className="pestanas">
        {PESTANAS.map((p) => (
          <button key={p} role="tab" type="button" aria-selected={activa === p} aria-controls={`panel-${p}`} id={`tab-${p}`} onClick={() => setActiva(p)}>
            {p}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`panel-${activa}`} aria-labelledby={`tab-${activa}`}>
        {activa === 'Preparar' && <Preparar f={f} />}
        {activa === 'Administrar' && <Administrar f={f} />}
        {activa === 'Compatibilidad' && <Compatibilidad f={f} />}
        {activa === 'Seguridad' && <Seguridad f={f} />}
        {activa === 'Fuentes' && <Fuentes f={f} />}
      </div>
    </article>
  )
}
