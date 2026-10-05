import { useState, type ReactNode } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { Resultado } from '../../calculos/calculadoras'
import { masaAMl, mlAMasa } from '../../calculos/oralConversion'
import { calcularFija, calcularPorPeso, type ResultadoOral } from '../../calculos/oral'
import { parsearNumero } from '../../calculos/numeros'
import { convertirMasa, type Cantidad } from '../../calculos/unidades'
import { obtenerOral } from '../../datos/cargarOrales'
import type { DosisOral, FichaOral, PresentacionOral } from '../../esquema/ficha-oral'
import { AVISO } from '../aviso'
import Campo from '../componentes/Campo'

const MODOS = ['Por peso', 'Dosis fija', 'mg ↔ ml'] as const
type Modo = (typeof MODOS)[number]

const fmt = (n: number) => String(n).replace('.', ',')
const FRACCIONES: Record<number, string> = { 0.25: '¼', 0.5: '½', 0.75: '¾' }
const esLiquida = (p: PresentacionOral) => p.forma === 'jarabe' || p.forma === 'suspension' || p.forma === 'gotas'

function textoUnidades(n: number): string {
  const entero = Math.floor(n)
  const frac = FRACCIONES[Math.round((n - entero) * 100) / 100]
  if (!frac) return fmt(n)
  return entero === 0 ? frac : `${entero} ${frac}`
}

function etiquetaPresentacion(p: PresentacionOral): string {
  const base = p.concentracion ? `${fmt(p.concentracion.valor)} ${p.concentracion.unidad}/ml` : p.cantidad ? `${fmt(p.cantidad.valor)} ${p.cantidad.unidad}` : ''
  return `${p.forma} ${base}`.trim()
}

/** Tope de adulto de la ficha: el más bajo entre las dosis de adulto (nunca se supera). */
function topeAdultoDe(ficha: FichaOral) {
  const menor = (xs: Cantidad[]): Cantidad | undefined => {
    let mejor: Cantidad | undefined
    for (const c of xs) {
      if (!mejor) {
        mejor = c
        continue
      }
      try {
        if (convertirMasa(c.valor, c.unidad, mejor.unidad) < mejor.valor) mejor = c
      } catch {
        // unidad no comparable con la de referencia: se omite ese tope
      }
    }
    return mejor
  }
  const adultos = ficha.dosis.filter((d) => d.poblacion === 'adulto')
  const porToma = menor(adultos.flatMap((d) => (d.topePorToma ? [d.topePorToma] : [])))
  const diario = menor(adultos.flatMap((d) => (d.topeDiario ? [d.topeDiario] : [])))
  return porToma || diario ? { porToma, diario } : undefined
}

function sugerenciaLiquida(ficha: FichaOral, actual: PresentacionOral): string | undefined {
  if (esLiquida(actual)) return undefined
  const l = ficha.presentaciones.find(esLiquida)
  return l ? `Prueba con la presentación líquida (${l.forma}) de esta ficha` : undefined
}

/** Presentación elegida; si es líquida, su concentración es editable y obligatoria. */
function usePresentacion(ficha: FichaOral) {
  const [indice, setIndice] = useState(0)
  const base = ficha.presentaciones[indice]
  const [conc, setConc] = useState(base.concentracion ? fmt(base.concentracion.valor) : '')
  const liquida = esLiquida(base)
  const unidadConc = base.concentracion?.unidad ?? 'mg'
  const valorConc = parsearNumero(conc)
  const faltaConcentracion = liquida && valorConc === null
  const presentacion: PresentacionOral =
    liquida && valorConc !== null ? { ...base, concentracion: { valor: valorConc, unidad: unidadConc } } : base

  const elegir = (id: string) => {
    const i = ficha.presentaciones.findIndex((p) => p.id === id)
    const p = ficha.presentaciones[i]
    setIndice(i)
    setConc(p.concentracion ? fmt(p.concentracion.valor) : '')
  }
  const controles: ReactNode = (
    <>
      <label className="campo">
        <span>Presentación</span>
        <select aria-label="Presentación" value={base.id} onChange={(e) => elegir(e.target.value)}>
          {ficha.presentaciones.map((p) => (
            <option key={p.id} value={p.id}>
              {etiquetaPresentacion(p)}
            </option>
          ))}
        </select>
      </label>
      {liquida && <Campo etiqueta={`Concentración del frasco (${unidadConc}/ml)`} valor={conc} onCambio={setConc} />}
    </>
  )
  return { presentacion, faltaConcentracion, controles }
}

function Salida({ r, fuente, sugerencia }: { r: Resultado<ResultadoOral>; fuente?: DosisOral['fuente']; sugerencia?: string }) {
  return (
    <div className="salida">
      <div role="status" className="resultado">
        {r.ok ? <Bloque r={r} fuente={fuente} /> : <span className="falta">{r.error}</span>}
      </div>
      {!r.ok && sugerencia && <p className="aviso">{sugerencia}</p>}
    </div>
  )
}

