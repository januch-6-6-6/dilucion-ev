import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { parsearNumero } from '../../calculos/numeros'
import { MAX_PASOS, objetivosDe, presentacionesVerificables, tieneVerificador, verificar, type PasoNumerico } from '../../calculos/verificadorOcular'
import { obtenerOcular } from '../../datos/cargarOculares'
import { convertirOcular, type DosisOcular, type FichaOcular, type PresentacionOcular, type UnidadOcular } from '../../esquema/ficha-ocular'
import { AVISO_FORMACION, AVISO_PABELLON, describirPresentacion, finalTexto, unidadTexto } from './textos'

type TipoPaso = 'reconstituir' | 'diluir'
type Fila = { clave: number; tipo: TipoPaso; a: string; b: string }

const redondear = (n: number) => Number(n.toPrecision(3))
const coma = (n: number) => String(redondear(n)).replace('.', ',')

/** El polvo siempre parte reconstituyéndose; una solución puede usarse tal como viene, así que no abre con ningún paso. */
const filasIniciales = (p: PresentacionOcular, clave: number): Fila[] => (p.forma === 'polvo' ? [{ clave, tipo: 'reconstituir', a: '', b: '' }] : [])

/** Dosis de la fuente que aplican a la presentación, en el mismo orden que `objetivosDe`. */
const dosisConFinal = (f: FichaOcular, presentacionId: string): DosisOcular[] =>
  f.dosis.filter((d) => d.final && (!d.presentaciones || d.presentaciones.includes(presentacionId)))

/** «1.000» o «7.500» en un volumen en ml son jeringa con 3 decimales (1 y 7,5), no mil ni siete mil quinientos. */
function leerVolumen(texto: string): number | null {
  const t = texto.trim()
  return /^\d+\.\d{3}$/.test(t) ? parsearNumero(t.replace('.', ',')) : parsearNumero(t)
}

function aPasos(filas: Fila[]): PasoNumerico[] | null {
  const pasos: PasoNumerico[] = []
  for (const fila of filas) {
    const a = leerVolumen(fila.a)
    if (a === null) return null
    if (fila.tipo === 'reconstituir') {
      pasos.push({ tipo: 'reconstituir', volumenMl: a })
    } else {
      const b = leerVolumen(fila.b)
      if (b === null) return null
      pasos.push({ tipo: 'diluir', tomarMl: a, llevarAMl: b })
    }
  }
  return pasos
}

