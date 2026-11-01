"""Orales, tanda 4: medicamentos orales de uso oftalmológico (Tarea 9 del plan Oftalmología v1).

Dos cosas:
- `fichas()`: 7 fichas nuevas (acetazolamida, metazolamida, valaciclovir, famciclovir, doxiciclina, minociclina,
  pirimetamina). Cargan SOLO el uso oftalmológico del fármaco (todas sus dosis llevan `oftalmica`).
- `marcar(fichas)`: agrega `usos: ['oftalmologia']` y dosis oftálmicas a 4 fichas que ya existen (aciclovir,
  azitromicina, prednisona, cotrimoxazol) sin tocar sus dosis anteriores.

Las citas se construyen con `oftalmo.comun` (CIMA, Pediamécum, DailyMed y `web/` leídos de `datos/crudos/oftalmo/`),
así cada cita apunta a un archivo que existe. Fecha de consulta: 2026-10-31.

No se citan (verificación pendiente, ver informe): autores del PPP de cierre angular de la AAO, conversión de
metilprednisolona del ONTT y el estudio ZEDS (valaciclovir en zóster oftálmico; un repositorio lo marca «withdrawn»).
"""
from oftalmo import comun as oc
from .comun import dosis, discrepancia, ficha_oral, pres

USOS = ['oftalmologia']
EW = 'American Academy of Ophthalmology (EyeWiki)'
HARVARD = 'Massachusetts Eye and Ear / Harvard Medical School (guía aceptada por la AAO)'
CDC = 'Centers for Disease Control and Prevention (CDC)'
SOLO_OFT = 'Esta ficha carga solo el uso oftalmológico del fármaco; no carga sus otras indicaciones.'

_cache = {}


def _o(**kw):
    """Dosis oftálmica: atajo de `dosis(..., oftalmica=True)`."""
    return dosis(oftalmica=True, **kw)


# ---------------------------------------------------------------------------------------------- citas
def _citas():
    c = {}
    # Herpes
    c['hsv'] = lambda t: oc.web('oral-herpes', 'hsv-keratitis', HARVARD, t, anio=2014)  # noqa: E731
    c['hzo'] = lambda t: oc.web('oral-herpes', 'Herpes_Zoster_Ophthalmicus', EW, t, anio=2026)  # noqa: E731
    c['bert'] = lambda t: oc.web('oral-herpes', 'pediatric-herpes-keratitis', 'Review of Ophthalmology', t, anio=2017)  # noqa: E731
    # Glaucoma agudo
    c['rveeh'] = lambda t: oc.web('oral-glaucoma-agudo', 'Acute-Angle-Closure-Glaucoma-Final-2022',
                                  'Royal Victoria Eye and Ear Hospital (Dublín)', t, anio=2022)  # noqa: E731
    c['nhs'] = lambda t: oc.web('oral-glaucoma-agudo', 'acute-angle-closure-glaucoma-guidelines', 'NHS Highland', t, anio=2026)  # noqa: E731
    c['deitz'] = lambda t: oc.web('oral-glaucoma-agudo', 'systemic-ocular-antihypertensive', 'Glaucoma Today', t, anio=2023)  # noqa: E731
    c['pcg'] = lambda t: oc.web('oral-glaucoma-agudo', 'Primary_Congenital_Glaucoma', EW, t, anio=2026)  # noqa: E731
    # Blefaritis
    c['ppp'] = lambda t: oc.web('oral-blefaritis', 'blepharitis-ppp', 'American Academy of Ophthalmology (Preferred Practice Pattern)', t)  # noqa: E731
    c['mgd'] = lambda t: oc.web('oral-blefaritis', 'PMC3072163', 'Investigative Ophthalmology & Visual Science', t)  # noqa: E731
    c['cochrane'] = lambda t: oc.web('oral-blefaritis', 'how-well-do-antibiotics', 'Cochrane Database of Systematic Reviews', t)  # noqa: E731
    # Corticoides
    c['uveitis'] = lambda t: oc.web('oral-corticoides', 'Treatment_of_Uveitis', EW, t, anio=2026)  # noqa: E731
    c['gca'] = lambda t: oc.web('oral-corticoides', 'Giant_Cell_Arteritis', EW, t, anio=2026)  # noqa: E731
    c['bsr'] = lambda t: oc.web('oral-corticoides', 'rheumatology/article/59/3/487', 'Rheumatology (British Society for Rheumatology)', t)  # noqa: E731
    c['ontt'] = lambda t: oc.web('oral-corticoides', 'EXT_ID:1734247', 'New England Journal of Medicine', t)  # noqa: E731
    # Toxoplasmosis
    c['dunay'] = lambda t: oc.web('oral-toxoplasmosis', 'PMC6148195', 'Clinical Microbiology Reviews', t)  # noqa: E731
    c['cdc'] = lambda t: oc.web('oral-toxoplasmosis', 'toxoplasmosis/hcp', CDC, t, anio=2026)  # noqa: E731
    c['felix'] = lambda t: oc.web('oral-toxoplasmosis', 'EXT_ID:24388839', 'American Journal of Ophthalmology', t)  # noqa: E731
    return c


