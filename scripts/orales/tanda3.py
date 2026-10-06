"""Orales, tanda 3: neurología, psiquiatría y vitaminas (20 fichas).

Cada cifra sale de datos/crudos/orales/ (fichas CIMA, Pediamécum y arsenal de APS de Atacama);
la tabla «cifra → archivo:línea» se detalla en el reporte de la Tarea 14.

Convenciones de esta tanda (mismas que 12a/12b/13):
- Rangos de dosis de la fuente → `min`/`max`; topes y frecuencias con rango → extremo conservador, dicho en `condicion`.
- Dosis diaria (`base='dia'`) con «1 o 2 tomas» → se cargan 2 tomas (toma más pequeña). Si la fuente da la dosis
  diaria sin decir cuántas tomas, se carga una toma diaria y la `condicion` lo dice.
- `topeDiario` de adulto solo cuando la fuente lo declara como máximo (nunca toma × tomas).
- En fármacos con dosificación en hierro elemental (`sulfato-ferroso`), las presentaciones y dosis declaran
  el valor de hierro elemental en sus cantidades.
"""
from .comun import (ARSENAL, discrepancia, dosis, ficha_oral, fu, fuente_arsenal, fuente_cima, fuente_externa,
                    fuente_pediamecum_oral, pres)


def _ped(k, slug=None, anio=None):
    return fuente_pediamecum_oral(k, slug=slug, anio=anio)['id']


# ---------------------------------------------------------------- referencias de fuentes
CBZ = 'CIMA-CARBAMAZEPINA'  # Carbamazepina Normon 200 mg
VAL_C = 'CIMA-ACIDO-VALPROICO-48827'  # Depakine 200 mg comprimidos gastrorresistentes
VAL_S = 'CIMA-ACIDO-VALPROICO-48828'  # Depakine 200 mg/ml solución oral
CLO_C = 'CIMA-CLONAZEPAM-79769'  # Clonazepam Biomed 2 mg comprimidos
CLO_G = 'CIMA-CLONAZEPAM-52333'  # Rivotril 2,5 mg/ml gotas orales en solución
FEN = 'CIMA-FENOBARBITAL'  # Luminal 100 mg comprimidos
LAM = 'CIMA-LAMOTRIGINA'  # Crisomet 100 mg comprimidos dispersables/masticables
LEV_C = 'CIMA-LEVETIRACETAM-75005'  # Levetiracetam Cinfa 1000 mg comprimidos
LEV_S = 'CIMA-LEVETIRACETAM-76440'  # Levetiracetam Cinfa 100 mg/ml solución oral
PHT = 'CIMA-FENITOINA'  # Epanutin 100 mg cápsulas duras
SER_C = 'CIMA-SERTRALINA-59718'  # Besitran 100 mg comprimidos
SER_S = 'CIMA-SERTRALINA-63477'  # Besitran 20 mg/ml concentrado para solución oral
FLX_C = 'CIMA-FLUOXETINA-63499'  # Fluoxetina Cinfa 20 mg cápsulas
FLX_S = 'CIMA-FLUOXETINA-62427'  # Fluoxetina Normon 20 mg/5 ml solución oral
ESC_C = 'CIMA-ESCITALOPRAM-71430'  # Escitalopram Cinfa 10 mg comprimidos
ESC_G = 'CIMA-ESCITALOPRAM-76398'  # Escitalopram Cinfa 20 mg/ml gotas
AMI = 'CIMA-AMITRIPTILINA'  # Tryptizol 10 mg comprimidos
MIR = 'CIMA-MIRTAZAPINA'  # Mirtazapina Cinfa 15 mg comprimidos
VEN_37 = 'CIMA-VENLAFAXINA-60666'  # Dobupal 37,5 mg comprimidos
VEN_50 = 'CIMA-VENLAFAXINA-60667'  # Dobupal 50 mg comprimidos
QUE_100 = 'CIMA-QUETIAPINA-70169'  # Qudix 100 mg comprimidos
QUE_200 = 'CIMA-QUETIAPINA-70170'  # Qudix 200 mg comprimidos
HAL_C = 'CIMA-HALOPERIDOL-58343'  # Haloperidol Esteve 10 mg comprimidos
HAL_S = 'CIMA-HALOPERIDOL-58355'  # Haloperidol Esteve 2 mg/ml solución oral
RIS_C = 'CIMA-RISPERIDONA-60336'  # Risperdal 1 mg comprimidos
RIS_S = 'CIMA-RISPERIDONA-62096'  # Risperdal 1 mg/ml solución oral
ZOP = 'CIMA-ZOPICLONA'  # Limovan 7,5 mg comprimidos
DZP_C = 'CIMA-DIAZEPAM-80699'  # Diazepam Cinfa 10 mg comprimidos
DZP_S = 'CIMA-DIAZEPAM-41598'  # Diazepan Prodes 2 mg/ml solución oral
FOL = 'CIMA-ACIDO-FOLICO'  # Acfol 5 mg comprimidos
FER_T = 'CIMA-SULFATO-FERROSO-52994'  # Tardyferon 80 mg comprimidos de liberación prolongada
FER_F = 'CIMA-SULFATO-FERROSO-48330'  # Fero-Gradumet 105 mg comprimidos de liberación prolongada


