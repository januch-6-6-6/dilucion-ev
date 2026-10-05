"""Orales, tanda 2: cardiovascular, digestivo y endocrino (28 fichas).

Cada cifra sale de datos/crudos/orales/ (fichas CIMA, Pediamécum, DailyMed, guía MINSAL de hipotiroidismo y arsenal
de APS de Atacama); la tabla «cifra → archivo:línea» está en .superpowers/sdd/2026-10-05-orales-v1/task-13-report.md.

Convenciones de esta tanda (mismas que 12a/12b):
- Rangos de dosis de la fuente → `min`/`max`; topes y frecuencias con rango → extremo conservador, dicho en `condicion`.
- Dosis diaria (`base='dia'`) con «1 o 2 tomas» → se cargan 2 tomas (toma más pequeña). Si la fuente da la dosis
  diaria sin decir cuántas tomas, se carga una toma diaria y la `condicion` lo dice.
- `topeDiario` de adulto solo cuando la fuente lo declara como máximo (nunca toma × tomas).
"""
from .comun import (ARSENAL, discrepancia, dosis, ficha_oral, fu, fuente_arsenal, fuente_cima, fuente_externa,
                    fuente_pediamecum_oral, pres)


def _ped(k):
    return f'PEDIAMECUM-{k.upper()}'


def _pres_mcg(id, forma, mcg, *, partible='no', fuente):
    """Comprimido dosificado en microgramos (pres() solo admite mg)."""
    p = pres(id, forma, mg=mcg, partible=partible, fuente=fuente)
    p['cantidad'] = {'valor': mcg, 'unidad': 'mcg'}
    return p


# ---------------------------------------------------------------- referencias
ENA = 'CIMA-ENALAPRIL'  # Enalapril Cinfa 10 mg
CAP = 'CIMA-CAPTOPRIL'  # Captopril Cinfa 25 mg
LOS = 'CIMA-LOSARTAN'  # Cozaar 100 mg
AML = 'CIMA-AMLODIPINO'  # Amlodipino Cinfa 10 mg
ATE = 'CIMA-ATENOLOL'  # Atenolol Cinfa 100 mg
PRO_C = 'CIMA-PROPRANOLOL-77174'  # Propranolol Accord 10 mg
PRO_H = 'CIMA-PROPRANOLOL-114919001'  # Hemangiol 3,75 mg/ml solución oral
CAR = 'CIMA-CARVEDILOL'  # Carvedilol Cinfa 25 mg
MDO = 'CIMA-METILDOPA'  # Aldomet Forte 500 mg
HCT = 'DAILYMED-HIDROCLOROTIAZIDA'  # Hydrochlorothiazide tablets USP (A-S Medication Solutions)
FUR = 'CIMA-FUROSEMIDA'  # Furosemida Cinfa 40 mg
ESP = 'CIMA-ESPIRONOLACTONA'  # Aldactone 100 mg
AAS = 'CIMA-ACIDO-ACETILSALICILICO'  # Aspirina 500 mg
ATO = 'CIMA-ATORVASTATINA'  # Atorvastatina Cinfa 10 mg
GEM = 'CIMA-GEMFIBROZILO'  # Gemfibrozilo Stada 600 mg
ISO = 'CIMA-ISOSORBIDE'  # Mononitrato de isosorbida Normon 20 mg
OME = 'CIMA-OMEPRAZOL'  # Gastromel 20 mg (venta libre)
FAM = 'CIMA-FAMOTIDINA'  # Famotidina Cinfa 20 mg
MET_S = 'CIMA-METOCLOPRAMIDA-69266'  # Metoclopramida Kern Pharma 1 mg/ml solución oral
MET_C = 'CIMA-METOCLOPRAMIDA-75665'  # Metoclopramida Accord 10 mg
OND = 'CIMA-ONDANSETRON'  # Ondansetrón Normon 4 mg
DOM_S = 'CIMA-DOMPERIDONA-55411'  # Motilium 1 mg/ml suspensión oral
DOM_C = 'CIMA-DOMPERIDONA-57096'  # Domperidona Gamir 10 mg cápsulas
LAC = 'CIMA-LACTULOSA'  # Duphalac 10 g solución oral en sobre (la ficha incluye la solución 667 mg/ml)
MTF = 'CIMA-METFORMINA'  # Dianben 850 mg
GLI = 'DAILYMED-GLIBENCLAMIDA'  # Glyburide tablets USP 1.25, 2.5 y 5 mg (Teva)
VIL = 'CIMA-VILDAGLIPTINA'  # Galvus 50 mg
EMP = 'CIMA-EMPAGLIFLOZINA'  # Jardiance 10 mg
LEV = 'CIMA-LEVOTIROXINA'  # Eutirox 100 microgramos
MINSAL_HIPO = 'MINSAL-HIPOTIROIDISMO-2020'
LNG = 'CIMA-LEVONORGESTREL'  # Levonorgestrel Exeltis 1,5 mg

DAILYMED = 'U.S. FDA / DailyMed'


def fuentes():
    return [
        fuente_cima('enalapril', '73300', 'Enalapril Cinfa 10 mg comprimidos'),
        fuente_pediamecum_oral('enalapril', 'Enalapril', anio=2022),
        fuente_cima('captopril', '62304', 'Captopril Cinfa 25 mg comprimidos EFG'),
        fuente_pediamecum_oral('captopril', 'Captopril', anio=2022),
        fuente_cima('losartan', '64971', 'Cozaar 100 mg comprimidos recubiertos con película'),
        fuente_pediamecum_oral('losartan', 'Losartán', anio=2020),
        fuente_cima('amlodipino', '65461', 'Amlodipino Cinfa 10 mg comprimidos EFG'),
        fuente_pediamecum_oral('amlodipino', 'Amlodipino', anio=2022),
        fuente_cima('atenolol', '63146', 'Atenolol Cinfa 100 mg comprimidos EFG'),
        fuente_pediamecum_oral('atenolol', 'Atenolol', anio=2021),
        fuente_cima('propranolol', '77174', 'Propranolol Accord 10 mg comprimidos recubiertos con película EFG', varios=True),
        fuente_cima('propranolol', '114919001', 'Hemangiol 3,75 mg/ml solución oral', varios=True),
        fuente_pediamecum_oral('propranolol', 'Propranolol', anio=2021),
        fuente_cima('carvedilol', '68328', 'Carvedilol Cinfa 25 mg comprimidos EFG'),
        fuente_pediamecum_oral('carvedilol', 'Carvedilol', anio=2020),
        fuente_cima('metildopa', '53587', 'Aldomet Forte 500 mg comprimidos recubiertos con película'),
        fuente_pediamecum_oral('metildopa', 'Metildopa', anio=2020),
        fuente_externa(HCT, 'Hydrochlorothiazide Tablets, USP (A-S Medication Solutions), prospecto de EE. UU.', DAILYMED,
                       'https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=hydrochlorothiazide+tablets', 2026),
        fuente_pediamecum_oral('hidroclorotiazida', 'Hidroclorotiazida', anio=2022),
        fuente_cima('furosemida', '64140', 'Furosemida Cinfa 40 mg comprimidos EFG'),
        fuente_pediamecum_oral('furosemida', 'Furosemida', anio=2025),
        fuente_cima('espironolactona', '54900', 'Aldactone 100 mg comprimidos recubiertos con película'),
        fuente_pediamecum_oral('espironolactona', 'Espironolactona', anio=2020),
        fuente_cima('acido-acetilsalicilico', '2011', 'Aspirina 500 mg comprimidos'),
        fuente_pediamecum_oral('acido-acetilsalicilico', 'Ácido acetilsalicílico (AAS)', anio=2023, slug='acido-acetilsalicilico-aas'),
        fuente_cima('atorvastatina', '69534', 'Atorvastatina Cinfa 10 mg comprimidos recubiertos con película EFG'),
        fuente_pediamecum_oral('atorvastatina', 'Atorvastatina', anio=2020),
        fuente_cima('gemfibrozilo', '61830', 'Gemfibrozilo Stada 600 mg comprimidos EFG'),
        fuente_cima('isosorbide', '63396', 'Mononitrato de isosorbida Normon 20 mg comprimidos EFG'),
        fuente_cima('omeprazol', '64004', 'Gastromel 20 mg cápsulas duras gastrorresistentes EFG'),
        fuente_pediamecum_oral('omeprazol', 'Omeprazol', anio=2020),
        fuente_cima('famotidina', '63319', 'Famotidina Cinfa 20 mg comprimidos recubiertos con película EFG'),
        fuente_pediamecum_oral('famotidina', 'Famotidina', anio=2020),
        fuente_cima('metoclopramida', '69266', 'Metoclopramida Kern Pharma 1 mg/ml solución oral EFG', varios=True),
        fuente_cima('metoclopramida', '75665', 'Metoclopramida Accord 10 mg comprimidos EFG', varios=True),
        fuente_pediamecum_oral('metoclopramida', 'Metoclopramida', anio=2020),
        fuente_cima('ondansetron', '69378', 'Ondansetrón Normon 4 mg comprimidos recubiertos con película EFG'),
        fuente_pediamecum_oral('ondansetron', 'Ondansetrón', anio=2020),
        fuente_cima('domperidona', '55411', 'Motilium 1 mg/ml suspensión oral', varios=True),
        fuente_cima('domperidona', '57096', 'Domperidona Gamir 10 mg cápsulas duras', varios=True),
        fuente_pediamecum_oral('domperidona', 'Domperidona', anio=2020),
        fuente_pediamecum_oral('trimebutino', 'Trimebutina', anio=2021, slug='trimebutina'),
        fuente_cima('lactulosa', '60189', 'Duphalac 10 g solución oral en sobre'),
        fuente_pediamecum_oral('lactulosa', 'Lactulosa', anio=2020),
        fuente_cima('metformina', '55211', 'Dianben 850 mg comprimidos recubiertos con película'),
        fuente_pediamecum_oral('metformina', 'Metformina', anio=2021),
        fuente_externa(GLI, 'Glyburide Tablets USP 1.25, 2.5 and 5 mg (Teva Pharmaceuticals USA), prospecto de EE. UU.', DAILYMED,
                       'https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=glyburide+tablets+teva', 2026),
        fuente_pediamecum_oral('glibenclamida', 'Glibenclamida', anio=2020),
        fuente_cima('vildagliptina', '07414005', 'Galvus 50 mg comprimidos'),
        fuente_cima('empagliflozina', '114930014', 'Jardiance 10 mg comprimidos recubiertos con película'),
        fuente_cima('levotiroxina', '64014', 'Eutirox 100 microgramos comprimidos'),
        fuente_pediamecum_oral('levotiroxina', 'Levotiroxina sódica', anio=2022, slug='levotiroxina-sodica'),
        fuente_externa(MINSAL_HIPO, 'Resumen ejecutivo Guía de Práctica Clínica Hipotiroidismo en personas de 15 años y más',
                       'Ministerio de Salud de Chile',
                       'http://diprece.minsal.cl/le-informamos/auge/acceso-guias-clinicas/guias-clinicas-desarrolladas-utilizando-manual-metodologico/',
                       2020),
        fuente_cima('levonorgestrel', '78873', 'Levonorgestrel Exeltis 1,5 mg comprimido EFG'),
        fuente_pediamecum_oral('levonorgestrel', 'Levonorgestrel', anio=2020),
        fuente_arsenal(),
    ]


SIN_TOPE_PED = 'La fuente no da tope pediátrico en mg para esta pauta por kg'


# ================================================================ §3 cardiovascular
def enalapril():
    P = _ped('enalapril')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(ENA, 'Enalapril Cinfa 10 mg comprimidos (la ficha no menciona ranura ni partición); el arsenal de APS lista 10 mg')),
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ENALAPRIL CINFA 5 mg COMPRIMIDOS EFG (no se indica si es partible)')),
        pres('comprimido-20-mg', 'comprimido', mg=20, partible='no',
             fuente=fu(ARSENAL, 'Grupo 11.03: Enalapril, Comprimido 10 mg y 20 mg (Pediamécum también lista ENALAPRIL CINFA 20 mg)')),
    ]
    dosis_ = [
        dosis('Hipertensión (adultos)', 'adulto', 'fija', 'mg', min=5, max=20, tomas=1, intervalo_h=24, tope_dia=(40, 'mg'),
              condicion='Hipertensión leve: inicio 5-10 mg; con sistema renina-angiotensina muy activo o tras diuréticos: 5 mg o menos',
              texto='Inicio 5 hasta un máximo de 20 mg una vez al día; mantenimiento habitual 20 mg/día; máximo de mantenimiento 40 mg/día',
              fuente=fu(ENA, '4.2.1 Hipertensión: "La dosificación inicial es de 5 hasta un máximo de 20 mg ... una vez al día ... '
                             'La dosis máxima de mantenimiento es 40 mg al día"')),
        dosis('Insuficiencia cardíaca o disfunción ventricular izquierda asintomática (adultos)', 'adulto', 'fija', 'mg', min=2.5,
              max=2.5, tomas=1, intervalo_h=24, tope_dia=(40, 'mg'),
              condicion='Inicio bajo estrecha supervisión; aumento gradual en 2-4 semanas',
              texto='Inicio 2,5 mg/día (días 1-3); días 4-7: 5 mg/día en dos tomas; semana 2: 10 mg/día; semanas 3-4: 20 mg/día en una o dos '
                    'tomas; máximo 40 mg/día en dos tomas',
              fuente=fu(ENA, '4.2.1: "La dosis inicial ... es de 2,5 mg" y Tabla 1; "La dosis máxima es de 40 mg al día administrada en dos tomas"')),
        dosis('Hipertensión (niños ≥6 años de 20 a <50 kg que puedan tragar comprimidos)', 'pediatrico', 'fija', 'mg', min=2.5, max=2.5,
              tomas=1, intervalo_h=24, tope_dia=(20, 'mg'),
              condicion='No recomendado en recién nacidos ni en niños con filtración glomerular <30 ml/min/1,73 m²',
              texto='Inicio 2,5 mg una vez al día; ajustar hasta un máximo de 20 mg/día',
              fuente=fu(ENA, '4.2.1 Población pediátrica: "La dosis inicial recomendada es de 2,5 mg en pacientes de 20 a < 50 kg ... '
                             'hasta un máximo de 20 mg al día en pacientes de 20 a < 50 kg"')),
        dosis('Hipertensión (niños ≥6 años y ≥50 kg)', 'pediatrico', 'fija', 'mg', min=5, max=5, tomas=1, intervalo_h=24, tope_dia=(40, 'mg'),
              condicion='No recomendado con filtración glomerular <30 ml/min/1,73 m²',
              texto='Inicio 5 mg una vez al día; ajustar hasta un máximo de 40 mg/día',
              fuente=fu(P, 'Niños >6 años con peso ≥20 kg (A): "Dosis inicial ... 5 mg en pacientes >50 kg ... hasta un máximo de ... 40 mg en '
                           'pacientes >50 kg" (igual que CIMA 73300, 4.2.1)')),
        dosis('Hipertensión (niños >1 mes, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=0.08, tomas=1,
              intervalo_h=24, tope_dia=(5, 'mg'), estatus='off_label',
              condicion='Dosis inicial; ajustar según la presión arterial. No se han estudiado dosis >0,58 mg/kg/día (o >40 mg). '
                        'Una toma diaria (Pediamécum: "Vía oral una vez al día")',
              texto='0,08 mg/kg/día (dosis máxima: 5 mg)',
              fuente=fu(P, 'Niños >1 mes (E: off-label): "dosis iniciales de 0,08 mg/kg/día (dosis máxima: 5 mg)"')),
        dosis('Proteinuria y síndrome nefrótico (niños y adolescentes, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='dia',
              min=0.2, max=0.6, tomas=1, intervalo_h=24, tope_dia=(20, 'mg'), estatus='off_label',
              condicion='Inicio 0,2 mg/kg/día, escalando cada 4-12 semanas; datos limitados. Una toma diaria (Pediamécum: "Vía oral una vez al día")',
              texto='0,2-0,6 mg/kg/día (máximo: 20 mg/día)',
              fuente=fu(P, 'Proteinuria y síndrome nefrótico: "dosis inicial de 0,2 mg/kg/día ... rango: 0,2-0,6 mg/kg/día (máximo: 20 mg/día)"')),
    ]
    alertas = [
        'La dosis de 2,5 mg (inicio en insuficiencia cardíaca y en niños de 20 a <50 kg) no se puede obtener con los comprimidos cargados '
        '(5, 10 y 20 mg, sin ranura declarada): haría falta medio comprimido de 5 mg partible o una presentación de 2,5 mg.',
        'Contraindicado en el segundo y tercer trimestre del embarazo, con antecedente de angioedema por IECA y en angioedema hereditario o '
        'idiopático; no combinar con sacubitrilo/valsartán (36 h de separación) (CIMA, 4.3).',
        'Riesgo de hipotensión sintomática tras la primera dosis si hay depleción de volumen (diuréticos, restricción de sal, diálisis, '
        'diarrea o vómitos) (CIMA, 4.4).',
    ]
    return ficha_oral(
        'enalapril', 'Enalapril', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral. Los alimentos no afectan la absorción de enalapril (CIMA). Pediamécum: una vez al día, independientemente de las comidas.',
            'fuente': fu(ENA, '4.2.2 Forma de administración: "Los alimentos no afectan la absorción de enalapril"'),
        },
        comerciales=['Enalapril Cinfa'],
        renal='Dosis inicial según aclaramiento de creatinina: 30-80 ml/min, 5-10 mg/día; 10-30 ml/min, 2,5 mg/día; ≤10 ml/min, 2,5 mg los '
              'días de diálisis. En general, prolongar el intervalo y/o reducir la dosis. Ancianos: adecuar a la función renal.',
        fuente_ajuste=fu(ENA, '4.2.1 Insuficiencia renal, Tabla 2'),
        alertas=alertas,
    )