# ---------------------------------------------------------------------------------------------- fichas nuevas
def acetazolamida(c):
    cima = lambda d: oc.cima('acetazolamida', '24408', d)  # noqa: E731
    ped = lambda d: oc.ped('acetazolamida', d)  # noqa: E731
    presentaciones = [pres('comprimido-250-mg', 'comprimido', mg=250, partible='no',
                           fuente=cima('Edemox 250 mg comprimidos (la ficha no menciona ranura ni partición)'))]
    dosis_ = [
        _o(indicacion='Glaucoma de ángulo abierto, adyuvante (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=250, max=250, tomas=4, tope_dia=(1000, 'mg'),
           texto='250 mg de 1 a 4 veces al día, según síntomas y presión intraocular',
           fuente=cima('4.2 Glaucoma: "de una a cuatro dosis diarias de 250 mg"; "Las dosis superiores a 1 g/día no suelen ocasionar mayor respuesta"')),
        _o(indicacion='Glaucoma secundario y tratamiento preoperatorio del glaucoma agudo de ángulo cerrado (adultos)',
           poblacion='adulto', regimen='fija', unidad='mg', base='dia', min=250, max=1000,
           texto='250 a 1000 mg/día repartidos en varias tomas (la ficha cita 250 mg cada 4 horas)',
           fuente=cima('4.2 Glaucoma secundario y preoperatorio del agudo de ángulo cerrado: "250-1.000 mg/día repartidos en varias tomas (250 mg cada cuatro horas)"')),
        _o(indicacion='Cierre angular agudo, urgencia: dosis de carga', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=500, max=500, tomas=1, estatus='off_label',
           condicion='Una sola vez; la vía IV es la preferida en las guías de urgencia; la define el equipo de oftalmología',
           texto='500 mg una vez (VO o IV); después 250 mg cuatro veces al día',
           fuente=c['rveeh']('Acetazolamide 500mg PO/IV (IV es la vía preferida por inicio de acción más rápido); precaución con insuficiencia renal, pedir función renal basal')),
        _o(indicacion='Cierre angular agudo, urgencia: mantenimiento tras la carga', poblacion='adulto', regimen='fija',
           unidad='mg', base='toma', min=250, max=250, tomas=4, intervalo_h=6, estatus='off_label',
           condicion='Después de la dosis de carga de 500 mg; la guía permite la vía oral o la IV',
           fuente=c['nhs']('"Actetazolamide 500mg IV stat then 250mg orally (or IV) 4 times daily" (errata «Actetazolamide» en el original)')),
        _o(indicacion='Glaucoma (niños)', poblacion='pediatrico', regimen='por_peso', unidad='mg/kg', base='dia', min=8, max=30,
           tomas=4, tope_dia=(750, 'mg'), condicion='La misma ficha dice que la seguridad y eficacia no están establecidas en pacientes de 12 años y menores',
           fuente=cima('4.2 Población pediátrica, epilepsia y glaucoma: "de 8 a 30 mg por kilo en dosis separadas hasta una dosis máxima diaria de 750 mg"')),
        _o(indicacion='Glaucoma congénito primario (niños)', poblacion='pediatrico', regimen='por_peso', unidad='mg/kg',
           base='dia', min=10, max=20, tomas=4, estatus='off_label', texto='10 a 20 mg/kg/día repartidos en 3 o 4 tomas',
           fuente=c['pcg']('"acetazolamide (Diamox, dose 10-20 mg/kg/day divided into 3 or 4 doses)"')),
    ]
    disc = [
        discrepancia('Tope diario pediátrico en glaucoma',
                     [('CIMA-OFT-ACETAZOLAMIDA-24408', '750 mg/día de máximo (Edemox, CIMA; dosis de 8 a 30 mg/kg/día)'),
                      ('PEDIAMECUM-OFT-ACETAZOLAMIDA', '1000 mg/día de máximo (Pediamécum; dosis de 8-30 mg/kg en dosis separadas cada 6-8 h)')],
                     '750 mg/día de máximo (el más bajo)', 'Se muestra el tope más conservador mientras no se aclare.'),
        discrepancia('Dosis diaria en glaucoma secundario y preoperatorio (misma ficha)',
                     [('CIMA-OFT-ACETAZOLAMIDA-24408', '250-1.000 mg/día repartidos en varias tomas'),
                      ('CIMA-OFT-ACETAZOLAMIDA-24408', '250 mg cada cuatro horas (6 tomas = 1500 mg/día)')],
                     'Rango de 250 a 1000 mg/día',
                     'La ficha cita las dos cosas y 250 mg cada 4 horas supera el máximo de 1000 mg/día; se muestra el rango diario.'),
    ]
    alertas = [
        SOLO_OFT + ' No carga diurético, epilepsia ni mal de altura.',
        'Es una sulfonamida: las reacciones de hipersensibilidad pueden repetirse con cualquier derivado de sulfamidas (CIMA 4.4).',
        'El uso prolongado está contraindicado en el glaucoma crónico de ángulo cerrado no congestivo: puede producirse cierre orgánico del ángulo (CIMA 4.3).',
        'Contraindicada en insuficiencia hepática grave (CIMA 4.3).',
        'Más de 1 g al día no baja más la presión intraocular (CIMA; Deitz 2023).',
        'En niños los efectos adversos son frecuentes (más del 40 %: letargia, falta de apetito, acidosis metabólica; EyeWiki).',
    ]
    return ficha_oral(
        'acetazolamida', 'Acetazolamida', 'antiglaucomatoso', presentaciones, dosis_,
        {'comida': 'ayunas',
         'texto': 'Preferentemente en ayunas; si hay náuseas o vómitos se puede dar con leche o alimentos para mejorar la tolerancia digestiva.',
         'fuente': cima('4.2 Forma de administración: "preferentemente en ayunas, aunque si aparecen náuseas o vómitos se puede administrar con leche o alimentos"')},
        comerciales=['Edemox', 'Diamox'], usos=USOS, discrepancias=disc, alertas=alertas,
        renal='Se excreta por vía renal: con aclaramiento de creatinina < 60 ml/min puede ser necesario bajar la dosis; en insuficiencia renal moderada a severa, reducir la dosis a la mitad o pasar a una toma cada 12 horas (CIMA 4.2).',
        hepatico='Contraindicada en insuficiencia hepática grave; puede aumentar la hiperamonemia en pacientes con insuficiencia hepática (CIMA 4.3 y 4.4).',
        fuente_ajuste=cima('4.2 Insuficiencia renal; 4.3 y 4.4 Insuficiencia hepática'),
    )


