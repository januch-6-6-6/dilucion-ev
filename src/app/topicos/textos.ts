import type { DosisTopica, FormaTopica, PresentacionTopica, Via } from '../../esquema/ficha-topica'

export const VIA: Record<Via, string> = { ojo: 'Oftálmico', oido: 'Ótico', nariz: 'Nasal' }
export const FORMA: Record<FormaTopica, string> = {
  solucion: 'Solución',
  suspension: 'Suspensión',
  emulsion: 'Emulsión',
  unguento: 'Ungüento',
  gel: 'Gel',
  spray: 'Spray',
}
export const PEDIATRIA = {
  con_dosis: 'Con dosis pediátrica',
  no_establecida: 'No establecida en niños',
  contraindicada: 'Contraindicada en niños',
  sin_datos: 'Sin datos pediátricos',
} as const

export const TEXTO_SIN_PAUTA = 'Ficha informativa: no se muestra una pauta de dosis.'

export const describirPresentacion = (p: PresentacionTopica): string =>
  `${FORMA[p.forma]} ${VIA[p.via].toLowerCase()} ${p.concentracion}${p.unidosis ? ' (unidosis)' : ''}`

const SITIO = { ojo: ['ojo', 'ojos'], oido: ['oído', 'oídos'], fosa: ['fosa nasal', 'fosas nasales'] } as const
export const nombreSitio = (s: DosisTopica['porSitio'], n: number): string => (s ? SITIO[s][n === 1 ? 0 : 1] : n === 1 ? 'sitio' : 'sitios')
export const UNIDAD = { gota: ['gota', 'gotas'], pulverizacion: ['pulverización', 'pulverizaciones'], cm: ['cm', 'cm'], aplicacion: ['aplicación', 'aplicaciones'] } as const