def captopril():
    P = _ped('captopril')
    presentaciones = [
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='cuartos',
             fuente=fu(CAP, '4.2: "Los comprimidos de captopril presentan unas ranuras que permiten un fraccionamiento ... para ajustar la '
                            'dosis" (la propia ficha usa 6,25 y 12,5 mg con el comprimido de 25 mg); el arsenal de APS lista 25 mg')),
    ]
    dosis_ = [
        dosis('Hipertensión (adultos)', 'adulto', 'fija', 'mg', base='dia', min=25, max=50, tomas=2, intervalo_h=12, tope_dia=(150, 'mg'),
              condicion='Con sistema renina-angiotensina muy activo: empezar con 6,25 o 12,5 mg en dosis única. Aumentos cada ≥2 semanas',
              texto='Inicio 25-50 mg/día en dos dosis; hasta 100-150 mg/día en dos dosis; dosis máxima diaria recomendada 150 mg',
              fuente=fu(CAP, '4.2: "La dosis máxima diaria recomendada es de 150 mg"; Hipertensión: "25-50 mg al día administrada en dos dosis"')),
        dosis('Insuficiencia cardíaca (adultos)', 'adulto', 'fija', 'mg', min=6.25, max=12.5, tomas=2, intervalo_h=12, tope_dia=(150, 'mg'),
              condicion='Inicio bajo estrecha supervisión; dos o tres veces al día (se carga el extremo conservador: dos tomas)',
              texto='Inicio 6,25-12,5 mg dos o tres veces al día; mantenimiento 75-150 mg/día; máximo 150 mg/día en dos dosis',
              fuente=fu(CAP, '4.2 Insuficiencia cardíaca: "6,25 mg - 12,5 mg dos veces al día (BID) o tres veces al día (TID) ... hasta un '
                             'máximo de 150 mg al día"')),
        dosis('Hipertensión (niños y adolescentes, dosis inicial de la ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=0.3,
              tomas=3, intervalo_h=8,
              condicion='Solo si otras medidas no han sido efectivas; inicio bajo estrecha supervisión. Eficacia y seguridad no establecidas por completo',
              texto='0,30 mg/kg por toma, generalmente 3 veces al día',
              fuente=fu(CAP, '4.2 Población pediátrica: "La dosis inicial de captopril es de 0,30 mg/kg de peso ... generalmente captopril se '
                             'administra 3 veces al día"')),
        dosis('Hipertensión (prematuros, recién nacidos, niños de corta edad o con disfunción renal)', 'pediatrico', 'por_peso', 'mg/kg',
              base='toma', max=0.15, tomas=3, intervalo_h=8,
              condicion='Inicio bajo estrecha supervisión; neonatos más susceptibles a hipotensión, oliguria y convulsiones',
              texto='0,15 mg/kg por toma',
              fuente=fu(CAP, '4.2 Población pediátrica: "la dosis inicial debe ser de solamente 0,15 mg de captopril/kg de peso"')),
        dosis('Hipertensión (niños y adolescentes, pauta de otras publicaciones)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', min=0.3,
              max=0.5, tomas=3, intervalo_h=8, tope_dia=(450, 'mg'), estatus='off_label',
              condicion='Pediamécum la toma de otras publicaciones (la ficha solo da 0,30 y 0,15 mg/kg). Máximo 6 mg/kg/día. La calculadora '
                        'aplica además el tope de adulto (150 mg/día)',
              texto='0,3-0,5 mg/kg cada 8 h (máximo 6 mg/kg/día; dosis diaria máxima 450 mg)',
              fuente=fu(P, 'Hipertensión, niños y adolescentes: "0,3-0,5 mg/kg/8 h ... (máximo 6 mg/kg/día ...; dosis diaria máxima: 450 mg)"')),
    ]
    disc = [
        discrepancia('Tope diario',
                     [(CAP, '150 mg/día: dosis máxima diaria recomendada de la ficha (adultos)'),
                      (P, '450 mg/día: hipertensión en niños y adolescentes (otras publicaciones; en insuficiencia cardíaca, 150 mg/día)')],
                     '150 mg/día como tope de adulto (la calculadora lo aplica también a las pautas pediátricas por peso)',
                     'Regla del tope más bajo. La pauta pediátrica de Pediamécum conserva su propio máximo de 450 mg/día, pero la calculadora '
                     'limita además al tope de adulto de la ficha.'),
        discrepancia('Relación con las comidas',
                     [(CAP, 'Antes, durante y después de las comidas (CIMA)'),
                      (P, 'Una hora antes de las comidas o dos horas después: el alimento dificulta la absorción (Pediamécum)')],
                     'Se muestran ambas indicaciones',
                     'La ficha técnica permite tomarlo con comida; Pediamécum recomienda separarlo de las comidas.'),
    ]
    alertas = [
        'Las pautas por kg de la ficha (0,30 y 0,15 mg/kg) no traen tope pediátrico en mg; como referencia, la dosis máxima diaria del adulto es '
        '150 mg (CIMA) y la calculadora limita a ese tope.',
        'Contraindicado en el segundo y tercer trimestre del embarazo y con antecedente de angioedema por IECA (CIMA, 4.3).',
    ]
    return ficha_oral(
        'captopril', 'Captopril', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Captopril se puede tomar antes, durante y después de las comidas; los comprimidos ranurados se pueden fraccionar y las '
                     'fracciones se guardan en lugar seco (CIMA). Pediamécum recomienda 1 h antes o 2 h después de comer.',
            'fuente': fu(CAP, '4.2 Forma de administración'),
        },
        comerciales=['Captopril Cinfa'], discrepancias=disc,
        renal='Dosis diaria según aclaramiento (ml/min/1,73 m²): >40, inicio 25-50 mg y máximo 150 mg; 21-40, inicio 25 y máximo 100 mg; '
              '10-20, inicio 12,5 y máximo 75 mg; <10, inicio 6,25 y máximo 37,5 mg. Ancianos: iniciar con 6,25 mg dos veces al día.',
        fuente_ajuste=fu(CAP, '4.2 Insuficiencia renal (tabla) y personas de edad avanzada'),
        alertas=alertas,
    )


def losartan():
    P = _ped('losartan')
    presentaciones = [
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(LOS, 'Cozaar 100 mg; 4.2.2: "Los comprimidos de losartán se deben tragar enteros"')),
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: COZAAR 50 mg COMPRIMIDOS RECUBIERTOS CON PELICULA (el arsenal de APS lista 50 mg)')),
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: LOSARTAN NORMON 25 mg COMPRIMIDOS RECUBIERTOS CON PELICULA')),
        pres('comprimido-12-5-mg', 'comprimido', mg=12.5, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: COZAAR 12.5 mg INICIO COMPRIMIDOS RECUBIERTOS CON PELICULA')),
    ]
    dosis_ = [
        dosis('Hipertensión (adultos)', 'adulto', 'fija', 'mg', min=50, max=50, tomas=1, intervalo_h=24,
              condicion='Depleción de volumen: considerar 25 mg; >75 años: valorar iniciar con 25 mg',
              texto='50 mg una vez al día (inicio y mantenimiento); algunos pacientes, 100 mg una vez al día por la mañana',
              fuente=fu(LOS, '4.2.1 Hipertensión: "La dosis habitual de inicio y de mantenimiento es de 50 mg una vez al día ... aumentando la '
                             'dosis a 100 mg una vez al día"')),
        dosis('Insuficiencia cardíaca (adultos)', 'adulto', 'fija', 'mg', min=12.5, max=12.5, tomas=1, intervalo_h=24, tope_dia=(150, 'mg'),
              texto='Inicio 12,5 mg una vez al día; aumentar a intervalos semanales (25, 50, 100 mg/día) hasta un máximo de 150 mg/día',
              fuente=fu(LOS, '4.2.1 Insuficiencia cardiaca: "12,5 mg una vez al día ... hasta una dosis máxima de 150 mg al día"')),
        dosis('Hipertensión (6-18 años, >20 a <50 kg)', 'pediatrico', 'fija', 'mg', min=25, max=25, tomas=1, intervalo_h=24, tope_dia=(50, 'mg'),
              condicion='Pacientes que pueden tragar comprimidos; hasta 50 mg una vez al día solo en casos excepcionales',
              texto='25 mg una vez al día (máximo 50 mg una vez al día en casos excepcionales)',
              fuente=fu(LOS, '4.2.1 6 a 18 años: "la dosis recomendada es 25 mg una vez al día en pacientes de >20 a <50 kg ... hasta un máximo '
                             'de 50 mg una vez al día"')),
        dosis('Hipertensión (6-18 años, >50 kg)', 'pediatrico', 'fija', 'mg', min=50, max=50, tomas=1, intervalo_h=24, tope_dia=(100, 'mg'),
              condicion='Hasta 100 mg una vez al día solo en casos excepcionales; no estudiadas dosis >1,4 mg/kg/día (o >100 mg)',
              texto='50 mg una vez al día (máximo 100 mg una vez al día en casos excepcionales)',
              fuente=fu(P, 'Hipertensión arterial (A): "Pacientes de más de 50 kg: 50 mg ... una vez al día ... hasta un máximo de 100 mg una vez '
                           'al día" (igual que CIMA 64971, 4.2.1)')),
        dosis('Hipertensión (6-16 años, dosis por peso)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=0.7, tomas=1, intervalo_h=24,
              tope_dia=(50, 'mg'), estatus='off_label',
              condicion='Pediamécum: "según distintas fuentes de datos, no ficha técnica". Máximo 50 mg/día hasta conseguir el efecto '
                        '(máximo absoluto 1,4 mg/kg/día o 100 mg/día). Una vez al día o cada 12 h (se carga una toma)',
              texto='0,7 mg/kg/día, máximo 50 mg/día',
              fuente=fu(P, 'Dosis ajustada por edad: "6-16 años: 0,7 mg/kg/día, máximo 50 mg/día hasta conseguir el efecto"')),
    ]
    alertas = [
        'No recomendado en niños <6 años, con filtración glomerular <30 ml/min/1,73 m² ni con insuficiencia hepática (CIMA, 4.2).',
        'Contraindicado en el segundo y tercer trimestre del embarazo y en insuficiencia hepática grave (CIMA, 4.3).',
    ]
    return ficha_oral(
        'losartan', 'Losartán', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Tragar los comprimidos enteros con un vaso de agua, con o sin alimentos (CIMA).',
            'noTriturar': True,
            'fuente': fu(LOS, '4.2.2 Forma de administración'),
        },
        comerciales=['Cozaar'],
        renal='No es necesario ajustar la dosis inicial en insuficiencia renal ni en hemodiálisis (adultos).',
        hepatico='Con antecedentes de insuficiencia hepática, considerar una dosis menor; contraindicado en insuficiencia hepática grave.',
        fuente_ajuste=fu(LOS, '4.2.1 Poblaciones especiales'),
        alertas=alertas,
    )


def amlodipino():
    P = _ped('amlodipino')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(AML, 'Amlodipino Cinfa 10 mg (la ficha no menciona partición); el arsenal de APS lista 5 y 10 mg')),
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: AMLODIPINO CINFA 5 mg COMPRIMIDOS EFG')),
    ]
    dosis_ = [
        dosis('Hipertensión y angina (adultos)', 'adulto', 'fija', 'mg', min=5, max=5, tomas=1, intervalo_h=24, tope_dia=(10, 'mg'),
              texto='Inicio 5 mg una vez al día; puede aumentarse hasta una dosis máxima de 10 mg',
              fuente=fu(AML, '4.2 Adultos: "la dosis inicial recomendada es 5 mg ... una vez al día, que puede aumentarse hasta una dosis máxima de 10 mg"')),
        dosis('Hipertensión (6-17 años)', 'pediatrico', 'fija', 'mg', min=2.5, max=2.5, tomas=1, intervalo_h=24, tope_dia=(5, 'mg'),
              condicion='Subir a 5 mg una vez al día si no se alcanza el objetivo tras 4 semanas; no se han estudiado dosis >5 mg/día',
              texto='2,5 mg una vez al día; 5 mg una vez al día tras 4 semanas si hace falta',
              fuente=fu(P, '6-17 años (A): "2,5 mg / 1 vez al día, como dosis inicial, elevándola hasta 5 mg / 1 vez al día" (igual que CIMA 65461)')),
        dosis('Hipertensión (niños <6 años, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=0.05, max=0.1, tomas=1,
              intervalo_h=24, tope_dia=(5, 'mg'), estatus='off_label',
              condicion='Dosis de inicio, preferentemente en dosis única (pueden precisar cada 12 h); máximo 0,6 mg/kg/día. La ficha: "No hay datos disponibles" en <6 años',
              texto='0,05-0,1 mg/kg/día (dosis máxima 0,6 mg/kg/día; máximo 5 mg/día)',
              fuente=fu(P, 'Niños <6 años: "0,05-0,1 mg/kg/día (dosis máxima: 0,6 mg/kg/día; máximo: 5 mg/día), preferentemente en dosis única"')),
    ]
    disc = [
        discrepancia('Dosis máxima en 6-17 años',
                     [(AML, '5 mg diarios: no se han estudiado dosis superiores en pacientes pediátricos (CIMA)'),
                      (P, '10 mg/día: "Hay estudios con una dosis máxima de hasta 10 mg/día"; >5 mg/día es off-label (Pediamécum)')],
                     '5 mg/día',
                     'Regla del tope más bajo para la misma población y pauta.'),
    ]
    alertas = [
        'La dosis de 2,5 mg requiere medio comprimido de 5 mg y ninguna fuente dice que sea partible: haría falta una presentación de 2,5 mg o '
        'confirmar la ranura del producto.',
        'Contraindicado en hipotensión grave, shock, estenosis aórtica grave e insuficiencia cardíaca inestable tras infarto agudo (CIMA, 4.3).',
    ]
    return ficha_oral(
        'amlodipino', 'Amlodipino', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Comprimido para administración oral (CIMA). Pediamécum: oral, con o sin comidas.',
            'fuente': fu(P, 'Administración: "oral, con o sin comidas"'),
        },
        comerciales=['Amlodipino Cinfa'], discrepancias=disc,
        renal='No se correlaciona con el grado de insuficiencia renal: dosis normales; no es dializable.',
        hepatico='Insuficiencia hepática: empezar con el rango inferior de la dosis; en insuficiencia hepática grave, iniciar con la dosis más baja y ajustar lentamente.',
        fuente_ajuste=fu(AML, '4.2 Poblaciones especiales'),
        alertas=alertas,
    )


def atenolol():
    P = _ped('atenolol')
    presentaciones = [
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(ATE, 'Atenolol Cinfa 100 mg (la ficha no menciona partición); el arsenal de APS lista 50 y 100 mg')),
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ATENOLOL CINFA 50 mg COMPRIMIDOS EFG')),
    ]
    dosis_ = [
        dosis('Hipertensión arterial esencial (adultos)', 'adulto', 'fija', 'mg', min=50, max=50, tomas=1, intervalo_h=24,
              texto='50 mg al día; si la respuesta no es suficiente, hasta 100 mg',
              fuente=fu(ATE, '4.2 Hipertensión: "La dosis inicial es de 50 mg al día ... se puede incrementar la dosis hasta 100 mg"')),
        dosis('Angina de pecho (adultos)', 'adulto', 'fija', 'mg', min=100, max=100, tomas=1, intervalo_h=24,
              texto='100 mg en una dosis única o en dos dosis de 50 mg al día',
              fuente=fu(ATE, '4.2 Angina de pecho: "100 mg en una dosis única oral o en dos dosis de 50 mg al día"')),
        dosis('Hipertensión y arritmias (niños, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=0.5, max=1, tomas=2,
              intervalo_h=12, tope_dia=(100, 'mg'), estatus='off_label',
              condicion='En una o dos dosis (se cargan dos). Dosis máxima 2 mg/kg/día; no exceder 100 mg/día (máximo oral del adulto). '
                        'La ficha técnica no lo recomienda en niños',
              texto='0,5-1 mg/kg/día en una o dos dosis; máximo 2 mg/kg/día sin superar 100 mg',
              fuente=fu(P, 'Hipertensión y arritmias, vía oral: "0,5-1 mg/kg/día repartido en una o dos dosis. Dosis máxima, 2 mg/kg/día. No exceder '
                           'la dosis oral máxima diaria de adultos de 100 mg"')),
    ]
    disc = [
        discrepancia('Uso en niños',
                     [(ATE, 'No se ha establecido la seguridad y eficacia en niños: no se recomienda su empleo (CIMA)'),
                      (P, 'Todas las indicaciones pediátricas son off-label, con pauta por peso (Pediamécum)')],
                     'Se muestra la pauta de Pediamécum como uso fuera de ficha técnica (off-label)',
                     'Discrepancia de población: la ficha no lo recomienda en niños.'),
    ]
    alertas = [
        'Contraindicado en bradicardia, shock cardiogénico, hipotensión, acidosis metabólica, bloqueo cardíaco de 2.º o 3.er grado, '
        'síndrome del seno enfermo, feocromocitoma no tratado e insuficiencia cardíaca no controlada (CIMA, 4.3).',
    ]
    return ficha_oral(
        'atenolol', 'Atenolol', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral (la ficha CIMA no indica relación con las comidas). Pediamécum: separar de los alimentos al menos 30 minutos.',
            'fuente': fu(ATE, '4.2 Forma de administración: "Vía oral"'),
        },
        comerciales=['Atenolol Cinfa'], discrepancias=disc,
        renal='Aclaramiento de creatinina 15-35 ml/min/1,73 m²: 50 mg/día; <15 ml/min/1,73 m²: 25 mg al día o 50 mg en días alternos; '
              'hemodiálisis: 50 mg tras cada diálisis, en medio hospitalario. Ancianos: considerar reducir la dosis. '
              'Pediamécum (niños): filtrado 30-50, 0,5-1 mg/kg; <30, 0,5-1 mg/kg cada 48 h.',
        fuente_ajuste=fu(ATE, '4.2 Pacientes con insuficiencia renal (la frase pediátrica es de Pediamécum)'),
        alertas=alertas,
    )


