import { parse } from 'yaml'
import { Fuente } from '../esquema/ficha'
import { FichaOral } from '../esquema/ficha-oral'
import { verificacionDe } from '../esquema/validar-orales'

type Glob = Record<string, string>

// Globs (y no imports directos) para que la ausencia de los archivos no rompa la compilación.
const archivos = import.meta.glob('../../datos/orales/*.yaml', { query: '?raw', import: 'default', eager: true }) as Glob
const archivoFuentes = import.meta.glob('../../datos/fuentes-orales.yaml', { query: '?raw', import: 'default', eager: true }) as Glob

/** Fichas orales ya validadas al compilar (npm run validar); aquí se vuelven a parsear para tiparlas. */
export const orales: FichaOral[] = Object.values(archivos)
  .map((texto) => FichaOral.parse(parse(texto)))
  .sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))

const textoFuentes = Object.values(archivoFuentes)[0]
export const fuentesOrales: Fuente[] = textoFuentes ? (parse(textoFuentes) as unknown[]).map((f) => Fuente.parse(f)) : []

const porId = new Map(orales.map((o) => [o.id, o]))

export const obtenerOral = (id: string): FichaOral | undefined => porId.get(id)

export const verificacion = (ficha: FichaOral): 'dos_fuentes' | 'fuente_unica' => verificacionDe(ficha, fuentesOrales)
