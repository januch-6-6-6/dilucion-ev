"""Orales, tanda 1a: analgésicos, antiinflamatorios, antihistamínicos y corticoides (15 fichas).

Cada cifra sale de datos/crudos/orales/ (fichas CIMA, Pediamécum y arsenal de APS de Atacama);
la tabla «cifra → archivo:línea» está en .superpowers/sdd/2026-10-05-orales-v1/task-12a-report.md.
"""
from .comun import (ARSENAL, discrepancia, dosis, ficha_oral, fu, fuente_arsenal, fuente_cima,
                    fuente_pediamecum_oral, pres)


def _ped(k):
    return f'PEDIAMECUM-{k.upper()}'


# ---------------------------------------------------------------- referencias CIMA
IBU_C = 'CIMA-IBUPROFENO-88314'  # Difenadol 400 mg comprimidos
IBU_S = 'CIMA-IBUPROFENO-74559'  # Difenadol Rapid 400 mg granulado (sobre)
DIC = 'CIMA-DICLOFENACO'  # Diclofenaco Cinfa 50 mg gastrorresistente
KET = 'CIMA-KETOROLACO'  # Ketorolaco Qualigen 10 mg
MEL = 'CIMA-MELOXICAM'  # Meloxicam Cinfa 15 mg
CEL = 'CIMA-CELECOXIB'  # Artilog 200 mg
MET = 'CIMA-METAMIZOL'  # Metamizol Cinfa 575 mg cápsulas
TRA_S = 'CIMA-TRAMADOL-61617'  # Adolonta 100 mg/ml solución oral
TRA_R = 'CIMA-TRAMADOL-61784'  # Adolonta retard 100 mg
PTR = 'CIMA-PARACETAMOL-TRAMADOL'  # Captor 37,5/325 mg
MOR_R = 'CIMA-MORFINA-57898'  # MST Continus 10 mg
MOR_G = 'CIMA-MORFINA-83323'  # Dropizol 10 mg/ml gotas
ALO = 'CIMA-ALOPURINOL'  # Alopurinol Cinfamed 100 mg
CIC = 'CIMA-CICLOBENZAPRINA'  # Yurelax 10 mg
LOR_C = 'CIMA-LORATADINA-58518'  # Clarityne 10 mg
LOR_J = 'CIMA-LORATADINA-64243'  # Loratadina Normon 1 mg/ml jarabe
DES_C = 'CIMA-DESLORATADINA-00160009'  # Aerius 5 mg
DES_S = 'CIMA-DESLORATADINA-00160065'  # Aerius 0,5 mg/ml solución oral
PRE = 'CIMA-PREDNISONA'  # Prednisona Cinfa 10 mg
DEX = 'CIMA-DEXAMETASONA'  # Dexametasona Abdrug 20 mg

POBLACION_SIN_CIFRA = 'Se muestra la dosis pediátrica de Pediamécum, marcada como uso fuera de ficha técnica (off-label)'


def fuentes():
    return [
        fuente_cima('ibuprofeno', '88314', 'Difenadol 400 mg comprimidos recubiertos con película', varios=True),
        fuente_cima('ibuprofeno', '74559', 'Difenadol Rapid 400 mg granulado para solución oral', varios=True),
        fuente_pediamecum_oral('ibuprofeno', 'Ibuprofeno', anio=2020),
        fuente_cima('diclofenaco', '62161', 'Diclofenaco Cinfa 50 mg comprimidos gastrorresistentes EFG'),
        fuente_pediamecum_oral('diclofenaco', 'Diclofenaco', anio=2020),
        fuente_cima('ketorolaco', '70105', 'Ketorolaco trometamol Qualigen 10 mg comprimidos recubiertos con película EFG'),
        fuente_pediamecum_oral('ketorolaco', 'Ketorolaco', anio=2026),
        fuente_cima('meloxicam', '69094', 'Meloxicam Cinfa 15 mg comprimidos EFG'),
        fuente_pediamecum_oral('meloxicam', 'Meloxicam', anio=2020),
        fuente_cima('celecoxib', '63891', 'Artilog 200 mg cápsulas duras'),
        fuente_pediamecum_oral('celecoxib', 'Celecoxib', anio=2020),
        fuente_cima('metamizol', '68116', 'Metamizol Cinfa 575 mg cápsulas duras EFG'),
        fuente_pediamecum_oral('metamizol', 'Metamizol', anio=2025),
        fuente_cima('tramadol', '61617', 'Adolonta 100 mg/ml solución oral', varios=True),
        fuente_cima('tramadol', '61784', 'Adolonta retard 100 mg comprimidos de liberación prolongada', varios=True),
        fuente_cima('paracetamol-tramadol', '75629', 'Captor 37,5 mg/325 mg comprimidos EFG'),
        fuente_cima('morfina', '57898', 'MST Continus 10 mg comprimidos de liberación prolongada', varios=True),
        fuente_cima('morfina', '83323', 'Dropizol 10 mg/ml gotas orales en solución', varios=True),
        fuente_pediamecum_oral('morfina', 'Morfina', anio=2020),
        fuente_cima('alopurinol', '84085', 'Alopurinol Cinfamed 100 mg comprimidos EFG'),
        fuente_pediamecum_oral('alopurinol', 'Alopurinol', anio=2020),
        fuente_cima('ciclobenzaprina', '56428', 'Yurelax 10 mg cápsulas duras'),
        fuente_cima('loratadina', '58518', 'Clarityne 10 mg comprimidos', varios=True),
        fuente_cima('loratadina', '64243', 'Loratadina Normon 1 mg/ml jarabe EFG', varios=True),
        fuente_pediamecum_oral('loratadina', 'Loratadina', anio=2020),
        fuente_cima('desloratadina', '00160009', 'Aerius 5 mg comprimidos recubiertos con película', varios=True),
        fuente_cima('desloratadina', '00160065', 'Aerius 0,5 mg/ml solución oral', varios=True),
        fuente_pediamecum_oral('desloratadina', 'Desloratadina', anio=2020),
        fuente_cima('prednisona', '75649', 'Prednisona Cinfa 10 mg comprimidos'),
        fuente_pediamecum_oral('prednisona', 'Prednisona', anio=2021),
        fuente_cima('dexametasona', '86125', 'Dexametasona Abdrug 20 mg comprimidos'),
        fuente_pediamecum_oral('dexametasona', 'Dexametasona', anio=2022),
        fuente_arsenal(),
    ]


