// Fixtures de prueba para fichas orales (datos ficticios, solo para tests).
export const fuentesOralesPrueba = [
  { id: 'F1', titulo: 'Fuente oral de prueba', institucion: 'Test', url: 'https://example.org', anio: 2026, consultado: '2026-10-01' },
]

const f = { ref: 'F1', detalle: 'p. 1' }

export function fichaOralValida(id = 'paracetamol', extra: Record<string, unknown> = {}) {
  return {
    id,
    nombre: id,
    comerciales: [],
    grupo: 'analgesico',
    ambitos: ['aps'],
    altoRiesgo: false,
    presentaciones: [
      {
        id: 'comp-500',
        forma: 'comprimido',
        cantidad: { valor: 500, unidad: 'mg' },
        partible: 'mitades',
        liberacionProlongada: false,
        registroChile: 'verificado',
        fuente: f,
      },
      {
        id: 'jarabe-32',
        forma: 'jarabe',
        concentracion: { valor: 32, unidad: 'mg' },
        partible: 'no',
        liberacionProlongada: false,
        registroChile: 'verificado',
        fuente: f,
      },
    ],
    dosis: [
      { indicacion: 'Dolor', poblacion: 'adulto', regimen: 'fija', base: 'toma', unidad: 'mg', min: 500, max: 1000, tomasPorDia: 4, estatus: 'autorizada', fuente: f },
      { indicacion: 'Dolor', poblacion: 'pediatrico', regimen: 'por_peso', base: 'toma', unidad: 'mg/kg', min: 10, max: 15, intervaloH: 6, estatus: 'autorizada', fuente: f },
    ],
    pediatria: { estado: 'con_dosis' },
    discrepancias: [],
    administracion: { comida: 'indiferente', texto: 'Con agua', fuente: f },
    ajusteRenalHepatico: null,
    alertas: [],
    meta: {},
    ...extra,
  }
}