def metazolamida(c):
    dm = lambda d: oc.dm('metazolamida', d)  # noqa: E731
    presentaciones = [
        pres('comprimido-25-mg', 'comprimido', mg=25, partible='no', registro_chile='no_registrado',
             fuente=dm('Descripción: "Each tablet ... contains 25 mg or 50 mg methazolamide USP"')),
        pres('comprimido-50-mg', 'comprimido', mg=50, partible='no', registro_chile='no_registrado',
             fuente=dm('Descripción: "Each tablet ... contains 25 mg or 50 mg methazolamide USP"')),
    ]
    dosis_ = [
        _o(indicacion='Glaucoma crónico de ángulo abierto, glaucoma secundario y preoperatorio del glaucoma agudo de ángulo cerrado (adultos)',
           poblacion='adulto', regimen='fija', unidad='mg', base='toma', min=50, max=100, tomas=3, tope_dia=(300, 'mg'),
           condicion='Autorizada por la FDA; sin registro en Chile (importación o uso compasivo)',
           texto='50 a 100 mg, 2 o 3 veces al día',
           fuente=dm('DOSAGE AND ADMINISTRATION: "varies from 50 mg to 100 mg two or three times daily"; tope diario de 300 mg según Deitz 2023 («maximum dose of 100 mg three times per day»)')),
        _o(indicacion='Glaucoma congénito primario (niños)', poblacion='pediatrico', regimen='por_peso', unidad='mg/kg',
           base='dia', max=2, tomas=2, estatus='off_label',
           texto='Menos de 2 mg/kg/día repartidos en 2 tomas',
           condicion='La etiqueta de la FDA dice que la seguridad y eficacia en niños no están establecidas',
           fuente=c['pcg']('"methazolamide (Neptazane, dose < 2 mg/kg/day, divided into 2 doses"')),
    ]
    disc = [
        discrepancia('Uso en niños',
                     [('DAILYMED-OFT-METAZOLAMIDA', 'Etiqueta FDA: «The safety and effectiveness of methazolamide in children have not been established»'),
                      ('WEB-OFT-ORAL-GLAUCOMA-AGUDO-PRIMARY_CONGENITAL_GLAUCOMA', 'EyeWiki: dosis < 2 mg/kg/día en 2 tomas en glaucoma congénito')],
                     'Se muestra la pauta de EyeWiki como off-label', 'La etiqueta no la respalda; es práctica de especialista.'),
    ]
    alertas = [
        SOLO_OFT,
        'No registrada en Chile: solo por importación o uso compasivo.',
        'Contraindicada en enfermedad renal o hepática marcada, con sodio o potasio bajos y en acidosis hiperclorémica (etiqueta FDA).',
        'El uso prolongado está contraindicado en glaucoma de ángulo cerrado: puede cerrarse el ángulo aunque baje la presión (etiqueta FDA).',
        'Es una sulfonamida: se han descrito reacciones graves (Stevens-Johnson, necrólisis epidérmica, discrasias sanguíneas) (etiqueta FDA).',
        'Con aspirina en dosis altas hay riesgo de anorexia, taquipnea, letargo, coma y muerte (etiqueta FDA).',
    ]
    return ficha_oral(
        'metazolamida', 'Metazolamida', 'antiglaucomatoso', presentaciones, dosis_,
        {'comida': 'indiferente',
         'texto': 'La etiqueta de la FDA no da indicación sobre las comidas.',
         'fuente': dm('DOSAGE AND ADMINISTRATION (no menciona relación con las comidas)')},
        comerciales=['Neptazane'], usos=USOS, discrepancias=disc, alertas=alertas,
        renal='Contraindicada en enfermedad renal marcada; en enfermedad renal leve hay que ajustar la dosis (etiqueta FDA; Deitz 2023).',
        hepatico='Contraindicada en enfermedad o disfunción hepática marcada (etiqueta FDA).',
        fuente_ajuste=dm('CONTRAINDICATIONS: "marked kidney or liver disease or dysfunction"'),
    )