# ---------------------------------------------------------------- AINE
def ibuprofeno():
    P = _ped('ibuprofeno')
    presentaciones = [
        pres('comprimido-400-mg', 'comprimido', mg=400, partible='no',
             fuente=fu(IBU_C, 'Difenadol 400 mg: "deben tragarse enteros, sin masticar, triturar ni chupar" (4.2)')),
        pres('sobre-400-mg', 'sobre', mg=400, partible='no',
             fuente=fu(IBU_S, 'Difenadol Rapid 400 mg granulado: "400 mg (1 sobre)" (4.2.1)')),
        pres('comprimido-200-mg', 'comprimido', mg=200, partible='no',
             fuente=fu(ARSENAL, 'Grupo 02.01: Ibuprofeno, Gragea o cápsula 200 mg (el arsenal solo indica la dosis; no dice si es partible)')),
        pres('suspension-20-mg-ml', 'suspension', mg_ml=20,
             fuente=fu(P, 'Presentaciones de Pediamécum: IBUPROFENO CINFA 20 MG/ML SUSPENSIÓN ORAL EFG')),
        pres('suspension-40-mg-ml', 'suspension', mg_ml=40,
             fuente=fu(P, 'Presentaciones de Pediamécum: IBUPROFENO CINFA 40 MG/ML SUSPENSION ORAL EFG')),
    ]
    dosis_ = [
        dosis('Dolor leve a moderado y fiebre (adultos y adolescentes ≥12 años y ≥40 kg)', 'adulto', 'fija', 'mg',
              min=400, max=400, tomas=3, intervalo_h=8, tope_dia=(1200, 'mg'),
              texto='400 mg (1 comprimido o 1 sobre) cada 6-8 horas; intervalo no inferior a 6 horas; máximo 1200 mg (3 comprimidos) en 24 horas',
              condicion='Solo uso a corto plazo; no recomendado en <40 kg ni <12 años (dosis del producto no adecuada)',
              fuente=fu(IBU_C, '4.2: "400 mg (1 comprimido) cada 6-8 horas ... no debe ser inferior a 6 horas. La dosis máxima diaria es de 1.200 mg (3 comprimidos)"')),
        dosis('Antipirético y analgésico (niños ≥6 meses)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=40,
              tomas=4, intervalo_h=6, tope_dia=(2400, 'mg'),
              condicion='Pediamécum (A), autorizado en niños ≥6 meses; la ficha CIMA cargada (Difenadol 400 mg) es de una presentación adulta '
                        'y no se recomienda en <40 kg o <12 años por su dosis fija. Usar la suspensión (20 o 40 mg/ml)',
              texto='40 mg/kg/día repartidos cada 6-8 horas; dosis máxima 2400 mg/día',
              presentaciones=['suspension-20-mg-ml', 'suspension-40-mg-ml', 'comprimido-200-mg'],
              fuente=fu(P, 'Oral: "Antipirético y analgésico ( A ) (autorizado en niños ≥6 meses): 40 mg/kg/día cada 6-8 horas. Dosis máxima: 2400 mg/día"')),
    ]
    disc = [
        discrepancia('Tope diario',
                     [(IBU_C, '1200 mg/24 h: adultos y adolescentes ≥12 años y ≥40 kg, 400 mg cada 6-8 h (CIMA, Difenadol 400 mg)'),
                      (P, '2400 mg/día: adolescentes, 400-600 mg cada 6-8 h (Pediamécum, párrafo de dismenorrea primaria)')],
                     '1200 mg/día como tope de adulto',
                     'Regla del tope más bajo para el adulto/adolescente ≥40 kg con dosis fija cada 6-8 h. La pauta por peso de Pediamécum '
                     '(40 mg/kg/día, ≥6 meses) es otro régimen con su propio máximo de 2400 mg/día (Ruling 9): no se reemplaza; '
                     'la calculadora aplica además el tope de adulto (1200 mg/día).'),
        discrepancia('Tabla por peso de Pediamécum (20-29 kg, 30-39 kg, ≥40 kg)',
                     [(P, '20-30 mg/kg/día en 3-4 dosis con topes de 600, 800 y 1200 mg/día por peso: aparece bajo el epígrafe «Intravenoso»')],
                     'No se carga como dosis oral',
                     'En el texto de Pediamécum esa tabla pertenece a la vía intravenosa (dolor moderado-grave y fiebre en >6 años y >20 kg), '
                     'no a la oral; el informe la había leído como una segunda pauta oral.'),
    ]
    alertas = [
        'Ibuprofeno a dosis altas (2400 mg/día) se asocia a un pequeño aumento del riesgo de acontecimientos trombóticos arteriales; '
        'con ≤1200 mg/día no se ha visto ese aumento (CIMA 88314, 4.4).',
        'Contraindicado en insuficiencia renal o hepática grave, insuficiencia cardíaca grave (NYHA IV), hemorragia activa y tercer trimestre de embarazo (CIMA 88314, 4.3).',
        'Se aconseja evitar ibuprofeno en caso de varicela (CIMA 88314, 4.4).',
        'Los comprimidos y sobres de 400 mg no son para <40 kg ni <12 años: en niños usar la suspensión y calcular por peso.',
    ]
    return ficha_oral(
        'ibuprofeno', 'Ibuprofeno', 'aine', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Comprimidos enteros con un vaso de agua, sin masticar, triturar ni chupar; con estómago sensible, tomar con alimentos '
                     '(CIMA 88314). Sobre: disolver en un vaso de agua (CIMA 74559). Pediamécum: antes de las comidas o con leche para evitar molestias digestivas.',
            'noTriturar': True,
            'fuente': fu(IBU_C, '4.2 Forma de administración'),
        },
        comerciales=['Difenadol', 'Difenadol Rapid'], discrepancias=disc,
        renal='Insuficiencia renal leve o moderada: reducir la dosis inicial; no usar en insuficiencia renal grave (contraindicado).',
        hepatico='Insuficiencia hepática leve o moderada: iniciar con dosis reducidas y vigilar; no usar en insuficiencia hepática grave (contraindicado).',
        fuente_ajuste=fu(IBU_C, '4.2 Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def diclofenaco():
    P = _ped('diclofenaco')
    presentaciones = [
        pres('comprimido-gastrorresistente-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(DIC, 'Diclofenaco Cinfa 50 mg: "deben tragarse enteros ... No deben dividirse ni masticarse" (4.2)')),
    ]
    dosis_ = [
        dosis('Enfermedades reumáticas, gota aguda, dolor e inflamación postraumática (adultos)', 'adulto', 'fija', 'mg', base='dia',
              min=75, max=100, tomas=2, tope_dia=(100, 'mg'),
              condicion='Tope mostrado: 100 mg/día, el extremo conservador; la ficha permite hasta 150 mg/día',
              texto='Casos leves y tratamientos prolongados: 75-100 mg al día en 2-3 tomas; dosis máxima diaria recomendada 100-150 mg',
              fuente=fu(DIC, '4.2.1: "75-100 mg al día. La dosis máxima diaria recomendada es de 100 a 150 mg ... en 2-3 tomas diarias"')),
        dosis('Dolor, fiebre e inflamación (niños de 1 a 12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=0.5, max=3,
              tomas=2, tope_dia=(150, 'mg'), estatus='off_label',
              condicion='La ficha técnica no lo recomienda en <14 años; el único comprimido (50 mg, no partible) no permite dosis pequeñas',
              texto='0,5-3 mg/kg/día repartidos en 2-4 dosis; máximo 150 mg/día',
              fuente=fu(P, 'Oral: "Niños de 1 a 12 años: 0,5-3 mg/kg/día, repartidos en 2-4 dosis. Máximo de 150 mg/día"')),
        dosis('Dolor e inflamación (niños de 12 a 14 años)', 'pediatrico', 'fija', 'mg', min=50, max=50, tomas=2, intervalo_h=12,
              estatus='off_label', condicion='Pediamécum autoriza (A) solo en mayores de 14 años; la ficha técnica no lo recomienda en <14 años',
              texto='Dosis inicial 50 mg cada 8-12 horas; mantenimiento 50 mg cada 12 horas',
              fuente=fu(P, 'Oral: "Niños >12 años: La dosis inicial es de 50 mg cada 8-12 horas; la dosis de mantenimiento 50 mg cada 12 horas"')),
        dosis('Dolor, fiebre e inflamación (adolescentes mayores de 14 años)', 'pediatrico', 'fija', 'mg', min=50, max=50, tomas=2,
              intervalo_h=12, condicion='Pediamécum (A) en mayores de 14 años; la ficha técnica solo lo desaconseja en <14 años',
              texto='Dosis inicial 50 mg cada 8-12 horas; mantenimiento 50 mg cada 12 horas',
              fuente=fu(P, 'Uso clínico: "en mayores de 14 años ( A )"; dosis: "Niños >12 años: ... 50 mg cada 8-12 horas; ... mantenimiento 50 mg cada 12 horas"')),
    ]
    disc = [
        discrepancia('Población pediátrica',
                     [(DIC, 'CIMA: debido a la dosis del comprimido no se recomienda en niños ni adolescentes menores de 14 años'),
                      (P, 'Pediamécum: 0,5-3 mg/kg/día en 2-4 dosis (máx. 150 mg/día) desde 1 año; autorizado (A) solo en mayores de 14 años')],
                     POBLACION_SIN_CIFRA,
                     'Contradicción de población, no de cifra: la ficha técnica no respalda la dosis en <14 años. El rango por peso es amplio (6 veces).'),
        discrepancia('Tope diario del adulto',
                     [(DIC, '100 mg/día: extremo inferior de "La dosis máxima diaria recomendada es de 100 a 150 mg"'),
                      (DIC, '150 mg/día: extremo superior del mismo rango')],
                     '100 mg/día',
                     'La ficha da un rango para el máximo; se muestra el extremo conservador y se avisa que permite hasta 150 mg/día.'),
    ]
    alertas = [
        'Contraindicado en insuficiencia cardíaca congestiva (NYHA II-IV), cardiopatía isquémica, enfermedad arterial periférica o cerebrovascular, '
        'insuficiencia hepática o renal grave y tercer trimestre de embarazo (CIMA, 4.3).',
        'Con factores de riesgo cardiovascular, en tratamientos de más de 4 semanas usar ≤100 mg diarios (CIMA, 4.2).',
        'Dismenorrea primaria (CIMA): 50-200 mg/día, con dosis inicial de 50-100 mg; no se carga como pauta aparte.',
        'El comprimido gastrorresistente de 50 mg no se puede partir: no sirve para dosis pediátricas pequeñas.',
        'Adultos: con el comprimido de 50 mg no partible solo se puede dar 100 mg/día (50 mg × 2 tomas). El extremo inferior de la ficha '
        '(75 mg/día en 2-3 tomas) exigiría 37,5 mg por toma (2 tomas) o 25 mg por toma (3 tomas): haría falta una presentación de 25 mg '
        '(3 × 25 mg) que no está cargada (CIMA, 4.2.1: "75-100 mg al día ... en 2-3 tomas diarias").',
    ]
    return ficha_oral(
        'diclofenaco', 'Diclofenaco', 'aine', presentaciones, dosis_,
        {
            'comida': 'antes',
            'texto': 'Comprimidos entéricos enteros, con líquido, preferentemente antes de las comidas; no dividir ni masticar (CIMA). '
                     'Pediamécum, en cambio, recomienda administrarlo tras las comidas para reducir el riesgo digestivo.',
            'noTriturar': True,
            'fuente': fu(DIC, '4.2 Forma de administración'),
        },
        comerciales=['Diclofenaco Cinfa'], discrepancias=disc,
        renal='Contraindicado en insuficiencia renal grave; precaución en leve a moderada (sin recomendación de ajuste de dosis).',
        hepatico='Contraindicado en insuficiencia hepática grave; precaución en leve a moderada (sin recomendación de ajuste de dosis).',
        fuente_ajuste=fu(DIC, '4.2 Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def ketorolaco():
    P = _ped('ketorolaco')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(KET, 'Ketorolaco Qualigen 10 mg comprimidos (la ficha no menciona ranura ni partición)')),
    ]
    dosis_ = [
        dosis('Dolor leve o moderado postoperatorio, a corto plazo (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=4,
              intervalo_h=6, tope_dia=(40, 'mg'), condicion='Duración máxima 7 días; iniciar en el medio hospitalario',
              texto='1 comprimido (10 mg) cada 4-6 horas; no sobrepasar 4 comprimidos al día (40 mg/día)',
              fuente=fu(KET, '4.2: "1 comprimido (10 mg) cada 4 a 6 horas ... no debiendo sobrepasar los 4 comprimidos al día (40 mg/día)"')),
        dosis('Dolor (niños de 2 a 16 años, y >16 años con <50 kg)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=1,
              tomas=4, intervalo_h=6, tope_toma=(10, 'mg'), tope_dia=(40, 'mg'), estatus='off_label',
              condicion='Por lo general como continuación de un tratamiento IV o IM; no exceder 5 días consecutivos',
              texto='1 mg/kg/dosis cada 4-6 horas (máximo 10 mg/dosis y 40 mg/día)',
              fuente=fu(P, 'Oral: "1 mg/kg/dosis (máximo, 10 mg/dosis y 40 mg/día), cada 4-6 horas ( E: off-label )"')),
    ]
    disc = [
        discrepancia('Población pediátrica',
                     [(KET, 'CIMA: eficacia y seguridad no establecidas en niños; no se recomienda en menores de 16 años'),
                      (P, 'Pediamécum: oral 1 mg/kg/dosis en 2-16 años (off-label)')],
                     POBLACION_SIN_CIFRA,
                     'Coinciden en el tope (40 mg/día) y en la duración máxima; difieren en la edad mínima.'),
    ]
    alertas = [
        'Duración total máxima 7 días, sumando vía parenteral y oral; con ambas vías no superar 90 mg/día en adultos y 60 mg/día en ancianos (CIMA, 4.2).',
        'Contraindicado en úlcera péptica activa o antecedente de sangrado digestivo, asma, insuficiencia renal moderada a grave, '
        'hipovolemia, embarazo, parto y lactancia (CIMA, 4.3).',
        'Ancianos (≥65 años): dosis en el límite inferior del intervalo (CIMA, 4.2).',
    ]
    return ficha_oral(
        'ketorolaco', 'Ketorolaco', 'aine', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Administración oral. La ficha técnica no indica relación con las comidas.',
            'fuente': fu(KET, '4.2 Posología y forma de administración'),
        },
        comerciales=['Ketorolaco Qualigen'], discrepancias=disc,
        renal='Contraindicado en insuficiencia renal moderada o grave (creatinina sérica >442 µmol/l). Con creatinina sérica 170-442 µmol/l: '
              'la mitad de la dosis recomendada, sin superar 60 mg/día, con control de la función renal.',
        fuente_ajuste=fu(KET, '4.2 Pacientes con insuficiencia renal'),
        alertas=alertas,
    )


def meloxicam():
    P = _ped('meloxicam')
    presentaciones = [
        pres('comprimido-15-mg', 'comprimido', mg=15, partible='mitades',
             fuente=fu(MEL, 'Meloxicam Cinfa 15 mg: 4.2 contempla "medio comprimido de 15 mg"')),
    ]
    dosis_ = [
        dosis('Crisis agudas de osteoartrosis (adultos)', 'adulto', 'fija', 'mg', min=7.5, max=7.5, tomas=1, intervalo_h=24,
              tope_dia=(15, 'mg'), texto='7,5 mg/día en una sola toma; si no mejora, puede aumentarse a 15 mg/día. No sobrepasar 15 mg/día',
              fuente=fu(MEL, '4.2: "Crisis agudas de osteoartrosis: 7,5 mg/día ... puede aumentarse a 15 mg/día" y "NO SOBREPASAR LA DOSIS DE 15 mg/día"')),
        dosis('Artritis reumatoide y espondilitis anquilosante (adultos)', 'adulto', 'fija', 'mg', min=7.5, max=15, tomas=1,
              intervalo_h=24, tope_dia=(15, 'mg'), texto='15 mg/día en una sola toma; puede reducirse a 7,5 mg/día. Ancianos: 7,5 mg/día',
              fuente=fu(MEL, '4.2: "Artritis reumatoide, espondilitis anquilosante: 15 mg/día ... puede reducirse a 7,5 mg/día"')),
        dosis('Osteoartritis, artritis reumatoide y espondilitis (adolescentes ≥16 años)', 'pediatrico', 'fija', 'mg', min=7.5, max=15,
              tomas=1, intervalo_h=24, tope_dia=(15, 'mg'), condicion='Solo ≥16 años: la ficha técnica lo contraindica en menores de 16 años',
              texto='7,5-15 mg/día (tope de 15 mg/día de la ficha técnica CIMA)',
              fuente=fu(P, '"Osteoartritis, artritis reumatoide y espondilitis (en pacientes ≥16 años o >50 kg): 7,5-15 mg/día"; tope: CIMA 4.2')),
    ]
    disc = [
        discrepancia('Población pediátrica',
                     [(MEL, 'CIMA: contraindicado en niños y adolescentes menores de 16 años (4.2 y 4.3)'),
                      (P, 'Pediamécum: artritis idiopática juvenil 0,125 mg/kg una vez al día, dosis máxima 7,5 mg/día (off-label; FDA desde 2 años)')],
                     'No se carga la pauta de artritis idiopática juvenil; solo la de adolescentes de dieciséis años o más',
                     'Donde la ficha técnica dice «contraindicado» no se carga dosis (regla de datos 4). El «>50 kg» de Pediamécum no habilita a menores de 16 años.'),
    ]
    alertas = [
        'Contraindicado en menores de 16 años, tercer trimestre de embarazo, antecedente de hemorragia o perforación digestiva por AINE, '
        'insuficiencia hepática grave e insuficiencia renal grave no dializada (CIMA, 4.3).',
        'Con riesgo aumentado de reacciones adversas (antecedente digestivo o factores de riesgo cardiovascular), iniciar con 7,5 mg/día (CIMA, 4.2).',
    ]
    return ficha_oral(
        'meloxicam', 'Meloxicam', 'aine', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Comprimidos con agua u otro líquido, junto con alimentos; la dosis diaria se toma en una sola toma.',
            'fuente': fu(MEL, '4.2 Forma de administración'),
        },
        comerciales=['Meloxicam Cinfa'], discrepancias=disc,
        renal='Hemodiálisis por enfermedad renal terminal: no superar 7,5 mg diarios. Aclaramiento de creatinina >25 ml/min: sin reducción. '
              'Contraindicado en fallo renal grave no dializado.',
        hepatico='Insuficiencia hepática leve a moderada: sin reducción de dosis; grave: contraindicado.',
        fuente_ajuste=fu(MEL, '4.2 Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def celecoxib():
    P = _ped('celecoxib')
    presentaciones = [
        pres('capsula-200-mg', 'capsula', mg=200, partible='no', fuente=fu(CEL, 'Artilog 200 mg cápsulas duras')),
        pres('capsula-100-mg', 'capsula', mg=100, partible='no',
             fuente=fu(P, '"Las únicas presentaciones disponibles en España son las cápsulas de 200 mg y de 100 mg"')),
    ]
    dosis_ = [
        dosis('Artrosis, artritis reumatoide y espondilitis anquilosante (adultos)', 'adulto', 'fija', 'mg', min=200, max=200,
              tomas=1, intervalo_h=24, tope_dia=(400, 'mg'),
              texto='200 mg al día en una o dos tomas; si el alivio es insuficiente, 200 mg dos veces al día. Máximo 400 mg/día en todas las indicaciones',
              fuente=fu(CEL, '4.2.1: "200 mg administrados una vez al día o en dos tomas" y "La dosis diaria máxima recomendada es de 400 mg"')),
        dosis('Artritis idiopática juvenil (niños 2-18 años)', 'pediatrico', 'por_edad', 'mg', tomas=2, intervalo_h=12,
              estatus='off_label', texto='Niños de 10-25 kg: 50 mg cada 12 h. Niños de más de 25 kg: 100 mg cada 12 h',
              condicion='Tabla por peso: se muestra, no se calcula. Con cápsulas de 100 o 200 mg no se puede dar 50 mg exactos',
              fuente=fu(P, '"Niños de 10-25 kg: 50 mg/12 h. Niños más de 25 kg: 100 mg/12 h"; uso clínico ( E: off label )')),
    ]
    disc = [
        discrepancia('Población pediátrica',
                     [(CEL, 'CIMA: no está indicado el uso de celecoxib en niños'),
                      (P, 'Pediamécum: artritis idiopática juvenil 50 mg cada 12 h (10-25 kg) o 100 mg cada 12 h (>25 kg), off-label')],
                     POBLACION_SIN_CIFRA,
                     'Contradicción de población, no de cifra. Pediamécum advierte que las cápsulas disponibles dificultan dosificar a niños pequeños.'),
    ]
    alertas = [
        'Contraindicado en cardiopatía isquémica, enfermedad arterial periférica o cerebrovascular, insuficiencia cardíaca NYHA II-IV, '
        'aclaramiento de creatinina <30 ml/min, alergia a sulfamidas, embarazo y lactancia (CIMA, 4.3).',
        'Si tras 2 semanas no mejora el beneficio, considerar otras alternativas (CIMA, 4.2).',
        'Metabolizadores lentos del CYP2C9: considerar la mitad de la dosis mínima recomendada (CIMA, 4.2).',
    ]
    return ficha_oral(
        'celecoxib', 'Celecoxib', 'aine', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Con o sin alimentos. Si cuesta tragar, el contenido de la cápsula puede mezclarse con una cucharadita de compota de manzana, '
                     'arroz, yogur o plátano y tomarse de inmediato con 240 ml de agua.',
            'fuente': fu(CEL, '4.2.2 Forma de administración'),
        },
        comerciales=['Artilog'], discrepancias=disc,
        renal='Experiencia limitada en insuficiencia renal leve o moderada: precaución. Contraindicado con aclaramiento de creatinina <30 ml/min.',
        hepatico='Insuficiencia hepática moderada (albúmina 25-35 g/l): iniciar con la mitad de la dosis recomendada. Grave: contraindicado.',
        fuente_ajuste=fu(CEL, '4.2 Insuficiencia hepática / Insuficiencia renal y 4.3'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- analgésico no opioide
def metamizol():
    P = _ped('metamizol')
    presentaciones = [
        pres('capsula-575-mg', 'capsula', mg=575, partible='no',
             fuente=fu(MET, 'Metamizol Cinfa 575 mg: "Las cápsulas deben ingerirse enteras, sin masticar" (4.2)')),
        pres('comprimido-300-mg', 'comprimido', mg=300, partible='no',
             fuente=fu(ARSENAL, 'Grupo 02.01: Metamizol sódico, Comprimido 300 mg (lectura por columnas del PDF)')),
        pres('solucion-gotas-500-mg-ml', 'jarabe', mg_ml=500,
             fuente=fu(P, 'Presentaciones de Pediamécum: METAMIZOL NORMON 500 MG/ML GOTAS ORALES EN SOLUCION EFG (metamizol sódico). '
                          'Se carga como solución: ninguna fuente da gotas por ml')),
    ]
    dosis_ = [
        dosis('Dolor agudo moderado o intenso y fiebre alta (adultos y adolescentes ≥15 años, >53 kg)', 'adulto', 'fija', 'mg',
              min=575, max=575, tomas=6, intervalo_h=4, tope_dia=(3450, 'mg'),
              texto='575 mg por dosis, hasta 6 veces al día en intervalos de 4-6 horas; máximo 3450 mg/día. Uso a corto plazo',
              fuente=fu(MET, '4.2: "575 mg de metamizol en una dosis única, que se puede administrar hasta 6 veces al día, en intervalos de 4 a 6 horas, correspondiente a una dosis máxima diaria de 3.450 mg"')),
        dosis('Dolor y fiebre (niños y adolescentes hasta 14 años)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', min=8, max=16,
              tomas=4, intervalo_h=6,
              condicion='Pediamécum (A) para la forma oral; la ficha CIMA cargada (cápsula 575 mg) es de una presentación adulta. '
                        'En fiebre, 10 mg/kg suele bastar. Usar solución o comprimidos',
              texto='8-16 mg/kg cada 6-8 horas',
              presentaciones=['solucion-gotas-500-mg-ml', 'comprimido-300-mg'],
              fuente=fu(P, 'Vía oral: "En niños y adolescentes hasta de 14 años de edad, se pueden administrar de 8 a 16 mg/kg cada 6-8 horas"')),
        dosis('Dolor y fiebre: tabla por edad y peso (niños)', 'pediatrico', 'por_edad', 'mg',
              texto='<12 meses (<9 kg): 25-125 mg/dosis, máx. 100-500 mg/día. 1-3 años (9-15 kg): 75-250 mg/dosis, máx. 300-1000 mg/día. '
                    '4-6 años (16-23 kg): 125-375 mg/dosis, máx. 500-1500 mg/día. 7-9 años (24-30 kg): 200-500 mg/dosis, máx. 800-2000 mg/día. '
                    '10-12 años (31-45 kg): 250-750 mg/dosis, máx. 1000-3000 mg/día. 13-14 años (46-53 kg): 375-875 mg/dosis, máx. 1500-3500 mg/día',
              tope_toma=(875, 'mg'),
              condicion='Tabla por edad: se muestra, no se calcula. El tope por toma cargado (875 mg) es solo el de la fila 13-14 años; '
                        'cada fila de la tabla tiene su propio máximo por dosis y por día. '
                        'Pediamécum (A) para la forma oral; la ficha CIMA cargada es de una presentación adulta',
              presentaciones=['solucion-gotas-500-mg-ml', 'comprimido-300-mg'],
              fuente=fu(P, 'Tabla "Edad (peso) mg/dosis Dosis máxima diaria (mg)" de la vía oral; tope por toma = fila 13-14 años "375-875"')),
    ]
    disc = [
        discrepancia('Tope diario del adulto',
                     [(MET, '3450 mg/día: cápsulas de 575 mg, adultos y adolescentes ≥15 años (>53 kg) (CIMA); Pediamécum da el mismo máximo para esta población'),
                      (P, '4000 mg/día: "En general, la dosis oral máxima de metamizol magnésico es de 4000 mg/día" (Pediamécum)')],
                     '3450 mg/día',
                     'Misma sal (la cápsula Metamizol Cinfa 575 mg es metamizol magnésico) y misma población (≥15 años, >53 kg): se aplica la regla '
                     'del tope más bajo y se muestran 3450 mg/día. En CIMA, los 4000 mg/día corresponden al uso oral de la ampolla en el dolor '
                     'oncológico (media ampolla hasta 4 veces al día, máximo 7 días): otra presentación e indicación.'),
    ]
    alertas = [
        'Contraindicado con antecedente de agranulocitosis por metamizol u otras pirazolonas, alteración de la médula ósea, asma por analgésicos, '
        'porfiria hepática aguda, déficit de G6PD y tercer trimestre de embarazo (CIMA, 4.3).',
        'La cápsula de 575 mg no se recomienda en <15 años por su cantidad fija; existen otras formas para niños (CIMA, 4.2).',
        'Gotas orales 500 mg/ml: ninguna fuente cargada indica cuántas gotas tiene 1 ml; la calculadora da el volumen en ml.',
        'Pediamécum describe dosis off-label de 12,5-20 mg/kg cada 6 h; no se cargan.',
        'La pauta de 8-16 mg/kg no trae tope propio; los máximos por dosis y por día están en la tabla por edad (hasta 875 mg/dosis en 13-14 años).',
        'Reducir la dosis en ancianos, pacientes debilitados y con aclaramiento de creatinina disminuido (CIMA, 4.2).',
    ]
    return ficha_oral(
        'metamizol', 'Metamizol (dipirona)', 'analgesico-no-opioide', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Cápsulas enteras, sin masticar, con un poco de líquido. El efecto suele aparecer a los 30-60 minutos.',
            'noTriturar': True,
            'fuente': fu(MET, '4.2 Forma de administración'),
        },
        comerciales=['Metamizol Cinfa'], discrepancias=disc,
        renal='Reducir la dosis con aclaramiento de creatinina disminuido; evitar dosis elevadas repetidas en insuficiencia renal. '
              'En tratamientos cortos no es necesario reducir.',
        hepatico='Evitar dosis elevadas repetidas en insuficiencia hepática; en tratamientos cortos no es necesario reducir.',
        fuente_ajuste=fu(MET, '4.2 Poblaciones especiales / Insuficiencia hepática y renal'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- opioides
def tramadol():
    presentaciones = [
        pres('solucion-oral-100-mg-ml', 'jarabe', mg_ml=100,
             fuente=fu(TRA_S, 'Adolonta 100 mg/ml solución oral con bomba dosificadora: "1 pulsación = 0,125 ml de solución oral = 12,5 mg"')),
        pres('comprimido-retard-100-mg', 'comprimido', mg=100, partible='no', retard=True,
             fuente=fu(TRA_R, 'Adolonta retard 100 mg: "se deben tomar enteros, sin dividir ni masticar" (4.2.2)')),
        pres('capsula-50-mg', 'capsula', mg=50, partible='no',
             fuente=fu(ARSENAL, 'Grupo 02.02: Tramadol, Cápsula 50 mg')),
    ]
    dosis_ = [
        dosis('Dolor moderado a intenso (adultos y adolescentes >12 años)', 'adulto', 'fija', 'mg', min=50, max=100, tomas=4,
              intervalo_h=6, tope_toma=(100, 'mg'), tope_dia=(400, 'mg'),
              texto='50-100 mg cada 4-6 horas; no exceder 100 mg por toma ni 400 mg/día',
              presentaciones=['solucion-oral-100-mg-ml', 'capsula-50-mg'],
              fuente=fu(TRA_S, '4.2.1: "50-100 mg cada 4-6 horas ... No se debe exceder de 100 mg de tramadol por toma"; "No deben superarse dosis diarias de 400 mg"')),
        dosis('Dolor moderado a intenso, liberación prolongada (adultos y adolescentes >12 años)', 'adulto', 'fija', 'mg', min=100,
              max=100, tomas=2, intervalo_h=12, tope_dia=(400, 'mg'),
              texto='Dosis inicial 50-100 mg dos veces al día (mañana y noche); puede aumentarse a 150-200 mg dos veces al día. Máximo 400 mg/día. '
                    'El comprimido retard de 100 mg no se divide',
              presentaciones=['comprimido-retard-100-mg'],
              fuente=fu(TRA_R, '4.2.1: "50-100 mg ... dos veces al día ... incrementar la dosis a 150 mg o 200 mg ... dos veces al día"; "No deberían superarse dosis diarias de 400 mg"')),
        dosis('Dolor moderado a intenso (niños desde 3 años)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=1, tomas=4,
              intervalo_h=6, condicion='Contraindicado en <3 años. Dosis máxima 2 mg/kg por toma y 8 mg/kg/día; solo con la solución oral',
              texto='1 mg/kg por toma, 3-4 veces en 24 h (cada 6-8 h); máximo 2 mg/kg por toma y 8 mg/kg en 24 h. '
                    'Al pasar a pulsaciones, redondear hacia abajo',
              presentaciones=['solucion-oral-100-mg-ml'],
              fuente=fu(TRA_S, '4.2.1 Población pediátrica: "1 mg de tramadol por kg ... en cada toma. La dosis máxima recomendada por toma es de 2 mg ... de 3 a 4 veces en 24 horas ... 8 mg ... por kg"')),
        dosis('Dolor moderado a intenso: tabla orientativa por peso en pulsaciones (niños)', 'pediatrico', 'por_edad', 'mg',
              texto='1 pulsación = 0,125 ml = 12,5 mg. 15-20 kg (3-5 años): habitual 1, máx. 2 pulsaciones. 20-25 kg (5-8 años): 1, máx. 3. '
                    '25-35 kg (8-11 años): 2, máx. 4. 35-37 kg (11 años): 3, máx. 5. 37-44 kg (11-13 años): 3, máx. 6. '
                    '44-45 kg (>13 años): 3, máx. 7 pulsaciones por toma',
              condicion='Tabla orientativa: se muestra, no se calcula',
              presentaciones=['solucion-oral-100-mg-ml'],
              fuente=fu(TRA_S, '4.2.1: tabla "Dosis habitual / Dosis máxima por peso del niño y por toma (en pulsaciones)"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (Pediamécum no tiene ficha de tramadol); no hay contraste con otra fuente.',
        'Contraindicado en menores de 3 años, con IMAO (o en los 14 días previos), epilepsia no controlada e intoxicación aguda por alcohol, '
        'hipnóticos, opioides o psicótropos (CIMA, 4.3).',
        'No recomendado en metabolizadores ultrarrápidos ni en niños con problemas respiratorios operados de adenoidectomía/amigdalectomía: '
        'riesgo de depresión respiratoria mortal (CIMA, 4.2).',
        'La solución oral se dosifica en pulsaciones de la bomba (1 pulsación = 0,125 ml = 12,5 mg); la calculadora da ml. '
        'El arsenal chileno lista gotas orales 100 mg/ml, pero ninguna fuente cargada indica cuántas gotas tiene 1 ml.',
        'El comprimido retard no debe usarse en menores de 12 años ni en insuficiencia renal o hepática grave (CIMA 61784).',
    ]
    return ficha_oral(
        'tramadol', 'Tramadol', 'analgesico-opioide', presentaciones, dosis_, {
            'comida': 'indiferente',
            'texto': 'Solución: con un poco de líquido o de azúcar, con o sin comidas (CIMA 61617). Retard: enteros, sin dividir ni masticar, '
                     'con suficiente líquido, independientemente de las comidas (CIMA 61784).',
            'noTriturar': True,
            'fuente': fu(TRA_R, '4.2.2 Forma de administración (y 4.2.2 de la solución oral, ficha 61617)'),
        },
        comerciales=['Adolonta', 'Adolonta retard'], alto_riesgo=True,
        renal='La eliminación es lenta: considerar cuidadosamente prolongar el intervalo entre dosis. Retard: no recomendado en insuficiencia renal grave.',
        hepatico='La eliminación es lenta: considerar cuidadosamente prolongar el intervalo entre dosis. Retard: no recomendado en insuficiencia hepática grave.',
        fuente_ajuste=fu(TRA_R, '4.2.1 Insuficiencia renal/diálisis e insuficiencia hepática'),
        alertas=alertas,
    )


def paracetamol_tramadol():
    presentaciones = [
        pres('comprimido-37-5-325-mg', 'comprimido', mg=37.5, partible='no',
             fuente=fu(PTR, 'Captor 37,5 mg/325 mg: cantidad expresada en mg de tramadol (325 mg de paracetamol por comprimido); '
                            'la ranura de 37,5/325 sirve para fraccionar y facilitar la deglución, no para medias dosis (4.2.2)')),
    ]
    dosis_ = [
        dosis('Dolor moderado a intenso (adultos y adolescentes ≥12 años), en mg de tramadol', 'adulto', 'fija', 'mg', min=75, max=75,
              tomas=4, intervalo_h=6, tope_dia=(300, 'mg'),
              texto='Dosis inicial 2 comprimidos (2 × 37,5 mg de tramadol + 2 × 325 mg de paracetamol); intervalo mínimo 6 horas; '
                    'máximo 8 comprimidos al día (300 mg de tramadol y 2600 mg de paracetamol)',
              fuente=fu(PTR, '4.2.1: "dosis inicial de dos comprimidos ... sin exceder de 8 comprimidos (equivalente a 300 mg de tramadol y 2600 mg de paracetamol) al día"; '
                             '"El intervalo entre dosis no deberá ser menor de 6 horas"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (Captor); no hay contraste con otra fuente.',
        'Cada comprimido contiene 37,5 mg de tramadol y 325 mg de paracetamol: la dosis y la presentación se expresan en mg de tramadol.',
        'No sumar con otros medicamentos con paracetamol o tramadol sin contar el total diario.',
        'Contraindicado en insuficiencia hepática grave, epilepsia no controlada, con IMAO (o en las 2 semanas previas) e intoxicación aguda por alcohol u opioides (CIMA, 4.3).',
        '>75 años: intervalo mínimo entre dosis no inferior a 6 horas (CIMA, 4.2).',
    ]
    return ficha_oral(
        'paracetamol-tramadol', 'Paracetamol + tramadol', 'analgesico-opioide', presentaciones, dosis_, {
            'comida': 'indiferente',
            'texto': 'Vía oral, con suficiente líquido; los comprimidos no deben masticarse. La ficha no indica relación con las comidas.',
            'noTriturar': True,
            'fuente': fu(PTR, '4.2.2 Forma de administración'),
        },
        comerciales=['Captor'], alto_riesgo=True, pediatria='solo_adulto',
        motivo_solo_adulto='La ficha técnica (Captor) no lo recomienda en menores de 12 años: seguridad y eficacia no establecidas.',
        renal='Aclaramiento de creatinina 10-30 ml/min: aumentar el intervalo a 12 horas. <10 ml/min: no recomendado.',
        hepatico='Insuficiencia hepática grave: no usar. Moderada: considerar prolongar el intervalo entre dosis.',
        fuente_ajuste=fu(PTR, '4.2.1 Insuficiencia renal/diálisis e insuficiencia hepática'),
        alertas=alertas,
    )


def morfina():
    P = _ped('morfina')
    presentaciones = [
        pres('comprimido-lp-10-mg', 'comprimido', mg=10, partible='no', retard=True,
             fuente=fu(MOR_R, 'MST Continus 10 mg: "deben ser tragados enteros, y no deben romperse, masticarse o triturarse" (4.2)')),
        pres('comprimido-lp-30-mg', 'comprimido', mg=30, partible='no', retard=True,
             fuente=fu(ARSENAL, 'Grupo 01.05: Morfina, Comprimido de liberación prolongada 30 mg')),
        pres('gotas-20-mg-ml-arsenal', 'jarabe', mg_ml=20,
             fuente=fu(ARSENAL, 'Grupos 01.05 y 02.02: Morfina, Solución para gotas orales 20 mg/mL. Se carga como solución: ninguna fuente da gotas por ml')),
    ]
    dosis_ = [
        dosis('Dolor crónico intenso, comprimidos de liberación prolongada (adultos)', 'adulto', 'fija', 'mg', min=30, max=30, tomas=2,
              intervalo_h=12, condicion='Pacientes con dolor intenso no controlado con opioides más débiles; reducir la dosis inicial en debilitados o de poco peso',
              texto='Empezar con 30 mg cada 12 horas, aumentando a 60 mg cada 12 horas si fuera necesario; incrementos posteriores del 30-50 %',
              presentaciones=['comprimido-lp-10-mg', 'comprimido-lp-30-mg'],
              fuente=fu(MOR_R, '4.2: "normalmente deberá empezar con comprimidos de 30 mg cada 12 horas, aumentando a 60 mg cada 12 horas si fuera necesario"')),
        dosis('Dolor postquirúrgico, liberación prolongada (adultos <70 kg)', 'adulto', 'fija', 'mg', min=20, max=20, tomas=2,
              intervalo_h=12, condicion='No en las primeras 24 h del postoperatorio ni hasta que se normalice la función intestinal',
              presentaciones=['comprimido-lp-10-mg', 'comprimido-lp-30-mg'],
              fuente=fu(MOR_R, '4.2 Dolor post-quirúrgico: "Comprimidos de 20 mg cada 12 horas en pacientes de menos de 70 kg de peso"')),
        dosis('Dolor postquirúrgico, liberación prolongada (adultos >70 kg)', 'adulto', 'fija', 'mg', min=30, max=30, tomas=2,
              intervalo_h=12, condicion='No en las primeras 24 h del postoperatorio ni hasta que se normalice la función intestinal',
              presentaciones=['comprimido-lp-10-mg', 'comprimido-lp-30-mg'],
              fuente=fu(MOR_R, '4.2 Dolor post-quirúrgico: "Comprimidos de 30 mg cada 12 horas en pacientes de más de 70 kg de peso"')),
        dosis('Dolor oncológico intenso y crónico, liberación prolongada (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='toma',
              min=0.2, max=0.8, tomas=2, intervalo_h=12,
              condicion='Solo comprimidos de liberación prolongada (no gotas ni solución); no en dolor postoperatorio en niños; los de 200 mg no son pediátricos',
              texto='Dosis inicial 0,2-0,8 mg/kg cada 12 horas; graduar como en adultos',
              presentaciones=['comprimido-lp-10-mg', 'comprimido-lp-30-mg'],
              fuente=fu(MOR_R, '4.2 Población pediátrica: "dosis inicial de entre 0,2 y 0,8 mg/kg cada 12 horas"; Pediamécum coincide')),
        dosis('Dolor (formas orales de liberación normal), por edad (niños)', 'pediatrico', 'por_edad', 'mg',
              texto='>13 años: inicial 10-20 mg cada 4-6 h. 6-12 años: máx. 5-10 mg cada 4 h. 1-6 años: máx. 2,5-5 mg cada 4 h. No usar en menores de 1 año',
              estatus='off_label',
              condicion='Tabla por edad: se muestra, no se calcula. Pediamécum (A), pero ninguna ficha CIMA cargada autoriza morfina de '
                        'liberación normal en niños: la única pauta pediátrica de ficha técnica (MST Continus, CIMA 57898) es para comprimidos '
                        'de liberación prolongada en dolor oncológico. Opioide de alto riesgo ⇒ off-label (Ruling 11). Confirmar la concentración del frasco',
              presentaciones=['gotas-20-mg-ml-arsenal'],
              fuente=fu(P, 'Formas de liberación normal de sulfato de morfina (solución oral, comprimidos): ">13 años: inicial, 10-20 mg/4-6 h. '
                           '6-12 años: máx. 5-10 mg/4 h. 1-6 años: máx. 2,5-5 mg/4 h"; "No usar en menores de un año"')),
    ]
    disc = [
        discrepancia('Concentración de las gotas orales',
                     [(MOR_G, 'Dropizol (CIMA): 10 mg/ml'), (ARSENAL, 'Arsenal de APS de Atacama: solución para gotas orales 20 mg/mL')],
                     'Solo se carga la concentración del arsenal chileno como presentación; elegir siempre la concentración del frasco',
                     'Riesgo de error de concentración (doble). Dropizol no se carga como presentación porque es antidiarreico y ninguna dosis de la ficha la usa.'),
        discrepancia('Población de las gotas',
                     [(MOR_G, 'Dropizol (CIMA): no usar en menores de 18 años; indicado solo en diarrea aguda del adulto'),
                      (P, 'Pediamécum: formas orales de liberación normal desde 1 año (dolor)')],
                     'Se muestra la tabla por edad de Pediamécum para liberación normal; Dropizol no se usa como pauta analgésica',
                     'La restricción de edad de Dropizol corresponde a otra indicación (antidiarreico), no al uso analgésico.'),
    ]
    alertas = [
        'Opioide de alto riesgo: confirmar concentración y forma (liberación prolongada cada 12 h vs. liberación normal cada 4 h) antes de calcular.',
        'La fuente no da tope pediátrico para 0,2-0,8 mg/kg cada 12 h (dolor oncológico crónico); la dosis inicial de adulto es 30 mg cada 12 h '
        '(CIMA 57898): no usar sin supervisión especializada.',
        'Los comprimidos de liberación prolongada se tragan enteros: rotos, masticados o triturados liberan rápidamente una dosis potencialmente letal (CIMA 57898).',
        'Liberación prolongada: no en las primeras 24 h del postoperatorio; en niños no se recomienda para dolor postoperatorio (CIMA 57898).',
        'Dropizol (CIMA, 10 mg/ml) está autorizado solo para la diarrea aguda del adulto (5-10 gotas 2-3 veces al día, dosis individual ≤1 ml '
        'y diaria ≤6 ml) y no se debe usar en <18 años: no es una pauta analgésica.',
        'El arsenal chileno lista gotas orales de 20 mg/ml: el doble que Dropizol. Ninguna fuente cargada indica cuántas gotas tiene 1 ml.',
        'Ancianos (>65 años): puede ser aconsejable reducir la dosis (CIMA 57898).',
    ]
    return ficha_oral(
        'morfina', 'Morfina', 'analgesico-opioide', presentaciones, dosis_, {
            'comida': 'indiferente',
            'texto': 'Vía oral. Comprimidos de liberación prolongada cada 12 horas, enteros, sin romper, masticar ni triturar. '
                     'La ficha no indica relación con las comidas.',
            'noTriturar': True,
            'fuente': fu(MOR_R, '4.2 Posología y Forma de administración'),
        },
        comerciales=['MST Continus'], alto_riesgo=True, discrepancias=disc,
        renal='MST Continus: reducir la dosis en enfermedad renal crónica, como con todos los narcóticos; precaución con función renal gravemente alterada. '
              'Dropizol: la insuficiencia renal reduce y retrasa la eliminación (evitar o reducir la dosis).',
        hepatico='MST Continus: reducir la dosis en enfermedad hepática crónica; precaución con función hepática gravemente alterada. '
                 'Dropizol: la morfina puede precipitar coma en insuficiencia hepática (evitar o reducir la dosis).',
        fuente_ajuste=fu(MOR_R, '4.4 (reducir la dosis en enfermedad renal y hepática crónica); Dropizol 83323, 4.2'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- antigotoso
def alopurinol():
    P = _ped('alopurinol')
    presentaciones = [
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(ALO, 'Alopurinol Cinfamed 100 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('comprimido-300-mg', 'comprimido', mg=300, partible='no', fuente=fu(ARSENAL, 'Grupo 02.03: Alopurinol, Comprimido 300 mg')),
    ]
    dosis_ = [
        dosis('Hiperuricemia, alteraciones leves (adultos)', 'adulto', 'fija', 'mg', base='dia', min=100, max=200, tomas=1,
              condicion='Iniciar con dosis bajas (p. ej. 100 mg/día) y subir solo si el urato sérico no responde',
              texto='100-200 mg diarios, una vez al día después de las comidas',
              fuente=fu(ALO, '4.2: "100 a 200 mg diarios en alteraciones leves"; "una vez al día después de las comidas"')),
        dosis('Hiperuricemia, alteraciones moderadas (adultos)', 'adulto', 'fija', 'mg', base='dia', min=300, max=600, tomas=1,
              condicion='Si supera 300 mg y hay intolerancia digestiva, puede repartirse en varias tomas',
              texto='300-600 mg diarios',
              fuente=fu(ALO, '4.2: "300 a 600 mg diarios en alteraciones moderadas"')),
        dosis('Hiperuricemia, alteraciones graves (adultos)', 'adulto', 'fija', 'mg', base='dia', min=700, max=900, tomas=1,
              condicion='Si hay intolerancia digestiva, repartir en varias tomas',
              texto='700-900 mg diarios',
              fuente=fu(ALO, '4.2: "700 a 900 mg diarios en alteraciones graves"')),
        dosis('Hiperuricemia asociada a enfermedades neoplásicas y quimioterapia (niños <15 años)', 'pediatrico', 'por_peso', 'mg/kg',
              base='dia', min=10, max=20, tomas=3, intervalo_h=8, tope_dia=(400, 'mg'),
              condicion='Uso pediátrico raramente indicado salvo procesos malignos y alteraciones enzimáticas (CIMA). Ojo: las unidades varían entre fuentes',
              texto='10-20 mg/kg/día cada 8 horas; tope 400 mg/día (CIMA: 100-400 mg diarios; Pediamécum: máximo 800 mg/día)',
              fuente=fu(P, 'Vía oral: "Por peso 10-20 mg/kg/día cada 8 horas (dosis máxima: 800 mg/día)"; tope mostrado: CIMA 84085 4.2 "10 a 20 mg/kg ... o 100 a 400 mg diarios"')),
    ]
    disc = [
        discrepancia('Tope diario pediátrico',
                     [(ALO, '400 mg/día: niños <15 años, 10-20 mg/kg/día o 100-400 mg diarios (CIMA)'),
                      (P, '800 mg/día: 10-20 mg/kg/día cada 8 h; por edad >10 años y adolescentes 600-800 mg/día (Pediamécum)')],
                     '400 mg/día',
                     'Mismo régimen y población (niños, por peso): se muestra el tope más bajo. En la tabla por edad de Pediamécum '
                     '(<6 años 150, 6-10 años 300, >10 años 600-800 mg/día) solo la fila >10 años supera ese tope; la tabla no se carga como dosis.'),
    ]
    alertas = [
        'Riesgo de error de unidad: las fuentes pediátricas dosifican en mg/m², mg/kg/día y mg fijos (Pediamécum).',
        'Iniciar a dosis bajas para reducir el riesgo de reacciones adversas (CIMA, 4.2).',
        'Pediamécum describe además pautas por superficie corporal (50-100 mg/m²/dosis cada 8 h); no se cargan.',
    ]
    return ficha_oral(
        'alopurinol', 'Alopurinol', 'antigotoso', presentaciones, dosis_, {
            'comida': 'despues',
            'texto': 'Una vez al día después de las comidas; se tolera mejor tras la ingesta. Si la dosis supera 300 mg y hay intolerancia '
                     'digestiva, repartir en varias tomas.',
            'fuente': fu(ALO, '4.2 Frecuencia de la dosificación'),
        },
        comerciales=['Alopurinol Cinfamed'], discrepancias=disc,
        renal='Iniciar con un máximo de 100 mg/día y aumentar solo si la respuesta no es satisfactoria. Insuficiencia renal grave: menos de 100 mg/día '
              'o 100 mg a intervalos mayores de un día. Diálisis 2-3 veces por semana: 300-400 mg inmediatamente después de cada sesión.',
        hepatico='En pacientes con alteración hepática se debe reducir la dosis; pruebas periódicas de función hepática al inicio del tratamiento.',
        fuente_ajuste=fu(ALO, '4.2 Dosis recomendada en casos de insuficiencia renal / diálisis renal / insuficiencia hepática'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- relajante muscular
def ciclobenzaprina():
    presentaciones = [
        pres('capsula-10-mg', 'capsula', mg=10, partible='no', fuente=fu(CIC, 'Yurelax 10 mg cápsulas duras')),
    ]
    dosis_ = [
        dosis('Espasmo muscular asociado a condiciones agudas dolorosas musculoesqueléticas (adultos)', 'adulto', 'fija', 'mg', min=10,
              max=10, tomas=3, intervalo_h=8, tope_dia=(60, 'mg'), condicion='No más de 3 semanas',
              texto='1 cápsula de 10 mg tres veces al día; rango 20-40 mg diarios en dosis fraccionadas, hasta un máximo de 60 mg diarios',
              fuente=fu(CIC, '4.2: "1 cápsula de 10 mg, tres veces al día ... entre 20 y 40 mg diarios ... hasta un máximo de 60 mg diarios"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (Yurelax); no hay contraste con otra fuente.',
        'El periodo de tratamiento no debe superar 3 semanas (CIMA).',
        'Contraindicado en arritmias, alteraciones de la conducción, insuficiencia cardíaca congestiva, infarto reciente, hipertiroidismo '
        'y con IMAO (o en los 14 días previos) (CIMA, 4.3).',
        'Riesgo de síndrome serotoninérgico con ISRS, IRSN, tricíclicos, IMAO o buprenorfina (CIMA, 4.4).',
    ]
    return ficha_oral(
        'ciclobenzaprina', 'Ciclobenzaprina', 'relajante-muscular', presentaciones, dosis_, {
            'comida': 'indiferente',
            'texto': 'Las cápsulas pueden tomarse con un poco de agua. La ficha no indica relación con las comidas.',
            'fuente': fu(CIC, '4.2.2 Forma de administración'),
        },
        comerciales=['Yurelax'], pediatria='solo_adulto',
        motivo_solo_adulto='Fuente única (ficha técnica de Yurelax, CIMA) sin pauta pediátrica; Pediamécum no tiene ficha de ciclobenzaprina.',
        hepatico='Insuficiencia hepática moderada o severa: usar con precaución por posible aumento de las concentraciones plasmáticas.',
        fuente_ajuste=fu(CIC, '4.4 Advertencias: insuficiencia hepática'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- antihistamínicos
def loratadina():
    P = _ped('loratadina')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(LOR_C, 'Clarityne 10 mg comprimidos (no adecuado para ≤30 kg; la ficha no menciona partición)')),
        pres('jarabe-1-mg-ml', 'jarabe', mg_ml=1, fuente=fu(LOR_J, 'Loratadina Normon 1 mg/ml jarabe')),
    ]
    dosis_ = [
        dosis('Rinitis alérgica y urticaria (adultos y niños >12 años)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=1, intervalo_h=24,
              texto='1 comprimido de 10 mg (o 10 ml de jarabe) una vez al día',
              fuente=fu(LOR_C, '4.2.1 Adultos: "1 comprimido una vez al día"; jarabe (64243): "10 ml (10 mg) de jarabe una vez al día"')),
        dosis('Rinitis alérgica y urticaria (niños de 2 a 12 años con ≤30 kg)', 'pediatrico', 'fija', 'mg', min=5, max=5, tomas=1,
              intervalo_h=24, condicion='No establecida en menores de 2 años; el comprimido de 10 mg no es adecuado para ≤30 kg',
              texto='5 ml (5 mg) de jarabe una vez al día',
              presentaciones=['jarabe-1-mg-ml'],
              fuente=fu(LOR_J, '4.2: "Peso corporal igual o inferior a 30 kg: 5 ml (5 mg) de jarabe una vez al día"')),
        dosis('Rinitis alérgica y urticaria (niños de 2 a 12 años con >30 kg)', 'pediatrico', 'fija', 'mg', min=10, max=10, tomas=1,
              intervalo_h=24, texto='10 mg una vez al día (1 comprimido o 10 ml de jarabe)',
              fuente=fu(P, '"Peso corporal >30 kg: Comprimidos: 10 mg, 1 vez al día ... Jarabe: 10 ml (10 mg) de jarabe, 1 vez al día"; CIMA coincide')),
    ]
    alertas = [
        'No se ha establecido la seguridad y eficacia en menores de 2 años (CIMA); Pediamécum lo marca como off-label.',
    ]
    return ficha_oral(
        'loratadina', 'Loratadina', 'antihistaminico', presentaciones, dosis_, {
            'comida': 'indiferente',
            'texto': 'Vía oral, con independencia de las horas de las comidas.',
            'fuente': fu(LOR_C, '4.2.2 Forma de administración'),
        },
        comerciales=['Clarityne', 'Loratadina Normon'],
        renal='No se requiere ajuste en insuficiencia renal.',
        hepatico='Daño hepático grave: dosis inicial más baja; adultos y niños >30 kg, 10 mg en días alternos; niños ≤30 kg, 5 ml (5 mg) en días alternos.',
        fuente_ajuste=fu(LOR_J, '4.2 Pacientes con insuficiencia hepática / renal'),
        alertas=alertas,
    )


def desloratadina():
    P = _ped('desloratadina')
    presentaciones = [
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='no', fuente=fu(DES_C, 'Aerius 5 mg comprimidos recubiertos con película')),
        pres('solucion-oral-0-5-mg-ml', 'jarabe', mg_ml=0.5, fuente=fu(DES_S, 'Aerius 0,5 mg/ml solución oral')),
    ]
    dosis_ = [
        dosis('Rinitis alérgica y urticaria (adultos y adolescentes ≥12 años)', 'adulto', 'fija', 'mg', min=5, max=5, tomas=1,
              intervalo_h=24, texto='1 comprimido de 5 mg (o 10 ml de solución oral) una vez al día',
              fuente=fu(DES_C, '4.2: "un comprimido una vez al día"; solución (00160065): "10 ml (5 mg) de solución oral una vez al día"')),
        dosis('Rinitis alérgica y urticaria (niños de 1 a 5 años)', 'pediatrico', 'fija', 'mg', min=1.25, max=1.25, tomas=1, intervalo_h=24,
              texto='2,5 ml (1,25 mg) de solución oral una vez al día',
              presentaciones=['solucion-oral-0-5-mg-ml'],
              fuente=fu(DES_S, '4.2: "Niños de 1 a 5 años de edad: 2,5 ml (1,25 mg) de Aerius solución oral una vez al día"')),
        dosis('Rinitis alérgica y urticaria (niños de 6 a 11 años)', 'pediatrico', 'fija', 'mg', min=2.5, max=2.5, tomas=1, intervalo_h=24,
              texto='5 ml (2,5 mg) de solución oral una vez al día',
              presentaciones=['solucion-oral-0-5-mg-ml'],
              fuente=fu(DES_S, '4.2: "Niños de 6 a 11 años de edad: 5 ml (2,5 mg) de Aerius solución oral una vez al día"')),
        dosis('Lactantes de 6 a 11 meses', 'pediatrico', 'fija', 'mg', min=1, max=1, tomas=1, intervalo_h=24, estatus='off_label',
              condicion='La ficha técnica no lo ha establecido en menores de 1 año', texto='1 mg cada 24 h (jarabe)',
              presentaciones=['solucion-oral-0-5-mg-ml'],
              fuente=fu(P, '"Lactantes de 6 meses a 11 meses: 1 mg/24 h (jarabe)"; "No recomendado en niños menores de 1 año ( E: off-label )"')),
    ]
    disc = [
        discrepancia('Población pediátrica (menores de 1 año)',
                     [(DES_S, 'CIMA: no se ha establecido la seguridad y eficacia en niños menores de 1 año'),
                      (P, 'Pediamécum: lactantes de 6 a 11 meses, 1 mg/24 h (off-label)')],
                     POBLACION_SIN_CIFRA,
                     'Contradicción de población, no de cifra; en el resto de edades ambas fuentes coinciden.'),
    ]
    alertas = [
        'La mayoría de las rinitis en menores de 2 años son infecciosas y no hay datos que apoyen tratarlas con desloratadina (CIMA, 4.2).',
        'Contraindicado si hay hipersensibilidad a loratadina (CIMA, 4.3).',
    ]
    return ficha_oral(
        'desloratadina', 'Desloratadina', 'antihistaminico', presentaciones, dosis_, {
            'comida': 'indiferente',
            'texto': 'Vía oral, con o sin alimentos.',
            'fuente': fu(DES_C, '4.2 Forma de administración'),
        },
        comerciales=['Aerius'], discrepancias=disc,
        renal='CIMA (Aerius): en insuficiencia renal severa, usar con precaución. Pediamécum: 5 mg cada 48 horas (comprimidos) o 10 ml cada 48 horas (jarabe).',
        hepatico='Pediamécum: 5 mg cada 48 horas (comprimidos) o 10 ml cada 48 horas (jarabe). La ficha técnica no da ajuste hepático.',
        fuente_ajuste=fu(P, 'Insuficiencia renal o hepática (Pediamécum); precaución renal: CIMA 00160009, 4.4'),
        alertas=alertas,
    )


# ---------------------------------------------------------------- corticoides
def prednisona():
    P = _ped('prednisona')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(PRE, 'Prednisona Cinfa 10 mg comprimidos (la ficha no menciona ranura ni partición)')),
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='no', fuente=fu(ARSENAL, 'Grupo 03.03: Prednisona, Comprimido 5 mg')),
        pres('comprimido-20-mg', 'comprimido', mg=20, partible='no', fuente=fu(ARSENAL, 'Grupo 03.03: Prednisona, Comprimido 20 mg')),
        pres('suspension-4-mg-ml', 'suspension', mg_ml=4,
             fuente=fu(ARSENAL, 'Grupo 03.03: Prednisona, Suspensión oral 20 mg/5 mL (= 4 mg por 1 ml)')),
    ]
    dosis_ = [
        dosis('Asma bronquial (adultos)', 'adulto', 'fija', 'mg', base='dia', min=15, max=60, tomas=3,
              condicion='La dosis depende de la indicación y la gravedad; reducir progresivamente, no suspender bruscamente',
              texto='15-60 mg al día; como norma general repartidos en 3-4 tomas (en algunos casos dosis única por la mañana)',
              fuente=fu(PRE, '4.2.1: "Asma bronquial: de 15 mg a 60 mg al día"; forma de administración: "repartirse en 3 o 4 tomas"')),
        dosis('Dosis intermedias (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=1, tomas=3,
              condicion='Dosis altas: 2-3 mg/kg/día; mantenimiento: 0,25 mg/kg/día. En niños en crecimiento, preferir pauta alternante o intermitente',
              texto='1 mg/kg/día (dosis intermedias); dosis diaria repartida en 3-4 tomas',
              fuente=fu(PRE, '4.2.1 Dosificación en niños (dosis diarias): "Tratamiento con dosis intermedias: 1 mg prednisona/kg peso corporal"')),
        dosis('Asma: exacerbación aguda (niños <12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=1, max=2, tomas=2,
              intervalo_h=12, tope_dia=(60, 'mg'),
              texto='1-2 mg/kg/día divididos en 2 dosis; máximo 60 mg/día',
              fuente=fu(P, 'Asma, niños <12 años: "Exacerbaciones agudas: 1-2 mg/kg/día, divididos en 2 dosis (máximo: 60 mg/día)"')),
    ]
    alertas = [
        'La dosis depende de la indicación y de la gravedad; ver la fuente para cada enfermedad (CIMA da pautas de 5 a 300 mg/día según indicación).',
        'Tratamientos prolongados: no suspender bruscamente; reducir gradualmente según el esquema de la ficha técnica (CIMA, 4.2).',
        'En niños en fase de crecimiento, el tratamiento debería ser alternante o intermitente (CIMA, 4.2).',
        'Pediamécum agrega pautas de asma para ≥12 años (40-80 mg/día en exacerbaciones) y por edad; no se cargan.',
        'La dosis intermedia de 1 mg/kg/día no tiene tope pediátrico en la fuente; como referencia, la pauta de asma del adulto llega '
        'a 60 mg al día (CIMA 75649, «Asma bronquial: de 15 mg a 60 mg al día»).',
    ]
    return ficha_oral(
        'prednisona', 'Prednisona', 'corticoide', presentaciones, dosis_, {
            'comida': 'despues',
            'texto': 'Dosis diaria repartida en 3-4 tomas, preferentemente después de las comidas y al acostarse; en algunos casos, dosis única '
                     'por la mañana. Comprimidos enteros con suficiente líquido.',
            'fuente': fu(PRE, '4.2 Forma de administración'),
        },
        comerciales=['Prednisona Cinfa'],
        alertas=alertas,
    )


def dexametasona():
    P = _ped('dexametasona')
    presentaciones = [
        pres('comprimido-20-mg', 'comprimido', mg=20, partible='mitades',
             fuente=fu(DEX, 'Dexametasona Abdrug 20 mg: "Los comprimidos se pueden dividir en dosis iguales" (4.2)')),
        pres('comprimido-4-mg', 'comprimido', mg=4, partible='mitades',
             fuente=fu(DEX, '4.2: "se presenta en forma de comprimidos de 4 mg, 8 mg y 20 mg. Los comprimidos se pueden dividir en dosis iguales"')),
        pres('comprimido-8-mg', 'comprimido', mg=8, partible='mitades',
             fuente=fu(DEX, '4.2: "se presenta en forma de comprimidos de 4 mg, 8 mg y 20 mg. Los comprimidos se pueden dividir en dosis iguales"')),
    ]
    dosis_ = [
        dosis('Dosis habitual según la enfermedad (adultos)', 'adulto', 'fija', 'mg', base='dia', min=0.5, max=10, tomas=1,
              condicion='La dosis depende de la indicación; en situaciones graves pueden requerirse más de 10 mg/día',
              texto='0,5-10 mg al día, como única dosis por la mañana cuando no es posible el tratamiento en días alternos',
              fuente=fu(DEX, '4.2: "Dexametasona se da en dosis habituales de 0,5 a 10 mg al día"; "única dosis por la mañana"')),
        dosis('Crup (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=0.6, tomas=1, estatus='off_label',
              condicion='Dosis única; según la evolución puede continuarse con 0,15 mg/kg cada 6 h',
              texto='Dosis única de 0,6 mg/kg vía oral',
              fuente=fu(P, 'Niños <12 años: "Crou ( E : off-label ): dosis única de 0,6 mg/kg VO o IM"')),
    ]
    disc = [
        discrepancia('Forma de dosificar en niños',
                     [(DEX, 'CIMA: no da mg/kg; la dosis pediátrica se ajusta en función de la superficie corporal'),
                      (P, 'Pediamécum: dosis por indicación en mg/kg (crup, edema cerebral, edema de vía aérea, etc.)')],
                     'Se muestra la dosis oral de crup de Pediamécum, marcada como off-label',
                     'Diferencia de método (superficie corporal frente a mg/kg), no de cifra.'),
    ]
    alertas = [
        'La dosis depende de la indicación; ver la fuente (CIMA da pautas propias para emesis por quimioterapia, mieloma, púrpura, miositis y otras indicaciones).',
        'Dexametasona Abdrug es un medicamento de dosis alta: usar la menor dosis efectiva (CIMA, 4.2).',
        'Pediamécum: la pauta antiinflamatoria de 0,08-0,3 mg/kg/día es por vía IM o IV; no se carga como dosis oral.',
        'Tratamientos prolongados: reducir gradualmente; tras la terapia inicial, cambiar a prednisona/prednisolona (CIMA, 4.2).',
        'Evitar bebidas con alcohol o cafeína (CIMA, 4.2).',
        'Pediamécum no da dosis máxima para el crup (0,6 mg/kg en dosis única); la dosis habitual de adulto en CIMA es «de 0,5 a 10 mg al día»: '
        'con 70 kg el cálculo daría 42 mg.',
    ]
    return ficha_oral(
        'dexametasona', 'Dexametasona', 'corticoide', presentaciones, dosis_, {
            'comida': 'con_comida',
            'texto': 'Junto con o después de las comidas para minimizar la irritación gastrointestinal.',
            'fuente': fu(DEX, '4.2 Forma de administración'),
        },
        comerciales=['Dexametasona Abdrug'], discrepancias=disc,
        renal='Pacientes en hemodiálisis activa: puede aumentar el aclaramiento por diálisis y requerir ajuste de la dosis.',
        hepatico='Insuficiencia hepática grave: puede ser necesario ajustar la dosis (efectos potenciados por metabolismo más lento e hipoalbuminemia).',
        fuente_ajuste=fu(DEX, '4.2 Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def fichas():
    return {
        'ibuprofeno': ibuprofeno(),
        'diclofenaco': diclofenaco(),
        'ketorolaco': ketorolaco(),
        'meloxicam': meloxicam(),
        'celecoxib': celecoxib(),
        'metamizol': metamizol(),
        'tramadol': tramadol(),
        'paracetamol-tramadol': paracetamol_tramadol(),
        'morfina': morfina(),
        'alopurinol': alopurinol(),
        'ciclobenzaprina': ciclobenzaprina(),
        'loratadina': loratadina(),
        'desloratadina': desloratadina(),
        'prednisona': prednisona(),
        'dexametasona': dexametasona(),
    }