def fuentes():
    return [
        # §6 Neurología
        fuente_cima('carbamazepina', '62620', 'Carbamazepina Normon 200 mg comprimidos EFG'),
        fuente_cima('acido-valproico', '48827', 'Depakine 200 mg comprimidos gastrorresistentes', varios=True),
        fuente_cima('acido-valproico', '48828', 'Depakine 200 mg/ml solución oral', varios=True),
        fuente_pediamecum_oral('acido-valproico', 'Ácido valproico', anio=2021),
        fuente_cima('clonazepam', '79769', 'Clonazepam Biomed 2 mg comprimidos EFG', varios=True),
        fuente_cima('clonazepam', '52333', 'Rivotril 2,5 mg/ml gotas orales en solución', varios=True),
        fuente_pediamecum_oral('clonazepam', 'Clonazepam', anio=2020),
        fuente_cima('fenobarbital', '35052', 'Luminal 100 mg comprimidos'),
        fuente_pediamecum_oral('fenobarbital', 'Fenobarbital', anio=2022),
        fuente_cima('lamotrigina', '64462', 'Crisomet 100 mg comprimidos masticables/dispersables'),
        fuente_pediamecum_oral('lamotrigina', 'Lamotrigina', anio=2020),
        fuente_cima('levetiracetam', '75005', 'Levetiracetam Cinfa 1000 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('levetiracetam', '76440', 'Levetiracetam Cinfa 100 mg/ml solución oral EFG', varios=True),
        fuente_pediamecum_oral('levetiracetam', 'Levetiracetam', anio=2020),
        fuente_cima('fenitoina', '45695', 'Epanutin 100 mg cápsulas duras'),
        fuente_pediamecum_oral('fenitoina', 'Fenitoína', anio=2020, slug='fenitoina-difenilhidantoina'),

        # §6 Psiquiatría
        fuente_cima('sertralina', '59718', 'Besitran 100 mg comprimidos recubiertos con película', varios=True),
        fuente_cima('sertralina', '63477', 'Besitran 20 mg/ml concentrado para solución oral', varios=True),
        fuente_cima('fluoxetina', '63499', 'Fluoxetina Cinfa 20 mg cápsulas duras EFG', varios=True),
        fuente_cima('fluoxetina', '62427', 'Fluoxetina Normon 20 mg/5 ml solución oral EFG', varios=True),
        fuente_pediamecum_oral('fluoxetina', 'Fluoxetina', anio=2020),
        fuente_cima('escitalopram', '71430', 'Escitalopram Cinfa 10 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('escitalopram', '76398', 'Escitalopram Cinfa 20 mg/ml gotas orales en solución EFG', varios=True),
        fuente_cima('amitriptilina', '51064', 'Tryptizol 10 mg comprimidos recubiertos con película'),
        fuente_pediamecum_oral('amitriptilina', 'Amitriptilina', anio=2021),
        fuente_cima('mirtazapina', '86890', 'Mirtazapina Cinfa 15 mg comprimidos recubiertos con película EFG'),
        fuente_cima('venlafaxina', '60666', 'Dobupal 37,5 mg comprimidos', varios=True),
        fuente_cima('venlafaxina', '60667', 'Dobupal 50 mg comprimidos', varios=True),
        fuente_pediamecum_oral('venlafaxina', 'Venlafaxina', anio=2021),
        fuente_cima('quetiapina', '70169', 'Qudix 100 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('quetiapina', '70170', 'Qudix 200 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('haloperidol', '58343', 'Haloperidol Esteve 10 mg comprimidos', varios=True),
        fuente_cima('haloperidol', '58355', 'Haloperidol Esteve 2 mg/ml solución oral', varios=True),
        fuente_pediamecum_oral('haloperidol', 'Haloperidol', anio=2020),
        fuente_cima('risperidona', '60336', 'Risperdal 1 mg comprimidos recubiertos con película', varios=True),
        fuente_cima('risperidona', '62096', 'Risperdal 1 mg/ml solución oral', varios=True),
        fuente_pediamecum_oral('risperidona', 'Risperidona', anio=2020),
        fuente_cima('zopiclona', '58538', 'Limován 7,5 mg comprimidos recubiertos con película'),
        fuente_cima('diazepam', '80699', 'Diazepam Cinfa 10 mg comprimidos EFG', varios=True),
        fuente_cima('diazepam', '41598', 'Diazepan Prodes 2 mg/ml solución oral', varios=True),
        fuente_pediamecum_oral('diazepam', 'Diazepam', anio=2020),

        # §7 Vitaminas y minerales
        fuente_cima('acido-folico', '11265', 'Acfol 5 mg comprimidos'),
        fuente_pediamecum_oral('acido-folico', 'Ácido fólico', anio=2022),
        fuente_cima('sulfato-ferroso', '52994', 'Tardyferon 80 mg comprimidos de liberación prolongada', varios=True),
        fuente_cima('sulfato-ferroso', '48330', 'Fero-Gradumet 105 mg comprimidos de liberación prolongada', varios=True),
        fuente_pediamecum_oral('sulfato-ferroso', 'Sulfato ferroso', anio=2020, slug='sulfato-ferroso-y-glicina-sulfato-ferroso'),

        fuente_arsenal(),
    ]


# ================================================================ §6 Neurología
def carbamazepina():
    presentaciones = [
        pres('comprimido-200-mg', 'comprimido', mg=200, partible='mitades',
             fuente=fu(CBZ, 'Carbamazepina Normon 200 mg comprimidos (ranurados que permiten división en mitades); '
                            'el arsenal de APS lista comprimido 200 mg')),
        pres('comprimido-retard-200-mg', 'comprimido', mg=200, partible='no', retard=True,
             fuente=fu(ARSENAL, 'Grupo 05.01: Carbamazepina, Comprimido de liberación prolongada 200 mg y 400 mg')),
        pres('comprimido-retard-400-mg', 'comprimido', mg=400, partible='no', retard=True,
             fuente=fu(ARSENAL, 'Grupo 05.01: Carbamazepina, Comprimido de liberación prolongada 400 mg')),
    ]
    dosis_ = [
        dosis('Epilepsia (adultos)', 'adulto', 'fija', 'mg', min=100, max=200, tomas=2, intervalo_h=12,
              tope_dia=(1600, 'mg'),
              condicion='Inicialmente 100-200 mg 1 o 2 veces al día; aumentar gradualmente hasta respuesta óptima '
                        '(habitual 400 mg 2-3 veces al día; en algunos pacientes hasta 1600 mg al día)',
              texto='Inicial 100-200 mg 1-2 veces/día; mantenimiento habitual 400 mg 2-3 veces/día; máximo 1600 mg/día',
              presentaciones=['comprimido-200-mg'],
              fuente=fu(CBZ, '4.2.1 Adultos: "Inicialmente 100-200 mg, una o dos veces al día ... habitual 400 mg dos o tres veces al día. '
                             'En algunos pacientes puede ser necesaria una dosis de 1600 mg al día"')),
        dosis('Epilepsia: dosis inicial (niños <4 años)', 'pediatrico', 'fija', 'mg', min=20, max=60, tomas=2,
              intervalo_h=12,
              condicion='Dosis inicial de 20-60 mg/día aumentándola de 20-60 mg cada dos días',
              texto='20-60 mg/día en dosis divididas, incrementando cada dos días',
              fuente=fu(CBZ, '4.2.1 Población pediátrica: "Para niños menores de 4 años se recomienda una dosis inicial de 20-60 mg/día '
                             'aumentándola de 20-60 mg cada dos días"')),
        dosis('Epilepsia: dosis inicial (niños >4 años)', 'pediatrico', 'fija', 'mg', min=100, max=100, tomas=2,
              intervalo_h=12,
              condicion='Iniciar con 100 mg/día incrementando en 100 mg a intervalos semanales',
              texto='100 mg/día en dosis divididas, incrementando 100 mg semanalmente',
              presentaciones=['comprimido-200-mg'],
              fuente=fu(CBZ, '4.2.1 Población pediátrica: "Para niños mayores de 4 años, el tratamiento puede iniciarse con 100 mg/día '
                             'incrementándolo en 100 mg a intervalos semanales"')),
        dosis('Epilepsia: mantenimiento (niños y adolescentes)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=10, max=20, tomas=2, intervalo_h=12, tope_dia=(1000, 'mg'),
              condicion='10-20 mg/kg/día divididos en 2 o 3 tomas. Topes máximos: hasta 6 años 35 mg/kg/día; '
                        '6-15 años 1000 mg/día; mayores de 15 años 1200 mg/día',
              texto='10-20 mg/kg/día en 2-3 tomas diarias (máx. 1000 mg/día en 6-15 años; 35 mg/kg/día en <6 años)',
              fuente=fu(CBZ, '4.2.1: "Dosis de mantenimiento: Se administrarán dosis de 10-20 mg/kg de peso al día, en dosis divididas ... '
                             'Hasta los 6 años: 35 mg/Kg/día, 6-15 años: 1000 mg/día, Mayores de 15 años: 1200 mg/día"')),
        dosis('Neuralgia del trigémino (adultos)', 'adulto', 'fija', 'mg', min=200, max=400, tomas=2, intervalo_h=12,
              tope_dia=(1200, 'mg'),
              condicion='Inicial 200-400 mg diarios, aumentar lentamente hasta suprimir el dolor (normalmente 200 mg 3 o 4 veces/día); '
                        'máximo 1200 mg/día. Ancianos: inicio 100 mg 2 veces al día',
              texto='Inicial 200-400 mg/día; mantenimiento habitual 200 mg 3-4 veces/día; máximo 1200 mg/día',
              presentaciones=['comprimido-200-mg'],
              fuente=fu(CBZ, '4.2.1 Neuralgia del trigémino: "La dosis inicial de 200-400 mg diarios se aumentará lentamente ... '
                             'La dosis máxima recomendada es de 1200 mg/día"')),
    ]
    return ficha_oral(
        'carbamazepina', 'Carbamazepina', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Los comprimidos pueden ingerirse durante, después o entre las comidas con un poco de líquido. '
                                 'Las presentaciones de liberación prolongada deben tragarse enteras sin masticar.',
                        'fuente': fu(CBZ, '4.2 Forma de administración: "Los comprimidos pueden ingerirse durante, después o entre las '
                                         'comidas con un poco de líquido"')},
        ajusteRenalHepatico={'renal': 'No se dispone de datos de carbamazepina en pacientes con insuficiencia renal.',
                             'hepatico': 'No se dispone de datos de carbamazepina en pacientes con insuficiencia hepática.',
                             'fuente': fu(CBZ, '4.2 Poblaciones especiales: "No se dispone de datos de carbamazepina en pacientes con '
                                              'insuficiencia hepática o renal"')},
        alertas=['Ficha de fuente única: se apoya exclusivamente en CIMA (España); Pediamécum no dispone de monografía para carbamazepina.',
                 'Para niños pequeños que requieran dosis iniciales de 20-60 mg se requiere formulación líquida o fraccionamiento específico '
                 'no cubierto por comprimidos de 200 mg.'],
        comerciales=['Tegretol', 'Carbamazepina Normon'],
    )


def acido_valproico():
    P = _ped('acido-valproico', anio=2021)
    presentaciones = [
        pres('comprimido-gastrorresistente-200-mg', 'comprimido', mg=200, partible='no',
             fuente=fu(VAL_C, 'Depakine 200 mg comprimidos gastrorresistentes (tragar enteros sin masticar ni triturar); '
                              'el arsenal de APS lista comprimido 200 mg')),
        pres('solucion-oral-200-mg-ml', 'jarabe', mg_ml=200,
             fuente=fu(VAL_S, 'Depakine 200 mg/ml solución oral (frasco con jeringa dosificadora)')),
        pres('solucion-gotas-375-mg-ml', 'gotas', mg_ml=375, gotas_por_ml=25,
             fuente=fu(ARSENAL, 'Grupo 05.01: Ácido Valproico, Solución para gotas orales 375 mg/mL (1 gota ≈ 15 mg)')),
        pres('solucion-oral-50-mg-ml', 'jarabe', mg_ml=50,
             fuente=fu(ARSENAL, 'Grupo 05.01: Ácido Valproico, Solución oral 250 mg/5 mL (50 mg/mL)')),
    ]
    dosis_ = [
        dosis('Epilepsia: mantenimiento (adolescentes ≥12 años y adultos)', 'adulto', 'por_peso', 'mg/kg', base='dia',
              min=20, max=30, tomas=2, intervalo_h=12,
              condicion='20-30 mg/kg/día en 1 o 2 tomas, preferentemente con comidas. Mayores de 65 años: 15-20 mg/kg/día',
              texto='20-30 mg/kg/día en 1-2 tomas diarias con comidas',
              fuente=fu(VAL_C, '4.2 Dosis media: "Adolescentes (≥12 años) y adultos (≥18 años): 20-30 mg/kg. '
                               'Pacientes de edad avanzada (≥65 años): 15-20 mg/kg"')),
        dosis('Epilepsia: mantenimiento (lactantes y niños de 28 días a 11 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=30, max=30, tomas=2, intervalo_h=12,
              condicion='Dosis media de mantenimiento: 30 mg/kg/día en 1 o 2 tomas. En niños <11 años es preferible la solución oral. '
                        'Pediamécum cita mantenimiento de 30-60 mg/kg/día',
              texto='30 mg/kg/día en 1-2 tomas diarias (CIMA); Pediamécum indica mantenimiento habitual 30-60 mg/kg/día',
              fuente=fu(VAL_C, '4.2 Dosis media: "Lactantes y niños (28 días a 11 años): 30 mg/kg"')),
        dosis('Epilepsia: inicio de titulación oral (niños y adolescentes)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=10, max=15, tomas=2, intervalo_h=12,
              condicion='10-15 mg/kg/día en 2 o 3 tomas con incrementos semanales de 5-10 mg/kg/día hasta control',
              texto='10-15 mg/kg/día en 2-3 tomas, con incrementos semanales de 5-10 mg/kg/día',
              fuente=fu(P, 'Vía oral: "10-15 mg/kg/día administrado en dos o tres tomas con incrementos semanales de 5-10 mg/kg/día hasta control"')),
    ]
    discrepancias_ = [
        discrepancia('Dosis de mantenimiento pediátrica',
                     [(VAL_C, '30 mg/kg/día'), (P, '30-60 mg/kg/día')],
                     '30 mg/kg/día',
                     'CIMA fija 30 mg/kg/día para lactantes y niños (28 días a 11 años); Pediamécum amplía el rango a 30-60 mg/kg/día '
                     'señalando que niños con inductores enzimáticos pueden requerir dosis mayores. Se muestra la cifra más conservadora.')
    ]
    return ficha_oral(
        'acido-valproico', 'Ácido valproico', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'con_comida',
                        'texto': 'Los comprimidos se deben tragar enteros sin masticar ni triturar, preferentemente durante las comidas. '
                                 'La solución oral se puede tomar en medio vaso de agua sin gas.',
                        'noTriturar': True,
                        'fuente': fu(VAL_C, '4.2 Forma de administración: "Los comprimidos se deben tragar enteros sin masticar ni triturar '
                                           'con ayuda de un poco de agua en 1 ó 2 tomas, preferentemente en el curso de las comidas"')},
        ajusteRenalHepatico={'renal': 'En pacientes con insuficiencia renal debe tenerse en cuenta la elevación de valproico libre en plasma '
                                      'y reducir la dosis adecuadamente.',
                             'hepatico': 'Contraindicado en enfermedad o insuficiencia hepática grave (riesgo de hepatotoxicidad mortal).',
                             'fuente': fu(VAL_C, '4.2 Insuficiencia renal y 4.3 Contraindicaciones')},
        discrepancias=discrepancias_,
        alertas=['Teratogénico mayor: contraindicado en mujeres con capacidad de gestación salvo estricto cumplimiento del Plan de Prevención de Embarazos.',
                 'En niños menores de 11 años se recomienda la solución oral o gotas frente al comprimido gastrorresistente.'],
        comerciales=['Depakine', 'Valcote'],
    )


def clonazepam():
    P = _ped('clonazepam', anio=2020)
    presentaciones = [
        pres('comprimido-0-5-mg', 'comprimido', mg=0.5, partible='mitades',
             fuente=fu(CLO_G, 'Rivotril 0,5 mg comprimidos (divisibles en dos mitades iguales); el arsenal de APS lista 0,5 mg')),
        pres('comprimido-2-mg', 'comprimido', mg=2, partible='cuartos',
             fuente=fu(CLO_C, 'Clonazepam Biomed 2 mg comprimidos (divisibles en cuatro partes iguales de 0,5 mg); el arsenal lista 2 mg')),
        pres('gotas-2-5-mg-ml', 'gotas', mg_ml=2.5, gotas_por_ml=25,
             fuente=fu(CLO_G, 'Rivotril 2,5 mg/ml gotas orales en solución (1 ml = 25 gotas = 2,5 mg; 1 gota = 0,1 mg)')),
    ]
    dosis_ = [
        dosis('Epilepsia: dosis inicial (adultos)', 'adulto', 'fija', 'mg', max=1.5, tomas=3, intervalo_h=8,
              tope_dia=(20, 'mg'),
              condicion='La dosis inicial no debe superar 1,5 mg/día divididos en 3 tomas (0,5 mg c/8 h). Incrementar 0,5 mg cada 72 horas',
              texto='Inicial ≤1,5 mg/día en 3 tomas; incrementar 0,5 mg c/72 h; mantenimiento habitual 3-6 mg/día; máximo 20 mg/día',
              fuente=fu(CLO_C, '4.2 Adultos: "La dosis inicial para los adultos no debe superar los 1,5 mg/día, dividido en 3 tomas ... '
                               'dosis de mantenimiento de 3-6 mg diarios. La dosis terapéutica máxima ... es de 20 mg diarios"')),
        dosis('Epilepsia: inicio (lactantes y niños ≤10 años o ≤30 kg)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=0.01, max=0.03, tomas=2, intervalo_h=12,
              condicion='0,01-0,03 mg/kg/día en 2 o 3 tomas. Incrementar 0,25-0,5 mg cada 72 h hasta mantenimiento aproximado de 0,1-0,2 mg/kg/día. '
                        'Para lactantes usar formulación en gotas',
              texto='0,01-0,03 mg/kg/día en 2-3 tomas; mantenimiento 0,1-0,2 mg/kg/día (máximo 0,2 mg/kg/día)',
              presentaciones=['gotas-2-5-mg-ml'],
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: dosis inicial 0,01-0,03 mg/kg/día; '
                           'mantenimiento aproximado 0,1 mg/kg/día; máximo 0,2 mg/kg/día')),
        dosis('Epilepsia: inicio (niños y adolescentes de 10 a 16 años)', 'pediatrico', 'fija', 'mg', min=1, max=1.5, tomas=2,
              intervalo_h=12,
              condicion='Inicial 1-1,5 mg/día en 2 o 3 tomas; incrementar 0,25-0,5 mg cada 72 h hasta mantenimiento habitual de 3-6 mg/día',
              texto='Inicial 1-1,5 mg/día en 2-3 tomas; mantenimiento 3-6 mg/día',
              fuente=fu(CLO_C, '4.2 Niños y adolescentes de 10-16 años: "La dosis inicial es de 1-1,5 mg/día, divididos en 2 o 3 tomas ... '
                               'mantenimiento individual (por lo general, de 3-6 mg diarios)"')),
    ]
    discrepancias_ = [
        discrepancia('Tope pediátrico en adolescentes 10-16 años',
                     [(CLO_C, 'Mantenimiento 3-6 mg/día (máximo no especificado en niños)'),
                      (P, 'Dosis máxima 20 mg/día')],
                     'Mantenimiento 3-6 mg/día',
                     'Pediamécum indica dosis máxima 20 mg/día para 10-16 años, cifra idéntica al tope de adultos; '
                     'se trata como advertencia clínica no confirmada para no inducir sobredosis en adolescentes.')
    ]
    return ficha_oral(
        'clonazepam', 'Clonazepam', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Las gotas se deben mezclar con agua, té o zumo de frutas y administrarse con cuchara, nunca directamente '
                                 'del frasco a la boca.',
                        'fuente': fu(CLO_G, '4.2 Pauta de administración y Pediamécum')},
        ajusteRenalHepatico={'renal': 'No se precisa ajuste posológico en insuficiencia renal de acuerdo con datos farmacocinéticos.',
                             'hepatico': 'No hay datos disponibles sobre la influencia de insuficiencia hepática; usar con precaución.',
                             'fuente': fu(CLO_C, '4.2 Pacientes con alteraciones en la función renal o hepática')},
        alto_riesgo=True,
        discrepancias=discrepancias_,
        alertas=['Medicamento de alto riesgo (benzodiacepina): riesgo de dependencia, tolerancia y depresión respiratoria.',
                 '1 gota de solución al 2,5 mg/ml equivale exactamente a 0,1 mg de clonazepam (25 gotas/ml).'],
        comerciales=['Rivotril', 'Clonazepam Biomed'],
    )