def propranolol():
    P = _ped('propranolol')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(PRO_C, 'Propranolol Accord 10 mg; Pediamécum: "Los comprimidos de propanolol deben tragarse enteros"; el arsenal lista 10 y 40 mg')),
        pres('comprimido-40-mg', 'comprimido', mg=40, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: PROPRANOLOL ACCORD 40 MG COMPRIMIDOS RECUBIERTOS CON PELICULA EFG')),
        pres('solucion-3-75-mg-ml', 'jarabe', mg_ml=3.75,
             fuente=fu(PRO_H, 'Hemangiol 3,75 mg/ml solución oral (posología expresada como propranolol base; jeringa oral en mg)')),
    ]
    comp = ['comprimido-10-mg', 'comprimido-40-mg']
    dosis_ = [
        dosis('Hipertensión (adultos)', 'adulto', 'fija', 'mg', min=40, max=40, tomas=2, intervalo_h=12, presentaciones=comp,
              condicion='Dos o tres veces al día (se cargan dos tomas). Aumentos semanales; intervalo habitual 160-320 mg/día',
              texto='Inicio 40 mg dos o tres veces al día; habitual 160-320 mg al día',
              fuente=fu(PRO_C, '4.2 Hipertensión: "Inicialmente, 40 mg dos o tres veces al día ... El intervalo de dosis habitual es de entre 160 y 320 mg al día"')),
        dosis('Angina de pecho, migraña y temblor esencial (adultos)', 'adulto', 'fija', 'mg', min=40, max=40, tomas=2, intervalo_h=12,
              presentaciones=comp,
              condicion='Dos o tres veces al día (se cargan dos tomas). Migraña: 80-160 mg/día; angina y temblor: 120-240 mg/día',
              texto='Inicio 40 mg dos o tres veces al día, con aumentos semanales',
              fuente=fu(PRO_C, '4.2 Angina de pecho, migraña y temblor esencial: "La dosis inicial es de 40 mg dos o tres veces al día"')),
        dosis('Arritmias, miocardiopatía obstructiva hipertrófica y tirotoxicosis (adultos)', 'adulto', 'fija', 'mg', min=10, max=40, tomas=3,
              intervalo_h=8, presentaciones=comp, condicion='Tres o cuatro veces al día (se cargan tres tomas)',
              texto='10-40 mg tres o cuatro veces al día',
              fuente=fu(PRO_C, '4.2: "un intervalo de dosis entre 10 y 40 mg tres o cuatro veces al día"')),
        dosis('Arritmias (niños y adolescentes)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', min=0.25, max=0.5, tomas=3, intervalo_h=8,
              tope_dia=(160, 'mg'), presentaciones=comp,
              condicion='Tres o cuatro veces al día (se cargan tres tomas), ajustado a la respuesta; máximo 1 mg/kg 4 veces al día sin exceder 160 mg/día',
              texto='0,25-0,5 mg/kg 3-4 veces al día; dosis máxima total 160 mg al día',
              fuente=fu(P, 'Arritmias, vía oral: "0,25-0,5 mg/kg, 3 o 4 veces al día ... no excediéndose una dosis máxima total de 160 mg al día" '
                           '(la pauta coincide con CIMA 77174, 4.2 Población pediátrica)')),
        dosis('Migraña (niños menores de 12 años)', 'pediatrico', 'fija', 'mg', min=20, max=20, tomas=2, intervalo_h=12, presentaciones=comp,
              condicion='Dos o tres veces al día (se cargan dos tomas). Mayores de 12 años: dosis de adultos',
              texto='20 mg dos o tres veces al día',
              fuente=fu(PRO_C, '4.2 Población pediátrica, Migraña: "Niños menores de 12 años: 20 mg dos o tres veces al día"')),
        dosis('Hemangioma infantil proliferativo (lactantes de 5 semanas a 5 meses)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=1,
              max=3, tomas=2, presentaciones=['solucion-3-75-mg-ml'],
              condicion='Solo Hemangiol, iniciado por un médico experto en un contexto clínico controlado. 1 mg/kg/día la 1.ª semana, 2 mg/kg/día '
                        'la 2.ª y 3 mg/kg/día de mantenimiento, en 2 tomas con al menos 9 h de intervalo, durante o justo después de la toma de alimento; 6 meses',
              texto='1 → 2 → 3 mg/kg/día en dos dosis separadas (mantenimiento 1,5 mg/kg dos veces al día)',
              fuente=fu(PRO_H, '4.2: "La dosis inicial recomendada es de 1 mg/kg/día, administrada en dos dosis ... 3 mg/kg/día como dosis de mantenimiento"')),
        dosis('Hipertensión (niños, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=0.5, max=1, tomas=4,
              intervalo_h=6, estatus='off_label', presentaciones=comp,
              condicion='Formulaciones de liberación inmediata, cada 6-12 h (se cargan cuatro tomas). Incrementar cada 5-7 días; habitual '
                        '1-5 mg/kg/día; máximo 8 mg/kg/día',
              texto='Inicio 0,5-1 mg/kg/día cada 6-12 horas (máximo 8 mg/kg/día)',
              fuente=fu(P, 'Hipertensión: "dosis inicial de 0,5-1 mg/kg/día, cada 6-12 horas ... dosis máxima: 8 mg/kg/día"')),
    ]
    alertas = [
        'Hemangiol y la pauta de hipertensión infantil no traen tope en mg (solo mg/kg); como referencia, en adultos la hipertensión usa 160-320 mg/día '
        '(CIMA 77174). La ficha no declara un máximo diario de adulto que la calculadora pueda aplicar.',
        'No existe una pauta pediátrica única: la dosis depende de la indicación (arritmias, migraña, hemangioma, hipertensión).',
        'Contraindicado en asma o broncoespasmo, bloqueo AV de 2.º-3.er grado, bradicardia intensa, hipotensión grave, shock cardiogénico y '
        'en pacientes propensos a hipoglucemia (CIMA 77174 y 114919001, 4.3). Hemangiol: no en lactantes <5 semanas.',
        'No suspender bruscamente: reducir la dosis en 7-14 días (CIMA 77174).',
    ]
    return ficha_oral(
        'propranolol', 'Propranolol', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Vía oral (CIMA 77174). Pediamécum: con comida; los comprimidos se tragan enteros con líquido, sin masticar. Hemangiol: con la '
                     'jeringa oral del envase, durante o justo después de la alimentación del niño para evitar hipoglucemia; puede mezclarse con '
                     'un poco de leche infantil o zumo (CIMA 114919001).',
            'noTriturar': True,
            'fuente': fu(P, 'Administración: "Por vía oral, debe administrarse con comida"; arritmias: "deben tragarse enteros con líquido y no deben masticar"'),
        },
        comerciales=['Propranolol Accord', 'Hemangiol'],
        renal='Insuficiencia renal significativa o hemodiálisis: precaución al iniciar y al elegir la dosis inicial.',
        hepatico='Hepatopatía grave (p. ej., cirrosis): dosis inicial baja, sin superar 20 mg tres veces al día, vigilando la respuesta.',
        fuente_ajuste=fu(PRO_C, '4.2 Insuficiencia hepática / renal'),
        alertas=alertas,
    )


def carvedilol():
    P = _ped('carvedilol')
    presentaciones = [
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no',
             fuente=fu(CAR, 'Carvedilol Cinfa 25 mg (la ficha no dice que el de 25 mg sea partible); el arsenal lista 6,25 y 25 mg')),
        pres('comprimido-6-25-mg', 'comprimido', mg=6.25, partible='mitades',
             fuente=fu(CAR, '4.2.1: "3,125 mg (medio comprimido de 6,25 mg)"; Pediamécum lista CARVEDILOL CINFA 6,25 mg COMPRIMIDOS EFG')),
    ]
    dosis_ = [
        dosis('Hipertensión esencial (adultos)', 'adulto', 'fija', 'mg', min=12.5, max=25, tomas=1, intervalo_h=24, tope_dia=(50, 'mg'),
              condicion='12,5 mg/día los dos primeros días y luego 25 mg/día; aumentos cada ≥2 semanas',
              texto='12,5 mg una vez al día 2 días; después 25 mg una vez al día; máximo 50 mg una vez al día o en dos dosis',
              fuente=fu(CAR, '4.2.1 Hipertensión, adultos: "12,5 mg una vez al día durante los dos primeros días ... 25 mg una vez al día ... '
                             'dosis máxima recomendada de 50 mg"')),
        dosis('Cardiopatía isquémica (adultos)', 'adulto', 'fija', 'mg', min=12.5, max=25, tomas=2, intervalo_h=12, tope_dia=(100, 'mg'),
              condicion='12,5 mg dos veces al día los dos primeros días y luego 25 mg dos veces al día. Ancianos: máximo 50 mg/día en dos dosis',
              texto='12,5 → 25 mg dos veces al día; máximo 100 mg/día en dos dosis',
              fuente=fu(CAR, '4.2.1 Cardiopatía isquémica: "12,5 mg dos veces al día ... 25 mg dos veces al día ... máxima recomendada de 100 mg"')),
        dosis('Insuficiencia cardíaca congestiva (adultos)', 'adulto', 'fija', 'mg', min=3.125, max=3.125, tomas=2, intervalo_h=12,
              tope_toma=(25, 'mg'), tope_dia=(50, 'mg'),
              condicion='Inicio 3,125 mg (medio comprimido de 6,25 mg) dos veces al día 2 semanas; subir cada ≥2 semanas a 6,25, 12,5 y 25 mg dos '
                        'veces al día. Tope cargado: 25 mg dos veces al día (<85 kg); con >85 kg la ficha permite 50 mg dos veces al día',
              texto='3,125 mg dos veces al día, con escalada hasta el máximo tolerado',
              fuente=fu(CAR, '4.2.1 Insuficiencia cardiaca: "3,125 mg (medio comprimido de 6,25 mg) dos veces al día ... inferior a 85 kg, la '
                             'dosis máxima recomendada es de 25 mg dos veces al día"')),
        dosis('Hipertensión e insuficiencia cardíaca (lactantes y niños <12 años, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg',
              base='toma', min=0.05, max=0.1, tomas=2, intervalo_h=12, tope_toma=(3.125, 'mg'), estatus='off_label',
              condicion='Dosis de inicio (máxima inicial 3,125 mg/12 h); subir cada 1-2 semanas 0,1 mg/kg hasta un máximo de 0,5-0,8 mg/kg/12 h '
                        '(máximo 25 mg/12 h). Fuentes muy variables. La ficha: no establecido en <18 años',
              texto='0,05-0,1 mg/kg cada 12 h (dosis máxima inicial 3,125 mg/12 h)',
              fuente=fu(P, 'Lactantes y niños <12 años: "empezar con 0,05-0,1 mg/kg/12 h (dosis máxima inicial 3,125 mg/12 h)"')),
        dosis('Hipertensión (niños >12 años, uso fuera de ficha)', 'pediatrico', 'fija', 'mg', min=12.5, max=25, tomas=1, intervalo_h=24,
              tope_toma=(25, 'mg'), tope_dia=(50, 'mg'), estatus='off_label',
              condicion='12,5 mg/día los 2 primeros días, después 25 mg una vez al día; máximo 25 mg/12 h. La ficha: no establecido en <18 años',
              texto='12,5 → 25 mg una vez al día; máximo 25 mg cada 12 h',
              fuente=fu(P, 'Niños >12 años: "En hipertensión arterial (HTA) ... 12,5 mg una vez al día durante los 2 primeros días ... 25 mg una vez '
                           'al día ... Máximo 25 mg/12 h"')),
    ]
    disc = [
        discrepancia('Uso en menores de 18 años',
                     [(CAR, 'No se ha establecido la seguridad y eficacia en niños y adolescentes menores de 18 años (CIMA)'),
                      (P, 'Pautas off-label con variabilidad importante entre fuentes (Pediamécum)')],
                     'Se muestran las pautas de Pediamécum como uso fuera de ficha técnica (off-label)',
                     'Discrepancia de población: la ficha no establece su uso en <18 años.'),
    ]
    alertas = [
        'Contraindicado en disfunción hepática clínicamente manifiesta, asma bronquial, EPOC con broncoespasmo, insuficiencia cardíaca NYHA IV '
        'descompensada, bloqueo AV de 2.º-3.er grado, bradicardia grave (<50 lpm), shock cardiogénico e hipotensión grave (CIMA, 4.3).',
        'No suspender bruscamente; si se interrumpe más de una semana, reiniciar con 3,125 mg dos veces al día (CIMA).',
    ]
    return ficha_oral(
        'carvedilol', 'Carvedilol', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Con suficiente líquido. No es necesario tomarlo con comida, salvo en insuficiencia cardíaca congestiva, en la que debe tomarse '
                     'con alimentos para reducir los efectos ortostáticos (CIMA).',
            'fuente': fu(CAR, '4.2.2 Forma de administración'),
        },
        comerciales=['Carvedilol Cinfa'], discrepancias=disc,
        renal='No hay evidencia de que haga falta ajustar la dosis; vigilar la función renal con insuficiencia cardíaca y presión arterial baja.',
        hepatico='Contraindicado en disfunción hepática clínicamente manifiesta.',
        fuente_ajuste=fu(CAR, '4.2.1 Insuficiencia renal / Disfunción hepática'),
        alertas=alertas,
    )


def metildopa():
    P = _ped('metildopa')
    presentaciones = [
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='no', fuente=fu(MDO, 'Aldomet Forte 500 mg (la ficha no menciona partición)')),
        pres('comprimido-250-mg', 'comprimido', mg=250, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ALDOMET 250 MG COMPRIMIDOS RECUBIERTOS CON PELÍCULA (el arsenal de APS lista 250 mg)')),
    ]
    dosis_ = [
        dosis('Hipertensión (adultos)', 'adulto', 'fija', 'mg', min=250, max=250, tomas=2, intervalo_h=12, tope_dia=(3000, 'mg'),
              condicion='Dos o tres veces al día durante las primeras 48 h (se cargan dos tomas); ajustar cada ≥2 días. Tras otros antihipertensivos, '
                        'inicio ≤500 mg/día. Mayores de 65 años: inicio ≤250 mg/día (p. ej., 125 mg dos veces al día) y máximo 2 g/día',
              texto='250 mg dos o tres veces al día; dosis máxima diaria recomendada 3 g',
              fuente=fu(MDO, '4.2 Adultos: "250 mg dos o tres veces al día durante las primeras 48 horas ... La dosis máxima diaria recomendada es de 3 g"')),
        dosis('Hipertensión (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=10, tomas=4, intervalo_h=6, tope_dia=(3000, 'mg'),
              condicion='Dividida en 2-4 dosis (se cargan cuatro). Aumentar cada 2 días; máximo 65 mg/kg/día o 3 g/día, la que resulte menor',
              texto='Inicio 10 mg/kg/día en 2-4 dosis; máximo 65 mg/kg/día o 3 g/día',
              fuente=fu(P, 'Oral: "dosis inicial de 10 mg/kg/día, dividida en 2-4 dosis ... hasta un máximo de 65 mg/kg/día. Dosis máxima: 3 g/día" '
                           '(la ficha CIMA 53587 da la misma pauta en 4.2 Población pediátrica)')),
    ]
    alertas = [
        'La dosis de 125 mg de los mayores de 65 años no se puede obtener con los comprimidos cargados (250 y 500 mg, sin ranura declarada).',
        'Contraindicado en enfermedad hepática activa, depresión, tratamiento con IMAO, feocromocitoma o paraganglioma y porfiria (CIMA, 4.3).',
        'Somnolencia al inicio y al subir la dosis: aumentar primero la dosis de la noche (CIMA).',
    ]
    return ficha_oral(
        'metildopa', 'Metildopa', 'antihipertensivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral (CIMA). Pediamécum: puede administrarse con o sin alimentos; aumentar la dosis por las noches para minimizar la sedación diurna.',
            'fuente': fu(P, 'Administración: "Oral: puede administrarse con o sin alimentos"'),
        },
        comerciales=['Aldomet'],
        renal='Los pacientes con insuficiencia renal pueden responder a dosis menores (CIMA). Pediamécum: aclaramiento 10-50 ml/min, dosis normal '
              'cada 8-12 h; <10 ml/min, cada 12-24 h.',
        fuente_ajuste=fu(MDO, '4.2 Pacientes con insuficiencia renal (la tabla de intervalos es de Pediamécum)'),
        alertas=alertas,
    )


