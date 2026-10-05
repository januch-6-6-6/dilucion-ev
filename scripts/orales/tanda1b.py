"""Orales, tanda 1b: antiinfecciosos (15 fichas: antibióticos, antiparasitario, antivirales y antifúngicos).

Cada cifra sale de datos/crudos/orales/ (fichas CIMA, Pediamécum, ficha EMC de flucloxacilina y arsenal de APS
de Atacama); la tabla «cifra → archivo:línea» está en .superpowers/sdd/2026-10-05-orales-v1/task-12b-report.md.
"""
from .comun import (ARSENAL, discrepancia, dosis, ficha_oral, fu, fuente_arsenal, fuente_cima, fuente_externa,
                    fuente_pediamecum_oral, pres)


def _ped(k):
    return f'PEDIAMECUM-{k.upper()}'


# ---------------------------------------------------------------- referencias
AMX_C = 'CIMA-AMOXICILINA-62880'  # Amoxicilina Cinfa 1000 mg comprimidos
AMX_S = 'CIMA-AMOXICILINA-64117'  # Amoxicilina Cinfa 1000 mg polvo para suspensión oral en sobres
AMC_C = 'CIMA-AMOXICILINA-CLAVULANICO-59515'  # Augmentine 875/125 comprimidos (7:1)
AMC_S = 'CIMA-AMOXICILINA-CLAVULANICO-59518'  # Augmentine 875/125 sobre (7:1)
CFD_C = 'CIMA-CEFADROXILO-55730'  # Duracef 500 mg cápsulas
CFD_S = 'CIMA-CEFADROXILO-55731'  # Duracef 250 mg/5 ml suspensión
FLX = 'EMC-FLUCLOXACILINA'  # Flucloxacillin 500 mg capsules (EMC, Reino Unido)
CLA_C = 'CIMA-CLARITROMICINA-67638'  # Claritromicina Cinfa 250 mg comprimidos
CLA_S = 'CIMA-CLARITROMICINA-66388'  # Claritromicina Sandoz 25 mg/ml granulado para suspensión
AZI_C = 'CIMA-AZITROMICINA-65600'  # Azitromicina Cinfa 500 mg comprimidos
AZI_S = 'CIMA-AZITROMICINA-65601'  # Azitromicina Cinfa 500 mg polvo para suspensión oral (sobre)
SXT = 'CIMA-COTRIMOXAZOL'  # Septrin Forte 160/800 mg comprimidos (NO Balsoprim)
CIP_S = 'CIMA-CIPROFLOXACINO-62602'  # Cetraxal 100 mg/ml suspensión oral
CIP_C = 'CIMA-CIPROFLOXACINO-62768'  # Ciprofloxacino Cinfa 250 mg comprimidos
NIT_C = 'CIMA-NITROFURANTOINA-22974'  # Furantoína 50 mg comprimidos
NIT_S = 'CIMA-NITROFURANTOINA-34388'  # Furantoína 10 mg/ml suspensión oral
MTZ_C = 'CIMA-METRONIDAZOL-62223'  # Metronidazol Normon 250 mg comprimidos
MTZ_S = 'CIMA-METRONIDAZOL-47656'  # Flagyl 125 mg/5 ml suspensión oral
MEB_C = 'CIMA-MEBENDAZOL-51200'  # Lomper 100 mg comprimidos
MEB_S = 'CIMA-MEBENDAZOL-53775'  # Lomper 20 mg/ml suspensión oral
FLU_C = 'CIMA-FLUCONAZOL-58804'  # Diflucan 100 mg cápsulas
FLU_S = 'CIMA-FLUCONAZOL-59672'  # Diflucan 10 mg/ml polvo para suspensión oral
NIS = 'CIMA-NISTATINA'  # Mycostatin 100.000 UI/ml suspensión oral
TER = 'CIMA-TERBINAFINA'  # Lamisil 250 mg comprimidos
ACI_C = 'CIMA-ACICLOVIR-84468'  # Aciclovir Cinfa 200 mg comprimidos
ACI_S = 'CIMA-ACICLOVIR-59226'  # Zovirax 400 mg/5 ml suspensión oral

POBLACION_OFF_LABEL = 'Se muestran las pautas pediátricas de Pediamécum, marcadas como uso fuera de ficha técnica (off-label)'