def fenobarbital():
    P = _ped('fenobarbital', anio=2022)
    presentaciones = [
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='mitades',
             fuente=fu(FEN, 'Luminal 100 mg comprimidos (ranurados que permiten división en mitades); el arsenal de APS lista 100 mg')),
        pres('comprimido-15-mg', 'comprimido', mg=15, partible='no',
             fuente=fu(ARSENAL, 'Grupo 05.01: Fenobarbital, Comprimido 15 mg y 100 mg')),
    ]
    dosis_ = [
        dosis('Epilepsia (adultos)', 'adulto', 'fija', 'mg', min=50, max=100, tomas=2, intervalo_h=12,
              tope_dia=(200, 'mg'),
              condicion='Inicio 50-100 mg/día en 2 dosis. Mantenimiento 50-200 mg/día (CIMA indica hasta 250 mg/día; Pediamécum máx. 200 mg/día)',
              texto='Inicio 50-100 mg/día en 2 tomas; mantenimiento 50-200 mg/día (máximo 200 mg/día según Pediamécum; CIMA hasta 250 mg/día)',
              fuente=fu(FEN, '4.2 Adultos: "dosis de inicio recomendada es de 50 - 100 mg al día ... dividida en 2 dosis diarias. '
                             'La dosis de mantenimiento recomendada es de 50-250 mg al día" y Pediamécum: "Dosis máxima adultos: 50-200 mg/día"')),
        dosis('Epilepsia (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=3, max=5, tomas=2,
              intervalo_h=12,
              condicion='Inicio y mantenimiento de 3 a 5 mg/kg de peso corporal al día, en 1 o 2 tomas diarias. '
                        'Pediamécum indica lactantes 5-8 mg/kg/día y neonatos 2-5 mg/kg/día',
              texto='3-5 mg/kg/día en 1-2 tomas diarias',
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: dosis de inicio y mantenimiento de 3 a 5 mg/kg de peso corporal al día en 1 o 2 tomas')),
    ]
    discrepancias_ = [
        discrepancia('Dosis máxima en adultos',
                     [(FEN, '250 mg/día: dosis máxima de mantenimiento recomendada (CIMA)'),
                      (P, '200 mg/día: dosis máxima en adultos (Pediamécum)')],
                     '200 mg/día',
                     'Pediamécum fija como dosis máxima en adultos 200 mg/día, mientras CIMA sitúa el mantenimiento hasta 250 mg/día. '
                     'Se muestra el tope más conservador (200 mg/día).')
    ]
    return ficha_oral(
        'fenobarbital', 'Fenobarbital', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Administrar preferentemente a la misma hora cada día, tragando los comprimidos con agua.',
                        'fuente': fu(FEN, '4.2 Posología y forma de administración')},
        ajusteRenalHepatico={'renal': 'Aumentar intervalo entre dosis. Con filtración glomerular <10 ml/min se recomienda reducción del 50 %.',
                             'hepatico': 'Reducir dosis por riesgo de precipitar encefalopatía hepática.',
                             'fuente': fu(P, 'Insuficiencia renal y hepática (Pediamécum) y CIMA 4.2')},
        alto_riesgo=True,
        discrepancias=discrepancias_,
        alertas=['Medicamento de alto riesgo (barbitúrico): inductor enzimático potente, riesgo de sedación profunda, dependencia y tolerancia.',
                 'Monitorear niveles plasmáticos: rango terapéutico habitual 15-40 mcg/ml.'],
        comerciales=['Luminal', 'Fenobarbital'],
    )


def lamotrigina():
    P = _ped('lamotrigina', anio=2020)
    presentaciones = [
        pres('comprimido-masticable-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(LAM, 'Crisomet 100 mg comprimidos masticables/dispersables; el arsenal de APS lista comprimido 100 mg')),
        pres('comprimido-masticable-25-mg', 'comprimido', mg=25, partible='no',
             fuente=fu(ARSENAL, 'Grupo 05.01: Lamotrigina, Comprimido bucodispersable/masticable 25 mg')),
        pres('comprimido-masticable-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(ARSENAL, 'Grupo 05.01: Lamotrigina, Comprimido 50 mg')),
    ]
    dosis_ = [
        dosis('Epilepsia: monoterapia inicial semanas 1 y 2 (adultos y adolescentes ≥13 años)', 'adulto', 'fija', 'mg',
              min=25, max=25, tomas=1, intervalo_h=24,
              condicion='Semanas 1 y 2: 25 mg una vez al día. Semanas 3 y 4: 50 mg una vez al día. '
                        'Mantenimiento habitual: 100-200 mg/día en 1 o 2 tomas (hasta 500 mg/día)',
              texto='Semanas 1+2: 25 mg/día; semanas 3+4: 50 mg/día; mantenimiento 100-200 mg/día (máx. 500 mg/día)',
              presentaciones=['comprimido-masticable-25-mg'],
              fuente=fu(LAM, 'Tabla 1 Adultos y adolescentes de 13 años y en adelante: Monoterapia: '
                             '"Semanas 1 + 2: 25 mg/día; Semanas 3 + 4: 50 mg/día; Mantenimiento habitual: 100-200 mg/día"')),
        dosis('Epilepsia: monoterapia crisis de ausencia (niños de 2 a 12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=0.3, max=0.3, tomas=1, intervalo_h=24, tope_dia=(200, 'mg'),
              condicion='Semanas 1 y 2: 0,3 mg/kg/día en 1 o 2 tomas. Semanas 3 y 4: 0,6 mg/kg/día. '
                        'Mantenimiento habitual: 1-15 mg/kg/día en 1 o 2 tomas (máximo 200 mg/día)',
              texto='Semanas 1+2: 0,3 mg/kg/día; semanas 3+4: 0,6 mg/kg/día; mantenimiento 1-15 mg/kg/día (máx. 200 mg/día)',
              fuente=fu(P, 'Tabla 2 Niños 2-12 años: monoterapia en crisis de ausencia típica: '
                           'semanas 1+2: 0,3 mg/kg/día; semanas 3+4: 0,6 mg/kg/día; mantenimiento: 1-15 mg/kg/día (máximo 200 mg/día) (Pediamécum y CIMA)')),
        dosis('Epilepsia: terapia complementaria con valproato (niños de 2 a 12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=0.15, max=0.15, tomas=1, intervalo_h=24, tope_dia=(200, 'mg'),
              condicion='Valproato inhibe la glucuronidación de lamotrigina: semanas 1 y 2: 0,15 mg/kg/día; '
                        'semanas 3 y 4: 0,3 mg/kg/día; mantenimiento 1-5 mg/kg/día (máximo 200 mg/día)',
              texto='Con valproato: semanas 1+2: 0,15 mg/kg/día; semanas 3+4: 0,3 mg/kg/día; mantenimiento 1-5 mg/kg/día (máx. 200 mg/día)',
              fuente=fu(LAM, 'Tabla 2 Terapia complementaria con valproato: "Semanas 1 + 2: 0,15 mg/kg/día ... '
                             'Mantenimiento habitual: 1-5 mg/kg/día ... máxima de 200 mg/día"')),
    ]
    return ficha_oral(
        'lamotrigina', 'Lamotrigina', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Los comprimidos masticables/dispersables se pueden masticar, disolver en un pequeño volumen de agua '
                                 '(al menos suficiente para cubrir el comprimido) o tragarse enteros con agua. '
                                 'Si la dosis calculada no equivale a comprimidos enteros, redondear hacia abajo.',
                        'fuente': fu(LAM, '4.2 Forma de administración y posología general')},
        ajusteRenalHepatico={'renal': 'Usar con precaución; la acumulación del metabolito glucurónido es esperable en insuficiencia renal terminal.',
                             'hepatico': 'Reducir las dosis inicial, de escalada y de mantenimiento aproximadamente en un 50 % en insuficiencia '
                                         'moderada (Child-Pugh B) y en un 75 % en insuficiencia grave (Child-Pugh C).',
                             'fuente': fu(LAM, '4.2 Insuficiencia hepática e Insuficiencia renal')},
        alertas=['Riesgo de erupción cutánea grave (síndrome de Stevens-Johnson / necrólisis epidérmica tóxica): '
                 'respetar estrictamente la pauta lenta de escalada. Suspender al primer signo de exantema.',
                 'Si se interrumpe el tratamiento durante más de 5 semividas, reiniciar la escalada desde la dosis inicial.'],
        comerciales=['Crisomet', 'Lamictal'],
    )


def levetiracetam():
    P = _ped('levetiracetam', anio=2020)
    presentaciones = [
        pres('comprimido-1000-mg', 'comprimido', mg=1000, partible='mitades',
             fuente=fu(LEV_C, 'Levetiracetam Cinfa 1000 mg comprimidos (ranurados en mitades); el arsenal de APS lista 1000 mg')),
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='mitades',
             fuente=fu(ARSENAL, 'Grupo 05.01: Levetiracetam, Comprimido 500 mg')),
        pres('solucion-oral-100-mg-ml', 'jarabe', mg_ml=100,
             fuente=fu(LEV_S, 'Levetiracetam Cinfa 100 mg/ml solución oral; el arsenal de APS lista solución oral 100 mg/mL')),
    ]
    dosis_ = [
        dosis('Epilepsia: monoterapia y terapia complementaria (adultos y adolescentes ≥50 kg)', 'adulto', 'fija', 'mg',
              min=250, max=500, tomas=2, intervalo_h=12, tope_dia=(3000, 'mg'),
              condicion='Inicio habitual 500 mg 2 veces al día (o 250 mg c/12 h si se prefiere). '
                        'Aumentar de a 250-500 mg c/12 h cada 2-4 semanas hasta máximo 1500 mg 2 veces al día (3000 mg/día)',
              texto='Inicial 250-500 mg c/12 h; titular cada 2-4 semanas hasta 1500 mg c/12 h (máximo 3000 mg/día)',
              fuente=fu(LEV_C, '4.2 Adultos (≥18 años) y adolescentes ≥50 kg: "La dosis terapéutica inicial es de 500 mg dos veces al día ... '
                               'se puede incrementar hasta 1.500 mg dos veces al día"')),
        dosis('Epilepsia: politerapia (lactantes ≥6 meses, niños y adolescentes <50 kg)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=20, max=20, tomas=2, intervalo_h=12, tope_dia=(3000, 'mg'),
              condicion='Dosis inicial 10 mg/kg 2 veces al día (20 mg/kg/día). Incrementar en 10 mg/kg 2 veces al día cada 2 semanas '
                        'hasta 30 mg/kg 2 veces al día (60 mg/kg/día). Dosis máxima: 60 mg/kg/día (hasta 3000 mg/día)',
              texto='Inicial 10 mg/kg c/12 h (20 mg/kg/día); titular hasta 30 mg/kg c/12 h (60 mg/kg/día; máx. 3000 mg/día)',
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: dosis inicial 10 mg/kg 2 veces al día (20 mg/kg/día); '
                           'incremento hasta 30 mg/kg 2 veces al día (60 mg/kg/día; máximo 3000 mg/día)')),
    ]
    return ficha_oral(
        'levetiracetam', 'Levetiracetam', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Administrar dos veces al día repartido en tomas cada 12 horas aproximadamente, con o sin alimentos. '
                                 'La solución oral se puede diluir en un vaso de agua o zumo.',
                        'fuente': fu(LEV_C, '4.2 Forma de administración')},
        ajusteRenalHepatico={'renal': 'Ajuste según ClCr: ClCr ≥80: 500-1500 mg c/12 h; ClCr 50-79: 500-1000 mg c/12 h; '
                                      'ClCr 30-49: 250-750 mg c/12 h; ClCr <30: 250-500 mg c/12 h; hemodiálisis: 500-1000 mg c/24 h '
                                      'con carga de 750 mg y suplemento post-diálisis.',
                             'hepatico': 'No es necesario ajuste en insuficiencia hepática leve a moderada. En insuficiencia grave con ClCr <60 '
                                         'reducir la dosis de mantenimiento un 50 %.',
                             'fuente': fu(LEV_C, '4.2 Insuficiencia renal e Insuficiencia hepática')},
        alertas=['En niños pequeños y pacientes con peso <50 kg se debe utilizar la solución oral con jeringa graduada para dosificación precisa.'],
        comerciales=['Keppra', 'Levetiracetam Cinfa'],
    )