def valaciclovir(c):
    cima = lambda d: oc.cima('valaciclovir', '61240', d)  # noqa: E731
    ped = lambda d: oc.ped('valaciclovir', d)  # noqa: E731
    presentaciones = [pres('comprimido-500-mg', 'comprimido', mg=500, partible='no',
                           fuente=cima('Valtrex 500 mg comprimidos recubiertos (la ficha no menciona ranura ni partición)'))]
    dosis_ = [
        _o(indicacion='Herpes zóster oftálmico (adultos inmunocompetentes)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=1000, max=1000, tomas=3, tope_dia=(3000, 'mg'),
           condicion='7 días; empezar lo antes posible (no hay datos si se inicia después de 72 h de la erupción)',
           fuente=cima('4.2: "1.000 mg tres veces al día durante siete días (dosis diaria total de 3.000 mg)"')),
        _o(indicacion='Queratitis herpética epitelial dendrítica (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=500, max=500, tomas=2, estatus='off_label', condicion='7 a 10 días',
           fuente=c['hsv']('App. VI, epitelial dendrítica: "Valacyclovir (Valtrex): 500 mg twice daily for 7-10 days"')),
        _o(indicacion='Queratitis herpética epitelial geográfica (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=1000, max=1000, tomas=3, estatus='off_label', condicion='14 a 21 días',
           fuente=c['hsv']('App. VI, epitelial geográfica: "Valacyclovir (Valtrex): 1 g 3 times daily for 14-21 days"')),
        _o(indicacion='Profilaxis de queratitis herpética recurrente (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=500, max=500, tomas=1, estatus='off_label',
           condicion='Al menos un año; la duración óptima no está establecida',
           fuente=c['hsv']('App. VI, profilaxis: "Valacyclovir (Valtrex): 500 mg once daily ... at least one year is recommended"')),
        _o(indicacion='Supresión de infecciones oculares recurrentes por herpes simple (≥12 años)', poblacion='pediatrico',
           regimen='fija', unidad='mg', base='toma', min=500, max=500, tomas=1, estatus='off_label',
           condicion='Adolescentes inmunocompetentes de 12 años o más',
           fuente=ped('Uso clínico (>12 años): "tratamiento y supresión de infecciones oculares recurrentes"; supresión del VHS en ≥12 años: 500 mg/24 h')),
        _o(indicacion='Enfermedad ocular aguda tras ciclo de aciclovir IV (≥12 años)', poblacion='pediatrico', regimen='fija',
           unidad='mg', base='toma', min=1000, max=1000, tomas=3, estatus='off_label',
           condicion='4 a 6 semanas, después de un ciclo intravenoso de aciclovir de 10 a 14 días',
           fuente=ped('"Tratamiento de enfermedad ocular aguda: 1000 mg, 3 veces al día durante 4-6 semanas, tras haber finalizado un ciclo endovenoso de aciclovir (10-14 días)"')),
    ]
    disc = [
        discrepancia('Edad mínima de uso',
                     [('CIMA-OFT-VALACICLOVIR-61240', '12 años como edad mínima en la ficha técnica (Valtrex, CIMA): seguridad y eficacia no establecidas en menores'),
                      ('WEB-OFT-ORAL-HERPES-HSV-KERATITIS', '2 años como edad mínima en la guía MEEI/Harvard: valaciclovir indicado en niños mayores')],
                     'Solo la pauta para adolescentes, que es la edad mínima de la ficha técnica',
                     'La ficha técnica y Pediamécum dan datos desde esa edad; en menores decide el especialista.'),
    ]
    alertas = [
        SOLO_OFT,
        'El zóster oftálmico de un paciente inmunodeprimido se trata con aciclovir intravenoso, no con la vía oral (CIMA 4.4).',
        'Precaución en mayores de 65 años y en insuficiencia renal: los tres antivirales orales pueden dañar el riñón, y aciclovir y valaciclovir dan más reacciones del sistema nervioso en ancianos (guía MEEI/Harvard).',
        'En el estudio HEDS agregar un antiviral oral de dosis alta al tópico en la queratitis epitelial no evitó la queratitis estromal posterior (guía MEEI/Harvard).',
    ]
    return ficha_oral(
        'valaciclovir', 'Valaciclovir', 'antiviral-antifungico', presentaciones, dosis_,
        {'comida': 'indiferente',
         'texto': 'La ficha técnica no fija relación con las comidas.',
         'fuente': cima('4.2 Posología y forma de administración (sin indicación sobre las comidas)')},
        comerciales=['Valtrex', 'Perviroral'], usos=USOS, discrepancias=disc, alertas=alertas,
        renal='La dosis se reduce según el aclaramiento de creatinina (Tabla 1 de la ficha); mantener buena hidratación; en hemodiálisis dar la dosis después de la sesión (CIMA 4.2).',
        hepatico='No hace falta ajustar la dosis en cirrosis leve o moderada ni en cirrosis avanzada, según los estudios de la ficha (CIMA 4.2).',
        fuente_ajuste=cima('4.2 Insuficiencia renal / Insuficiencia hepática'),
    )


def famciclovir(c):
    cima = lambda d: oc.cima('famciclovir', '60609', d)  # noqa: E731
    presentaciones = [pres('comprimido-250-mg', 'comprimido', mg=250, partible='no', registro_chile='no_registrado',
                           fuente=cima('Famvir 250 mg comprimidos recubiertos (la ficha no menciona ranura ni partición)'))]
    dosis_ = [
        _o(indicacion='Herpes zóster oftálmico (adultos inmunocompetentes)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=500, max=500, tomas=3, condicion='7 días; empezar apenas se diagnostique',
           fuente=cima('4.2 Herpes zoster y zoster oftálmico en adultos inmunocompetentes: "500 mg tres veces al día durante siete días"')),
        _o(indicacion='Queratitis herpética epitelial dendrítica (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=250, max=250, tomas=2, estatus='off_label', condicion='7 a 10 días',
           fuente=c['hsv']('App. VI, epitelial dendrítica: "Famciclovir (Famvir): 250 mg twice daily for 7-10 days"')),
        _o(indicacion='Queratitis herpética epitelial geográfica (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=500, max=500, tomas=2, estatus='off_label', condicion='14 a 21 días',
           fuente=c['hsv']('App. VI, epitelial geográfica: "Famciclovir (Famvir): 500 mg twice daily for 14-21 days"')),
        _o(indicacion='Profilaxis de queratitis herpética recurrente (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
           base='toma', min=250, max=250, tomas=2, estatus='off_label', condicion='Al menos un año; la duración óptima no está establecida',
           fuente=c['hsv']('Profilaxis: "Famciclovir (Famvir): 250 mg twice daily"; "at least one year is recommended"')),
    ]
    alertas = [
        SOLO_OFT,
        'No registrado en Chile: solo por importación o uso compasivo.',
        'La guía MEEI/Harvard lo prefiere en mayores de 65 años (con o sin función renal reducida), porque aciclovir y valaciclovir dan más reacciones del sistema nervioso central en ancianos.',
        'Para la profilaxis la guía lo propone como alternativa extrapolada de los estudios de herpes genital; solo aciclovir y valaciclovir tienen estudio ocular que demuestre menos recurrencias (HEDS).',
    ]
    return ficha_oral(
        'famciclovir', 'Famciclovir', 'antiviral-antifungico', presentaciones, dosis_,
        {'comida': 'indiferente', 'texto': 'Puede administrarse con independencia de las comidas.',
         'fuente': cima('4.2 Forma de administración: "con independencia de las comidas"')},
        comerciales=['Famvir'], usos=USOS, pediatria='solo_adulto',
        motivo_solo_adulto='La seguridad y la eficacia no están establecidas en menores de 18 años (CIMA 4.2); la guía MEEI/Harvard lo indica igual.',
        alertas=alertas,
        renal='Hay que ajustar la dosis según el aclaramiento de creatinina; en hemodiálisis dar la dosis justo después de la diálisis (CIMA 4.2, Tabla 1).',
        hepatico='No hace falta ajustar en insuficiencia hepática leve o moderada; no hay datos en insuficiencia grave (CIMA 4.2).',
        fuente_ajuste=cima('4.2 Pacientes con insuficiencia renal / hepática'),
    )


