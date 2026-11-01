/** Ficha tópica mínima y válida para pruebas. Cada prueba la copia y la rompe a propósito. */
export function fichaTopicaValida() {
  return {
    id: 'colirio-x',
    nombre: 'Colirio X 0,5 %',
    comerciales: ['Equis'],
    grupo: 'antibiotico',
    vias: ['ojo'],
    componentes: [],
    altoRiesgo: false,
    presentaciones: [
      {
        id: 'ojo-solucion-0-5',
        forma: 'solucion',
        via: 'ojo',
        concentracion: '0,5 %',
        registrosIsp: ['F-1/26'],
        fuente: { ref: 'ISP', detalle: 'F-1/26' },
      },
    ],
    dosis: [
      {
        indicacion: 'Conjuntivitis',
        poblacion: 'adulto',
        texto: '1 gota 3 veces al día',
        cantidad: 1,
        unidad: 'gota',
        vecesAlDia: 3,
        porSitio: 'ojo',
        estatus: 'autorizada',
        fuente: { ref: 'CIMA', detalle: '4.2' },
      },
      {
        indicacion: 'Conjuntivitis',
        poblacion: 'pediatrico',
        texto: '1 gota 3 veces al día',
        cantidad: 1,
        unidad: 'gota',
        vecesAlDia: 3,
        porSitio: 'ojo',
        estatus: 'autorizada',
        fuente: { ref: 'CIMA', detalle: '4.2' },
        tambien: [{ ref: 'PED', detalle: 'igual' }],
      },
    ],
    sinPauta: null,
    pediatria: { estado: 'con_dosis', motivo: 'Desde 1 año.' },
    conservacion: [{ validezAbiertoDias: 28, texto: '4 semanas', fuente: { ref: 'CIMA', detalle: '6.3' } }],
    administracion: { texto: 'Ocluir', fuente: { ref: 'CIMA', detalle: '4.2' } },
    contraindicaciones: [],
    alertas: [],
    discrepancias: [],
    meta: {},
  }
}

const f = (id: string, institucion: string) => ({ id, titulo: id, institucion, url: `https://example.org/${id}`, anio: 2026, consultado: '2026-10-30' })
export const fuentesTopicasPrueba = [f('ISP', 'ISP'), f('CIMA', 'AEMPS'), f('CIMA2', 'AEMPS'), f('PED', 'AEP')]
