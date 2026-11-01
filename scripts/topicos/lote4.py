"""Tópicos, lote 4: mometasona → tropicamida."""
from .comun import NC, cima, conserv, disc, dm, dosis, ficha, ped, pres
from .lote2 import BETABLOQ, ESPACIAR, OCLUSION, IMAO
from .lote3 import CORTICOIDE_OJO

CORTICOIDE_NARIZ = ['Infección localizada no tratada de la mucosa nasal (p. ej., herpes simple) (CIMA).',
                    'Cirugía o traumatismo nasal reciente, hasta que cicatrice (CIMA).']


def fichas():
    f = {}

    # ---------------------------------------------------------------- mometasona nasal
    c = lambda d: cima('mometasona', '61905', d)  # noqa: E731  Nasonex 50 mcg
    p = lambda d: ped('mometasona', d)  # noqa: E731
    f['mometasona'] = ficha(
        'mometasona', 'MOMETASONA', 'Mometasona nasal 50 mcg/dosis', 'corticoide-nasal',
        [pres('spray', '50 mcg por pulverización', 'nariz', 'F-22780/26', 'F-25024/24', 'F-28065/24', 'F-19862/23', 'F-15316/25', 'F-28612/24',
              'F-22337/25', 'F-25912/26', 'F-19277/22', 'F-2341/24', 'F-23560/22', 'F-20526/23', 'F-20095/23')],
        [dosis('Rinitis alérgica estacional o perenne', 'adulto',
               '2 pulverizaciones en cada fosa 1 vez al día (200 mcg); mantención 1 por fosa; máximo 4 por fosa al día',
               c('4.2.1: adultos y niños de 12 años y mayores, dos pulverizaciones en cada orificio nasal una vez al día'),
               cantidad=2, unidad='pulverizacion', veces_dia=1, sitio='fosa', condicion='Adultos y desde 12 años',
               tambien=[p('Adolescentes ≥12 años: dos aplicaciones (50 µg/dosis) en cada fosa nasal, una vez al día (200 µg/día)')]),
         dosis('Poliposis nasal', 'adulto', '2 pulverizaciones en cada fosa 1 vez al día; si no hay control a las 5–6 semanas, 2 por fosa 2 veces al día',
               c('4.2.1 Poliposis nasal'), cantidad=2, unidad='pulverizacion', veces_dia=1, sitio='fosa'),
         dosis('Rinitis alérgica', 'pediatrico', '1 pulverización en cada fosa 1 vez al día (100 mcg)',
               c('4.2.1: niños de 3 a 11 años, una pulverización en cada orificio nasal una vez al día'),
               cantidad=1, unidad='pulverizacion', veces_dia=1, sitio='fosa', condicion='3 a 11 años',
               tambien=[p('Niños de 3 a 11 años: una pulverización (50 µg) en cada orificio nasal una vez al día')])],
        pediatria=('con_dosis', 'Desde los 3 años (CIMA).', '3 años'),
        conservacion=conserv('Usar dentro de 2 meses desde la primera aplicación. Bajo 25 °C; no congelar.', c('6.3: utilizar dentro de los 2 meses desde la primera administración'), dias=60),
        administracion={'texto': 'Cebar la bomba antes del primer uso. Dirigir hacia la pared lateral de la nariz, no hacia el tabique.',
                        'fuente': p('Se debe administrar hacia el lateral de la cavidad nasal (no hacia el septo)')},
        contraindicaciones=CORTICOIDE_NARIZ,
    )

    # ---------------------------------------------------------------- mometasona + olopatadina
    c = lambda d: cima('mometasona-olopatadina', '86059', d)  # noqa: E731  Ryaltris 25/600
    f['mometasona-olopatadina'] = ficha(
        'mometasona-olopatadina', 'MOMETASONA + OLOPATADINA', 'Olopatadina + mometasona nasal', 'corticoide-nasal',
        [pres('spray', '600 mcg olopatadina + 25 mcg mometasona por pulverización', 'nariz', 'F-28399/24')],
        [dosis('Rinitis alérgica', 'adulto', '2 pulverizaciones en cada fosa 2 veces al día (mañana y noche)',
               c('4.2: adultos y adolescentes (12 años y mayores), dos pulverizaciones en cada orificio nasal dos veces al día'),
               cantidad=2, unidad='pulverizacion', veces_dia=2, sitio='fosa', condicion='Adultos y desde 12 años')],
        componentes=['Olopatadina', 'Mometasona'],
        pediatria=('no_establecida', 'No se recomienda en menores de 12 años (CIMA).', '12 años'),
        conservacion=conserv('Desechar 2 meses después del primer uso o al terminar las pulverizaciones de la etiqueta. No congelar.',
                             c('4.2/6.3: desechar en los 2 meses posteriores a la primera utilización'), dias=60),
        administracion={'texto': 'Solo nasal. Agitar 10 segundos antes de cada uso; cebar 6 veces la primera vez y 2 si lleva 14 días sin uso. Limpiar la boquilla.',
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=CORTICOIDE_NARIZ,
        discrepancias=[disc('Fuente pediátrica descargada', [('PEDIAMECUM-TOP-OLOPATADINA', 'Olopatadina en colirio (vía oftálmica)')],
                            'No se usa', 'Vía equivocada y componente aislado.')],
    )

    # ---------------------------------------------------------------- moxifloxacino
    c = lambda d: cima('moxifloxacino', '71576', d)  # noqa: E731  Vigamox 5 mg/ml
    f['moxifloxacino'] = ficha(
        'moxifloxacino', 'MOXIFLOXACINO', 'Moxifloxacino oftálmico 0,5 %', 'antibiotico',
        [pres('solucion', '0,5 %', 'ojo', 'F-21130/24', 'F-22365/25', 'F-15694/26', 'F-25812/25', 'F-21672/25', 'F-27866/23')],
        [dosis('Conjuntivitis bacteriana', 'adulto', '1 gota 3 veces al día; suele mejorar en 5 días y se sigue 2–3 días más',
               c('4.2: una gota 3 veces al día; continuar 2-3 días más tras mejorar'), cantidad=1, unidad='gota', veces_dia=3, sitio='ojo'),
         dosis('Conjuntivitis bacteriana', 'pediatrico', 'Igual que en adultos', c('4.2 Población pediátrica: no se requiere un ajuste de la dosis'),
               cantidad=1, unidad='gota', veces_dia=3, sitio='ojo')],
        pediatria=('con_dosis', 'No requiere ajuste en niños (CIMA).'),
        conservacion=conserv('Desechar 4 semanas después de abrir.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Solo vía oftálmica; no inyectar. Ocluir el conducto nasolagrimal 2–3 minutos, sobre todo en recién nacidos y niños. ' + ESPACIAR,
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a moxifloxacino u otras quinolonas (CIMA).'],
        alertas=['Si no mejora a los 5 días, reconsiderar el diagnóstico o el tratamiento (CIMA).'],
    )

    # ---------------------------------------------------------------- mupirocina nasal
    c = lambda d: cima('mupirocina', '59531', d)  # noqa: E731  Bactroban nasal 20 mg/g
    p = lambda d: ped('mupirocina', d)  # noqa: E731
    f['mupirocina'] = ficha(
        'mupirocina', 'MUPIROCINA', 'Mupirocina ungüento nasal 2 %', 'antibiotico',
        [pres('unguento', '2 %', 'nariz', 'F-22821/26', 'F-13363/23')],
        [dosis('Descolonización de Staphylococcus aureus nasal', 'adulto', 'Pequeña cantidad (cabeza de fósforo, ~30 mg) en cada fosa 2 o 3 veces al día',
               c('4.2: aplicar una pequeña cantidad en cada fosa nasal dos o tres veces al día'), veces_dia=3, sitio='fosa',
               duracion='La erradicación suele lograrse en 5–7 días',
               tambien=[p('Descolonización por SARM en portadores nasales: pequeña cantidad en cada fosa nasal 2-3 veces al día')]),
         dosis('Descolonización de Staphylococcus aureus nasal', 'pediatrico', 'Igual que en adultos; en lactantes, aplicar con una tórula',
               c('4.2: adultos y población pediátrica'), veces_dia=3, sitio='fosa',
               tambien=[p('Descolonización por SARM en portadores nasales: aplicar una pequeña cantidad en cada fosa nasal 2-3 veces al día')])],
        pediatria=('con_dosis', 'La ficha incluye a la población pediátrica.'),
        conservacion=conserv('Bajo 25 °C. Desechar lo que sobre al terminar.', c('6.4: conservar por debajo de 25 ºC; desechar el producto sobrante')),
        administracion={'texto': 'Poner la pomada en el meñique (o en una tórula en lactantes), aplicar en cada fosa y apretar varias veces las alas de la nariz.',
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a mupirocina o a algún excipiente (CIMA).'],
    )

    # ---------------------------------------------------------------- nafazolina
    d_ = lambda d: dm('nafazolina', d)  # noqa: E731
    p = lambda d: ped('nafazolina', d)  # noqa: E731
    baja = ['F-26855/22', 'F-635/23', 'F-23836/23', 'F-22543/26', 'F-25701/25', 'F-21476/24', 'F-20411/23', 'F-22542/26']
    f['nafazolina'] = ficha(
        'nafazolina', 'NAFAZOLINA', 'Nafazolina oftálmica', 'descongestionante',
        [pres('solucion', '0,012 %', 'ojo', *baja), pres('solucion', '0,1 %', 'ojo', 'F-17094/23')],
        [dosis('Enrojecimiento o irritación ocular leve', 'adulto', '1 o 2 gotas en el ojo afectado hasta 4 veces al día',
               d_('Directions: put 1 or 2 drops in the affected eye(s) up to 4 times daily'), cantidad=2, unidad='gota', veces_dia=4, sitio='ojo',
               presentaciones=['ojo-solucion-0-012'], condicion='Producto FDA de nafazolina con propilenglicol'),
         dosis('Enrojecimiento o irritación ocular leve', 'pediatrico', '1 o 2 gotas hasta 4 veces al día, cada 6 a 8 h',
               p('1 o 2 gotas hasta 4 veces al día, cada 6 a 8 horas; contraindicado en niños menores de 3 años'),
               cantidad=2, unidad='gota', veces_dia=4, sitio='ojo', presentaciones=['ojo-solucion-0-012'], estatus='off_label',
               condicion='Desde los 3 años; sin ficha técnica de la concentración', duracion='Reevaluar si sigue igual a los 3–4 días')],
        pediatria=('con_dosis', 'Contraindicada en menores de 3 años (Pediamécum).', '3 años'),
        conservacion=conserv('Conservar a 20–25 °C y cerrar bien tras usar.', d_('Storage: store at 20-25°C'), presentaciones=['ojo-solucion-0-012']),
        administracion={'texto': 'Lavarse las manos; dejar caer la gota sin tocar el ojo con la punta.', 'fuente': p('Administración')},
        contraindicaciones=['Glaucoma de ángulo estrecho o predisposición (Pediamécum).',
                            'Diabetes, enfermedad ocular grave, hipertensión o hipertiroidismo (Pediamécum).', 'Niños menores de 3 años (Pediamécum).'],
        alertas=['Ninguna fuente indica la concentración. La pauta se asocia a 0,012 %; la presentación de 0,1 % (Thrive) queda sin pauta.',
                 'Si a los 3–4 días sigue o empeora, reevaluar (Pediamécum).'],
        discrepancias=[disc('Producto de la fuente FDA',
                            [('DAILYMED-TOP-NAFAZOLINA', 'Gotas de nafazolina + propilenglicol (lubricante); no indica concentración')],
                            'Se usa solo para la frecuencia de adulto', 'La pauta coincide con la de Pediamécum; fuente débil.')],
    )

    # ---------------------------------------------------------------- nepafenaco
    c = lambda d: cima('nepafenaco', '07433001', d)  # noqa: E731  Nevanac 1 mg/ml
    f['nepafenaco'] = ficha(
        'nepafenaco', 'NEPAFENACO', 'Nepafenaco oftálmico 0,1 %', 'aine',
        [pres('suspension', '0,1 %', 'ojo', 'F-27299/23')],
        [dosis('Dolor e inflamación por cirugía de catarata', 'adulto',
               '1 gota 3 veces al día desde el día anterior a la cirugía, el mismo día y las 2 primeras semanas; 1 gota extra 30–120 min antes',
               c('4.2: 1 gota 3 veces al día; empezar el día anterior; 2 primeras semanas (hasta 3)'), cantidad=1, unidad='gota', veces_dia=3, sitio='ojo',
               duracion='2 semanas (hasta 3)'),
         dosis('Prevención del edema macular tras catarata en diabéticos', 'adulto', '1 gota 3 veces al día desde el día anterior y hasta 60 días después',
               c('4.2: pacientes diabéticos, hasta los 60 días del período postoperatorio'), cantidad=1, unidad='gota', veces_dia=3, sitio='ojo', duracion='Hasta 60 días')],
        pediatria=('no_establecida', 'No recomendado en niños y adolescentes; sin datos (CIMA).'),
        conservacion=conserv('Desechar 4 semanas después de abrir. Bajo 30 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Agitar bien; retirar el anillo del precinto. ' + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a otros AINE (CIMA).', 'Asma, urticaria o rinitis aguda desencadenadas por salicilatos u otros AINE (CIMA).'],
    )

    # ---------------------------------------------------------------- netilmicina
    c = lambda d: cima('netilmicina', '84965', d)  # noqa: E731  Netenax 3 mg/ml
    f['netilmicina'] = ficha(
        'netilmicina', 'NETILMICINA', 'Netilmicina oftálmica 0,3 %', 'antibiotico',
        [pres('solucion', '0,3 %', 'ojo', 'B-3058/24')],
        [dosis('Infección ocular externa bacteriana', 'adulto', '1 o 2 gotas en el saco conjuntival 3 veces al día', c('4.2: 1 o 2 gotas 3 veces al día'),
               cantidad=2, unidad='gota', veces_dia=3, sitio='ojo', duracion='Habitualmente 5 días')],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas de 3 a 18 años (CIMA).'),
        conservacion=conserv('Después de abrir: 28 días. Bajo 25 °C, protegido de la luz.', c('6.3: después de la primera apertura, 28 días'), dias=28),
        administracion={'texto': 'Enroscar el tapón hacia abajo para perforar la punta. Retirar lentes de contacto y esperar 15 minutos. '
                                 'Comprimir el saco lagrimal 1 minuto.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a netilmicina u otros aminoglucósidos (CIMA).'],
    )

    # ---------------------------------------------------------------- olopatadina
    c = lambda d: cima('olopatadina', '02217001', d)  # noqa: E731  Opatanol 1 mg/ml
    p = lambda d: ped('olopatadina', d)  # noqa: E731
    f['olopatadina'] = ficha(
        'olopatadina', 'OLOPATADINA', 'Olopatadina oftálmica', 'antialergico',
        [pres('solucion', '0,1 %', 'ojo', 'F-22927/26', 'F-720/23'),
         pres('solucion', '0,2 %', 'ojo', 'F-22948/26', 'F-29681/26', 'F-27809/23', 'F-24871/24', 'F-22309/25', 'F-29832/26', 'F-27399/23', 'F-15242/25', 'F-23073/26')],
        [dosis('Conjuntivitis alérgica estacional', 'adulto', '1 gota 2 veces al día (con 8 h de intervalo)', c('4.2: una gota dos veces al día (con un intervalo de 8 horas)'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', presentaciones=['ojo-solucion-0-1'], duracion='Hasta 4 meses si hace falta',
               tambien=[p('Uso oftálmico: una gota de colirio de olopatadina dos veces al día (con un intervalo de 8 horas)')]),
         dosis('Conjuntivitis alérgica estacional', 'pediatrico', '1 gota 2 veces al día (con 8 h de intervalo)',
               c('4.2: pacientes pediátricos de 3 años o mayores a la misma dosis que en adultos'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo',
               presentaciones=['ojo-solucion-0-1'], condicion='Desde los 3 años')],
        pediatria=('con_dosis', 'Desde los 3 años; sin datos en menores (CIMA).', '3 años'),
        conservacion=conserv('Desechar 4 semanas después de abrir.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28, presentaciones=['ojo-solucion-0-1']),
        administracion={'texto': ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a olopatadina o a algún excipiente (CIMA).'],
        discrepancias=[disc('Concentración 0,2 %',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: 0,1 % y 0,2 % (Patanol S y otros)'), ('CIMA-TOP-OLOPATADINA-02217001', 'CIMA: Opatanol 1 mg/ml (0,1 %)')],
                            'Pauta solo para 0,1 %', 'Regla de concentración: la de 0,2 % (en otros países, 1 vez al día) no tiene ficha descargada.')],
    )

    # ---------------------------------------------------------------- oximetazolina nasal
    c = lambda d: cima('oximetazolina', '41111', d)  # noqa: E731  Respir 0,5 mg/ml pulverización
    f['oximetazolina'] = ficha(
        'oximetazolina', 'OXIMETAZOLINA', 'Oximetazolina nasal 0,05 %', 'descongestionante',
        [pres('spray', '0,05 %', 'nariz', 'F-17530/24', 'F-27336/23'),
         pres('solucion', '0,05 %', 'nariz', 'F-12765/23', 'F-21969/25', 'F-15485/26', 'F-28549/24',
              nota='El nombre del registro no indica si es gota o pulverizador')],
        [dosis('Congestión nasal', 'adulto', '1 pulverización en cada fosa, máximo 2 veces al día (no repetir antes de 12 h)',
               c('4.2: adultos, adolescentes y niños mayores de 6 años, 1 pulverización en cada fosa nasal, máximo 2 veces al día'),
               cantidad=1, unidad='pulverizacion', veces_dia=2, sitio='fosa', presentaciones=['nariz-spray-0-05'], duracion='Suspender si a los 3 días sigue igual'),
         dosis('Congestión nasal', 'pediatrico', '1 pulverización en cada fosa, máximo 2 veces al día',
               c('4.2: niños mayores de 6 años; contraindicado en menores de 6 años'), cantidad=1, unidad='pulverizacion', veces_dia=2, sitio='fosa',
               presentaciones=['nariz-spray-0-05'], condicion='Mayores de 6 años')],
        pediatria=('con_dosis', 'Contraindicada en menores de 6 años (CIMA).', '6 años'),
        conservacion=conserv('Sin condiciones especiales. La ficha no fija validez tras abrir.', c('6.3/6.4'), presentaciones=['nariz-spray-0-05']),
        administracion={'texto': 'Cabeza erguida, boquilla en la fosa sin taparla, pulsar con firmeza. Mantener el frasco vertical.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Niños menores de 6 años (CIMA).', IMAO.replace(' o con antidepresivos que afectan la transmisión noradrenérgica (tricíclicos, mianserina)', ' o en las 2 semanas previas'),
                            'Glaucoma de ángulo estrecho; rinitis seca (CIMA).', 'Hipofisectomía transesfenoidal o cirugía con exposición de la duramadre (CIMA).'],
        alertas=['No más de 2 aplicaciones en 24 h ni intervalos menores de 12 h (CIMA).',
                 'Las soluciones nasales cuyo nombre no indica la forma (gota o pulverizador) quedan sin pauta.'],
    )

    # ---------------------------------------------------------------- pilocarpina
    c = lambda d: cima('pilocarpina', '10955', d)  # noqa: E731  Colircusí pilocarpina 20 mg/ml
    f['pilocarpina'] = ficha(
        'pilocarpina', 'PILOCARPINA', 'Pilocarpina oftálmica', 'antiglaucomatoso',
        [pres('solucion', '2 %', 'ojo', 'F-1167/23'), pres('solucion', '4 %', 'ojo', 'F-1168/23')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota hasta 4 veces al día según la presión y la respuesta',
               c('4.2: 1 gota hasta 4 veces al día'), cantidad=1, unidad='gota', veces_dia=4, sitio='ojo', presentaciones=['ojo-solucion-2']),
         dosis('Glaucoma agudo de ángulo cerrado', 'adulto', '1 gota hasta 3 veces en 30 minutos (junto con otras medidas hipotensoras)',
               c('4.2: dosis inicial de 1 gota hasta tres veces en un período de 30 minutos'), presentaciones=['ojo-solucion-2']),
         dosis('Miosis / profilaxis de PIO en cirugía láser', 'adulto', '1 o 2 gotas espaciadas 5 minutos (en láser, 15–60 min antes)',
               c('4.2: inducción de miosis; profilaxis de presión intraocular elevada en cirugía de láser'), presentaciones=['ojo-solucion-2'])],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas en niños (CIMA).'),
        conservacion=conserv('Desechar 4 semanas después de abrir. Bajo 25 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28, presentaciones=['ojo-solucion-2']),
        administracion={'texto': OCLUSION + 'Ocluir o cerrar 2 minutos. ' + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Iritis aguda o uveítis anterior (cuando la miosis no es deseable) (CIMA).', 'Glaucoma por bloqueo pupilar (CIMA).'],
        discrepancias=[disc('Concentración 4 %',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: 2 % y 4 %'), ('CIMA-TOP-PILOCARPINA-10955', 'CIMA: Colircusí pilocarpina 20 mg/ml (2 %)')],
                            'Pauta solo para 2 %', 'Regla de concentración.')],
    )

    # ---------------------------------------------------------------- prednisolona
    c = lambda d: cima('prednisolona', '62038', d)  # noqa: E731  Pred Forte 10 mg/ml
    f['prednisolona'] = ficha(
        'prednisolona', 'PREDNISOLONA', 'Prednisolona acetato oftálmica 1 %', 'corticoide',
        [pres('suspension', '1 %', 'ojo', 'F-22116/25', 'F-24979/24', 'FX-357/25', 'F-25859/25', 'F-22198/20', 'F-8553/26', 'F-25788/25', 'F-22874/26', 'F-16082/22')],
        [dosis('Inflamación ocular que responde a corticoides', 'adulto', '1 o 2 gotas 2 a 4 veces al día (puede aumentarse según indicación)',
               c('4.2: una o dos gotas de 2 a 4 veces al día'), cantidad=2, unidad='gota', veces_dia=4, sitio='ojo')],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas en niños (CIMA).'),
        conservacion=conserv('Una vez abierto, desechar a los 28 días. Bajo 25 °C; no congelar.', c('6.3: una vez abierto el envase, desechar a los 28 días'), dias=28),
        administracion={'texto': 'Agitar antes de usar. ' + OCLUSION + ESPACIAR, 'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=CORTICOIDE_OJO,
    )

    # ---------------------------------------------------------------- proparacaína
    d_ = lambda d: dm('proparacaina', d)  # noqa: E731  Alcaine 0,5 %
    f['proparacaina'] = ficha(
        'proparacaina', 'PROPARACAINA', 'Proparacaína oftálmica 0,5 %', 'anestesico',
        [pres('solucion', '0,5 %', 'ojo', 'F-2798/24', 'F-27237/22', 'F-26758/22', 'F-11855/22')],
        [dosis('Tonometría, retiro de cuerpo extraño o de suturas', 'adulto', '1 o 2 gotas en cada ojo antes del procedimiento',
               d_('Usual dosage: removal of foreign bodies and sutures, and for tonometry: 1 to 2 drops in each eye before operating'),
               cantidad=2, unidad='gota', sitio='ojo'),
         dosis('Procedimientos cortos de córnea y conjuntiva', 'adulto', '1 gota en cada ojo cada 5–10 minutos, 5 a 7 dosis',
               d_('Short corneal and conjunctival procedures: 1 drop in each eye every 5 to 10 minutes for 5 to 7 doses')),
         dosis('Tonometría, retiro de cuerpo extraño o de suturas', 'pediatrico', '1 o 2 gotas en cada ojo antes del procedimiento',
               d_('Pediatric use: safety and effectiveness in pediatric patients have been established'), cantidad=2, unidad='gota', sitio='ojo')],
        pediatria=('con_dosis', 'Seguridad y eficacia establecidas en pediatría (FDA).'),
        conservacion=conserv('Refrigerar a 2–8 °C en su caja (luz). Una vez abierto, usable hasta el vencimiento. Desechar si se oscurece.',
                             d_('Storage: store under refrigeration 2°C to 8°C; after opening can be used until the expiration date')),
        administracion={'texto': 'Uso en procedimientos por profesional. No tocar superficies con el gotero.', 'fuente': d_('Precaution')},
        contraindicaciones=['Hipersensibilidad a algún componente (FDA).'],
        alertas=['Cadena de frío: refrigerar (FDA, Alcaine).', 'Anestésico de uso en procedimiento: no es para tratamiento continuado.'],
    )

    # ---------------------------------------------------------------- tetrizolina
    c = lambda d: cima('tetrizolina', '69030', d)  # noqa: E731  Vispring 0,5 mg/ml unidosis
    p = lambda d: ped('tetrizolina', d)  # noqa: E731
    f['tetrizolina'] = ficha(
        'tetrizolina', 'TETRIZOLINA', 'Tetrizolina oftálmica 0,05 %', 'descongestionante',
        [pres('solucion', '0,05 %', 'ojo', 'F-1830/24')],
        [dosis('Irritación ocular menor', 'adulto', '1 o 2 gotas 2 o 3 veces al día según necesidad; máximo 4 veces al día',
               c('4.2: adultos y niños mayores de 6 años, 1 ó 2 gotas 2 o 3 veces al día, hasta un máximo de 4 veces al día'),
               cantidad=2, unidad='gota', veces_dia=4, sitio='ojo', duracion='Máximo 72 horas (Pediamécum; la ficha técnica permite hasta 1 semana)',
               tambien=[p('1 o 2 gotas por aplicación, 2-3 veces al día, máximo 4 veces al día')]),
         dosis('Irritación ocular menor', 'pediatrico', '1 o 2 gotas 2 o 3 veces al día; máximo 4 veces al día',
               c('4.2: niños mayores de 6 años; de 2 a 6 años solo bajo estricto control médico; menores de 2 años contraindicado'),
               cantidad=2, unidad='gota', veces_dia=4, sitio='ojo', condicion='Mayores de 6 años (de 2 a 6, solo con control médico)',
               duracion='Máximo 72 horas', tambien=[p('El tratamiento no debe continuar más de 72 horas')])],
        alto_riesgo=False,
        pediatria=('con_dosis', 'Contraindicada en menores de 2 años; de 2 a 6 años solo bajo estricto control médico (CIMA).', '6 años'),
        conservacion=conserv('Ficha de unidosis: desechar después de cada uso. Bajo 25 °C.', c('4.2/6.4: desechar el envase después de cada uso')),
        contraindicaciones=['Niños menores de 2 años (CIMA).', 'Glaucoma de ángulo estrecho (CIMA).',
                            'Enfermedad cardiovascular grave, feocromocitoma, hipertiroidismo o diabetes (CIMA).',
                            'Tratamiento con IMAO u otros fármacos que suben la presión arterial (CIMA).'],
        alertas=['Si no alivia en 48 h, o el enrojecimiento aumenta o persiste, suspender y consultar (CIMA).'],
        discrepancias=[disc('Duración máxima',
                            [('CIMA-TOP-TETRIZOLINA-69030', 'Nunca más de una semana'), ('PEDIAMECUM-TOP-TETRIZOLINA', 'No más de 72 horas')],
                            'Máximo 72 horas', 'Se muestra la cifra más baja: es el mismo régimen y la misma población.')],
    )

    # ---------------------------------------------------------------- timolol
    c = lambda d: cima('timolol', '55236', d)  # noqa: E731  Timoftol 5 mg/ml
    p = lambda d: ped('timolol', d)  # noqa: E731
    f['timolol'] = ficha(
        'timolol', 'TIMOLOL', 'Timolol oftálmico 0,5 %', 'antiglaucomatoso',
        [pres('solucion', '0,5 %', 'ojo', 'F-9066/26', 'F-29551/26', 'F-22975/26', 'F-22085/25', 'F-27289/23', 'F-20039/23', 'F-5546/25')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota de 0,5 % en el ojo afectado 2 veces al día; si la presión se controla, puede bastar 1 vez al día',
               c('4.2: si la respuesta no es suficiente, una gota de TIMOFTOL 5 mg/ml dos veces al día; luego puede pasarse a una vez al día'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo',
               condicion='La ficha inicia con 0,25 %, que no está registrado en Chile como monofármaco',
               tambien=[p('1 gota al 0,25% cada 12 horas y, si no hay respuesta, 1 gota al 0,5% cada 12 horas')]),
         dosis('Glaucoma congénito o juvenil, de forma transitoria', 'pediatrico',
               'La concentración más baja disponible, 1 vez al día; si no controla, hasta 2 gotas al día por ojo (cada 12 h)',
               c('4.2 Población pediátrica: uso transitorio; menor concentración disponible, solamente una vez al día; máximo dos gotas por día'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo', condicion='En Chile solo hay 0,5 %; Pediamécum considera suficiente 0,1 % en niños',
               tambien=[p('Concentración más baja disponible, 1 vez al día; máximo de 2 gotas diarias; observar 1-2 h a neonatos')])],
        alto_riesgo=True,
        pediatria=('con_dosis', 'Solo transitorio en glaucoma congénito o juvenil, con historia y examen previos; observar 1–2 h tras la primera dosis, '
                                'sobre todo a neonatos (CIMA, Pediamécum).'),
        conservacion=conserv('Tras la primera apertura: un mes (la calculadora usa 28 días). Bajo 25 °C, protegido de la luz.', c('6.3: tras la primera apertura, un mes'), dias=28),
        administracion={'texto': 'Separar al menos 10 minutos de otros colirios. No usar dos betabloqueantes tópicos a la vez.', 'fuente': c('4.2 Posología')},
        contraindicaciones=['Hipersensibilidad a otros betabloqueantes (CIMA).'] + BETABLOQ + ['Distrofia corneal; rinitis alérgica grave e hiperreactividad bronquial (CIMA).'],
    )

    # ---------------------------------------------------------------- timolol + travoprost
    c = lambda d: cima('timolol-travoprost', '106338004', d)  # noqa: E731  DuoTrav 40 mcg + 5 mg/ml
    f['timolol-travoprost'] = ficha(
        'timolol-travoprost', 'TIMOLOL + TRAVOPROST', 'Travoprost + timolol oftálmico', 'antiglaucomatoso',
        [pres('solucion', NC, 'ojo', 'F-15433/26', 'F-17825/25')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 1 vez al día, siempre a la misma hora (no más)',
               c('4.2: una gota una vez al día por la mañana o por la noche; no sobrepasar una gota diaria'), cantidad=1, unidad='gota', veces_dia=1, sitio='ojo')],
        componentes=['Travoprost', 'Timolol'],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas en menores de 18 años; sin datos (CIMA).'),
        conservacion=conserv('Desechar 4 semanas después de abrir. Bajo 30 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Retirar el envoltorio protector antes del primer uso. Retirar lentes blandos y esperar 15 minutos. Ocluir o cerrar 2 minutos. ' + ESPACIAR,
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a otros betabloqueantes (CIMA).'] + BETABLOQ + ['Rinitis alérgica grave y distrofias corneales (CIMA).'],
        alertas=['DuoTrav es 40 mcg/ml + 5 mg/ml; los registros chilenos no indican concentración en el nombre.'],
    )

    # ---------------------------------------------------------------- tobramicina
    c = lambda d: cima('tobramicina', '57593', d)  # noqa: E731  Tobrex ungüento 3 mg/g
    f['tobramicina'] = ficha(
        'tobramicina', 'TOBRAMICINA', 'Tobramicina oftálmica 0,3 %', 'antibiotico',
        [pres('unguento', '0,3 %', 'ojo', 'B-2368/24', 'B-2807/25', 'B-2803/22'),
         pres('solucion', '0,3 %', 'ojo', 'B-2369/23', 'B-3075/25', 'B-2630/26', 'B-1261/26', 'B-2808/25', 'B-2802/22')],
        [dosis('Infección leve o moderada', 'adulto', '1 cm de pomada 2 o 3 veces al día', c('4.2: infecciones leves o moderadas, 1 cm de pomada dos o tres veces al día'),
               cantidad=1, unidad='cm', veces_dia=3, sitio='ojo', presentaciones=['ojo-unguento-0-3']),
         dosis('Infección grave', 'adulto', '1 cm de pomada cada 3–4 h hasta mejorar; luego espaciar', c('4.2: infecciones graves, 1 cm cada tres o cuatro horas'),
               cantidad=1, unidad='cm', sitio='ojo', presentaciones=['ojo-unguento-0-3']),
         dosis('Infección leve o moderada', 'pediatrico', 'Igual que en adultos', c('4.2 Población pediátrica: adolescentes y niños de 1 año y mayores, misma dosis'),
               cantidad=1, unidad='cm', veces_dia=3, sitio='ojo', presentaciones=['ojo-unguento-0-3'], condicion='Desde 1 año')],
        pediatria=('con_dosis', 'Desde 1 año; no establecida en menores (CIMA).', '1 año'),
        conservacion=conserv('Desechar 4 semanas después de abrir. Bajo 25 °C.', c('6.3: desechar cuatro semanas después de la primera apertura'), dias=28,
                             presentaciones=['ojo-unguento-0-3']),
        administracion={'texto': 'Aplicar al final si se usan colirios. No tocar el ojo con la punta del tubo.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a tobramicina o a algún excipiente (CIMA).'],
        alertas=['Con aminoglucósidos sistémicos a la vez, vigilar niveles séricos (CIMA).', 'La solución 0,3 % no tiene ficha técnica en las fuentes consultadas: sin pauta.'],
    )

    # ---------------------------------------------------------------- travoprost
    c = lambda d: cima('travoprost', '101199003', d)  # noqa: E731  Travatan 40 mcg/ml
    f['travoprost'] = ficha(
        'travoprost', 'TRAVOPROST', 'Travoprost oftálmico 0,004 %', 'antiglaucomatoso',
        [pres('solucion', '0,004 %', 'ojo', 'F-17796/24', 'F-25563/25', 'F-22122/25', 'F-23473/22', 'F-25612/25', 'F-9089/26', 'F-24800/24', 'F-29697/26')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota 1 vez al día, de preferencia por la noche (no más)',
               c('4.2: una gota una vez al día; efecto óptimo por la noche; no sobrepasar una gota diaria'), cantidad=1, unidad='gota', veces_dia=1, sitio='ojo'),
         dosis('Glaucoma pediátrico', 'pediatrico', 'Igual que en adultos: 1 gota 1 vez al día',
               c('4.2: pacientes pediátricos desde los 2 meses a <18 años con la misma posología; datos limitados de 2 meses a 3 años'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo', condicion='Desde los 2 meses (datos limitados hasta los 3 años)')],
        pediatria=('con_dosis', 'Desde los 2 meses; datos limitados entre 2 meses y 3 años (CIMA).', '2 meses'),
        conservacion=conserv('Desechar 4 semanas después de abrir.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Retirar el envoltorio protector antes del primer uso. ' + OCLUSION + ESPACIAR, 'fuente': c('4.2')},
        contraindicaciones=['Hipersensibilidad a travoprost o a algún excipiente (CIMA).'],
        alertas=['No requiere ajuste en insuficiencia hepática o renal (CIMA).'],
    )

    # ---------------------------------------------------------------- tropicamida
    c = lambda d: cima('tropicamida', '57050', d)  # noqa: E731  Colirofta tropicamida 10 mg/ml
    p = lambda d: ped('tropicamida', d)  # noqa: E731
    f['tropicamida'] = ficha(
        'tropicamida', 'TROPICAMIDA', 'Tropicamida oftálmica 1 %', 'midriatico',
        [pres('solucion', '1 %', 'ojo', 'F-27161/22', 'F-28820/25', 'F-1180/23', 'F-22314/25')],
        [dosis('Midriasis para examen', 'adulto', '1 o 2 gotas; repetir a los 5 minutos. Si el examen se atrasa 20–30 min, 1 gota más',
               c('4.2 Uso en adultos: 1 o 2 gotas, repetir al cabo de 5 minutos'), cantidad=2, unidad='gota', sitio='ojo'),
         dosis('Midriasis para examen', 'pediatrico', '1 gota y repetir a los 5 minutos; explorar a los 15 minutos',
               p('Tópica oftálmica: 1 gota y repetir a los 5 minutos. Explorar a los 15 minutos'), cantidad=1, unidad='gota', sitio='ojo',
               condicion='No recomendada al 1 % en recién nacidos y lactantes (CIMA)', estatus='autorizada',
               tambien=[c('4.2 Población pediátrica: precaución; dosis eficaz más baja')])],
        alto_riesgo=True,
        pediatria=('con_dosis', 'Con precaución; al 1 % no se recomienda en recién nacidos ni lactantes (CIMA).'),
        conservacion=conserv('Desechar 4 semanas después de abrir. Bajo 25 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Ocluir el conducto nasolagrimal al menos 2 minutos. Precaución en ojos inflamados (más absorción). ' + ESPACIAR,
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Glaucoma de ángulo estrecho conocido o sospechado (CIMA).'],
        alertas=['Ancianos y presión intraocular elevada: precaución (CIMA).'],
    )
    return f