def doxiciclina(c):
    cima = lambda d: oc.cima('doxiciclina', '46406', d)  # noqa: E731
    presentaciones = [pres('capsula-100-mg', 'capsula', mg=100, partible='no',
                           fuente=cima('Vibracina 100 mg cápsulas duras (cápsula: no se parte)'))]
    dosis_ = [
        _o(indicacion='Blefaritis posterior y disfunción de glándulas de Meibomio (adultos), pauta del Wills Eye Manual',
           poblacion='adulto', regimen='fija', unidad='mg', base='toma', min=100, max=100, tomas=2, estatus='off_label',
           condicion='6 semanas; en casos recurrentes los tratamientos pueden extenderse meses',
           fuente=c['mgd']('Tabla 2, Wills Eye Manual: "Tetracycline 250 mg four times a day or doxycycline 100 mg twice a day for 6 weeks"')),
        _o(indicacion='Blefaritis con compromiso corneal (adultos), pauta del Moorfields Manual', poblacion='adulto',
           regimen='fija', unidad='mg', base='toma', min=100, max=100, tomas=1, estatus='off_label', condicion='8 semanas',
           fuente=c['mgd']('Tabla 2, Moorfields Manual: "With corneal involvement: doxycycline 100 mg once a day ... for 8 weeks"')),
    ]
    alertas = [
        SOLO_OFT + ' El uso en blefaritis y disfunción de glándulas de Meibomio no está en la ficha técnica.',
        'Contraindicada en el embarazo y en la lactancia; no se usa en menores de 8 años por riesgo de decoloración permanente de los dientes (CIMA 4.3 y 4.4; AAO PPP).',
        'Una revisión Cochrane concluye que no hay evidencia suficiente para sacar conclusiones sobre los antibióticos orales en la blefaritis crónica y que la doxiciclina puede dar más efectos adversos serios (Cochrane 2021).',
        'Los estudios con dosis subantimicrobianas usaron 40 mg al día o 20 mg dos veces al día (Cochrane 2021; IOVS 2011); esa presentación no está cargada aquí.',
        'La guía AAO la da una vez al día y la baja cuando hay mejoría; existe una presentación de liberación sostenida que reduce los efectos adversos (AAO PPP 2024).',
        'Fotosensibilidad, molestias digestivas, y rara vez seudotumor cerebral o síndrome de Stevens-Johnson; baja el efecto de anticonceptivos orales y potencia a la warfarina (AAO PPP 2024).',
    ]
    return ficha_oral(
        'doxiciclina', 'Doxiciclina', 'antibiotico', presentaciones, dosis_,
        {'comida': 'con_comida',
         'texto': 'Con la comida y un vaso de agua (200 ml) o leche, y esperar al menos una hora antes de acostarse para evitar irritar el esófago.',
         'fuente': cima('4.2 Forma de administración: "en el transcurso de una comida, acompañado de un vaso de agua (200 ml) o con leche ... al menos una hora antes de tumbarse"')},
        comerciales=['Vibracina'], usos=USOS, pediatria='solo_adulto',
        motivo_solo_adulto='Las tetraciclinas no se usan en menores de 8 años; en niños con blefaritis la guía AAO propone eritromicina o azitromicina.',
        alertas=alertas,
    )


def minociclina(c):
    cima = lambda d: oc.cima('minociclina', '51179', d)  # noqa: E731
    presentaciones = [pres('capsula-100-mg', 'capsula', mg=100, partible='no',
                           fuente=cima('Minocin 100 mg cápsulas duras ("Las cápsulas deben tragarse enteras")'))]
    dosis_ = [
        _o(indicacion='Blefaritis posterior y disfunción de glándulas de Meibomio (adultos)', poblacion='adulto', regimen='fija',
           unidad='mg', base='toma', min=50, max=100, tomas=2, estatus='off_label',
           condicion='Los estudios usaron 50 a 100 mg una o dos veces al día; la fuente no fija una pauta única. Con 100 mg por cápsula, 50 mg exige otra presentación',
           texto='50 a 100 mg, 1 o 2 veces al día; se baja cuando hay mejoría',
           fuente=c['mgd']('Dosis en estudios: "50 to 100 mg once or twice a day (doxycycline and minocycline)"')),
    ]
    alertas = [
        SOLO_OFT + ' El uso en blefaritis no está en la ficha técnica.',
        'Contraindicada en el embarazo, la lactancia y en menores de 8 años (CIMA 4.3 y 4.4).',
        'Puede manchar la piel, las uñas, la esclera, la conjuntiva, los dientes y el hueso (AAO PPP 2024).',
        'Una revisión Cochrane concluye que no hay evidencia suficiente sobre los antibióticos orales en la blefaritis crónica (Cochrane 2021).',
    ]
    return ficha_oral(
        'minociclina', 'Minociclina', 'antibiotico', presentaciones, dosis_,
        {'comida': 'con_comida',
         'texto': 'Con la comida y un vaso de agua (200 ml) o leche; tragar las cápsulas enteras y esperar al menos una hora antes de acostarse.',
         'fuente': cima('4.2 Forma de administración: cápsulas enteras, "en el transcurso de una comida", un vaso de agua (200 ml) o leche')},
        comerciales=['Minocin', 'Bagomicina'], usos=USOS, pediatria='solo_adulto',
        motivo_solo_adulto='Contraindicada en menores de 8 años (CIMA 4.3); en niños con blefaritis la guía AAO propone eritromicina o azitromicina.',
        alertas=alertas,
    )


