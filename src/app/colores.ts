/** Color de acento por grupo terapéutico. El rojo NO se usa aquí: queda reservado a alertas y alto riesgo. */
export type ColorGrupo = 'naranjo' | 'violeta' | 'indigo' | 'azul' | 'turquesa' | 'verde' | 'ambar' | 'neutro'

const COLORES: Record<string, ColorGrupo> = {
  vasoactivo: 'naranjo',
  antiarritmico: 'violeta',
  sedante: 'indigo',
  'analgesico-opioide': 'azul',
  anestesico: 'turquesa',
  electrolito: 'verde',
  anticolinergico: 'ambar',
}

export const colorGrupo = (grupo: string): ColorGrupo => COLORES[grupo] ?? 'neutro'