def hidroclorotiazida():
    P = _ped('hidroclorotiazida')
    presentaciones = [
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(HCT, 'DESCRIPTION: "Each tablet ... contains 12.5 mg, 25 mg and 50 mg"; el arsenal de APS lista 50 mg (no se indica ranura)')),
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no', fuente=fu(HCT, 'DESCRIPTION: comprimidos de 12.5, 25 y 50 mg')),
        pres('comprimido-12-5-mg', 'comprimido', mg=12.5, partible='no', fuente=fu(HCT, 'DESCRIPTION: comprimidos de 12.5, 25 y 50 mg')),
    ]
    dosis_ = [
        dosis('Hipertensión (adultos)', 'adulto', 'fija', 'mg', min=25, max=25, tomas=1, intervalo_h=24,
              condicion='Se puede subir a 50 mg/día en una o dos dosis; por encima de 50 mg aumenta mucho la pérdida de potasio',
              texto='Inicio 25 mg al día en dosis única; hasta 50 mg al día',
              fuente=fu(HCT, 'DOSAGE AND ADMINISTRATION, Control of Hypertension: "The usual initial dose in adults is 25 mg daily given as a single dose"')),
        dosis('Edema (adultos)', 'adulto', 'fija', 'mg', base='dia', min=25, max=100, tomas=2, intervalo_h=12,
              condicion='En dosis única o dividida (se cargan dos tomas); puede usarse en días alternos o 3-5 días por semana',
              texto='25-100 mg al día',
              fuente=fu(HCT, 'DOSAGE AND ADMINISTRATION, For Edema: "25mg to 100 mg daily as a single or divided dose"')),
        dosis('Diuresis e hipertensión (lactantes hasta 2 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=1, max=2, tomas=2,
              intervalo_h=12, tope_dia=(37.5, 'mg'),
              condicion='En una o dos dosis (se cargan dos). Menores de 6 meses pueden requerir hasta 3 mg/kg/día en dos dosis. '
                        'Pediamécum: sin indicación pediátrica aprobada en España',
              texto='1-2 mg/kg/día; sin exceder 37,5 mg/día',
              fuente=fu(HCT, 'Infants and Children: "1 to 2 mg/kg per day in single or two divided doses, not to exceed 37.5 mg per day in infants up to 2 years"')),
        dosis('Hipertensión y edema (niños de 2 a 12 años)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=1, max=2, tomas=2, intervalo_h=12,
              tope_dia=(100, 'mg'),
              condicion='En una o dos dosis (se cargan dos). Autorizada en el prospecto de EE. UU. (DailyMed: 100 mg/día en 2-12 años); '
                        'Pediamécum la considera off-label en España y da el mismo máximo para niños y adolescentes',
              texto='1-2 mg/kg/día en 1 o 2 dosis; máximo 100 mg/día',
              fuente=fu(P, 'Hipertensión: "de 1 a 2 mg/kg por vía oral en 1 o 2 dosis"; Dosis máxima: "Niños y adolescentes: 100 mg/día"')),
    ]
    disc = [
        discrepancia('Estatus pediátrico',
                     [(HCT, 'El prospecto de EE. UU. da pauta pediátrica basada en uso empírico y literatura publicada (sin ensayos controlados)'),
                      (P, 'Sin ninguna indicación aprobada en población pediátrica en España: off-label (Pediamécum)')],
                     'Se muestra la pauta pediátrica como autorizada por la ficha de EE. UU.',
                     'Las cifras coinciden (1-2 mg/kg/día; 37,5 y 100 mg/día); difiere el estatus regulatorio entre países.'),
    ]
    alertas = [
        'Fuente de dosis extranjera (prospecto de la FDA de EE. UU., DailyMed): no hay ficha técnica CIMA de hidroclorotiazida sola.',
        'Riesgo de cáncer de piel no melanoma: protegerse del sol y hacer controles periódicos de la piel (DailyMed).',
        'No dar con litio; contraindicado en anuria y en alergia a sulfonamidas; riesgo de miopía aguda y glaucoma de ángulo cerrado (DailyMed).',
        'Vigilar electrolitos (hipopotasemia, hiponatremia, hipomagnesemia), glucemia y ácido úrico (DailyMed).',
    ]
    return ficha_oral(
        'hidroclorotiazida', 'Hidroclorotiazida', 'diuretico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral, con o sin comida (Pediamécum). El prospecto de EE. UU. no indica relación con las comidas.',
            'fuente': fu(P, 'Administración: "se puede administrar con o sin comida"'),
        },
        discrepancias=disc,
        renal='Usar con precaución en enfermedad renal grave: puede precipitar azotemia; si aparece deterioro renal progresivo, considerar suspenderla. '
              'Pediamécum: con aclaramiento <30 ml/min puede no ser efectiva.',
        hepatico='Precaución en insuficiencia hepática o enfermedad hepática progresiva (pequeños cambios hidroelectrolíticos pueden precipitar coma hepático).',
        fuente_ajuste=fu(HCT, 'WARNINGS y PRECAUTIONS (la frase de aclaramiento <30 es de Pediamécum)'),
        alertas=alertas,
    )


def furosemida():
    P = _ped('furosemida')
    presentaciones = [
        pres('comprimido-40-mg', 'comprimido', mg=40, partible='mitades',
             fuente=fu(FUR, 'Furosemida Cinfa 40 mg; 4.2: "iniciar el tratamiento con medio, uno o dos comprimidos" (el arsenal de APS lista 40 mg)')),
    ]
    dosis_ = [
        dosis('Edema e hipertensión (adultos, mantenimiento)', 'adulto', 'fija', 'mg', base='dia', min=20, max=40, tomas=1, intervalo_h=24,
              condicion='Inicio: medio, uno o dos comprimidos diarios (20-80 mg); la dosis máxima depende de la respuesta diurética. La ficha no dice '
                        'en cuántas tomas: se carga una toma diaria',
              texto='Mantenimiento: medio a un comprimido (20-40 mg) al día',
              fuente=fu(FUR, '4.2 Adultos: "La dosis de mantenimiento es de medio a un comprimido al día"')),
        dosis('Edema (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=2, tomas=1, intervalo_h=24, tope_dia=(40, 'mg'),
              condicion='La ficha da la dosis diaria sin número de tomas: se carga una toma diaria',
              texto='2 mg/kg al día, hasta un máximo de 40 mg por día',
              fuente=fu(FUR, '4.2 Población pediátrica: "2 mg/kg de peso corporal, hasta un máximo de 40 mg por día de furosemida por vía oral"')),
        dosis('Uso crónico (lactantes y niños)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', min=0.5, max=2, tomas=1, intervalo_h=24,
              tope_toma=(20, 'mg'), tope_dia=(40, 'mg'),
              condicion='Cada 6-24 h (se carga cada 24 h); sin superar 20-40 mg por dosis (se carga 20). Tope diario de la ficha CIMA (40 mg/día): '
                        'Pediamécum permite subir hasta 6 mg/kg/día y 600 mg/día',
              texto='0,5-2 mg/kg/dosis (sin superar 20-40 mg/dosis) cada 6-24 horas',
              fuente=fu(P, 'Lactantes y niños, oral, uso crónico: "inicialmente, 0,5-2 mg/kg/dosis (sin superar 20-40 mg/dosis) cada 6-24 horas"')),
    ]
    disc = [
        discrepancia('Tope diario pediátrico',
                     [(FUR, '40 mg por día de furosemida por vía oral (CIMA, niños)'),
                      (P, '600 mg/día: uso crónico, subiendo hasta 6 mg/kg/día (Pediamécum); uso agudo hasta 6 mg/kg/dosis y 200 mg/dosis')],
                     '40 mg/día',
                     'Regla del tope más bajo para la misma población y vía; es la mayor diferencia del bloque cardiovascular.'),
    ]
    alertas = [
        'Contraindicado en hipovolemia o deshidratación, anuria que no responde, hipopotasemia o hiponatremia graves, encefalopatía hepática '
        '(precoma o coma) y lactancia; posible sensibilidad cruzada con sulfonamidas (CIMA, 4.3).',
    ]
    return ficha_oral(
        'furosemida', 'Furosemida', 'diuretico', presentaciones, dosis_,
        {
            'comida': 'ayunas',
            'texto': 'Con el estómago vacío; tragar sin masticar con suficiente líquido (CIMA). Pediamécum indica, en cambio, preferiblemente con comidas.',
            'noTriturar': True,
            'fuente': fu(FUR, '4.2 Forma de administración: "con el estómago vacío ... sin masticar"'),
        },
        comerciales=['Furosemida Cinfa'], discrepancias=disc,
        renal='Pediamécum: no precisa ajuste; evitar en insuficiencia renal anúrica (la ficha CIMA la contraindica en anuria que no responde).',
        hepatico='Pediamécum: no precisa ajuste; vigilar estrechamente en cirróticos (hipopotasemia, depleción de volumen).',
        fuente_ajuste=fu(P, 'Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def espironolactona():
    P = _ped('espironolactona')
    presentaciones = [
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(ESP, 'Aldactone 100 mg; Pediamécum: "Los comprimidos no deben manipularse" (NIOSH grupo 2)')),
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ALDACTONE 25 mg COMPRIMIDOS RECUBIERTOS CON PELICULA (el arsenal de APS lista 25 mg)')),
    ]
    dosis_ = [
        dosis('Hipertensión arterial esencial (adultos)', 'adulto', 'fija', 'mg', base='dia', min=50, max=100, tomas=1, intervalo_h=24,
              condicion='En casos graves, subir gradualmente hasta 200 mg/día cada dos semanas. La ficha no dice en cuántas tomas: se carga una toma diaria',
              texto='Inicio 50-100 mg al día',
              fuente=fu(ESP, '4.2.1: "La dosis inicial habitual es de 50-100 mg al día, que en los casos más graves podrá aumentarse ... hasta los 200 mg"')),
        dosis('Insuficiencia cardíaca grave NYHA III-IV (adultos)', 'adulto', 'fija', 'mg', min=25, max=25, tomas=1, intervalo_h=24,
              condicion='Con potasio ≤5,0 mmol/l y creatinina ≤2,5 mg/dl; se puede subir a 50 mg una vez al día o bajar a 25 mg en días alternos. '
                        'La dosis no debe superar 50 mg al día (no se carga como tope para que no limite las pautas de otras indicaciones)',
              texto='25 mg una vez al día (máximo 50 mg al día)',
              fuente=fu(ESP, '4.2.1 Insuficiencia cardíaca grave: "25 mg una vez al día ... no debe ser superior a 50 mg al día"')),
        dosis('Edemas y edema asociado a insuficiencia cardíaca crónica (hiperaldosteronismo secundario, adultos)', 'adulto', 'fija', 'mg',
              base='dia', min=100, max=100, tomas=1, intervalo_h=24,
              condicion='Casos graves: hasta 400 mg/día; mantenimiento 25-200 mg/día. La ficha no dice en cuántas tomas: se carga una toma diaria',
              texto='100 mg al día',
              fuente=fu(ESP, '4.2.1 Hiperaldosteronismo secundario: "La dosis habitual ... es de 100 mg al día"')),
        dosis('Diurético e hipertensión arterial (niños)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', min=1, max=3, tomas=2, intervalo_h=12,
              tope_dia=(100, 'mg'),
              condicion='Solo bajo supervisión de un pediatra (datos limitados). En 1-2 dosis (se cargan dos). Autorizada en la ficha CIMA '
                        '("1-3 mg/kg ... en tomas separadas"); Pediamécum la considera off-label y fija el máximo de 100 mg/día',
              texto='1-3 mg/kg/día en 1-2 dosis; dosis máxima 100 mg diarios',
              fuente=fu(P, 'Como diurético y en hipertensión arterial en niños: "1-3 mg/kg/día en 1-2 dosis. Dosis máxima 100 mg diarios"')),
    ]
    alertas = [
        'Fármaco peligroso (lista NIOSH grupo 2): no partir, triturar ni manipular los comprimidos (Pediamécum).',
        'Contraindicada en insuficiencia renal moderada a grave (adultos y niños), insuficiencia renal aguda, anuria, hiperpotasemia, '
        'enfermedad de Addison y con eplerenona (CIMA, 4.3).',
        'El tope de 100 mg/día es pediátrico (Pediamécum); la ficha no da tope en mg para niños.',
    ]
    return ficha_oral(
        'espironolactona', 'Espironolactona', 'diuretico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral. Ninguna de las dos fuentes indica relación con las comidas. Los comprimidos no deben manipularse (NIOSH grupo 2; '
                     'consultar al Servicio de Farmacia).',
            'noTriturar': True,
            'fuente': fu(P, 'Administración: "Los comprimidos no deben manipularse, consultar al Servicio de Farmacia"'),
        },
        comerciales=['Aldactone'],
        renal='Insuficiencia renal leve: 25 mg al día; moderada: 25 mg en días alternos, siempre con potasio <5,0 mmol/l. Contraindicada en '
              'insuficiencia renal moderada a grave según 4.3. Ancianos: 25 mg al día o en días alternos.',
        fuente_ajuste=fu(ESP, '4.2.1 Población con insuficiencia renal / de edad avanzada; 4.3'),
        alertas=alertas,
    )


def acido_acetilsalicilico():
    P = _ped('acido-acetilsalicilico')
    presentaciones = [
        pres('comprimido-500-mg', 'comprimido', mg=500, partible='no', fuente=fu(AAS, 'Aspirina 500 mg comprimidos (la ficha no menciona partición)')),
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(ARSENAL, 'Grupo 11.05: Ácido acetilsalicílico, Comprimido 100 mg (Pediamécum lista ADIRO 100 MG COMPRIMIDOS GASTRORRESISTENTES)')),
    ]
    dosis_ = [
        dosis('Dolor leve o moderado y fiebre (adultos y adolescentes >16 años)', 'adulto', 'fija', 'mg', min=500, max=500, tomas=6, intervalo_h=4,
              tope_dia=(4000, 'mg'), presentaciones=['comprimido-500-mg'],
              condicion='Repetir solo si es necesario y tras un mínimo de 4 h; dolor >5 días o fiebre >3 días: reevaluar',
              texto='1 comprimido (500 mg); repetir en caso necesario tras un mínimo de 4 h; no exceder 4000 mg en 24 h',
              fuente=fu(AAS, '4.2: "1 comprimido (500 mg de ácido acetilsalicílico), repetir ... después de un periodo mínimo de 4 horas. No se excederá '
                             'de 4000 mg en 24 horas"')),
        dosis('Antiagregante plaquetario (>16 años)', 'adulto', 'fija', 'mg', base='dia', min=100, max=300, tomas=1, intervalo_h=24,
              condicion='Pediamécum no indica el número de tomas: se carga una toma diaria. El efecto antitrombótico dura más de 7 días',
              texto='100-300 mg/día',
              fuente=fu(P, 'Uso clínico: antiagregante "en >16 años (A)"; Dosis: "Tratamiento antiagregante: 100-300 mg/día"')),
    ]
    disc = [
        discrepancia('Uso en menores de 16 años',
                     [(AAS, 'Contraindicado en niños menores de 16 años por su relación con el síndrome de Reye (CIMA)'),
                      (P, 'Pautas pediátricas especializadas: dolor, artritis idiopática juvenil, fiebre reumática, Kawasaki y antiagregación (Pediamécum)')],
                     'No se muestra dosis pediátrica',
                     'Decisión del proyecto: solo dosis de adulto; las pautas pediátricas son de uso especializado y nunca como analgésico o antipirético común.'),
    ]
    alertas = [
        'No usar en menores de 16 años (síndrome de Reye), sobre todo con fiebre, gripe o varicela (CIMA, 4.3 y 4.4).',
        'Contraindicado en úlcera gastroduodenal, antecedente de hemorragia digestiva por AINE, diátesis hemorrágica, asma inducida por salicilatos, '
        'insuficiencia renal, hepática o cardíaca grave, metotrexato ≥15 mg/semana y tercer trimestre del embarazo (CIMA, 4.3).',
        'El comprimido de 100 mg del arsenal (antiagregante) no sirve para la dosis analgésica de 500 mg.',
    ]
    return ficha_oral(
        'acido-acetilsalicilico', 'Ácido acetilsalicílico', 'aine', presentaciones, dosis_,
        {
            'comida': 'despues',
            'texto': 'Con un vaso de agua después de las comidas o con algún alimento; no tomar con el estómago vacío (CIMA).',
            'fuente': fu(AAS, '4.2 Forma de administración'),
        },
        comerciales=['Aspirina'], pediatria='solo_adulto',
        motivo_solo_adulto='La ficha técnica contraindica el ácido acetilsalicílico en menores de 16 años por el síndrome de Reye, y sus pautas '
                           'pediátricas de Pediamécum son de uso especializado.',
        discrepancias=disc,
        renal='Contraindicado en insuficiencia renal grave.',
        hepatico='Contraindicado en insuficiencia hepática grave.',
        fuente_ajuste=fu(AAS, '4.3 Contraindicaciones'),
        alertas=alertas,
    )