function VerificadorVista({ f }: { f: FichaOcular }) {
  const preparables = presentacionesVerificables(f)
  const [presentacionId, setPresentacionId] = useState(preparables[0].id)
  const presentacion = preparables.find((p) => p.id === presentacionId) ?? preparables[0]
  const [filas, setFilas] = useState<Fila[]>(filasIniciales(preparables[0], 1))
  const [siguiente, setSiguiente] = useState(2)

  const cambiarFila = (clave: number, cambio: Partial<Fila>) => setFilas(filas.map((x) => (x.clave === clave ? { ...x, ...cambio } : x)))
  const elegirPresentacion = (id: string) => {
    const nueva = preparables.find((p) => p.id === id) ?? preparables[0]
    setPresentacionId(nueva.id)
    setFilas(filasIniciales(nueva, siguiente))
    setSiguiente(siguiente + 1)
  }

  const pasos = aPasos(filas)
  const dosis = dosisConFinal(f, presentacion.id)
  let salida: React.ReactNode
  let resumen: string
  if (pasos === null) {
    salida = <span className="falta">Completa los volúmenes de todos los pasos</span>
    resumen = 'Completa los volúmenes de todos los pasos.'
  } else {
    const r = verificar({ presentacion, pasos, objetivos: objetivosDe(f, presentacion.id) })
    if (!r.ok) {
      salida = <span className="falta">{r.error}</span>
      resumen = r.error
    } else {
      const lineas = r.comparaciones.map((c, i) => ({ c, d: dosis[i], obtenido: r.porVolumenObjetivo[i] }))
      const coinciden = lineas.filter((l) => l.c.estado === 'coincide' && l.c.volumenAlcanza)
      const sinVolumen = lineas.filter((l) => l.c.estado === 'coincide' && !l.c.volumenAlcanza)
      resumen = coinciden.length > 0 ? 'Coincide con la fuente.' : sinVolumen.length > 0 ? 'La concentración coincide pero el volumen no alcanza para una dosis.' : 'No coincide con la fuente. No administres; revisa los pasos.'
      salida = (
        <>
          <p>Concentración final: {coma(r.porMl.valor)} {unidadTexto(r.porMl.unidad)} por ml</p>
          <ul className="pasos">
            {lineas.map((l, i) => (
              <li key={i}>
                En {coma(l.d.final?.volumenMl ?? 0)} ml hay {coma(l.obtenido.valor)} {unidadTexto(l.obtenido.unidad)} ·{' '}
                {l.c.estado === 'coincide' ? 'coincide' : 'no coincide'} con {l.d.final ? finalTexto(l.d.final) : ''}
              </li>
            ))}
          </ul>
          {coinciden.length > 0 ? (
            <div className="coincide">
              <p>
                <strong>Coincide con</strong> la fuente:
              </p>
              <ul>
                {coinciden.map((l, i) => (
                  <li key={i}>
                    {l.d.final ? finalTexto(l.d.final) : ''} — {l.d.texto}{' '}
                    <cite className="fuente" title={l.d.fuente.detalle}>[{l.d.fuente.ref}]</cite>
                  </li>
                ))}
              </ul>
              <p className="sin-datos">Solo compara con la fuente: confirma el resultado con el protocolo de tu pabellón.</p>
            </div>
          ) : sinVolumen.length > 0 ? (
            <p className="alerta-roja">
              La concentración coincide con la fuente, pero te quedan {coma(r.volumenDisponibleMl)} ml y la dosis es de{' '}
              {coma(sinVolumen[0].d.final?.volumenMl ?? 0)} ml: no alcanza para una dosis. Revisa los volúmenes.
            </p>
          ) : (
            <p className="alerta-roja">{textoNoCoincide(lineas)}</p>
          )}
        </>
      )
    }
  }

  return (
    <section className="calculadora">
      <p>
        <Link to={`/oftalmologia/m/${f.id}`}>← {f.nombre}</Link>
      </p>
      <h2>Verificar mi preparación: {f.nombre}</h2>
      <p role="note" className="aviso">
        {AVISO_FORMACION}
      </p>
      <p role="note" className="aviso">
        {AVISO_PABELLON}
      </p>
      <p className="sin-datos">Esta herramienta solo compara lo que preparaste con la dosis de la fuente; no propone cómo preparar.</p>
      <label className="campo">
        <span>Frasco o presentación de partida</span>
        <select value={presentacion.id} onChange={(e) => elegirPresentacion(e.target.value)}>
          {preparables.map((p) => (
            <option key={p.id} value={p.id}>
              {describirPresentacion(p)}
            </option>
          ))}
        </select>
      </label>
      {presentacion.forma === 'polvo' && (
        <p className="aviso">
          Supuesto: escribes el volumen total que queda tras disolver el polvo, tal como lo indica la fuente (pestaña Preparación de la ficha). El
          polvo ocupa volumen, así que ese total puede ser mayor que el diluyente que agregas; el verificador no lo calcula por ti.
          {presentacion.nota ? ` Nota de la presentación: ${presentacion.nota}` : ''}
        </p>
      )}
      <h3>Pasos que hiciste</h3>
      {filas.length === 0 && presentacion.forma !== 'polvo' && (
        <p className="sin-datos">Sin pasos: se compara la solución tal como viene. Agrega un paso si la diluiste.</p>
      )}
      {filas.map((fila, i) => {
        const n = i + 1
        return (
          <fieldset key={fila.clave} className="campo">
            <legend>Paso {n}</legend>
            <label className="campo">
              <span>Tipo</span>
              <select aria-label={`Paso ${n}: tipo`} value={fila.tipo} onChange={(e) => cambiarFila(fila.clave, { tipo: e.target.value as TipoPaso, a: '', b: '' })}>
                <option value="reconstituir">Reconstituir el polvo</option>
                <option value="diluir">Diluir (tomar y llevar a un volumen)</option>
              </select>
            </label>
            {fila.tipo === 'reconstituir' ? (
              <label className="campo">
                <span>Volumen final tras reconstituir (ml)</span>
                <input inputMode="decimal" aria-label={`Paso ${n}: volumen final tras reconstituir (ml)`} value={fila.a} onChange={(e) => cambiarFila(fila.clave, { a: e.target.value })} />
              </label>
            ) : (
              <>
                <label className="campo">
                  <span>Tomar (ml)</span>
                  <input inputMode="decimal" aria-label={`Paso ${n}: tomar (ml)`} value={fila.a} onChange={(e) => cambiarFila(fila.clave, { a: e.target.value })} />
                </label>
                <label className="campo">
                  <span>Llevar a (ml)</span>
                  <input inputMode="decimal" aria-label={`Paso ${n}: llevar a (ml)`} value={fila.b} onChange={(e) => cambiarFila(fila.clave, { b: e.target.value })} />
                </label>
              </>
            )}
            <button type="button" className="boton-paso" aria-label={`Quitar paso ${n}`} onClick={() => setFilas(filas.filter((x) => x.clave !== fila.clave))}>
              Quitar paso
            </button>
          </fieldset>
        )
      })}
      <button
        type="button"
        className="boton-paso"
        disabled={filas.length >= MAX_PASOS}
        onClick={() => {
          setFilas([...filas, { clave: siguiente, tipo: 'diluir', a: '', b: '' }])
          setSiguiente(siguiente + 1)
        }}
      >
        Agregar paso
      </button>
      <div className="salida">
        <p role="status" className="solo-lector">
          {resumen}
        </p>
        <div data-testid="resultado" className="resultado">
          {salida}
        </div>
      </div>
    </section>
  )
}