def fenitoina():
    P = _ped('fenitoina', slug='fenitoina-difenilhidantoina', anio=2020)
    presentaciones = [
        pres('capsula-100-mg', 'capsula', mg=100, partible='no',
             fuente=fu(PHT, 'Epanutin 100 mg cápsulas duras (de fenitoína sódica); el arsenal de APS lista comprimido 100 mg')),
    ]
    dosis_ = [
        dosis('Epilepsia: mantenimiento (adultos sin tratamiento previo)', 'adulto', 'fija', 'mg', min=300, max=300, tomas=3,
              intervalo_h=8,
              condicion='Dosis de inicio 300 mg al día dividida en 3 tomas (100 mg cada 8 horas). Ajustar según niveles plasmáticos '
                        '(rango terapéutico habitual 10-20 mcg/ml)',
              texto='Inicial 100 mg c/8 h (300 mg/día); ajustar individualmente según niveles plasmáticos',
              fuente=fu(PHT, '4.2 Adultos: "comenzar con una dosis de inicio de 300 mg al día, dividida en tres tomas iguales '
                             '(1 cápsula de 100 mg cada 8 horas antes de las comidas)"')),
        dosis('Epilepsia: dosis de carga oral (adultos en ámbito hospitalario/supervisado)', 'adulto', 'fija', 'mg', min=1000, max=1000,
              tomas=3, intervalo_h=2,
              condicion='1000 mg divididos en 3 tomas (400 mg, 300 mg, 300 mg) a intervalos de 2 horas con monitorización clínica',
              texto='1000 mg divididos en 3 tomas (400 + 300 + 300 mg) cada 2 horas',
              fuente=fu(PHT, '4.2 Dosis de carga por vía oral: "1.000 mg de fenitoína dividida en tres dosis (400 mg, 300 mg, 300 mg) '
                             'administradas a intervalos de 2 horas"')),
        dosis('Epilepsia: inicio y mantenimiento (niños y adolescentes)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=5, max=5, tomas=2, intervalo_h=12, tope_dia=(300, 'mg'),
              condicion='Dosis inicial 5 mg/kg/día en 2 o 3 tomas. Mantenimiento habitual 4-8 mg/kg/día hasta un máximo de 300 mg al día. '
                        'Pediamécum señala que en niños mayores se puede usar 8-10 mg/kg/día',
              texto='Inicio 5 mg/kg/día en 2-3 tomas; mantenimiento 4-8 mg/kg/día (máximo 300 mg/día)',
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: dosis inicial recomendada 5 mg/kg/día en 2 o 3 tomas; '
                           'mantenimiento 4-8 mg/kg/día; máximo 300 mg/día')),
    ]
    discrepancias_ = [
        discrepancia('Dosis pediátrica de mantenimiento en niños mayores',
                     [(PHT, 'Mantenimiento 4-8 mg/kg/día, máximo 300 mg/día'),
                      (P, 'En niños más mayores se recomienda 8-10 mg/kg/día (máximo 300 mg/día)')],
                     '4-8 mg/kg/día',
                     'Pediamécum amplía el mantenimiento en niños mayores hasta 8-10 mg/kg/día, lo que a pesos intermedios puede saturar '
                     'la cinética no lineal de Michaelis-Menten. Se conserva la recomendación de 4-8 mg/kg/día con tope de 300 mg/día.')
    ]
    return ficha_oral(
        'fenitoina', 'Fenitoína', 'anticonvulsivante', presentaciones, dosis_,
        administracion={'comida': 'antes',
                        'texto': 'Tomar con al menos medio vaso de agua. Administrar preferentemente antes de las comidas; '
                                 'si produce molestias gastrointestinales se puede tomar durante o después de las comidas.',
                        'fuente': fu(PHT, '4.2 Forma de administración: "tomarse por lo menos medio vaso de agua ... '
                                         'antes de las comidas ... o durante o después de las comidas"')},
        ajusteRenalHepatico={'renal': 'No requiere ajuste de dosis en insuficiencia renal; considerar monitoreo de fenitoína libre.',
                             'hepatico': 'Metabolismo hepático saturable: ajustar individualmente según niveles plasmáticos y respuesta clínica.',
                             'fuente': fu(P, 'Insuficiencia renal o hepática (Pediamécum) y CIMA 4.2')},
        discrepancias=discrepancias_,
        alertas=['Cinética no lineal (saturable): pequeños incrementos de dosis pueden provocar grandes aumentos en los niveles plasmáticos y toxicidad.',
                 'Cápsulas de 100 mg no son adecuadas para niños con peso inferior a 20 kg que requieran dosificación fraccionada fina.'],
        comerciales=['Epanutin', 'Fenitoína'],
    )


# ================================================================ §6 Psiquiatría
def sertralina():
    presentaciones = [
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='mitades',
             fuente=fu(ARSENAL, 'Grupo 20.02.01.02: Sertralina, Comprimido 50 mg (divisible en dos mitades)')),
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='mitades',
             fuente=fu(SER_C, 'Besitran 100 mg comprimidos recubiertos con película (ranurados que permiten división en mitades)')),
        pres('concentrado-20-mg-ml', 'gotas', mg_ml=20, gotas_por_ml=20,
             fuente=fu(SER_S, 'Besitran 20 mg/ml concentrado para solución oral (gotero graduado; contiene etanol)')),
    ]
    dosis_ = [
        dosis('Depresión y trastorno obsesivo-compulsivo (adultos)', 'adulto', 'fija', 'mg', min=50, max=50, tomas=1,
              intervalo_h=24, tope_dia=(200, 'mg'),
              condicion='Iniciar con 50 mg una vez al día. En angustia o fobia social iniciar con 25 mg/día la primera semana. '
                        'Incrementos de a 50 mg a intervalos de al menos 1 semana hasta máximo 200 mg/día',
              texto='Inicial 50 mg/día (25 mg/día la primera semana en angustia); incrementos de 50 mg semanalmente hasta máximo 200 mg/día',
              fuente=fu(SER_C, '4.2 Adultos: "iniciarse con una dosis de 50 mg/día ... incrementos en rangos de 50 mg, a intervalos de al '
                               'menos una semana y hasta un máximo de 200 mg/día"')),
        dosis('Trastorno obsesivo-compulsivo (niños de 6 a 12 años)', 'pediatrico', 'fija', 'mg', min=25, max=25, tomas=1,
              intervalo_h=24, tope_dia=(200, 'mg'),
              condicion='Iniciar con 25 mg una vez al día. Incrementar a 50 mg/día tras una semana. '
                        'Siguientes aumentos en rangos de 50 mg cada varias semanas hasta máximo 200 mg/día',
              texto='Inicial 25 mg/día; 50 mg/día a la semana; aumentos progresivos hasta máximo 200 mg/día',
              presentaciones=['comprimido-50-mg', 'concentrado-20-mg-ml'],
              fuente=fu(SER_C, '4.2 Población pediátrica: "De 6-12 años: El tratamiento debe iniciarse con 25 mg una vez al día. '
                               'La dosis se puede incrementar a 50 mg una vez al día, tras una semana ... dosis máxima es de 200 mg/día"')),
        dosis('Trastorno obsesivo-compulsivo (adolescentes de 13 a 17 años)', 'pediatrico', 'fija', 'mg', min=50, max=50, tomas=1,
              intervalo_h=24, tope_dia=(200, 'mg'),
              condicion='Iniciar con 50 mg una vez al día; incrementos graduales en rangos de 50 mg hasta máximo 200 mg/día',
              texto='Inicial 50 mg/día; incrementos graduales hasta máximo 200 mg/día',
              fuente=fu(SER_C, '4.2 Población pediátrica: "De 13 – 17 años: El tratamiento debe iniciarse con 50 mg una vez al día ... '
                               'dosis máxima es de 200 mg/día"')),
    ]
    return ficha_oral(
        'sertralina', 'Sertralina', 'antidepresivo', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Los comprimidos y el concentrado se pueden administrar con o sin alimentos, en una sola toma diaria '
                                 '(por la mañana o por la noche). El concentrado debe diluirse antes de tomar en agua, zumo o bebida.',
                        'fuente': fu(SER_C, '4.2 Forma de administración y CIMA 63477')},
        ajusteRenalHepatico={'renal': 'No es necesario ajustar la dosis en insuficiencia renal.',
                             'hepatico': 'Usar con precaución; utilizar una dosis más baja o espaciar el intervalo. No usar en insuficiencia grave.',
                             'fuente': fu(SER_C, '4.2 Pacientes con insuficiencia hepática y renal')},
        alertas=['Ficha de fuente única: se apoya exclusivamente en CIMA (España); Pediamécum no dispone de monografía para sertralina.',
                 'No se ha demostrado eficacia en pacientes pediátricos para el trastorno de depresión mayor (uso pediátrico limitado a TOC).',
                 'El concentrado oral contiene un porcentaje de etanol (alcohol).'],
        comerciales=['Besitran', 'Zoloft'],
    )


