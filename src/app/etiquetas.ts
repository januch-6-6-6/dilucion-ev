export const AMBITOS: Record<string, string> = {
  samu: 'SAMU',
  urgencia: 'Urgencia',
  upc: 'UPC',
  hospitalizacion: 'Hospitalización',
  aps: 'APS',
}

export const GRUPOS: Record<string, string> = {
  vasoactivo: 'Vasoactivos',
  antiarritmico: 'Antiarrítmicos',
  anticolinergico: 'Anticolinérgicos',
  sedante: 'Sedantes',
  'analgesico-opioide': 'Analgésicos opioides',
  anestesico: 'Anestésicos',
  electrolito: 'Electrolitos',
}

export const etiquetaGrupo = (g: string) => GRUPOS[g] ?? g
