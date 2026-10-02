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
  'analgesico-no-opioide': 'Analgésicos no opioides',
  antidoto: 'Antídotos',
  antiemetico: 'Antieméticos',
  antihipertensivo: 'Antihipertensivos',
  antihistaminico: 'Antihistamínicos',
  antiinfeccioso: 'Antiinfecciosos',
  antipsicotico: 'Antipsicóticos',
  anticonvulsivante: 'Anticonvulsivantes',
  'bloqueador-neuromuscular': 'Bloqueadores neuromusculares',
  corticoide: 'Corticoides',
  diuretico: 'Diuréticos',
  hematologico: 'Hematológicos',
  metabolico: 'Metabólicos',
  'protector-gastrico': 'Protectores gástricos',
}

export const etiquetaGrupo = (g: string) => GRUPOS[g] ?? g