function Bloque({ r, fuente }: { r: Extract<Resultado<ResultadoOral>, { ok: true }>; fuente?: DosisOral['fuente'] }) {
  const v = r.valor
  const s = v.salida
  return (
    <div data-testid="resultado">
      <p>
        Dosis por toma: <strong>{fmt(v.mgPorToma.valor)} {v.mgPorToma.unidad}</strong>
      </p>
      <p>
        {s.tipo === 'ml' && <strong>{fmt(s.ml)} ml</strong>}
        {s.tipo === 'gotas' && <strong>{fmt(s.gotas)} gotas</strong>}
        {s.tipo === 'unidades' && (
          <>
            <strong>{textoUnidades(s.unidades)} unidad(es)</strong> (entrega {fmt(s.entregado.valor)} {s.entregado.unidad})
          </>
        )}
      </p>
      <p>Tomas por día: {v.tomasPorDia === null ? 'no indicadas' : fmt(v.tomasPorDia)}</p>
      <p>Total diario: {v.totalDiario === null ? 'no calculable' : `${fmt(v.totalDiario.valor)} ${v.totalDiario.unidad}`}</p>
      {v.limitadaPor.length > 0 && <p className="aviso">Limitada por: {v.limitadaPor.join(', ')}</p>}
      {v.alertas.length > 0 && (
        <div role="alert" className="alerta-roja">
          {v.alertas.map((a) => (
            <p key={a.mensaje}>{a.mensaje}</p>
          ))}
        </div>
      )}
      <ol className="pasos">
        {r.pasos.map((p) => (
          <li key={p}>{p}</li>
        ))}
      </ol>
      {fuente && (
        <cite className="fuente">
          Fuente de la dosis [{fuente.ref}] {fuente.detalle}
        </cite>
      )}
    </div>
  )
}

function etiquetaDosis(d: DosisOral): string {
  if (d.min === undefined && d.max === undefined) return `${d.indicacion} (${d.texto ?? 'sin cantidad numérica'})`
  const cant = d.max !== undefined && d.min !== undefined && d.min !== d.max ? `${fmt(d.min)}–${fmt(d.max)}` : fmt((d.max ?? d.min) as number)
  return `${d.indicacion} (${cant} ${d.unidad})`
}

function SelectorDosis({ opciones, indice, onCambio }: { opciones: DosisOral[]; indice: number; onCambio: (i: number) => void }) {
  return (
    <label className="campo">
      <span>Dosis</span>
      <select aria-label="Dosis" value={indice} onChange={(e) => onCambio(Number(e.target.value))}>
        {opciones.map((d, i) => (
          <option key={i} value={i}>
            {etiquetaDosis(d)}
          </option>
        ))}
      </select>
    </label>
  )
}

function ModoPorPeso({ ficha }: { ficha: FichaOral }) {
  const opciones = ficha.dosis.filter((d) => d.poblacion === 'pediatrico')
  const [iDosis, setIDosis] = useState(0)
  const [peso, setPeso] = useState('')
  const { presentacion, faltaConcentracion, controles } = usePresentacion(ficha)
  const dosis = opciones[iDosis]
  const pesoKg = parsearNumero(peso)
  let r: Resultado<ResultadoOral>
  if (!dosis) r = { ok: false, error: 'Sin dosis pediátrica en la fuente' }
  else if (pesoKg === null) r = { ok: false, error: 'Falta el peso' }
  else if (faltaConcentracion) r = { ok: false, error: 'Falta la concentración' }
  else r = calcularPorPeso({ pesoKg, dosis, presentacion, topeAdulto: topeAdultoDe(ficha) })
  const falloCalculo = dosis !== undefined && pesoKg !== null && !faltaConcentracion
  return (
    <>
      <Campo etiqueta="Peso (kg)" valor={peso} onCambio={setPeso} />
      {opciones.length > 0 && <SelectorDosis opciones={opciones} indice={iDosis} onCambio={setIDosis} />}
      {controles}
      <Salida r={r} fuente={dosis?.fuente} sugerencia={falloCalculo ? sugerenciaLiquida(ficha, presentacion) : undefined} />
    </>
  )
}

function ModoFija({ ficha }: { ficha: FichaOral }) {
  const opciones = ficha.dosis.filter((d) => d.poblacion === 'adulto')
  const [iDosis, setIDosis] = useState(0)
  const { presentacion, faltaConcentracion, controles } = usePresentacion(ficha)
  const dosis = opciones[iDosis]
  let r: Resultado<ResultadoOral>
  if (!dosis) r = { ok: false, error: 'Sin dosis de adulto en la fuente' }
  else if (faltaConcentracion) r = { ok: false, error: 'Falta la concentración' }
  else r = calcularFija({ dosis, presentacion })
  const falloCalculo = dosis !== undefined && !faltaConcentracion
  return (
    <>
      {opciones.length > 0 && <SelectorDosis opciones={opciones} indice={iDosis} onCambio={setIDosis} />}
      {controles}
      <Salida r={r} fuente={dosis?.fuente} sugerencia={falloCalculo ? sugerenciaLiquida(ficha, presentacion) : undefined} />
    </>
  )
}

