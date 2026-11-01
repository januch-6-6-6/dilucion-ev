import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { combinacionesCalculables, duracionEnvase, GOTAS_POR_ML_SUPUESTO, validezDe } from '../../calculos/duracionEnvase'
import { parsearNumero } from '../../calculos/numeros'
import { obtenerTopico } from '../../datos/cargarTopicos'
import type { FichaTopica } from '../../esquema/ficha-topica'
import { AVISO } from '../aviso'
import Campo from '../componentes/Campo'
import { describirPresentacion, nombreSitio, UNIDAD } from './textos'

const fmt = (n: number) => String(n).replace('.', ',')

export function CalculadoraTopicaVista({ ficha }: { ficha: FichaTopica }) {
  const opciones = combinacionesCalculables(ficha)
  const [i, setI] = useState(0)
  const [sitios, setSitios] = useState(1)
  const [contenido, setContenido] = useState('')
  const [gotasPorMl, setGotasPorMl] = useState(String(GOTAS_POR_ML_SUPUESTO))
  const op = opciones[i]
  if (!op) return <p className="sin-datos">Esta ficha no tiene una pauta con cantidad y frecuencia diaria fijas: no se puede calcular.</p>
  const { dosis, presentacion } = op
  const esGota = dosis.unidad === 'gota'
  const unidad = dosis.unidad === 'gota' ? 'gota' : 'pulverizacion'
  const validez = validezDe(ficha, presentacion.id)

  let salida: React.ReactNode
  const c = parsearNumero(contenido)
  const g = parsearNumero(gotasPorMl)
  if (c === null) salida = <span className="falta">{esGota ? 'Falta el volumen del frasco (ml)' : 'Faltan las pulverizaciones del envase'}</span>
  else if (esGota && g === null) salida = <span className="falta">Faltan las gotas por ml</span>
  else {
    try {
      const r = duracionEnvase({
        cantidad: dosis.cantidad as number,
        vecesAlDia: dosis.vecesAlDia as number,
        sitios,
        unidad,
        contenido: c,
        gotasPorMl: g ?? undefined,
        validezAbiertoDias: validez,
      })
      const [uno, varios] = UNIDAD[unidad]
      salida = (
        <>
          <p>
            Alcanza para <strong>{r.dias} días</strong>
            {r.limita === 'validez' ? ` (limita la validez tras abrir: ${validez} días; por contenido alcanzaría ${r.diasPorContenido})` : ''}.
          </p>
          <ol className="pasos">
            <li>
              Contenido: {esGota ? `${fmt(c)} ml × ${fmt(g as number)} gotas/ml = ` : ''}
              {fmt(r.unidadesTotales)} {r.unidadesTotales === 1 ? uno : varios}
            </li>
            <li>
              Consumo diario: {fmt(dosis.cantidad as number)} × {fmt(dosis.vecesAlDia as number)} veces × {sitios} {nombreSitio(dosis.porSitio, sitios)} ={' '}
              {fmt(r.consumoDiario)} {varios}/día
            </li>
            <li>
              {fmt(r.unidadesTotales)} ÷ {fmt(r.consumoDiario)} = {r.diasPorContenido} días
              {validez ? `; validez tras abrir: ${validez} días` : '; la fuente no fija validez tras abrir'}
            </li>
          </ol>
        </>
      )
    } catch (e) {
      salida = <span className="falta">{(e as Error).message}</span>
    }
  }

  return (
    <section className="calculadora">
      <p>
        <Link to={`/topicos/m/${ficha.id}`}>← {ficha.nombre}</Link>
      </p>
      <h2>¿Cuánto dura el frasco? {ficha.nombre}</h2>
      <p className="aviso-fijo">{AVISO}</p>
      <label className="campo">
        <span>Pauta y presentación</span>
        <select aria-label="Pauta y presentación" value={i} onChange={(e) => setI(Number(e.target.value))}>
          {opciones.map((o, k) => (
            <option key={`${o.indice}-${o.presentacion.id}`} value={k}>
              {o.dosis.poblacion === 'adulto' ? 'Adulto' : 'Pediátrica'} · {o.dosis.indicacion} · {describirPresentacion(o.presentacion)}
            </option>
          ))}
        </select>
      </label>
      <p>
        Pauta: {dosis.texto} <cite className="fuente" title={dosis.fuente.detalle}>[{dosis.fuente.ref}]</cite>
        {dosis.estatus === 'off_label' && <span className="etiqueta off-label"> Off-label</span>}
      </p>
      <label className="campo">
        <span>¿En cuántos {nombreSitio(dosis.porSitio, 2)}?</span>
        <select aria-label="Sitios" value={sitios} onChange={(e) => setSitios(Number(e.target.value))}>
          <option value={1}>1 ({nombreSitio(dosis.porSitio, 1)})</option>
          <option value={2}>2 (ambos)</option>
        </select>
      </label>
      <Campo etiqueta={esGota ? 'Volumen del frasco (ml)' : 'Pulverizaciones por envase'} valor={contenido} onCambio={setContenido} />
      {esGota && (
        <>
          <Campo etiqueta="Gotas por ml" valor={gotasPorMl} onCambio={setGotasPorMl} />
          <p className="aviso">
            Supuesto: {GOTAS_POR_ML_SUPUESTO} gotas por ml es un valor habitual, no un dato del producto. El tamaño de la gota cambia según el gotero.
            Si el envase indica otro número, cámbialo.
          </p>
        </>
      )}
      <div className="salida">
        <div role="status" className="resultado">
          {salida}
        </div>
      </div>
    </section>
  )
}

export default function CalculadoraTopica() {
  const { id } = useParams()
  const ficha = id ? obtenerTopico(id) : undefined
  if (!ficha) return <p>Medicamento no encontrado</p>
  return <CalculadoraTopicaVista key={ficha.id} ficha={ficha} />
}
