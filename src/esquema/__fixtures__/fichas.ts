// Fixtures de prueba (datos ficticios, solo para tests del validador).
export const fuentesPrueba = [
  { id: 'F1', titulo: 'Fuente de prueba', institucion: 'Test', url: 'https://example.org', anio: 2026, consultado: '2026-10-01' },
]

const f = { ref: 'F1', detalle: 'p. 1' }

export function fichaValida(id = 'droga-a', extra: Record<string, unknown> = {}) {
  return {
    id,
    nombre: id,
    comerciales: [],
    grupo: 'vasoactivo',
    ambitos: ['urgencia'],
    altoRiesgo: false,
    presentaciones: [{ id: 'amp', forma: 'ampolla', cantidad: { valor: 4, unidad: 'mg' }, volumenMl: 4, fuente: f }],
    reconstitucion: null,
    dilucion: {
      sueros: ['SG5'],
      concentracionMax: { valor: 32, unidad: 'mcg', fuente: f },
      estandar: [{ descripcion: '4 mg en 250 ml', cantidad: { valor: 4, unidad: 'mg' }, volumenFinalMl: 250, fuente: f }],
    },
    administracion: { vias: ['infusion_continua'], texto: 'Por bomba', requiereViaCentral: true, requiereBomba: true, fuente: f },
    dosis: [{ indicacion: 'Shock', poblacion: 'adulto', unidad: 'mcg/kg/min', min: 0.05, max: 1, fuente: f }],
    sinDosisPediatrica: true,
    estabilidad: { ambienteH: 24, protegerLuz: true, fuente: f },
    compatibilidad: [],
    interaccionesGraves: [],
    efectosAdversos: { frecuentes: ['x'], graves: ['y'], vigilar: ['PA'], fuente: f },
    alertas: [],
    meta: { discrepancias: [] },
    ...extra,
  }
}