function ModoConversion({ ficha }: { ficha: FichaOral }) {
  const liquidas = ficha.presentaciones.filter(esLiquida)
  const [origen, setOrigen] = useState<'masa' | 'ml'>('masa')
  const [masa, setMasa] = useState('')
  const [ml, setMl] = useState('')
  const [id, setId] = useState(liquidas[0]?.id ?? '')
  const base = liquidas.find((p) => p.id === id)
  const [conc, setConc] = useState(base?.concentracion ? fmt(base.concentracion.valor) : '')
  if (!base?.concentracion) return <p className="sin-datos">Este medicamento no tiene presentación líquida para convertir.</p>
  const unidad = base.concentracion.unidad
  const valorConc = parsearNumero(conc)
  const presentacion: PresentacionOral = { ...base, concentracion: { valor: valorConc ?? 0, unidad } }
  const cambiar = (nuevo: string) => {
    const p = liquidas.find((x) => x.id === nuevo)
    setId(nuevo)
    setConc(p?.concentracion ? fmt(p.concentracion.valor) : '')
  }
  let texto: ReactNode
  let error: string | null = null
  if (valorConc === null) error = 'Falta la concentración'
  else if (origen === 'masa') {
    const m = parsearNumero(masa)
    if (m === null) error = 'Falta la dosis'
    else {
      const r = masaAMl({ valor: m, unidad }, presentacion)
      if (r.ok) texto = <>{fmt(m)} {unidad} = <strong>{fmt(r.valor)} ml</strong></>
      else error = r.error
    }
  } else {
    const v = parsearNumero(ml)
    if (v === null) error = 'Falta el volumen'
    else {
      const r = mlAMasa(v, presentacion)
      if (r.ok) texto = <>{fmt(v)} ml = <strong>{fmt(r.valor.valor)} {r.valor.unidad}</strong></>
      else error = r.error
    }
  }
  return (
    <>
      <label className="campo">
        <span>Presentación</span>
        <select aria-label="Presentación" value={id} onChange={(e) => cambiar(e.target.value)}>
          {liquidas.map((p) => (
            <option key={p.id} value={p.id}>
              {etiquetaPresentacion(p)}
            </option>
          ))}
        </select>
      </label>
      <Campo etiqueta={`Concentración del frasco (${unidad}/ml)`} valor={conc} onCambio={setConc} />
      <Campo etiqueta={`Dosis (${unidad})`} valor={masa} onCambio={(v) => { setOrigen('masa'); setMasa(v) }} />
      <Campo etiqueta="Volumen (ml)" valor={ml} onCambio={(v) => { setOrigen('ml'); setMl(v) }} />
      <div className="salida">
        <div role="status" className="resultado">
          {error ? <span className="falta">{error}</span> : texto}
        </div>
      </div>
    </>
  )
}

export function CalculadoraOralVista({ ficha }: { ficha: FichaOral }) {
  const soloAdulto = ficha.pediatria.estado === 'solo_adulto'
  const [modo, setModo] = useState<Modo>(soloAdulto ? 'Dosis fija' : 'Por peso')
  return (
    <section className="calculadora">
      <p>
        <Link to={`/orales/m/${ficha.id}`}>← {ficha.nombre}</Link>
      </p>
      <h2>Calculadora oral: {ficha.nombre}</h2>
      <p className="aviso-fijo">{AVISO}</p>
      {soloAdulto && <p className="sin-datos">Solo adulto: {ficha.pediatria.motivo}</p>}
      <div role="tablist" aria-label="Tipo de cálculo" className="pestanas">
        {MODOS.map((m) => (
          <button key={m} role="tab" type="button" aria-selected={modo === m} disabled={m === 'Por peso' && soloAdulto} onClick={() => setModo(m)}>
            {m}
          </button>
        ))}
      </div>
      <div role="tabpanel" key={modo}>
        {modo === 'Por peso' && <ModoPorPeso ficha={ficha} />}
        {modo === 'Dosis fija' && <ModoFija ficha={ficha} />}
        {modo === 'mg ↔ ml' && <ModoConversion ficha={ficha} />}
      </div>
    </section>
  )
}

export default function CalculadoraOral() {
  const { id } = useParams()
  const ficha = id ? obtenerOral(id) : undefined
  if (!ficha) return <p>Medicamento no encontrado</p>
  return <CalculadoraOralVista key={ficha.id} ficha={ficha} />
}
