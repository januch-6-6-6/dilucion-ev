import { parse } from 'yaml'
import { Fuente } from '../esquema/ficha'
import { FichaOcular } from '../esquema/ficha-ocular'
import { verificacionOcular } from '../esquema/validar-oculares'
import type { Verificacion } from '../esquema/validar-topicos'

type Glob = Record<string, string>

// Globs (y no imports directos) para que la ausencia de los archivos no rompa la compilación.
const archivos = import.meta.glob('../../datos/oftalmo/*.yaml', { query: '?raw', import: 'default', eager: true }) as Glob
const archivoFuentes = import.meta.glob('../../datos/fuentes-oftalmo.yaml', { query: '?raw', import: 'default', eager: true }) as Glob

/** Fichas de pabellón ya validadas al compilar (npm run validar); aquí se vuelven a parsear para tiparlas. */
export const oculares: FichaOcular[] = Object.values(archivos)
  .map((texto) => FichaOcular.parse(parse(texto)))
  .sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))

const textoFuentes = Object.values(archivoFuentes)[0]
export const fuentesOculares: Fuente[] = textoFuentes ? (parse(textoFuentes) as unknown[]).map((f) => Fuente.parse(f)) : []

const porId = new Map(oculares.map((o) => [o.id, o]))

export const obtenerOcular = (id: string): FichaOcular | undefined => porId.get(id)

export const verificacionDeOcular = (ficha: FichaOcular): Verificacion => verificacionOcular(ficha, fuentesOculares)
