import { useState } from 'react'
import { Link } from 'react-router-dom'
import paquete from '../../../package.json'
import { fuentes, medicamentos } from '../../datos/cargar'
import { AVISO } from '../aviso'
import { aplicarTema, leerTema, type Tema } from '../tema'

export default function Acerca() {
  const [tema, setTema] = useState<Tema>(leerTema)
  return (
    <section>
      <p>
        <Link to="/">← Inicio</Link>
      </p>
      <h2>Acerca de Dilución EV</h2>
      <p className="aviso-fijo">{AVISO}</p>
      <p>
        Versión {paquete.version} · {medicamentos.length} medicamentos · datos consultados en las fuentes listadas abajo.
      </p>
      <label className="campo">
        <span>Tema</span>
        <select
          aria-label="Tema"
          value={tema}
          onChange={(e) => {
            const t = e.target.value as Tema
            setTema(t)
            aplicarTema(t)
          }}
        >
          <option value="sistema">Según el sistema</option>
          <option value="claro">claro</option>
          <option value="oscuro">oscuro</option>
        </select>
      </label>
      <h3>Fuentes</h3>
      <ul>
        {fuentes.map((f) => (
          <li key={f.id}>
            <strong>{f.id}</strong>: <a href={f.url} target="_blank" rel="noreferrer">{f.titulo}</a> — {f.institucion} ({f.anio})
          </li>
        ))}
      </ul>
      <h3>Medicamentos orales (APS)</h3>
      <p>
        La sección de medicamentos orales tiene un propósito estrictamente de formación. Las fuentes primarias utilizadas
        (CIMA y Pediamécum) son españolas y <strong>no son chilenas</strong>. El registro sanitario ante el Instituto de Salud Pública (ISP)
        de Chile se encuentra actualmente <strong>sin verificar</strong> para estas presentaciones.
      </p>
      <p>
        El aviso de «fuente única» señala fichas en las que la información posológica proviene de una sola institución (habitualmente CIMA),
        al no disponer de monografía pediátrica independiente en Pediamécum. En dichos casos se recomienda contrastar especialmente la dosis con
        guías clínicas y protocolos institucionales.
      </p>
      <p>Proyecto de formación y portafolio de Héctor Salvo Agüero (TENS e Ingeniero en Informática).</p>
      <p>
        Privacidad: la app cuenta visitas de forma anónima con{' '}
        <a href="https://www.goatcounter.com/" target="_blank" rel="noreferrer">GoatCounter</a> (sin cookies ni datos personales). Lo que
        escribe en las calculadoras no sale de su dispositivo.
      </p>
    </section>
  )
}