def fluoxetina():
    P = _ped('fluoxetina', anio=2020)
    presentaciones = [
        pres('capsula-20-mg', 'capsula', mg=20, partible='no',
             fuente=fu(FLX_C, 'Fluoxetina Cinfa 20 mg cápsulas duras; el arsenal de APS lista comprimido 20 mg')),
        pres('solucion-oral-4-mg-ml', 'jarabe', mg_ml=4,
             fuente=fu(FLX_S, 'Fluoxetina Normon 20 mg/5 ml solución oral (4 mg/ml; 2,5 ml = 10 mg)')),
    ]
    dosis_ = [
        dosis('Depresión mayor (adultos)', 'adulto', 'fija', 'mg', min=20, max=20, tomas=1, intervalo_h=24,
              tope_dia=(60, 'mg'),
              condicion='Dosis recomendada 20 mg diarios. En caso necesario incrementar gradualmente hasta un máximo de 60 mg/día '
                        '(en bulimia nerviosa se recomiendan 60 mg/día)',
              texto='Inicial 20 mg/día; titular según respuesta hasta máximo 60 mg/día (máx. 80 mg/día en estudios)',
              fuente=fu(FLX_C, '4.2 Adultos: "La dosis recomendada es de 20 mg diarios ... incrementar gradualmente hasta un máximo de 60 mg"')),
        dosis('Depresión moderada a grave (niños ≥8 años y adolescentes)', 'pediatrico', 'fija', 'mg', min=10, max=10, tomas=1,
              intervalo_h=24, tope_dia=(20, 'mg'),
              condicion='Iniciar con 10 mg/día (2,5 ml de solución oral). Tras 1 o 2 semanas incrementar a 20 mg/día. '
                        'El tratamiento debe ser iniciado y supervisado por un especialista en psiquiatría infanto-juvenil',
              texto='Inicial 10 mg/día (2,5 ml solución); tras 1-2 semanas incrementar a 20 mg/día (tope ficha técnica: 20 mg/día)',
              presentaciones=['solucion-oral-4-mg-ml'],
              fuente=fu(P, '4.2 Niños a partir de 8 años y Pediamécum: dosis inicial 10 mg/día; '
                           'a las 1-2 semanas incrementar a 20 mg/día; máx 20 mg/día')),
    ]
    discrepancias_ = [
        discrepancia('Techo pediátrico en depresión y TOC',
                     [(FLX_C, '20 mg/día en depresión pediátrica (experiencia mínima con >20 mg)'),
                      (P, 'Hasta 40 mg/día en depresión (dosis alternativa de expertos); 20-60 mg/día en TOC')],
                     '20 mg/día',
                     'CIMA sitúa el límite pediátrico avalado en 20 mg/día señalando experiencia mínima por encima de esa cifra; '
                     'Pediamécum recoge pautas de expertos hasta 40-60 mg/día. Se muestra el tope oficial conservador de 20 mg/día.')
    ]
    return ficha_oral(
        'fluoxetina', 'Fluoxetina', 'antidepresivo', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Administrar en dosis única por la mañana o fraccionada en dos tomas, durante o entre las comidas.',
                        'fuente': fu(FLX_C, '4.2 Forma de administración')},
        ajusteRenalHepatico={'renal': 'No es necesario ajuste en insuficiencia renal leve a moderada.',
                             'hepatico': 'Considerar una dosis menor o menos frecuente (ej. 20 mg cada dos días) por semivida prolongada.',
                             'fuente': fu(FLX_C, '4.2 Pacientes con insuficiencia hepática y renal')},
        discrepancias=discrepancias_,
        alertas=['En niños y adolescentes menores de 18 años existe mayor riesgo de conductas suicidas y hostilidad: '
                 'vigilar estrechamente al inicio del tratamiento.',
                 'Semivida muy prolongada de fluoxetina y su metabolito norfluoxetina (hasta 1-2 semanas tras suspender).'],
        comerciales=['Prozac', 'Fluoxetina Cinfa'],
    )


def escitalopram():
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='mitades',
             fuente=fu(ESC_C, 'Escitalopram Cinfa 10 mg comprimidos (ranurados que permiten división en mitades); '
                              'el arsenal de APS lista comprimido 10 mg')),
        pres('gotas-20-mg-ml', 'gotas', mg_ml=20, gotas_por_ml=20,
             fuente=fu(ESC_G, 'Escitalopram Cinfa 20 mg/ml gotas orales en solución (1 gota = 1 mg escitalopram)')),
    ]
    dosis_ = [
        dosis('Depresión mayor y trastornos de ansiedad (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=1,
              intervalo_h=24, tope_dia=(20, 'mg'),
              condicion='Dosis habitual 10 mg una vez al día. En trastorno de angustia iniciar con 5 mg/día la primera semana. '
                        'Según respuesta puede aumentarse hasta un máximo de 20 mg/día. Pacientes >65 años: inicio 5 mg, máx. 10 mg/día',
              texto='Inicial 10 mg/día (5 mg/día en angustia o ancianos); máximo 20 mg/día (máx. 10 mg/día en ancianos)',
              fuente=fu(ESC_C, '4.2 Posología: "La dosis recomendada es de 10 mg una vez al día ... puede aumentarse hasta un máximo de 20 mg"')),
    ]
    return ficha_oral(
        'escitalopram', 'Escitalopram', 'antidepresivo', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Administrar en dosis única diaria (por la mañana o por la noche), con o sin alimentos. '
                                 'Las gotas pueden mezclarse con agua, zumo de naranja o zumo de manzana.',
                        'fuente': fu(ESC_C, '4.2 Forma de administración y CIMA 76398')},
        ajusteRenalHepatico={'renal': 'No es necesario ajuste en insuficiencia renal leve o moderada; precaución con ClCr <30 ml/min.',
                             'hepatico': 'Inicio 5 mg/día durante las primeras 2 semanas; según respuesta aumentar hasta máximo 10 mg/día.',
                             'fuente': fu(ESC_C, '4.2 Insuficiencia renal e Insuficiencia hepática')},
        pediatria='solo_adulto',
        motivo_solo_adulto='No debe utilizarse en el tratamiento de niños y adolescentes menores de 18 años por falta de eficacia '
                           'y aumento de comportamientos suicidas en ensayos clínicos (CIMA)',
        alertas=['Ficha de fuente única: se apoya exclusivamente en CIMA (España); Pediamécum no dispone de monografía para escitalopram.',
                 '1 gota de solución oral equivale exactamente a 1 mg de escitalopram (20 gotas/ml).'],
        comerciales=['Cipralex', 'Escitalopram Cinfa'],
    )


def amitriptilina():
    P = _ped('amitriptilina', anio=2021)
    presentaciones = [
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no',
             fuente=fu(ARSENAL, 'Grupo 20.02.01.01: Amitriptilina, Comprimido 25 mg')),
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(AMI, 'Tryptizol 10 mg comprimidos recubiertos con película')),
    ]
    dosis_ = [
        dosis('Depresión (adultos)', 'adulto', 'fija', 'mg', min=25, max=75, tomas=2, intervalo_h=12,
              tope_toma=(75, 'mg'), tope_dia=(150, 'mg'),
              condicion='Inicial 25 mg 2 veces al día (50 mg/día). Aumentar de a 25 mg en días alternos hasta 100-150 mg/día '
                        'en 2 tomas (máximo 150 mg/día; 75 mg por toma). Ancianos: inicio 10-25 mg/día',
              texto='Inicial 25 mg 2 veces/día (50 mg/día); titular hasta 100-150 mg/día divididos en dos tomas (máx. 75 mg/toma, 150 mg/día)',
              fuente=fu(AMI, '4.2 Adultos: "Inicialmente, 25 mg 2 veces al día (50 mg al día) ... hasta un máximo de 150 mg al día divididos en dos tomas"')),
        dosis('Dolor neuropático y profilaxis de migraña (adultos)', 'adulto', 'fija', 'mg', min=10, max=25, tomas=1,
              intervalo_h=24, tope_dia=(75, 'mg'),
              condicion='Dosis inicial 10-25 mg por la noche; aumentar en 10-25 mg cada 3-7 días. '
                        'Dosis habitual 25-75 mg/día en toma única nocturna (no se recomienda dosis única superior a 75 mg)',
              texto='Inicial 10-25 mg por la noche; aumentar cada 3-7 días; habitual 25-75 mg nocturnos (máximo 75 mg/dosis única)',
              fuente=fu(AMI, '4.2 Dolor neuropático y profilaxis de cefalea/migraña: "La dosis inicial debe ser de 10 mg-25 mg por la noche ... '
                             'No se recomienda una dosis única superior a 75 mg"')),
        dosis('Enuresis nocturna (niños de 6 a 10 años)', 'pediatrico', 'fija', 'mg', min=10, max=20, tomas=1,
              intervalo_h=24, tope_dia=(20, 'mg'),
              condicion='10 a 20 mg al acostarse. Administrar 1-2 horas antes de acostarse. El tratamiento no debe superar los 3 meses sin revisión médica',
              texto='10-20 mg al acostarse (máx. 20 mg/día; no superar 3 meses seguidos)',
              presentaciones=['comprimido-10-mg'],
              fuente=fu(P, '4.2 Niños de 6 a 10 años y Pediamécum: 10 mg ‑ 20 mg al acostarse; máx 20 mg/día')),
        dosis('Enuresis nocturna (niños y adolescentes ≥11 años)', 'pediatrico', 'fija', 'mg', min=25, max=50, tomas=1,
              intervalo_h=24, tope_dia=(50, 'mg'),
              condicion='25 a 50 mg al acostarse. Administrar 1-2 horas antes de acostarse. No superar los 3 meses sin revisión médica',
              texto='25-50 mg al acostarse (máx. 50 mg/día; no superar 3 meses seguidos)',
              fuente=fu(P, '4.2 Niños ≥11 años y Pediamécum: 25 mg – 50 mg al día antes de acostarse; máx 50 mg/día')),
    ]
    return ficha_oral(
        'amitriptilina', 'Amitriptilina', 'antidepresivo', presentaciones, dosis_,
        administracion={'comida': 'con_comida',
                        'texto': 'Tomar con comidas para disminuir los síntomas gastrointestinales. En dosis única diaria administrar '
                                 'preferentemente por la noche antes de acostarse por su marcado efecto sedante.',
                        'fuente': fu(AMI, '4.2 Forma de administración y Pediamécum')},
        ajusteRenalHepatico={'renal': 'Se puede administrar en dosis habituales en insuficiencia renal.',
                             'hepatico': 'Administrar con precaución; considerar reducción del 50 % de la dosis de inicio por menor metabolismo.',
                             'fuente': fu(AMI, '4.2 Pacientes con insuficiencia renal o hepática')},
        alertas=['No autorizada para depresión en niños y adolescentes menores de 18 años (uso pediátrico autorizado restringido a enuresis nocturna).',
                 'Efectos anticolinérgicos marcados: sequedad bucal, estreñimiento, retención urinaria y riesgo de prolongación del intervalo QT.'],
        comerciales=['Tryptizol', 'Amitriptilina'],
    )


def mirtazapina():
    presentaciones = [
        pres('comprimido-15-mg', 'comprimido', mg=15, partible='mitades',
             fuente=fu(MIR, 'Mirtazapina Cinfa 15 mg comprimidos (ranurados en mitades); el arsenal de APS lista 15 mg')),
        pres('comprimido-30-mg', 'comprimido', mg=30, partible='mitades',
             fuente=fu(ARSENAL, 'Grupo 20.02.01.03: Mirtazapina, Comprimido 30 mg')),
    ]
    dosis_ = [
        dosis('Episodio de depresión mayor (adultos)', 'adulto', 'fija', 'mg', min=15, max=30, tomas=1,
              intervalo_h=24, tope_dia=(45, 'mg'),
              condicion='Dosis de inicio 15 o 30 mg al día. Dosis eficaz habitual entre 15 y 45 mg al día. '
                        'Administrar preferiblemente en toma única por la noche antes de acostarse',
              texto='Inicio 15-30 mg/día nocturnos; titular según respuesta hasta 45 mg/día (máximo 45 mg/día)',
              fuente=fu(MIR, '4.2 Adultos: "La dosis eficaz diaria que se utiliza generalmente es de entre 15 y 45 mg; '
                             'la dosis de inicio es de 15 o 30 mg ... dosis máxima [45 mg]"')),
    ]
    return ficha_oral(
        'mirtazapina', 'Mirtazapina', 'antidepresivo', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Tomar preferiblemente en dosis única por la noche antes de acostarse. '
                                 'También puede administrarse repartida en dos tomas (mañana y noche, dosis mayor por la noche). '
                                 'Los comprimidos se ingieren con un poco de agua sin masticar.',
                        'fuente': fu(MIR, '4.2 Forma de administración')},
        ajusteRenalHepatico={'renal': 'El aclaramiento puede disminuir con ClCr <40 ml/min; usar con precaución.',
                             'hepatico': 'El aclaramiento puede disminuir en insuficiencia hepática; usar con precaución.',
                             'fuente': fu(MIR, '4.2 Insuficiencia renal e Insuficiencia hepática')},
        pediatria='solo_adulto',
        motivo_solo_adulto='No debe utilizarse en niños y adolescentes menores de 18 años por falta de eficacia en ensayos clínicos '
                           'y aumento de ideación suicida y hostilidad (CIMA)',
        alertas=['Ficha de fuente única: se apoya exclusivamente en CIMA (España); Pediamécum no dispone de monografía para mirtazapina.',
                 'Marcado efecto sedante e incremento del apetito / ganancia ponderal característicos del bloqueo histaminérgico H1.'],
        comerciales=['Rexer', 'Mirtazapina Cinfa'],
    )


