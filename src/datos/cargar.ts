import { parse } from 'yaml'
import { Ficha, Fuente } from '../esquema/ficha'
import textoFuentes from '../../datos/fuentes.yaml?raw'

const archivos = import.meta.glob('../../datos/medicamentos/*.yaml', { query: '?raw', import: 'default', eager: true }) as Record<
  string,
  string
>

/** Fichas ya validadas al compilar (npm run validar); aquí se vuelven a parsear para tiparlas. */
export const medicamentos: Ficha[] = Object.values(archivos)
  .map((texto) => Ficha.parse(parse(texto)))
  .sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))

export const fuentes: Fuente[] = (parse(textoFuentes) as unknown[]).map((f) => Fuente.parse(f))

const porId = new Map(medicamentos.map((m) => [m.id, m]))

export function obtenerFicha(id: string): Ficha | undefined {
  return porId.get(id)
}
