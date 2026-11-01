"""Tópicos, lote 1: aciclovir → bepotastina (orden alfabético de lista-isp.json)."""
from .comun import NC, cima, conserv, disc, dm, dosis, ficha, ped, pres

SIN_COMBO = ('Combinación registrada solo en Chile: ninguna fuente consultada (CIMA, DailyMed, Pediamécum) trae la '
             'posología de esta asociación; solo hay datos por componente, que no valen para la combinación.')


def fichas():
    f = {}

    # ---------------------------------------------------------------- aciclovir
    c = lambda d: cima('aciclovir', '84832', d)  # noqa: E731  Xorox 30 mg/g pomada oftálmica
    f['aciclovir'] = ficha(
        'aciclovir', 'ACICLOVIR', 'Aciclovir oftálmico', 'antiviral-antifungico',
        [pres('unguento', '3 %', 'ojo', 'F-8844/26', 'F-8704/26', 'F-9585/26')],
        [dosis('Queratitis por herpes simple', 'adulto',
               'Tira de 1 cm de pomada en el saco conjuntival inferior 5 veces al día (cada 4 h aprox.); seguir al menos 3 días después de la curación',
               c('4.2 Adultos: tira de 1 cm dentro del saco conjuntival inferior cinco veces al día (intervalos de aproximadamente 4 horas)'),
               cantidad=1, unidad='cm', veces_dia=5, sitio='ojo', duracion='Hasta 3 días después de la curación completa'),
         dosis('Queratitis por herpes simple', 'pediatrico', 'Igual que en adultos: tira de 1 cm 5 veces al día',
               c('4.2 Población pediátrica: igual que los adultos'), cantidad=1, unidad='cm', veces_dia=5, sitio='ojo')],
        pediatria=('con_dosis', 'La ficha técnica indica la misma pauta que en adultos.'),
        conservacion=conserv('Una vez abierto, máximo 28 días a 25 °C. Conservar por debajo de 25 °C.',
                             c('6.3: una vez abierto, máximo 28 días a 25°C; 6.4 conservar por debajo de 25°C'), dias=28),
        administracion={'texto': 'Vía oftálmica: aplicar la tira de pomada dentro del saco conjuntival inferior.',
                        'fuente': c('4.2 Método de administración: vía oftálmica')},
        contraindicaciones=['Hipersensibilidad a aciclovir, valaciclovir o a algún excipiente (CIMA).'],
        alertas=['No requiere ajuste en mayores de 65 años ni en insuficiencia renal o hepática (CIMA).'],
        discrepancias=[disc('Pauta pediátrica tópica',
                            [('CIMA-TOP-ACICLOVIR-84832', 'Pomada oftálmica: 1 cm 5 veces al día, igual que adultos'),
                             ('PEDIAMECUM-TOP-ACICLOVIR', 'Tópica (sin precisar vía oftálmica): 1 aplicación 6 veces al día durante 7 días')],
                            'Pauta de la ficha técnica oftálmica (5 veces al día)',
                            'La pauta tópica de Pediamécum no es específica de la vía oftálmica (aplica a piel y mucosas); no se usa como pauta del ungüento oftálmico.')],
    )
    ped('aciclovir', 'Tópica: una aplicación en la zona 6 veces/día durante 7 días (no específica de vía oftálmica)')

    # ---------------------------------------------------------------- Rinobanedif
    f['antazolina-bacitracina-neomicina-xilometazolina'] = ficha(
        'antazolina-bacitracina-neomicina-xilometazolina', 'ANTAZOLINA + BACITRACINA + NEOMICINA + XILOMETAZOLINA',
        'Antazolina + bacitracina + neomicina + xilometazolina (ungüento nasal)', 'antibiotico',
        [pres('unguento', NC, 'nariz', 'B-157/23')], [],
        componentes=['Antazolina', 'Bacitracina', 'Neomicina', 'Xilometazolina'],
        pediatria=('sin_datos', 'Sin fuente de posología para la combinación.'),
        alertas=['Neomicina (Pediamécum): con filtrado glomerular <10 ml/min no usarla por vía oral ni tópica.'],
        sin_pauta=SIN_COMBO,
    )
    ped('neomicina', 'Insuficiencia renal: FG <10: no utilizarla por vía oral ni por vía tópica')

    # ---------------------------------------------------------------- antazolina + nafazolina
    c = lambda d: cima('antazolina-nafazolina', '19763', d)  # noqa: E731  Alergoftal 0,25+5 mg/ml
    f['antazolina-nafazolina'] = ficha(
        'antazolina-nafazolina', 'ANTAZOLINA + NAFAZOLINA', 'Antazolina + nafazolina oftálmica', 'descongestionante',
        [pres('solucion', NC, 'ojo', 'F-5540/25')],
        [dosis('Conjuntivitis alérgica / irritación ocular', 'adulto',
               '1 o 2 gotas en cada ojo afectado 3 o 4 veces al día (o cada 3–4 h según síntomas); no más de 3–5 días',
               c('4.2.1 Adultos: 1 ó 2 gotas en cada ojo afectado 3 ó 4 veces al día; duración no superior a 3-5 días'),
               cantidad=2, unidad='gota', veces_dia=4, sitio='ojo', duracion='Máximo 3–5 días (congestión de rebote)')],
        componentes=['Antazolina', 'Nafazolina'],
        pediatria=('no_establecida', 'La ficha técnica no establece seguridad ni eficacia en niños.'),
        conservacion=conserv('Desechar al mes de abierto (la calculadora usa 28 días). No conservar sobre 30 °C.',
                             c('6.3: desechar el envase al mes de abierto; 6.4 no conservar a temperatura superior a 30º'), dias=28),
        administracion={'texto': 'Cabeza hacia atrás, bajar el párpado inferior y dejar caer las gotas en el saco conjuntival; '
                                 'cerrar los ojos unos segundos. Esperar al menos 5 minutos antes de otro colirio.',
                        'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Glaucoma de ángulo estrecho (CIMA).', 'Hipersensibilidad a los principios activos o a agentes adrenérgicos (CIMA).'],
        alertas=['Uso prolongado: congestión de rebote; si no mejora en 3–5 días, reevaluar (CIMA).'],
        discrepancias=[disc('Pauta pediátrica',
                            [('CIMA-TOP-ANTAZOLINA-NAFAZOLINA-19763', 'No establecida en niños'),
                             ('PEDIAMECUM-TOP-NAFAZOLINA', 'Nafazolina sola: 1–2 gotas hasta 4 veces al día')],
                            'Sin pauta pediátrica',
                            'Pediamécum describe solo la nafazolina; la ficha de un componente no vale para la combinación.')],
    )
    ped('nafazolina', '1 o 2 gotas hasta 4 veces al día, cada 6 a 8 horas (nafazolina sola)')

    # ---------------------------------------------------------------- atropina
    c = lambda d: cima('atropina', '39474', d)  # noqa: E731  Colirofta atropina 10 mg/ml
    p = lambda d: ped('atropina', d)  # noqa: E731
    f['atropina'] = ficha(
        'atropina', 'ATROPINA', 'Atropina oftálmica 1 %', 'midriatico',
        [pres('solucion', '1 %', 'ojo', 'F-1161/23', 'F-15393/26')],
        [dosis('Efecto ciclopléjico sostenido (uveítis, iritis)', 'adulto', '2 gotas 3 veces al día',
               c('4.2 Uso en adultos: cuando se pretenda un efecto sostenido, tres aplicaciones diarias de 2 gotas'),
               cantidad=2, unidad='gota', veces_dia=3, sitio='ojo'),
         dosis('Refracción ciclopléjica', 'adulto', '1 o 2 gotas en cada ojo 2 veces al día, de 1 a 3 días antes del examen',
               c('4.2 Uso en adultos: refracción ciclopléjica 1 ó 2 gotas en cada ojo dos veces al día, de 1 a 3 días antes'),
               cantidad=2, unidad='gota', veces_dia=2, sitio='ojo', duracion='1 a 3 días'),
         dosis('Efecto sostenido', 'pediatrico', '1 gota 3 veces al día; usar la dosis eficaz más baja',
               c('4.2 Población pediátrica: 10 mg/ml contraindicado en menores de 3 años; efecto sostenido, tres aplicaciones diarias de 1 gota'),
               cantidad=1, unidad='gota', veces_dia=3, sitio='ojo', condicion='Solo desde los 3 años, con precaución',
               tambien=[p('Finalidad terapéutica: 1 gota, 3 veces al día')]),
         dosis('Refracción ciclopléjica', 'pediatrico', '1 o 2 gotas 2 veces al día, de 1 a 3 días antes del examen',
               c('4.2 Población pediátrica: examen de refracción 1 ó 2 gotas 2 veces al día, de 1 a 3 días antes'),
               cantidad=2, unidad='gota', veces_dia=2, sitio='ojo', condicion='Solo desde los 3 años, con precaución'),
         dosis('Refracción en niños de 1 a 3 años', 'pediatrico', '1 gota 2 veces al día, 1–2 días antes del examen',
               p('En estudio de refracción en niños ≥1 año: 1 gota 2 veces al día, 1-2 días antes del examen'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', estatus='off_label',
               condicion='Pediamécum desde 1 año; la ficha técnica contraindica la atropina 1 % en menores de 3 años')],
        alto_riesgo=True,
        pediatria=('con_dosis', 'Ficha técnica: la atropina 1 % está contraindicada en menores de 3 años; desde los 3 años con precaución.', '3 años (ficha técnica)'),
        conservacion=conserv('Desechar 4 semanas después de abrir. Conservar por debajo de 25 °C.',
                             c('6.3: desechar 4 semanas después de la primera apertura; 6.4 por debajo de 25ºC'), dias=28),
        administracion={'texto': 'Lavarse las manos. Tras instilar, ocluir el conducto nasolagrimal 2–3 minutos para reducir la absorción sistémica. '
                                 'Espaciar al menos 5 minutos de otros colirios; las pomadas al final. No tocar el ojo con la punta del frasco.',
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Glaucoma primario o predisposición a glaucoma de ángulo estrecho (CIMA).',
                            'Niños con síndrome de Down, parálisis espástica o lesión cerebral (CIMA).',
                            'Atropina 1 % en menores de 3 años (CIMA).',
                            'Menores de 12 años con reacción grave previa a atropina; lactancia (CIMA).'],
        alertas=['Riesgo de efectos adversos sistémicos graves en niños: usar la dosis eficaz más baja (CIMA).',
                 'Ancianos: más riesgo de glaucoma no diagnosticado y de reacciones psicóticas (CIMA).'],
        discrepancias=[disc('Edad mínima pediátrica',
                            [('CIMA-TOP-ATROPINA-39474', 'Atropina 10 mg/ml (1 %): contraindicada en menores de 3 años'),
                             ('PEDIAMECUM-TOP-ATROPINA', 'Refracción en niños ≥1 año: 1 gota 2 veces al día')],
                            'Ambas: ficha técnica como autorizada (≥3 años) y Pediamécum como off-label (1–3 años)',
                            'Decisión de Héctor (31-oct): la pauta de Pediamécum se muestra como off-label con alerta.')],
    )

    # ---------------------------------------------------------------- azelastina
    c = lambda d: cima('azelastina', '62373', d)  # noqa: E731  Afluon 0,5 mg/ml
    p = lambda d: ped('azelastina-oftalmica', d)  # noqa: E731
    f['azelastina'] = ficha(
        'azelastina', 'AZELASTINA', 'Azelastina oftálmica', 'antialergico',
        [pres('solucion', '0,05 %', 'ojo', 'F-11830/22')],
        [dosis('Conjuntivitis alérgica estacional', 'adulto', '1 gota en cada ojo 2 veces al día; si hace falta, hasta 4 veces al día',
               c('4.2: adultos y niños desde 4 años, una gota en cada ojo dos veces al día, aumentable a cuatro'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', duracion='Máximo 6 semanas',
               tambien=[p('1 gota cada 12 horas; se puede aumentar hasta 4 veces por día; máximo 6 semanas')]),
         dosis('Conjuntivitis alérgica perenne', 'adulto', '1 gota en cada ojo 2 veces al día; si hace falta, hasta 4 veces al día',
               c('4.2: conjuntivitis no estacional, adultos y niños desde 12 años, una gota dos veces al día; máximo 6 semanas'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', duracion='Máximo 6 semanas'),
         dosis('Conjuntivitis alérgica estacional', 'pediatrico', '1 gota en cada ojo 2 veces al día; si hace falta, hasta 4 veces al día',
               c('4.2: la dosis normal en adultos y niños a partir de los 4 años'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo',
               condicion='Desde los 4 años (perenne: desde los 12)', duracion='Máximo 6 semanas',
               tambien=[p('Administración: 1 gota cada 12 horas; hasta 4 veces por día')])],
        pediatria=('con_dosis', 'Estacional desde los 4 años; perenne desde los 12 años.', '4 años'),
        conservacion=conserv('Una vez abierto, no usar después de 4 semanas. Sin condiciones especiales de conservación.',
                             c('6.3: una vez abierto, no utilizar después de 4 semanas'), dias=28),
        administracion={'texto': 'Si se prevé exposición al alérgeno, aplicarla antes, de forma preventiva. '
                                 'Consultar si no mejora en 48 horas.', 'fuente': c('4.2 Posología y aviso para uso sin prescripción')},
        contraindicaciones=['Hipersensibilidad a azelastina o a algún excipiente (CIMA).'],
        alertas=['Más de 6 semanas de uso solo con supervisión médica (CIMA, Pediamécum).'],
    )

    # ---------------------------------------------------------------- azelastina + fluticasona
    c = lambda d: cima('azelastina-fluticasona', '76618', d)  # noqa: E731  Dymista 137/50
    f['azelastina-fluticasona'] = ficha(
        'azelastina-fluticasona', 'AZELASTINA + FLUTICASONA', 'Azelastina + fluticasona nasal', 'corticoide-nasal',
        [pres('spray', '137 mcg azelastina + 50 mcg fluticasona por pulverización', 'nariz', 'F-28330/24')],
        [dosis('Rinitis alérgica', 'adulto', '1 pulverización en cada fosa nasal 2 veces al día (mañana y noche)',
               c('4.2.1 Adultos y adolescentes (12 años y mayores): una aplicación en cada fosa nasal, dos veces al día'),
               cantidad=1, unidad='pulverizacion', veces_dia=2, sitio='fosa', condicion='Adultos y adolescentes desde 12 años',
               duracion='Uso regular mientras dure la exposición al alérgeno')],
        componentes=['Azelastina', 'Fluticasona'],
        pediatria=('no_establecida', 'No se recomienda en menores de 12 años: seguridad y eficacia no establecidas (CIMA).', '12 años'),
        conservacion=conserv('Validez en uso: 6 meses desde el primer uso. No refrigerar ni congelar.',
                             c('6.3: validez en uso (después del primer uso) 6 meses; 6.4 no refrigerar o congelar'), dias=180),
        administracion={'texto': 'Agitar suavemente 5 segundos. Antes del primer uso, cebar la bomba 6 veces (y otra vez si lleva más de 7 días sin usar). '
                                 'Sonarse, inclinar la cabeza hacia abajo y pulverizar una vez en cada fosa. Evitar los ojos.',
                        'fuente': c('4.2.2 Forma de administración e instrucciones de uso')},
        contraindicaciones=['Hipersensibilidad a los principios activos o a algún excipiente (CIMA).'],
        alertas=['Sin datos en insuficiencia renal ni hepática (CIMA).'],
        discrepancias=[disc('Fuente pediátrica descargada',
                            [('PEDIAMECUM-TOP-AZELASTINA-OFTALMICA', 'Ficha de azelastina COLIRIO (vía oftálmica)')],
                            'No se usa', 'Vía equivocada: el colirio no informa sobre el spray nasal combinado.')],
    )
    ped('azelastina-oftalmica', 'Ficha de la vía oftálmica (no aplica al spray nasal)')

    # ---------------------------------------------------------------- azitromicina
    c = lambda d: cima('azitromicina', '69522', d)  # noqa: E731  Azydrop 15 mg/g unidosis
    f['azitromicina'] = ficha(
        'azitromicina', 'AZITROMICINA', 'Azitromicina oftálmica', 'antibiotico',
        [pres('solucion', '1,43 %', 'ojo', 'F-19315/22', unidosis=True)],
        [dosis('Conjuntivitis bacteriana o tracomatosa', 'adulto', '1 gota en el fondo de saco conjuntival 2 veces al día (mañana y tarde) durante 3 días',
               c('4.2.1 Población adulta: una gota dos veces al día, mañana y tarde durante tres días'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', duracion='3 días; no hace falta prolongarlo'),
         dosis('Conjuntivitis bacteriana o tracomatosa', 'pediatrico', 'Igual que en adultos: 1 gota 2 veces al día durante 3 días',
               c('4.2.1 Población pediátrica: no se requiere un ajuste de la dosis'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo',
               duracion='3 días')],
        pediatria=('con_dosis', 'La ficha técnica no exige ajuste en niños.'),
        conservacion=conserv('Envase unidosis: usar de inmediato y desechar después de cada uso. No conservar sobre 25 °C; mantener en el sobre (luz).',
                             c('6.3: desechar el envase unidosis inmediatamente después del primer uso; 6.4')),
        administracion={'texto': 'Lavarse las manos antes y después. No tocar el ojo ni los párpados con la punta del unidosis; desecharlo tras usarlo.',
                        'fuente': c('4.2 Método de administración')},
        contraindicaciones=['Hipersensibilidad a azitromicina u otro macrólido (CIMA).'],
        alertas=['El cumplimiento de las 6 dosis es importante para el éxito del tratamiento (CIMA).'],
    )

    # ---------------------------------------------------------------- bacitracina + neomicina + polimixina B
    d_ = lambda d: dm('bacitracina-neomicina-polimixina-b', d)  # noqa: E731
    f['bacitracina-neomicina-polimixina-b'] = ficha(
        'bacitracina-neomicina-polimixina-b', 'BACITRACINA + NEOMICINA + POLIMIXINA B', 'Bacitracina + neomicina + polimixina B oftálmica',
        'antibiotico',
        [pres('unguento', NC, 'ojo', 'B-885/25')],
        [dosis('Infección ocular superficial', 'adulto', 'Aplicar el ungüento en el saco conjuntival cada 3 o 4 horas durante 7 a 10 días',
               d_('DOSAGE: apply into the conjunctival sac every 3 or 4 hours for 7 to 10 days'),
               duracion='7 a 10 días')],
        componentes=['Bacitracina', 'Neomicina', 'Polimixina B'],
        pediatria=('no_establecida', 'Seguridad y eficacia en niños no establecidas (etiqueta FDA).'),
        conservacion=conserv('Conservar entre 15 y 25 °C, bien cerrado. La etiqueta no fija validez tras abrir.',
                             d_('Storage: store between 15°C to 25°C; keep tightly closed')),
        administracion={'texto': 'Aplicar en el saco conjuntival del ojo afectado.', 'fuente': d_('DOSAGE AND ADMINISTRATION')},
        contraindicaciones=['Hipersensibilidad a cualquiera de sus componentes (FDA).'],
        alertas=['Neomicina: reacciones de sensibilización alérgica frecuentes (FDA).'],
    )

    # ---------------------------------------------------------------- bepotastina
    d_ = lambda d: dm('bepotastina', d)  # noqa: E731
    f['bepotastina'] = ficha(
        'bepotastina', 'BEPOTASTINA', 'Bepotastina oftálmica', 'antialergico',
        [pres('solucion', '1,5 %', 'ojo', 'F-27478/23')],
        [dosis('Prurito por conjuntivitis alérgica', 'adulto', '1 gota en el ojo afectado 2 veces al día',
               d_('DOSAGE: instill one drop into the affected eye(s) twice a day'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo'),
         dosis('Prurito por conjuntivitis alérgica', 'pediatrico', '1 gota en el ojo afectado 2 veces al día',
               d_('8.4 Pediatric Use: not established under 2 years of age; efficacy under 10 years extrapolated'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', condicion='Desde los 2 años')],
        pediatria=('con_dosis', 'No establecida en menores de 2 años (FDA).', '2 años'),
        conservacion=None,
        administracion={'texto': 'Retirar los lentes de contacto antes de instilar.', 'fuente': d_('DOSAGE: remove contact lenses prior to instillation')},
        contraindicaciones=['Hipersensibilidad a bepotastina o a algún componente (FDA).'],
    )
    return f