def venlafaxina():
    P = _ped('venlafaxina', anio=2021)
    presentaciones = [
        pres('comprimido-75-mg', 'comprimido', mg=75, partible='no',
             fuente=fu(ARSENAL, 'Grupo 20.02.01.02: Venlafaxina, Comprimido 75 mg (de liberación inmediata)')),
        pres('comprimido-37-5-mg', 'comprimido', mg=37.5, partible='mitades',
             fuente=fu(VEN_37, 'Dobupal 37,5 mg comprimidos (liberación inmediata, ranurados que permiten división en mitades)')),
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(VEN_50, 'Dobupal 50 mg comprimidos (liberación inmediata)')),
    ]
    dosis_ = [
        dosis('Episodio de depresión mayor (adultos)', 'adulto', 'fija', 'mg', min=75, max=75, tomas=2,
              intervalo_h=12, tope_dia=(375, 'mg'),
              condicion='Dosis inicial recomendada de liberación inmediata: 75 mg/día en 2 o 3 dosis divididas tomadas con comida. '
                        'Incrementar según respuesta cada ≥2 semanas hasta máximo 375 mg/día',
              texto='Inicial 75 mg/día en 2-3 tomas con comida; titular cada 2 semanas hasta máximo 375 mg/día',
              fuente=fu(VEN_37, '4.2 Adultos: "La dosis inicial recomendada de venlafaxina de liberación inmediata es de 75 mg/día '
                                'en dos o tres dosis divididas tomadas con comida ... hasta una dosis máxima de 375 mg/día"')),
        dosis('Trastorno depresivo mayor resistente (adolescentes >40 kg, uso fuera de ficha)', 'adulto', 'fija', 'mg',
              min=37.5, max=75, tomas=2, intervalo_h=12, tope_dia=(75, 'mg'), estatus='off_label',
              condicion='Pediamécum: baja eficacia y aumento de ideación suicida en <18 años; reservar exclusivamente para pacientes '
                        'sin respuesta a fluoxetina o sertralina. Dosis inicial 12,5-37,5 mg/día; titular con alimentos hasta máx. 75 mg/día',
              texto='Inicial 12,5-37,5 mg/día; titular semanalmente hasta máximo 75 mg/día en 2-3 tomas con comida',
              fuente=fu(P, 'Pediamécum: "Dosis y Pautas: Dosis de inicio: 12,5 mg/24 h-37,5 mg/24 h ... >40 kg: hasta un máximo de 75 mg/día (E: off-label)"')),
    ]
    return ficha_oral(
        'venlafaxina', 'Venlafaxina', 'antidepresivo', presentaciones, dosis_,
        administracion={'comida': 'con_comida',
                        'texto': 'Los comprimidos de liberación inmediata se deben tomar con alimentos, repartidos en 2 o 3 tomas al día '
                                 'aproximadamente a las mismas horas.',
                        'fuente': fu(VEN_37, '4.2 Forma de administración')},
        ajusteRenalHepatico={'renal': 'Reducir la dosis diaria total en un 50 % en pacientes en hemodiálisis o con TFG <30 ml/min.',
                             'hepatico': 'Reducir la dosis en un 50 % en insuficiencia hepática leve a moderada; en casos graves reducir en más del 50 %.',
                             'fuente': fu(VEN_37, '4.2 Pacientes con insuficiencia renal y hepática')},
        pediatria='solo_adulto',
        motivo_solo_adulto='No recomendada en niños y adolescentes: los ensayos clínicos no demostraron eficacia en depresión y evidenciaron '
                           'aumento de ideación suicida y hostilidad. Las presentaciones de liberación inmediata del arsenal no permiten dosis pediátricas.',
        alertas=['Presentación de liberación inmediata: no confundir con cápsulas de liberación prolongada (retard).',
                 'Interrupción obligatoriamente gradual (síndrome de retirada frecuente si se suspende de forma brusca).'],
        comerciales=['Dobupal', 'Efexor'],
    )


def quetiapina():
    presentaciones = [
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no',
             fuente=fu(ARSENAL, 'Grupo 20.01.03: Quetiapina, Comprimido 25 mg (de liberación inmediata)')),
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(QUE_100, 'Qudix 100 mg comprimidos recubiertos con película (liberación inmediata)')),
        pres('comprimido-200-mg', 'comprimido', mg=200, partible='no',
             fuente=fu(QUE_200, 'Qudix 200 mg comprimidos recubiertos con película (liberación inmediata)')),
    ]
    dosis_ = [
        dosis('Esquizofrenia (adultos)', 'adulto', 'fija', 'mg', min=50, max=50, tomas=2, intervalo_h=12,
              tope_dia=(750, 'mg'),
              condicion='Titulación en 2 tomas diarias: día 1: 50 mg; día 2: 100 mg; día 3: 200 mg; día 4: 300 mg. '
                        'Dosis habitual efectiva: 300-450 mg/día (rango terapéutico 150-750 mg/día)',
              texto='Días 1-4: 50, 100, 200, 300 mg/día en 2 tomas; habitual 300-450 mg/día; rango 150-750 mg/día',
              fuente=fu(QUE_100, '4.2 Esquizofrenia: "dos veces al día ... 50 mg (Día 1), 100 mg (Día 2), 200 mg (Día 3) y 300 mg (Día 4) ... '
                                 'rango de 150 a 750 mg/día"')),
        dosis('Episodios maníacos en trastorno bipolar (adultos)', 'adulto', 'fija', 'mg', min=100, max=100, tomas=2,
              intervalo_h=12, tope_dia=(800, 'mg'),
              condicion='Titulación en 2 tomas diarias: día 1: 100 mg; día 2: 200 mg; día 3: 300 mg; día 4: 400 mg. '
                        'Aumentos de hasta 200 mg/día hasta máximo 800 mg/día en el día 6. Habitual 400-800 mg/día',
              texto='Días 1-4: 100, 200, 300, 400 mg/día en 2 tomas; titular hasta máximo 800 mg/día en el día 6',
              fuente=fu(QUE_100, '4.2 Episodios maníacos: "100 mg (Día 1), 200 mg (Día 2), 300 mg (Día 3) y 400 mg (Día 4) ... '
                                 'hasta 800 mg/día en el Día 6 ... rango de 400 a 800 mg/día"')),
    ]
    return ficha_oral(
        'quetiapina', 'Quetiapina', 'antipsicotico', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Los comprimidos de liberación inmediata se pueden administrar con o sin alimentos, '
                                 'divididos en dos tomas al día (mañana y noche). Tragarse enteros con agua.',
                        'fuente': fu(QUE_100, '4.2 Forma de administración')},
        ajusteRenalHepatico={'renal': 'No se requiere ajuste posológico en pacientes con insuficiencia renal.',
                             'hepatico': 'Metabolismo hepático extenso: iniciar con 25 mg/día e incrementar diariamente en 25-50 mg/día según respuesta.',
                             'fuente': fu(QUE_100, '4.2 Insuficiencia renal e Insuficiencia hepática')},
        pediatria='solo_adulto',
        motivo_solo_adulto='No se debe utilizar en niños ni adolescentes menores de 18 años debido a la falta de datos que avalen su uso '
                           'y aumento de efectos adversos tiroideos y extrapiramidales (CIMA)',
        alertas=['Ficha de fuente única: se apoya exclusivamente en CIMA (España); Pediamécum no dispone de monografía para quetiapina.',
                 'Formulación de liberación inmediata (Qudix / arsenal 25 mg): no intercambiable directamente mg a mg con la de liberación prolongada.',
                 'Riesgo de hipotensión ortostática y somnolencia durante la fase de titulación inicial.'],
        comerciales=['Qudix', 'Seroquel'],
    )


def haloperidol():
    P = _ped('haloperidol', anio=2020)
    presentaciones = [
        pres('gotas-2-mg-ml', 'gotas', mg_ml=2, gotas_por_ml=20,
             fuente=fu(HAL_S, 'Haloperidol Esteve 2 mg/ml solución oral (frasco cuentagotas: 20 gotas = 2 mg; 1 gota = 0,1 mg)')),
        pres('comprimido-1-mg', 'comprimido', mg=1, partible='no',
             fuente=fu(ARSENAL, 'Grupo 20.01: Haloperidol, Comprimido 1 mg')),
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='no',
             fuente=fu(ARSENAL, 'Grupo 20.01: Haloperidol, Comprimido 5 mg')),
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='mitades',
             fuente=fu(HAL_C, 'Haloperidol Esteve 10 mg comprimidos (ranurados que permiten división en mitades)')),
    ]
    dosis_ = [
        dosis('Esquizofrenia y psicosis crónica (adultos)', 'adulto', 'fija', 'mg', min=2, max=10, tomas=2,
              intervalo_h=12, tope_dia=(20, 'mg'),
              condicion='2 a 10 mg/día en toma única o 2 tomas divididas. Ajustar cada 1-7 días. '
                        'Dosis máxima 20 mg/día (dosis >10 mg/día aumentan síntomas extrapiramidales sin mayor eficacia)',
              texto='Inicial 2-10 mg/día en 1 o 2 tomas; titular cada 1-7 días; máximo 20 mg/día',
              fuente=fu(HAL_C, 'Tabla 1 Adultos: "2 a 10 mg/día por vía oral, en una sola dosis o en 2 dosis divididas ... '
                               'La dosis máxima es de 20 mg/día"')),
        dosis('Esquizofrenia (adolescentes de 13 a 17 años)', 'pediatrico', 'fija', 'mg', min=0.5, max=3, tomas=2,
              intervalo_h=12, tope_dia=(5, 'mg'),
              condicion='Dosis recomendada de 0,5 a 3 mg/día administrados en 2 o 3 dosis divididas. Dosis máxima recomendada 5 mg/día',
              texto='0,5-3 mg/día en 2-3 tomas diarias (máximo 5 mg/día en CIMA; Pediamécum hasta 15 mg/día)',
              fuente=fu(HAL_S, '4.2 Población pediátrica: "0,5 a 3 mg/día por vía oral, divididos en 2 o 3 tomas ... '
                               'La dosis máxima es de 5 mg/día"')),
        dosis('Esquizofrenia y alteraciones graves de conducta (niños de 3 a 12 años)', 'pediatrico', 'fija', 'mg',
              min=0.5, max=0.5, tomas=2, intervalo_h=12, tope_dia=(6, 'mg'),
              condicion='Inicial 0,5 mg/día repartidos en 2 o 3 tomas; habitual 1-4 mg/día; máximo 6 mg/día',
              texto='Inicial 0,5 mg/día en 2-3 tomas; habitual 1-4 mg/día; máximo 6 mg/día',
              presentaciones=['gotas-2-mg-ml', 'comprimido-1-mg'],
              fuente=fu(P, 'Esquizofrenia: "3-13 años: inicialmente dosis de 0,5 mg/día, repartidos en 2-3 dosis; '
                           'habitualmente se requieren dosis de 1-4 mg/día, hasta un máximo de 6 mg/día"')),
    ]
    discrepancias_ = [
        discrepancia('Dosis máxima en adolescentes >13 años',
                     [(HAL_S, 'Máximo 5 mg/día en adolescentes 13-17 años'),
                      (P, 'Máximo 15 mg/día repartidos en 2-3 dosis')],
                     '5 mg/día',
                     'CIMA establece un techo estricto de 5 mg/día en adolescentes para limitar el riesgo de distonías y síntomas extrapiramidales; '
                     'Pediamécum contempla hasta 15 mg/día. Se muestra el límite oficial de 5 mg/día.')
    ]
    return ficha_oral(
        'haloperidol', 'Haloperidol', 'antipsicotico', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'La solución oral se puede mezclar con agua o zumo para facilitar la deglución. '
                                 'Para dosis menores a 1 mg debe utilizarse la solución oral cuentagotas.',
                        'fuente': fu(HAL_S, '4.2 Forma de administración: "Haloperidol Esteve solución oral se debe usar para '
                                           'dosis únicas inferiores a 1 mg"')},
        ajusteRenalHepatico={'renal': 'Dosificación ajustada no formalmente establecida; usar con precaución.',
                             'hepatico': 'Metabolizado por el hígado: usar con precaución y a dosis reducidas.',
                             'fuente': fu(HAL_C, '4.2 Poblaciones especiales y Pediamécum')},
        discrepancias=discrepancias_,
        alertas=['1 gota de solución al 2 mg/ml contiene exactamente 0,1 mg de haloperidol (20 gotas = 2 mg).',
                 'Riesgo elevado de reacciones extrapiramidales agudas (distonía aguda, acatisia, parkinsonismo) y de prolongación del QT.'],
        comerciales=['Haloperidol Esteve', 'Haldol'],
    )