def pirimetamina(c):
    cima = lambda d: oc.cima('pirimetamina', '19625', d)  # noqa: E731
    presentaciones = [pres('comprimido-25-mg', 'comprimido', mg=25, partible='no',
                           fuente=cima('Daraprim 25 mg comprimidos (la ficha no menciona ranura ni partición)'))]
    dosis_ = [
        _o(indicacion='Toxoplasmosis, incluida la retinocoroiditis: dosis de carga, día 1 (adultos inmunocompetentes)',
           poblacion='adulto', regimen='fija', unidad='mg', base='toma', min=100, max=100, tomas=1,
           condicion='Solo el primer día (el CDC acepta 1 o 2 días); siempre junto con sulfadiazina o clindamicina',
           fuente=cima('4.2 Toxoplasmosis, adultos inmunocompetentes: "Una dosis de carga de 100 mg de pirimetamina seguida de 25 a 50 mg de pirimetamina al día"')),
        _o(indicacion='Toxoplasmosis, incluida la retinocoroiditis: mantenimiento (adultos inmunocompetentes)',
           poblacion='adulto', regimen='fija', unidad='mg', base='toma', min=25, max=50, tomas=1,
           condicion='En la toxoplasmosis ocular el CDC da el tratamiento 4 a 6 semanas y luego reevalúa; con ácido folínico (leucovorina) en cada dosis',
           fuente=c['cdc']('Tabla ocular, adultos: "100 mg for one day as a loading dose, then 25 - 50 mg per day"; "Therapy should be given for 4 to 6 weeks, followed by reevaluation"')),
        _o(indicacion='Toxoplasmosis: dosis de carga, día 1 (niños de 3 a 6 años)', poblacion='pediatrico', regimen='por_peso',
           unidad='mg/kg', base='dia', min=2, max=2, tomas=1, tope_dia=(50, 'mg'),
           condicion='El CDC da la misma pauta en toxoplasmosis ocular de niños: 2 mg/kg el primer día; junto con sulfadiazina',
           fuente=cima('4.2 Niños de 3 a 6 años: "dosis de carga de pirimetamina 2 mg/kg peso corporal (hasta un máximo de 50 mg) seguida de una dosis de 1 mg/kg/día (dosis máxima de 25 mg)"')),
        _o(indicacion='Toxoplasmosis: mantenimiento (niños de 3 a 6 años)', poblacion='pediatrico', regimen='por_peso',
           unidad='mg/kg', base='dia', min=1, max=1, tomas=1, tope_dia=(25, 'mg'),
           condicion='El CDC da 1 mg/kg/día en toxoplasmosis ocular de niños, con ácido folínico',
           fuente=cima('4.2 Niños de 3 a 6 años: "1 mg/kg/día (dosis máxima de 25 mg)"')),
    ]
    disc = [
        discrepancia('Duración del tratamiento de la toxoplasmosis ocular',
                     [('CIMA-OFT-PIRIMETAMINA-19625', 'Daraprim (CIMA): no fija una duración para la forma ocular'),
                      ('WEB-OFT-ORAL-TOXOPLASMOSIS-TOXOPLASMOSIS/HCP', 'CDC: 4 a 6 semanas y luego reevaluar')],
                     'Se muestra la duración del CDC (4 a 6 semanas)', 'Es la única fuente que da duración para la retinocoroiditis.'),
    ]
    alertas = [
        SOLO_OFT + ' No carga malaria ni la toxoplasmosis congénita.',
        'Se usa siempre en combinación con un medicamento sinérgico: sulfadiazina o clindamicina (CIMA 4.2).',
        'Deprime la médula ósea en el 25 a 50 % de los pacientes con dosis terapéuticas; el folinato de calcio (ácido folínico) reduce el riesgo, y el hemograma se hace semanal durante el tratamiento y 2 semanas después (CIMA 4.4).',
        'Evitar en el primer trimestre del embarazo; no se recomienda en la lactancia (CDC; CIMA 4.6).',
        'Con antecedentes de convulsiones evitar dosis de carga altas (CIMA 4.4).',
        'Una lesión ya cicatrizada no se trata (CDC).',
    ]
    return ficha_oral(
        'pirimetamina', 'Pirimetamina', 'antiparasitario', presentaciones, dosis_,
        {'comida': 'indiferente', 'texto': 'La ficha técnica no fija relación con las comidas.',
         'fuente': cima('4.2 Posología y forma de administración (sin indicación sobre las comidas)')},
        comerciales=['Daraprim'], usos=USOS, discrepancias=disc, alertas=alertas,
        hepatico='Se usa con precaución; no hay recomendación general de reducir la dosis (CIMA 4.2 y 4.4).',
        fuente_ajuste=cima('4.2 Insuficiencia hepática'),
    )


