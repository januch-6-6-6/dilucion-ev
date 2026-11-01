"""Tópicos, lote 3: dexametasona + moxifloxacino → loteprednol + tobramicina."""
from .comun import NC, cima, conserv, disc, dm, dosis, ficha, ped, pres
from .lote1 import SIN_COMBO
from .lote2 import BETABLOQ, ESPACIAR, OCLUSION

CORTICOIDE_OJO = ['Queratitis por herpes simple; vaccinia, varicela y otras infecciones víricas de córnea o conjuntiva.',
                  'Infecciones fúngicas o micobacterianas del ojo; infecciones agudas no tratadas.']


def fichas():
    f = {}

    # ---------------------------------------------------------------- combinaciones chilenas sin fuente
    for id_, mol, nombre, grupo, comps, via, codigos in [
        ('dexametasona-moxifloxacino', 'DEXAMETASONA + MOXIFLOXACINO', 'Moxifloxacino + dexametasona oftálmico', 'antibiotico-corticoide',
         ['Moxifloxacino', 'Dexametasona'], 'ojo', ['FX-354/25']),
        ('dextrano-hipromelosa-nafazolina', 'DEXTRANO + HIPROMELOSA + NAFAZOLINA', 'Dextrano + hipromelosa + nafazolina oftálmica', 'descongestionante',
         ['Dextrano', 'Hipromelosa', 'Nafazolina'], 'ojo', ['F-13530/24']),
        ('fenazona-lidocaina', 'FENAZONA + LIDOCAINA', 'Fenazona + lidocaína ótica', 'analgesico-otico',
         ['Fenazona', 'Lidocaína'], 'oido', ['F-11846/22']),
        ('lidocaina-sulfatiazol', 'LIDOCAINA + SULFATIAZOL', 'Lidocaína + sulfatiazol ótico', 'analgesico-otico',
         ['Lidocaína', 'Sulfatiazol'], 'oido', ['F-11656/26']),
    ]:
        f[id_] = ficha(id_, mol, nombre, grupo, [pres('solucion', NC, via, *codigos)], [], componentes=comps,
                       pediatria=('sin_datos', 'Sin fuente de posología para la combinación.'), sin_pauta=SIN_COMBO)

    # ---------------------------------------------------------------- dexametasona + tobramicina
    c = lambda d: cima('dexametasona-tobramicina', '61575', d)  # noqa: E731  Tobradex 1 + 3 mg/ml suspensión
    f['dexametasona-tobramicina'] = ficha(
        'dexametasona-tobramicina', 'DEXAMETASONA + TOBRAMICINA', 'Tobramicina + dexametasona oftálmica', 'antibiotico-corticoide',
        [pres('suspension', '0,3 % + 0,1 %', 'ojo', 'B-2727/23', 'B-2801/22', 'B-2798/26', 'B-2371/23', 'B-2813/22', 'B-2816/21', 'B-2811/21', 'B-2805/22'),
         pres('unguento', NC, 'ojo', 'B-2797/26', 'B-2815/26', 'B-2804/22')],
        [dosis('Inflamación ocular con infección bacteriana o riesgo de ella', 'adulto',
               '1 o 2 gotas cada 4–6 h; las primeras 24–48 h, hasta cada 2 h. Bajar la frecuencia al mejorar',
               c('4.2: 1 o 2 gotas cada 4-6 horas; primeras 24-48 horas, 1-2 gotas cada dos horas; no más de 14 días'),
               cantidad=2, unidad='gota', veces_dia=6, sitio='ojo', presentaciones=['ojo-suspension-0-3-0-1'], duracion='No más de 14 días'),
         dosis('Después de cirugía de catarata', 'adulto', '1 gota 4 veces al día desde el día siguiente a la cirugía, hasta 24 días',
               c('4.2: después de la cirugía de cataratas, 1 gota cuatro veces al día hasta 24 días'),
               cantidad=1, unidad='gota', veces_dia=4, sitio='ojo', presentaciones=['ojo-suspension-0-3-0-1'], duracion='Hasta 24 días'),
         dosis('Inflamación ocular con infección bacteriana o riesgo de ella', 'pediatrico', 'Igual que en adultos: 1 o 2 gotas cada 4–6 h',
               c('4.2 Población pediátrica: niños de 2 años y mayores, a la misma dosis que en adultos'),
               cantidad=2, unidad='gota', veces_dia=6, sitio='ojo', presentaciones=['ojo-suspension-0-3-0-1'], condicion='Desde los 2 años')],
        componentes=['Tobramicina', 'Dexametasona'],
        pediatria=('con_dosis', 'Desde los 2 años, igual que en adultos; no establecida en menores de 2 (CIMA).', '2 años'),
        conservacion=conserv('Desechar 4 semanas después de abrir. No conservar sobre 25 °C; no congelar.', c('6.3: desechar 4 semanas después de la primera apertura'),
                             dias=28, presentaciones=['ojo-suspension-0-3-0-1']),
        administracion={'texto': 'Agitar bien antes de usar. ' + OCLUSION + ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=CORTICOIDE_OJO + ['Extracción simple de un cuerpo extraño de la córnea (CIMA).'],
        alertas=['El ungüento no tiene ficha en las fuentes consultadas: sin pauta.', 'Para calcular se usa la frecuencia de cada 4 h (6 veces al día).'],
    )

    # ---------------------------------------------------------------- dextrano + hipromelosa (lágrima artificial)
    d_ = lambda d: dm('dextrano-hipromelosa', d)  # noqa: E731
    f['dextrano-hipromelosa'] = ficha(
        'dextrano-hipromelosa', 'DEXTRANO + HIPROMELOSA', 'Dextrano + hipromelosa (lágrima artificial)', 'lubricante-ocular',
        [pres('solucion', NC, 'ojo', 'FX-337/24')],
        [dosis('Sequedad o irritación ocular', 'adulto', '1 o 2 gotas en el ojo afectado según necesidad',
               d_('Directions: put 1 or 2 drops in the affected eye(s) as needed'), cantidad=2, unidad='gota', sitio='ojo')],
        componentes=['Dextrano 70', 'Hipromelosa'],
        pediatria=('sin_datos', 'La etiqueta de venta libre no trae indicaciones por edad.'),
        conservacion=conserv('Conservar a 15–25 °C. La etiqueta FDA consultada indica no reutilizar una vez abierto.', d_('Storage; do not reuse once opened')),
        contraindicaciones=[],
        alertas=['Suspender y consultar si hay dolor ocular, cambios de visión, o si el enrojecimiento empeora o dura más de 72 h (FDA).'],
    )

    # ---------------------------------------------------------------- diclofenaco
    c = lambda d: cima('diclofenaco', '58308', d)  # noqa: E731  Voltaren 1 mg/ml
    p = lambda d: ped('diclofenaco', d)  # noqa: E731
    f['diclofenaco'] = ficha(
        'diclofenaco', 'DICLOFENACO', 'Diclofenaco oftálmico 0,1 %', 'aine',
        [pres('solucion', '0,1 %', 'ojo', 'F-1877/24', 'F-9586/26')],
        [dosis('Inflamación ocular', 'adulto', '1 gota 4 a 5 veces al día en el saco conjuntival',
               c('4.2.1 Adultos: 1 gota de 4 a 5 veces al día'), cantidad=1, unidad='gota', veces_dia=5, sitio='ojo'),
         dosis('Dolor y fotofobia en cirugía', 'adulto',
               '1 gota 30–60 min antes; después, 1 gota 1 o 2 veces en los 10 min siguientes y luego 1 gota 4 veces al día por 2 días',
               c('4.2.1: tratamiento del dolor y de la fotofobia'), duracion='2 días'),
         dosis('Inflamación ocular', 'pediatrico', '1 gota cada 6 horas', p('Colirio: 1 gota cada 6 horas'),
               cantidad=1, unidad='gota', veces_dia=4, sitio='ojo', estatus='off_label',
               condicion='La ficha técnica dice que no está indicado en niños')],
        pediatria=('con_dosis', 'Ficha técnica: no indicado en niños (experiencia limitada a cirugía de estrabismo). Pediamécum da pauta, como off-label.'),
        conservacion=conserv('Una vez abierto: 28 días. Desechar al terminar el tratamiento aunque quede.', c('6.3: una vez abierto el envase, 28 días'), dias=28),
        administracion={'texto': 'Manos recién lavadas; no tocar el ojo con el gotero. Ocluir o cerrar los ojos 5 minutos. Esperar 5 minutos antes de otro colirio.',
                        'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Asma, urticaria o rinitis aguda desencadenadas por ácido acetilsalicílico u otros AINE (CIMA).'],
        alertas=['Posible sensibilidad cruzada con ácido acetilsalicílico y otros AINE (CIMA).'],
        discrepancias=[disc('Uso pediátrico',
                            [('CIMA-TOP-DICLOFENACO-58308', 'No indicado en niños'), ('PEDIAMECUM-TOP-DICLOFENACO', 'Colirio: 1 gota cada 6 horas')],
                            'Ambas: Pediamécum como off-label', 'Decisión de Héctor (31-oct) para pediatría no autorizada en la ficha técnica.')],
    )

    # ---------------------------------------------------------------- dorzolamida
    c = lambda d: cima('dorzolamida', '60651', d)  # noqa: E731  Trusopt 20 mg/ml
    p = lambda d: ped('dorzolamida', d)  # noqa: E731
    f['dorzolamida'] = ficha(
        'dorzolamida', 'DORZOLAMIDA', 'Dorzolamida oftálmica 2 %', 'antiglaucomatoso',
        [pres('solucion', '2 %', 'ojo', 'F-26236/26', 'F-26462/26', 'F-28465/24', 'FX-329/24', 'F-23044/26', 'F-24570/24', 'F-28468/24',
              'F-11896/22', 'F-29674/26', 'F-29939/26')],
        [dosis('Glaucoma / hipertensión ocular (monoterapia)', 'adulto', '1 gota en el ojo afectado 3 veces al día',
               c('4.2: monoterapia, una gota tres veces al día'), cantidad=1, unidad='gota', veces_dia=3, sitio='ojo',
               tambien=[p('Una gota cada 8 h en cada ojo afectado')]),
         dosis('Glaucoma / hipertensión ocular (con betabloqueante)', 'adulto', '1 gota en el ojo afectado 2 veces al día',
               c('4.2: terapia coadyuvante con un betabloqueante oftálmico, una gota dos veces al día'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo',
               tambien=[p('Una gota cada 12 h')]),
         dosis('Glaucoma pediátrico', 'pediatrico', '1 gota cada 8 h (monoterapia) o cada 12 h si se asocia a betabloqueante',
               p('Una gota cada 8 h en cada ojo afectado | Una gota cada 12 h'), cantidad=1, unidad='gota', veces_dia=3, sitio='ojo',
               condicion='Datos clínicos pediátricos limitados (CIMA)', tambien=[c('4.2 Población pediátrica: datos limitados tres veces al día')])],
        pediatria=('con_dosis', 'Datos pediátricos limitados con 3 veces al día (CIMA).'),
        conservacion=conserv('No usar más de 28 días tras abrir. Proteger de la luz.', c('6.3: después de la primera apertura, no más de 28 días'), dias=28),
        administracion={'texto': 'Lavarse las manos. Tras la gota, oprimir el ángulo interno del ojo o cerrar los párpados unos 2 minutos. '
                                 'Separar al menos 10 minutos de otros colirios.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Insuficiencia renal grave (ClCr <30 ml/min) o acidosis hiperclorémica (CIMA).'],
    )

    # ---------------------------------------------------------------- dorzolamida + timolol
    c = lambda d: cima('dorzolamida-timolol', '62535', d)  # noqa: E731  Cosopt 20 + 5 mg/ml
    reg = ['F-26522/21', 'F-26134/26', 'F-20789/24', 'F-27653/23', 'F-24559/24', 'F-24561/24', 'F-22044/25', 'F-28211/24', 'F-11829/22',
           'F-26526/21', 'F-14275/24', 'F-29819/26', 'F-5304/25']
    f['dorzolamida-timolol'] = ficha(
        'dorzolamida-timolol', 'DORZOLAMIDA + TIMOLOL', 'Dorzolamida + timolol oftálmico', 'antiglaucomatoso',
        [pres('solucion', '2 % + 0,5 %', 'ojo', 'F-26840/22', 'F-28487/24', 'F-28464/24'), pres('solucion', NC, 'ojo', *reg)],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 2 veces al día',
               c('4.2.1: una gota de COSOPT dos veces al día'), cantidad=1, unidad='gota', veces_dia=2, sitio='ojo')],
        componentes=['Dorzolamida', 'Timolol'],
        pediatria=('no_establecida', 'Eficacia no establecida en niños; seguridad no establecida en menores de 2 años (CIMA).'),
        conservacion=conserv('Usar dentro de 28 días tras abrir. Proteger de la luz.', c('6.3: una vez abierto, no superior a 28 días'), dias=28),
        administracion={'texto': 'Cerrar el ojo y oprimir el ángulo interno unos 2 minutos. Separar al menos 10 minutos de otros colirios.',
                        'fuente': c('4.2.1 Método de administración')},
        contraindicaciones=BETABLOQ + ['Insuficiencia renal grave (ClCr <30 ml/min) o acidosis hiperclorémica (CIMA).'],
        alertas=['Cosopt es 20 mg/ml + 5 mg/ml (2 % + 0,5 %); varios registros chilenos no indican concentración: verificar el envase.'],
    )

    # ---------------------------------------------------------------- fenilefrina (concentración distinta)
    p = lambda d: ped('fenilefrina', d)  # noqa: E731
    c = lambda d: cima('fenilefrina', '34185', d)  # noqa: E731  Colircusí fenilefrina 100 mg/ml (10 %)
    f['fenilefrina'] = ficha(
        'fenilefrina', 'FENILEFRINA', 'Fenilefrina oftálmica 2,5 %', 'midriatico',
        [pres('solucion', '2,5 %', 'ojo', 'F-29863/26', 'F-3249/25', 'F-26762/22')],
        [dosis('Midriasis para procedimientos (menores de 1 año)', 'pediatrico', '1 gota al 2,5 % 15–30 minutos antes del procedimiento',
               p('Niños <1 año: instilación de una gota al 2,5%, 15-30 minutos antes del procedimiento'), cantidad=1, unidad='gota', sitio='ojo',
               estatus='off_label', condicion='Sin ficha técnica para la concentración de 2,5 %'),
         dosis('Midriasis para procedimientos (mayores de 1 año)', 'pediatrico', '1 gota al 2,5 %; repetir en 10–60 minutos si hace falta',
               p('Niños >1 año: instilación de una gota al 2,5% o solución al 10%, repetir en 10-60 minutos si es necesario'),
               cantidad=1, unidad='gota', sitio='ojo', estatus='off_label', condicion='Sin ficha técnica para la concentración de 2,5 %')],
        alto_riesgo=True,
        pediatria=('con_dosis', 'Solo pauta de Pediamécum para 2,5 %. La ficha CIMA (10 %) contraindica su uso en menores de 12 años.'),
        administracion={'texto': 'Ocluir el conducto nasolagrimal al menos 2 minutos o cerrar suavemente los ojos. La midriasis completa tarda 30–60 minutos. ' + ESPACIAR,
                        'fuente': c('4.2 Forma de administración (válida para la vía, no para la dosis)')},
        contraindicaciones=['Ángulo estrecho anatómico o glaucoma de ángulo estrecho (CIMA, 10 %).', 'Hipertensión grave; cardiopatía orgánica, aneurismas (CIMA, 10 %).'],
        alertas=['Sin pauta de adulto para 2,5 %: la ficha CIMA es de 10 % (cuatro veces más concentrada); su pauta y su contraindicación en '
                 'menores de 12 años y ancianos son de esa concentración.', 'Los niños pueden ser especialmente sensibles a la fenilefrina (CIMA).'],
        discrepancias=[disc('Concentración',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: solución 2,5 %'),
                             ('CIMA-TOP-FENILEFRINA-34185', 'CIMA: Colircusí 100 mg/ml (10 %): 1 gota, repetir en 1 h; contraindicado <12 años y ancianos'),
                             ('PEDIAMECUM-TOP-FENILEFRINA', 'Pediamécum: 1 gota al 2,5 % (desde lactantes)')],
                            'Solo la pauta pediátrica de 2,5 % (off-label)', 'Regla de concentración (decisión de Héctor, 31-oct).')],
    )

    # ---------------------------------------------------------------- feniramina + nafazolina
    d_ = lambda d: dm('feniramina-nafazolina', d)  # noqa: E731
    f['feniramina-nafazolina'] = ficha(
        'feniramina-nafazolina', 'FENIRAMINA + NAFAZOLINA', 'Nafazolina + feniramina oftálmica', 'descongestionante',
        [pres('solucion', NC, 'ojo', 'F-26856/22', 'F-9001/26', 'F-22329/25')],
        [dosis('Alergia ocular (picazón y enrojecimiento)', 'adulto', '1 o 2 gotas en el ojo afectado hasta 4 veces al día',
               d_('Directions: adults and children 6 years of age and older: instill 1 or 2 drops up to 4 times daily'),
               cantidad=2, unidad='gota', veces_dia=4, sitio='ojo'),
         dosis('Alergia ocular (picazón y enrojecimiento)', 'pediatrico', '1 o 2 gotas hasta 4 veces al día',
               d_('Directions: children 6 years of age and older; children under 6 years: ask a doctor'),
               cantidad=2, unidad='gota', veces_dia=4, sitio='ojo', condicion='Desde los 6 años')],
        componentes=['Nafazolina', 'Feniramina'],
        pediatria=('con_dosis', 'Desde los 6 años; en menores, consultar al médico (FDA).', '6 años'),
        conservacion=conserv('Conservar a 20–25 °C, protegido de la luz.', d_('Storage: store at 20-25°C; protect from light')),
        alertas=['Pediamécum (nafazolina): si tras 3–4 días los síntomas siguen o empeoran, reevaluar.'],
    )

    # ---------------------------------------------------------------- fluorometolona
    c = lambda d: cima('fluorometolona', '56132', d)  # noqa: E731  Isopto Flucon 1 mg/ml
    f['fluorometolona'] = ficha(
        'fluorometolona', 'FLUOROMETOLONA', 'Fluorometolona oftálmica 0,1 %', 'corticoide',
        [pres('suspension', '0,1 %', 'ojo', 'F-20888/24', 'F-12259/22', 'F-21677/25')],
        [dosis('Inflamación ocular que responde a corticoides', 'adulto', '1 gota 2 a 4 veces al día; las primeras 24–48 h puede darse cada 4 h',
               c('4.2: adultos y niños mayores de 3 años, 1 gota de 2 a 4 veces al día; primeras 24-48 horas cada 4 horas'),
               cantidad=1, unidad='gota', veces_dia=4, sitio='ojo', duracion='Evitar tratamientos prolongados; retirar de forma gradual'),
         dosis('Inflamación ocular que responde a corticoides', 'pediatrico', '1 gota 2 a 4 veces al día; reducir frecuencia y duración en niños',
               c('4.2: niños mayores de 3 años; se recomienda reducir la frecuencia y la duración en niños'), cantidad=1, unidad='gota', veces_dia=4,
               sitio='ojo', condicion='Mayores de 3 años')],
        pediatria=('con_dosis', 'No establecida en menores de 3 años (CIMA).', '3 años'),
        conservacion=conserv('Desechar 4 semanas después de abrir. No conservar sobre 30 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28),
        administracion={'texto': 'Agitar bien. Si no mejora en 2 días, reevaluar. En glaucoma, limitar a 2 semanas. ' + ESPACIAR, 'fuente': c('4.2')},
        contraindicaciones=CORTICOIDE_OJO,
    )

    # ---------------------------------------------------------------- fluticasona nasal
    c = lambda d: cima('fluticasona', '07434003', d)  # noqa: E731  Avamys 27,5 mcg (furoato)
    f['fluticasona'] = ficha(
        'fluticasona', 'FLUTICASONA', 'Fluticasona nasal', 'corticoide-nasal',
        [pres('spray', '27,5 mcg (furoato) por pulverización', 'nariz', 'F-16784/23', 'F-16477/22', 'F-22559/26', 'F-28280/24', 'FX-424/23'),
         pres('spray', '50 mcg (propionato) por pulverización', 'nariz', 'F-10656/26', 'F-15296/25', 'F-24823/24')],
        [dosis('Rinitis alérgica', 'adulto', '2 pulverizaciones en cada fosa 1 vez al día (110 mcg); al controlar, 1 por fosa (55 mcg)',
               c('4.2: adultos y adolescentes (12 años y mayores), dos pulverizaciones en cada fosa nasal una vez al día'),
               cantidad=2, unidad='pulverizacion', veces_dia=1, sitio='fosa', presentaciones=['nariz-spray-27-5-mcg-furoato'],
               condicion='Adultos y adolescentes desde 12 años'),
         dosis('Rinitis alérgica', 'pediatrico', '1 pulverización en cada fosa 1 vez al día (55 mcg); si no responde, 2 por fosa',
               c('4.2: niños de 6 a 11 años, una pulverización en cada fosa nasal una vez al día'),
               cantidad=1, unidad='pulverizacion', veces_dia=1, sitio='fosa', presentaciones=['nariz-spray-27-5-mcg-furoato'], condicion='6 a 11 años')],
        pediatria=('con_dosis', 'No establecida en menores de 6 años (CIMA).', '6 años'),
        conservacion=conserv('Tras abrir: 2 meses. No refrigerar ni congelar; guardar vertical y con la tapa.', c('6.3: tras la apertura, 2 meses'), dias=60,
                             presentaciones=['nariz-spray-27-5-mcg-furoato']),
        administracion={'texto': 'Solo vía intranasal. Agitar antes de usar; cebar con al menos 6 pulverizaciones la primera vez.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a fluticasona o a algún excipiente (CIMA).'],
        alertas=['No requiere ajuste en ancianos ni en insuficiencia renal o hepática (CIMA).',
                 'Furoato (27,5 mcg) y propionato (50 mcg) de fluticasona no son intercambiables pulverización por pulverización.'],
        discrepancias=[disc('Sal y dosis por pulverización',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: furoato 27,5 mcg/dosis y propionato 50 mcg/dosis'),
                             ('CIMA-TOP-FLUTICASONA-07434003', 'Ficha descargada: Avamys (furoato 27,5 mcg)')],
                            'Pauta solo para 27,5 mcg (furoato)', 'Regla de concentración: el propionato 50 mcg queda sin pauta.')],
    )

    # ---------------------------------------------------------------- ganciclovir
    c = lambda d: cima('ganciclovir', '67075', d)  # noqa: E731  Virgan 1,5 mg/g gel
    p = lambda d: ped('ganciclovir', d)  # noqa: E731
    f['ganciclovir'] = ficha(
        'ganciclovir', 'GANCICLOVIR', 'Ganciclovir gel oftálmico', 'antiviral-antifungico',
        [pres('gel', '0,15 % (1,5 mg/g)', 'ojo', 'F-19120/21')],
        [dosis('Queratitis herpética superficial aguda', 'adulto', '1 gota 5 veces al día hasta la reepitelización completa; luego 1 gota 3 veces al día por 7 días',
               c('4.2.1: 1 gota 5 veces al día hasta la reepitelización corneal completa, después 1 gota 3 veces al día durante 7 días'),
               cantidad=1, unidad='gota', veces_dia=5, sitio='ojo', duracion='Máximo 21 días',
               tambien=[p('1 gota, 5 veces al día hasta la reepitelización corneal completa; después, 1 gota, 3 veces al día durante 7 días')]),
         dosis('Queratitis herpética superficial aguda', 'pediatrico', '1 gota 5 veces al día hasta la reepitelización; luego 1 gota 3 veces al día por 7 días',
               p('Gel oftálmico tópico en la queratitis superficial aguda por herpes simple; duración máxima 21 días'),
               cantidad=1, unidad='gota', veces_dia=5, sitio='ojo', estatus='off_label', condicion='La ficha técnica no lo recomienda en menores de 18 años',
               duracion='Máximo 21 días')],
        pediatria=('con_dosis', 'Ficha técnica: no recomendado en menores de 18 años (sin estudios). Pediamécum da la misma pauta, como off-label.'),
        conservacion=conserv('Después de abrir: 4 semanas.', c('6.3: después de la apertura, 4 semanas'), dias=28),
        administracion={'texto': 'Instilar en el fondo de saco conjuntival inferior del ojo afectado.', 'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a ganciclovir o aciclovir (CIMA).'],
        discrepancias=[disc('Uso pediátrico',
                            [('CIMA-TOP-GANCICLOVIR-67075', 'No recomendado en menores de 18 años'),
                             ('PEDIAMECUM-TOP-GANCICLOVIR', 'Misma pauta que en adultos')],
                            'Ambas: Pediamécum como off-label', 'Decisión de Héctor (31-oct).')],
    )

    # ---------------------------------------------------------------- gatifloxacino + prednisolona (fuente del monofármaco)
    dm('gatifloxacino-prednisolona', 'Etiqueta de gatifloxacino 0,5 % solo (sin prednisolona)')
    ped('prednisolona', 'Prednisolona oral (síndrome nefrótico); sin pauta oftálmica')
    f['gatifloxacino-prednisolona'] = ficha(
        'gatifloxacino-prednisolona', 'GATIFLOXACINO + PREDNISOLONA', 'Gatifloxacino + prednisolona oftálmico', 'antibiotico-corticoide',
        [pres('suspension', NC, 'ojo', 'F-19136/21')], [], componentes=['Gatifloxacino', 'Prednisolona'],
        pediatria=('sin_datos', 'Sin fuente de posología para la combinación.'), sin_pauta=SIN_COMBO,
        discrepancias=[disc('Fuentes descargadas',
                            [('DAILYMED-TOP-GATIFLOXACINO-PREDNISOLONA', 'FDA: gatifloxacino 0,5 % solo'),
                             ('PEDIAMECUM-TOP-PREDNISOLONA', 'Pediamécum: prednisolona oral')],
                            'No se usan', 'Son fichas de un solo componente o de otra vía; no valen para la combinación.')],
    )

    # ---------------------------------------------------------------- gentamicina
    c = lambda d: cima('gentamicina', '52662', d)  # noqa: E731  Oftalmolosa Cusí gentamicina 3 mg/g
    f['gentamicina'] = ficha(
        'gentamicina', 'GENTAMICINA', 'Gentamicina oftálmica 0,3 %', 'antibiotico',
        [pres('unguento', '0,3 %', 'ojo', 'B-2519/25', 'B-2250/22', 'B-889/25'),
         pres('solucion', '0,3 %', 'ojo', 'B-2632/26', 'B-2638/26', 'B-2654/26', 'B-1243/26', 'B-888/25', 'B-2639/26')],
        [dosis('Infección ocular bacteriana', 'adulto', '1 cm de pomada 2 o 3 veces al día', c('4.2.1: en general se aplicará 1 cm de pomada dos o tres veces al día'),
               cantidad=1, unidad='cm', veces_dia=3, sitio='ojo', presentaciones=['ojo-unguento-0-3']),
         dosis('Infección ocular bacteriana', 'pediatrico', '1 cm de pomada 2 o 3 veces al día',
               c('4.2.1: uso en adultos, adolescentes y pacientes pediátricos'), cantidad=1, unidad='cm', veces_dia=3, sitio='ojo',
               presentaciones=['ojo-unguento-0-3'])],
        pediatria=('con_dosis', 'La ficha técnica de la pomada incluye a los pacientes pediátricos.'),
        conservacion=conserv('Desechar 4 semanas después de abrir. No conservar sobre 25 °C.', c('6.3: desechar 4 semanas después de la primera apertura'), dias=28,
                             presentaciones=['ojo-unguento-0-3']),
        administracion={'texto': ESPACIAR, 'fuente': c('4.2.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a gentamicina u otros aminoglucósidos (CIMA).'],
        alertas=['La solución 0,3 % no tiene ficha técnica en las fuentes consultadas: sin pauta.'],
    )
    ped('gentamicina', 'Sin pauta tópica oftálmica')

    # ---------------------------------------------------------------- gramicidina + neomicina + polimixina B
    c = lambda d: cima('gramicidina-neomicina-polimixina-b', '45030', d)  # noqa: E731  Oftalmowell colirio
    f['gramicidina-neomicina-polimixina-b'] = ficha(
        'gramicidina-neomicina-polimixina-b', 'GRAMICIDINA + NEOMICINA + POLIMIXINA B', 'Gramicidina + neomicina + polimixina B oftálmica', 'antibiotico',
        [pres('solucion', NC, 'ojo', 'B-519/24')],
        [dosis('Conjuntivitis bacteriana, queratitis, úlcera corneal', 'adulto',
               '1 o 2 gotas cada 2–4 h durante el día los 2 primeros días; luego 1 o 2 gotas cada 4–6 h hasta resolver',
               c('4.2: durante los dos primeros días, una o dos gotas cada 2-4 horas; posteriormente cada 4-6 horas'),
               cantidad=2, unidad='gota', sitio='ojo', duracion='Hasta 2 días después de resolver; no más de 7 días sin control'),
         dosis('Conjuntivitis bacteriana, queratitis, úlcera corneal', 'pediatrico', 'Igual que en adultos',
               c('4.2 Población pediátrica: niños mayores de dos años a la misma dosis de adultos'), cantidad=2, unidad='gota', sitio='ojo',
               condicion='Mayores de 2 años; no recomendado en neonatos ni menores de 2')],
        componentes=['Gramicidina', 'Neomicina', 'Polimixina B'],
        pediatria=('con_dosis', 'Mayores de 2 años igual que adultos; no recomendado en neonatos ni menores de 2 años (CIMA).', '2 años'),
        conservacion=conserv('1 mes tras la primera apertura (la calculadora usa 28 días). Bajo 25 °C, protegido de la luz.', c('6.3: 1 mes tras la primera apertura'), dias=28),
        administracion={'texto': ESPACIAR, 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Sensibilidad cruzada con framicetina, kanamicina, gentamicina y antibióticos relacionados (CIMA).',
                            'Cuando el producto pueda llegar a fluidos intraoculares (CIMA).'],
        alertas=['Insuficiencia renal: precaución, puede haber absorción sistémica de neomicina (CIMA).',
                 'Oftalmowell (CIMA) es la misma asociación; el registro chileno no indica concentración en el nombre.'],
    )

    # ---------------------------------------------------------------- hialuronato
    d_ = lambda d: dm('hialuronato', d)  # noqa: E731
    f['hialuronato'] = ficha(
        'hialuronato', 'HIALURONATO', 'Hialuronato de sodio oftálmico 0,4 % (lágrima artificial)', 'lubricante-ocular',
        [pres('solucion', '0,4 %', 'ojo', 'FX-374/26')],
        [dosis('Sequedad ocular', 'adulto', '1 o 2 gotas según necesidad', d_('Directions: instill 1 or 2 drops as needed'),
               cantidad=2, unidad='gota', sitio='ojo')],
        pediatria=('sin_datos', 'La etiqueta no trae indicaciones por edad.'),
        conservacion=conserv('Usar dentro de 30 días después de abrir. Conservar a 15–30 °C, protegido del sol.', d_('Warnings: use within 30 days after opening'), dias=30),
        alertas=['Fuente débil: etiqueta FDA de un distribuidor de venta libre que no indica la concentración. Tómalo como orientación.'],
    )

    # ---------------------------------------------------------------- ipratropio nasal
    c = lambda d: cima('ipratropio', '61848', d)  # noqa: E731  Atrovent nasal 0,30 mg/ml (21 mcg/pulsación)
    p = lambda d: ped('ipratropio', d)  # noqa: E731
    f['ipratropio'] = ficha(
        'ipratropio', 'IPRATROPIO', 'Ipratropio nasal', 'anticolinergico',
        [pres('spray', '21 mcg por pulverización', 'nariz', 'F-18345/25'), pres('spray', '42 mcg por pulverización', 'nariz', 'F-24099/23')],
        [dosis('Rinorrea', 'adulto', '2 pulverizaciones en cada fosa (42 mcg por fosa) 2 o 3 veces al día',
               c('4.2: adultos y adolescentes mayores de 12 años, 2 pulverizaciones en cada fosa nasal (42 mcg/fosa nasal), 2-3 veces al día'),
               cantidad=2, unidad='pulverizacion', veces_dia=3, sitio='fosa', presentaciones=['nariz-spray-21-mcg'], condicion='Desde los 12 años',
               tambien=[p('>12 años: 42 µg en cada fosa nasal de 2-3 veces al día')]),
         dosis('Rinorrea', 'pediatrico', '2 pulverizaciones en cada fosa (42 mcg por fosa) 2 veces al día',
               c('4.2: niños de 6 a 12 años, 2 pulverizaciones en cada fosa nasal (42 mcg/fosa nasal), 2 veces al día'),
               cantidad=2, unidad='pulverizacion', veces_dia=2, sitio='fosa', presentaciones=['nariz-spray-21-mcg'], condicion='6 a 12 años',
               tambien=[p('6-12 años: 42 µg en cada fosa nasal 2 veces al día')])],
        pediatria=('con_dosis', 'Desde los 6 años (CIMA, Pediamécum).', '6 años'),
        conservacion=conserv('No usar después de 12 meses de abierto.', c('6.3: no utilizar después de 12 meses de abrir el envase'), dias=365,
                             presentaciones=['nariz-spray-21-mcg']),
        contraindicaciones=['Hipersensibilidad a sustancias análogas a la atropina (CIMA).'],
        alertas=['La presentación de 42 mcg por pulverización no tiene ficha: la dosis en microgramos sería 1 pulverización por fosa, pero no se muestra como pauta.'],
    )

    # ---------------------------------------------------------------- ketorolaco (concentración distinta)
    cima('ketorolaco', '61690', 'Acular 5 mg/ml: 1 gota 3 veces al día desde 24 h antes de la cirugía, 3-4 semanas')
    f['ketorolaco'] = ficha(
        'ketorolaco', 'KETOROLACO', 'Ketorolaco oftálmico 0,4 %', 'aine',
        [pres('solucion', '0,4 %', 'ojo', 'F-14888/25')], [],
        pediatria=('no_establecida', 'Sin fuente para 0,4 %; la ficha de 0,5 % no tiene uso pediátrico relevante.'),
        sin_pauta='En Chile está registrado al 0,4 % (Acular LS); la ficha disponible es del 0,5 % (Acular, CIMA). Por la regla de concentración no se muestra su pauta.',
        contraindicaciones=['Sensibilidad previa a ácido acetilsalicílico u otros AINE (CIMA).'],
        discrepancias=[disc('Concentración',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: 0,4 %'), ('CIMA-TOP-KETOROLACO-61690', 'CIMA: Acular 5 mg/ml (0,5 %), 1 gota 3 veces al día')],
                            'Sin pauta', 'Decisión de Héctor (31-oct).')],
    )

    # ---------------------------------------------------------------- ketotifeno
    c = lambda d: cima('ketotifeno', '63616', d)  # noqa: E731  Zaditen 0,25 mg/ml unidosis
    f['ketotifeno'] = ficha(
        'ketotifeno', 'KETOTIFENO', 'Ketotifeno oftálmico', 'antialergico',
        [pres('solucion', '0,025 %', 'ojo', 'F-14977/25', 'F-21952/25'), pres('solucion', '0,05 %', 'ojo', 'F-21531/24', 'F-2555/24')],
        [dosis('Conjuntivitis alérgica estacional', 'adulto', '1 gota en el saco conjuntival 2 veces al día', c('4.2: una gota de Zaditen en el saco conjuntival, dos veces al día'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', presentaciones=['ojo-solucion-0-025']),
         dosis('Conjuntivitis alérgica estacional', 'pediatrico', '1 gota 2 veces al día', c('4.2: niños a partir de 3 años de edad'),
               cantidad=1, unidad='gota', veces_dia=2, sitio='ojo', presentaciones=['ojo-solucion-0-025'], condicion='Desde los 3 años')],
        pediatria=('con_dosis', 'No establecida en menores de 3 años (CIMA).', '3 años'),
        conservacion=conserv('La ficha es de envases unidosis: usar de inmediato tras abrir; con el blíster abierto, 28 días. '
                             'No hay dato de validez para frasco multidosis.', c('6.3 Periodo de validez'), presentaciones=['ojo-solucion-0-025']),
        contraindicaciones=['Hipersensibilidad a ketotifeno o a algún excipiente (CIMA).'],
        discrepancias=[disc('Concentración 0,05 %',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: 0,025 % y 0,05 % (Oftaler Forte, Kenaler)'),
                             ('CIMA-TOP-KETOTIFENO-63616', 'CIMA: Zaditen 0,25 mg/ml (0,025 %)')],
                            'Pauta solo para 0,025 %', 'Regla de concentración.')],
    )

    # ---------------------------------------------------------------- latanoprost
    c = lambda d: cima('latanoprost', '1231763001', d)  # noqa: E731  Catiolanze 50 mcg/ml emulsión unidosis
    sol = ['F-29700/26', 'F-24272/23', 'F-15625/26', 'F-26909/22', 'F-19214/22', 'F-28401/24', 'F-23582/22', 'F-24791/24', 'FX-275/23',
           'FX-307/24', 'F-3393/25', 'FX-195/21', 'FX-214/22', 'F-24966/24', 'F-7585/26', 'F-21752/25', 'F-56/22']
    f['latanoprost'] = ficha(
        'latanoprost', 'LATANOPROST', 'Latanoprost oftálmico 0,005 %', 'antiglaucomatoso',
        [pres('solucion', '0,005 %', 'ojo', *sol), pres('emulsion', '0,005 %', 'ojo', 'F-25281/25'), pres('solucion', NC, 'ojo', 'FX-308/24')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 1 vez al día, de preferencia por la noche (no más)',
               c('4.2: una gota en el (los) ojo(s) afectado(s) una vez al día; óptimo por la noche; no exceder de una vez al día'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo', presentaciones=['ojo-solucion-0-005', 'ojo-emulsion-0-005']),
         dosis('Glaucoma pediátrico', 'pediatrico', 'Igual que en adultos: 1 gota 1 vez al día',
               c('4.2: Catiolanze se puede administrar a pacientes pediátricos a partir de 4 años con la misma posología'),
               cantidad=1, unidad='gota', veces_dia=1, sitio='ojo', presentaciones=['ojo-emulsion-0-005'], condicion='Desde los 4 años; dato de la emulsión')],
        pediatria=('con_dosis', 'Emulsión: desde los 4 años (CIMA). Para la solución no hay fuente pediátrica.', '4 años (emulsión)'),
        conservacion=conserv('Emulsión unidosis sin conservantes: desechar inmediatamente después de usar. Bajo 30 °C.', c('6.3/6.4'), presentaciones=['ojo-emulsion-0-005']),
        administracion={'texto': 'Comprimir el saco lagrimal en el canto interno 1 minuto tras cada gota. Retirar lentes de contacto y esperar 15 minutos. '
                                 'Separar 5 minutos de otros colirios.', 'fuente': c('4.2 Forma de administración')},
        contraindicaciones=['Hipersensibilidad a latanoprost o a algún excipiente (CIMA).'],
        alertas=['La ficha consultada es de la emulsión unidosis (Catiolanze); para los frascos multidosis chilenos no hay dato de validez tras abrir.'],
    )

    # ---------------------------------------------------------------- latanoprost + timolol
    c = lambda d: cima('latanoprost-timolol', '64187', d)  # noqa: E731  Xalacom 50 mcg + 5 mg/ml
    f['latanoprost-timolol'] = ficha(
        'latanoprost-timolol', 'LATANOPROST + TIMOLOL', 'Latanoprost + timolol oftálmico', 'antiglaucomatoso',
        [pres('solucion', NC, 'ojo', 'F-23312/22', 'F-24787/24', 'FX-213/22', 'F-11937/22', 'F-25053/24', 'FX-309/24', 'F-17877/24', 'F-25497/25', 'F-11936/22')],
        [dosis('Glaucoma de ángulo abierto / hipertensión ocular', 'adulto', '1 gota en el ojo afectado 1 vez al día (no más)',
               c('4.2: una gota una vez al día; no debe exceder de una gota una vez al día'), cantidad=1, unidad='gota', veces_dia=1, sitio='ojo')],
        componentes=['Latanoprost', 'Timolol'],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas en niños y adolescentes (CIMA).'),
        conservacion=conserv('Antes de abrir: en refrigerador (2–8 °C). Después de abrir: bajo 25 °C y usar dentro de 4 semanas. Proteger de la luz.',
                             c('6.3/6.4: antes de la primera apertura conservar en nevera; después, máximo 4 semanas'), dias=28),
        administracion={'texto': 'Retirar lentes de contacto y esperar 15 minutos. Ocluir o cerrar los párpados 2 minutos. Separar 5 minutos de otros colirios.',
                        'fuente': c('4.2 Forma de administración')},
        contraindicaciones=BETABLOQ,
        alertas=['Cadena de frío: el frasco cerrado va en el refrigerador (CIMA, Xalacom).',
                 'Xalacom es 50 mcg/ml + 5 mg/ml; los registros chilenos no indican concentración en el nombre.'],
    )

    # ---------------------------------------------------------------- levofloxacino (concentración distinta)
    dm('levofloxacino', 'Levofloxacino 1,5 %: régimen intensivo de úlcera corneal')
    f['levofloxacino'] = ficha(
        'levofloxacino', 'LEVOFLOXACINO', 'Levofloxacino oftálmico 0,5 %', 'antibiotico',
        [pres('solucion', '0,5 %', 'ojo', 'F-28814/25')], [],
        pediatria=('no_establecida', 'Sin fuente para 0,5 %; la etiqueta de 1,5 % no lo establece en menores de 6 años.'),
        sin_pauta='En Chile está registrado al 0,5 % (Landax); la única fuente es la etiqueta FDA del 1,5 % para úlcera corneal, con un régimen '
                  'intensivo que no aplica al colirio de 0,5 %. Por la regla de concentración no se muestra.',
        contraindicaciones=['Hipersensibilidad a levofloxacino u otras quinolonas (FDA).'],
        discrepancias=[disc('Concentración',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: 0,5 %'),
                             ('DAILYMED-TOP-LEVOFLOXACINO', 'FDA: 1,5 %, días 1-3 cada 30 min a 2 h despierto y de noche; luego cada 1-4 h')],
                            'Sin pauta', 'Decisión de Héctor (31-oct).')],
    )

    # ---------------------------------------------------------------- loteprednol
    d_ = lambda d: dm('loteprednol', d)  # noqa: E731  0,2 %
    f['loteprednol'] = ficha(
        'loteprednol', 'LOTEPREDNOL', 'Loteprednol oftálmico', 'corticoide',
        [pres('suspension', '0,2 %', 'ojo', 'F-15929/22', 'F-17918/25'), pres('suspension', '0,5 %', 'ojo', 'F-21664/25', 'F-15780/21')],
        [dosis('Conjuntivitis alérgica estacional', 'adulto', '1 gota en el ojo afectado 4 veces al día', d_('DOSAGE: one drop instilled into the affected eye(s) four times daily'),
               cantidad=1, unidad='gota', veces_dia=4, sitio='ojo', presentaciones=['ojo-suspension-0-2'])],
        pediatria=('no_establecida', 'Seguridad y eficacia no establecidas en niños (FDA).'),
        conservacion=conserv('Conservar vertical a 15–25 °C; no congelar. La etiqueta no fija validez tras abrir.', d_('Storage: store upright between 15°C to 25°C; do not freeze'),
                             presentaciones=['ojo-suspension-0-2']),
        administracion={'texto': 'Agitar enérgicamente antes de usar.', 'fuente': d_('SHAKE VIGOROUSLY BEFORE USING')},
        contraindicaciones=['Queratitis por herpes simple epitelial, vaccinia, varicela y la mayoría de las virosis de córnea y conjuntiva (FDA).',
                            'Infección micobacteriana o fúngica del ojo (FDA).'],
        discrepancias=[disc('Concentración 0,5 %',
                            [('ISP-REGISTRO-TOPICOS', 'Chile: 0,2 % (Oftol, Talof) y 0,5 % (Oftol Forte, Disalot)'),
                             ('DAILYMED-TOP-LOTEPREDNOL', 'FDA: suspensión 0,2 %')],
                            'Pauta solo para 0,2 %', 'Regla de concentración.')],
    )

    # ---------------------------------------------------------------- loteprednol + tobramicina
    d_ = lambda d: dm('loteprednol-tobramicina', d)  # noqa: E731  0,5 % + 0,3 %
    ped('tobramicina', 'Solo vía sistémica (endocarditis); sin pauta oftálmica')
    f['loteprednol-tobramicina'] = ficha(
        'loteprednol-tobramicina', 'LOTEPREDNOL + TOBRAMICINA', 'Loteprednol + tobramicina oftálmico', 'antibiotico-corticoide',
        [pres('suspension', NC, 'ojo', 'B-2152/25')],
        [dosis('Inflamación ocular con infección bacteriana o riesgo de ella', 'adulto',
               '1 o 2 gotas en el saco conjuntival cada 4–6 h; las primeras 24–48 h, hasta cada 1–2 h. Bajar la frecuencia al mejorar',
               d_('2.1: one or two drops every four to six hours; during the initial 24 to 48 hours, every one to two hours'),
               cantidad=2, unidad='gota', veces_dia=6, sitio='ojo')],
        componentes=['Loteprednol', 'Tobramicina'],
        pediatria=('no_establecida', 'En ensayos de 0 a 6 años no demostró eficacia (FDA).'),
        conservacion=conserv('Conservar vertical a 15–25 °C; no congelar. Una vez abierto puede usarse hasta la fecha de vencimiento.',
                             d_('Storage: after opening, can be used until the expiration date')),
        administracion={'texto': 'Agitar enérgicamente. No indicar más de 20 ml de inicio sin reevaluar.', 'fuente': d_('2.2 Prescription guideline')},
        contraindicaciones=['Virosis de córnea y conjuntiva (incluido herpes simple), infección micobacteriana o fúngica del ojo (FDA).'],
        alertas=['La etiqueta FDA es de 0,5 % + 0,3 %; el registro chileno (Oftol Plus) no indica concentración en el nombre.',
                 'Para calcular se usa la frecuencia de cada 4 h (6 veces al día).'],
    )
    return f
