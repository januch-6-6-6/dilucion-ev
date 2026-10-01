import { useMemo, useState, type ReactNode } from 'react'
import { Link, useParams } from 'react-router-dom'
import { alertaConcentracion, alertaDosis, alertaTiempo, type Alerta } from '../../calculos/alertas'
import {
  concentracion,
  dosisAVelocidad,
  dosisPediatrica,
  velocidadADosis,
  velocidadPorDosis,
  velocidadPorTiempo,
  volumenACargar,
  type Resultado,
} from '../../calculos/calculadoras'
import { parsearNumero } from '../../calculos/numeros'
import { parsearUnidadDosis, type Cantidad, type UnidadMasa } from '../../calculos/unidades'
import { obtenerFicha } from '../../datos/cargar'
import type { Dosis, Ficha } from '../../esquema/ficha'

const MODOS = ['Concentración', 'Volumen a cargar', 'Velocidad por tiempo', 'Velocidad por dosis', 'Dosis → velocidad', 'Velocidad → dosis', 'Pediátrica'] as const
type Modo = (typeof MODOS)[number]
const UNIDADES: UnidadMasa[] = ['g', 'mg', 'mcg', 'UI']
const fmt = (n: number) => String(n).replace('.', ',')
const num = (t: string) => parsearNumero(t) ?? 0
const seguro = (f: () => Alerta[]): Alerta[] => {
  try {
    return f()
  } catch {
    return []
  }
}

function Campo({ etiqueta, valor, onCambio }: { etiqueta: string; valor: string; onCambio: (v: string) => void }) {
  return (
    <label className="campo">
      <span>{etiqueta}</span>
      <input inputMode="decimal" aria-label={etiqueta} value={valor} onChange={(e) => onCambio(e.target.value)} />
    </label>
  )
}

function SelectorUnidad({ etiqueta, valor, onCambio }: { etiqueta: string; valor: UnidadMasa; onCambio: (u: UnidadMasa) => void }) {
  return (
    <label className="campo">
      <span>{etiqueta}</span>
      <select aria-label={etiqueta} value={valor} onChange={(e) => onCambio(e.target.value as UnidadMasa)}>
        {UNIDADES.map((u) => (
          <option key={u}>{u}</option>
        ))}
      </select>
    </label>
  )
}