# ---------------------------------------------------------------------------------------------- fichas ya existentes
def _extras(c):
    """Dosis y alertas oftálmicas que se suman a las 4 fichas ya cargadas: {id: (dosis, alertas)}."""
    hzo = c['hzo']
    hsv = c['hsv']
    uve = c['uveitis']
    ppp = c['ppp']
    aciclovir = (
        [
            _o(indicacion='Herpes zóster oftálmico (adultos)', poblacion='adulto', regimen='fija', unidad='mg', base='toma',
               min=800, max=800, tomas=5, estatus='off_label', condicion='7 a 10 días; es el tratamiento estándar según EyeWiki',
               presentaciones=['comprimido-800-mg'],
               fuente=hzo('"Oral acyclovir 800 mg PO five times daily for 7 to 10 days is the standard treatment."')),
            _o(indicacion='Queratitis herpética epitelial dendrítica (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
               base='toma', min=400, max=400, tomas=5, estatus='off_label', condicion='7 a 10 días',
               texto='400 mg, de 3 a 5 veces al día', presentaciones=['comprimido-400-mg'],
               fuente=hsv('App. VI, epitelial dendrítica: "Acyclovir (Zovirax): 400 mg 3-5 times daily for 7-10 days"')),
            _o(indicacion='Queratitis herpética epitelial geográfica (adultos)', poblacion='adulto', regimen='fija', unidad='mg',
               base='toma', min=800, max=800, tomas=5, estatus='off_label', condicion='14 a 21 días',
               presentaciones=['comprimido-800-mg'],
               fuente=hsv('App. VI, epitelial geográfica: "Acyclovir (Zovirax): 800 mg 5 times daily for 14-21 days"')),
            _o(indicacion='Profilaxis de queratitis herpética recurrente (adultos)', poblacion='adulto', regimen='fija',
               unidad='mg', base='toma', min=400, max=400, tomas=2, estatus='off_label',
               condicion='Al menos un año; con el antiviral oral de profilaxis mientras se usen corticoides tópicos',
               presentaciones=['comprimido-400-mg'],
               fuente=hsv('Profilaxis: "Acyclovir (Zovirax): 400 mg twice daily for one year"; HEDS: es uno de los dos antivirales que reducen las recurrencias')),
            _o(indicacion='Queratitis herpética (niños), dosis de tratamiento', poblacion='pediatrico', regimen='por_peso',
               unidad='mg/kg', base='dia', min=12, max=80, estatus='off_label', presentaciones=['suspension-80-mg-ml'],
               condicion='Fuente secundaria (revista profesional) que cita el estudio de Schwartz y Holland; dosis divididas',
               fuente=c['bert']('"The range that was used in the study by Gary Schwartz, MD, and Edward Holland, MD, was 12 to 80 mg/kg/day in divided doses."')),
            _o(indicacion='Queratitis herpética (niños), supresión', poblacion='pediatrico', regimen='por_peso',
               unidad='mg/kg', base='dia', min=12, max=20, estatus='off_label', presentaciones=['suspension-80-mg-ml'],
               condicion='Fuente secundaria (revista profesional)',
               fuente=c['bert']('"For children the suppression dose was found to range between 12 to 20 mg/kg/day."')),
        ],
        [
            'Uso oftalmológico: en el estudio HEDS, agregar aciclovir oral de dosis alta al tratamiento tópico de la queratitis epitelial no evitó la queratitis estromal posterior (guía MEEI/Harvard).',
            'Precaución en mayores de 65 años y en insuficiencia renal (nefrotoxicidad; más reacciones del sistema nervioso en ancianos). Niños y atópicos pueden requerir dosis relativamente más altas (guía MEEI/Harvard).',
            'Las dosis pediátricas oftálmicas vienen de un artículo de revista profesional, no de una guía; revisar con oftalmología pediátrica.',
        ],
    )
    azitromicina = (
        [
            _o(indicacion='Blefaritis y disfunción de glándulas de Meibomio (adultos), pulsos de 3 días', poblacion='adulto',
               regimen='fija', unidad='mg', base='toma', min=500, max=500, tomas=1, estatus='off_label',
               condicion='500 mg/día durante 3 días; tres ciclos con 7 días de descanso entre ciclos (serie abierta de 13 pacientes)',
               presentaciones=['comprimido-500-mg'],
               fuente=ppp('"oral azithromycin 500 mg per day for 3 days in three cycles with 7-day intervals yielded good clinical improvement in 13 patients"')),
            _o(indicacion='Blefaritis y disfunción de glándulas de Meibomio (adultos), pulso semanal', poblacion='adulto',
               regimen='fija', unidad='mg', base='toma', min=1000, max=1000, tomas=1, intervalo_h=168, estatus='off_label',
               condicion='1 g por semana durante 3 semanas', presentaciones=['comprimido-500-mg'],
               fuente=ppp('"Another acceptable dosing regimen for pulsed oral azithromycin in adults is 1 g per week for 3 weeks."')),
            _o(indicacion='Blefaritis (niños)', poblacion='pediatrico', regimen='por_peso', unidad='mg/kg', base='dia', min=5, max=5,
               tomas=1, estatus='off_label', condicion='2 meses; ayudó en una serie pequeña de casos', presentaciones=['suspension-40-mg-ml'],
               fuente=ppp('"A pediatric dosing regimen for azithromycin of 5 mg/kg daily for 2 months was shown to be helpful for clinical improvement in a small case series."')),
        ],
        [
            'Uso oftalmológico (blefaritis, no está en la ficha técnica): por vía oral puede producir arritmias cardíacas en pacientes con problemas cardiovasculares; en una cohorte de Medicaid (Tennessee) hubo un pequeño aumento absoluto de muertes cardiovasculares, mayor en quienes ya tenían alto riesgo cardiovascular (AAO PPP 2024; alerta FDA 2013).',
            'Es la alternativa a las tetraciclinas en niños y en mujeres en edad fértil (AAO PPP 2024).',
        ],
    )
    prednisona = (
        [
            _o(indicacion='Uveítis no infecciosa, dosis inicial (adultos)', poblacion='adulto', regimen='por_peso', unidad='mg/kg',
               base='dia', min=1, max=1.5, tomas=1, estatus='off_label',
               condicion='Después se baja de forma gradual según la respuesta clínica; bajar muy rápido o suspender pronto puede causar recaída',
               fuente=uve('"Initial dosing of oral prednisone is typically 1-1.5 mg/kg/day."; "Too rapid tapering or early discontinuation ... may lead to disease recurrence."')),
            _o(indicacion='Arteritis de células gigantes (adultos), guía británica', poblacion='adulto', regimen='fija', unidad='mg',
               base='dia', min=40, max=60, tomas=1, estatus='off_label',
               condicion='Prednisona o prednisolona; el descenso lleva 12 a 18 meses',
               fuente=c['bsr']('Rec. 3: "The standard initial glucocorticoid dose for GCA is 40-60 mg oral prednis(ol)one per day."')),
            _o(indicacion='Arteritis de células gigantes (adultos), EyeWiki', poblacion='adulto', regimen='por_peso', unidad='mg/kg',
               base='dia', min=1, max=1, tomas=1, tope_dia=(100, 'mg'), estatus='off_label',
               condicion='Rango de 40 a 100 mg/día; la dosis habitual de inicio es 1 mg/kg/día',
               fuente=c['gca']('"Suggested dosages of prednisone for initiation of treatment range from 40-100 mg per day with a common starting dosage of 1 mg/kg/day."')),
            _o(indicacion='Retinocoroiditis toxoplásmica, corticoide acompañante (adultos)', poblacion='adulto', regimen='por_peso',
               unidad='mg/kg', base='dia', min=0.5, max=1, tomas=1, estatus='off_label',
               condicion='Se empieza unos días después del antiparasitario y dura cerca de 1 mes con descenso gradual; la decisión es del oftalmólogo',
               fuente=c['dunay']('Nota a la Tabla 1: "concomitant steroids (prednisone at 0.5 to 1 mg/kg/day) with gradual tapering can be used; this decision is best made by the ophthalmologist"')),
        ],
        [
            'Uso oftalmológico: en la neuritis óptica aguda, la prednisona oral sola (1 mg/kg/día por 14 días) resultó ineficaz y aumentó el riesgo de nuevos episodios en el ONTT; no es la pauta de la neuritis óptica (ONTT, NEJM 1992).',
            'En arteritis de células gigantes con pérdida visual la guía británica usa pulsos de metilprednisolona intravenosa (500 mg a 1 g al día hasta 3 días); esa pauta no está cargada aquí.',
            'Los corticoides sistémicos pueden causar catarata, aumento de la presión intraocular y glaucoma; con más de 7,5 mg/día por más de 3 meses hay que considerar ahorradores de esteroides, y dar calcio y vitamina D (EyeWiki, tratamiento de uveítis).',
        ],
    )
    cotrimoxazol = (
        [
            _o(indicacion='Retinocoroiditis toxoplásmica: tratamiento (adultos), en mg de trimetoprima', poblacion='adulto',
               regimen='fija', unidad='mg', base='toma', min=160, max=160, tomas=2, estatus='off_label',
               condicion='45 días; en el estudio, 800 mg de sulfametoxazol con 160 mg de trimetoprima dos veces al día',
               presentaciones=['comprimido-forte-160-800-mg'],
               fuente=c['felix']('"trimethoprim-sulfamethoxazole (800 mg/160 mg) twice daily for 45 days" (el resumen invierte el orden de las cifras)')),
            _o(indicacion='Retinocoroiditis toxoplásmica: profilaxis de recurrencias (adultos), en mg de trimetoprima', poblacion='adulto',
               regimen='fija', unidad='mg', base='toma', min=160, max=160, intervalo_h=48, estatus='off_label',
               condicion='Un comprimido forte cada 2 días hasta 1 año; redujo las recurrencias a 0 de 46 frente a 6 de 47 con placebo',
               presentaciones=['comprimido-forte-160-800-mg'],
               fuente=c['felix']('"trimethoprim/sulfamethoxazole tablet every 2 days" vs placebo; "0 of 46 (0%) and 6 of 47 (12.80%)"')),
        ],
        [
            'Uso oftalmológico (toxoplasmosis ocular): el CDC lo usa como alternativa a la pirimetamina con sulfadiazina, que es el esquema clásico (CDC).',
            'Evitar cerca del término del embarazo por riesgo de hiperbilirrubinemia y kernicterus en el recién nacido; no se recomienda en menores de 2 meses (CDC).',
        ],
    )
    return {'aciclovir': aciclovir, 'azitromicina': azitromicina, 'prednisona': prednisona, 'cotrimoxazol': cotrimoxazol}