def atorvastatina():
    P = _ped('atorvastatina')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(ATO, 'Atorvastatina Cinfa 10 mg; Pediamécum: "Tomar los comprimidos enteros"')),
        pres('comprimido-20-mg', 'comprimido', mg=20, partible='no',
             fuente=fu(ARSENAL, 'Grupo 11.06: Atorvastatina, Comprimido 20 mg (Pediamécum lista ATORVASTATINA CINFA 20 mg)')),
        pres('comprimido-40-mg', 'comprimido', mg=40, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ATORVASTATINA CINFA 40 mg COMPRIMIDOS RECUBIERTOS CON PELICULA EFG')),
        pres('comprimido-80-mg', 'comprimido', mg=80, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: ATORVASTATINA CINFA 80 mg COMPRIMIDOS RECUBIERTOS CON PELICULA EFG')),
    ]
    dosis_ = [
        dosis('Hipercolesterolemia y prevención cardiovascular (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=1, intervalo_h=24,
              tope_dia=(80, 'mg'),
              condicion='Ajustes cada ≥4 semanas. Con elbasvir/grazoprevir o letermovir: no superar 20 mg/día',
              texto='Inicio 10 mg una vez al día; dosis máxima 80 mg una vez al día',
              fuente=fu(ATO, '4.2.1: "La dosis inicial recomendada es de 10 mg una vez al día ... La dosis máxima es de 80 mg una vez al día"')),
        dosis('Hipercolesterolemia familiar heterocigótica (niños desde 10 años y adolescentes)', 'pediatrico', 'fija', 'mg', min=10, max=10,
              tomas=1, intervalo_h=24, tope_dia=(80, 'mg'),
              condicion='Solo por médicos con experiencia en hiperlipidemia pediátrica; ajustes cada ≥4 semanas, por lo general de 10 en 10 mg',
              texto='10 mg cada 24 h; hasta un máximo de 80 mg/día según respuesta y tolerancia',
              fuente=fu(P, 'Niños >10 años y adolescentes: "dosis inicial: 10 mg/24 horas ... hasta una dosis máxima de 80 mg/día" (igual que CIMA 69534)')),
        dosis('Hipercolesterolemia (niños de 4 a 10 años, uso fuera de ficha)', 'pediatrico', 'fija', 'mg', min=5, max=5, tomas=1, intervalo_h=24,
              tope_dia=(40, 'mg'), estatus='off_label',
              condicion='La ficha: no indicada en <10 años. Aumentar cada 4 semanas; máximo 40 mg/día (en algunos casos se ha llegado a 80 mg/día)',
              texto='Inicio 5 mg cada 24 h; máximo 40 mg/día',
              fuente=fu(P, 'Niños 4-10 años: "dosis inicial de 5 mg/24 horas ... hasta un máximo de 40 mg/día, aunque en algunos casos se ha aumentado hasta 80 mg/día"')),
    ]
    disc = [
        discrepancia('Dosis máxima en niños de 4 a 10 años',
                     [(P, '40 mg/día: máximo recomendado (Pediamécum)'),
                      (P, '80 mg/día: "en algunos casos se ha aumentado hasta 80 mg/día" (Pediamécum)')],
                     '40 mg/día',
                     'Regla del tope más bajo dentro de la misma fuente y población.'),
        discrepancia('Uso en menores de 10 años',
                     [(ATO, 'No está indicada en pacientes de menos de 10 años; no se puede hacer una recomendación posológica (CIMA)'),
                      (P, 'Pauta para niños de 4 a 10 años (Pediamécum)')],
                     'Se muestra la pauta de Pediamécum como uso fuera de ficha técnica (off-label)',
                     'Discrepancia de población. Pediamécum advierte que la seguridad con dosis >20 mg (≈0,5 mg/kg) en niños es limitada.'),
    ]
    alertas = [
        'La dosis de 5 mg (niños de 4 a 10 años) no se puede obtener con los comprimidos cargados (10 mg o más, para tragar enteros): '
        'haría falta una presentación de 5 mg.',
        'Contraindicada en enfermedad hepática activa o transaminasas >3 veces el límite superior, embarazo, lactancia, mujeres fértiles sin '
        'anticoncepción y con glecaprevir/pibrentasvir (CIMA, 4.3).',
    ]
    return ficha_oral(
        'atorvastatina', 'Atorvastatina', 'hipolipemiante', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Una toma diaria a cualquier hora, con o sin comida (CIMA). Pediamécum: tomar los comprimidos enteros con un vaso de agua.',
            'fuente': fu(ATO, '4.2.2 Forma de administración'),
        },
        comerciales=['Atorvastatina Cinfa'], discrepancias=disc,
        renal='No es necesario ajustar la dosis.',
        hepatico='Usar con precaución en insuficiencia hepática; contraindicada en enfermedad hepática activa.',
        fuente_ajuste=fu(ATO, '4.2.1 Insuficiencia renal / hepática'),
        alertas=alertas,
    )