def risperidona():
    P = _ped('risperidona', anio=2020)
    presentaciones = [
        pres('solucion-oral-1-mg-ml', 'jarabe', mg_ml=1,
             fuente=fu(RIS_S, 'Risperdal 1 mg/ml solución oral (jeringa dosificadora graduada; mínimo medible 0,25 mg)')),
        pres('comprimido-1-mg', 'comprimido', mg=1, partible='mitades',
             fuente=fu(RIS_C, 'Risperdal 1 mg comprimidos recubiertos con película (ranurados en mitades); el arsenal de APS lista 1 mg')),
        pres('comprimido-3-mg', 'comprimido', mg=3, partible='mitades',
             fuente=fu(ARSENAL, 'Grupo 20.01: Risperidona, Comprimido 3 mg')),
    ]
    dosis_ = [
        dosis('Esquizofrenia (adultos)', 'adulto', 'fija', 'mg', min=2, max=2, tomas=1, intervalo_h=24,
              tope_dia=(16, 'mg'),
              condicion='Día 1: 2 mg/día; día 2: 4 mg/día. Dosis habitual 4 a 6 mg/día en 1 o 2 tomas. '
                        'Dosis >10 mg/día no muestran mayor eficacia y aumentan extrapiramidales. Máximo evaluado 16 mg/día',
              texto='Día 1: 2 mg/día; día 2: 4 mg/día; habitual 4-6 mg/día; máximo 16 mg/día',
              fuente=fu(RIS_C, '4.2 Esquizofrenia: "comenzando con 2 mg de risperidona ... aumentarse hasta 4 mg el día 2 ... '
                               'mayoría resultarán beneficiados con 4 a 6 mg/día ... seguridad no evaluada >16 mg/día"')),
        dosis('Irritabilidad y agresión en autismo (niños ≥5 años y adolescentes <50 kg)', 'pediatrico', 'fija', 'mg',
              min=0.25, max=0.25, tomas=1, intervalo_h=24, tope_dia=(1.5, 'mg'),
              condicion='Inicio 0,25 mg una vez al día. Incrementar en 0,25 mg cada ≥14 días. Dosis óptima habitual: 0,5 mg/día '
                        '(rango 0,25-0,75 mg/día). Pediamécum fija tope en ≤20 kg de 1,5 mg/día y en >20 kg de 2,5 mg/día',
              texto='Inicial 0,25 mg/día; óptima 0,5 mg/día (rango 0,25-0,75 mg/día); máximo 1,5 mg/día',
              presentaciones=['solucion-oral-1-mg-ml'],
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: dosis inicial 0,25 mg una vez al día; '
                           'dosis óptima 0,5 mg/día; máximo 1,5 mg/día')),
        dosis('Irritabilidad y agresión en autismo (niños ≥5 años y adolescentes ≥50 kg)', 'pediatrico', 'fija', 'mg',
              min=0.5, max=0.5, tomas=1, intervalo_h=24, tope_dia=(3.5, 'mg'),
              condicion='Inicio 0,5 mg una vez al día. Incrementar en 0,5 mg cada ≥14 días. Dosis óptima habitual: 1 mg/día '
                        '(rango 0,5-1,5 mg/día). Pediamécum fija tope en >45 kg de 3,5 mg/día',
              texto='Inicial 0,5 mg/día; óptima 1 mg/día (rango 0,5-1,5 mg/día); máximo 3,5 mg/día',
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: dosis inicial 0,5 mg una vez al día; '
                           'dosis óptima 1 mg/día; máximo 3,5 mg/día')),
    ]
    return ficha_oral(
        'risperidona', 'Risperidona', 'antipsicotico', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Se puede tomar con o sin alimentos. La solución oral se puede mezclar con agua, leche o zumo de naranja, '
                                 'pero NO con té ni bebidas de cola.',
                        'fuente': fu(RIS_S, '4.2 Forma de administración y Pediamécum')},
        ajusteRenalHepatico={'renal': 'Reducir la dosis inicial y de mantenimiento a la mitad; titular más lentamente.',
                             'hepatico': 'Reducir la dosis inicial y de mantenimiento a la mitad; titular más lentamente.',
                             'fuente': fu(RIS_C, '4.2 Insuficiencia renal y hepática: "tanto la dosis inicial como las consecutivas '
                                                'deben reducirse a la mitad"')},
        alertas=['Esquizofrenia y manía bipolar: no recomendada en niños y adolescentes menores de 18 años por falta de eficacia.',
                 'La dosis mínima medible con la jeringa de solución oral es de 0,25 mg (0,25 ml).',
                 'Riesgo de hiperprolactinemia, aumento de peso y síntomas extrapiramidales dosis-dependientes.'],
        comerciales=['Risperdal', 'Risperidona'],
    )


def zopiclona():
    presentaciones = [
        pres('comprimido-7-5-mg', 'comprimido', mg=7.5, partible='mitades',
             fuente=fu(ZOP, 'Limován 7,5 mg comprimidos recubiertos con película (ranurados que permiten división en dos mitades de 3,75 mg); '
                            'el arsenal de APS lista comprimido 7,5 mg')),
    ]
    dosis_ = [
        dosis('Insomnio transitorio o de corta duración (adultos)', 'adulto', 'fija', 'mg', min=7.5, max=7.5, tomas=1,
              intervalo_h=24, tope_dia=(7.5, 'mg'),
              condicion='7,5 mg por vía oral antes de acostarse. Esta dosis de 7,5 mg no debe ser sobrepasada. '
                        'En pacientes de edad avanzada o con insuficiencia hepática, renal o respiratoria iniciar con 3,75 mg',
              texto='7,5 mg al acostarse (máximo estricto 7,5 mg/día; 3,75 mg en ancianos o insuficiencia hepática/renal)',
              fuente=fu(ZOP, '4.2 Adultos: "La dosis recomendada para adultos es de 7,5 mg de Limován por vía oral, antes de acostarse. '
                            'Esta dosis de 7,5 mg no debe ser sobrepasada"')),
    ]
    return ficha_oral(
        'zopiclona', 'Zopiclona', 'hipnotico-ansiolitico', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Tomar inmediatamente antes de acostarse, asegurando un periodo de sueño ininterrumpido de 7 a 8 horas.',
                        'fuente': fu(ZOP, '4.2 Posología y forma de administración')},
        ajusteRenalHepatico={'renal': 'Iniciar con 3,75 mg (medio comprimido); aumentar a 7,5 mg solo en caso necesario.',
                             'hepatico': 'Iniciar con 3,75 mg (medio comprimido); aumentar a 7,5 mg solo en caso necesario.',
                             'fuente': fu(ZOP, '4.2 Insuficiencia hepática e Insuficiencia renal')},
        pediatria='solo_adulto',
        motivo_solo_adulto='Contraindicada en niños y adolescentes menores de 18 años por ausencia de datos de seguridad y eficacia (CIMA)',
        alertas=['Ficha de fuente única: se apoya exclusivamente en CIMA (España); Pediamécum no dispone de monografía para zopiclona.',
                 'Tratamiento de corta duración: no superar las 4 semanas de tratamiento incluyendo el periodo de retirada gradual.',
                 'Riesgo de amnesia anterógrada y sonambulismo si no se dispone de 7-8 horas de reposo tras la toma.'],
        comerciales=['Limovan', 'Zopiclona'],
    )


def diazepam():
    P = _ped('diazepam', anio=2020)
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='mitades',
             fuente=fu(DZP_C, 'Diazepam Cinfa 10 mg comprimidos (ranurados que permiten división en mitades); '
                              'el arsenal de APS lista comprimido 10 mg')),
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='mitades',
             fuente=fu(DZP_C, 'Diazepam Cinfa 5 mg comprimidos (divisibles en dos mitades de 2,5 mg)')),
        pres('solucion-oral-2-mg-ml', 'gotas', mg_ml=2, gotas_por_ml=20,
             fuente=fu(DZP_S, 'Diazepan Prodes 2 mg/ml solución oral (frasco con cuentagotas: 20 gotas = 2 mg; 1 gota = 0,1 mg)')),
    ]
    dosis_ = [
        dosis('Ansiedad y tensión psíquica (adultos)', 'adulto', 'fija', 'mg', min=2, max=10, tomas=3,
              intervalo_h=8, tope_dia=(40, 'mg'),
              condicion='2 a 10 mg, 2 a 4 veces al día según gravedad. Ancianos o pacientes debilitados: 2-2,5 mg 1-2 veces al día',
              texto='2 a 10 mg 2-4 veces al día (habitual 5-20 mg/día; ancianos 2-2,5 mg 1-2 veces/día)',
              fuente=fu(DZP_C, '4.2 Adultos: "Síntomas de ansiedad: 2 a 10 mg, 2 a 4 veces al día, dependiendo de la gravedad"')),
        dosis('Ansiedad, espasmo muscular y sedación (niños >6 meses)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=0.1, max=0.3, tomas=2, intervalo_h=12,
              condicion='Norma general: 0,1-0,3 mg/kg al día repartidos en 2 o 3 tomas. CIMA cita también 2 a 2,5 mg 1 o 2 veces al día. '
                        'No recomendado en menores de 6 meses. Pediamécum contempla hasta 0,8-1 mg/kg/día',
              texto='0,1-0,3 mg/kg/día en 2-3 tomas diarias (tope ficha técnica CIMA: 0,3 mg/kg/día)',
              fuente=fu(P, '4.2 Población pediátrica y Pediamécum: como norma general 0,1-0,3 mg/kg al día en 2 o 3 tomas')),
    ]
    discrepancias_ = [
        discrepancia('Techo pediátrico oral',
                     [(DZP_C, '0,3 mg/kg/día: norma general máxima al día (CIMA)'),
                      (P, '0,8 mg/kg/día: dosis máxima en ansiedad (Pediamécum); 1 mg/kg/día en convulsiones febriles')],
                     '0,3 mg/kg/día',
                     'CIMA establece como norma general pediátrica 0,1-0,3 mg/kg/día; Pediamécum autoriza hasta 0,8 mg/kg/día '
                     'en ansiedad y 1 mg/kg/día en convulsiones febriles (3 veces el techo de la ficha). '
                     'Se muestra el límite conservador de CIMA (0,3 mg/kg/día).')
    ]
    return ficha_oral(
        'diazepam', 'Diazepam', 'hipnotico-ansiolitico', presentaciones, dosis_,
        administracion={'comida': 'indiferente',
                        'texto': 'Los comprimidos se ingieren enteros o fraccionados con agua. Las gotas se pueden diluir en un poco de agua.',
                        'fuente': fu(DZP_C, '4.2 Posología y forma de administración')},
        ajusteRenalHepatico={'renal': 'Usar con precaución; iniciar con 2-2,5 mg 1-2 veces al día por posible acumulación de metabolitos.',
                             'hepatico': 'Contraindicado en insuficiencia hepática grave. En insuficiencia leve a moderada reducir la dosis al 50 %.',
                             'fuente': fu(DZP_C, '4.2 Pacientes con insuficiencia renal y/o hepática y 4.3 Contraindicaciones')},
        alto_riesgo=True,
        discrepancias=discrepancias_,
        alertas=['Medicamento de alto riesgo (benzodiacepina): riesgo de tolerancia, dependencia física/psíquica y depresión respiratoria.',
                 'Contraindicado en miastenia gravis, insuficiencia respiratoria grave, síndrome de apnea del sueño e insuficiencia hepática grave.'],
        comerciales=['Valium', 'Diazepam Cinfa'],
    )