function Salida<T>({ r, texto, alertas = [], extra }: { r: Resultado<T>; texto: (v: T) => ReactNode; alertas?: Alerta[]; extra?: ReactNode }) {
  return (
    <div className="salida">
      <div role="status" className="resultado">
        {r.ok ? texto(r.valor) : <span className="falta">{r.error}</span>}
      </div>
      {r.ok && alertas.length > 0 && (
        <div role="alert" className="alerta-roja">
          {alertas.map((a) => (
            <p key={a.mensaje}>{a.mensaje}</p>
          ))}
        </div>
      )}
      {extra}
      {r.ok && (
        <ol className="pasos">
          {r.pasos.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ol>
      )}
    </div>
  )
}

/** Concentración por ml de una dilución estándar expresada en la unidad pedida. */
function concentracionEstandar(ficha: Ficha | undefined, indice: number, unidad: UnidadMasa): string {
  const e = ficha?.dilucion.estandar[indice]
  if (!e) return ''
  const r = concentracion(e.cantidad, e.volumenFinalMl, unidad)
  return r.ok ? fmt(r.valor) : ''
}

function SelectorDilucion({ ficha, indice, onCambio }: { ficha?: Ficha; indice: number; onCambio: (i: number) => void }) {
  if (!ficha || ficha.dilucion.estandar.length === 0) return null
  return (
    <label className="campo">
      <span>Dilución</span>
      <select aria-label="Dilución" value={indice} onChange={(e) => onCambio(Number(e.target.value))}>
        {ficha.dilucion.estandar.map((d, i) => (
          <option key={d.descripcion} value={i}>
            {d.descripcion}
          </option>
        ))}
      </select>
    </label>
  )
}

function ModoConcentracion({ ficha }: { ficha?: Ficha }) {
  const e = ficha?.dilucion.estandar[0]
  const [cant, setCant] = useState(e ? fmt(e.cantidad.valor) : '')
  const [unidad, setUnidad] = useState<UnidadMasa>(e?.cantidad.unidad ?? 'mg')
  const [vol, setVol] = useState(e ? fmt(e.volumenFinalMl) : '')
  const [salida, setSalida] = useState<UnidadMasa>(ficha?.dilucion.concentracionMax?.unidad ?? e?.cantidad.unidad ?? 'mg')
  const r = concentracion({ valor: num(cant), unidad }, num(vol), salida)
  const alertas = r.ok ? seguro(() => alertaConcentracion({ valor: r.valor, unidad: salida }, ficha?.dilucion.concentracionMax)) : []
  return (
    <>
      <Campo etiqueta="Cantidad de medicamento" valor={cant} onCambio={setCant} />
      <SelectorUnidad etiqueta="Unidad" valor={unidad} onCambio={setUnidad} />
      <Campo etiqueta="Volumen final (ml)" valor={vol} onCambio={setVol} />
      <SelectorUnidad etiqueta="Expresar en" valor={salida} onCambio={setSalida} />
      <Salida r={r} alertas={alertas} texto={(v) => `${fmt(v)} ${salida}/ml`} />
    </>
  )
}

function ModoVolumen({ ficha }: { ficha?: Ficha }) {
  const [iPres, setIPres] = useState(0)
  const pres = ficha?.presentaciones[iPres]
  const [presCant, setPresCant] = useState('')
  const [presVol, setPresVol] = useState('')
  const [dosis, setDosis] = useState('')
  const [unidad, setUnidad] = useState<UnidadMasa>(pres?.cantidad.unidad ?? 'mg')
  const presentacion = pres
    ? { cantidad: pres.cantidad, volumenMl: pres.volumenMl }
    : { cantidad: { valor: num(presCant), unidad }, volumenMl: num(presVol) }
  const r = volumenACargar({ valor: num(dosis), unidad }, presentacion)
  const forma = pres?.forma ?? 'unidad'
  return (
    <>
      {ficha ? (
        <label className="campo">
          <span>Presentación</span>
          <select aria-label="Presentación" value={iPres} onChange={(e) => setIPres(Number(e.target.value))}>
            {ficha.presentaciones.map((p, i) => (
              <option key={p.id} value={i}>
                {p.forma} {fmt(p.cantidad.valor)} {p.cantidad.unidad} / {fmt(p.volumenMl)} ml
              </option>
            ))}
          </select>
        </label>
      ) : (
        <>
          <Campo etiqueta="Cantidad por presentación" valor={presCant} onCambio={setPresCant} />
          <Campo etiqueta="Volumen de la presentación (ml)" valor={presVol} onCambio={setPresVol} />
        </>
      )}
      <Campo etiqueta="Dosis" valor={dosis} onCambio={setDosis} />
      <SelectorUnidad etiqueta="Unidad de la dosis" valor={unidad} onCambio={setUnidad} />
      <Salida r={r} texto={(v) => `${fmt(v.ml)} ml · ${v.unidades} ${forma}${v.unidades > 1 ? 's' : ''}`} />
    </>
  )
}

function ModoTiempo({ ficha }: { ficha?: Ficha }) {
  const [vol, setVol] = useState('')
  const [min, setMin] = useState('')
  const r = velocidadPorTiempo(num(vol), num(min))
  const alertas = alertaTiempo(num(min), ficha?.administracion.tiempoMinimoMin)
  return (
    <>
      <Campo etiqueta="Volumen (ml)" valor={vol} onCambio={setVol} />
      <Campo etiqueta="Tiempo (min)" valor={min} onCambio={setMin} />
      <Salida
        r={r}
        alertas={alertas}
        texto={(v) => `${fmt(v.mlh)} ml/h · macrogotero ${v.gotasMacro} gotas/min · microgotero ${v.gotasMicro} gotas/min`}
      />
    </>
  )
}

/** Campo de concentración con su propia unidad: cambiar la unidad de la dosis nunca la reetiqueta. */
function CampoConcentracion({ valor, unidad, onValor, onUnidad }: { valor: string; unidad: UnidadMasa; onValor: (v: string) => void; onUnidad: (u: UnidadMasa) => void }) {
  return (
    <>
      <Campo etiqueta="Concentración" valor={valor} onCambio={onValor} />
      <SelectorUnidad etiqueta="Unidad de concentración" valor={unidad} onCambio={onUnidad} />
      <p className="unidad">{unidad}/ml</p>
    </>
  )
}

const tiempoDe = (u: string) => parsearUnidadDosis(u)?.tiempo ?? null
const esTasaSinPeso = (d: Dosis) => { const u = parsearUnidadDosis(d.unidad); return Boolean(u && !u.porKg && u.tiempo) }
const esTasaPorPeso = (d: Dosis) => { const u = parsearUnidadDosis(d.unidad); return Boolean(u && u.porKg && u.tiempo) }

function ModoPorDosis({ ficha }: { ficha?: Ficha }) {
  const opciones = (ficha?.dosis ?? []).filter((d) => d.poblacion === 'adulto' && esTasaSinPeso(d))
  const [iOp, setIOp] = useState(0)
  const actual = opciones[iOp] as Dosis | undefined
  const [masaLibre, setMasaLibre] = useState<UnidadMasa>(ficha?.dilucion.estandar[0]?.cantidad.unidad ?? 'mg')
  const [tiempoLibre, setTiempoLibre] = useState<'min' | 'h'>('h')
  const masa = actual ? parsearUnidadDosis(actual.unidad)!.masa : masaLibre
  const tiempo = actual ? tiempoDe(actual.unidad)! : tiempoLibre
  const [iDil, setIDil] = useState(0)
  const [dosis, setDosis] = useState('')
  const [concUnidad, setConcUnidad] = useState<UnidadMasa>(masa)
  const [conc, setConc] = useState(concentracionEstandar(ficha, 0, masa))
  const factor = tiempo === 'min' ? 60 : 1
  const r = velocidadPorDosis({ valor: num(dosis) * factor, unidad: masa }, { valor: num(conc), unidad: concUnidad })
  const alertas = r.ok ? [...(actual ? alertaDosis(num(dosis), actual.unidad, actual) : []), ...seguro(() => alertaConcentracion({ valor: num(conc), unidad: concUnidad }, ficha?.dilucion.concentracionMax))] : []
  return (
    <>
      {opciones.length > 0 ? (
        <label className="campo">
          <span>Indicación</span>
          <select aria-label="Indicación" value={iOp} onChange={(e) => setIOp(Number(e.target.value))}>
            {opciones.map((d, i) => (
              <option key={d.indicacion} value={i}>{d.indicacion}</option>
            ))}
          </select>
        </label>
      ) : (
        <>
          <SelectorUnidad etiqueta="Unidad de la dosis" valor={masaLibre} onCambio={setMasaLibre} />
          <label className="campo">
            <span>Por</span>
            <select aria-label="Por" value={tiempoLibre} onChange={(e) => setTiempoLibre(e.target.value as 'min' | 'h')}>
              <option value="h">hora</option>
              <option value="min">minuto</option>
            </select>
          </label>
        </>
      )}
      <SelectorDilucion ficha={ficha} indice={iDil} onCambio={(i) => { setIDil(i); setConc(concentracionEstandar(ficha, i, concUnidad)) }} />
      <Campo etiqueta="Dosis" valor={dosis} onCambio={setDosis} />
      <p className="unidad">Unidad: {masa}/{tiempo}</p>
      <CampoConcentracion valor={conc} unidad={concUnidad} onValor={setConc} onUnidad={(u) => { setConcUnidad(u); setConc(concentracionEstandar(ficha, iDil, u)) }} />
      <Salida r={r} alertas={alertas} texto={(v) => `${fmt(v)} ml/h`} />
    </>
  )
}

const UNIDADES_LIBRES = ['mcg/kg/min', 'mcg/kg/h', 'mg/kg/min', 'mg/kg/h']

function ModoDosisVelocidad({ ficha, inverso = false, indicacionFija }: { ficha?: Ficha; inverso?: boolean; indicacionFija?: Dosis }) {
  const opciones = useMemo(() => (ficha?.dosis ?? []).filter((d) => d.poblacion === 'adulto' && esTasaPorPeso(d)), [ficha])
  const [iOp, setIOp] = useState(0)
  const actual = indicacionFija ?? (opciones[iOp] as Dosis | undefined)
  const [unidadLibre, setUnidadLibre] = useState(UNIDADES_LIBRES[0])
  const ud = parsearUnidadDosis(actual?.unidad ?? unidadLibre)!
  const tiempo = ud.tiempo ?? 'min'
  const [iDil, setIDil] = useState(0)
  const [peso, setPeso] = useState('')
  const [dosis, setDosis] = useState('')
  const [mlh, setMlh] = useState('')
  const [concUnidad, setConcUnidad] = useState<UnidadMasa>(ud.masa)
  const [conc, setConc] = useState(concentracionEstandar(ficha, 0, ud.masa))
  const concentracionPorMl: Cantidad = { valor: num(conc), unidad: concUnidad }
  const r = inverso
    ? velocidadADosis({ pesoKg: num(peso), mlh: num(mlh), concentracionPorMl, unidadSalida: ud.masa, tiempo })
    : dosisAVelocidad({ pesoKg: num(peso), dosis: { valor: num(dosis), unidad: ud.masa, tiempo }, concentracionPorMl })
  const dosisEvaluada = inverso ? (r.ok ? (r.valor as number) : 0) : num(dosis)
  const alertas = r.ok
    ? [...(actual ? alertaDosis(dosisEvaluada, actual.unidad, actual) : []), ...seguro(() => alertaConcentracion(concentracionPorMl, ficha?.dilucion.concentracionMax))]
    : []
  return (
    <>
      {!indicacionFija &&
        (opciones.length > 0 ? (
          <label className="campo">
            <span>Indicación</span>
            <select aria-label="Indicación" value={iOp} onChange={(e) => setIOp(Number(e.target.value))}>
              {opciones.map((d, i) => (
                <option key={d.indicacion} value={i}>{d.indicacion}</option>
              ))}
            </select>
          </label>
        ) : (
          <label className="campo">
            <span>Unidad de dosis</span>
            <select aria-label="Unidad de dosis" value={unidadLibre} onChange={(e) => setUnidadLibre(e.target.value)}>
              {UNIDADES_LIBRES.map((u) => (
                <option key={u}>{u}</option>
              ))}
            </select>
          </label>
        ))}
      <SelectorDilucion ficha={ficha} indice={iDil} onCambio={(i) => { setIDil(i); setConc(concentracionEstandar(ficha, i, concUnidad)) }} />
      <Campo etiqueta="Peso (kg)" valor={peso} onCambio={setPeso} />
      {inverso ? <Campo etiqueta="Velocidad (ml/h)" valor={mlh} onCambio={setMlh} /> : <Campo etiqueta="Dosis" valor={dosis} onCambio={setDosis} />}
      <p className="unidad">Unidad: {actual?.unidad ?? unidadLibre}</p>
      <CampoConcentracion valor={conc} unidad={concUnidad} onValor={setConc} onUnidad={(u) => { setConcUnidad(u); setConc(concentracionEstandar(ficha, iDil, u)) }} />
      <Salida r={r} alertas={alertas} texto={(v) => (inverso ? `${fmt(v as number)} ${ud.masa}/kg/${tiempo}` : `${fmt(v as number)} ml/h`)} />
    </>
  )
}

function ModoPediatrico({ ficha }: { ficha?: Ficha }) {
  const opciones = (ficha?.dosis ?? []).filter((d) => d.poblacion === 'pediatrico')
  const [i, setI] = useState(0)
  const [peso, setPeso] = useState('')
  const d = opciones[i] as Dosis | undefined
  const ud = d ? parsearUnidadDosis(d.unidad) : null
  const [porKg, setPorKg] = useState(d ? fmt(d.max ?? d.min ?? 0) : '')

  if (!ficha || ficha.sinDosisPediatrica || !d) {
    return <p className="sin-datos">sin dosis pediátrica en la fuente</p>
  }

  const selector = (
    <label className="campo">
      <span>Indicación</span>
      <select aria-label="Indicación" value={i} onChange={(e) => { const j = Number(e.target.value); setI(j); setPorKg(fmt(opciones[j].max ?? opciones[j].min ?? 0)) }}>
        {opciones.map((o, j) => (
          <option key={o.indicacion} value={j}>{o.indicacion}</option>
        ))}
      </select>
    </label>
  )
  if (ud?.porKg && ud.tiempo) return <>{selector}<ModoDosisVelocidad key={i} ficha={ficha} indicacionFija={d} /></>
  if (!ud?.porKg) return <>{selector}<p className="sin-datos">Esta dosis no se calcula por peso: {d.unidad}.</p></>

  const dosisPorKg: Cantidad = { valor: num(porKg), unidad: ud.masa }
  const r = dosisPediatrica({ pesoKg: num(peso), dosisPorKg, topeAdulto: d.topeAdulto ?? { valor: Number.MAX_SAFE_INTEGER, unidad: ud.masa } })
  const alertas: Alerta[] = r.ok
    ? [
        ...alertaDosis(num(porKg), d.unidad, d),
        ...(r.valor.limitada && d.topeAdulto ? [{ nivel: 'rojo' as const, mensaje: `Dosis limitada a la dosis tope (${fmt(d.topeAdulto.valor)} ${d.topeAdulto.unidad}).` }] : []),
      ]
    : []
  return (
    <>
      {selector}
      <Campo etiqueta="Peso (kg)" valor={peso} onCambio={setPeso} />
      <Campo etiqueta={`Dosis por kg (${ud.masa}/kg)`} valor={porKg} onCambio={setPorKg} />
      <Salida
        r={r}
        alertas={alertas}
        texto={(v) => `${fmt(v.dosis.valor)} ${v.dosis.unidad}`}
        extra={!d.topeAdulto && r.ok ? <p className="aviso">La fuente no indica dosis tope para esta indicación.</p> : null}
      />
    </>
  )
}

export function CalculadoraVista({ ficha }: { ficha?: Ficha }) {
  const [modo, setModo] = useState<Modo>(ficha?.dosis.some((d) => parsearUnidadDosis(d.unidad)?.tiempo) ? 'Dosis → velocidad' : 'Velocidad por tiempo')
  return (
    <section className="calculadora">
      <p>
        <Link to={ficha ? `/m/${ficha.id}` : '/'}>← {ficha ? ficha.nombre : 'Inicio'}</Link>
      </p>
      <h2>Calculadora{ficha ? `: ${ficha.nombre}` : ' libre'}</h2>
      <div role="tablist" aria-label="Tipo de cálculo" className="pestanas">
        {MODOS.map((m) => (
          <button key={m} role="tab" type="button" aria-selected={modo === m} onClick={() => setModo(m)}>
            {m}
          </button>
        ))}
      </div>
      <div role="tabpanel" key={modo}>
        {modo === 'Concentración' && <ModoConcentracion ficha={ficha} />}
        {modo === 'Volumen a cargar' && <ModoVolumen ficha={ficha} />}
        {modo === 'Velocidad por tiempo' && <ModoTiempo ficha={ficha} />}
        {modo === 'Velocidad por dosis' && <ModoPorDosis ficha={ficha} />}
        {modo === 'Dosis → velocidad' && <ModoDosisVelocidad ficha={ficha} />}
        {modo === 'Velocidad → dosis' && <ModoDosisVelocidad ficha={ficha} inverso />}
        {modo === 'Pediátrica' && <ModoPediatrico ficha={ficha} />}
      </div>
    </section>
  )
}

export default function Calculadora() {
  const { id } = useParams()
  const ficha = id ? obtenerFicha(id) : undefined
  if (id && !ficha) return <p>Medicamento no encontrado</p>
  return <CalculadoraVista ficha={ficha} />
}
