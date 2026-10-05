import type { FichaOral } from '../../esquema/ficha-oral'

export default function TablaDiscrepancias({ discrepancias }: { discrepancias: FichaOral['discrepancias'] }) {
  if (discrepancias.length === 0) return <p className="vacio">Sin discrepancias entre las fuentes</p>
  return (
    <table className="compatibilidad tabla-discrepancias">
      <thead>
        <tr>
          <th scope="col">Campo</th>
          <th scope="col">Valores por fuente</th>
          <th scope="col">Mostrado</th>
          <th scope="col">Motivo</th>
        </tr>
      </thead>
      <tbody>
        {discrepancias.map((d) => (
          <tr key={d.campo}>
            <td>{d.campo}</td>
            <td>
              <ul>
                {d.valores.map((v) => (
                  <li key={v.fuente}>
                    {v.valor} <cite className="fuente">[{v.fuente}]</cite>
                  </li>
                ))}
              </ul>
            </td>
            <td>
              <strong>{d.mostrado}</strong>
            </td>
            <td>{d.motivo}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