def gemfibrozilo():
    presentaciones = [
        pres('comprimido-600-mg', 'comprimido', mg=600, partible='no',
             fuente=fu(GEM, 'Gemfibrozilo Stada 600 mg (la ficha no menciona partición); el arsenal de APS lista 300 y 600 mg')),
        pres('comprimido-300-mg', 'comprimido', mg=300, partible='no',
             fuente=fu(ARSENAL, 'Grupo 11.06: Gemfibrozilo, Comprimido 300 mg y 600 mg (no se indica si es partible)')),
    ]
    dosis_ = [
        dosis('Dislipemia (adultos), 1200 mg al día', 'adulto', 'fija', 'mg', min=600, max=600, tomas=2, intervalo_h=12,
              condicion='Media hora antes del desayuno y de la cena. Rango de la ficha: 900-1200 mg/día; 1200 mg/día es la única dosis con '
                        'efecto documentado sobre la morbilidad',
              texto='600 mg dos veces al día (1200 mg/día)',
              fuente=fu(GEM, '4.2 Forma de administración: "La dosis de 1200 mg se toma como 600 mg dos veces al día, media hora antes del desayuno y de la cena"')),
        dosis('Dislipemia (adultos), 900 mg al día', 'adulto', 'fija', 'mg', min=900, max=900, tomas=1, intervalo_h=24,
              condicion='Media hora antes de la cena. Dosis de inicio en insuficiencia renal leve a moderada',
              texto='900 mg en dosis única antes de la cena',
              fuente=fu(GEM, '4.2: "La dosis de 900 mg se toma como una dosis única media hora antes de la cena"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (Gemfibrozilo Stada); Pediamécum no tiene ficha de gemfibrozilo.',
        'La dosis de 900 mg requiere tres comprimidos de 300 mg (arsenal): el de 600 mg no es partible según las fuentes.',
        'Contraindicado en disfunción hepática, disfunción renal grave, enfermedad de vesícula o vías biliares, con repaglinida, dasabuvir, '
        'selexipag, simvastatina o rosuvastatina 40 mg, y con antecedente de fotoalergia a fibratos (CIMA, 4.3).',
    ]
    return ficha_oral(
        'gemfibrozilo', 'Gemfibrozilo', 'hipolipemiante', presentaciones, dosis_,
        {
            'comida': 'antes',
            'texto': 'Vía oral, media hora antes del desayuno y de la cena (1200 mg) o antes de la cena (900 mg), manteniendo la dieta hipolipemiante (CIMA).',
            'fuente': fu(GEM, '4.2 Forma de administración'),
        },
        pediatria='solo_adulto',
        motivo_solo_adulto='La ficha técnica no lo recomienda en niños y adolescentes por ausencia de datos de seguridad y eficacia.',
        renal='Insuficiencia renal leve a moderada (filtrado 30-80 ml/min/1,73 m²): iniciar con 900 mg/día y valorar la función renal antes de '
              'subir; no usar en insuficiencia renal grave.',
        hepatico='Contraindicado en insuficiencia hepática.',
        fuente_ajuste=fu(GEM, '4.2 Insuficiencia renal / hepática'),
        alertas=alertas,
    )


def isosorbide():
    mono = ['comprimido-20-mg', 'comprimido-40-mg']
    presentaciones = [
        pres('comprimido-20-mg', 'comprimido', mg=20, partible='mitades',
             fuente=fu(ISO, '4.2: "Los comprimidos son ranurados y pueden ser partidos fácilmente en dos mitades"')),
        pres('comprimido-40-mg', 'comprimido', mg=40, partible='no',
             fuente=fu(ISO, '4.2: "un régimen posológico de un comprimido de 40 mg dos o tres veces al día" (mononitrato; la ranura se declara '
                            'solo para el de 20 mg)')),
        pres('comprimido-10-mg-arsenal', 'comprimido', mg=10, partible='no',
             fuente=fu(ARSENAL, 'Grupo 11.01 Antianginosos: "Isosorbide, Comprimido 10 mg." (no dice si es mononitrato o dinitrato)')),
    ]
    dosis_ = [
        dosis('Angina de pecho, inicio (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=2, presentaciones=['comprimido-20-mg'],
              condicion='Primeros dos días, para prevenir la cefalea; luego 20 mg dos veces al día',
              texto='Medio comprimido de 20 mg (10 mg) dos veces al día durante dos días',
              fuente=fu(ISO, '4.2: "reducir la dosis a medio comprimido de mononitrato de isosorbida 20 mg dos veces al día durante los dos primeros días"')),
        dosis('Angina de pecho (adultos)', 'adulto', 'fija', 'mg', min=20, max=20, tomas=2, presentaciones=mono,
              condicion='Puede subirse a un comprimido de 20 mg tres veces al día; si hay crisis nocturnas, 40 mg poco antes de acostarse',
              texto='Un comprimido de 20 mg dos veces al día',
              fuente=fu(ISO, '4.2: "La dosis habitual es de un comprimido de mononitrato de isosorbida 20 mg dos vecesal día"')),
        dosis('Angina de pecho sin respuesta satisfactoria (adultos)', 'adulto', 'fija', 'mg', min=40, max=40, tomas=2, presentaciones=mono,
              condicion='Dos o tres veces al día (se cargan dos tomas)',
              texto='Un comprimido de 40 mg dos o tres veces al día',
              fuente=fu(ISO, '4.2: "se utilizará un régimen posológico de un comprimido de 40 mg dos o tres veces al día"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (mononitrato de isosorbida Normon); Pediamécum no tiene ficha y no hay ficha de dinitrato.',
        'El comprimido de 10 mg del arsenal de APS no indica la sal (mononitrato o dinitrato de isosorbida): no se vincula a ninguna dosis de '
        'mononitrato; confirmar el producto antes de usarlo.',
        'No usar con inhibidores de la 5-fosfodiesterasa (sildenafilo y similares); contraindicado en hipotensión pronunciada, shock, infarto agudo '
        'con presión de llenado baja, anemia marcada, traumatismo o hemorragia cerebral (CIMA, 4.3).',
        'Instaurar de forma gradual, sobre todo con diuréticos u otros antihipertensivos (CIMA).',
    ]
    return ficha_oral(
        'isosorbide', 'Isosorbida (mononitrato)', 'antianginoso', presentaciones, dosis_,
        {
            'comida': 'despues',
            'texto': 'Después de las comidas, sin masticar y con abundante líquido; el comprimido de 20 mg se puede partir en dos mitades (CIMA).',
            'noTriturar': True,
            'fuente': fu(ISO, '4.2: "Los comprimidos deben tomarse después de las comidas, sin masticar y con abundante líquido"'),
        },
        comerciales=['Mononitrato de isosorbida Normon'], pediatria='solo_adulto',
        motivo_solo_adulto='La ficha técnica indica que la dosis, eficacia y seguridad en niños no se han establecido aún.',
        alertas=alertas,
    )


# ================================================================ §4 digestivo
def omeprazol():
    P = _ped('omeprazol')
    presentaciones = [
        pres('capsula-20-mg', 'capsula', mg=20, partible='no',
             fuente=fu(OME, 'Gastromel 20 mg cápsulas duras gastrorresistentes; el arsenal de APS lista 20 mg con gránulos de recubrimiento entérico')),
        pres('capsula-10-mg', 'capsula', mg=10, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: OMEPRAZOL NORMON 10 mg CAPSULAS DURAS GASTRORRESISTENTES')),
        pres('capsula-40-mg', 'capsula', mg=40, partible='no',
             fuente=fu(P, 'Presentaciones de Pediamécum: OMEPRAZOL CINFA 40 MG CAPSULAS DURAS GASTRORRESISTENTES')),
    ]
    dosis_ = [
        dosis('Síntomas de reflujo: ardor y regurgitación ácida (adultos, sin receta)', 'adulto', 'fija', 'mg', min=20, max=20, tomas=1,
              intervalo_h=24,
              condicion='Durante 14 días; suspender al lograr alivio completo (la mayoría en 7 días)',
              texto='Una cápsula de 20 mg una vez al día durante 14 días',
              fuente=fu(OME, '4.2: "La dosis recomendada es de una cápsula gastrorresistente de 20 mg una vez al día durante 14 días"')),
        dosis('Esofagitis por reflujo y ERGE sintomática (niños de 1 año, 10-20 kg)', 'pediatrico', 'fija', 'mg', min=10, max=10, tomas=1,
              intervalo_h=24,
              condicion='En caso necesario, subir a 20 mg una vez al día. Esofagitis 4-8 semanas; síntomas 2-4 semanas',
              texto='10 mg una vez al día (hasta 20 mg)',
              fuente=fu(P, 'Niños >1 año y ≥10 kg: "1 año 10-20 kg 10 mg, 1 vez al día. En caso necesario, puede aumentarse la dosis a 20 mg"')),
        dosis('Esofagitis por reflujo y ERGE sintomática (niños ≥2 años, >20 kg)', 'pediatrico', 'fija', 'mg', min=20, max=20, tomas=1,
              intervalo_h=24,
              condicion='En caso necesario, subir a 40 mg una vez al día. Esofagitis 4-8 semanas; síntomas 2-4 semanas',
              texto='20 mg una vez al día (hasta 40 mg)',
              fuente=fu(P, '"2 años >20 kg 20 mg, 1 vez al día. En caso necesario, puede aumentarse la dosis a 40 mg, 1 vez al día"')),
        dosis('Úlcera duodenal por Helicobacter pylori (niños >4 años), con dos antibióticos', 'pediatrico', 'por_edad', 'mg',
              texto='15-30 kg: 10 mg de omeprazol + amoxicilina 25 mg/kg + claritromicina 7,5 mg/kg, 2 veces al día, 1 semana. '
                    '31-40 kg: 20 mg + amoxicilina 750 mg + claritromicina 7,5 mg/kg, 2 veces al día, 1 semana. '
                    '>40 kg: 20 mg + amoxicilina 1 g + claritromicina 500 mg, 2 veces al día, 1 semana',
              condicion='Tener en cuenta las recomendaciones locales de resistencia bacteriana (normalmente 7 días, hasta 14)',
              fuente=fu(P, 'Tratamiento de la enfermedad gastroduodenal por Helicobacter pylori: tabla por peso')),
    ]
    disc = [
        discrepancia('Ficha CIMA cargada',
                     [(OME, 'Gastromel es de venta libre: solo cubre el ardor y la regurgitación en adultos, 20 mg/día durante 14 días'),
                      (P, 'Indicaciones pediátricas autorizadas (esofagitis, ERGE y H. pylori) con pautas por peso')],
                     'Se muestra la dosis de venta libre para adultos y las pautas pediátricas de Pediamécum',
                     'No hay ficha de prescripción para adultos en las fuentes: la úlcera, la esofagitis del adulto y la erradicación de H. pylori en adultos '
                     'no tienen dosis cargada.'),
    ]
    alertas = [
        'La ficha CIMA cargada (Gastromel) es de venta libre: no sirve como fuente de dosis clínica del adulto fuera del ardor.',
        'No administrar con nelfinavir (CIMA, 4.3).',
    ]
    return ficha_oral(
        'omeprazol', 'Omeprazol', 'protector-gastrico', presentaciones, dosis_,
        {
            'comida': 'antes',
            'texto': 'Por la mañana, tragando la cápsula entera con medio vaso de agua, sin masticar ni triturar; si hay dificultad para tragar, se '
                     'puede abrir y mezclar el contenido con agua sin gas o un líquido ligeramente ácido (no leche ni agua con gas) (CIMA). '
                     'Pediamécum: 15-30 minutos antes del desayuno.',
            'noTriturar': True,
            'fuente': fu(OME, '4.2.2 Forma de administración'),
        },
        comerciales=['Gastromel'], discrepancias=disc,
        renal='No es necesario ajustar la dosis en insuficiencia renal.',
        hepatico='Los pacientes con insuficiencia hepática deben consultar con un médico antes de tomarlo (CIMA). Pediamécum: en insuficiencia hepática '
                 'grave, reducir la dosis a la mitad.',
        fuente_ajuste=fu(OME, '4.2 Insuficiencia renal / hepática (la reducción a la mitad es de Pediamécum)'),
        alertas=alertas,
    )


def famotidina():
    P = _ped('famotidina')
    presentaciones = [
        pres('comprimido-20-mg', 'comprimido', mg=20, partible='no', fuente=fu(FAM, 'Famotidina Cinfa 20 mg (la ficha no menciona partición)')),
        pres('comprimido-40-mg', 'comprimido', mg=40, partible='no',
             fuente=fu(ARSENAL, 'Grupo 16.01: Famotidina, Comprimido 40 mg (Pediamécum lista FAMOTIDINA CINFA 40 mg)')),
    ]
    dosis_ = [
        dosis('Úlcera duodenal o gástrica benigna (adultos)', 'adulto', 'fija', 'mg', min=40, max=40, tomas=1, intervalo_h=24,
              condicion='Por la noche, 4-8 semanas (úlcera duodenal: también 20 mg cada 12 h). Mantenimiento: 20 mg por la noche',
              texto='40 mg por la noche',
              fuente=fu(FAM, '4.2 Úlcera duodenal: "40 mg diario por la noche"; úlcera gástrica: "40 mg tomado por la noche"')),
        dosis('Enfermedad por reflujo gastroesofágico, alivio sintomático (adultos)', 'adulto', 'fija', 'mg', min=20, max=20, tomas=2,
              intervalo_h=12, texto='20 mg dos veces al día',
              fuente=fu(FAM, '4.2: "20 mg de famotidina dos veces al día"')),
        dosis('Erosión o úlcera esofágica asociada a ERGE (adultos)', 'adulto', 'fija', 'mg', min=40, max=40, tomas=2, intervalo_h=12,
              texto='40 mg dos veces al día',
              fuente=fu(FAM, '4.2: "la dosis recomendada es de 40 mg de famotidina dos veces al día"')),
        dosis('Úlcera péptica (niños >1 año y adolescentes, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='dia', max=0.5,
              tomas=2, intervalo_h=12, tope_dia=(40, 'mg'), estatus='off_label',
              condicion='Antes de acostarse o dividido en 2 veces al día (se cargan dos). >40 kg: 40 mg/24 h o 20 mg/12 h',
              texto='0,5 mg/kg/día (máximo 40 mg/día)',
              fuente=fu(P, 'Úlcera péptica, oral: "0,5 mg/kg/día administrado antes de acostarse o dividido en 2 veces al día (máximo: 40 mg/día)"')),
        dosis('Esofagitis y reflujo gastroesofágico (1-12 años, uso fuera de ficha)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=0.5,
              tomas=2, intervalo_h=12, tope_toma=(40, 'mg'), estatus='off_label',
              condicion='Hasta 8 semanas; se han notificado casos de hasta 1 mg/kg dos veces al día',
              texto='0,5 mg/kg dos veces al día (dosis máxima 40 mg/dosis)',
              fuente=fu(P, 'Esofagitis y reflujo, 1-12 años: "0,5 mg/kg, 2 veces al día (dosis máxima: 40 mg/dosis)"')),
        dosis('Esofagitis y reflujo gastroesofágico (>12 años, uso fuera de ficha)', 'pediatrico', 'fija', 'mg', min=20, max=20, tomas=2,
              intervalo_h=12, estatus='off_label', condicion='Durante 6 semanas', texto='20 mg cada 12 h',
              fuente=fu(P, '">12 años: 20 mg/12 h durante 6 semanas"')),
    ]
    disc = [
        discrepancia('Uso en niños',
                     [(FAM, 'La ficha solo da posología de adultos'),
                      (P, 'No se ha establecido la eficacia y seguridad en niños: todos los usos son off-label (Pediamécum)')],
                     'Se muestran las pautas pediátricas de Pediamécum como uso fuera de ficha técnica (off-label)',
                     'Solo Pediamécum respalda la dosis pediátrica.'),
    ]
    alertas = [
        'Las pautas pediátricas por kg traen tope propio (40 mg/día o 40 mg/dosis); la dosis de adulto de referencia es 40 mg por la noche o 20 mg cada 12 h (CIMA).',
    ]
    return ficha_oral(
        'famotidina', 'Famotidina', 'protector-gastrico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral, según el horario indicado en cada pauta (dosis de 40 mg por la noche) (CIMA). La ficha no indica relación con las comidas.',
            'fuente': fu(FAM, '4.2 Forma de administración: "Vía oral. Seguir las recomendaciones indicadas anteriormente"'),
        },
        comerciales=['Famotidina Cinfa'], discrepancias=disc,
        renal='Aclaramiento de creatinina <50 ml/min: reducir la dosis a la mitad o alargar el intervalo a 36-48 h según la respuesta (riesgo de efectos '
              'adversos del SNC).',
        fuente_ajuste=fu(FAM, '4.2 Ajuste de dosis en pacientes con insuficiencia renal grave o moderada'),
        alertas=alertas,
    )


def metoclopramida():
    P = _ped('metoclopramida')
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(MET_C, 'Metoclopramida Accord 10 mg (la ficha no menciona partición); el arsenal de APS lista 10 mg')),
        pres('solucion-1-mg-ml', 'jarabe', mg_ml=1, fuente=fu(MET_S, 'Metoclopramida Kern Pharma 1 mg/ml solución oral (1 mg = 1 ml)')),
    ]
    dosis_ = [
        dosis('Náuseas y vómitos (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=3, tope_dia=(30, 'mg'),
              condicion='Hasta tres veces al día con un intervalo mínimo de 6 h; máximo 30 mg/día o 0,5 mg/kg/día; duración máxima 5 días',
              texto='10 mg hasta tres veces al día',
              fuente=fu(MET_C, '4.2 Población adulta: "una dosis única de 10 mg, que se puede repetir hasta 3 veces al día. La dosis máxima diaria '
                               'recomendada es de 30 mg o 0,5mg/kg"')),
        dosis('Prevención de náuseas y vómitos retardados por quimioterapia (1-18 años)', 'pediatrico', 'por_peso', 'mg/kg', base='toma',
              min=0.1, max=0.15, tomas=3, presentaciones=['solucion-1-mg-ml'],
              condicion='Segunda línea; hasta 3 veces al día con intervalo mínimo de 6 h; máximo 0,5 mg/kg en 24 h; máximo 5 días. Contraindicada <1 año',
              texto='0,1-0,15 mg/kg hasta tres veces al día (máximo 0,5 mg/kg/24 h)',
              fuente=fu(MET_S, '4.2 NVIQ (1-18 años): "0,1 a 0,15 mg/kg de peso corporal, que se puede repetir hasta tres veces al día ... La dosis '
                               'máxima en 24 horas es 0,5 mg/kg"')),
        dosis('Prevención de náuseas y vómitos retardados por quimioterapia (1-18 años), tabla por edad y peso', 'pediatrico', 'por_edad', 'mg',
              presentaciones=['solucion-1-mg-ml'],
              texto='1-3 años (10-14 kg): 1 mg (1 ml); 3-5 años (15-19 kg): 2 mg (2 ml); 5-9 años (20-29 kg): 2,5 mg (2,5 ml); 9-18 años '
                    '(30-60 kg): 5 mg (5 ml); 15-18 años (>60 kg): 10 mg (10 ml); todas hasta 3 veces al día',
              condicion='Máximo 5 días; intervalo mínimo de 6 h entre tomas',
              fuente=fu(MET_S, '4.2 Tabla de dosis (solución oral 1 mg/ml)')),
    ]
    disc = [
        discrepancia('Vía de la pauta pediátrica en Pediamécum',
                     [(MET_S, 'Pauta oral de la ficha: 0,1-0,15 mg/kg hasta tres veces al día, máximo 0,5 mg/kg/24 h'),
                      (P, 'La misma pauta descrita para la vía intravenosa; la nota de seguridad de la AEMPS limita a 0,5 mg/kg/24 h y 5 días')],
                     'Se muestra la pauta oral de la ficha técnica',
                     'Pediamécum no trae una pauta oral propia: no se usa como fuente de dosis, por lo que la ficha queda con una sola institución.'),
    ]
    alertas = [
        'Fuente de dosis única en la práctica: solo las fichas CIMA dan pauta oral; Pediamécum describe la vía intravenosa.',
        'La pauta por kg no trae tope pediátrico en mg (solo 0,5 mg/kg/24 h); como referencia, el adulto tiene un máximo de 30 mg/día (CIMA) y la '
        'calculadora limita a ese tope.',
        'Los comprimidos no son adecuados para niños de menos de 30 kg y no permiten 2,5 o 5 mg (10 mg, sin ranura): en niños usar la solución '
        '(CIMA 75665).',
        'Contraindicada en menores de 1 año (trastornos extrapiramidales), epilepsia, Parkinson, discinesia tardía previa, feocromocitoma, '
        'hemorragia, obstrucción o perforación digestiva y con levodopa (CIMA, 4.3).',
    ]
    return ficha_oral(
        'metoclopramida', 'Metoclopramida', 'antiemetico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral, con un intervalo mínimo de 6 h entre dos tomas, incluso si hay vómito o rechazo de la dosis. La solución se mide con '
                     'el tapón dosificador graduado en ml (CIMA). La ficha no indica relación con las comidas.',
            'fuente': fu(MET_C, '4.2 Forma de administración'),
        },
        comerciales=['Metoclopramida Accord', 'Metoclopramida Kern Pharma'], discrepancias=disc,
        renal='Enfermedad renal terminal (aclaramiento ≤15 ml/min): reducir la dosis diaria un 75 %; insuficiencia renal moderada a grave (15-60 ml/min): '
              'reducir un 50 %. Ancianos: considerar reducir la dosis.',
        hepatico='Insuficiencia hepática grave: reducir la dosis un 50 %.',
        fuente_ajuste=fu(MET_C, '4.2 Poblaciones especiales'),
        alertas=alertas,
    )


def ondansetron():
    P = _ped('ondansetron')
    presentaciones = [
        pres('comprimido-4-mg', 'comprimido', mg=4, partible='no',
             fuente=fu(OND, '4.2 nota c: "La dosis de 2 mg no puede obtenerse con los comprimidos de 4 mg ya que estos no han sido fabricados para romperse"')),
        pres('comprimido-8-mg', 'comprimido', mg=8, partible='no',
             fuente=fu(ARSENAL, 'Grupo 16.02: Ondansetrón, Comprimido 8 mg (Pediamécum lista ONDANSETRON NORMON 8 mg COMPRIMIDOS)')),
    ]
    dosis_ = [
        dosis('Náuseas y vómitos por quimioterapia o radioterapia emetógenas (adultos)', 'adulto', 'fija', 'mg', min=8, max=8, tomas=2,
              intervalo_h=12, tope_dia=(32, 'mg'),
              condicion='8 mg 1-2 h antes del tratamiento y luego 8 mg cada 12 h, máximo 5 días. Tope diario: "la dosis de adultos de 32 mg" (CIMA)',
              texto='8 mg 1-2 h antes; después 8 mg cada 12 h hasta 5 días',
              fuente=fu(OND, '4.2 Adultos: "una dosis de 8 mg por vía oral, 1-2 horas antes ... seguida de 8 mg ... 12 horas durante un periodo máximo de 5 días"')),
        dosis('Quimioterapia altamente emetógena (adultos), dosis única', 'adulto', 'fija', 'mg', min=24, max=24, tomas=1, tope_dia=(32, 'mg'),
              condicion='Junto con 12 mg de dexametasona oral, 1-2 h antes; desde las 24 h, 8 mg dos veces al día hasta 5 días',
              texto='24 mg en dosis única',
              fuente=fu(OND, '4.2: "una única dosis de 24 mg de ondansetrón administrada por vía oral junto con 12 mg de dexametasona"')),
        dosis('Prevención de náuseas y vómitos postoperatorios (adultos)', 'adulto', 'fija', 'mg', min=16, max=16, tomas=1, tope_dia=(32, 'mg'),
              texto='16 mg una hora antes de la anestesia',
              fuente=fu(OND, '4.2 NVPO, adultos: "la dosis oral recomendada es de 16 mg administrados una hora antes de la anestesia"')),
        dosis('Náuseas y vómitos por quimioterapia (≥6 meses), >10 kg', 'pediatrico', 'fija', 'mg', min=4, max=4, tomas=2, intervalo_h=12,
              tope_dia=(32, 'mg'),
              condicion='Vía oral desde 12 h después de la dosis intravenosa, hasta 5 días; dosis diaria total sin superar la de adultos (32 mg)',
              texto='4 mg vía oral cada 12 h',
              fuente=fu(P, 'Dosis por peso: ">10 kg ... 4 mg vía oral cada 12 h"; "La dosis diaria total no debe exceder la dosis de adultos de 32 mg"')),
        dosis('Náuseas y vómitos por quimioterapia (≥6 meses), ≤10 kg', 'pediatrico', 'fija', 'mg', min=2, max=2, tomas=2, intervalo_h=12,
              tope_dia=(32, 'mg'),
              condicion='Vía oral desde 12 h después de la dosis intravenosa, hasta 5 días. No se puede dar con el comprimido de 4 mg (no partible)',
              texto='2 mg vía oral cada 12 h',
              fuente=fu(P, 'Dosis por peso: "=10 kg ... 2 mg vía oral cada 12 h"; nota c: "La dosis de 2 mg no puede obtenerse con los comprimidos de 4 mg"')),
        dosis('Náuseas y vómitos por quimioterapia (≥6 meses), por superficie corporal', 'pediatrico', 'por_superficie', 'mg',
              texto='<0,6 m²: 2 mg vía oral cada 12 h; ≥0,6 m²: 4 mg vía oral cada 12 h (días 2-6, tras 5 mg/m² IV el día 1); total diario ≤32 mg',
              condicion='Por superficie la dosis diaria resulta menor que por peso',
              fuente=fu(OND, '4.2 Tabla 1: Dosis por superficie corporal')),
        dosis('Vómitos de repetición en gastroenteritis aguda (niños, uso fuera de ficha)', 'pediatrico', 'por_edad', 'mg', estatus='off_label',
              texto='Dosis única oral según peso: 8-15 kg: 2 mg; 15-30 kg: 4 mg; >30 kg: 8 mg',
              condicion='Pediamécum lo incluye entre los usos off-label en Pediatría. El tramo de 2 mg no se puede dar con los comprimidos cargados',
              fuente=fu(P, 'Vómitos de repetición asociados a gastroenteritis aguda: "8-15 kg: 2 mg. 15-30 kg: 4 mg. >30 kg: 8 mg"')),
    ]
    alertas = [
        'La dosis de 2 mg no puede obtenerse con los comprimidos de 4 mg (no fabricados para romperse) ni con los de 8 mg: haría falta una forma '
        'líquida o bucodispersable de 2 mg, que no está cargada (CIMA, nota c).',
        'Insuficiencia hepática moderada o grave: no superar 8 mg/día en total (CIMA).',
        'Contraindicado con apomorfina (hipotensión profunda y pérdida de conocimiento) (CIMA, 4.3).',
    ]
    return ficha_oral(
        'ondansetron', 'Ondansetrón', 'antiemetico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Los comprimidos se tragan enteros con un poco de agua (CIMA). Pediamécum: las formas orales pueden administrarse con o sin alimentos.',
            'noTriturar': True,
            'fuente': fu(OND, '4.2.2 Forma de administración'),
        },
        comerciales=['Ondansetrón Normon'],
        renal='No requiere variar la dosis diaria, la frecuencia ni la vía.',
        hepatico='Insuficiencia hepática moderada o grave: no exceder una dosis diaria total de 8 mg.',
        fuente_ajuste=fu(OND, '4.2 Pacientes con insuficiencia renal / hepática'),
        alertas=alertas,
    )


def domperidona():
    P = _ped('domperidona')
    liquidas = ['suspension-1-mg-ml', 'solucion-gotas-10-mg-ml-arsenal']
    presentaciones = [
        pres('capsula-10-mg', 'capsula', mg=10, partible='no', fuente=fu(DOM_C, 'Domperidona Gamir 10 mg cápsulas duras')),
        pres('suspension-1-mg-ml', 'suspension', mg_ml=1, fuente=fu(DOM_S, 'Motilium 1 mg/ml suspensión oral')),
        pres('solucion-gotas-10-mg-ml-arsenal', 'jarabe', mg_ml=10,
             fuente=fu(ARSENAL, 'Grupo 16.02: Domperidona, Solución para gotas orales 10 mg/mL, "Uso en >12 A." (ninguna fuente da gotas por ml: '
                                'se carga como solución medida en ml)')),
    ]
    dosis_ = [
        dosis('Náuseas y vómitos (adultos y adolescentes ≥12 años y ≥35 kg), cápsulas', 'adulto', 'fija', 'mg', min=10, max=10, tomas=3,
              tope_dia=(30, 'mg'), presentaciones=['capsula-10-mg'],
              condicion='Hasta tres veces al día, antes de las comidas; dosis efectiva más baja durante el menor tiempo; normalmente no más de una semana',
              texto='Una cápsula de 10 mg hasta tres veces al día; dosis máxima 30 mg al día',
              fuente=fu(DOM_C, '4.2.1: "Una cápsula de 10 mg hasta tres veces al día con una dosis máxima de 30 mg al día"')),
        dosis('Náuseas y vómitos (adultos y adolescentes ≥12 años y ≥35 kg), formas líquidas', 'adulto', 'fija', 'mg', min=10, max=10, tomas=3,
              intervalo_h=8, tope_dia=(30, 'mg'), presentaciones=liquidas,
              condicion='Antes de las comidas; normalmente no más de una semana. Suspensión de 1 mg/ml: 10 ml hasta tres veces al día, máximo 30 ml/día (CIMA 55411)',
              texto='10 mg cada 8 horas; máximo 30 mg/día',
              fuente=fu(P, 'Niños >12 años y peso ≥35 kg, vía oral: "10 mg administrados cada 8 horas. Máximo vía oral: 30 mg/día" (uso autorizado en '
                           'adultos y adolescentes ≥12 años y ≥35 kg)')),
    ]
    disc = [
        discrepancia('Uso en menores de 12 años o de 35 kg',
                     [(DOM_S, 'No debe utilizarse en niños menores de 12 años ni en adolescentes de menos de 35 kg (sin eficacia) (CIMA)'),
                      (P, '0,25 mg/kg cada 8 h como off-label en lactantes y niños <12 años o <35 kg, con alerta de seguridad: supresión de la '
                          'indicación en Pediatría (Pediamécum)')],
                     'No se muestra dosis pediátrica',
                     'Decisión del proyecto: solo la dosis de adultos y adolescentes ≥12 años y ≥35 kg.'),
    ]
    alertas = [
        'Alerta de seguridad: supresión de la indicación en Pediatría (Pediamécum); no usar en <12 años ni en <35 kg (CIMA).',
        'Contraindicada con prolongación del QTc, alteraciones electrolíticas significativas o cardiopatía (p. ej., insuficiencia cardíaca), con '
        'fármacos que prolongan el QT o inhibidores potentes del CYP3A4, en insuficiencia hepática moderada o grave, prolactinoma y hemorragia, '
        'obstrucción o perforación digestiva (CIMA, 4.3).',
        'Las gotas orales del arsenal (10 mg/ml) se cargan como solución medida en ml: ninguna fuente indica cuántas gotas tiene 1 ml.',
    ]
    return ficha_oral(
        'domperidona', 'Domperidona', 'antiemetico', presentaciones, dosis_,
        {
            'comida': 'antes',
            'texto': 'Antes de las comidas (si se toma después, la absorción se retrasa ligeramente); si se olvida una dosis, omitirla sin duplicar la siguiente (CIMA).',
            'fuente': fu(DOM_C, '4.2: "Se recomienda tomar Domperidona Gamir por vía oral antes de las comidas"'),
        },
        comerciales=['Motilium', 'Domperidona Gamir'], pediatria='solo_adulto',
        motivo_solo_adulto='La ficha técnica no permite usarla en menores de 12 años ni en adolescentes de menos de 35 kg y Pediamécum recoge la '
                           'alerta de seguridad de supresión de la indicación en Pediatría.',
        discrepancias=disc,
        renal='Insuficiencia renal grave: reducir la frecuencia a una o dos veces al día según la gravedad; puede ser necesario reducir la dosis.',
        hepatico='Contraindicada en insuficiencia hepática moderada o grave; sin ajuste en la leve.',
        fuente_ajuste=fu(DOM_C, '4.2.1 Insuficiencia hepática / renal'),
        alertas=alertas,
    )