/** Texto rojo exacto: la dosis de la fuente más cercana a lo obtenido (las demás quedan en la lista de arriba). */
function textoNoCoincide(lineas: { c: { diferenciaPct: number | null }; d: DosisOcular; obtenido: { valor: number; unidad: UnidadOcular } }[]): string {
  const distancia = (l: (typeof lineas)[number]): number => {
    const fin = l.d.final
    if (!fin) return Infinity
    const c = fin.cantidad
    if ('min' in c) {
      const min = convertirOcular(c.min, c.unidad, l.obtenido.unidad) ?? c.min
      const max = convertirOcular(c.max, c.unidad, l.obtenido.unidad) ?? c.max
      return l.obtenido.valor < min ? (min - l.obtenido.valor) / min : (l.obtenido.valor - max) / max
    }
    return Math.abs(l.c.diferenciaPct ?? Infinity)
  }
  const cercana = [...lineas].sort((a, b) => distancia(a) - distancia(b))[0]
  const fin = cercana.d.final
  return `NO coincide: obtuviste ${coma(cercana.obtenido.valor)} ${unidadTexto(cercana.obtenido.unidad)} en ${coma(fin?.volumenMl ?? 0)} ml; la fuente dice ${fin ? finalTexto(fin) : ''}. No administres; revisa los pasos.`
}

export default function VerificadorOcular() {
  const { id = '' } = useParams()
  const f = obtenerOcular(id)
  if (!f) return <p>Medicamento no encontrado</p>
  if (!tieneVerificador(f)) {
    return (
      <section className="calculadora">
        <p>
          <Link to={`/oftalmologia/m/${f.id}`}>← {f.nombre}</Link>
        </p>
        <p role="note" className="aviso">
          {AVISO_PABELLON}
        </p>
        <p className="sin-datos">Esta ficha no tiene verificador</p>
      </section>
    )
  }
  return <VerificadorVista key={f.id} f={f} />
}
