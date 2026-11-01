"""Tópicos, lote 2: betametasona → dexametasona + levofloxacino."""
from .comun import NC, cima, conserv, disc, dm, dosis, ficha, isp, ped, pres
from .lote1 import SIN_COMBO

OCLUSION = 'Tras instilar, cerrar suavemente los ojos u ocluir el conducto nasolagrimal para reducir la absorción sistémica. '
ESPACIAR = 'Espaciar al menos 5 minutos de otros colirios; las pomadas al final. No tocar el ojo con la punta del frasco.'
BETABLOQ = ['Asma bronquial o antecedente de asma, EPOC grave (CIMA).',
            'Bradicardia sinusal, síndrome del seno enfermo, bloqueo sinoauricular o AV de 2.º–3.er grado sin marcapasos (CIMA).',
            'Insuficiencia cardiaca manifiesta o shock cardiogénico (CIMA).']
IMAO = 'En tratamiento con IMAO o con antidepresivos que afectan la transmisión noradrenérgica (tricíclicos, mianserina) (CIMA).'
SIN_FUENTE_SOLA = ('Ninguna fuente consultada trae la posología de esta presentación por vía oftálmica: Pediamécum solo describe '
                   'la betametasona inyectable y cutánea, y CIMA y DailyMed no tienen ficha.')


