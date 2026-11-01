import { parse } from 'yaml'
import { Fuente } from '../esquema/ficha'
import { FichaTopica } from '../esquema/ficha-topica'
import { verificacionTopica, type Verificacion } from '../esquema/validar-topicos'

type Glob = Record<string, string>

// Globs (y no imports directos) para que la ausencia de los archivos no rompa la compilación.
const archivos = import.meta.glob('../../datos/topicos/*.yaml', { query: '?raw', import: 'default', eager: true }) as Glob
const archivoFuentes = import.meta.glob('../../datos/fuentes-topicos.yaml', { query: '?raw', import: 'default', eager: true }) as Glob

/** Fichas tópicas ya validadas al compilar (npm run validar); aquí se vuelven a parsear para tiparlas. */
export const topicos: FichaTopica[] = Object.values(archivos)
  .map((texto) => FichaTopica.parse(parse(texto)))
  .sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))

const textoFuentes = Object.values(archivoFuentes)[0]
export const fuentesTopicos: Fuente[] = textoFuentes ? (parse(textoFuentes) as unknown[]).map((f) => Fuente.parse(f)) : []

const porId = new Map(topicos.map((t) => [t.id, t]))

export const obtenerTopico = (id: string): FichaTopica | undefined => porId.get(id)

export const verificacionDeTopico = (ficha: FichaTopica): Verificacion => verificacionTopica(ficha, fuentesTopicos)
