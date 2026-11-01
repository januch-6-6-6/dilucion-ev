/** Ficha ocular mínima y válida (cefuroxima intracameral, PNT SEFH). Cada prueba la copia y la rompe a propósito. */
export function fichaOcularValida() {
  return {
    id: 'cefuroxima',
    nombre: 'Cefuroxima intracameral',
    comerciales: ['Aprokam'],
    grupo: 'antibiotico',
    familias: ['intracameral'],
    modo: 'intraocular',
    componentes: [],
    altoRiesgo: true,
    registroChile: 'verificado',
    presentaciones: [
      {
        id: 'polvo-750',
        forma: 'polvo',
        cantidad: { valor: 750, unidad: 'mg' },
        registrosIsp: ['F-1/26'],
        usoDirecto: false,
        fuente: { ref: 'ISP', detalle: 'F-1/26' },
      },
    ],
    dosis: [
      {
        indicacion: 'Profilaxis de endoftalmitis',
        via: 'intracameral',
        poblacion: 'adulto',
        final: { cantidad: { valor: 1, unidad: 'mg' }, volumenMl: 0.1 },
        texto: '1 mg en 0,1 ml al final de la cirugía',
        estatus: 'off_label',
        fuente: { ref: 'PNT', detalle: 'cefuroxima intracameral' },
      },
    ],
    protocolos: [
      {
        id: 'pnt-sefh',
        dosis: 0,
        titulo: 'Desde frasco de 750 mg (PNT SEFH)',
        partida: 'polvo-750',
        pasos: [
          { tipo: 'reconstituir', diluyente: 'agua para inyección', volumenMl: 7.5 },
          { tipo: 'diluir', tomarMl: 1, llevarAMl: 10, diluyente: 'suero fisiológico' },
          { tipo: 'cargar', volumenMl: 0.1 },
        ],
        resultado: { valor: 1, unidad: 'mg', volumenMl: 0.1 },
        fuente: { ref: 'PNT', detalle: 'cefuroxima intracameral' },
      },
    ],
    sinPauta: null,
    pediatria: { estado: 'sin_datos', motivo: 'Sin pauta pediátrica en la fuente.' },
    conservacion: [],
    contraindicaciones: [],
    alertas: [],
    discrepancias: [],
    meta: {},
  } as Record<string, any>
}