def _discrepancias_extra(c):
    return {
        'prednisona': [
            discrepancia('Dosis inicial en arteritis de células gigantes',
                         [(c['bsr']('x')['ref'], 'Guía británica (BSR): 40 a 60 mg/día de prednisona o prednisolona'),
                          (c['gca']('x')['ref'], 'EyeWiki: 40 a 100 mg/día, habitual 1 mg/kg/día')],
                         'Se muestran las dos pautas, cada una con su fuente',
                         'Son guías distintas; el rango de EyeWiki llega a 100 mg/día.'),
        ],
        'cotrimoxazol': [
            discrepancia('Intervalo de la profilaxis de la retinocoroiditis',
                         [(c['felix']('x')['ref'], 'Felix 2014 (ensayo): un comprimido cada 2 días por 1 año'),
                          (c['dunay']('x')['ref'], 'Dunay 2018 (revisión): 160/800 mg cada 3 días hasta 20 meses')],
                         'Se muestra la pauta del ensayo (cada 2 días)', 'Es el único ensayo aleatorizado con placebo citado.'),
        ],
    }


# ---------------------------------------------------------------------------------------------- API del módulo
def _construir():
    if 'nuevas' in _cache:
        return _cache
    c = _citas()
    _cache['nuevas'] = {f['id']: f for f in (
        acetazolamida(c), metazolamida(c), valaciclovir(c), famciclovir(c), doxiciclina(c), minociclina(c), pirimetamina(c))}
    _cache['extras'] = _extras(c)
    _cache['disc'] = _discrepancias_extra(c)
    return _cache


def fuentes():
    _construir()
    return list(oc.FUENTES.values())


def fichas():
    return dict(_construir()['nuevas'])


def marcar(fichas_):
    """Agrega `usos` y las dosis, alertas y discrepancias oftálmicas a las fichas ya existentes (modifica el dict)."""
    cache = _construir()
    for id_, (dosis_, alertas) in cache['extras'].items():
        f = fichas_[id_]
        f['usos'] = list(USOS)
        f['dosis'] = f['dosis'] + dosis_
        f['alertas'] = f['alertas'] + alertas
        f['discrepancias'] = f['discrepancias'] + cache['disc'].get(id_, [])
        # `usos` va en la cabecera del YAML, junto a `ambitos`
        orden = list(f)
        orden.remove('usos')
        orden.insert(orden.index('ambitos') + 1, 'usos')
        fichas_[id_] = {k: f[k] for k in orden}
    return fichas_