def trimebutino():
    P = _ped('trimebutino')
    presentaciones = [
        pres('suspension-4-8-mg-ml', 'suspension', mg_ml=4.8,
             fuente=fu(P, 'Polibutin suspensión oral (presentación de Pediamécum). 4,8 mg/ml derivado de las equivalencias de la propia ficha: '
                          '12 mg = 2,5 ml, 24 mg = 5 ml y 48 mg = 10 ml; el registro de CIMA (sin ficha técnica) indica 0,48 g/100 ml')),
        pres('comprimido-100-mg', 'comprimido', mg=100, partible='no',
             fuente=fu(ARSENAL, 'Grupo 16.04 Antiespasmódicos: Trimebutino, Comprimido 100 mg (no se indica si es partible)')),
    ]
    dosis_ = [
        dosis('Tratamiento coadyuvante en gastroenteritis infantil (niños hasta 5 años)', 'pediatrico', 'por_edad', 'mg',
              presentaciones=['suspension-4-8-mg-ml'],
              texto='<1 año: 12 mg cada 8-12 h (2,5 ml por toma); 1-3 años: 24 mg cada 8-12 h (5 ml); 3-5 años: 48 mg cada 8-12 h (10 ml)',
              condicion='Pediamécum lo marca autorizado (A) como refuerzo en diarreas de gastroenteritis; no hay ficha técnica descargable en CIMA para contrastar',
              fuente=fu(P, 'Tratamiento coadyuvante en gastroenteritis infantiles: "Niños <1 años: 12 mg/8-12 horas (2,5 ml/toma). Niños de 1-3 años: '
                           '24 mg/8-12 horas (5 ml/toma). Niños de 3-5 años: 48 mg/8-12 horas (10 ml/toma)"')),
    ]
    disc = [
        discrepancia('Dosis de adultos y >12 años (síndrome del colon irritable)',
                     [(P, '300-400 mg/día de inicio y luego 200 mg/día (Pediamécum)'),
                      (P, '200 mg cada 8 h, es decir 600 mg/día, en la frase siguiente de la misma ficha (Pediamécum)')],
                     'No se carga dosis de adulto',
                     'Inconsistencia interna de la única fuente disponible; sin ficha técnica ni fuente chilena que la resuelva.'),
    ]
    alertas = [
        'Fuente única: solo Pediamécum; CIMA registra Polibutin pero sin ficha técnica descargable.',
        'Sin dosis de adulto: Pediamécum da para >12 años 300-400 mg/día (bajando a 200 mg/día) y, a la vez, 200 mg cada 8 h; no se muestra hasta '
        'contrastar con otra fuente. El comprimido de 100 mg del arsenal queda sin pauta cargada.',
        'Riesgo de aumento rápido de la temperatura corporal en niños en lugares muy cálidos; dosis elevadas pueden causar hiperexcitabilidad (Pediamécum).',
    ]
    return ficha_oral(
        'trimebutino', 'Trimebutino (trimebutina)', 'digestivo', presentaciones, dosis_,
        {
            'comida': 'antes',
            'texto': 'Administrar antes de las comidas (Pediamécum).',
            'fuente': fu(P, 'Administración: "Administrar antes de las comidas"'),
        },
        comerciales=['Polibutin'], discrepancias=disc, alertas=alertas,
    )


def lactulosa():
    P = _ped('lactulosa')
    presentaciones = [
        pres('solucion-667-mg-ml', 'jarabe', mg_ml=667,
             fuente=fu(LAC, 'Duphalac 667 mg/ml solución oral (tabla de 4.2: 10 g = 15 ml); Pediamécum lista DUPHALAC 667 MG/ML SOLUCION ORAL')),
        pres('sobre-10-g', 'sobre', mg=10000, partible='no',
             fuente=fu(LAC, 'Duphalac 10 g solución oral en sobre (15 ml por sobre)')),
    ]
    sol = ['solucion-667-mg-ml']
    dosis_ = [
        dosis('Estreñimiento o ablandamiento de las heces (adultos y adolescentes >14 años)', 'adulto', 'fija', 'g', base='dia', min=10, max=30,
              tomas=2, intervalo_h=12,
              condicion='En una toma diaria o dividida en dos (se cargan dos). Mantenimiento 10-20 g/día; el efecto puede tardar 2-3 días',
              texto='Inicio 10-30 g/día (15-45 ml de solución o 1-3 sobres); mantenimiento 10-20 g/día (15-30 ml)',
              fuente=fu(LAC, '4.2 Adultos: "10 – 30 g (correspondiente a 15 - 45 ml/día de solución oral)"; mantenimiento "10 – 20 g"')),
        dosis('Encefalopatía portosistémica (adultos)', 'adulto', 'fija', 'g', min=20, max=30, tomas=3, intervalo_h=8,
              condicion='De 3 a 4 veces al día (se cargan tres tomas); mantenimiento ajustado a 2-3 deposiciones blandas al día',
              texto='20-30 g (30-45 ml) de 3 a 4 veces al día',
              fuente=fu(LAC, '4.2: "La dosis inicial es de 20 – 30 g, que corresponden a 30 - 45 ml de solución oral, administrados de 3 a 4 veces al día"')),
        dosis('Estreñimiento (niños hasta 14 años), tabla por edad', 'pediatrico', 'por_edad', 'g', presentaciones=sol,
              texto='<1 año: hasta 3 g/día (hasta 5 ml); 1-6 años: 3-7 g/día (5-10 ml); 7-14 años: inicio 10 g/día (15 ml), mantenimiento 7-10 g/día '
                    '(10-15 ml)',
              condicion='En lactantes y niños hasta 7 años, y con dosis <15 ml, usar la solución de 667 mg/ml',
              fuente=fu(LAC, '4.2 Población pediátrica (tabla) y nota: "Para una dosificación precisa en lactantes y niños hasta 7 años, debe utilizarse duphalac '
                             '667 mg/ml solución oral"')),
        dosis('Estreñimiento crónico (niños), dosis por peso', 'pediatrico', 'por_peso', 'g/kg', base='dia', min=0.7, max=2, tomas=2,
              intervalo_h=12, tope_dia=(40, 'g'), presentaciones=sol,
              condicion='Pediamécum (indicación autorizada A) la ofrece como alternativa a la tabla por edad de la ficha. "Dividido a lo largo del '
                        'día" (se cargan dos tomas, como permite la ficha). Calcular siempre los ml con la concentración del frasco',
              texto='0,7-2 g/kg/día; dosis máxima 40 g/día',
              fuente=fu(P, '"También se puede dosificar por kg en niños: 0,7-2 g/kg/día (1-3 ml/kg/día) dividido a lo largo del día, dosis máxima: 40 g/día (60 ml/día)"')),
    ]
    disc = [
        discrepancia('Equivalencia g → ml en niños de 7 a 14 años',
                     [(LAC, '10 g (correspondiente a 15 ml/día de solución oral) (CIMA, solución de 667 mg/ml)'),
                      (P, '10 g/día (20 ml/día) (Pediamécum)')],
                     '10 g = 15 ml con la solución de 667 mg/ml (la calculadora convierte por concentración)',
                     'Error de conversión en Pediamécum: con 667 mg/ml, 10 g son ≈15 ml, no 20 ml. No se copia ningún «ml» de las fichas.'),
    ]
    alertas = [
        'Calcular siempre el volumen con la concentración del frasco; no copiar los ml de las fichas (Pediamécum equivoca 10 g = 20 ml).',
        'El arsenal de APS lista lactulosa «Solución oral 65%» sin expresarla en mg/ml: no se carga como presentación; comprobar en la etiqueta la '
        'concentración real antes de usar la calculadora (la cargada es la de 667 mg/ml de CIMA).',
        'Contraindicada en galactosemia y en obstrucción, perforación o riesgo de perforación digestiva (CIMA, 4.3).',
        'Encefalopatía portosistémica: seguridad y eficacia no establecidas en menores de 18 años (CIMA).',
    ]
    return ficha_oral(
        'lactulosa', 'Lactulosa', 'digestivo', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'En una toma diaria o dividida en dos; si es única, siempre a la misma hora (p. ej., en el desayuno). Diluida o sin diluir; tragar '
                     'de inmediato. Beber 1,5-2 litros de líquido al día (CIMA). Pediamécum: con zumo, leche o agua.',
            'fuente': fu(LAC, '4.2 Forma de administración'),
        },
        comerciales=['Duphalac'], discrepancias=disc,
        renal='No es necesario ajustar la dosis (exposición sistémica insignificante).',
        hepatico='No es necesario ajustar la dosis (exposición sistémica insignificante).',
        fuente_ajuste=fu(LAC, '4.2 Insuficiencia renal e insuficiencia hepática'),
        alertas=alertas,
    )


# ================================================================ §5 endocrino
def metformina():
    P = _ped('metformina')
    ir = ['comprimido-850-mg']
    presentaciones = [
        pres('comprimido-850-mg', 'comprimido', mg=850, partible='no',
             fuente=fu(MTF, 'Dianben 850 mg comprimidos recubiertos (la ficha no menciona partición); el arsenal de APS lista 850 mg')),
        pres('comprimido-lp-1000-mg', 'comprimido', mg=1000, partible='no', retard=True,
             fuente=fu(ARSENAL, 'Grupo 17.08.02: Metformina, Comprimido de liberación prolongada 1000 mg (GES)')),
    ]
    dosis_ = [
        dosis('Diabetes tipo 2 (adultos con función renal normal)', 'adulto', 'fija', 'mg', min=500, max=850, tomas=2, intervalo_h=12,
              tope_dia=(3000, 'mg'), presentaciones=ir,
              condicion='Durante o después de las comidas; 2 o 3 veces al día (se cargan dos). Ajustar tras 10-15 días. Máximo 3 g/día en 3 tomas',
              texto='Inicio 500 u 850 mg 2 o 3 veces al día; dosis máxima recomendada 3 g/día',
              fuente=fu(MTF, '4.2.1: "500 mg u 850 mg ... 2 ó 3 veces al día ... La dosis máxima recomendada es de 3 g ... al día, dividida en 3 tomas"')),
        dosis('Diabetes tipo 2 (niños desde 10 años y adolescentes)', 'pediatrico', 'fija', 'mg', min=500, max=850, tomas=1, intervalo_h=24,
              tope_dia=(2000, 'mg'), presentaciones=ir,
              condicion='Durante o después de las comidas; ajustar tras 10-15 días. Dosis máxima 2 g/día en 2 o 3 tomas',
              texto='500-850 mg una vez al día; máximo 2 g/día',
              fuente=fu(P, 'Diabetes mellitus tipo 2 (ficha técnica, A, niños ≥10 años): "500-850 mg, una vez al día ... Dosis máxima recomendada: 2 g/día" '
                           '(igual que CIMA 55211, 4.2.1 Población pediátrica)')),
    ]
    alertas = [
        'La dosis de 500 mg no se puede dar con los comprimidos cargados (850 mg sin ranura declarada; 1000 mg de liberación prolongada): haría falta '
        'un comprimido de 500 mg.',
        'El comprimido de liberación prolongada de 1000 mg del arsenal no tiene posología en ninguna fuente cargada: las pautas de 1 a 3 tomas '
        'son de la ficha de comprimidos de liberación inmediata y no se vinculan a él.',
        'Contraindicada con TFG <30 ml/min, acidosis metabólica aguda, precoma diabético, situaciones agudas que alteren la función renal o causen '
        'hipoxia, insuficiencia hepática y alcoholismo (CIMA, 4.3).',
    ]
    return ficha_oral(
        'metformina', 'Metformina', 'antidiabetico', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Durante o después de las comidas (CIMA). Pediamécum: con las comidas mejora la tolerancia; en niños los comprimidos pueden dispersarse en agua.',
            'fuente': fu(MTF, '4.2.1: "administrados durante o después de las comidas"'),
        },
        comerciales=['Dianben'],
        renal='Evaluar la TFG antes de iniciar y al menos una vez al año. Dosis diaria máxima total (en 2-3 dosis): TFG 60-89, 3000 mg; 45-59, 2000 mg '
              '(inicio como máximo la mitad); 30-44, 1000 mg; <30, contraindicada.',
        hepatico='Contraindicada en insuficiencia hepática.',
        fuente_ajuste=fu(MTF, '4.2.1 Insuficiencia renal (tabla) y 4.3'),
        alertas=alertas,
    )


def glibenclamida():
    P = _ped('glibenclamida')
    presentaciones = [
        pres('comprimido-5-mg', 'comprimido', mg=5, partible='mitades',
             fuente=fu(GLI, 'HOW SUPPLIED: "5 mg ... engraved with N horizontal bisect 344" (ranura); el arsenal de APS lista 5 mg')),
        pres('comprimido-2-5-mg', 'comprimido', mg=2.5, partible='mitades',
             fuente=fu(GLI, 'HOW SUPPLIED: "2.5 mg ... engraved with N horizontal bisect 343"')),
        pres('comprimido-1-25-mg', 'comprimido', mg=1.25, partible='mitades',
             fuente=fu(GLI, 'HOW SUPPLIED: "1.25 mg ... engraved with N horizontal bisect 342"')),
    ]
    dosis_ = [
        dosis('Diabetes tipo 2 (adultos), dosis de inicio', 'adulto', 'fija', 'mg', min=2.5, max=5, tomas=1, intervalo_h=24,
              tope_toma=(10, 'mg'), tope_dia=(15, 'mg'),
              condicion='Con el desayuno o la primera comida principal; pacientes sensibles, 1,25 mg/día. Mantenimiento 1,25-20 mg/día; aumentos de '
                        '≤2,5 mg por semana; >10 mg/día puede repartirse en dos tomas. Topes de Pediamécum (15 mg/día, no más de 10 mg por toma): '
                        'el prospecto de EE. UU. no recomienda >20 mg/día',
              texto='2,5-5 mg al día con el desayuno; máximo cargado 15 mg/día',
              fuente=fu(GLI, 'Usual Starting Dose: "2.5 to 5 mg daily, administered with breakfast or the first main meal"')),
        dosis('Diabetes MODY y diabetes tipo 2 (niños y adolescentes, uso fuera de ficha)', 'pediatrico', 'fija', 'mg', min=2.5, max=5, tomas=1,
              intervalo_h=24, tope_toma=(10, 'mg'), tope_dia=(15, 'mg'), estatus='off_label',
              condicion='Dosis empleadas en estudios pediátricos; la dosis pediátrica no está establecida y el prospecto de EE. UU. no la recomienda en niños. '
                        'Una toma por la mañana con el desayuno',
              texto='2,5-5 mg/día en una dosis diaria',
              fuente=fu(P, '"En la diabetes MODY y en la diabetes mellitus tipo 2 las dosis empleadas ... en pacientes pediátricos oscilan entre 2,5 y 5 mg/día, '
                           'en una dosis diaria"')),
    ]
    disc = [
        discrepancia('Dosis diaria máxima',
                     [(GLI, '20 mg/día: "Daily doses of more than 20 mg are not recommended" (prospecto de EE. UU.)'),
                      (P, '15 mg/día: "la dosis máxima recomendada es de 15 mg/día", sin más de 10 mg por toma (Pediamécum)')],
                     '15 mg/día',
                     'Regla del tope más bajo.'),
    ]
    alertas = [
        'Fuente de dosis de adulto extranjera (prospecto de la FDA de EE. UU., DailyMed): no hay ficha técnica CIMA de glibenclamida.',
        'Riesgo de hipoglucemia, sobre todo en ancianos, desnutridos y con insuficiencia renal o hepática: dosis inicial y de mantenimiento conservadoras (DailyMed).',
        'Contraindicada en cetoacidosis diabética, diabetes tipo 1 y con bosentán (DailyMed). No recomendada en el embarazo.',
        'Diabetes neonatal (0,2 → 0,8 mg/kg/día, Pediamécum) no se carga: uso hospitalario especializado.',
    ]
    return ficha_oral(
        'glibenclamida', 'Glibenclamida', 'antidiabetico', presentaciones, dosis_,
        {
            'comida': 'con_comida',
            'texto': 'Con el desayuno o la primera comida principal (DailyMed). Pediamécum: una única toma por la mañana con el desayuno; si se pautan '
                     '15 mg/día, repartir en 2 tomas. Si se usa colesevelam, tomar la glibenclamida al menos 4 h antes.',
            'fuente': fu(GLI, 'Usual Starting Dose: "administered with breakfast or the first main meal"'),
        },
        discrepancias=disc,
        renal='Insuficiencia renal: dosis inicial y de mantenimiento conservadoras (DailyMed). Pediamécum: en insuficiencia renal grave, usar insulina.',
        hepatico='Insuficiencia hepática: dosis conservadoras (DailyMed). Pediamécum: en insuficiencia hepática grave, usar insulina.',
        fuente_ajuste=fu(GLI, 'Specific Patient Populations (las frases sobre insulina son de Pediamécum)'),
        alertas=alertas,
    )


