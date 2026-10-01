/** Color de acento por grupo terapéutico. El rojo NO se usa aquí: queda reservado a alertas y alto riesgo. */
export type ColorGrupo = 'naranjo' | 'violeta' | 'indigo' | 'azul' | 'turquesa' | 'verde' | 'ambar' | 'cian' | 'lima' | 'neutro'

const COLORES: Record<string, ColorGrupo> = {
  vasoactivo: 'naranjo',
  antiarritmico: 'violeta',
  antihipertensivo: 'violeta',
  diuretico: 'violeta',
  sedante: 'indigo',
  anticonvulsivante: 'indigo',
  antipsicotico: 'indigo',
  'analgesico-opioide': 'azul',
  'analgesico-no-opioide': 'azul',
  anestesico: 'turquesa',
  'bloqueador-neuromuscular': 'turquesa',
  antiemetico: 'lima',
  'protector-gastrico': 'lima',
  corticoide: 'lima',
  electrolito: 'verde',
  metabolico: 'verde',
  antiinfeccioso: 'cian',
  antidoto: 'ambar',
  antihistaminico: 'ambar',
  anticolinergico: 'ambar',
}

export const colorGrupo = (grupo: string): ColorGrupo => COLORES[grupo] ?? 'neutro'