# ================================================================ §7 Vitaminas y hierro
def acido_folico():
    P = _ped('acido-folico', anio=2022)
    presentaciones = [
        pres('comprimido-1-mg', 'comprimido', mg=1, partible='no',
             fuente=fu(ARSENAL, 'Grupo 08.01: Ácido Fólico, Comprimido 1 mg (adecuado para dosificación pediátrica)')),
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='no',
             fuente=fu(FOL, 'Acfol 5 mg comprimidos; el arsenal de APS lista comprimido 5 mg')),
    ]
    dosis_ = [
        dosis('Tratamiento de estados carenciales y anemia megaloblástica (adultos)', 'adulto', 'fija', 'mg',
              min=5, max=15, tomas=1, intervalo_h=24, tope_dia=(15, 'mg'),
              condicion='1 a 3 comprimidos de 5 mg diarios (5-15 mg/día) en 1 o 2 tomas. '
                        'En anemia megaloblástica por déficit de folato: 5 mg/día durante 4 meses',
              texto='5-15 mg/día en 1-2 tomas diarias (habitual 5 mg/día durante 4 meses)',
              presentaciones=['comprimido-5-mg'],
              fuente=fu(FOL, '4.2 Tratamiento de estados carenciales: "1 a 3 comprimidos diarios (5-15 mg de ácido fólico) en 1-2 tomas al día ... '
                             'anemia megaloblástica folato-deficiente se recomienda una dosis de 5 mg/dia durante 4 meses; puede ser necesario hasta 15mg"')),
        dosis('Prevención de defectos del tubo neural (mujeres en edad fértil con deseo de gestación)', 'adulto', 'fija', 'mg',
              min=5, max=5, tomas=1, intervalo_h=24, tope_dia=(5, 'mg'),
              condicion='1 comprimido de 5 mg al día durante 4 semanas antes de la concepción y los 3 primeros meses de gestación',
              texto='5 mg una vez al día desde 4 semanas antes de la concepción y hasta la semana 12 de gestación',
              presentaciones=['comprimido-5-mg'],
              fuente=fu(FOL, '4.2 Prevención de defectos en el tubo neural: "1 comprimido al día durante cuatro semanas antes de la concepción '
                             'y los tres primeros meses de gestación"')),
        dosis('Deficiencia de ácido fólico (niños y adolescentes)', 'pediatrico', 'fija', 'mg', min=1, max=1, tomas=1,
              intervalo_h=24, tope_dia=(1, 'mg'),
              condicion='1 mg al día por vía oral hasta la resolución de la deficiencia, independientemente de la edad. '
                        'No utilizar el comprimido de 5 mg en niños (usar la presentación de 1 mg del arsenal)',
              texto='1 mg/día vía oral en toma única hasta resolución de la carencia',
              presentaciones=['comprimido-1-mg'],
              fuente=fu(P, 'Dosificación: "La dosificación recomendada en caso de deficiencia de ácido fólico es de 1 mg/día (vía oral) '
                           'hasta la resolución de la deficiencia, independientemente de la edad"')),
    ]
    discrepancias_ = [
        discrepancia('Dosis en estados carenciales (adultos vs niños)',
                     [(FOL, 'Adultos: 5-15 mg/día (comprimidos de 5 mg)'),
                      (P, 'Niños: 1 mg/día independiente de la edad')],
                     '1 mg/día en pediatría / 5 mg/día en adultos',
                     'CIMA sólo dispone de la presentación de 5 mg con pauta adulta de 5-15 mg/día; '
                     'en pediatría la dosis de consenso es de 1 mg/día (respaldada por el comprimido de 1 mg del arsenal chileno). '
                     'No debe administrarse el comprimido de 5 mg a pacientes pediátricos.')
    ]
    return ficha_oral(
        'acido-folico', 'Ácido fólico', 'vitamina-mineral', presentaciones, dosis_,
        administracion={'comida': 'antes',
                        'texto': 'Administrar preferiblemente antes de las comidas con agua (el pico de absorción se alcanza a los 30-60 minutos).',
                        'fuente': fu(FOL, '4.2 Forma de administración y Pediamécum')},
        discrepancias=discrepancias_,
        alertas=['No usar la presentación de 5 mg para dosis pediátricas: utilizar el comprimido de 1 mg del arsenal chileno de APS.',
                 'El ácido fólico puede enmascarar una anemia perniciosa por déficit de vitamina B12 (el daño neurológico puede progresar).'],
        comerciales=['Acfol', 'Ácido Fólico'],
    )


def sulfato_ferroso():
    P = _ped('sulfato-ferroso', slug='sulfato-ferroso-y-glicina-sulfato-ferroso', anio=2020)
    presentaciones = [
        pres('comprimido-retard-80-mg-fe', 'comprimido', mg=80, partible='no', retard=True,
             elemental={'valor': 80, 'unidad': 'mg', 'de': 'hierro elemental'},
             fuente=fu(FER_T, 'Tardyferon 80 mg comprimidos de liberación prolongada (equivalente a 80 mg de hierro elemental)')),
        pres('comprimido-retard-105-mg-fe', 'comprimido', mg=105, partible='no', retard=True,
             elemental={'valor': 105, 'unidad': 'mg', 'de': 'hierro elemental'},
             fuente=fu(FER_F, 'Fero-Gradumet 105 mg comprimidos de liberación prolongada (equivalente a 105 mg de hierro elemental)')),
        pres('gotas-25-mg-ml-fe', 'gotas', mg_ml=25, gotas_por_ml=20,
             elemental={'valor': 25, 'unidad': 'mg', 'de': 'hierro elemental por ml'},
             fuente=fu(ARSENAL, 'Grupo 08.01: Ferroso sulfato, Solución para gotas orales 125 mg/mL '
                                '(equivalente a 25 mg/mL de hierro elemental; 20 gotas = 25 mg Fe; 1 gota = 1,25 mg Fe elemental)')),
    ]
    dosis_ = [
        dosis('Anemia ferropénica leve y prevención (adultos y niños ≥28 kg)', 'adulto', 'fija', 'mg', min=80, max=105,
              tomas=1, intervalo_h=24,
              condicion='1 comprimido de liberación prolongada al día (80 a 105 mg de hierro elemental). '
                        'No superar la dosis diaria de 5 mg Fe²⁺/kg de peso corporal. No usar comprimidos retard en <28 kg',
              texto='1 comprimido diario (80-105 mg Fe elemental/día) en ayunas; máximo 5 mg Fe elemental/kg/día',
              presentaciones=['comprimido-retard-80-mg-fe', 'comprimido-retard-105-mg-fe'],
              fuente=fu(FER_T, '4.2 Posología: "Anemias ferropénicas leves ... 1 comprimido recubierto una vez al día ... '
                               'En todo caso no debe superarse la dosis diaria de 5 mg Fe2+/kg de peso corporal ... '
                               'No debe administrarse a niños con peso inferior a 28 kg"')),
        dosis('Anemia ferropénica grave con Hb <8-9 g/dl (adultos)', 'adulto', 'fija', 'mg', min=160, max=210, tomas=2,
              intervalo_h=12,
              condicion='1 comprimido por la mañana y otro por la tarde durante unas 3 semanas, y a continuación 1 comprimido diario',
              texto='1 comprimido c/12 h (160-210 mg Fe elemental/día) durante 3 semanas, luego 1 diario',
              presentaciones=['comprimido-retard-80-mg-fe', 'comprimido-retard-105-mg-fe'],
              fuente=fu(FER_T, '4.2 Posología: "Anemias ferropénicas graves, con menos de 8 a 9 g/dl de hemoglobina: '
                               '1 comprimido recubierto por la mañana y otro por la tarde, durante unas 3 semanas, y a continuación 1 comprimido diario"')),
        dosis('Tratamiento de anemia ferropénica leve a moderada (lactantes y niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=3, max=3, tomas=2, intervalo_h=12,
              condicion='3 mg/kg/día de hierro elemental divididos en 1 o 2 tomas en ayunas. '
                        'Para lactantes y niños usar la formulación en gotas',
              texto='3 mg Fe elemental/kg/día en 1-2 tomas diarias en ayunas',
              presentaciones=['gotas-25-mg-ml-fe'],
              fuente=fu(P, 'Tratamiento de anemia: "Leve a moderada: 3 mg/kg/día de hierro elemental divididos en 1-2 dosis"')),
        dosis('Tratamiento de anemia ferropénica grave (lactantes y niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=4, max=6, tomas=3, intervalo_h=8,
              condicion='4 a 6 mg/kg/día de hierro elemental divididos en 3 tomas diarias en ayunas',
              texto='4-6 mg Fe elemental/kg/día en 3 tomas diarias en ayunas',
              presentaciones=['gotas-25-mg-ml-fe'],
              fuente=fu(P, 'Tratamiento de anemia: "Grave: 4-6 mg/kg/día de hierro elemental divididos en 3 dosis"')),
        dosis('Prevención de deficiencia de hierro en lactantes y niños', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=1, max=2, tomas=1, intervalo_h=24,
              condicion='1 a 2 mg/kg/día de hierro elemental en toma única. Pretérminos pueden requerir 2-4 mg/kg/día',
              texto='1-2 mg Fe elemental/kg/día en toma única diaria',
              presentaciones=['gotas-25-mg-ml-fe'],
              fuente=fu(P, 'Prevención de la deficiencia de hierro: "Lactantes >4 meses ... 1 mg/kg/día de hierro elemental ... '
                           'desde 6 meses a 5 años ... 2 mg/kg/día de hierro elemental"')),
    ]
    discrepancias_ = [
        discrepancia('Presentaciones retard en pediatría',
                     [(FER_T, 'Contraindicado en niños con peso inferior a 28 kg (aproximadamente menores de 9-10 años)'),
                      (P, 'Dosis pediátricas calculadas en mg de hierro elemental desde el periodo neonatal')],
                     'Dosificación en hierro elemental con gotas orales en <28 kg',
                     'Los comprimidos retard contienen dosis altas (80-105 mg Fe) no fraccionables; '
                     'en lactantes y niños <28 kg debe emplearse estrictamente la formulación en gotas.')
    ]
    return ficha_oral(
        'sulfato-ferroso', 'Sulfato ferroso', 'vitamina-mineral', presentaciones, dosis_,
        administracion={'comida': 'antes',
                        'texto': 'Administrar con agua o zumo de cítricos (la vitamina C favorece la absorción), en ayunas, '
                                 '1 hora antes o 3 horas después de las comidas. NUNCA administrar con leche, productos lácteos, té o café. '
                                 'Los comprimidos de liberación prolongada deben tragarse enteros sin masticar ni chupar.',
                        'noTriturar': True,
                        'fuente': fu(FER_T, '4.2 Forma de administración y Pediamécum')},
        discrepancias=discrepancias_,
        alertas=['Dosificación expresada en mg de HIERRO ELEMENTAL (Fe²+): 125 mg de sulfato ferroso heptahidratado equivalen a ~25 mg de Fe elemental.',
                 'Los comprimidos retard no deben masticarse ni disolverse en la boca por riesgo de ulceración oral y pigmentación dental.',
                 'Sobredosis aguda de hierro en niños es potencialmente mortal: mantener fuera del alcance de los niños.'],
        comerciales=['Tardyferon', 'Fero-Gradumet'],
    )


def fichas():
    return {
        'carbamazepina': carbamazepina(),
        'acido-valproico': acido_valproico(),
        'clonazepam': clonazepam(),
        'fenobarbital': fenobarbital(),
        'lamotrigina': lamotrigina(),
        'levetiracetam': levetiracetam(),
        'fenitoina': fenitoina(),
        'sertralina': sertralina(),
        'fluoxetina': fluoxetina(),
        'escitalopram': escitalopram(),
        'amitriptilina': amitriptilina(),
        'mirtazapina': mirtazapina(),
        'venlafaxina': venlafaxina(),
        'quetiapina': quetiapina(),
        'haloperidol': haloperidol(),
        'risperidona': risperidona(),
        'zopiclona': zopiclona(),
        'diazepam': diazepam(),
        'acido-folico': acido_folico(),
        'sulfato-ferroso': sulfato_ferroso(),
    }