def fuentes():
    return [
        fuente_cima('amoxicilina', '62880', 'Amoxicilina Cinfa 1000 mg comprimidos EFG', varios=True),
        fuente_cima('amoxicilina', '64117', 'Amoxicilina Cinfa 1000 mg polvo para suspensión oral en sobres EFG', varios=True),
        fuente_pediamecum_oral('amoxicilina', 'Amoxicilina', anio=2021),
        fuente_cima('amoxicilina-clavulanico', '59515', 'Augmentine 875/125 comprimidos', varios=True),
        fuente_cima('amoxicilina-clavulanico', '59518', 'Augmentine 875/125 sobre', varios=True),
        fuente_pediamecum_oral('amoxicilina-clavulanico', 'Amoxicilina clavulánico', anio=2021),
        fuente_cima('cefadroxilo', '55730', 'Duracef 500 mg cápsulas duras', varios=True),
        fuente_cima('cefadroxilo', '55731', 'Duracef 250 mg/5 ml polvo para suspensión oral', varios=True),
        fuente_pediamecum_oral('cefadroxilo', 'Cefadroxilo', anio=2021),
        fuente_externa(FLX, 'Summary of Product Characteristics: Flucloxacillin 500 mg capsules, hard (Brown & Burk UK Ltd)',
                       'Electronic Medicines Compendium (Reino Unido)', 'https://www.medicines.org.uk/emc/product/12636/smpc', 2025),
        fuente_cima('claritromicina', '67638', 'Claritromicina Cinfa 250 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('claritromicina', '66388', 'Claritromicina Sandoz 25 mg/ml granulado para suspensión oral', varios=True),
        fuente_pediamecum_oral('claritromicina', 'Claritromicina', anio=2024),
        fuente_cima('azitromicina', '65600', 'Azitromicina Cinfa 500 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('azitromicina', '65601', 'Azitromicina Cinfa 500 mg polvo para suspensión oral EFG', varios=True),
        fuente_pediamecum_oral('azitromicina', 'Azitromicina', anio=2021),
        fuente_cima('cotrimoxazol', '58501', 'Septrin Forte 160 mg/800 mg comprimidos'),
        fuente_pediamecum_oral('cotrimoxazol', 'Cotrimoxazol', anio=2026),
        fuente_cima('ciprofloxacino', '62602', 'Cetraxal 100 mg/ml suspensión oral', varios=True),
        fuente_cima('ciprofloxacino', '62768', 'Ciprofloxacino Cinfa 250 mg comprimidos recubiertos EFG', varios=True),
        fuente_pediamecum_oral('ciprofloxacino', 'Ciprofloxacino', anio=2020),
        fuente_cima('nitrofurantoina', '22974', 'Furantoína 50 mg comprimidos', varios=True),
        fuente_cima('nitrofurantoina', '34388', 'Furantoína 10 mg/ml suspensión oral', varios=True),
        fuente_pediamecum_oral('nitrofurantoina', 'Nitrofurantoína', anio=2020),
        fuente_cima('metronidazol', '62223', 'Metronidazol Normon 250 mg comprimidos EFG', varios=True),
        fuente_cima('metronidazol', '47656', 'Flagyl 125 mg/5 ml suspensión oral', varios=True),
        fuente_pediamecum_oral('metronidazol', 'Metronidazol', anio=2020),
        fuente_cima('mebendazol', '51200', 'Lomper 100 mg comprimidos', varios=True),
        fuente_cima('mebendazol', '53775', 'Lomper 20 mg/ml suspensión oral', varios=True),
        fuente_pediamecum_oral('mebendazol', 'Mebendazol', anio=2020),
        fuente_cima('fluconazol', '58804', 'Diflucan 100 mg cápsulas duras', varios=True),
        fuente_cima('fluconazol', '59672', 'Diflucan 10 mg/ml polvo para suspensión oral', varios=True),
        fuente_pediamecum_oral('fluconazol', 'Fluconazol', anio=2020),
        fuente_cima('nistatina', '28262', 'Mycostatin 100.000 UI/ml suspensión oral'),
        fuente_pediamecum_oral('nistatina', 'Nistatina', anio=2020),
        fuente_cima('terbinafina', '59435', 'Lamisil 250 mg comprimidos'),
        fuente_pediamecum_oral('terbinafina', 'Terbinafina', anio=2021),
        fuente_cima('aciclovir', '84468', 'Aciclovir Cinfa 200 mg comprimidos EFG', varios=True),
        fuente_cima('aciclovir', '59226', 'Zovirax 400 mg/5 ml suspensión oral', varios=True),
        fuente_pediamecum_oral('aciclovir', 'Aciclovir', anio=2021),
        fuente_arsenal(),
    ]


# ---------------------------------------------------------------- penicilinas
def amoxicilina():
    P = _ped('amoxicilina')
    presentaciones = [
        pres('comprimido-1-g', 'comprimido', mg=1000, partible='no',
             fuente=fu(AMX_C, 'Amoxicilina Cinfa 1000 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('sobre-1-g', 'sobre', mg=1000, partible='no', fuente=fu(AMX_S, 'Amoxicilina Cinfa 1000 mg polvo para suspensión oral en sobres')),
        pres('capsula-500-mg', 'capsula', mg=500, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: AMOXICILINA CINFA 500 MG CÁPSULAS DURAS EFG (el arsenal de APS también lista cápsula 500 mg)')),
        pres('suspension-50-mg-ml', 'suspension', mg_ml=50,
             fuente=fu(P, 'Presentaciones de Pediamécum: AMOXICILINA NORMON 250 MG/5 ML POLVO PARA SUSPENSIÓN ORAL EFG (= 50 mg por 1 ml)')),
        pres('suspension-100-mg-ml', 'suspension', mg_ml=100,
             fuente=fu(ARSENAL, 'Grupo 06.02.01: Amoxicilina, Polvo para suspensión oral 500 mg/5 mL (= 100 mg por 1 ml)')),
    ]
    dosis_ = [
        dosis('Sinusitis, cistitis, pielonefritis, bacteriuria asintomática del embarazo y abscesos dentales (adultos y niños ≥40 kg)',
              'adulto', 'fija', 'mg',
              min=250, max=500, tomas=3, intervalo_h=8,
              texto='De 250 mg a 500 mg cada 8 horas o de 750 mg a 1 g cada 12 horas. Infecciones graves: de 750 mg a 1 g cada 8 horas',
              fuente=fu(AMX_C, '4.2 Adultos y niños ≥40 kg: "De 250 mg a 500 mg cada 8 horas o de 750 mg a 1 g cada 12 horas. Para infecciones graves, de 750 mg a 1 g cada 8 horas"')),
        dosis('Otitis media aguda (adultos y niños ≥40 kg)', 'adulto', 'fija', 'mg', min=500, max=500, tomas=3, intervalo_h=8,
              condicion='Alternativa: de 750 mg a 1 g cada 12 horas. Infecciones graves: de 750 mg a 1 g cada 8 horas durante 10 días',
              texto='500 mg cada 8 horas, o de 750 mg a 1 g cada 12 horas; infecciones graves de 750 mg a 1 g cada 8 horas durante 10 días',
              fuente=fu(AMX_C, '4.2 Adultos y niños ≥40 kg, fila "Otitis media aguda": "500 mg cada 8 horas, de 750 mg a 1 g cada 12 horas. '
                               'Para infecciones graves, de 750 mg a 1 g cada 8 horas, durante 10 días"')),
        dosis('Neumonía adquirida en la comunidad, amigdalitis y faringitis estreptocócica, exacerbación de bronquitis crónica (adultos y niños ≥40 kg)',
              'adulto', 'fija', 'mg', min=500, max=1000, tomas=3, intervalo_h=8, texto='De 500 mg a 1 g cada 8 horas',
              fuente=fu(AMX_C, '4.2 Adultos y niños ≥40 kg: "De 500 mg a 1 g cada 8 horas"')),
        dosis('Infecciones habituales (niños <40 kg)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=25, max=50, tomas=3,
              intervalo_h=8,
              condicion='La ficha CIMA admite de 20 a 90 mg/kg/día en dosis divididas según la indicación (sinusitis, otitis, neumonía, '
                        'cistitis, pielonefritis, abscesos dentales). Los niños de 40 kg o más reciben la dosis de adulto',
              texto='25-50 mg/kg/día repartidos cada 8 horas',
              fuente=fu(P, 'Dosis: "Niños de menos de 40 kg: 25-50 mg/kg/día cada 8 horas"; CIMA 62880 4.2: "De 20 a 90 mg/kg/día en dosis divididas"')),
        dosis('Otitis media, sinusitis o neumonía de probable causa neumocócica con resistencia (niños <40 kg)', 'pediatrico', 'por_peso',
              'mg/kg', base='dia', min=80, max=90, tomas=3, intervalo_h=8,
              condicion='CIMA admite hasta 90 mg/kg/día; con la dosis en el rango superior, la ficha sugiere considerar pautas de dos veces al día. '
                        'Duración: 10 días en <2 años y 5-7 días en >2 años (sinusitis 7-10 días)',
              texto='80-90 mg/kg/día en tres dosis al día',
              fuente=fu(P, '"Infecciones respiratorias (otitis media aguda, sinusitis, neumonía) de probable causa neumocócica ... 80-90 mg/kg/día en tres dosis al día"')),
        dosis('Faringoamigdalitis por S. pyogenes (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=40, max=50, tomas=2,
              intervalo_h=12, tope_toma=(500, 'mg'), tope_dia=(1000, 'mg'),
              condicion='Durante 10 días. Pediamécum también da 50 mg/kg/día en 2-3 dosis; CIMA, 40-90 mg/kg/día en amigdalitis y faringitis',
              texto='40-50 mg/kg/día cada 12 horas (o cada 24 h); máximo 500 mg cada 12 h o 1 g cada 24 h, durante 10 días',
              fuente=fu(P, '"faringoamigdalitis por S. pyogenes (40-50 mg/kg/día cada 12 o 24 h; máximo 500 mg/12 h o 1 g/24 h) durante 10 días"')),
    ]
    disc = [
        discrepancia('Dosis pediátrica en faringoamigdalitis estreptocócica',
                     [(AMX_C, 'hasta 90 mg/kg/día: "De 40 a 90 mg/kg/día en dosis divididas" en amigdalitis y faringitis (CIMA)'),
                      (P, 'hasta 50 mg/kg/día: 40-50 mg/kg/día cada 12 o 24 h, máximo 500 mg/12 h o 1 g/24 h (Pediamécum)')],
                     '50 mg/kg/día, con máximo de 500 mg por toma',
                     'Mismo régimen y población: se muestra la cifra más baja (Pediamécum), que además trae tope en mg.'),
    ]
    alertas = [
        'Las pautas de 25-50 y 80-90 mg/kg/día no traen tope en mg en las fuentes. Pediamécum fija un máximo de 150 mg/kg/día (40 mg/kg/día en '
        'menores de 2 meses, cada 12 h) y, para niños de más de 40 kg, una dosis oral máxima de 6 g/día. Como referencia, la dosis de adulto '
        'de CIMA es de 250-500 mg cada 8 h o de 750 mg a 1 g cada 12 h (hasta 1 g cada 8 h en infecciones graves).',
        'Cistitis aguda del adulto: 3 g dos veces al día durante un día; profilaxis de endocarditis: 2 g en dosis única (niños 50 mg/kg) '
        '30-60 minutos antes del procedimiento (CIMA 62880). No se cargan como pautas aparte.',
        'Enfermedad de Lyme y fiebre tifoidea tienen pautas propias (CIMA: hasta 4 g/día en etapa temprana y 6 g/día en la tardía en adultos; '
        'niños 100 mg/kg/día en tres dosis en fiebre tifoidea); no se cargan.',
        'Dos concentraciones de suspensión (50 y 100 mg/ml): confirmar la del frasco antes de calcular el volumen.',
        'Evitar en sospecha de mononucleosis infecciosa (erupción morbiliforme) (CIMA, 4.4).',
    ]
    return ficha_oral(
        'amoxicilina', 'Amoxicilina', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral, tragar con agua. La absorción de amoxicilina no se ve afectada por los alimentos.',
            'fuente': fu(AMX_C, '4.2 Forma de administración'),
        },
        comerciales=['Amoxicilina Cinfa'], discrepancias=disc,
        renal='Filtrado >30 ml/min: sin ajuste. 10-30 ml/min: adultos y niños ≥40 kg, máximo 500 mg dos veces al día; niños <40 kg, 15 mg/kg '
              'dos veces al día (máximo 500 mg dos veces al día). <10 ml/min: adultos, máximo 500 mg/día; niños <40 kg, 15 mg/kg en dosis única '
              'diaria (máximo 500 mg). Hemodiálisis (fila «Adultos y niños ≥40 kg» de la ficha): 15 mg/kg/día en dosis única, con una dosis adicional de 15 mg/kg antes y otra tras la sesión. '
              'Diálisis peritoneal: máximo 500 mg/día.',
        hepatico='Dosificar con precaución y monitorizar la función hepática a intervalos regulares.',
        fuente_ajuste=fu(AMX_C, '4.2 Insuficiencia renal (tabla por filtrado glomerular), hemodiálisis, diálisis peritoneal e insuficiencia hepática'),
        alertas=alertas,
    )


def amoxicilina_clavulanico():
    P = _ped('amoxicilina-clavulanico')
    presentaciones = [
        pres('comprimido-875-125-mg-7-1', 'comprimido', mg=875, partible='no',
             fuente=fu(AMC_C, 'Augmentine 875/125 comprimidos, proporción 7:1; cantidad en mg de amoxicilina (125 mg de clavulánico). '
                              '"los comprimidos no se deben partir" (4.2.1)')),
        pres('sobre-875-125-mg-7-1', 'sobre', mg=875, partible='no',
             fuente=fu(AMC_S, 'Augmentine 875/125 sobre, proporción 7:1; cantidad en mg de amoxicilina. Disolver en medio vaso de agua (4.2.2)')),
        pres('comprimido-500-125-mg-4-1', 'comprimido', mg=500, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: AUGMENTINE 500 MG/125 MG COMPRIMIDOS RECUBIERTOS CON PELÍCULA (proporción 4:1; '
                          'cantidad en mg de amoxicilina). El arsenal de APS también lista el comprimido 500 + 125 mg')),
        pres('suspension-100-12-5-mg-ml-8-1', 'suspension', mg_ml=100,
             fuente=fu(P, 'Presentaciones de Pediamécum: AUGMENTINE 100mg/ml + 12,5 mg/ml POLVO PARA SUSPENSION ORAL (proporción 8:1; '
                          'concentración en mg de amoxicilina por 1 ml)')),
        pres('suspension-250-62-5-mg-5-ml-4-1', 'suspension', mg_ml=50,
             fuente=fu(P, 'Presentaciones de Pediamécum: AMOXICILINA/ACIDO CLAVULANICO VIATRIS 250 MG/5ML + 62,5 MG/5 ML (proporción 4:1; '
                          '= 50 mg de amoxicilina por 1 ml). El arsenal de APS también lista 250 + 62,5 mg/5 mL')),
        pres('suspension-125-31-25-mg-5-ml-4-1', 'suspension', mg_ml=25,
             fuente=fu(P, 'Presentaciones de Pediamécum: AMOXICILINA/ACIDO CLAVULANICO NORMON 125 mg/31,25 mg/5 ml (proporción 4:1; '
                          '= 25 mg de amoxicilina por 1 ml)')),
        pres('suspension-500-125-mg-5-ml-4-1-arsenal', 'suspension', mg_ml=100,
             fuente=fu(ARSENAL, 'Grupo 06.02.01: Amoxicilina + Ácido Clavulánico, Suspensión oral 500 + 125 mg/5 mL (proporción 4:1; '
                                '= 100 mg de amoxicilina y 25 mg de clavulánico por 1 ml). Lectura por columnas del PDF')),
    ]
    dosis_ = [
        dosis('Dosis estándar, proporción 7:1 (adultos y niños ≥40 kg), en mg de amoxicilina', 'adulto', 'fija', 'mg', min=875, max=875,
              tomas=2, intervalo_h=12,
              texto='875 mg/125 mg dos veces al día (1750 mg de amoxicilina/250 mg de clavulánico al día)',
              presentaciones=['comprimido-875-125-mg-7-1', 'sobre-875-125-mg-7-1'],
              fuente=fu(AMC_C, '4.2.1: "dosis estándar (para todas las indicaciones): 875 mg/125 mg administrada dos veces al día"; '
                               '"dosis diaria total de 1 750 mg de amoxicilina/250 mg de ácido clavulánico con la dosis de dos veces al día"')),
        dosis('Dosis superior: otitis media, sinusitis, infección respiratoria baja y urinaria (adultos y niños ≥40 kg), proporción 7:1',
              'adulto', 'fija', 'mg', min=875, max=875, tomas=3, intervalo_h=8,
              texto='875 mg/125 mg tres veces al día (2625 mg de amoxicilina/375 mg de clavulánico al día)',
              presentaciones=['comprimido-875-125-mg-7-1', 'sobre-875-125-mg-7-1'],
              fuente=fu(AMC_C, '4.2.1: "dosis superior ... 875 mg/125 mg administrada tres veces al día"; "2 625 mg de amoxicilina/375 mg de '
                               'ácido clavulánico con la dosis de tres veces al día"')),
        dosis('Dosis habitual (niños <40 kg), solo presentaciones 7:1, en mg de amoxicilina', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=25,
              max=45, tomas=2, intervalo_h=12, tope_dia=(2625, 'mg'),
              condicion='Solo con el comprimido 7:1 de 875/125 (el sobre 875/125 solo tiene posología para ≥40 kg, CIMA 59518); NO calcular con la suspensión 4:1 del arsenal (exceso de ácido clavulánico). Clavulánico 3,6-6,4 mg/kg/día. Comprimidos 875/125 solo con ≥25 kg (no se pueden partir); '
                        'por debajo, presentaciones pediátricas 7:1 que no están cargadas. Tope diario 2625 mg de amoxicilina, derivado: '
                        '375 mg/día de clavulánico (máximo de Pediamécum) en proporción 7:1',
              texto='25 mg/3,6 mg/kg/día a 45 mg/6,4 mg/kg/día divididos en dos dosis al día',
              presentaciones=['comprimido-875-125-mg-7-1'],
              fuente=fu(AMC_C, '4.2.1 Niños <40 kg: "25 mg/3,6 mg/kg/día a 45 mg/6,4 mg/kg/día dividida en dos dosis al día"; '
                               'tope: Pediamécum "Clavulánico: 15 mg/kg/día, sin superar 375 mg/día"')),
        dosis('Otitis media, sinusitis e infección respiratoria baja (niños <40 kg), solo presentaciones 7:1, en mg de amoxicilina', 'pediatrico',
              'por_peso', 'mg/kg', base='dia', max=70, tomas=2, intervalo_h=12, tope_dia=(2625, 'mg'),
              condicion='Solo con el comprimido 7:1 de 875/125 (el sobre 875/125 solo tiene posología para ≥40 kg, CIMA 59518); NO calcular con la suspensión 4:1 del arsenal (exceso de ácido clavulánico). Solo ≥2 años: no hay datos de la proporción 7:1 por encima de 45 mg/6,4 mg/kg/día en menores de 2 años. '
                        'Clavulánico 10 mg/kg/día. Pediamécum usa 80-90 mg/kg/día con presentaciones 8:1 (suspensión) o 7:1 (comprimidos, sobres) '
                        '(ver discrepancias). Tope diario 2625 mg de amoxicilina, derivado: 375 mg/día de clavulánico (Pediamécum) en proporción 7:1',
              texto='Hasta 70 mg/10 mg/kg/día divididos en dos dosis al día',
              presentaciones=['comprimido-875-125-mg-7-1'],
              fuente=fu(AMC_C, '4.2.1: "hasta 70 mg/10 mg/kg/día dividida en dos dosis al día para infecciones tales como otitis media, sinusitis e '
                               'infecciones del tracto respiratorio inferior"; "No hay datos clínicos ... 7:1 ... superiores a 45 mg/6,4 mg por kg al día en niños menores de 2 años"')),
        dosis('Infección respiratoria leve o moderada con baja resistencia de S. pneumoniae (niños >3 meses), solo suspensión 4:1, en mg de amoxicilina',
              'pediatrico', 'por_peso', 'mg/kg', base='dia', min=35, max=40, tomas=3, intervalo_h=8, tope_dia=(1500, 'mg'),
              condicion='Proporción 4:1 (clavulánico 9-10 mg/kg/día). Pediamécum (A) en infecciones respiratorias. Tope diario 1500 mg de amoxicilina, '
                        'derivado: 375 mg/día de clavulánico (máximo de Pediamécum) en proporción 4:1 (la misma cifra que la nota 7 de la tabla)',
              texto='35-40 mg/9-10 mg/kg/día en 3 dosis',
              presentaciones=['suspension-250-62-5-mg-5-ml-4-1', 'suspension-125-31-25-mg-5-ml-4-1', 'suspension-500-125-mg-5-ml-4-1-arsenal'],
              fuente=fu(P, 'Tabla de usos clínicos, fila "IR leves, moderadas / Con baja tasa de R del S. pneumoniae": "35-40 mg/9-10 mg (3)" '
                           '(columna 4:1); máximo de clavulánico: "15 mg/kg/día, sin superar 375 mg/día"')),
        dosis('Infecciones de orina por enterobacterias sensibles (niños >3 meses), solo suspensión 4:1, en mg de amoxicilina', 'pediatrico',
              'por_peso', 'mg/kg', base='dia', min=35, max=40, tomas=3, intervalo_h=8, tope_dia=(1500, 'mg'),
              condicion='Proporción 4:1 (clavulánico 9-10 mg/kg/día). Pediamécum (A) en infecciones genitourinarias',
              texto='35-40 mg/9-10 mg/kg/día en 3 dosis; dosis máxima diaria de amoxicilina 1500 mg (375 mg de clavulánico)',
              presentaciones=['suspension-250-62-5-mg-5-ml-4-1', 'suspension-125-31-25-mg-5-ml-4-1', 'suspension-500-125-mg-5-ml-4-1-arsenal'],
              fuente=fu(P, 'Tabla de usos clínicos: "Infecciones de orina por enterobacterias sensibles ... 35-40 mg/9-10 mg (3)"; nota 7: '
                           '"Dosis máxima diaria de amoxicilina 1500 mg (375 mg de ácido clavulánico)"')),
    ]
    disc = [
        discrepancia('Dosis pediátrica alta (otitis, sinusitis, infección respiratoria baja)',
                     [(AMC_C, '70 mg/kg/día de amoxicilina (10 mg/kg/día de clavulánico) en 2 dosis, proporción 7:1 (CIMA, Augmentine 875/125)'),
                      (P, '80-90 mg/kg/día de amoxicilina (9-15 mg/kg/día de clavulánico) en 2-3 dosis, con alta tasa de resistencia de S. pneumoniae (Pediamécum)')],
                     '70 mg/kg/día de amoxicilina',
                     'Mismo régimen (dosis alta en infección respiratoria y ORL) y población: se muestra la cifra más baja. En la tabla de Pediamécum '
                     'la pauta de 80-90 mg/kg/día está en la columna «8:1 (susp) / 7:1 (comp, sobres)»; para pasar de 70 mg/kg/día la ficha '
                     'aconseja elegir otra formulación.'),
        discrepancia('Tope diario de amoxicilina en niños',
                     [(AMC_C, '2800 mg/día: máximo que aporta la formulación 7:1 en niños <40 kg ("1 000 – 2 800 mg de amoxicilina/143 - 400 mg de ácido clavulánico")'),
                      (P, '3000 mg/día de amoxicilina, "sin superar dosis máxima de ácido clavulánico" (15 mg/kg/día, sin superar 375 mg/día) (Pediamécum)')],
                     '2625 mg/día de amoxicilina en las pautas 7:1 (equivale a 375 mg/día de clavulánico)',
                     'Cifra derivada: se aplica el máximo de clavulánico de Pediamécum (375 mg/día), más restrictivo que ambas cifras de amoxicilina; '
                     'en proporción 7:1 corresponde a 2625 mg de amoxicilina, la misma cifra que la ficha da para 875/125 tres veces al día.'),
    ]
    alertas = [
        'La proporción amoxicilina:clavulánico cambia entre presentaciones (4:1, 7:1 y 8:1): elegir la presentación exacta. Todas las dosis y '
        'presentaciones de esta ficha se expresan en mg de amoxicilina (Pediamécum: "La dosificación se realiza en base a la amoxicilina").',
        'Clavulánico: máximo 15 mg/kg/día sin superar 375 mg/día (Pediamécum). Las pautas 7:1 (25-45 y 70 mg/kg/día) NO se deben calcular con '
        'las suspensiones 4:1 (las del arsenal: 500 + 125 y 250 + 62,5 mg/5 ml): con 4:1, 70 mg/kg/día de amoxicilina aportarían 17,5 mg/kg/día '
        'de clavulánico, por encima del máximo. Con la suspensión 4:1 usar solo las pautas 4:1 (35-40 mg/kg/día en 3 dosis). Cada pauta queda '
        'vinculada a sus presentaciones: las 7:1 de adultos y niños ≥40 kg, al comprimido y al sobre 875/125; las 7:1 de niños <40 kg, solo al '
        'comprimido 875/125 (la ficha del sobre, CIMA 59518, solo da posología para ≥40 kg); las 4:1, a las suspensiones 4:1.',
        'Niños de menos de 25 kg: no hay ninguna presentación 7:1 cargada que les sirva. Los comprimidos 875/125 no se pueden partir y no se '
        'deben usar con menos de 25 kg (CIMA 59515: "los niños que pesen menos de 25 kg no deben ser tratados con Augmentine comprimidos"; '
        '"deben ser tratados preferiblemente con Augmentine suspensión o sobres pediátricos"), y esas presentaciones pediátricas 7:1 no están '
        'cargadas. Las pautas 7:1 (25-45 y 70 mg/kg/día) no se pueden calcular con ninguna presentación de esta ficha en ese peso: no '
        'sustituirlas por la suspensión 4:1 ni por la 8:1.',
        'Dos suspensiones tienen 100 mg/ml de amoxicilina pero distinto clavulánico: 8:1 (12,5 mg/ml) y la 4:1 del arsenal (500 + 125 mg/5 ml, '
        '25 mg/ml). Confirmar el frasco.',
        'Los comprimidos 875/125 no se deben partir: no usar en niños de menos de 25 kg (CIMA 59515). Entre 25 y 40 kg, un comprimido aporta '
        '35,0 mg/kg (25 kg), 29,2 (30 kg), 25,0 (35 kg) o 21,9 mg/kg (40 kg) de amoxicilina por dosis, frente a la dosis única recomendada '
        'de 12,5-22,5 mg/kg (hasta 35) (tabla de CIMA 59515, 4.2.1).',
        'Las presentaciones 7:1 no se recomiendan con aclaramiento de creatinina <30 ml/min ni en menores de 2 meses (sin datos) (CIMA 59515).',
        'Contraindicado con antecedente de ictericia o insuficiencia hepática por amoxicilina/clavulánico; evitar en sospecha de mononucleosis (CIMA, 4.3 y 4.4).',
        'Esta presentación 7:1 no debe usarse para S. pneumoniae resistente a penicilina (CIMA 59515, 4.4).',
    ]
    return ficha_oral(
        'amoxicilina-clavulanico', 'Amoxicilina + ácido clavulánico', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Con las comidas, para reducir la posible intolerancia gastrointestinal. No partir los comprimidos (la ficha lo indica por la dosis); el sobre se '
                     'disuelve en medio vaso de agua (CIMA 59518).',
            'fuente': fu(AMC_C, '4.2.2 Forma de administración; partición: 4.2.1'),
        },
        comerciales=['Augmentine'], discrepancias=disc,
        renal='Aclaramiento de creatinina >30 ml/min: sin ajuste. <30 ml/min: no se recomiendan las presentaciones 7:1 (no hay recomendaciones de ajuste).',
        hepatico='Dosificar con precaución y controlar la función hepática a intervalos regulares.',
        fuente_ajuste=fu(AMC_C, '4.2.1 Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def flucloxacilina():
    presentaciones = [
        pres('capsula-500-mg', 'capsula', mg=500, partible='no',
             fuente=fu(FLX, 'Flucloxacillin 500 mg capsules, hard: "Each capsule contains flucloxacillin sodium equivalent to 500 mg of flucloxacillin"')),
        pres('suspension-50-mg-ml', 'suspension', mg_ml=50,
             fuente=fu(ARSENAL, 'Grupo 06.02.01: Flucloxacilina, Polvo para suspensión oral 250 mg/5 mL (= 50 mg por 1 ml)')),
    ]
    dosis_ = [
        dosis('Infecciones por grampositivos sensibles (adultos, incluidos ancianos)', 'adulto', 'fija', 'mg', min=250, max=250, tomas=4,
              intervalo_h=6, condicion='250 mg no se puede dar con la cápsula de 500 mg: usar la suspensión (250 mg/5 ml, arsenal)',
              texto='250 mg cuatro veces al día; en infecciones graves la dosis puede duplicarse',
              fuente=fu(FLX, '4.2 Adults (including elderly patients), Oral: "250 mg four times a day. In serious infections, the dosage may be doubled"')),
        dosis('Infecciones graves (adultos)', 'adulto', 'fija', 'mg', min=500, max=500, tomas=4, intervalo_h=6,
              texto='Dosis duplicada: 500 mg cuatro veces al día (1 cápsula)',
              fuente=fu(FLX, '4.2: "In serious infections, the dosage may be doubled" (2 × 250 mg cuatro veces al día)')),
        dosis('Infecciones por grampositivos sensibles (niños de 2 a 10 años)', 'pediatrico', 'fija', 'mg', min=125, max=125, tomas=4,
              intervalo_h=6, condicion='Usar la suspensión: la cápsula de 500 mg no permite 125 mg', texto='125 mg cuatro veces al día',
              fuente=fu(FLX, '4.2 Paediatric population: "2-10 years: 125 mg four times daily"')),
        dosis('Infecciones por grampositivos sensibles (niños menores de 2 años)', 'pediatrico', 'fija', 'mg', min=62.5, max=62.5, tomas=4,
              intervalo_h=6, condicion='Usar la suspensión: la cápsula de 500 mg no permite 62,5 mg. En prematuros, neonatos y lactantes pueden '
                                       'ser más adecuadas otras formas', texto='62,5 mg cuatro veces al día',
              fuente=fu(FLX, '4.2 Paediatric population: "Under 2 years: 62.5mg four times daily"')),
    ]
    alertas = [
        'Fuente única: solo la ficha técnica del Reino Unido (EMC); no hay ficha CIMA ni Pediamécum para contrastar.',
        'La cápsula de 500 mg solo sirve para dosis de 500 mg: 62,5, 125 y 250 mg requieren la suspensión de 250 mg/5 ml del arsenal chileno '
        '(la ficha EMC es de la cápsula).',
        'Osteomielitis y endocarditis: hasta 8 g diarios repartidos cada 6-8 horas (EMC); no se carga como pauta aparte.',
        'Hepatitis e ictericia colestásica descritas, incluso hasta 2 meses después del tratamiento; precaución en disfunción hepática y en '
        'mayores de 50 años. Contraindicado con antecedente de ictericia por flucloxacilina (EMC, 4.3 y 4.4).',
        'Precaución con paracetamol: riesgo de acidosis metabólica con anión gap elevado (EMC, 4.4). Hipopotasemia con dosis altas.',
    ]
    return ficha_oral(
        'flucloxacilina', 'Flucloxacilina', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'ayunas',
            'texto': 'En ayunas: al menos 1 hora antes o 2 horas después de las comidas, con un vaso lleno de agua (250 ml) para reducir el riesgo '
                     'de dolor esofágico; no acostarse inmediatamente después de tomarla.',
            'fuente': fu(FLX, '4.2 Method of administration'),
        },
        comerciales=['Flucloxacillin Brown & Burk (Reino Unido)'],
        renal='En general no requiere reducción. Insuficiencia renal grave (aclaramiento de creatinina <10 ml/min): considerar reducir la dosis '
              'o alargar el intervalo; la dosis máxima recomendada en adultos es 1 g cada 8 a 12 horas. No se elimina significativamente por diálisis.',
        hepatico='No es necesario reducir la dosis (precaución por el riesgo de reacciones hepáticas).',
        fuente_ajuste=fu(FLX, '4.2 Abnormal renal function / Hepatic impairment'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- cefalosporina
def cefadroxilo():
    P = _ped('cefadroxilo')
    presentaciones = [
        pres('capsula-500-mg', 'capsula', mg=500, partible='no',
             fuente=fu(CFD_C, 'Duracef 500 mg: "Las cápsulas deben tomarse enteras, sin masticar" (4.2)')),
        pres('suspension-50-mg-ml', 'suspension', mg_ml=50,
             fuente=fu(CFD_S, 'Duracef 250 mg/5 ml: "1 MS (= 5 ml) ... contiene 250 mg cefadroxilo" (= 50 mg por 1 ml)')),
    ]
    dosis_ = [
        dosis('Infecciones urinarias no complicadas e infecciones de piel y tejidos blandos (adultos y adolescentes ≥40 kg)', 'adulto', 'fija',
              'mg', min=1000, max=1000, tomas=2, intervalo_h=12,
              condicion='Pauta de la ficha: 2000 mg/día en total. Pediamécum admite hasta 4 g/día en adultos (ver discrepancias); no se carga como tope',
              texto='1000 mg dos veces al día',
              fuente=fu(CFD_C, '4.2 Adultos y adolescentes ≥40 kg: "Infecciones del tracto urinario no complicadas: 1000 mg dos veces al día"; '
                               '"Infecciones no complicadas de la piel y tejidos blandos: 1000 mg dos veces al día"')),
        dosis('Faringoamigdalitis (adultos y adolescentes ≥40 kg)', 'adulto', 'fija', 'mg', min=1000, max=1000, tomas=1, intervalo_h=24,
              texto='1000 mg una vez al día durante 10 días',
              fuente=fu(CFD_C, '4.2: "Faringoamigdalitis: 1000 mg una vez al día durante 10 días"')),
        dosis('Faringoamigdalitis, infecciones urinarias y de piel (niños <40 kg)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=30,
              tomas=2, intervalo_h=12, tope_dia=(2000, 'mg'),
              condicion='CIMA (Duracef suspensión) da la misma pauta. Usar la suspensión: la cápsula de 500 mg no sirve para <40 kg ni <6 años; '
                        'la suspensión no se recomienda con <6 kg. S. pyogenes: mínimo 10 días',
              texto='30 mg/kg/día divididos en 2 dosis; dosis máxima 2 g al día',
              presentaciones=['suspension-50-mg-ml'],
              fuente=fu(P, 'Niños: "30 mg/kg/día dividido en 2 dosis, vía oral. Dosis máxima de 2 g al día"; CIMA 55731 4.2: "30 mg/kg/día dividido en '
                           'dos dosis ... Dosis máxima 2 gramos al día"')),
    ]
    disc = [
        discrepancia('Dosis diaria máxima del adulto',
                     [(CFD_C, '2000 mg/día: 1000 mg dos veces al día (CIMA, Duracef)'),
                      (P, '4000 mg/día: "Dosis máxima en adultos 4 g al día"; dosis habitual 1-2 g al día en 1 o 2 dosis (Pediamécum)')],
                     '2000 mg/día (la pauta de la ficha, 1000 mg cada 12 h)',
                     'Misma población adulta: se muestra la cifra más baja (informe §2). No se carga un topeDiario de adulto: 2000 es el total '
                     'de la pauta, no un máximo declarado, y el de 4 g/día de Pediamécum es más alto.'),
        discrepancia('Dosis pediátrica diaria',
                     [(CFD_S, '50 mg/kg/día: tabla "Recomendaciones generales de dosificación basadas en 50 mg/kg/día" (CIMA, Duracef suspensión)'),
                      (CFD_S, '30 mg/kg/día en dos dosis, máximo 2 g/día: tabla por indicación de la misma ficha; Pediamécum coincide')],
                     '30 mg/kg/día',
                     'La ficha de la suspensión trae dos tablas orientativas; se muestra la cifra más baja, que es la de la tabla por indicación y la de Pediamécum.'),
    ]
    alertas = [
        'Con la cápsula de 500 mg no se consigue una dosis adecuada en niños ≥6 años de menos de 40 kg, y no está recomendada en menores de '
        '6 años: usar la suspensión de 250 mg/5 ml (CIMA 55730).',
        'La suspensión no está recomendada en lactantes y niños de menos de 6 kg (CIMA 55731).',
        'Contraindicado en niños ≥6 años de menos de 40 kg con insuficiencia renal o en hemodiálisis (CIMA 55730, 4.3).',
        'Duración: 2-3 días tras desaparecer los síntomas; en infecciones por Streptococcus pyogenes, hasta 10 días (CIMA).',
        'CIMA 55731 trae además una tabla de amigdalitis con 30 mg/kg/día en una sola toma; no se carga como pauta aparte.',
    ]
    return ficha_oral(
        'cefadroxilo', 'Cefadroxilo', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Con alimentos o con el estómago vacío (con alteraciones gástricas, mejor con alimentos). Cápsulas enteras, sin masticar, con líquido.',
            'noTriturar': True,
            'fuente': fu(CFD_C, '4.2 Forma de administración'),
        },
        comerciales=['Duracef'], discrepancias=disc,
        renal='Adultos, según aclaramiento de creatinina: 50-25 ml/min, dosis inicial 1000 mg y continuación 500-1000 mg cada 12 h; 25-10 ml/min, '
              'cada 24 h; 10-0 ml/min, cada 36 h. Hemodiálisis: dosis adicional de 500-1000 mg al final de la sesión.',
        hepatico='No es necesario ajustar la dosis.',
        fuente_ajuste=fu(CFD_C, '4.2 Insuficiencia renal (tabla), pacientes en hemodiálisis, insuficiencia hepática'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- macrólidos
def claritromicina():
    P = _ped('claritromicina')
    presentaciones = [
        pres('comprimido-250-mg', 'comprimido', mg=250, partible='no',
             fuente=fu(CLA_C, 'Claritromicina Cinfa 250 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: CLARITROMICINA CINFA 500 mg COMPRIMIDOS RECUBIERTOS CON PELICULA EFG')),
        pres('suspension-25-mg-ml', 'suspension', mg_ml=25, fuente=fu(CLA_S, 'Claritromicina Sandoz 25 mg/ml granulado para suspensión oral')),
        pres('suspension-50-mg-ml', 'suspension', mg_ml=50,
             fuente=fu(ARSENAL, 'Grupo 06.02.04: Claritromicina, Polvo para suspensión oral 250 mg/5 mL (= 50 mg por 1 ml)')),
    ]
    dosis_ = [
        dosis('Dosis estándar (adultos y adolescentes ≥12 años)', 'adulto', 'fija', 'mg', min=250, max=250, tomas=2, intervalo_h=12,
              texto='250 mg dos veces al día; duración habitual 5-14 días (neumonía y sinusitis, 6-14 días)',
              fuente=fu(CLA_C, '4.2.1: "La dosis recomendada ... en adultos y niños de 12 años o mayores es de 250 mg 2 veces al día"')),
        dosis('Infecciones graves (adultos y adolescentes ≥12 años)', 'adulto', 'fija', 'mg', min=500, max=500, tomas=2, intervalo_h=12,
              texto='500 mg dos veces al día',
              fuente=fu(CLA_C, '4.2.1: "En infecciones más graves, la dosis puede incrementarse a 500 mg 2 veces al día"')),
        dosis('Infecciones respiratorias, otitis media y de piel (niños de 6 meses a 12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='toma',
              max=7.5, tomas=2, intervalo_h=12, tope_toma=(500, 'mg'),
              condicion='Los menores de 12 años deben tomar la suspensión. Tope de 500 mg cada 12 h: Pediamécum ("hasta un máximo de 500 mg/12 horas"). '
                        'Duración habitual 5-10 días',
              texto='7,5 mg/kg dos veces al día',
              presentaciones=['suspension-25-mg-ml', 'suspension-50-mg-ml'],
              fuente=fu(CLA_S, '4.2 Niños de 6 meses a 12 años: "La dosis recomendada es de 7,5 mg/kg dos veces al día"; tope: Pediamécum')),
        dosis('Faringitis estreptocócica (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=7.5, tomas=2, intervalo_h=12,
              tope_toma=(250, 'mg'), condicion='Durante 10 días', texto='7,5 mg/kg cada 12 horas, con dosis máxima de 250 mg cada 12 horas, 10 días',
              presentaciones=['suspension-25-mg-ml', 'suspension-50-mg-ml'],
              fuente=fu(P, '"7,5 mg/kg/12 horas ..."; "En el caso de faringitis estreptocócica será de 10 días con una dosis máxima de 250 mg/12 horas"')),
    ]
    alertas = [
        'La claritromicina en comprimidos no ha sido estudiada en menores de 12 años (CIMA 67638): en niños usar la suspensión. Experiencia limitada en menores de 6 meses (CIMA 66388).',
        'Contraindicada con astemizol, cisaprida, domperidona, pimozida, terfenadina, ticagrelor, ivabradina, ranolazina, ergotamínicos, '
        'midazolam oral, lovastatina o simvastatina y lomitapida, y con QT largo o hipopotasemia/hipomagnesemia; no debe usarse en pacientes '
        'que estén tomando colchicina (CIMA, 4.3).',
        'La ficha de la suspensión trae una tabla orientativa en ml por peso (25 mg/ml); no se carga: la dosis se calcula por kg.',
        'Erradicación de H. pylori (adultos): 500 mg dos veces al día en terapia combinada (CIMA). Profilaxis de endocarditis: 15 mg/kg en dosis '
        'única (Pediamécum, off-label). No se cargan.',
        'Dos concentraciones de suspensión (25 y 50 mg/ml): confirmar la del frasco.',
    ]
    return ficha_oral(
        'claritromicina', 'Claritromicina', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Independientemente de los alimentos (solo retrasan ligeramente la absorción). La suspensión puede dejar sabor amargo: tomar algo '
                     'de comida o bebida justo después.',
            'fuente': fu(CLA_S, '4.2 Forma de administración'),
        },
        comerciales=['Claritromicina Cinfa', 'Claritromicina Sandoz'],
        renal='Aclaramiento de creatinina <30 ml/min: reducir la dosis a la mitad (250 mg una vez al día, o 250 mg dos veces al día en infecciones '
              'más graves); no más de 14 días. Niños (CIMA 66388): 7,5 mg/kg una vez al día.',
        hepatico='Precaución en insuficiencia hepática (metabolismo hepático). No administrar con insuficiencia hepática grave combinada con insuficiencia renal.',
        fuente_ajuste=fu(CLA_C, '4.2.1 Pacientes con insuficiencia renal; 4.3 y 4.4 (insuficiencia hepática); pauta pediátrica renal: CIMA 66388, 4.2'),
        alertas=alertas,
    )


def azitromicina():
    P = _ped('azitromicina')
    presentaciones = [
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='no',
             fuente=fu(AZI_C, 'Azitromicina Cinfa 500 mg: "Los comprimidos deben tragarse enteros" (4.2.2)')),
        pres('sobre-500-mg', 'sobre', mg=500, partible='no',
             fuente=fu(AZI_S, 'Azitromicina Cinfa 500 mg polvo para suspensión oral (sobre): contenido completo en unos 60 ml de agua (4.2.2)')),
        pres('suspension-40-mg-ml', 'suspension', mg_ml=40,
             fuente=fu(P, 'Presentaciones de Pediamécum: ZITROMAX 200 mg/5 ml POLVO PARA SUSPENSION ORAL EN FRASCO (= 40 mg por 1 ml)')),
    ]
    dosis_ = [
        dosis('Amigdalitis, sinusitis, otitis media, neumonía, bronquitis crónica agudizada y piel (adultos y adolescentes ≥45 kg)', 'adulto',
              'fija', 'mg', min=500, max=500, tomas=1, intervalo_h=24, tope_dia=(500, 'mg'), texto='500 mg/día durante 3 días, en una toma diaria',
              fuente=fu(AZI_C, '4.2.1 Tabla 1: "500 mg/día durante 3 días"; dosis diaria del adulto 500 mg (CIMA 65601, 4.2.1)')),
        dosis('Sinusitis, neumonía, piel y otitis media (niños ≥6 meses de <45 kg)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=10,
              tomas=1, intervalo_h=24, tope_dia=(500, 'mg'),
              condicion='Durante 3 días (alternativa: 10 mg/kg el día 1 y 5 mg/kg/día los días 2-5). Sin exceder la dosis diaria del adulto (500 mg) '
                        'ni 1500 mg en total por tratamiento',
              texto='10 mg/kg/día en una toma diaria durante 3 días',
              presentaciones=['suspension-40-mg-ml', 'sobre-500-mg'],
              fuente=fu(AZI_S, '4.2.1 Tabla 1: "10 mg/kg/día durante 3 días"; "La dosis diaria de azitromicina no debe exceder la dosis diaria en adultos de 500 mg"')),
        dosis('Amigdalitis y faringitis estreptocócica (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=20, tomas=1,
              intervalo_h=24, tope_dia=(500, 'mg'),
              condicion='Durante 3 días. CIMA coincide (20 mg/kg/día durante 3 días, sin exceder 500 mg/día)',
              texto='20 mg/kg/día durante 3 días consecutivos; dosis máxima diaria 500 mg',
              presentaciones=['suspension-40-mg-ml', 'sobre-500-mg'],
              fuente=fu(P, '"Para el tratamiento de la faringoamigdalitis, la dosis recomendada es de 20 mg/kg/día durante 3 días consecutivos (dosis máxima diaria: 500 mg)"')),
        dosis('Pauta por peso (niños, salvo faringoamigdalitis)', 'pediatrico', 'por_edad', 'mg', tomas=1, intervalo_h=24,
              texto='<15 kg: 10 mg/kg/día. 15-25 kg: 200 mg/día. 26-35 kg: 300 mg/día. 36-45 kg: 400 mg/día. Más de 45 kg: dosis de adulto. '
                    'Una toma diaria durante 3 días (alternativa en 5 días: la dosis del día 1 y luego la mitad los días 2-5)',
              condicion='Tabla por peso: se muestra, no se calcula',
              fuente=fu(P, '"La pauta posológica en función del peso es la siguiente: <15 kg: 10 mg/kg/día ... 15-25 kg: 200 mg/día ... 26-35 kg: '
                           '300 mg/día ... 36-45 kg: 400 mg/día ... 45 kg: la misma dosis que para adultos"')),
    ]
    alertas = [
        'Otitis media aguda: alternativa de dosis única de 30 mg/kg (máximo total 1500 mg); faringoamigdalitis: alternativa de 12 mg/kg/día '
        'durante 5 días (CIMA 65601). No se cargan como pautas aparte.',
        'Los sobres no sirven para niños de menos de 16 kg; en ellos usar la suspensión en frasco (CIMA 65601).',
        'No establecida en menores de 6 meses (CIMA 65601).',
        'Uretritis/cervicitis por Chlamydia y chancroide: 1000 mg en dosis única (adultos, CIMA). No se carga.',
        'Riesgo de prolongación del QT y torsade de pointes: precaución con QT largo, alteraciones electrolíticas, bradicardia y otros '
        'fármacos que prolongan el QT (CIMA, 4.4).',
    ]
    return ficha_oral(
        'azitromicina', 'Azitromicina', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Una toma diaria. Comprimidos enteros, con o sin comida; tomarlos justo antes de las comidas puede mejorar la tolerancia digestiva.',
            'noTriturar': True,
            'fuente': fu(AZI_C, '4.2.2 Forma de administración'),
        },
        comerciales=['Azitromicina Cinfa', 'Zitromax'],
        renal='Sin ajuste con filtrado glomerular ≥10 ml/min; precaución con <10 ml/min.',
        hepatico='Sin ajuste en insuficiencia hepática leve o moderada (Child-Pugh A o B); grave (C): sin datos, administrar con precaución.',
        fuente_ajuste=fu(AZI_C, '4.2.1 Poblaciones especiales: insuficiencia renal / hepática'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- sulfonamida (cifras en mg de TRIMETOPRIMA)
def cotrimoxazol():
    P = _ped('cotrimoxazol')
    presentaciones = [
        pres('comprimido-forte-160-800-mg', 'comprimido', mg=160, partible='no',
             fuente=fu(SXT, 'Septrin Forte: 160 mg de trimetoprima/800 mg de sulfametoxazol; cantidad en mg de TRIMETOPRIMA. '
                            'El arsenal de APS lista el mismo comprimido (800 mg + 160 mg)')),
        pres('comprimido-80-400-mg', 'comprimido', mg=80, partible='no',
             fuente=fu(SXT, '4.2 menciona "Septrin 80 mg/400 mg comprimidos"; cantidad en mg de trimetoprima')),
        pres('comprimido-pediatrico-20-100-mg', 'comprimido', mg=20, partible='no',
             fuente=fu(SXT, '4.2 menciona "Septrin Pediátrico 20 mg/100 mg comprimidos"; cantidad en mg de trimetoprima')),
        pres('suspension-8-40-mg-ml', 'suspension', mg_ml=8,
             fuente=fu(SXT, '4.2 menciona "Septrin Pediátrico 8 mg/40 mg/ml suspensión oral"; concentración en mg de trimetoprima por 1 ml '
                            '(40 mg de sulfametoxazol). El arsenal lista 200 mg + 40 mg/5 mL, la misma concentración')),
    ]
    dosis_ = [
        dosis('Dosis estándar (adultos y niños >12 años), en mg de trimetoprima', 'adulto', 'fija', 'mg', min=160, max=160, tomas=2,
              intervalo_h=12, condicion='Cifras en mg de trimetoprima (TMP); el sulfametoxazol (SMX) es 5 veces más',
              texto='160 mg de trimetoprima/800 mg de sulfametoxazol cada 12 horas (1 comprimido Forte, 2 comprimidos de 80/400 o 20 ml de suspensión)',
              presentaciones=['comprimido-forte-160-800-mg', 'comprimido-80-400-mg', 'suspension-8-40-mg-ml'],
              fuente=fu(SXT, '4.2 Dosis estándar: "160 mg de trimetoprima/800 mg de sulfametoxazol/12 horas"')),
        dosis('Dosis estándar por edad (lactantes y niños de 6 semanas a 12 años), en mg de trimetoprima', 'pediatrico', 'por_edad', 'mg',
              tomas=2, intervalo_h=12,
              texto='6 semanas a 5 meses: 20 mg TMP/100 mg SMX cada 12 h. 6 meses a 5 años: 40 mg TMP/200 mg SMX cada 12 h. '
                    '6 a 12 años: 80 mg TMP/400 mg SMX cada 12 h',
              condicion='Tabla por edad: se muestra, no se calcula. Contraindicado en menores de 6 semanas',
              presentaciones=['suspension-8-40-mg-ml', 'comprimido-pediatrico-20-100-mg'],
              fuente=fu(SXT, '4.2: "6 semanas a 5 meses: 20 mg de trimetoprima/ 100 mg de sulfametoxazol/ 12 horas ... 6 meses a 5 años: 40 mg ... '
                             '6 a 12 años: 80 mg de trimetroprima/ 400 mg sulfametoxazol/ 12 horas"')),
        dosis('Dosis estándar por peso (lactantes y niños de 6 semanas a 12 años), en mg de trimetoprima', 'pediatrico', 'por_peso', 'mg/kg',
              base='dia', max=6, tomas=2, intervalo_h=12,
              condicion='Cifra en mg de TRIMETOPRIMA por kg y día (≈30 mg de sulfametoxazol/kg/día). La ficha la da como aproximación de la tabla '
                        'por edad. Contraindicado en menores de 6 semanas',
              texto='Aproximadamente 6 mg de trimetoprima/30 mg de sulfametoxazol por kg cada 24 h, en 2 tomas (cada 12 h)',
              presentaciones=['suspension-8-40-mg-ml', 'comprimido-pediatrico-20-100-mg'],
              fuente=fu(SXT, '4.2 Lactantes y niños menores de 12 años: "las dosis se aproximan a 6 mg de trimetoprima/ 30 mg de sulfametoxazol/kg/24 horas"')),
        dosis('Profilaxis de infección urinaria (niños), en mg de trimetoprima', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=2,
              tomas=1, intervalo_h=24,
              condicion='Pediamécum escribe SMX/TMP: "10/2 mg/kg/24 h" = 10 mg de sulfametoxazol y 2 mg de TRIMETOPRIMA por kg. '
                        'Pediamécum (A) para profilaxis de infección urinaria en niños >6 semanas; la ficha CIMA cargada no describe esta pauta',
              texto='2 mg de trimetoprima (10 mg de sulfametoxazol) por kg cada 24 horas',
              fuente=fu(P, 'Niños <12 años: "Profilaxis de la infección del tracto urinario: 10/2 mg/kg/24 h por vía oral"')),
    ]
    disc = [
        discrepancia('Dosis pediátrica diaria en infecciones ORL, respiratorias y urinarias (mg de trimetoprima)',
                     [(SXT, '6 mg de trimetoprima/kg/día (30 mg de sulfametoxazol/kg/día) en 2 tomas (CIMA, Septrin)'),
                      (P, '8-12 mg de trimetoprima/kg/día: "20-30/4-6 mg/kg/12 h" en notación SMX/TMP, es decir 4-6 mg de trimetoprima/kg cada 12 h (Pediamécum)')],
                     '6 mg de trimetoprima/kg/día',
                     'Mismo régimen y población: se muestra la cifra más baja (Pediamécum da entre 1,3 y 2 veces más). La propia ficha da 5/25 mg/kg '
                     'cada 12 h durante 3 días como alternativa en infección urinaria no complicada y diarrea infecciosa.'),
    ]
    alertas = [
        'Todas las cifras de esta ficha (dosis y presentaciones) están en mg de TRIMETOPRIMA; el sulfametoxazol es 5 veces más (1:5).',
        'Notación invertida entre fuentes: Pediamécum escribe primero el sulfametoxazol (p. ej. 800/160 mg) y la ficha técnica primero la '
        'trimetoprima (160/800 mg). Confirmar a qué componente se refiere cada cifra.',
        'La pauta por peso no trae tope pediátrico en la fuente; como referencia, la dosis de adulto es 160 mg de trimetoprima cada 12 h (CIMA). '
        'En profilaxis de Pneumocystis y de toxoplasmosis la ficha limita a 320 mg de trimetoprima/1600 mg de sulfametoxazol al día.',
        'Contraindicado en prematuros y niños a término menores de 6 semanas, porfiria aguda y con dofetilida (CIMA, 4.3).',
        'CIMA 4.4: "Existen algunos datos procedentes de estudios que pueden sugerir que Septrin no debería administrarse a niños menores de 3 meses".',
        'Reacciones cutáneas graves (Stevens-Johnson, NET), discrasias sanguíneas y necrosis hepática descritas; hemograma mensual en tratamientos '
        'prolongados (CIMA, 4.4).',
        'Neumonía por Pneumocystis, toxoplasmosis, nocardiosis, brucelosis y melioidosis tienen pautas propias (CIMA, 4.2); no se cargan.',
        'No se usa la ficha de Balsoprim: lleva bromhexina, no es cotrimoxazol solo.',
    ]
    return ficha_oral(
        'cotrimoxazol', 'Cotrimoxazol (trimetoprima + sulfametoxazol)', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Tomar con algún alimento o bebida para minimizar las molestias digestivas; agitar bien la suspensión (CIMA). '
                     'Pediamécum, en cambio, aconseja la forma oral 1 h antes o 2 h después de las comidas para reducir las molestias gástricas.',
            'fuente': fu(SXT, '4.2 Forma de administración'),
        },
        comerciales=['Septrin', 'Septrin Forte', 'Septrin Pediátrico'], discrepancias=disc,
        renal='Adultos y niños >12 años (sin información en <12 años): aclaramiento de creatinina >30 ml/min, dosis estándar; 15-30 ml/min, '
              'la mitad de la dosis estándar; <15 ml/min, no se recomienda.',
        hepatico='Lesión grave del parénquima hepático: tener cuidado, puede alterarse la absorción y el metabolismo de trimetoprima y sulfametoxazol.',
        fuente_ajuste=fu(SXT, '4.2 Pacientes con insuficiencia renal; 4.4 (lesión hepática)'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- quinolona
def ciprofloxacino():
    P = _ped('ciprofloxacino')
    presentaciones = [
        pres('suspension-100-mg-ml', 'suspension', mg_ml=100, fuente=fu(CIP_S, 'Cetraxal 100 mg/ml suspensión oral (500 mg/5 ml)')),
        pres('comprimido-250-mg', 'comprimido', mg=250, partible='no',
             fuente=fu(CIP_C, 'Ciprofloxacino Cinfa 250 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='no', fuente=fu(ARSENAL, 'Grupo 06.02.06: Ciprofloxacino, Comprimido 500 mg')),
    ]
    dosis_ = [
        dosis('Infecciones respiratorias bajas, ORL, urinarias complicadas, piel, intraabdominales y osteoarticulares (adultos)', 'adulto',
              'fija', 'mg', min=500, max=750, tomas=2, intervalo_h=12,
              texto='500-750 mg dos veces al día; duración según indicación (7-14 días en la mayoría)',
              fuente=fu(CIP_S, '4.2.1 Adultos (tabla): "500 mg a 750 mg, dos veces al día"')),
        dosis('Cistitis aguda no complicada (adultos)', 'adulto', 'fija', 'mg', min=250, max=500, tomas=2, intervalo_h=12,
              condicion='Solo cuando no se considere apropiado el uso de otros antibacterianos de primera línea',
              texto='250-500 mg dos veces al día durante 3 días; en mujeres premenopáusicas puede usarse una dosis única de 500 mg',
              fuente=fu(CIP_S, '4.2.1: Cistitis aguda no complicada "250 mg a 500 mg, dos veces al día ... 3 días"; "En mujeres pre-menopáusicas, se puede utilizar una dosis única de 500 mg"')),
        dosis('Infecciones urinarias complicadas y pielonefritis aguda (niños y adolescentes)', 'pediatrico', 'por_peso', 'mg/kg', base='toma',
              min=10, max=20, tomas=2, intervalo_h=12, tope_toma=(750, 'mg'), tope_dia=(1500, 'mg'),
              condicion='Tratamiento de 2.ª-3.ª línea en niños >1 año (Pediamécum). Tope diario 1500 mg: Pediamécum ("20-40 mg/kg/día, cada 12 h ... '
                        'dosis máxima: 1500 mg/día"). Lo inicia un médico con experiencia en infecciones graves en niños. Duración 10-21 días',
              texto='10-20 mg/kg dos veces al día, con un máximo de 750 mg por dosis',
              fuente=fu(CIP_S, '4.2.1 Niños y adolescentes: "Infecciones complicadas de las vías urinarias y pielonefritis aguda: 10 mg/kg ... a 20 mg/kg ... '
                               'dos veces al día, con un máximo de 750 mg por dosis"')),
        dosis('Exacerbación pulmonar por P. aeruginosa en fibrosis quística (niños >5 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              max=40, tomas=2, intervalo_h=12, tope_toma=(750, 'mg'), tope_dia=(1500, 'mg'),
              condicion='Pediamécum (A) en niños >5 años. CIMA da la misma pauta: 20 mg/kg dos veces al día, máximo 750 mg por dosis, 10-14 días',
              texto='40 mg/kg/día divididos cada 12 horas; dosis máxima 1500 mg/día',
              fuente=fu(P, 'Fibrosis quística, "Vía oral: 40 mg/kg/día, divididos cada 12 horas; dosis máxima de 1500 mg/día"; CIMA 62602: '
                           '"20 mg/kg de peso corporal, dos veces al día, con un máximo de 750 mg por dosis"')),
    ]
    alertas = [
        'Fluoroquinolona: riesgo de tendinitis y rotura de tendón, neuropatía, aneurisma y disección aórtica y regurgitación valvular; evitar '
        'si hubo reacciones graves previas a quinolonas (CIMA, 4.4).',
        'No tomar con lácteos (leche, yogur) ni zumos enriquecidos en calcio (CIMA, 4.2.2).',
        'En niños solo indicaciones restringidas (ITU complicada, fibrosis quística, carbunco) y por médicos con experiencia; el resto de usos '
        'pediátricos es off-label (Pediamécum: otras infecciones 20-30 mg/kg/día en 2 dosis, máximo 1,5 g/día; no se cargan).',
        'Contraindicado con tizanidina (CIMA, 4.3).',
    ]
    return ficha_oral(
        'ciprofloxacino', 'Ciprofloxacino', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Independientemente de las comidas (en ayunas se absorbe más rápido). No tomar con productos lácteos ni con zumos enriquecidos en calcio.',
            'fuente': fu(CIP_S, '4.2.2 Forma de administración'),
        },
        comerciales=['Cetraxal', 'Ciprofloxacino Cinfa'],
        renal='Aclaramiento de creatinina 30-60 ml/min/1,73 m²: 250-500 mg cada 12 h. <30: 250-500 mg cada 24 h. Hemodiálisis: 250-500 mg cada 24 h '
              '(después de la diálisis). Diálisis peritoneal: 250-500 mg cada 24 h. No estudiado en niños con insuficiencia renal.',
        hepatico='No precisa ajuste de dosis (no estudiado en niños).',
        fuente_ajuste=fu(CIP_S, '4.2.1 Insuficiencia renal y hepática (tabla)'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- nitrofurano
def nitrofurantoina():
    P = _ped('nitrofurantoina')
    presentaciones = [
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(NIT_C, 'Furantoína 50 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('suspension-10-mg-ml', 'suspension', mg_ml=10, fuente=fu(NIT_S, 'Furantoína 10 mg/ml suspensión oral')),
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(ARSENAL, 'Grupo 06.02.12: Nitrofurantoína, "Cápsula o Comprimido" 100 mg (se carga como comprimido; el arsenal no precisa la forma)')),
    ]
    dosis_ = [
        dosis('Cistitis aguda no complicada (mujeres adultas)', 'adulto', 'fija', 'mg', min=50, max=100, tomas=3, intervalo_h=8,
              texto='50-100 mg (1-2 comprimidos de 50 mg) cada 8 horas durante 5-7 días',
              fuente=fu(NIT_C, '4.2.1 Adultos: "50-100 mg (1-2 comprimidos) cada 8 horas durante 5-7 días"')),
        dosis('Cistitis aguda, comprimidos (niñas mayores de 6 años y adolescentes)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=5,
              max=7, tomas=4, intervalo_h=6, tope_dia=(300, 'mg'),
              condicion='"Sin superar la dosis de adulto" (50-100 mg cada 8 h): tope de 300 mg/día (= 100 mg × 3 tomas del adulto, '
                        'CIMA 22974 4.2.1); con 4 tomas limita la toma a 75 mg, por debajo de los 100 mg por toma del adulto. Para niñas menores de 6 años, usar la suspensión',
              texto='5-7 mg/kg/día repartidos en cuatro tomas durante 5-7 días',
              fuente=fu(NIT_C, '4.2.1 Población pediátrica: "5-7 mg/kg de peso por día, sin superar la dosis de adulto, repartidas en cuatro tomas durante 5-7 días"')),
        dosis('Cistitis aguda, suspensión (niños de 3 meses a 6 años, o que no toleran comprimidos)', 'pediatrico', 'por_peso', 'mg/kg',
              base='toma', min=1, max=2, tomas=4, intervalo_h=6, tope_dia=(300, 'mg'),
              condicion='No usar en menores de 3 meses. CIMA 34388 da la misma pauta en volumen: 0,1-0,2 ml/kg de la suspensión de 10 mg/ml cada 6 h. '
                        '"Sin superar la dosis de adulto": tope de 300 mg/día (= 100 mg × 3 tomas del adulto, CIMA 22974 4.2.1); con 4 tomas limita la toma a 75 mg',
              texto='1-2 mg/kg cada 6 horas durante 5-7 días',
              presentaciones=['suspension-10-mg-ml'],
              fuente=fu(P, '"Menores o igual de 6 años o que no toleren comprimidos (no usar en menores de 3 meses): ... 1-2 mg/kg de peso cada 6 horas, '
                           'sin superar la dosis de adulto, durante 5-7 días"')),
    ]
    alertas = [
        'Contraindicada con aclaramiento de creatinina <45 ml/min (entre 30 y 44 ml/min solo ante microorganismos multirresistentes, valorando '
        'beneficio/riesgo), en menores de 3 meses, tratamientos >7 días, déficit de G6PD, porfiria aguda y en las dos últimas semanas de embarazo (CIMA, 4.3).',
        'No indicada en infecciones urinarias en varones, infecciones urinarias altas ni bacteriemia (CIMA, 4.4).',
        'Tratamientos prolongados: reacciones pulmonares y hepáticas graves y neuropatía periférica; no usar como profilaxis de infecciones urinarias recurrentes (CIMA, 4.4).',
        'Con 4 tomas y el tope de 300 mg/día (dosis de adulto: 100 mg × 3, CIMA 22974), la toma queda limitada a 75 mg: no se puede dar con el '
        'comprimido de 50 mg no partible (haría falta 1 comprimido y medio) ni con el de 100 mg; la suspensión de 10 mg/ml sí lo permite (7,5 ml).',
        'La orina puede teñirse de amarillo o marrón (CIMA).',
    ]
    return ficha_oral(
        'nitrofurantoina', 'Nitrofurantoína', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Durante las comidas o con un vaso de leche (la comida aumenta la absorción y reduce las molestias digestivas).',
            'fuente': fu(NIT_C, '4.2.2 Forma de administración; 4.4 y 4.5'),
        },
        comerciales=['Furantoína'],
        renal='Contraindicada con aclaramiento de creatinina <45 ml/min; entre 30 y 44 ml/min puede considerarse solo ante sospecha o antecedente '
              'de microorganismos multirresistentes, valorando el balance beneficio/riesgo.',
        hepatico='Usar con precaución en alteración de la función hepática; suspender si aparece hepatitis.',
        fuente_ajuste=fu(NIT_C, '4.2.1 Insuficiencia renal; 4.4 Hepatotoxicidad y precauciones'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- nitroimidazol
def metronidazol():
    P = _ped('metronidazol')
    presentaciones = [
        pres('comprimido-250-mg', 'comprimido', mg=250, partible='no',
             fuente=fu(MTZ_C, 'Metronidazol Normon 250 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('suspension-25-mg-ml', 'suspension', mg_ml=25,
             fuente=fu(MTZ_S, 'Flagyl suspensión: "Cada 5 ml contienen 125 mg de metronidazol" (= 25 mg de metronidazol base por 1 ml)')),
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='no', fuente=fu(ARSENAL, 'Grupo 06.06: Metronidazol, Comprimido 500 mg')),
    ]
    dosis_ = [
        dosis('Infecciones por anaerobios (adultos y adolescentes >12 años)', 'adulto', 'fija', 'mg', min=250, max=500, tomas=3,
              intervalo_h=8, condicion='La duración media no debe superar 7 días',
              texto='1 o 2 comprimidos de 250 mg tres veces al día (Flagyl: 500 mg cada 8 horas)',
              fuente=fu(MTZ_C, '4.2 Infección bacteriana anaerobia: "Adultos y adolescentes mayores de 12 años: 1 o 2 comprimidos de 250 mg tres veces al día"; '
                               'Flagyl (47656): "Adultos: 500 mg cada 8 horas"')),
        dosis('Infecciones por anaerobios (niños de 8 semanas a 12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=7.5, tomas=3,
              intervalo_h=8,
              condicion='Dosis diaria habitual 20-30 mg/kg (en una toma o en 7,5 mg/kg cada 8 h); puede aumentarse a 40 mg/kg/día según la gravedad. '
                        'Duración habitual 7 días',
              texto='7,5 mg/kg cada 8 horas',
              fuente=fu(MTZ_C, '4.2: "Niños mayores de 8 semanas a 12 años de edad: la dosis diaria habitual es de 20 a 30 mg/kg como dosis única o en dosis '
                               'divididas de 7,5 mg/kg cada 8 horas. La dosis diaria se puede aumentar a 40 mg/kg"')),
        dosis('Amebiasis (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=35, max=50, tomas=3, intervalo_h=8,
              tope_dia=(2400, 'mg'), condicion='Durante 5-10 días', texto='35-50 mg/kg al día en 3 dosis, sin exceder 2400 mg/día',
              fuente=fu(MTZ_S, '4.2 Amebiasis: "de 35 a 50 mg/kg al día divididos en 3 dosis durante 5 - 10 días, no excediendo la dosis de 2.400 mg/día"')),
        dosis('Giardiasis (lambliasis) (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=15, tomas=3, intervalo_h=8,
              tope_dia=(500, 'mg'), condicion='Durante 5-7 días. La ficha CIMA admite 15-40 mg/kg/día en 2-3 dosis, sin tope (ver discrepancias)',
              texto='15 mg/kg/día repartidos cada 8 horas; dosis máxima diaria 500 mg',
              fuente=fu(P, 'Lambliasis: "15 mg/kg/día repartidos cada 8 h, por 5-7 días. Dosis máxima diaria (vía oral o i.v.): 500 mg"')),
    ]
    disc = [
        discrepancia('Infecciones por anaerobios en niños: frecuencia y tope',
                     [(MTZ_C, '22,5 mg/kg/día: 7,5 mg/kg cada 8 h (dosis diaria 20-30 mg/kg, hasta 40 según gravedad), sin tope en mg (CIMA)'),
                      (P, '30 mg/kg/día divididos cada 6 h, máximo 4 g/día (Pediamécum, lactantes y niños)')],
                     '22,5 mg/kg/día (7,5 mg/kg cada 8 horas)',
                     'Mismo régimen y población: se muestra la pauta de la ficha (cada 8 h), la más baja. 4 g/día (Pediamécum) es el único tope '
                     'del régimen; con 7,5 mg/kg cada 8 h solo se alcanzaría con unos 178 kg, así que nunca se alcanza antes que la dosis de adulto. '
                     'El tope de 2400 mg/día de CIMA es de la amebiasis.'),
        discrepancia('Giardiasis en niños',
                     [(MTZ_C, '40 mg/kg/día como extremo superior de "15 a 40 mg/kg por día divididos en 2-3 dosis", sin tope en mg (CIMA)'),
                      (P, '15 mg/kg/día cada 8 h, máximo 500 mg/día (Pediamécum)')],
                     '15 mg/kg/día',
                     'Mismo régimen y población: se muestra la cifra más baja, con el tope de Pediamécum.'),
        discrepancia('Amebiasis en niños',
                     [(MTZ_S, '35-50 mg/kg/día en 3 dosis, sin exceder 2400 mg/día (CIMA)'),
                      (P, '40-50 mg/kg/día cada 6-8 h durante 10 días, sin tope (Pediamécum)')],
                     '35-50 mg/kg/día, máximo 2400 mg/día',
                     'Se muestra la pauta de la ficha (rango inferior más bajo y con tope).'),
    ]
    alertas = [
        'La pauta de anaerobios en niños (7,5 mg/kg cada 8 h) no trae tope en la ficha; como referencia, la dosis de adulto es de 250-500 mg '
        'cada 8 h (CIMA 62223; Flagyl: 500 mg cada 8 h).',
        'Giardiasis, pautas de la ficha en dosis única diaria durante 3 días: 1-3 años 500 mg, 3-7 años 600-800 mg (Flagyl) o 750 mg (Normon), '
        '7-10 años 1000 mg, >10 años 2000 mg. Salvo la de 1-3 años (500 mg, igual al máximo), superan el máximo de 500 mg/día de la pauta '
        'de Pediamécum; no se cargan.',
        'Tricomoniasis (adultos y niños >10 años: 2000 mg dosis única o 250 mg tres veces al día 7 días; <10 años: 40 mg/kg dosis única, máx. 2000 mg), '
        'vaginosis bacteriana, amebiasis del adulto (750 mg tres veces al día) y H. pylori tienen pautas propias (CIMA); no se cargan.',
        'Evitar alcohol durante el tratamiento (efecto antabús). Contraindicado en el primer trimestre del embarazo (CIMA 62223, 4.3).',
        'No superar 10 días de tratamiento salvo casos concretos con control clínico y analítico; vigilar neuropatía (CIMA 62223, 4.4).',
        'Hepatotoxicidad grave en el síndrome de Cockayne: no usar salvo que no haya alternativa (CIMA, 4.4).',
        'Flagyl suspensión contiene benzoato de metronidazol: 200 mg de benzoato equivalen a 125 mg de metronidazol base por 5 ml; las dosis se expresan en base (Pediamécum).',
    ]
    return ficha_oral(
        'metronidazol', 'Metronidazol', 'antibiotico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral; la ficha técnica no indica relación con las comidas. Pediamécum: preferiblemente con alimentos para evitar síntomas '
                     'gastrointestinales. En menores de 6 años o con dificultad para tragar pueden ser más adecuadas otras presentaciones (CIMA 62223).',
            'fuente': fu(MTZ_C, '4.2.2 Forma de administración'),
        },
        comerciales=['Metronidazol Normon', 'Flagyl'], discrepancias=disc,
        renal='Datos limitados; no indican necesidad de reducir la dosis. Hemodiálisis: programar la dosis después de la sesión en los días de diálisis. '
              'Diálisis peritoneal: sin ajuste.',
        hepatico='Insuficiencia hepática grave: reducir la dosis diaria total a una tercera parte y darla en una dosis única diaria.',
        fuente_ajuste=fu(MTZ_C, '4.2 Uso en pacientes con insuficiencia hepática / renal'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- antiparasitario
def mebendazol():
    P = _ped('mebendazol')
    presentaciones = [
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no', fuente=fu(MEB_C, 'Lomper 100 mg comprimidos')),
        pres('suspension-20-mg-ml', 'suspension', mg_ml=20, fuente=fu(MEB_S, 'Lomper 20 mg/ml suspensión oral (5 ml = 100 mg)')),
    ]
    dosis_ = [
        dosis('Enterobiasis (oxiuriasis) (adultos)', 'adulto', 'fija', 'mg', min=100, max=100, tomas=1,
              texto='Dosis única de 100 mg (1 comprimido o 5 ml); repetir a las 2 y 4 semanas',
              fuente=fu(MEB_C, '4.2.1: "Enterobiasis (oxiuriasis): Una única dosis de 1 comprimido o 5 ml ... Se recomienda repetir el tratamiento después de 2 y 4 semanas"')),
        dosis('Tricuriasis, ascariasis, anquilostomiasis, necatoriasis y parasitosis mixtas (adultos)', 'adulto', 'fija', 'mg', min=100,
              max=100, tomas=2, intervalo_h=12, texto='100 mg (1 comprimido o 5 ml) dos veces al día durante 3 días consecutivos',
              fuente=fu(MEB_C, '4.2.1: "un comprimido o 5 ml ... dos veces al día (por la mañana y por la tarde) durante tres días consecutivos"')),
        dosis('Enterobiasis (oxiuriasis) (niños ≥2 años)', 'pediatrico', 'fija', 'mg', min=100, max=100, tomas=1,
              condicion='CIMA: misma dosis desde los 2 años, repitiendo a las 2 y 4 semanas. Tratar también a los convivientes',
              texto='100 mg en dosis única; repetible a las 2-3 semanas',
              fuente=fu(P, '"Enterobiasis: 100 mg dosis única; repetible en 2-3 semanas ya que la reinfección es frecuente"')),
        dosis('Tricuriasis, ascariasis, anquilostomiasis e infecciones mixtas (niños ≥2 años)', 'pediatrico', 'fija', 'mg', min=100, max=100,
              tomas=2, intervalo_h=12, condicion='Si los parásitos persisten a las 3 semanas puede repetirse un ciclo (Pediamécum)',
              texto='100 mg dos veces al día durante 3 días',
              fuente=fu(MEB_C, '4.2.1 "Adultos, adolescentes y niños ≥ 2 años de edad": "un comprimido o 5 ml ... dos veces al día ... durante tres días consecutivos"')),
    ]
    disc = [
        discrepancia('Población: menores de 2 años',
                     [(MEB_C, 'CIMA: no establecida en menores de 2 años y no se puede hacer una recomendación posológica; no usar en menores de 1 año'),
                      (P, 'Pediamécum: en menores de 2 años solo cuando la parasitosis interfiera significativamente con el estado nutricional y el desarrollo')],
                     'No se carga dosis para menores de dos años',
                     'Ninguna fuente da una posología para menores de 2 años.'),
    ]
    alertas = [
        'No usar en menores de 1 año; entre 1 y 2 años solo si el beneficio justifica el riesgo (convulsiones descritas) (CIMA, 4.2 y 4.4).',
        'Evitar el uso junto con metronidazol (casos de Stevens-Johnson/NET) (CIMA, 4.4).',
        'En niños que no pueden tragar comprimidos, usar la suspensión para reducir el riesgo de asfixia (CIMA, 4.4).',
        'Insuficiencia hepática: no hay datos; monitorizar estrechamente (Pediamécum). Con cimetidina, ajustar la dosis (CIMA).',
    ]
    return ficha_oral(
        'mebendazol', 'Mebendazol', 'antiparasitario', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Comprimidos y suspensión con o sin comida; agitar la suspensión antes de usar (CIMA). Pediamécum: preferentemente entre las comidas.',
            'fuente': fu(MEB_C, '4.2.2 Forma de administración'),
        },
        comerciales=['Lomper'], discrepancias=disc, alertas=alertas,
    )


# ---------------------------------------------------------------- antifúngicos
def fluconazol():
    P = _ped('fluconazol')
    presentaciones = [
        pres('capsula-100-mg', 'capsula', mg=100, partible='no',
             fuente=fu(FLU_C, 'Diflucan 100 mg: "Las cápsulas deben tragarse enteras" (4.2.2)')),
        pres('capsula-150-mg', 'capsula', mg=150, partible='no',
             fuente=fu(ARSENAL, 'Grupo 06.04: Fluconazol, Cápsula 150 mg (Pediamécum también lista DIFLUCAN 150 mg CAPSULAS DURAS)')),
        pres('suspension-10-mg-ml', 'suspension', mg_ml=10, fuente=fu(FLU_S, 'Diflucan 10 mg/ml polvo para suspensión oral')),
        pres('suspension-40-mg-ml', 'suspension', mg_ml=40,
             fuente=fu(P, 'Presentaciones de Pediamécum: DIFLUCAN 40 mg/ml POLVO PARA SUSPENSION ORAL')),
    ]
    dosis_ = [
        dosis('Candidiasis orofaríngea (adultos)', 'adulto', 'fija', 'mg', min=100, max=200, tomas=1, intervalo_h=24,
              condicion='El primer día, dosis de carga de 200-400 mg. Duración 7-21 días',
              texto='Dosis de carga de 200-400 mg el 1.er día; después 100-200 mg una vez al día',
              fuente=fu(FLU_C, '4.2.1 Candidiasis orofaríngea: "Dosis de carga: de 200 mg a 400 mg el 1er día. Dosis posteriores:100 mg a 200 mg una vez al día"')),
        dosis('Candidiasis vaginal aguda y balanitis por Candida (adultos)', 'adulto', 'fija', 'mg', min=150, max=150, tomas=1,
              texto='150 mg en dosis única',
              fuente=fu(FLU_C, '4.2.1 Candidiasis genital: "Candidiasis vaginal aguda - Balanitis por Candida: 150 mg, Dosis única"')),
        dosis('Candidiasis de las mucosas, orofaríngea o esofágica (lactantes y niños de 28 días a 11 años)', 'pediatrico', 'por_peso', 'mg/kg',
              base='dia', max=3, tomas=1, intervalo_h=24, tope_dia=(400, 'mg'),
              condicion='Dosis inicial de 6 mg/kg el primer día. No exceder 400 mg al día en niños (CIMA). En lactantes y niños pequeños, formas líquidas',
              texto='Dosis inicial 6 mg/kg; siguientes dosis 3 mg/kg una vez al día',
              fuente=fu(FLU_C, '4.2.1 Lactantes y niños: "Candidiasis de las mucosas: Dosis inicial: 6 mg/kg. Siguientes dosis: 3 mg/kg una vez al día"; '
                               '"En la población pediátrica, no debe excederse una dosis máxima de 400 mg al día"')),
        dosis('Candidiasis sistémica o invasiva y meningitis criptocócica (lactantes y niños de 28 días a 11 años)', 'pediatrico', 'por_peso',
              'mg/kg', base='dia', min=6, max=12, tomas=1, intervalo_h=24, tope_dia=(400, 'mg'),
              condicion='Según la gravedad. CIMA da la misma pauta (6 a 12 mg/kg una vez al día) y limita a 400 mg al día en niños. Duración mínima 28 días',
              texto='6-12 mg/kg/día en una dosis diaria',
              fuente=fu(P, 'Lactantes y niños (28 días a 11 años): "Candidiasis sistémica: 6-12 mg/kg/día. Duración mínima: 28 días"; tope: CIMA 58804 4.2.1')),
    ]
    disc = [
        discrepancia('Tope diario pediátrico',
                     [(FLU_C, '400 mg/día: "En la población pediátrica, no debe excederse una dosis máxima de 400 mg al día" (CIMA)'),
                      (P, '800 mg/día: no sobrepasar la dosis máxima diaria de adultos (Pediamécum, que añade que la ficha técnica no recomienda superar 400-600 mg/día)')],
                     '400 mg/día',
                     'Misma población pediátrica: se muestra el tope más bajo.'),
    ]
    alertas = [
        'Neonatos a término: la misma dosis por kg cada 72 h (0-14 días) o cada 48 h (15-27 días), sin superar 12 mg/kg cada 72 h o cada 48 h '
        'respectivamente (CIMA). No se cargan dosis neonatales.',
        'Adolescentes de 12 a 17 años: según peso y desarrollo puberal, dosis de adulto o de niño; 100, 200 y 400 mg en adultos equivalen a 3, 6 y '
        '12 mg/kg en niños (CIMA).',
        'Dos concentraciones de suspensión (10 y 40 mg/ml): confirmar la del frasco.',
        'Contraindicado con fármacos que prolongan el QT y se metabolizan por CYP3A4 (p. ej. cisaprida) y con terfenadina si se dan ≥400 mg/día (CIMA, 4.3).',
        'No usar para Tinea capitis (CIMA, 4.4).',
        'Candidiasis invasiva y meningitis criptocócica del adulto (carga 400-800 mg, luego 200-400 mg/día) tienen pautas propias; no se cargan.',
    ]
    return ficha_oral(
        'fluconazol', 'Fluconazol', 'antiviral-antifungico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Cápsulas enteras, con independencia de la ingesta de alimentos. Las cápsulas no están adaptadas para bebés ni niños pequeños: usar formulaciones líquidas.',
            'noTriturar': True,
            'fuente': fu(FLU_C, '4.2.2 Forma de administración'),
        },
        comerciales=['Diflucan'], discrepancias=disc,
        renal='Dosis única: sin ajuste. Dosis múltiples (también en niños): dosis inicial de 50-400 mg y después, según aclaramiento de creatinina: '
              '>50 ml/min, 100 % de la dosis; ≤50 ml/min sin hemodiálisis, 50 %; hemodiálisis, 100 % después de cada sesión.',
        hepatico='Datos limitados: administrar con precaución en alteración de la función hepática.',
        fuente_ajuste=fu(FLU_C, '4.2.1 Pacientes con insuficiencia renal / hepática'),
        alertas=alertas,
    )


def _pres_ui(id, forma, ui_ml, fuente):
    """Suspensión dosificada en UI por 1 ml (pres() solo admite mg)."""
    p = pres(id, forma, mg_ml=ui_ml, fuente=fuente)
    p['concentracion'] = {'valor': ui_ml, 'unidad': 'UI'}
    return p


def nistatina():
    P = _ped('nistatina')
    presentaciones = [
        _pres_ui('suspension-100000-ui-ml', 'suspension', 100000,
                 fu(NIS, 'Mycostatin 100.000 UI/ml suspensión oral (el arsenal de APS lista la misma concentración)')),
    ]
    dosis_ = [
        dosis('Candidiasis oral (adultos)', 'adulto', 'fija', 'UI', min=250000, max=500000, tomas=2, intervalo_h=12,
              condicion='Intervalo cargado: 12 h, el extremo conservador de "cada 6-12 horas"',
              texto='250.000-500.000 UI (2,5-5 ml) cada 6-12 horas',
              fuente=fu(NIS, '4.2 Adultos: "Candidiasis oral: 250.000 - 500.000 UI (2,5 - 5 ml) cada 6-12 horas"')),
        dosis('Candidiasis intestinal (adultos)', 'adulto', 'fija', 'UI', min=500000, max=1000000, tomas=4, intervalo_h=6,
              texto='500.000-1.000.000 UI (5-10 ml) cada 6 horas',
              fuente=fu(NIS, '4.2 Adultos: "Candidiasis intestinal: 500.000 - 1.000.000 UI (5 - 10 ml) cada 6 horas"')),
        dosis('Candidiasis oral (lactantes mayores de 1 año, niños y adolescentes)', 'pediatrico', 'fija', 'UI', min=250000, max=500000,
              tomas=2, intervalo_h=12, condicion='Intervalo cargado: 12 h, el extremo conservador de "cada 6-12 horas"',
              texto='250.000-500.000 UI (2,5-5 ml) cada 6-12 horas',
              fuente=fu(NIS, '4.2 Población pediátrica: "Lactantes mayores de un año, niños y adolescentes: 250.000 - 500.000 UI (2,5 - 5 ml) cada 6-12 horas"')),
        dosis('Candidiasis oral (lactantes de 1 año o menos)', 'pediatrico', 'fija', 'UI', min=250000, max=250000, tomas=4, intervalo_h=6,
              condicion='CIMA coincide ("Lactantes menores o iguales a un año: 250.000 UI (2,5 ml) cada 6 horas"). No incluye recién nacidos',
              texto='250.000 UI (2,5 ml) cada 6 horas',
              fuente=fu(P, 'Candidiasis oral, niños: "Menores de 1 año: 250 000 cada 6 horas"')),
        dosis('Candidiasis intestinal (niños y adolescentes)', 'pediatrico', 'fija', 'UI', min=250000, max=750000, tomas=4, intervalo_h=6,
              texto='250.000-750.000 UI (2,5-7,5 ml) cada 6 horas',
              fuente=fu(NIS, '4.2 Candidiasis intestinal: "Niños y adolescentes: 250.000 - 750.000 UI (2,5 - 7,5 ml) cada 6 horas"')),
        dosis('Candidiasis intestinal (lactantes)', 'pediatrico', 'fija', 'UI', min=100000, max=300000, tomas=4, intervalo_h=6,
              texto='100.000-300.000 UI (1-3 ml) cada 6 horas',
              fuente=fu(NIS, '4.2 Candidiasis intestinal: "Lactantes: 100.000 - 300.000 UI (1 - 3 ml) cada 6 horas"')),
    ]
    disc = [
        discrepancia('Recién nacidos',
                     [(NIS, 'CIMA: recién nacidos y lactantes con bajo peso al nacer, 100.000 UI (1 ml) cada 6 horas'),
                      (P, 'Pediamécum: neonatos a término 200.000 UI (2 ml) cada 6 horas; pretérmino 100.000 UI (1 ml) cada 6 horas')],
                     'No se cargan dosis neonatales (fuera del alcance de esta versión)',
                     'Diferencia solo en el recién nacido a término; en lactantes, niños y adultos las fuentes coinciden.'),
    ]
    alertas = [
        'Dosis en unidades internacionales (UI): no se convierten a mg. 1 ml de suspensión = 100.000 UI.',
        'Candidiasis oral: mantener la suspensión en la boca el mayor tiempo posible (varios minutos) antes de tragarla; en lactantes y niños '
        'pequeños, poner la mitad de la dosis en cada lado de la boca (CIMA).',
        'Continuar al menos 48 horas después de que desaparezcan los síntomas; si empeora o persiste a los 14 días, reevaluar (CIMA).',
        'Pediamécum: no requiere ajuste en insuficiencia renal ni hepática (absorción sistémica despreciable).',
    ]
    return ficha_oral(
        'nistatina', 'Nistatina', 'antiviral-antifungico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Agitar bien. Puede tomarse sola, con agua o mezclada con un líquido o alimento blando no ácido (leche, miel, jalea). '
                     'En candidiasis oral, mantenerla en la boca varios minutos antes de tragar.',
            'fuente': fu(NIS, '4.2 Forma de administración'),
        },
        comerciales=['Mycostatin'], discrepancias=disc, alertas=alertas,
    )


def terbinafina():
    P = _ped('terbinafina')
    presentaciones = [
        pres('comprimido-250-mg', 'comprimido', mg=250, partible='no',
             fuente=fu(TER, 'Lamisil 250 mg comprimidos (la ficha no menciona ranura ni partición; Pediamécum: tomar los comprimidos enteros)')),
    ]
    dosis_ = [
        dosis('Tiñas de piel y cuero cabelludo y onicomicosis (adultos)', 'adulto', 'fija', 'mg', min=250, max=250, tomas=1, intervalo_h=24,
              texto='250 mg (1 comprimido) una vez al día. Duración: tinea pedis 2-6 semanas, corporis 4, cruris 2-4, capitis 4; '
                    'onicomicosis 6 semanas (manos) a 12 semanas (pies)',
              fuente=fu(TER, '4.2: "Adultos: 250 mg (1 comprimido) una vez al día"; duración del tratamiento por indicación')),
        dosis('Tinea capitis (niños mayores de 4 años)', 'pediatrico', 'por_edad', 'mg', tomas=1, intervalo_h=24, estatus='off_label',
              texto='<25 kg: 125 mg cada 24 h. 25-35 kg: 187,5 mg cada 24 h. >35 kg: 250 mg cada 24 h (como adultos). Durante un máximo de 6 semanas',
              condicion='Tabla por peso: se muestra, no se calcula. Ficha técnica: uso en niños no recomendado; Pediamécum (E: off-label). '
                        '125 y 187,5 mg exigen medio y tres cuartos de comprimido de 250 mg, que la ficha no dice que se pueda partir; '
                        'en España no hay forma líquida',
              fuente=fu(P, '"Tinea capitis. En niños >4 años: <25 kg: 125 mg/24 h. 25-35 kg: 187,5 mg/24 h. >35 kg: 250 mg/24 h (igual que adultos). '
                           'Durante un máximo de 6 semanas"')),
        dosis('Onicomicosis (niños)', 'pediatrico', 'por_edad', 'mg', tomas=1, intervalo_h=24, estatus='off_label',
              texto='<20 kg: 62,5 mg cada 24 h. 20-40 kg: 125 mg cada 24 h. >40 kg: 250 mg cada 24 h (como adultos). '
                    '6 semanas (uñas de las manos) o 12 semanas (pies)',
              condicion='Tabla por peso: se muestra, no se calcula. Ficha técnica: uso en niños no recomendado; Pediamécum (E: off-label). '
                        '62,5 y 125 mg exigen un cuarto y medio comprimido de 250 mg, que la ficha no dice que se pueda partir',
              fuente=fu(P, '"Onicomicosis: <20 kg: 62,5 mg/24 h. 20-40 kg 125 mg/24 h. >40 kg: 250 mg/24 h (igual que adultos). '
                           'Durante 6 semanas (en manos) o 12 semanas (pies)"')),
    ]
    disc = [
        discrepancia('Población pediátrica',
                     [(TER, 'CIMA: "La experiencia con Lamisil comprimidos en niños es limitada y por consiguiente su utilización no puede ser recomendada"'),
                      (P, 'Pediamécum: pautas por peso en tinea capitis (niños >4 años) y onicomicosis, uso off-label')],
                     POBLACION_OFF_LABEL,
                     'Contradicción de población, no de cifra: la ficha técnica no respalda el uso en niños.'),
    ]
    alertas = [
        'Dosis pediátricas de 62,5, 125 y 187,5 mg: con el comprimido de 250 mg harían falta un cuarto, medio y tres cuartos de comprimido; '
        'ninguna ficha cargada dice que el comprimido se pueda partir y en España no hay forma líquida ni granulada (Pediamécum).',
        'Hepatotoxicidad: pruebas de función hepática antes de empezar y controles periódicos (tras 4-6 semanas); suspender ante náuseas persistentes, '
        'anorexia, fatiga, vómitos, dolor en hipocondrio derecho, ictericia, orina oscura o heces claras (CIMA, 4.4).',
        'No es eficaz en pitiriasis versicolor ni en candidiasis cutánea (CIMA, 4.1).',
    ]
    return ficha_oral(
        'terbinafina', 'Terbinafina', 'antiviral-antifungico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Comprimidos enteros, sin masticar, con un poco de agua, con o sin alimentos.',
            'noTriturar': True,
            'fuente': fu(P, 'Dosis y pautas de administración, oral (la ficha CIMA no describe la forma de administración)'),
        },
        comerciales=['Lamisil'], discrepancias=disc,
        renal='No se recomienda en insuficiencia renal (no estudiada suficientemente); contraindicada en insuficiencia renal grave.',
        hepatico='Contraindicada en insuficiencia hepática crónica o activa.',
        fuente_ajuste=fu(TER, '4.2 Uso en pacientes con insuficiencia hepática / renal; 4.3'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- antiviral
def aciclovir():
    P = _ped('aciclovir')
    presentaciones = [
        pres('comprimido-200-mg', 'comprimido', mg=200, partible='no',
             fuente=fu(ACI_C, 'Aciclovir Cinfa 200 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('suspension-80-mg-ml', 'suspension', mg_ml=80,
             fuente=fu(ACI_S, 'Zovirax 400 mg/5 ml suspensión oral (= 80 mg por 1 ml; tabla de conversión: 400 mg = 5 ml)')),
        pres('comprimido-400-mg', 'comprimido', mg=400, partible='no', fuente=fu(ARSENAL, 'Grupo 06.05.01: Aciclovir, Comprimido 400 mg')),
        pres('comprimido-800-mg', 'comprimido', mg=800, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ACICLOVIR CINFA 800 MG COMPRIMIDOS EFG')),
    ]
    dosis_ = [
        dosis('Herpes simple de piel y mucosas (adultos)', 'adulto', 'fija', 'mg', min=200, max=200, tomas=5,
              condicion='En inmunodeprimidos graves o con absorción intestinal disminuida puede duplicarse a 400 mg 5 veces al día',
              texto='200 mg 5 veces al día, a intervalos de unas 4 horas omitiendo la dosis nocturna, durante 5 días',
              fuente=fu(ACI_C, '4.2: "1 comprimido de 200 mg 5 veces al día a intervalos de aproximadamente 4 horas, omitiendo la dosis nocturna ... durante 5 días"')),
        dosis('Varicela y herpes zóster (adultos)', 'adulto', 'fija', 'mg', min=800, max=800, tomas=5,
              texto='800 mg 5 veces al día, a intervalos de 4 horas omitiendo la dosis nocturna, durante 7 días',
              fuente=fu(ACI_C, '4.2 Tratamiento de la varicela y el herpes zóster: "800 mg de aciclovir ... 5 veces al día a intervalos de 4 horas, omitiendo la dosis nocturna ... 7 días"')),
        dosis('Supresión de herpes simple recurrente (adultos inmunocompetentes)', 'adulto', 'fija', 'mg', min=200, max=200, tomas=4,
              intervalo_h=6, condicion='Interrumpir cada 6-12 meses para reevaluar',
              texto='200 mg 4 veces al día (cada 6 h); alternativa 400 mg 2 veces al día (cada 12 h)',
              fuente=fu(ACI_C, '4.2: "1 comprimido de 200 mg administrado 4 veces al día a intervalos de aproximadamente 6 horas"; "400 mg ... 2 veces al día cada 12 horas"')),
        dosis('Herpes simple de piel y mucosas (niños de 2 años o más)', 'pediatrico', 'fija', 'mg', min=200, max=200, tomas=5,
              texto='200 mg 5 veces al día durante 5 días (dosis de adulto)',
              fuente=fu(ACI_C, '4.2 Población pediátrica: "en niños y adolescentes (de 2 a 18 años), se administrarán las mismas dosis de tratamiento que en los adultos"')),
        dosis('Herpes simple de piel y mucosas (lactantes de 28 días a 23 meses)', 'pediatrico', 'fija', 'mg', min=100, max=100, tomas=5,
              texto='100 mg 5 veces al día durante 5 días (mitad de la dosis de adulto)',
              fuente=fu(ACI_S, '4.2.1 Tabla 1: "Lactantes y niños menores de 2 años: 100 mg 5 veces al día durante 5 días"')),
        dosis('Varicela (niños de 6 años o más, inmunocompetentes)', 'pediatrico', 'fija', 'mg', min=800, max=800, tomas=4, intervalo_h=6,
              texto='800 mg 4 veces al día durante 5 días',
              fuente=fu(ACI_S, '4.2.1 Tabla 1: "6 años y mayores: 800 mg 4 veces al día durante 5 días"')),
        dosis('Varicela (niños de 2 a menos de 6 años, inmunocompetentes)', 'pediatrico', 'fija', 'mg', min=400, max=400, tomas=4,
              intervalo_h=6, texto='400 mg 4 veces al día durante 5 días',
              fuente=fu(ACI_S, '4.2.1 Tabla 1: "2 a < 6 años: 400 mg 4 veces al día durante 5 días"')),
        dosis('Varicela (niños menores de 2 años, inmunocompetentes)', 'pediatrico', 'fija', 'mg', min=200, max=200, tomas=4, intervalo_h=6,
              texto='200 mg 4 veces al día durante 5 días',
              fuente=fu(ACI_S, '4.2.1 Tabla 1: "Menores de 2 años: 200 mg 4 veces al día durante 5 días"')),
        dosis('Varicela en el niño inmunocompetente, por peso (≥2 años; Pediamécum)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=80,
              tomas=4, intervalo_h=6, tope_toma=(800, 'mg'), estatus='off_label',
              condicion='Pauta de Pediamécum, distinta de la de ficha técnica (dosis fijas por edad). Pediamécum: no hay indicación en niños sanos; '
                        'considerarla con riesgo de enfermedad moderada o grave; iniciar en las primeras 24 h del exantema. Durante 5 días',
              texto='80 mg/kg/día cada 6 horas durante 5 días; dosis máxima 800 mg por dosis',
              fuente=fu(P, 'Varicela en el huésped inmunocompetente, oral: "≥2 años: 80 mg/kg/día cada 6 h, durante 5 días. Dosis máxima: 800 mg/dosis"')),
        dosis('Gingivoestomatitis herpética (niños; Pediamécum)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=60, tomas=4,
              intervalo_h=6, tope_toma=(200, 'mg'), estatus='off_label',
              condicion='Uso off-label (Pediamécum). Iniciar en las primeras 72 h; eficacia controvertida. Durante 7 días',
              texto='60 mg/kg/día cada 6 horas (máximo 200 mg por dosis) durante 7 días',
              fuente=fu(P, 'Gingivoestomatitis herpética: "60 mg/kg/día (máximo: 200 mg/dosis) cada 6 h por vía oral (VO) durante 7 días"')),
    ]
    disc = [
        discrepancia('Método de dosificación en niños',
                     [(ACI_S, 'CIMA: dosis fijas por edad (herpes simple 100 o 200 mg cinco veces al día; varicela 200, 400 u 800 mg cuatro veces al día)'),
                      (P, 'Pediamécum: dosis por peso (varicela 80 mg/kg/día cada 6 h, máx. 800 mg/dosis; gingivoestomatitis 60 mg/kg/día, máx. 200 mg/dosis); '
                          '"Las dosis recomendadas aceptadas por la comunidad científica no siempre coinciden con las dosis aprobadas en ficha técnica"')],
                     'Se muestran las pautas de ficha técnica como autorizadas y las de Pediamécum, por peso, como off-label',
                     'Diferencia de método (dosis fija por edad frente a mg/kg), no un conflicto numérico de un mismo régimen.'),
    ]
    alertas = [
        'Pediamécum: en pacientes inmunodeprimidos o con malabsorción, la dosis oral debe duplicarse respecto de la de inmunocompetentes.',
        'No hay datos de herpes zóster en niños inmunocompetentes (CIMA 84468). La infección neonatal por herpes simple y la encefalitis se tratan por vía intravenosa.',
        'Mantener una hidratación adecuada, sobre todo con dosis altas, en ancianos y en insuficiencia renal (riesgo de reacciones neurológicas) (CIMA, 4.4).',
        'Inmunocomprometidos (Pediamécum, ≥2 años): 1000 mg/día en 3-5 dosis, máximo 80 mg/kg/día sin exceder 1 g/día; no se carga.',
        'Suspensión: no diluir (CIMA 59226).',
    ]
    return ficha_oral(
        'aciclovir', 'Aciclovir', 'antiviral-antifungico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral; la ficha no indica relación con las comidas. Mantener una hidratación adecuada.',
            'fuente': fu(ACI_C, '4.2 Forma de administración'),
        },
        comerciales=['Aciclovir Cinfa', 'Zovirax'], discrepancias=disc,
        renal='Herpes simple con aclaramiento de creatinina <10 ml/min: 200 mg dos veces al día (cada 12 h). Varicela y zóster: 10-25 ml/min, '
              '800 mg tres veces al día (cada 8 h); <10 ml/min, 800 mg dos veces al día (cada 12 h).',
        fuente_ajuste=fu(ACI_C, '4.2 Insuficiencia renal (herpes simple y varicela/zóster)'),
        alertas=alertas,
    )


def fichas():
    return {
        'amoxicilina': amoxicilina(),
        'amoxicilina-clavulanico': amoxicilina_clavulanico(),
        'cefadroxilo': cefadroxilo(),
        'flucloxacilina': flucloxacilina(),
        'claritromicina': claritromicina(),
        'azitromicina': azitromicina(),
        'cotrimoxazol': cotrimoxazol(),
        'ciprofloxacino': ciprofloxacino(),
        'nitrofurantoina': nitrofurantoina(),
        'metronidazol': metronidazol(),
        'mebendazol': mebendazol(),
        'fluconazol': fluconazol(),
        'nistatina': nistatina(),
        'terbinafina': terbinafina(),
        'aciclovir': aciclovir(),
    }