def fichas():
    f = {}

    # ---------------------------------------------------------------- betametasona sola y combinaciones chilenas
    ped('betametasona', 'Solo vía sistémica y cutánea; sin pauta oftálmica')
    f['betametasona'] = ficha(
        'betametasona', 'BETAMETASONA', 'Betametasona oftálmica', 'corticoide',
        [pres('solucion', NC, 'ojo', 'F-2376/24')], [],
        pediatria=('sin_datos', 'Sin fuente de posología oftálmica.'), sin_pauta=SIN_FUENTE_SOLA,
        discrepancias=[disc('Fuente pediátrica descargada', [('PEDIAMECUM-TOP-BETAMETASONA', 'Betametasona inyectable y cutánea')],
                            'No se usa', 'Vía equivocada: no informa sobre la solución oftálmica.')],
    )
    for id_, mol, nombre, comps, pres_ in [
        ('betametasona-gentamicina', 'BETAMETASONA + GENTAMICINA', 'Betametasona + gentamicina oftálmica', ['Betametasona', 'Gentamicina'],
         [pres('unguento', NC, 'ojo', 'B-887/25'), pres('solucion', NC, 'ojo', 'B-886/25')]),
        ('betametasona-neomicina', 'BETAMETASONA + NEOMICINA', 'Betametasona + neomicina oftálmica', ['Betametasona', 'Neomicina'],
         [pres('unguento', NC, 'ojo', 'B-890/25'), pres('solucion', NC, 'ojo', 'B-520/24')]),
        ('betametasona-neomicina-polimixina-b', 'BETAMETASONA + NEOMICINA + POLIMIXINA B', 'Betametasona + neomicina + polimixina B ótica',
         ['Betametasona', 'Neomicina', 'Polimixina B'], [pres('solucion', NC, 'oido', 'B-891/25')]),
    ]:
        alertas = (['Neomicina (Pediamécum): con filtrado glomerular <10 ml/min no usarla por vía oral ni tópica.']
                   if 'Neomicina' in comps else [])
        f[id_] = ficha(id_, mol, nombre, 'antibiotico-corticoide', pres_, [], componentes=comps,
                       pediatria=('sin_datos', 'Sin fuente de posología para la combinación.'), sin_pauta=SIN_COMBO, alertas=alertas)

    # ---------------------------------------------------------------- betaxolol (concentración distinta)
    c = lambda d: cima('betaxolol', '61015', d)  # noqa: E731  Betoptic suspensión 2,5 mg/ml
    f['betaxolol'] = ficha(
        'betaxolol', 'BETAXOLOL', 'Betaxolol oftálmico 0,5 %', 'antiglaucomatoso',
        [pres('solucion', '0,5 %', 'ojo', 'F-5522/25', 'F-8873/26')], [],
        pediatria=('no_establecida', 'Sin fuente para la concentración chilena; la ficha de 0,25 % no establece seguridad ni eficacia en niños.'),
        sin_pauta='En Chile está registrado al 0,5 % (solución); la única ficha disponible es de betaxolol 0,25 % en suspensión '
                  '(Betoptic, CIMA). Por la regla de concentración no se muestra su pauta.',
        contraindicaciones=['Hipersensibilidad a betaxolol u otros betabloqueantes (CIMA).'] + BETABLOQ,
        discrepancias=[disc('Concentración',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: solución oftálmica 0,5 % (5 mg/ml)'),
                             (c('4.2: suspensión 2,5 mg/ml')['ref'], 'CIMA: suspensión 0,25 % (2,5 mg/ml), 1–2 gotas 2 veces al día')],
                            'Sin pauta', 'Decisión de Héctor (31-oct): la ficha se ata a la concentración registrada en Chile.')],
    )

    # ---------------------------------------------------------------- bimatoprost
    c = lambda d: cima('bimatoprost', '02205003', d)  # noqa: E731  Lumigan 0,1 mg/ml
    f['bimatoprost'] = ficha(
        'bimatoprost', 'BIMATOPROST', 'Bimatoprost oftálmico', 'antiglaucomatoso',
        [pres('solucion', '0,01 %', 'ojo', 'F-18052/25'),
         pres('solucion', '0,03 %', 'ojo', 'F-28684/25', 'F-27211/22', 'F-27977/23', 'F-26442/26', 'F-28685/25', 'F-27202/22', 'F-9090/26'),
         pres('gel', '0,1 mg/g', 'ojo', 'F-29759/26')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 1 vez al día, por la noche',
               c('4.2: una gota en el ojo(s) afectado(s), una vez al día por la noche; no exceder de una vez al día'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo', presentaciones=['ojo-solucion-0-01'])],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas de 0 a 18 años (CIMA).'),
        conservacion=conserv('4 semanas después de abrir. Sin condiciones especiales de conservación.',
                             c('6.3: 4 semanas después que se haya abierto por primera vez'), dias=28, presentaciones=['ojo-solucion-0-01']),
        administracion={'texto': 'Más de 1 vez al día puede reducir el efecto. Espaciar al menos 5 minutos de otros colirios.',
                        'fuente': c('4.2 Posología y forma de administración')},
        contraindicaciones=['Reacción previa al cloruro de benzalconio que obligó a suspender (Lumigan 0,1 mg/ml, CIMA).'],
        alertas=['Precaución en insuficiencia renal o hepática moderada a grave (no estudiado, CIMA).'],
        discrepancias=[disc('Concentraciones sin ficha',
                            [('ISP-REGISTRO-TOPICOS', 'Chile también registra solución 0,03 % (0,3 mg/ml) y gel 0,1 mg/g'),
                             ('CIMA-TOP-BIMATOPROST-02205003', 'Ficha descargada: Lumigan 0,1 mg/ml (0,01 %)')],
                            'Pauta solo para 0,01 %', 'La pauta se ata a la concentración de la ficha; 0,03 % y gel quedan sin pauta.')],
    )

    # ---------------------------------------------------------------- Triplenex
    f['bimatoprost-brimonidina-timolol'] = ficha(
        'bimatoprost-brimonidina-timolol', 'BIMATOPROST + BRIMONIDINA + TIMOLOL', 'Bimatoprost + brimonidina + timolol oftálmico',
        'antiglaucomatoso', [pres('solucion', NC, 'ojo', 'F-23487/22')], [],
        componentes=['Bimatoprost', 'Brimonidina', 'Timolol'], alto_riesgo=True,
        pediatria=('sin_datos', 'Sin fuente para la combinación. Sus componentes brimonidina y timolol tienen riesgo sistémico grave en lactantes.'),
        sin_pauta=SIN_COMBO,
    )

    # ---------------------------------------------------------------- bimatoprost + timolol
    c = lambda d: cima('bimatoprost-timolol', '06340001', d)  # noqa: E731  Ganfort 0,3 + 5 mg/ml
    f['bimatoprost-timolol'] = ficha(
        'bimatoprost-timolol', 'BIMATOPROST + TIMOLOL', 'Bimatoprost + timolol oftálmico', 'antiglaucomatoso',
        [pres('solucion', NC, 'ojo', 'F-29877/26', 'F-27712/23', 'F-16196/22', 'F-28122/24')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 1 vez al día, siempre a la misma hora (mañana o noche)',
               c('4.2: una gota una vez al día bien por la mañana o bien por la noche; no exceder de una gota una vez al día'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo')],
        componentes=['Bimatoprost', 'Timolol'],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas de 0 a 18 años; sin datos (CIMA).'),
        conservacion=conserv('Usar dentro de 28 días tras abrir (a 25 °C).', c('6.3: estabilidad en uso hasta 28 días a 25 ºC'), dias=28),
        administracion={'texto': OCLUSION + 'Ocluir o cerrar los párpados 2 minutos. ' + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=BETABLOQ,
        alertas=['Ganfort es 0,3 mg/ml + 5 mg/ml; los registros chilenos no indican concentración en el nombre: verificar el envase.'],
    )

    # ---------------------------------------------------------------- brimonidina
    c = lambda d: cima('brimonidina', '62010', d)  # noqa: E731  Alphagan 2 mg/ml
    f['brimonidina'] = ficha(
        'brimonidina', 'BRIMONIDINA', 'Brimonidina oftálmica', 'antiglaucomatoso',
        [pres('solucion', '0,2 %', 'ojo', 'F-12304/22', 'F-23254/21', 'F-25575/25', 'F-25743/25', 'F-28518/24', 'F-11880/22'),
         pres('solucion', '0,15 %', 'ojo', 'F-12327/22', 'F-28236/24'),
         pres('solucion', NC, 'ojo', 'FX-328/24')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 2 veces al día, cada 12 h aprox.',
               c('4.2: una gota dos veces al día, con un intervalo de aproximadamente 12 horas'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', presentaciones=['ojo-solucion-0-2'])],
        alto_riesgo=True,
        pediatria=('contraindicada', 'Contraindicada en menores de 2 años (reacciones graves en neonatos); no recomendada en menores de 12 años (CIMA).', '12 años'),
        conservacion=conserv('Tras la primera apertura: 28 días. No conservar sobre 25 °C.', c('6.3: tras la primera apertura 28 días'), dias=28,
                             presentaciones=['ojo-solucion-0-2']),
        administracion={'texto': 'Inmediatamente después de cada gota, presionar el saco lagrimal en el canto interno 1 minuto. '
                                 'Separar 5–15 minutos de otros colirios. No tocar superficies con el gotero.',
                        'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Neonatos y niños menores de 2 años (CIMA).', IMAO],
        alertas=['Sin datos en insuficiencia renal o hepática (CIMA).'],
        discrepancias=[disc('Concentración 0,15 %',
                            [('ISP-REGISTRO-TOPICOS', 'Chile también registra 0,15 % (Alphagan P y genérico)'),
                             ('CIMA-TOP-BRIMONIDINA-62010', 'Ficha descargada: Alphagan 2 mg/ml (0,2 %)')],
                            'Pauta solo para 0,2 %', 'La pauta se ata a la concentración de la ficha; 0,15 % y el registro sin concentración quedan sin pauta.')],
    )

    # ---------------------------------------------------------------- brimonidina + brinzolamida
    c = lambda d: cima('brimonidina-brinzolamida', '114933001', d)  # noqa: E731  Simbrinza
    f['brimonidina-brinzolamida'] = ficha(
        'brimonidina-brinzolamida', 'BRIMONIDINA + BRINZOLAMIDA', 'Brinzolamida + brimonidina oftálmica', 'antiglaucomatoso',
        [pres('suspension', NC, 'ojo', 'F-21735/25')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 2 veces al día',
               c('4.2: una gota de SIMBRINZA dos veces al día en el ojo(s) afectado(s)'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo')],
        componentes=['Brinzolamida', 'Brimonidina'], alto_riesgo=True,
        pediatria=('contraindicada', 'Contraindicada en menores de 2 años; sin datos de 2 a 17 años (CIMA).'),
        conservacion=conserv('4 semanas tras la primera apertura.', c('6.3: 4 semanas tras la primera apertura del envase'), dias=28),
        administracion={'texto': 'Agitar bien antes de usar. ' + OCLUSION + 'Ocluir 2 minutos. ' + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a las sulfonamidas (CIMA).', IMAO, 'Insuficiencia renal grave (ClCr <30 ml/min) o acidosis hiperclorémica (CIMA).',
                            'Neonatos y niños menores de 2 años (CIMA).'],
        alertas=['Simbrinza es 10 mg/ml + 2 mg/ml; el registro chileno no indica concentración en el nombre.', 'Precaución en insuficiencia hepática (CIMA).'],
    )

    # ---------------------------------------------------------------- Krytantek / Tiof Max
    f['brimonidina-dorzolamida-timolol'] = ficha(
        'brimonidina-dorzolamida-timolol', 'BRIMONIDINA + DORZOLAMIDA + TIMOLOL', 'Brimonidina + dorzolamida + timolol oftálmico',
        'antiglaucomatoso', [pres('solucion', NC, 'ojo', 'F-28388/24', 'FX-331/24', 'F-29811/26')], [],
        componentes=['Brimonidina', 'Dorzolamida', 'Timolol'], alto_riesgo=True,
        pediatria=('sin_datos', 'Sin fuente para la combinación. Brimonidina está contraindicada en menores de 2 años.'),
        sin_pauta=SIN_COMBO,
    )

    # ---------------------------------------------------------------- brimonidina + timolol
    c = lambda d: cima('brimonidina-timolol', '67438', d)  # noqa: E731  Combigan 2 + 5 mg/ml
    f['brimonidina-timolol'] = ficha(
        'brimonidina-timolol', 'BRIMONIDINA + TIMOLOL', 'Brimonidina + timolol oftálmico', 'antiglaucomatoso',
        [pres('solucion', '0,2 % + 0,5 %', 'ojo', 'F-28836/25', 'F-26445/26', 'F-28290/24'),
         pres('solucion', NC, 'ojo', 'FX-325/24', 'F-20015/23', 'F-15423/26')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 2 veces al día, con unas 12 h de diferencia',
               c('4.2.1: una gota dos veces al día, con 12 horas de diferencia aproximadamente'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo')],
        componentes=['Brimonidina', 'Timolol'], alto_riesgo=True,
        pediatria=('contraindicada', 'Contraindicada en menores de 2 años; no recomendada de 2 a 17 años (CIMA).'),
        conservacion=conserv('Usar dentro de 28 días tras abrir. Mantener en la caja (luz).', c('6.3: después de la primera apertura, usar en el transcurso de 28 días'), dias=28),
        administracion={'texto': 'Presionar el saco lagrimal o cerrar los ojos 2 minutos inmediatamente después de cada gota. ' + ESPACIAR,
                        'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=BETABLOQ + ['Neonatos y niños menores de 2 años (CIMA).', IMAO],
        alertas=['Combigan es 2 mg/ml + 5 mg/ml (0,2 % + 0,5 %): igual a los registros chilenos que indican concentración.'],
    )

    # ---------------------------------------------------------------- brinzolamida
    c = lambda d: cima('brinzolamida', '00129001', d)  # noqa: E731  Azopt 10 mg/ml
    f['brinzolamida'] = ficha(
        'brinzolamida', 'BRINZOLAMIDA', 'Brinzolamida oftálmica 1 %', 'antiglaucomatoso',
        [pres('suspension', '1 %', 'ojo', 'F-1798/24', 'F-27002/22')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto',
               '1 gota en el ojo afectado 2 veces al día; algunos pacientes, 3 veces al día (máximo 1 gota 3 veces al día)',
               c('4.2: una gota dos veces al día; algunos pacientes pueden responder mejor con una gota tres veces al día'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo')],
        pediatria=('no_establecida', 'No se recomienda de 0 a 17 años (CIMA).'),
        conservacion=conserv('4 semanas después de la primera apertura.', c('6.3: 4 semanas después de la primera apertura del envase'), dias=28),
        administracion={'texto': 'Agitar bien antes de usar; retirar el anillo del precinto. ' + OCLUSION + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a las sulfonamidas (CIMA).', 'Insuficiencia renal grave o acidosis hiperclorémica (CIMA).'],
        alertas=['No se recomienda en insuficiencia hepática (no estudiado, CIMA).'],
    )

    # ---------------------------------------------------------------- brinzolamida + timolol
    c = lambda d: cima('brinzolamida-timolol', '08482001', d)  # noqa: E731  Azarga 10 + 5 mg/ml
    f['brinzolamida-timolol'] = ficha(
        'brinzolamida-timolol', 'BRINZOLAMIDA + TIMOLOL', 'Brinzolamida + timolol oftálmico', 'antiglaucomatoso',
        [pres('suspension', NC, 'ojo', 'F-17777/24', 'F-24628/24', 'F-27001/22', 'F-28625/24')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 2 veces al día (no sobrepasar)',
               c('4.2: una gota dos veces al día; la dosis no debe sobrepasar de una gota dos veces al día'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo')],
        componentes=['Brinzolamida', 'Timolol'],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas de 0 a 18 años; sin datos (CIMA).'),
        conservacion=conserv('4 semanas después de la primera apertura.', c('6.3: 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Agitar bien antes de usar. ' + OCLUSION + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a otros betabloqueantes o a sulfonamidas (CIMA).'] + BETABLOQ +
                           ['Rinitis alérgica grave, acidosis hiperclorémica, insuficiencia renal grave (CIMA).'],
        alertas=['Azarga es 10 mg/ml + 5 mg/ml; los registros chilenos no indican concentración en el nombre.'],
    )

    # ---------------------------------------------------------------- bromfenaco
    c = lambda d: cima('bromfenaco', '11692001', d)  # noqa: E731  Yellox 0,9 mg/ml
    f['bromfenaco'] = ficha(
        'bromfenaco', 'BROMFENACO', 'Bromfenaco oftálmico 0,09 %', 'aine',
        [pres('solucion', '0,09 %', 'ojo', 'F-23567/22')],
        [dosis('Inflamación tras cirugía de catarata', 'adulto', '1 gota en el ojo operado 2 veces al día, desde el día siguiente a la cirugía',
               c('4.2: una gota dos veces al día, desde el día siguiente a la cirugía, durante las primeras 2 semanas'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', duracion='2 semanas como máximo (sin datos de seguridad más allá)')],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas en niños; sin datos (CIMA).'),
        conservacion=conserv('Tras la primera apertura: 4 semanas. No conservar sobre 25 °C.', c('6.3: tras la primera apertura 4 semanas'), dias=28),
        administracion={'texto': ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a bromfenaco u otros AINE (CIMA).',
                            'Asma, urticaria o rinitis aguda desencadenadas por ácido acetilsalicílico u otros AINE (CIMA).'],
    )

    # ---------------------------------------------------------------- budesonida
    c = lambda d: cima('budesonida', '59533', d)  # noqa: E731  Budesonida Alcon (50 y 100 mcg/dosis)
    p = lambda d: ped('budesonida', d)  # noqa: E731
    f['budesonida'] = ficha(
        'budesonida', 'BUDESONIDA', 'Budesonida nasal 100 mcg/dosis', 'corticoide-nasal',
        [pres('spray', '100 mcg por pulverización', 'nariz', 'F-23599/22', 'F-15899/22')],
        [dosis('Rinitis', 'adulto', '2 pulverizaciones (200 mcg) en cada fosa nasal por la mañana (total 400 mcg); al mejorar, 1 pulverización por fosa al día (200 mcg)',
               c('4.2.1 Budesonida Alcon 100 mcg/dosis: dos aplicaciones (200 mcg) en cada fosa nasal, por la mañana (total 400 mcg)'),
               cantidad=2, unidad='pulverizacion', veces_dia=1, sitio='fosa',
               tambien=[p('Budesonida 100 µg/dosis: 2 aplicaciones (200 µg) en cada fosa nasal, por la mañana (total: 400 µg)')]),
         dosis('Rinitis', 'pediatrico', '2 pulverizaciones en cada fosa nasal por la mañana; al mejorar, 1 por fosa al día',
               c('4.2.1: adultos y niños a partir de 6 años'), cantidad=2, unidad='pulverizacion', veces_dia=1, sitio='fosa',
               condicion='Desde los 6 años',
               tambien=[p('Dosis nasal usual en niños a partir de 6 años; budesonida 100 µg/dosis')])],
        pediatria=('con_dosis', 'No establecida en menores de 6 años (Pediamécum, CIMA).', '6 años'),
        conservacion=conserv('Sin condiciones especiales. La ficha no fija una validez tras abrir.', c('6.3/6.4: validez 2 años; sin condiciones especiales')),
        administracion={'texto': 'Antes del primer uso, cargar la válvula. Limpiar la nariz, agitar, inclinar la cabeza hacia adelante, tapar la otra fosa, '
                                 'inspirar y pulsar. Respirar por la boca.', 'fuente': c('4.2.2 Instrucciones de uso')},
        contraindicaciones=['Hipersensibilidad a budesonida o a algún excipiente (CIMA).'],
        alertas=['En pólipos nasales la dosis diaria puede subir hasta 800 mcg (CIMA).'],
    )

    # ---------------------------------------------------------------- ciclopentolato
    c = lambda d: cima('ciclopentolato', '42117', d)  # noqa: E731  Colirofta ciclopléjico 10 mg/ml
    p = lambda d: ped('ciclopentolato', d)  # noqa: E731
    f['ciclopentolato'] = ficha(
        'ciclopentolato', 'CICLOPENTOLATO', 'Ciclopentolato oftálmico 1 %', 'midriatico',
        [pres('solucion', '1 %', 'ojo', 'F-22302/25', 'F-29430/26', 'F-2796/24')],
        [dosis('Refracción / examen de fondo de ojo', 'adulto', '1 o 2 gotas unos 40–45 minutos antes del examen; si hace falta, repetir a los 5–10 minutos',
               c('4.2 Uso en adultos: 1 o 2 gotas aproximadamente 40-45 minutos antes del examen; repetir a los 5 o 10 minutos'),
               cantidad=2, unidad='gota', sitio='ojo', duracion='Dosis única antes del examen'),
         dosis('Efecto ciclopléjico sostenido', 'adulto', '2 gotas 3 veces al día',
               c('4.2 Uso en adultos: efecto sostenido, en general 2 gotas tres veces al día'), cantidad=2, unidad='gota', veces_dia=3, sitio='ojo'),
         dosis('Refracción (menores de 6 años)', 'pediatrico', '1 gota 40–50 minutos antes del examen; si hace falta, una segunda gota 5–10 minutos después',
               c('4.2 Población pediátrica: niños menores de 6 años, 1 gota 40 o 50 minutos antes del examen'),
               cantidad=1, unidad='gota', sitio='ojo', condicion='No recomendado en recién nacidos ni lactantes (concentración >0,5 %)',
               tambien=[p('Para estudios de refracción, 1 gota, repetir a los 5 minutos, y explorar a los 45 minutos. En niños menores de 6 años, solo una gota')]),
         dosis('Refracción (mayores de 6 años)', 'pediatrico', '1 o 2 gotas; si hace falta, otra a los 5 minutos, 40–50 minutos antes del examen',
               c('4.2 Población pediátrica: niños mayores de 6 años, 1 o 2 gotas'), cantidad=2, unidad='gota', sitio='ojo',
               tambien=[p('1 gota, repetir a los 5 minutos y explorar a los 45 minutos')])],
        alto_riesgo=True,
        pediatria=('con_dosis', 'No recomendado en recién nacidos ni lactantes por riesgo sistémico grave (CIMA). Observar al niño 30 minutos.'),
        conservacion=conserv('Desechar 4 semanas después de abrir. No conservar sobre 25 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Ocluir el conducto nasolagrimal al menos 2 minutos (sobre todo en niños). En neonatos y lactantes, no darles alimento '
                                 'durante 4 horas después. ' + ESPACIAR, 'fuente': c('4.2 Población pediátrica y forma de administración')},
        contraindicaciones=['Glaucoma de ángulo estrecho o ángulo estrecho anatómico (CIMA).'],
        alertas=['Los niños son más susceptibles a la toxicidad sistémica: usar la dosis eficaz más baja (CIMA).',
                 'Ancianos: más riesgo de glaucoma no diagnosticado y reacciones psicóticas (CIMA).'],
    )

    # ---------------------------------------------------------------- ciclosporina
    c = lambda d: cima('ciclosporina', '115990001', d)  # noqa: E731  Ikervis 1 mg/ml emulsión
    p = lambda d: ped('ciclosporina', d)  # noqa: E731
    f['ciclosporina'] = ficha(
        'ciclosporina', 'CICLOSPORINA', 'Ciclosporina oftálmica', 'inmunomodulador-ocular',
        [pres('solucion', '0,1 %', 'ojo', 'F-13844/24'), pres('emulsion', '0,05 %', 'ojo', 'F-13719/24')],
        [dosis('Queratitis grave en ojo seco que no mejora con lágrimas artificiales', 'adulto',
               '1 gota en el ojo afectado 1 vez al día, al acostarse; reevaluar al menos cada 6 meses',
               c('4.2: una gota una vez al día en el (los) ojo(s) afectados a la hora de acostarse'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo', presentaciones=['ojo-solucion-0-1'],
               condicion='La ficha es de una emulsión de 1 mg/ml (Ikervis); en Chile, 0,1 % es solución (Modusik-A)'),
         dosis('Ojo seco (queratoconjuntivitis seca)', 'pediatrico', '1 gota en cada ojo cada 12 horas',
               p('Sequedad ocular en la queratoconjuntivitis seca en adolescentes >16 años: emulsión al 0,05%: 1 gota en cada ojo/12 horas'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', estatus='off_label', presentaciones=['ojo-emulsion-0-05'],
               condicion='Adolescentes mayores de 16 años')],
        pediatria=('con_dosis', 'Ficha técnica (Ikervis): no apropiada en menores de 18 años. Pediamécum da pauta para mayores de 16 años con la emulsión 0,05 %.', '16 años (Pediamécum)'),
        conservacion=conserv('Unidosis (Ikervis): desechar inmediatamente después de usar; no congelar; bajo 25 °C.', c('6.4 Precauciones especiales de conservación')),
        administracion={'texto': 'Lavarse las manos; agitar suavemente el unidosis. Ocluir y cerrar los párpados 2 minutos. '
                                 'Separar al menos 15 minutos de otros colirios y aplicarla al final. Tratamiento iniciado por oftalmólogo.',
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Neoplasias oculares o perioculares, o afecciones preneoplásicas (CIMA).', 'Infección ocular o periocular activa o sospechada (CIMA).'],
        discrepancias=[disc('Presentación y concentración',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: solución 0,1 % (Modusik-A) y emulsión 0,05 % (Restasis)'),
                             ('CIMA-TOP-CICLOSPORINA-115990001', 'CIMA: emulsión 1 mg/ml (0,1 %), 1 vez al día'),
                             ('PEDIAMECUM-TOP-CICLOSPORINA', 'Pediamécum: emulsión 0,05 %, 1 gota c/12 h en >16 años')],
                            'Cada pauta solo con su concentración', 'Regla de concentración. La solución 0,1 % chilena y la emulsión 0,1 % de CIMA tienen distinto vehículo.')],
    )

    # ---------------------------------------------------------------- ciprofloxacino (ótico y oftálmico)
    co = lambda d: cima('ciprofloxacino', '60608', d)  # noqa: E731  Oftacilox 3 mg/ml colirio
    ct = lambda d: cima('ciprofloxacino', '60883', d)  # noqa: E731  Cetraxal ótico 3 mg/ml
    ped('ciprofloxacino', 'Solo vía intravenosa y oral; sin pauta tópica')
    f['ciprofloxacino'] = ficha(
        'ciprofloxacino', 'CIPROFLOXACINO', 'Ciprofloxacino oftálmico y ótico 0,3 %', 'antibiotico',
        [pres('solucion', '0,3 %', 'ojo', 'F-27267/23', 'F-9567/21', 'F-21517/24', 'F-16044/22'),
         pres('unguento', '0,3 %', 'ojo', 'F-9569/26'),
         pres('solucion', '0,3 %', 'oido', 'F-20503/23', 'F-514/23')],
        [dosis('Conjuntivitis bacteriana, úlcera corneal, queratitis', 'adulto',
               '1 o 2 gotas cada 2 h durante el día los 2 primeros días; desde el 3.er día, 1 o 2 gotas cada 4 h durante el día',
               co('4.2.1: conjuntivitis, úlceras corneales y queratitis: 1-2 gotas c/2 h los dos primeros días; desde el tercer día c/4 h'),
               cantidad=2, unidad='gota', sitio='ojo', presentaciones=['ojo-solucion-0-3']),
         dosis('Absceso corneal', 'adulto',
               'Día 1: 2 gotas cada 15 min las primeras 6 h y luego cada 30 min; día 2: 2 gotas cada hora; días 3 a 14: 2 gotas cada 4 h (también de noche)',
               co('4.2.1 Abscesos corneales'), presentaciones=['ojo-solucion-0-3'], duracion='14 días o más'),
         dosis('Conjuntivitis bacteriana, úlcera corneal, queratitis', 'pediatrico', 'Igual que en adultos (incluye neonatos)',
               co('4.2.1: adultos, neonatos (0-27 días), lactantes, niños y adolescentes'), cantidad=2, unidad='gota', sitio='ojo',
               presentaciones=['ojo-solucion-0-3']),
         dosis('Otitis externa', 'adulto', '4 a 6 gotas en el conducto auditivo cada 8 h durante 7–8 días',
               ct('4.2: instilar 4-6 gotas en el conducto auditivo externo, cada 8 horas; 7 a 8 días'),
               cantidad=6, unidad='gota', veces_dia=3, sitio='oido', presentaciones=['oido-solucion-0-3'], duracion='7 a 8 días')],
        pediatria=('con_dosis', 'Colirio: misma pauta desde neonatos (CIMA). Gotas óticas: la ficha no trae pauta pediátrica.'),
        conservacion=[conserv('Colirio: desechar 4 semanas después de abrir; no refrigerar ni congelar.', co('6.3/6.4'), dias=28,
                              presentaciones=['ojo-solucion-0-3']),
                      conserv('Gotas óticas: conservar el frasco hasta terminar el tratamiento.', ct('4.2: conserve el frasco hasta la finalización del tratamiento'),
                              presentaciones=['oido-solucion-0-3'])],
        administracion={'texto': 'Oído: entibiar el frasco en la mano, cabeza de lado con el oído hacia arriba, instilar, tirar del lóbulo y mantener 5 minutos. '
                                 'Ojo: ' + ESPACIAR, 'fuente': ct('4.2 Forma de administración (ótico); Oftacilox 4.2.2 (oftálmico)')},
        contraindicaciones=['Hipersensibilidad a ciprofloxacino u otras quinolonas (CIMA).'],
        alertas=['El ungüento oftálmico 0,3 % (Ciproval) no tiene ficha en las fuentes consultadas: sin pauta.'],
    )

    # ---------------------------------------------------------------- ciprofloxacino + dexametasona
    d_ = lambda d: dm('ciprofloxacino-dexametasona', d)  # noqa: E731  ótico 0,3 % + 0,1 %
    f['ciprofloxacino-dexametasona'] = ficha(
        'ciprofloxacino-dexametasona', 'CIPROFLOXACINO + DEXAMETASONA', 'Ciprofloxacino + dexametasona ótico y oftálmico', 'antibiotico-corticoide',
        [pres('suspension', NC, 'oido', 'F-14179/24'),
         pres('suspension', NC, 'ojo', 'F-9566/21', 'F-22209/25'),
         pres('solucion', NC, 'ojo', 'F-17893/24'),
         pres('unguento', NC, 'ojo', 'F-15861/21', 'F-22098/25')],
        [dosis('Otitis externa aguda u otitis media aguda con tubos de timpanostomía', 'adulto', '4 gotas en el oído afectado 2 veces al día durante 7 días',
               d_('2: instill four drops into the affected ear twice daily, for seven days'),
               cantidad=4, unidad='gota', veces_dia=2, sitio='oido', presentaciones=['oido-suspension-sc'], duracion='7 días'),
         dosis('Otitis externa aguda u otitis media aguda con tubos de timpanostomía', 'pediatrico', '4 gotas en el oído afectado 2 veces al día durante 7 días',
               d_('2.2: pediatric patients age 6 months and older; 8.4 safety and efficacy established ≥6 months'),
               cantidad=4, unidad='gota', veces_dia=2, sitio='oido', presentaciones=['oido-suspension-sc'], condicion='Desde los 6 meses')],
        componentes=['Ciprofloxacino', 'Dexametasona'],
        pediatria=('con_dosis', 'Suspensión ótica: establecida desde los 6 meses (FDA). Presentaciones oftálmicas: sin fuente.', '6 meses'),
        conservacion=conserv('Suspensión ótica: desechar lo que sobre al terminar el tratamiento. Conservar a 20–25 °C.',
                             d_('2.2: discard unused portion after therapy is completed; storage 20°C to 25°C'), presentaciones=['oido-suspension-sc']),
        administracion={'texto': 'Solo para el oído (no oftálmico ni inyectable). Agitar bien, entibiar 1–2 minutos en la mano, acostarse con el oído hacia arriba, '
                                 'instilar y mantener 60 segundos. Con tubos: presionar el trago 5 veces.', 'fuente': d_('2.1 y 2.2 Administración')},
        contraindicaciones=['Hipersensibilidad a ciprofloxacino u otras quinolonas (FDA).', 'Infecciones virales (incluido herpes) o fúngicas del conducto auditivo (FDA).'],
        alertas=['Las presentaciones oftálmicas (suspensión, solución y ungüento) no tienen ficha en las fuentes consultadas: sin pauta.'],
    )
    ped('dexametasona', 'Tópica oftálmica: 1 gota 4-6 veces al día en el ojo afecto; suspensión gradual')

    # ---------------------------------------------------------------- ciprofloxacino + fluocinolona
    c = lambda d: cima('ciprofloxacino-fluocinolona', '64655', d)  # noqa: E731  Synalotic 3 + 0,25 mg/ml
    f['ciprofloxacino-fluocinolona'] = ficha(
        'ciprofloxacino-fluocinolona', 'CIPROFLOXACINO + FLUOCINOLONA', 'Ciprofloxacino + fluocinolona ótico', 'antibiotico-corticoide',
        [pres('solucion', '0,3 % + 0,025 %', 'oido', 'F-20638/23')],
        [dosis('Otitis externa aguda u otitis media aguda con tubos de timpanostomía', 'adulto', '6 a 8 gotas en el conducto auditivo cada 12 h durante 7 días',
               c('4.2.1: aplicar 6-8 gotas en el conducto auditivo externo afectado cada 12 horas durante 7 días'),
               cantidad=8, unidad='gota', veces_dia=2, sitio='oido', duracion='7 días'),
         dosis('Otitis externa aguda u otitis media aguda con tubos de timpanostomía', 'pediatrico', 'Igual que en adultos: 6 a 8 gotas cada 12 h durante 7 días',
               c('4.2.1 Población pediátrica: en niños de 6 meses y mayores la misma dosis que en adultos'),
               cantidad=8, unidad='gota', veces_dia=2, sitio='oido', condicion='Desde los 6 meses')],
        componentes=['Ciprofloxacino', 'Fluocinolona'],
        pediatria=('con_dosis', 'Desde los 6 meses, igual que en adultos (CIMA).', '6 meses'),
        conservacion=conserv('Una vez abierto: 1 mes (la calculadora usa 28 días). Conservar bajo 30 °C.', c('6.3: una vez abierto, 1 mes'), dias=28),
        administracion={'texto': 'Entibiar el frasco en la mano, cabeza de lado, instilar y tirar del lóbulo; con tubos, bombear el trago 4 veces. Mantener 1 minuto.',
                        'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a ciprofloxacino, fluocinolona u otras quinolonas (CIMA).',
                            'Infecciones virales (varicela, herpes) o fúngicas del conducto auditivo (CIMA).'],
        discrepancias=[disc('Pauta ótica',
                            [('CIMA-TOP-CIPROFLOXACINO-FLUOCINOLONA-64655', 'Synalotic 3 + 0,25 mg/ml: 6-8 gotas cada 12 h, 7 días'),
                             ('PEDIAMECUM-TOP-FLUOCINOLONA', 'Fluocinolona asociada a ciprofloxacino: 4-6 gotas cada 8 h')],
                            'Pauta de la ficha técnica (6–8 gotas cada 12 h)',
                            'Misma concentración que el registro chileno; Pediamécum no indica la concentración de la asociación que describe.')],
    )
    ped('fluocinolona', 'Ótico asociado con ciprofloxacino: 4-6 gotas/8 h')

    # ---------------------------------------------------------------- ciprofloxacino + hidrocortisona
    c = lambda d: cima('ciprofloxacino-hidrocortisona', '63285', d)  # noqa: E731  Ciproxina 2 + 10 mg/ml
    f['ciprofloxacino-hidrocortisona'] = ficha(
        'ciprofloxacino-hidrocortisona', 'CIPROFLOXACINO + HIDROCORTISONA', 'Ciprofloxacino + hidrocortisona ótico', 'antibiotico-corticoide',
        [pres('suspension', NC, 'oido', 'F-12589/22')],
        [dosis('Otitis externa', 'adulto', '3 gotas en el oído afectado 2 veces al día durante 7 días',
               c('4.2.1: en adultos y en niños a partir de dos años, instilar 3 gotas dos veces al día; 7 días'),
               cantidad=3, unidad='gota', veces_dia=2, sitio='oido', duracion='7 días'),
         dosis('Otitis externa', 'pediatrico', '3 gotas en el oído afectado 2 veces al día durante 7 días',
               c('4.2.1: niños a partir de dos años; menores de 2 años, datos limitados'), cantidad=3, unidad='gota', veces_dia=2, sitio='oido',
               condicion='Desde los 2 años')],
        componentes=['Ciprofloxacino', 'Hidrocortisona'],
        pediatria=('con_dosis', 'Desde los 2 años; datos limitados en menores (CIMA).', '2 años'),
        conservacion=conserv('Tras abrir e insertar el cuentagotas: 14 días. Bajo 25 °C, sin refrigerar, protegido de la luz; desechar lo sobrante al terminar.',
                             c('6.3: tras apertura e inserción del cuentagotas: 14 días'), dias=14),
        administracion={'texto': 'Solo vía ótica. Agitar bien, entibiar en la mano, cabeza de lado y mantener 5 minutos.', 'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Perforación de tímpano posible o conocida (CIMA).', 'Otitis media aguda o crónica (CIMA).',
                            'Infecciones víricas o fúngicas del conducto auditivo (CIMA).', 'Hipersensibilidad a quinolonas (CIMA).'],
        alertas=['Ciproxina es 2 mg/ml + 10 mg/ml; el registro chileno (Otex HC) no indica concentración en el nombre.'],
    )

    # ---------------------------------------------------------------- cloranfenicol
    c = lambda d: cima('cloranfenicol', '19495', d)  # noqa: E731  Oftalmolosa Cusí cloranfenicol 10 mg/g
    p = lambda d: ped('cloranfenicol', d)  # noqa: E731
    f['cloranfenicol'] = ficha(
        'cloranfenicol', 'CLORANFENICOL', 'Cloranfenicol oftálmico', 'antibiotico',
        [pres('unguento', '1 %', 'ojo', 'F-22797/26', 'F-12980/23', 'F-7259/25', 'F-19212/22', 'F-19320/22'),
         pres('solucion', '0,5 %', 'ojo', 'F-28264/24', 'F-25283/25', 'F-20082/23', 'F-22034/25')],
        [dosis('Infección ocular bacteriana', 'adulto', '1 cm de pomada cada 3 h (o más seguido las primeras 48 h); luego espaciar según indicación',
               c('4.2: una aplicación de 1 cm aproximadamente cada 3 horas, o más frecuentemente durante las primeras 48 horas'),
               cantidad=1, unidad='cm', sitio='ojo', presentaciones=['ojo-unguento-1'], duracion='Máximo 10–14 días'),
         dosis('Infección ocular bacteriana (pomada)', 'pediatrico', 'Pomada 3–4 veces al día, o por la noche junto al colirio',
               p('Pomada: 3-4 veces al día o por las noches asociadas al colirio'), presentaciones=['ojo-unguento-1'],
               condicion='En recién nacidos puede requerir ajuste (CIMA)', duracion='Máximo 10–14 días (CIMA)'),
         dosis('Infección ocular bacteriana (colirio)', 'pediatrico', '1 gota cada 3 h al inicio (más seguido en procesos graves)',
               p('Colirio: 1 gota cada 3 h inicialmente (más frecuente en procesos graves)'), cantidad=1, unidad='gota', sitio='ojo',
               presentaciones=['ojo-solucion-0-5'], condicion='Pediamécum no indica la concentración del colirio')],
        pediatria=('con_dosis', 'La ficha técnica de la pomada no excluye a los niños; en recién nacidos puede requerir ajuste.'),
        conservacion=conserv('Pomada: desechar 4 semanas después de abrir; no conservar sobre 25 °C.', c('6.3: desechar 4 semanas después de la primera apertura'),
                             dias=28, presentaciones=['ojo-unguento-1']),
        administracion={'texto': 'En infecciones graves, completar con un antibiótico sistémico. ' + ESPACIAR, 'fuente': c('4.2 Posología y forma de administración')},
        contraindicaciones=['Antecedentes de depresión de médula ósea o discrasias sanguíneas (CIMA).',
                            'Infecciones menores, profilaxis, o cuando sirven antibacterianos menos tóxicos (CIMA).'],
        alertas=['La solución 0,5 % no tiene ficha técnica en las fuentes consultadas; para adultos solo hay pauta de la pomada.'],
    )

    # ---------------------------------------------------------------- cloruro de sodio nasal
    c = lambda d: cima('cloruro-de-sodio', '60230', d)  # noqa: E731  Respitol 8,5 mg/ml gotas nasales
    f['cloruro-de-sodio'] = ficha(
        'cloruro-de-sodio', 'CLORURO DE SODIO', 'Cloruro de sodio nasal (suero fisiológico)', 'lavado-nasal',
        [pres('spray', '0,9 %', 'nariz', 'F-1993/24'), pres('solucion', '0,9 %', 'nariz', 'F-12764/23'),
         pres('spray', '3 % (hipertónica)', 'nariz', 'F-12574/22')],
        [dosis('Limpieza y humidificación nasal', 'adulto', '1 a 3 gotas en cada fosa nasal, tantas veces como sea necesario',
               c('4.2: aplicar de 1 a 3 gotas en cada orificio nasal, tantas veces como sea necesario'),
               cantidad=3, unidad='gota', sitio='fosa', presentaciones=['nariz-solucion-0-9'],
               condicion='Si no mejora en 3 días, reevaluar'),
         dosis('Limpieza y humidificación nasal', 'pediatrico', '1 a 3 gotas en cada fosa nasal, tantas veces como sea necesario',
               c('4.2: la ficha no distingue edades'), cantidad=3, unidad='gota', sitio='fosa', presentaciones=['nariz-solucion-0-9'],
               condicion='La ficha no distingue edades')],
        pediatria=('con_dosis', 'La ficha técnica no distingue edades.'),
        conservacion=conserv('Una vez abierto, lugar fresco y desechar a los 7 días. No conservar sobre 30 °C.', c('6.4: una vez abierto, desechar a los 7 días'), dias=7,
                             presentaciones=['nariz-solucion-0-9']),
        contraindicaciones=['Hipersensibilidad al cloruro de sodio o a algún excipiente (CIMA).'],
        discrepancias=[disc('Concentración y forma',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: solución nasal 0,9 %, nebulización 0,9 % y 3 % hipertónica'),
                             ('CIMA-TOP-CLORURO-DE-SODIO-60230', 'CIMA: gotas nasales 8,5 mg/ml (0,85 %)')],
                            'Pauta solo para la solución en gotas 0,9 %',
                            'Ambas son prácticamente isotónicas; los nebulizadores y la solución hipertónica 3 % no tienen ficha.')],
    )

    # ---------------------------------------------------------------- cromoglicato (forma distinta)
    ped('cromoglicato', 'Solo cromoglicato nebulizado por vía inhalatoria')
    f['cromoglicato'] = ficha(
        'cromoglicato', 'CROMOGLICATO', 'Cromoglicato oftálmico (ungüento 4 %)', 'antialergico',
        [pres('unguento', '4 %', 'ojo', 'F-9584/26')], [],
        pediatria=('sin_datos', 'Sin fuente para el ungüento.'),
        sin_pauta='En Chile está registrado como ungüento oftálmico 4 %; la única fuente oftálmica (FDA) es de solución 4 % en gotas '
                  '(1–2 gotas 4–6 veces al día), que no sirve para una pomada. Pediamécum solo trae la vía inhalatoria.',
        discrepancias=[disc('Forma farmacéutica',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: ungüento oftálmico 4 %'),
                             ('DAILYMED-TOP-CROMOGLICATO', 'FDA: solución oftálmica 4 %, 1-2 gotas 4-6 veces al día'),
                             ('PEDIAMECUM-TOP-CROMOGLICATO', 'Pediamécum: cromoglicato nebulizado (asma)')],
                            'Sin pauta', 'Forma (gotas vs. pomada) y vía (inhalatoria) distintas del registro chileno.')],
    )
    dm('cromoglicato', 'Solución oftálmica 4 %: 1 or 2 drops in each eye 4 to 6 times a day')

    # ---------------------------------------------------------------- dexametasona (concentración distinta)
    pd_ = lambda d: ped('dexametasona', d)  # noqa: E731
    cima('dexametasona', '40309', 'Pomada 0,5 mg/g: 1 cm 2-3 veces al día; máximo 14 días')
    f['dexametasona'] = ficha(
        'dexametasona', 'DEXAMETASONA', 'Dexametasona oftálmica 0,15 % (unidosis)', 'corticoide',
        [pres('solucion', '0,15 %', 'ojo', 'F-16739/23', unidosis=True)],
        [dosis('Inflamación ocular', 'pediatrico', '1 gota 4–6 veces al día en el ojo afectado; retirar de forma gradual',
               pd_('Tópica oftálmica: 1 gota 4-6 veces al día en el ojo afecto. Se aconseja la suspensión gradual del tratamiento'),
               cantidad=1, unidad='gota', veces_dia=6, sitio='ojo', estatus='off_label',
               condicion='Pediamécum no indica la concentración; la ficha técnica no establece el uso pediátrico')],
        pediatria=('con_dosis', 'Solo pauta de Pediamécum, como off-label.'),
        conservacion=conserv('Envase unidosis: usar y desechar tras cada aplicación.', isp('F-16739/23 ETACORTILEN SOLUCIÓN OFTÁLMICA UNIDOSIS 0,15%')),
        contraindicaciones=['Queratitis por herpes simple; infecciones bacterianas agudas no tratadas (CIMA).',
                            'Vaccinia, varicela y otras infecciones víricas de córnea o conjuntiva; infecciones fúngicas o por micobacterias (CIMA).'],
        alertas=['Sin pauta de adulto para la solución 0,15 %: la ficha CIMA es de pomada 0,05 % (regla de concentración).'],
        discrepancias=[disc('Concentración y forma',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: solución oftálmica unidosis 0,15 %'),
                             ('CIMA-TOP-DEXAMETASONA-40309', 'CIMA: pomada 0,5 mg/g (0,05 %), 1 cm 2-3 veces al día, máx. 14 días; pediatría no establecida')],
                            'Sin pauta de adulto; pediátrica de Pediamécum como off-label',
                            'Regla de concentración (decisión de Héctor, 31-oct) y regla pediátrica (Pediamécum off-label).')],
    )

    # ---------------------------------------------------------------- dexametasona + levofloxacino
    c = lambda d: cima('dexametasona-levofloxacino', '85248', d)  # noqa: E731  Ducressa 1 + 5 mg/ml
    f['dexametasona-levofloxacino'] = ficha(
        'dexametasona-levofloxacino', 'DEXAMETASONA + LEVOFLOXACINO', 'Levofloxacino + dexametasona oftálmico', 'antibiotico-corticoide',
        [pres('solucion', NC, 'ojo', 'F-26815/22')],
        [dosis('Prevención de infección e inflamación tras cirugía de catarata', 'adulto', '1 gota en el saco conjuntival cada 6 h durante 7 días',
               c('4.2: una gota aplicada en el saco conjuntival tras la intervención cada 6 horas; 7 días'),
               cantidad=1, unidad='gota', veces_dia=4, sitio='ojo', duracion='7 días; luego reevaluar')],
        componentes=['Levofloxacino', 'Dexametasona'],
        pediatria=('no_establecida', 'No se recomienda en menores de 18 años; sin datos (CIMA).'),
        administracion={'texto': 'Instilar en el canto externo presionando el canto interno. Lavarse las manos; no tocar el ojo con la punta. '
                                 'Separar 15 minutos de otros colirios.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a quinolonas o corticoides (CIMA).', 'Queratitis herpética, varicela y otras virosis corneales (CIMA).',
                            'Infecciones micobacterianas o micóticas del ojo; infección purulenta no tratada (CIMA).'],
        alertas=['Ducressa es 1 mg/ml + 5 mg/ml; el registro chileno (Istadine) no indica concentración en el nombre.'],
    )
    return f