def vildagliptina():
    presentaciones = [
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no',
             fuente=fu(VIL, 'Galvus 50 mg comprimidos (la ficha no menciona partición); el arsenal de APS lista 50 mg')),
    ]
    dosis_ = [
        dosis('Diabetes tipo 2 (adultos): monoterapia o con metformina, tiazolidindiona, metformina + sulfonilurea o insulina', 'adulto', 'fija',
              'mg', min=50, max=50, tomas=2, intervalo_h=12, tope_dia=(100, 'mg'),
              condicion='50 mg por la mañana y 50 mg por la noche; no se recomiendan dosis superiores a 100 mg',
              texto='100 mg al día: 50 mg por la mañana y 50 mg por la noche',
              fuente=fu(VIL, '4.2: "la dosis diaria recomendada ... es de 100 mg, dividida en 50 mg por la mañana y 50 mg por la noche ... No se recomiendan '
                             'dosis superiores a 100 mg"')),
        dosis('Diabetes tipo 2 (adultos) en combinación dual con una sulfonilurea', 'adulto', 'fija', 'mg', min=50, max=50, tomas=1, intervalo_h=24,
              condicion='Por la mañana; 100 mg una vez al día no fue más eficaz. Puede ser necesario bajar la sulfonilurea (hipoglucemia)',
              texto='50 mg una vez al día por la mañana',
              fuente=fu(VIL, '4.2: "en combinación dual con una sulfonilurea, la dosis recomendada ... es de 50 mg una vez al día administrada por la mañana"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (Galvus); Pediamécum no tiene ficha de vildagliptina.',
        'No usar en insuficiencia hepática, incluidos ALT o AST >3 veces el límite superior antes del tratamiento (CIMA).',
    ]
    return ficha_oral(
        'vildagliptina', 'Vildagliptina', 'antidiabetico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral, con o sin comida (CIMA). Si se omite una dosis, tomarla en cuanto se recuerde, sin dosis doble el mismo día.',
            'fuente': fu(VIL, '4.2 Forma de administración'),
        },
        comerciales=['Galvus'], pediatria='solo_adulto',
        motivo_solo_adulto='La ficha técnica no la recomienda en menores de 18 años: seguridad y eficacia no establecidas y sin datos.',
        renal='Insuficiencia renal leve (aclaramiento ≥50 ml/min): sin ajuste; moderada, grave o terminal: 50 mg una vez al día.',
        hepatico='No debe utilizarse en insuficiencia hepática (incluida ALT o AST >3 veces el límite superior de la normalidad).',
        fuente_ajuste=fu(VIL, '4.2 Insuficiencia renal / hepática'),
        alertas=alertas,
    )


def empagliflozina():
    presentaciones = [
        pres('comprimido-10-mg', 'comprimido', mg=10, partible='no',
             fuente=fu(EMP, 'Jardiance 10 mg; 4.2: "deben tragarse enteros con agua" (el arsenal de APS lista SGLT2, comprimido recubierto 10 mg)')),
    ]
    dosis_ = [
        dosis('Diabetes tipo 2 (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=1, intervalo_h=24, tope_dia=(25, 'mg'),
              condicion='Si tolera 10 mg, tiene TFGe ≥60 y necesita un control más estricto, subir a 25 mg una vez al día (dosis máxima diaria 25 mg)',
              texto='10 mg una vez al día; máximo 25 mg/día',
              fuente=fu(EMP, '4.2 Diabetes mellitus tipo 2: "La dosis inicial recomendada es 10 mg ... una vez al día ... La dosis máxima diaria es de 25 mg"')),
        dosis('Insuficiencia cardíaca y enfermedad renal crónica (adultos)', 'adulto', 'fija', 'mg', min=10, max=10, tomas=1, intervalo_h=24,
              texto='10 mg una vez al día',
              fuente=fu(EMP, '4.2 Insuficiencia cardíaca / Enfermedad renal crónica: "La dosis recomendada es 10 mg de empagliflozina una vez al día"')),
        dosis('Diabetes tipo 2 (niños desde 10 años)', 'pediatrico', 'fija', 'mg', min=10, max=10, tomas=1, intervalo_h=24, tope_dia=(25, 'mg'),
              condicion='Si tolera 10 mg y requiere control adicional, subir a 25 mg una vez al día. Sin datos en <10 años ni con TFGe <60',
              texto='10 mg una vez al día (hasta 25 mg)',
              fuente=fu(EMP, '4.2 Población pediátrica: "La dosis inicial recomendada es 10 mg ... una vez al día ... se puede aumentar a 25 mg una vez al día"')),
    ]
    alertas = [
        'Fuente única: solo ficha técnica CIMA (Jardiance); Pediamécum no tiene ficha de empagliflozina.',
        'La subida a 25 mg requiere un comprimido de 25 mg, que no está cargado (solo 10 mg, para tragar entero).',
        'Insuficiencia cardíaca y enfermedad renal crónica: seguridad y eficacia no establecidas en <18 años (CIMA).',
    ]
    return ficha_oral(
        'empagliflozina', 'Empagliflozina', 'antidiabetico', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Con o sin alimentos; tragar los comprimidos enteros con agua (CIMA).',
            'noTriturar': True,
            'fuente': fu(EMP, '4.2 Forma de administración'),
        },
        comerciales=['Jardiance'],
        renal='No iniciar con TFGe <20 ml/min/1,73 m²; con TFGe <60, dosis diaria de 10 mg; en diabetes tipo 2 la eficacia es menor con TFGe <45.',
        hepatico='Sin ajuste; no se recomienda en insuficiencia hepática grave (experiencia limitada).',
        fuente_ajuste=fu(EMP, '4.2 Insuficiencia renal / hepática'),
        alertas=alertas,
    )


def levotiroxina():
    P = _ped('levotiroxina')
    presentaciones = [
        _pres_mcg('comprimido-100-mcg', 'comprimido', 100,
                  fuente=fu(LEV, 'Eutirox 100 microgramos comprimidos (la ficha solo describe medio comprimido para Eutirox 150 en el test de supresión); '
                                 'el arsenal de APS lista 50 y 100 µg')),
        _pres_mcg('comprimido-50-mcg', 'comprimido', 50,
                  fuente=fu(P, 'Presentaciones de Pediamécum: EUTIROX 50 microgramos COMPRIMIDOS (el arsenal de APS lista 50 µg)')),
        _pres_mcg('comprimido-25-mcg', 'comprimido', 25,
                  fuente=fu(P, 'Presentaciones de Pediamécum: EUTIROX 25 microgramos COMPRIMIDOS')),
    ]
    dosis_ = [
        dosis('Hipotiroidismo, terapia de sustitución (adultos)', 'adulto', 'fija', 'mcg', min=25, max=50, tomas=1, intervalo_h=24,
              condicion='Aumentos progresivos cada 2-4 semanas según TSH; mantenimiento 100-200 µg/día. Ancianos, coronarios o hipotiroidismo grave '
                        'o antiguo: empezar con dosis bajas (p. ej., 12,5 µg/día) y subir 12,5 µg cada dos semanas',
              texto='Inicio 25-50 µg/día; mantenimiento 100-200 µg/día, en una toma',
              fuente=fu(LEV, '4.2.1 Tabla: "Terapia de sustitución del hipotiroidismo en adultos: dosis inicial 25 - 50; dosis de mantenimiento 100 - 200"')),
        dosis('Hipotiroidismo primario, <65 años con TSH 4,5-10 mIU/l (adultos)', 'adulto', 'fija', 'mcg', min=25, max=50, tomas=1, intervalo_h=24,
              condicion='Dosis inicial según TSH. La misma guía sugiere no tratar con levotiroxina el hipotiroidismo subclínico en <65 años y recomienda '
                        'no tratarlo en ≥65 años',
              texto='25-50 µg',
              fuente=fu(MINSAL_HIPO, 'Tratamiento y seguimiento: "En personas menores de 65 años, la dosis de levotiroxina según TSH es: 4,5-10 mIU/L 25-50 ug"')),
        dosis('Hipotiroidismo primario, <65 años con TSH 10-20 mIU/l (adultos)', 'adulto', 'fija', 'mcg', min=50, max=100, tomas=1, intervalo_h=24,
              condicion='Dosis inicial según TSH; objetivo TSH 2-4 mIU/l; control de TSH a las 4-6 semanas',
              texto='50-100 µg',
              fuente=fu(MINSAL_HIPO, 'Tratamiento y seguimiento: "10-20 mIU/L 50-100 ug"')),
        dosis('Hipotiroidismo primario, <65 años con TSH >20 mIU/l (adultos)', 'adulto', 'por_peso', 'mcg/kg', base='dia', min=1, max=1.6, tomas=1,
              intervalo_h=24,
              condicion='Dosis inicial según TSH. Mayores de 65 años, múltiples comorbilidades o cardiopatía coronaria: iniciar con 25-50 µg/día y '
                        'titular cada 4-6 semanas (objetivo TSH 3-6 mIU/l en el adulto mayor)',
              texto='1,0-1,6 µg/kg',
              fuente=fu(MINSAL_HIPO, 'Tratamiento y seguimiento: ">20 mIU/L 1,0 – 1,6 ug/kg"')),
        dosis('Hipotiroidismo (niños), dosis por kg según edad', 'pediatrico', 'por_edad', 'mcg',
              texto='1-3 meses: 10-15 µg/kg/día; 3-6 meses: 8-10 µg/kg/día o 25-50 µg/día; 6-12 meses: 6-8 µg/kg/día o 50-75 µg/día; 1-5 años: '
                    '5-6 µg/kg/día o 75-100 µg/día; 6-12 años: 4-5 µg/kg/día o 100-125 µg/día; >12 años: 2-3 µg/kg/día o ≥150 µg/día; crecimiento y '
                    'pubertad completos: 1,7 µg/kg/día',
              condicion='Una toma diaria en ayunas. Empezar con el 25 % de la dosis y subir cada semana hasta la dosis completa en 4 semanas; con riesgo '
                        'de insuficiencia cardíaca, no superar 25 µg/día de inicio',
              fuente=fu(P, 'Vía oral: "1-3 meses: 10-15 µg/kg/día ... >12 años: 2-3 µg/kg/día o ≥150 µg/día. Crecimiento y pubertad completos: 1,7 µg/kg/día"')),
        dosis('Hipotiroidismo (niños), dosis de la ficha por superficie corporal', 'pediatrico', 'por_superficie', 'mcg',
              texto='Inicio 12,5-50 µg/día; mantenimiento 100-150 µg/m² de superficie corporal al día. Recién nacidos y bebés con hipotiroidismo '
                    'congénito: 10-15 µg/kg/día los 3 primeros meses',
              condicion='Una toma diaria al menos 30 min antes de la primera comida; el comprimido se disuelve en un poco de agua en el momento',
              fuente=fu(LEV, '4.2.1 Tabla: "Terapia de sustitución del hipotiroidismo en niños: dosis inicial 12,5 - 50; dosis de mantenimiento 100 - 150 '
                             'microgramos/m2"; recién nacidos: "10 a 15 microgramos por kg de peso y día"')),
    ]
    disc = [
        discrepancia('Unidad de la dosis pediátrica de mantenimiento',
                     [(LEV, 'Por superficie corporal (por m²) e inicio en µg/día (CIMA)'),
                      (P, 'Por kg y edad, con equivalente en µg/día (Pediamécum)')],
                     'Se muestran ambas tablas como texto; no se calcula',
                     'Las dos fuentes usan unidades distintas: no son comparables cifra a cifra.'),
    ]
    alertas = [
        'Dosificar en microgramos (µg): 1 mg = 1000 µg. Las presentaciones cargadas son de 25, 50 y 100 µg.',
        'Ninguna fuente declara partibles los comprimidos de 25, 50 o 100 µg: la dosis de 12,5 µg necesita confirmar la ranura del producto.',
        'Iniciar con dosis bajas en ancianos, coronarios e hipotiroidismo grave o de larga evolución (CIMA). No iniciar en infarto agudo, '
        'miocarditis o pancarditis agudas; contraindicada en insuficiencia adrenal o hipofisaria y tirotoxicosis no tratadas (CIMA, 4.3).',
        'La sobredosificación puede disminuir la densidad mineral ósea y causar arritmias como fibrilación auricular (guía MINSAL).',
    ]
    return ficha_oral(
        'levotiroxina', 'Levotiroxina sódica', 'hormonal', presentaciones, dosis_,
        {
            'comida': 'ayunas',
            'texto': 'Dosis única por la mañana en ayunas, media hora antes del desayuno, con un poco de líquido; en niños, disolver el comprimido en un '
                     'poco de agua en el momento (CIMA). Guía MINSAL: en ayunas o 4 h después de comer, lejos de inhibidores de la bomba de protones '
                     'y de suplementos de calcio o fierro.',
            'fuente': fu(LEV, '4.2.2 Forma de administración'),
        },
        comerciales=['Eutirox'], discrepancias=disc, alertas=alertas,
    )


def levonorgestrel():
    P = _ped('levonorgestrel')
    presentaciones = [
        pres('comprimido-1-5-mg', 'comprimido', mg=1.5, partible='no', fuente=fu(LNG, 'Levonorgestrel Exeltis 1,5 mg comprimido')),
        pres('comprimido-0-75-mg', 'comprimido', mg=0.75, partible='no',
             fuente=fu(ARSENAL, 'Grupo 17.03 Anticonceptivos: Levonorgestrel, Comprimido 0,75 mg y 1,5 mg, "Uso de emergencia"')),
    ]
    dosis_ = [
        dosis('Anticoncepción de emergencia', 'adulto', 'fija', 'mg', min=1.5, max=1.5, tomas=1,
              condicion='Lo antes posible, preferiblemente en las primeras 12 h y no más tarde de 72 h tras la relación sin protección; si vomita en las '
                        '3 h siguientes, tomar otro comprimido. Pediamécum: autorizado en mayores de 16 años',
              texto='1500 µg (1,5 mg) en dosis única',
              fuente=fu(P, 'Dosis: "Vía de administración oral de 1500 µg, preferiblemente dentro de las primeras 12 horas, y no más tarde de las primeras 72 horas"')),
        dosis('Anticoncepción de emergencia con inductores enzimáticos en las últimas 4 semanas', 'adulto', 'fija', 'mg', min=3, max=3, tomas=1,
              condicion='Solo si no puede o no desea usar un DIU de cobre (opción preferente); dosis doble: 2 comprimidos de 1,5 mg a la vez',
              texto='3 mg (2 comprimidos de 1,5 mg juntos) en dosis única',
              fuente=fu(LNG, '4.2: "que tomen una dosis doble de levonorgestrel (es decir, 2 comprimidos a la vez) si no pueden o no desean utilizar el DIU-Cu"')),
    ]
    disc = [
        discrepancia('Uso en adolescentes',
                     [(LNG, 'No adecuado en niñas en edad prepuberal (CIMA)'),
                      (P, 'Autorizado en mayores de 16 años; no recomendado en menores de 16 (off-label) (Pediamécum)')],
                     'Solo pauta de adulto (sin dosis pediátrica)',
                     'Decisión del proyecto: anticoncepción de emergencia solo con la pauta de adulto.'),
    ]
    alertas = [
        'Tras la anticoncepción de emergencia, usar un método de barrera hasta la siguiente menstruación; no contraindica seguir con la '
        'anticoncepción hormonal regular (CIMA).',
        'Con inductores enzimáticos en las últimas 4 semanas, preferir un DIU de cobre (CIMA).',
        'Pediamécum mezcla en la misma ficha el sistema intrauterino de levonorgestrel (otro producto): esas pautas no se cargan.',
    ]
    return ficha_oral(
        'levonorgestrel', 'Levonorgestrel (anticoncepción de emergencia)', 'hormonal', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral, en cualquier momento del ciclo menstrual salvo que haya retraso de la menstruación (CIMA). La ficha no indica relación con las comidas.',
            'fuente': fu(LNG, '4.2 Forma de administración / Posología'),
        },
        comerciales=['Levonorgestrel Exeltis'], pediatria='solo_adulto',
        motivo_solo_adulto='Anticoncepción de emergencia con pauta solo de adulto: la ficha no la considera adecuada en niñas prepúberes y '
                           'Pediamécum no la recomienda en menores de 16 años.',
        discrepancias=disc, alertas=alertas,
    )


def fichas():
    fabricas = [enalapril, captopril, losartan, amlodipino, atenolol, propranolol, carvedilol, metildopa, hidroclorotiazida, furosemida,
                espironolactona, acido_acetilsalicilico, atorvastatina, gemfibrozilo, isosorbide, omeprazol, famotidina, metoclopramida,
                ondansetron, domperidona, trimebutino, lactulosa, metformina, glibenclamida, vildagliptina, empagliflozina, levotiroxina,
                levonorgestrel]
    todas = {}
    for f in fabricas:
        ficha = f()
        if ficha['id'] in todas:
            raise SystemExit(f'ficha repetida en tanda 2: {ficha["id"]}')
        todas[ficha['id']] = ficha
    return todas
