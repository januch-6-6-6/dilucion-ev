"""Tanda 1, resto (32 medicamentos de urgencia/SAMU). Valores citados; compatibilidad en Y la llena la matriz global."""
from .comun import C, P, PED, fu, fuente_cima, fuente_pediamecum, meta

CIMA = {
    'dopamina': ('90395', 'Dopamina Basi 40 mg/ml concentrado para solución para perfusión'),
    'dobutamina': ('61952', 'Dobutamina Hospira 12,5 mg/ml concentrado para solución para perfusión'),
    'fenilefrina': ('85084', 'Fenilefrina Aguettant 100 microgramos/ml solución inyectable y para perfusión'),
    'nitroglicerina': ('57127', 'Solinitrina Fuerte 5 mg/ml concentrado para solución para perfusión'),
    'labetalol': ('89082', 'Labetalol S.A.L.F. 5 mg/ml solución inyectable y para perfusión'),
    'lidocaina': ('44792', 'Lidocaína B. Braun 20 mg/ml solución inyectable'),
    'furosemida': ('62168', 'Furosemida Physan 20 mg/2 ml solución inyectable'),
    'metoclopramida': ('89715', 'Metoclopramida Basi 5 mg/ml solución inyectable y para perfusión'),
    'ondansetron': ('59071', 'Zofran 4 mg solución inyectable'),
    'ketorolaco': ('70102', 'Ketorolaco trometamol Normon 30 mg/ml solución inyectable'),
    'tramadol': ('59086', 'Adolonta 100 mg/2 ml solución inyectable y para perfusión'),
    'metamizol': ('63430', 'Metamizol Normon 0,4 g/ml solución inyectable y para perfusión'),
    'hidrocortisona': ('52105', 'Actocortina 373 mg polvo para solución inyectable (hidrocortisona fosfato sódico)'),
    'dexametasona': ('86438', 'Dexametasona Kalceks 4 mg/ml solución inyectable y para perfusión'),
    'metilprednisolona': ('71864', 'Metilprednisolona Normon 20 mg polvo y disolvente para solución inyectable'),
    'fenitoina': ('65372', 'Fenitoína Altan 50 mg/ml solución inyectable'),
    'levetiracetam': ('100146033', 'Keppra 100 mg/ml concentrado para solución para perfusión'),
    'diazepam': ('89559', 'Diazepam Basi 5 mg/ml solución inyectable'),
    'naloxona': ('82819', 'Fomed 0,4 mg/ml solución inyectable y para perfusión (naloxona)'),
    'flumazenil': ('82049', 'Flumazenilo Hikma 0,1 mg/ml solución inyectable y para perfusión'),
    'acido-tranexamico': ('53939', 'Amchafibrin 500 mg solución inyectable (ácido tranexámico)'),
    'heparina': ('58691', 'Heparina sódica Rovi 1.000 UI/ml y 5.000 UI/ml solución inyectable'),
    'insulina-cristalina': ('02230003', 'Actrapid 100 UI/ml solución inyectable en vial (insulina humana)'),
    'bicarbonato-de-sodio': ('60324', 'Bicarbonato sódico 1M Grifols solución inyectable'),
    'glucosa-30': ('67634', 'Glucosa B. Braun 30 % solución para perfusión'),
    'propofol': ('58785', 'Diprivan 10 mg/ml emulsión inyectable y para perfusión (propofol)'),
    'etomidato': ('64095', 'Etomidato-Lipuro 2 mg/ml emulsión inyectable'),
    'rocuronio': ('61141', 'Esmeron 10 mg/ml solución inyectable y para perfusión (rocuronio)'),
    'succinilcolina': ('84088', 'Suxametonio Ethypharm 50 mg/ml solución inyectable y para perfusión'),
}

PEDIAMECUM = {
    'dopamina': 'Dopamina', 'dobutamina': 'Dobutamina', 'fenilefrina': 'Fenilefrina', 'nitroglicerina': 'Nitroglicerina',
    'labetalol': 'Labetalol', 'lidocaina': 'Lidocaína', 'ondansetron': 'Ondansetrón', 'furosemida': 'Furosemida',
    'ketorolaco': 'Ketorolaco', 'hidrocortisona': 'Hidrocortisona', 'dexametasona': 'Dexametasona', 'metilprednisolona': 'Metilprednisolona',
    'levetiracetam': 'Levetiracetam', 'diazepam': 'Diazepam', 'naloxona': 'Naloxona', 'flumazenil': 'Flumazenilo', 'acido-tranexamico': 'Ácido tranexámico',
    'heparina': 'Heparina', 'etomidato': 'Etomidato', 'rocuronio': 'Rocuronio', 'succinilcolina': 'Succinilcolina',
}
PEDIAMECUM_SLUG = {'succinilcolina': 'suxametonio', 'flumazenil': 'flumazenilo'}

FDA = lambda k, d: fu(f'FDA-{k}', d)  # noqa: E731

FUENTES_EXTRA = [
    {
        'id': 'FDA-POTASIO',
        'titulo': 'Potassium chloride for injection concentrate — Prescribing information (Dosage and administration, Warnings)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=559a0a8c-a8fe-40a5-b196-21f9308780ab',
        'anio': 2026,
        'consultado': '2026-10-01',
    },
    {
        'id': 'FDA-GLUCONATO-CALCIO',
        'titulo': 'Calcium gluconate injection 100 mg/ml — Prescribing information (sección 2, Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=13d7cfc9-ff7a-437e-8c21-d9709ac07d48',
        'anio': 2026,
        'consultado': '2026-10-01',
    },
    {
        'id': 'FDA-DEXTROSA-50',
        'titulo': 'Dextrose 50 % injection — Prescribing information (Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=3842a9c0-8b15-1c94-e063-6394a90ae120',
        'anio': 2025,
        'consultado': '2026-10-01',
    },
    {
        'id': 'FDA-LIDOCAINA-SG5',
        'titulo': 'Lidocaine hydrochloride and 5% dextrose injection — Prescribing information (Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1bf999b5-e290-dcbd-e063-6294a90a2bab',
        'anio': 2026,
        'consultado': '2026-10-01',
    },
]

CIMA_PEND = {}  # se completa en los lotes siguientes


def fuentes():
    lista = [fuente_cima(k, nreg, nombre) for k, (nreg, nombre) in {**CIMA, **CIMA_PEND}.items()]
    lista += [fuente_pediamecum(k, n) for k, n in PEDIAMECUM.items()]
    for f in lista:
        if f['id'].startswith('PEDIAMECUM-'):
            k = f['id'][len('PEDIAMECUM-'):].lower()
            if k in PEDIAMECUM_SLUG:
                f['url'] = f"https://www.aeped.es/comite-medicamentos/pediamecum/{PEDIAMECUM_SLUG[k]}"
    return lista + FUENTES_EXTRA


# --- Atajos para escribir fichas compactas ---
def pres(id_, forma, valor, unidad, ml, fuente):
    return {'id': id_, 'forma': forma, 'cantidad': {'valor': valor, 'unidad': unidad}, 'volumenMl': ml, 'fuente': fuente}


def dil(descripcion, valor, unidad, volumen_final, fuente):
    return {'descripcion': descripcion, 'cantidad': {'valor': valor, 'unidad': unidad}, 'volumenFinalMl': volumen_final, 'fuente': fuente}


def dosis(indicacion, poblacion, unidad, fuente, mn=None, mx=None, maxima=None, tope=None):
    d = {'indicacion': indicacion, 'poblacion': poblacion, 'unidad': unidad}
    if mn is not None:
        d['min'] = mn
    if mx is not None:
        d['max'] = mx
    if maxima is not None:
        d['maximaAbsoluta'] = maxima
    if tope is not None:
        d['topeAdulto'] = {'valor': tope[0], 'unidad': tope[1]}
    d['fuente'] = fuente
    return d


def conc(valor, unidad, fuente):
    return {'valor': valor, 'unidad': unidad, 'fuente': fuente}


def ficha(id_, nombre, grupo, ambitos, alto_riesgo, presentaciones, dilucion, administracion, dosis_, estabilidad,
          interacciones, efectos, alertas, reconstitucion=None, discrepancias=()):
    return {
        'id': id_, 'nombre': nombre, 'comerciales': [], 'grupo': grupo, 'ambitos': ambitos, 'altoRiesgo': alto_riesgo,
        'presentaciones': presentaciones, 'reconstitucion': reconstitucion, 'dilucion': dilucion,
        'administracion': administracion, 'dosis': dosis_,
        'sinDosisPediatrica': not any(d['poblacion'] == 'pediatrico' for d in dosis_),
        'estabilidad': estabilidad, 'compatibilidad': [], 'interaccionesGraves': interacciones,
        'efectosAdversos': efectos, 'alertas': alertas, 'meta': meta(discrepancias),
    }


def ea(frecuentes, graves, vigilar, fuente):
    return {'frecuentes': frecuentes, 'graves': graves, 'vigilar': vigilar, 'fuente': fuente}


def ix(con, efecto, fuente):
    return {'con': con, 'efecto': efecto, 'fuente': fuente}


URG = ['samu', 'urgencia', 'upc']
URG_H = ['samu', 'urgencia', 'upc', 'hospitalizacion']
ALTO = 'Medicamento de alto riesgo.'


def fichas(stab=None):
    F = {}

    F['dopamina'] = ficha(
        'dopamina', 'Dopamina', 'vasoactivo', URG, True,
        [pres('amp-200mg-5ml', 'ampolla', 200, 'mg', 5, P('Anexo 6, Dopamina: 200 mg/5 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(4, 'mg', P('Anexo 6, Dopamina: 4 mg/ml (habitual 400 mg/100 ml)')),
         'estandar': [dil('400 mg en 100 ml (4 mg/ml)', 400, 'mg', 100, P('Anexo 6, Dopamina: habitual 400 mg/100 ml')),
                      dil('200 mg en 250 ml (800 mcg/ml)', 200, 'mg', 250, C('dopamina', '6.6: 5 ml (200 mg) en 250 ml → 800 mcg/ml')),
                      dil('200 mg en 500 ml (400 mcg/ml)', 200, 'mg', 500, C('dopamina', '6.6: 5 ml (200 mg) en 500 ml → 400 mcg/ml'))]},
        {'vias': ['infusion_continua'], 'texto': 'Solo diluida, en perfusión continua por bomba, en vena de grueso calibre (riesgo de isquemia tisular por extravasación). No mezclar con soluciones alcalinas como bicarbonato. Ajustar según PA, diuresis y perfusión.', 'requiereBomba': True, 'fuente': C('dopamina', '4.2 Forma de administración; 6.2')},
        [dosis('Inicio en respuesta modesta esperada', 'adulto', 'mcg/kg/min', C('dopamina', '4.2: iniciar a 2,5 mcg/kg/min'), mn=2.5, mx=5),
         dosis('Casos graves: aumentar de 5 a 10 mcg/kg/min hasta efecto', 'adulto', 'mcg/kg/min', C('dopamina', '4.2: hasta 20–50 mcg/kg/min'), mn=5, mx=20, maxima=50),
         dosis('Infusión continua (niños)', 'pediatrico', 'mcg/kg/min', PED('dopamina', 'Niños: 5–20 mcg/kg/min; máx. 50 mcg/kg/min'), mn=5, mx=20, maxima=50)],
        {'fuente': C('dopamina', '6.3: utilizar inmediatamente después de la dilución')},
        [ix('Anestésicos halogenados o ciclopropano', 'Arritmias ventriculares e hipertensión; evitar', C('dopamina', '4.5')),
         ix('Inhibidores de la monoaminooxidasa (IMAO)', 'Potenciación marcada del efecto presor', C('dopamina', '4.5'))],
        ea(['Cefalea', 'Náuseas y vómitos', 'Palpitaciones', 'Disnea'], ['Taquiarritmias y extrasístoles ventriculares', 'Dolor anginoso', 'Necrosis o gangrena por extravasación'], ['PA, FC y ECG continuos', 'Diuresis', 'Sitio de infusión'], C('dopamina', '4.8')),
        [ALTO, 'No administrar sin diluir. Incompatible con bicarbonato de sodio.'],
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: seguridad no establecida en niños', 'Pediamécum: 5–20 mcg/kg/min, máx. 50'], 'decision': 'Se registra la pauta de Pediamécum, marcada como fuente pediátrica.'}],
    )

    F['dobutamina'] = ficha(
        'dobutamina', 'Dobutamina', 'vasoactivo', URG, True,
        [pres('amp-250mg-5ml', 'ampolla', 250, 'mg', 5, P('Anexo 6, Dobutamina: 250 mg/5 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(5, 'mg', C('dobutamina', '4.2: no superar 5 mg/ml (5000 mcg/ml)')),
         'estandar': [dil('250 mg en 100 ml (2,5 mg/ml)', 250, 'mg', 100, P('Anexo 6, Dobutamina: habitual 250 mg/100 ml')),
                      dil('250 mg en 250 ml (1 mg/ml)', 250, 'mg', 250, C('dobutamina', '4.2: 250 mg en 250 ml = 1000 mcg/ml')),
                      dil('250 mg en 50 ml (5 mg/ml), restricción de volumen', 250, 'mg', 50, C('dobutamina', '4.2: 250 mg en 50 ml = 5000 mcg/ml'))]},
        {'vias': ['infusion_continua'], 'texto': 'Diluir justo antes de usar en SG5 %, SF o Ringer lactato y administrar en perfusión continua por bomba. Ajustar según FC, PA, diuresis y gasto cardíaco. Retirar gradualmente.', 'requiereBomba': True, 'fuente': C('dobutamina', '4.2')},
        [dosis('Perfusión habitual (rango 0,5–40)', 'adulto', 'mcg/kg/min', C('dobutamina', '4.2: mayoría responde a 2,5–10; raramente hasta 40 mcg/kg/min'), mn=2.5, mx=10, maxima=40),
         dosis('Perfusión continua (niños)', 'pediatrico', 'mcg/kg/min', PED('dobutamina', 'Neonatos y niños: 2–15 mcg/kg/min; máx. 40'), mn=2, mx=15, maxima=40)],
        {'ambienteH': 12, 'refrigeradoH': 24, 'fuente': C('dobutamina', '6.3: 24 h a 15–25 °C si dilución aséptica estricta; si no, 24 h en refrigerador o 12 h a temperatura ambiente (se registra lo conservador)')},
        [ix('Betabloqueadores', 'Disminuyen el efecto inotrópico; posible vasoconstricción', C('dobutamina', '4.5')),
         ix('Anestésicos inhalatorios', 'Mayor riesgo de arritmias ventriculares', C('dobutamina', '4.5'))],
        ea(['Cefalea', 'Náuseas', 'Palpitaciones'], ['Taquiarritmias y extrasístoles ventriculares', 'Angina', 'Hipotensión o hipertensión'], ['FC, PA y ECG continuos', 'Potasio (hipokalemia)'], P('Anexo 6, Dobutamina: RAM')),
        [ALTO, 'Incompatible con bicarbonato de sodio y otras soluciones alcalinas (furosemida, fenitoína).'],
    )

    F['fenilefrina'] = ficha(
        'fenilefrina', 'Fenilefrina', 'vasoactivo', URG, True,
        [pres('amp-10mg-1ml', 'ampolla', 10, 'mg', 1, P('Anexo 4 y 6, Fenilefrina: 10 mg/ml'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': [dil('40 mg en 100 ml (400 mcg/ml)', 40, 'mg', 100, P('Anexo 6, Fenilefrina: habitual 40 mg/100 ml')),
                      dil('10 mg en 100 ml (100 mcg/ml) para bolos', 10, 'mg', 100, C('fenilefrina', 'Presentación lista de 100 mcg/ml para bolo IV'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV de 50–100 mcg repetible, o infusión continua por bomba. No usar soluciones de color café o con precipitado. La extravasación puede causar necrosis.', 'requiereBomba': True, 'fuente': P('Anexo 6, Fenilefrina: precauciones')},
        [dosis('Bolo IV (no superar 100 mcg por bolo)', 'adulto', 'mcg', C('fenilefrina', '4.2: 50–100 mcg'), mn=50, mx=100),
         dosis('Infusión continua', 'adulto', 'mcg/min', C('fenilefrina', '4.2: inicio 25–50, hasta 100 mcg/min'), mn=25, mx=100),
         dosis('Hipotensión/shock: infusión (niños)', 'pediatrico', 'mcg/kg/min', PED('fenilefrina', 'Infusión IV 0,1–0,5 mcg/kg/min'), mn=0.1, mx=0.5),
         dosis('Hipotensión/shock: bolo IV (niños)', 'pediatrico', 'mcg/kg', PED('fenilefrina', 'Bolo IV 5–20 mcg/kg cada 10–15 min'), mn=5, mx=20, tope=(100, 'mcg'))],
        {'fuente': C('fenilefrina', '6.3: una vez abierto, utilizar inmediatamente')},
        [ix('IMAO no selectivos', 'Hipertensión paroxística e hipertermia posiblemente mortal (contraindicado)', C('fenilefrina', '4.5')),
         ix('Antidepresivos tricíclicos', 'Hipertensión paroxística con posible arritmia', C('fenilefrina', '4.5'))],
        ea(['Náuseas y vómitos', 'Cefalea'], ['Bradicardia refleja', 'Hipertensión', 'Arritmias', 'Necrosis por extravasación'], ['PA y FC frecuentes', 'Sitio de infusión'], C('fenilefrina', '4.8')),
        [ALTO, 'La ampolla de 10 mg/ml debe diluirse; no confundir con la presentación de 100 mcg/ml.'],
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: sin datos en niños', 'Pediamécum: bolo 5–20 mcg/kg; infusión 0,1–0,5 mcg/kg/min'], 'decision': 'Se registra la pauta de Pediamécum con tope de bolo adulto de 100 mcg.'}],
    )

    F['nitroglicerina'] = ficha(
        'nitroglicerina', 'Nitroglicerina', 'antihipertensivo', URG, False,
        [pres('amp-50mg-10ml', 'ampolla', 50, 'mg', 10, C('nitroglicerina', '6.6: ampolla de 10 ml con 50 mg (5 mg/ml)'))],
        {'sueros': ['SG5', 'SF'],
         'estandar': [dil('50 mg en 500 ml (100 mcg/ml), retirando 10 ml del suero', 50, 'mg', 500, C('nitroglicerina', '6.6: 1 ampolla de 50 mg en 500 ml → 100 mcg/ml'))]},
        {'vias': ['infusion_continua'], 'texto': 'Perfusión continua por bomba con monitorización de PA y FC. Preparar en envase de vidrio o polietileno: el PVC absorbe 40–80 % del fármaco. No bajar la PAS más de 10–15 mmHg en normotensos.', 'requiereBomba': True, 'fuente': C('nitroglicerina', '4.2; 6.2')},
        [dosis('Inicio (aumentar 10–20 mcg/min cada 5–10 min)', 'adulto', 'mcg/min', C('nitroglicerina', '4.2: inicio 10–20 mcg/min; efectiva 50–100'), mn=10, mx=100),
         dosis('Angina grave, IAM o edema pulmonar', 'adulto', 'mg/h', C('nitroglicerina', '4.2: 2–8 mg/h; máx. excepcional 10 mg/h'), mn=2, mx=8, maxima=10),
         dosis('Infusión continua (niños)', 'pediatrico', 'mcg/kg/min', PED('nitroglicerina', 'Inicio 0,25–0,5; habitual 1–3 mcg/kg/min'), mn=0.25, mx=3)],
        {'fuente': C('nitroglicerina', '6.3 (no informa estabilidad de la dilución)')},
        [ix('Inhibidores de la fosfodiesterasa 5 (sildenafilo, tadalafilo, vardenafilo)', 'Hipotensión grave; contraindicado', C('nitroglicerina', '4.5')),
         ix('Riociguat', 'Potenciación del efecto hipotensor; contraindicado', C('nitroglicerina', '4.5'))],
        ea(['Cefalea', 'Rubor', 'Mareo'], ['Hipotensión', 'Taquicardia refleja', 'Metahemoglobinemia (dosis altas)'], ['PA y FC continuas'], C('nitroglicerina', '4.8')),
        ['Usar envase de vidrio o polietileno y equipo sin PVC.', 'Contraindicada con sildenafilo y similares.'],
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Protocolo Pucón 2022 no incluye nitroglicerina'], 'decision': 'Ficha basada en CIMA (y Pediamécum para niños); confirmar presentación disponible en Chile.'}],
    )

    F['labetalol'] = ficha(
        'labetalol', 'Labetalol', 'antihipertensivo', URG_H, False,
        [pres('amp-100mg-20ml', 'ampolla', 100, 'mg', 20, P('Anexo 6, Labetalol: 100 mg/20 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(5, 'mg', P('Anexo 6, Labetalol: 1 a 5 mg/ml')),
         'estandar': [dil('200 mg en 200 ml (1 mg/ml)', 200, 'mg', 200, C('labetalol', '4.2: 2 ampollas de 100 mg diluidas a 200 ml')),
                      dil('100 mg en 100 ml (1 mg/ml)', 100, 'mg', 100, P('Anexo 6, Labetalol: habitual 100 mg/100 ml'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV de 50 mg en 1 minuto, repetible cada 5 min (total máx. 200 mg), o perfusión a 1 mg/ml. Paciente acostado. Usar vía exclusiva.', 'tiempoMinimoMin': 1, 'fuente': C('labetalol', '4.2')},
        [dosis('Hipertensión grave: bolo (total máx. 200 mg)', 'adulto', 'mg', C('labetalol', '4.2: 50 mg cada 5 min hasta 200 mg'), mn=50, mx=50, maxima=200),
         dosis('Perfusión', 'adulto', 'mg/h', C('labetalol', '4.2: habitual 160 mg/h; embarazo desde 20 mg/h'), mn=20, mx=160),
         dosis('Hipertensión grave: bolo (niños)', 'pediatrico', 'mg/kg', PED('labetalol', '0,2–1 mg/kg/dosis, máx. 40 mg'), mn=0.2, mx=1, tope=(40, 'mg')),
         dosis('Emergencia hipertensiva: infusión (niños)', 'pediatrico', 'mg/kg/h', PED('labetalol', '0,25–3 mg/kg/h'), mn=0.25, mx=3)],
        {'ambienteH': 24, 'fuente': C('labetalol', '6.3: estabilidad en uso de 24 h a 25 °C; microbiológicamente usar de inmediato')},
        [ix('Otros antihipertensivos', 'Sinergismo aditivo: hipotensión', C('labetalol', '4.5')),
         ix('AINE', 'Reducen el efecto hipotensor', C('labetalol', '4.5'))],
        ea(['Hipotensión ortostática', 'Fatiga', 'Cefalea', 'Náuseas', 'Congestión nasal'], ['Insuficiencia cardíaca', 'Broncoespasmo', 'Bloqueo cardíaco'], ['PA y FC', 'Mantener al paciente acostado 3 h tras la dosis'], P('Anexo 6, Labetalol: RAM')),
        ['Incompatible con bicarbonato de sodio.'],
    )

    F['lidocaina'] = ficha(
        'lidocaina', 'Lidocaína (antiarrítmico)', 'antiarritmico', URG, True,
        [pres('amp-2pct-5ml', 'ampolla 2 %', 100, 'mg', 5, P('Anexo 6, Lidocaína 2 %: ampollas de 5 y 10 ml (20 mg/ml)')),
         pres('amp-2pct-10ml', 'ampolla 2 %', 200, 'mg', 10, P('Anexo 6, Lidocaína 2 %: ampollas de 5 y 10 ml (20 mg/ml)'))],
        {'sueros': ['SG5', 'SF'], 'concentracionMax': conc(8, 'mg', P('Anexo 6, Lidocaína: máximo 8 mg/ml en infusión continua')),
         'estandar': [dil('1 g en 250 ml (4 mg/ml)', 1, 'g', 250, fu('FDA-LIDOCAINA-SG5', 'Solución 0,4 % (4 mg/ml)')),
                      dil('2 g en 250 ml (8 mg/ml), restricción de volumen', 2, 'g', 250, fu('FDA-LIDOCAINA-SG5', 'Solución 0,8 % (8 mg/ml)'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV de 1–1,5 mg/kg a 25–50 mg/min, seguido de infusión continua de 1–4 mg/min con bomba y ECG continuo. Reducir la velocidad a la mitad tras 24 h (acumulación).', 'requiereBomba': True, 'fuente': fu('FDA-LIDOCAINA-SG5', 'Dosage and administration')},
        [dosis('Arritmia ventricular: bolo', 'adulto', 'mg/kg', fu('FDA-LIDOCAINA-SG5', 'Bolo 1,0–1,5 mg/kg'), mn=1, mx=1.5),
         dosis('Infusión de mantención', 'adulto', 'mg/min', fu('FDA-LIDOCAINA-SG5', '1–4 mg/min'), mn=1, mx=4),
         dosis('Antiarrítmico: bolo (niños)', 'pediatrico', 'mg/kg', PED('lidocaina', 'Bolo IV 1 mg/kg'), mn=1, mx=1, tope=(100, 'mg')),
         dosis('Antiarrítmico: infusión (niños)', 'pediatrico', 'mcg/kg/min', PED('lidocaina', 'Infusión 20–50 mcg/kg/min'), mn=20, mx=50)],
        {'fuente': C('lidocaina', '6.3: tras la dilución, usar inmediatamente')},
        [ix('Inhibidores de su metabolismo (p. ej., cimetidina)', 'Concentraciones tóxicas con dosis altas repetidas', C('lidocaina', '4.5')),
         ix('Otros antiarrítmicos de clase I', 'Riesgo de efectos adversos cardíacos graves; evitar', C('lidocaina', '4.5')),
         ix('Adrenalina o noradrenalina', 'Potencian los efectos adversos cardíacos', C('lidocaina', '4.5'))],
        ea(['Mareo', 'Somnolencia', 'Parestesias', 'Visión borrosa'], ['Convulsiones', 'Depresión respiratoria', 'Bradicardia y paro cardíaco', 'Metahemoglobinemia'], ['ECG continuo', 'Nivel de conciencia (signos de toxicidad)'], fu('FDA-LIDOCAINA-SG5', 'Adverse reactions')),
        [ALTO, 'Usar solo la presentación sin adrenalina para vía EV.'],
        discrepancias=[{'campo': 'tope pediátrico del bolo', 'valores': ['Pediamécum: 1 mg/kg sin tope explícito', 'FDA adulto: 1–1,5 mg/kg (≈100 mg en 70 kg)'], 'decision': 'Se usa 100 mg como tope adulto del bolo pediátrico; confirmar en revisión.'}],
    )

    F['furosemida'] = ficha(
        'furosemida', 'Furosemida', 'diuretico', URG_H, False,
        [pres('amp-20mg-2ml', 'ampolla', 20, 'mg', 2, C('furosemida', 'Presentación: 20 mg/2 ml'))],
        {'sueros': ['SF'], 'concentracionMax': conc(10, 'mg', PED('furosemida', 'Perfusión: no superar 10 mg/ml')),
         'estandar': [dil('100 mg en 100 ml (1 mg/ml)', 100, 'mg', 100, P('Anexo 6, Furosemida: dilución 1 mg/ml'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Inyectar o perfundir lentamente, a no más de 4 mg/min (2,5 mg/min si creatinina > 5 mg/dl). No mezclar en jeringa con otros fármacos (pH 9; precipita con soluciones ácidas).', 'fuente': C('furosemida', '4.2.2; 6.2')},
        [dosis('Insuficiencia cardíaca aguda: bolo inicial', 'adulto', 'mg', C('furosemida', '4.2: 20–40 mg IV'), mn=20, mx=40),
         dosis('Perfusión continua', 'adulto', 'mg/h', C('furosemida', '4.2: 50–100 mg/h en IRA'), mn=50, mx=100),
         dosis('Niños: dosis parenteral máxima', 'pediatrico', 'mg/kg/24 h', C('furosemida', '4.2 Población pediátrica: 1 mg/kg hasta 20 mg/día'), mx=1)],
        {'fuente': C('furosemida', '6.3 (no informa estabilidad de la dilución)')},
        [ix('Aminoglucósidos y otros ototóxicos', 'Ototoxicidad que puede ser irreversible', C('furosemida', '4.5')),
         ix('Hidrato de cloral', 'Rubor, sudoración, hipertensión y taquicardia', C('furosemida', '4.5'))],
        ea(['Alteraciones electrolíticas', 'Deshidratación', 'Hipotensión'], ['Hipokalemia grave', 'Ototoxicidad (administración rápida)', 'Pancreatitis'], ['Diuresis', 'Potasio y sodio', 'PA'], C('furosemida', '4.8')),
        ['Velocidad máxima 4 mg/min.'],
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: máx. 1 mg/kg/día parenteral hasta 20 mg/día', 'Pediamécum: IV inicial 0,1–2 mg/kg (máx. 40 mg)'], 'decision': 'Se registra la pauta más conservadora (CIMA).'},
                       {'campo': 'presentación', 'valores': ['Pucón: «20 mg/ml»', 'CIMA: ampolla 20 mg/2 ml (10 mg/ml)'], 'decision': 'Se registra 20 mg/2 ml; verificar el rotulado de la ampolla local.'},
                       {'campo': 'suero', 'valores': ['Pediamécum: SF o SG5 %', 'Stabilis: SG5 % incompatible en Y (casilla roja); CIMA 6.2: precipita con pH < 7'], 'decision': 'Solo SF por criterio conservador.'}],
    )

    F['metoclopramida'] = ficha(
        'metoclopramida', 'Metoclopramida', 'antiemetico', URG_H, False,
        [pres('amp-10mg-2ml', 'ampolla', 10, 'mg', 2, P('Anexo 6, Metoclopramida: 10 mg/2 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(5, 'mg', P('Anexo 6, Metoclopramida: concentración máxima 5 mg/ml')),
         'estandar': [dil('10 mg en 50 ml (0,2 mg/ml)', 10, 'mg', 50, P('Anexo 6, Metoclopramida: 0,2 mg/ml'))]},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Bolo IV lento de al menos 3 minutos. Intervalo mínimo de 6 h entre dosis, aunque haya vómito. Precaución en niños y adultos mayores por reacciones extrapiramidales.', 'tiempoMinimoMin': 3, 'fuente': C('metoclopramida', '4.2 Forma de administración')},
        [dosis('Náuseas y vómitos (hasta 3 veces al día)', 'adulto', 'mg', C('metoclopramida', '4.2: 10 mg; máx. 30 mg/día'), mn=10, mx=10, maxima=30),
         dosis('Náuseas y vómitos, 1–18 años (hasta 3 veces al día)', 'pediatrico', 'mg/kg', C('metoclopramida', '4.2: 0,1–0,15 mg/kg; máx. 0,5 mg/kg/día'), mn=0.1, mx=0.15, tope=(10, 'mg'))],
        {'fuente': C('metoclopramida', '6.3: tras abrir o diluir, usar inmediatamente')},
        [ix('Levodopa y agonistas dopaminérgicos', 'Antagonismo mutuo (contraindicado)', C('metoclopramida', '4.5')),
         ix('Depresores del SNC y alcohol', 'Potenciación de la sedación', C('metoclopramida', '4.5'))],
        ea(['Somnolencia', 'Astenia'], ['Reacciones extrapiramidales', 'Síndrome neuroléptico maligno', 'Bradicardia o hipotensión con bolo rápido'], ['Movimientos anormales', 'PA'], C('metoclopramida', '4.8')),
        ['Contraindicada en menores de 1 año.', 'Incompatible con bicarbonato de sodio.'],
    )

    F['ondansetron'] = ficha(
        'ondansetron', 'Ondansetrón', 'antiemetico', URG_H, False,
        [pres('amp-4mg-2ml', 'ampolla', 4, 'mg', 2, P('Anexo 6, Ondansetrón: 4 mg/2 ml')),
         pres('amp-8mg-4ml', 'ampolla', 8, 'mg', 4, P('Anexo 6, Ondansetrón: 8 mg/4 ml'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': [dil('8 mg en 50 ml', 8, 'mg', 50, C('ondansetron', '4.2: dosis diluida en 50–100 ml de SF')),
                      dil('16 mg en 100 ml (en ≥ 15 min)', 16, 'mg', 100, C('ondansetron', '4.2: 16 mg en 50–100 ml en no menos de 15 min'))]},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Bolo IV lento (no menos de 30 segundos) o perfusión de 15 minutos. Dosis IV única máxima 16 mg (prolongación del QT). La administración rápida puede provocar hipotensión transitoria.', 'fuente': C('ondansetron', '4.2')},
        [dosis('Náuseas y vómitos (dosis única IV)', 'adulto', 'mg', C('ondansetron', '4.2: 8 mg; máx. 16 mg por dosis IV'), mn=8, mx=8, maxima=16),
         dosis('Náuseas y vómitos ≥ 6 meses (por peso)', 'pediatrico', 'mg/kg', PED('ondansetron', '0,15 mg/kg; dosis IV máx. 8 mg'), mn=0.15, mx=0.15, tope=(8, 'mg'))],
        {'ambienteH': 168, 'refrigeradoH': 168, 'fuente': C('ondansetron', '6.6: estable 7 días bajo 25 °C o en nevera con los fluidos indicados')},
        [ix('Fármacos que prolongan el QT', 'Prolongación aditiva del QT', C('ondansetron', '4.4')),
         ix('Fármacos serotoninérgicos (ISRS, IRSN)', 'Síndrome serotoninérgico', C('ondansetron', '4.4'))],
        ea(['Cefalea', 'Estreñimiento', 'Rubor'], ['Prolongación del QT', 'Reacciones de hipersensibilidad'], ['ECG si hay riesgo de QT largo'], C('ondansetron', '4.8')),
        ['No superar 16 mg IV por dosis (QT).'],
    )

    F['ketorolaco'] = ficha(
        'ketorolaco', 'Ketorolaco', 'analgesico-no-opioide', URG_H, False,
        [pres('amp-30mg-1ml', 'ampolla', 30, 'mg', 1, P('Anexo 6, Ketorolaco: 30 mg/ml'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': [dil('90 mg en 250 ml (infusión continua de 24 h)', 90, 'mg', 250, P('Anexo 6, Ketorolaco: habitualmente 90 mg/250 ml'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV en no menos de 15 segundos o infusión continua. Duración máxima del tratamiento parenteral 2 días. No mezclar en la misma jeringa con morfina, meperidina, prometazina o hidroxizina (precipita). Proteger de la luz.', 'fuente': C('ketorolaco', '4.2; 6.2')},
        [dosis('Dolor: dosis inicial 10 mg (30 mg si es intenso), luego 10–30 mg cada 4–6 h', 'adulto', 'mg', C('ketorolaco', '4.2: máx. 90 mg/día (60 mg en ancianos)'), mn=10, mx=30, maxima=90),
         dosis('Dolor 2–16 años, cada 6–8 h (fuera de ficha técnica)', 'pediatrico', 'mg/kg', PED('ketorolaco', 'IV 0,5 mg/kg/dosis, máx. 30 mg/dosis, 48–72 h'), mn=0.5, mx=0.5, tope=(30, 'mg'))],
        {'protegerLuz': True, 'fuente': P('Anexo 6, Ketorolaco: protegido de la luz, a temperatura ambiente')},
        [ix('Otros AINE, incluida aspirina', 'Mayor riesgo de úlcera y hemorragia digestiva; evitar', C('ketorolaco', '4.5')),
         ix('Anticoagulantes', 'Potencian el riesgo de sangrado', C('ketorolaco', '4.5'))],
        ea(['Náuseas', 'Dispepsia', 'Cefalea', 'Dolor en el sitio de inyección'], ['Úlcera, perforación o hemorragia digestiva', 'Insuficiencia renal aguda'], ['Signos de sangrado', 'Diuresis y función renal'], C('ketorolaco', '4.8')),
        ['Máximo 2 días por vía parenteral.'],
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: no recomendado en menores de 16 años', 'Pediamécum: 0,5 mg/kg/dosis (máx. 30 mg), uso fuera de ficha técnica'], 'decision': 'Se registra la pauta de Pediamécum indicada como fuera de ficha técnica; revisar si se mantiene.'}],
    )

    F['tramadol'] = ficha(
        'tramadol', 'Tramadol', 'analgesico-opioide', URG_H, True,
        [pres('amp-100mg-2ml', 'ampolla', 100, 'mg', 2, P('Anexo 4 y 6, Tramadol: 100 mg/2 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(1.2, 'mg', P('Anexo 6, Tramadol: 1,2 mg/ml')),
         'estandar': [dil('300 mg en 250 ml (1,2 mg/ml)', 300, 'mg', 250, P('Anexo 6, Tramadol: habitualmente 300 mg/250 ml'))]},
        {'vias': ['bolo', 'infusion_intermitente', 'infusion_continua'], 'texto': 'Inyección IV lenta de 2–3 minutos o perfusión diluida. Antídoto: naloxona.', 'tiempoMinimoMin': 2, 'fuente': C('tramadol', '4.2.2')},
        [dosis('Dolor intenso: dosis inicial', 'adulto', 'mg', C('tramadol', '4.2.1: 100 mg; luego 50–100 mg cada 4–6 h; máx. 400 mg/día'), mn=100, mx=100, maxima=400),
         dosis('Dolor, niños desde 3 años (3–4 veces al día)', 'pediatrico', 'mg/kg', C('tramadol', '4.2.1: 1–2 mg/kg; máx. 8 mg/kg/día o 400 mg'), mn=1, mx=2, tope=(100, 'mg'))],
        {'fuente': C('tramadol', '6.3 (no informa estabilidad de la dilución)')},
        [ix('IMAO', 'Interacciones con riesgo vital (SNC, respiratorio, cardiovascular); contraindicado', C('tramadol', '4.5')),
         ix('Depresores del SNC (benzodiazepinas, alcohol, otros opioides)', 'Sedación y depresión respiratoria', C('tramadol', '4.5'))],
        ea(['Náuseas', 'Mareos', 'Somnolencia', 'Sudoración'], ['Depresión respiratoria', 'Convulsiones', 'Síndrome serotoninérgico'], ['Frecuencia respiratoria y sedación'], C('tramadol', '4.8')),
        [ALTO, 'Contraindicado en menores de 3 años.', 'Incompatible en la misma solución con diazepam, midazolam, diclofenaco y nitroglicerina.'],
    )

    F['metamizol'] = ficha(
        'metamizol', 'Metamizol (dipirona)', 'analgesico-no-opioide', URG_H, False,
        [pres('amp-2g-5ml', 'ampolla', 2, 'g', 5, C('metamizol', 'Presentación 0,4 g/ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMin': conc(2, 'mg', P('Anexo 6, Metamizol: 2 a 10 mg/ml')), 'concentracionMax': conc(10, 'mg', P('Anexo 6, Metamizol: 2 a 10 mg/ml')),
         'estandar': [dil('1 g en 100 ml (10 mg/ml)', 1, 'g', 100, P('Anexo 6, Metamizol: 1000 mg/100 ml')),
                      dil('1 g en 500 ml (2 mg/ml)', 1, 'g', 500, P('Anexo 6, Metamizol: 1000 mg/500 ml'))]},
        {'vias': ['infusion_intermitente', 'infusion_continua'], 'texto': 'Administrar muy lentamente: la causa más frecuente de hipotensión grave y shock es la velocidad de inyección excesiva. Tener disponible equipo para tratar el shock. No mezclar con otros fármacos en la misma jeringa.', 'fuente': C('metamizol', '4.2')},
        [dosis('Dolor o fiebre (≥ 15 años, > 53 kg), hasta 4 veces al día', 'adulto', 'mg', C('metamizol', '4.2: hasta 1000 mg por dosis; máx. 4000 mg/día'), mx=1000, maxima=4000),
         dosis('Dolor o fiebre, niños hasta 14 años', 'pediatrico', 'mg/kg', C('metamizol', '4.2: 8–16 mg/kg en dosis única'), mn=8, mx=16, tope=(1, 'g'))],
        {'fuente': C('metamizol', '6.3 (no informa estabilidad de la dilución)')},
        [ix('Metotrexato y otros antineoplásicos', 'Mayor toxicidad hematológica; evitar', C('metamizol', '4.5')),
         ix('Clorpromazina', 'Hipotermia grave', C('metamizol', '4.5'))],
        ea(['Hipotensión', 'Prurito', 'Sudoración'], ['Agranulocitosis', 'Shock anafiláctico', 'Hipotensión grave con inyección rápida'], ['PA durante la administración', 'Fiebre o dolor de garganta (agranulocitosis)'], P('Anexo 6, Metamizol: RAM')),
        ['Administrar lento: riesgo de hipotensión grave.'],
        discrepancias=[{'campo': 'presentación', 'valores': ['Pucón: ampolla de 1 g (sin volumen indicado)', 'CIMA: 0,4 g/ml (ampolla de 2 g/5 ml)'], 'decision': 'Se registra la de CIMA; verificar la ampolla disponible en Chile.'}],
    )

    F['hidrocortisona'] = ficha(
        'hidrocortisona', 'Hidrocortisona', 'corticoide', URG_H, False,
        [pres('fa-100mg', 'frasco ampolla liofilizado', 100, 'mg', 2, P('Anexo 6, Hidrocortisona: frasco liofilizado 100 mg; reconstitución 50 mg/ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMin': conc(1, 'mg', P('Anexo 6, Hidrocortisona: dilución 1–5 mg/ml')), 'concentracionMax': conc(5, 'mg', P('Anexo 6, Hidrocortisona: dilución 1–5 mg/ml')),
         'estandar': [dil('100 mg en 100 ml (1 mg/ml)', 100, 'mg', 100, P('Anexo 6, Hidrocortisona: 1–5 mg/ml'))]},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Inyección IV lenta (1 a 10 minutos) o perfusión diluida. Repetible cada 2, 4 o 6 h según respuesta. No mezclar con otros fármacos.', 'tiempoMinimoMin': 1, 'fuente': C('hidrocortisona', '4.2.1; 6.2')},
        [dosis('Dosis IV única habitual, hasta aprox. 373 mg (la ficha indica que no está limitada; repetible cada 2–6 h)', 'adulto', 'mg', C('hidrocortisona', '4.2.1: desde una fracción del vial hasta aprox. 373 mg por dosis, «aunque no está limitado»'), mx=373),
         dosis('Insuficiencia suprarrenal aguda: dosis inicial (niños)', 'pediatrico', 'mg/kg', PED('hidrocortisona', 'Dosis inicial 2–3 mg/kg (hasta 100 mg/dosis)'), mn=2, mx=3, tope=(100, 'mg'))],
        {'refrigeradoH': 24, 'fuente': C('hidrocortisona', '6.3: solución reconstituida 24 h entre 2 y 8 °C')},
        [ix('Inductores enzimáticos (rifampicina, fenitoína, carbamazepina, barbitúricos)', 'Reducen el efecto del corticoide', C('hidrocortisona', '4.5'))],
        ea(['Hiperglicemia', 'Hipertensión', 'Edema', 'Insomnio'], ['Hipokalemia', 'Hemorragia digestiva'], ['Glicemia', 'Potasio', 'PA'], P('Anexo 6, Hidrocortisona: RAM')),
        [],
        reconstitucion={'diluyente': 'Agua para inyectables', 'volumenMl': 2, 'fuente': P('Anexo 6, Hidrocortisona: reconstitución 50 mg/ml (100 mg en 2 ml)')},
        discrepancias=[{'campo': 'presentación y dosis adulto', 'valores': ['Pucón: frasco liofilizado de 100 mg (succinato)', 'CIMA: Actocortina, hidrocortisona fosfato 373 mg'], 'decision': 'Presentación de Pucón; la dosis adulta se cita de CIMA (otra sal). Revisar dosis según protocolo local (p. ej., 100 mg en crisis suprarrenal).'}],
    )

    F['dexametasona'] = ficha(
        'dexametasona', 'Dexametasona', 'corticoide', URG_H, False,
        [pres('amp-4mg-1ml', 'ampolla', 4, 'mg', 1, P('Anexo 6, Dexametasona: 4 mg/ml'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Preferentemente IV directa o en el tubo de perfusión. Dosis menores de 10 mg no requieren dilución.', 'fuente': P('Anexo 6, Dexametasona: dosis menor a 10 mg no requiere dilución')},
        [dosis('Edema cerebral: dosis inicial', 'adulto', 'mg', C('dexametasona', '4.2: 8–10 mg IV (hasta 80 mg)'), mn=8, mx=10, maxima=80),
         dosis('Asma grave: dosis inicial', 'adulto', 'mg', C('dexametasona', '4.2: 8–40 mg IV'), mn=8, mx=40),
         dosis('Crisis suprarrenal aguda', 'adulto', 'mg', C('dexametasona', '4.2: 4–8 mg IV'), mn=4, mx=8),
         dosis('Asma grave aguda (niños)', 'pediatrico', 'mg/kg', PED('dexametasona', '0,15–0,3 mg/kg'), mn=0.15, mx=0.3, tope=(40, 'mg')),
         dosis('Edema cerebral: dosis inicial (niños)', 'pediatrico', 'mg/kg', PED('dexametasona', '1–2 mg/kg (máx. 10–20 mg)'), mn=1, mx=2, tope=(10, 'mg'))],
        {'ambienteH': 48, 'refrigeradoH': 48, 'protegerLuz': True, 'fuente': C('dexametasona', '6.3: diluida estable 48 h a 25 °C protegida de la luz y a 2–8 °C')},
        [ix('Digitálicos', 'Mayor efecto digitálico por hipokalemia', C('dexametasona', '4.5')),
         ix('Inductores del CYP3A4 (rifampicina, fenitoína, carbamazepina)', 'Reducen el efecto del corticoide', C('dexametasona', '4.5'))],
        ea(['Hiperglicemia', 'Hipertensión', 'Cefalea'], ['Hipokalemia', 'Úlcera digestiva'], ['Glicemia', 'Potasio'], P('Anexo 6, Dexametasona: RAM')),
        [],
    )

    F['metilprednisolona'] = ficha(
        'metilprednisolona', 'Metilprednisolona', 'corticoide', URG_H, False,
        [pres('fa-40mg', 'frasco ampolla en polvo + disolvente', 40, 'mg', 1, C('metilprednisolona', '6.6: viales de 20 y 40 mg disueltos en 1 ml')),
         pres('fa-20mg', 'frasco ampolla en polvo + disolvente', 20, 'mg', 1, C('metilprednisolona', '6.6: viales de 20 y 40 mg disueltos en 1 ml'))],
        {'sueros': ['SF', 'SG5'], 'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Inyección IV lenta o perfusión. No mezclar en la misma jeringa con soluciones distintas de SF o SG5 %. Usar la solución reconstituida de inmediato.', 'fuente': C('metilprednisolona', '6.2; 6.3')},
        [dosis('Situación con riesgo vital (shock anafiláctico, status asmático, edema cerebral)', 'adulto', 'mg', C('metilprednisolona', '4.2.1: 250–500 mg; riesgo vital 250–1000 mg'), mn=250, mx=500, maxima=1000),
         dosis('Exacerbación aguda de asma', 'adulto', 'mg/24 h', C('metilprednisolona', '4.2.1: 30–90 mg al día'), mn=30, mx=90),
         dosis('Situación con riesgo vital (niños)', 'pediatrico', 'mg/kg', C('metilprednisolona', '4.2.1: 4–20 mg/kg'), mn=4, mx=20, tope=(1, 'g')),
         dosis('Status asmático (niños): dosis inicial', 'pediatrico', 'mg/kg', PED('metilprednisolona', 'IV 2 mg/kg/dosis; luego 0,5–1 mg/kg cada 6 h'), mn=2, mx=2, tope=(500, 'mg'))],
        {'fuente': C('metilprednisolona', '6.3: usar inmediatamente tras reconstituir')},
        [ix('Anfotericina B', 'Hipokalemia con riesgo de toxicidad', C('metilprednisolona', '4.5')),
         ix('Anticolinesterásicos (neostigmina)', 'Antagonismo con depresión muscular; algunos casos requirieron ventilación', C('metilprednisolona', '4.5'))],
        ea(['Hiperglicemia', 'Retención de líquidos'], ['Hipokalemia', 'Úlcera digestiva', 'Arritmias con bolos rápidos de dosis altas'], ['Glicemia', 'Potasio', 'PA'], C('metilprednisolona', '4.8')),
        [],
        reconstitucion={'diluyente': 'Agua para inyectables (ampolla de disolvente)', 'volumenMl': 1, 'fuente': C('metilprednisolona', '6.6')},
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Protocolo Pucón 2022 no incluye metilprednisolona'], 'decision': 'Ficha basada en CIMA y Pediamécum; en Chile son habituales viales de 40, 125, 500 y 1000 mg: confirmar.'}],
    )

    F['fenitoina'] = ficha(
        'fenitoina', 'Fenitoína', 'anticonvulsivante', URG_H, True,
        [pres('amp-250mg-5ml', 'ampolla', 250, 'mg', 5, P('Anexo 6, Fenitoína: 250 mg/5 ml'))],
        {'sueros': ['SF'], 'concentracionMin': conc(1, 'mg', C('fenitoina', '6.2: solo SF, 1–10 mg/ml')), 'concentracionMax': conc(10, 'mg', C('fenitoina', '6.2: solo SF, 1–10 mg/ml')),
         'estandar': [dil('1 g en 100 ml de SF (10 mg/ml)', 1, 'g', 100, P('Anexo 6, Fenitoína: dilución 1 a 10 mg/ml'))]},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Diluir solo en suero fisiológico (precipita con glucosa). Velocidad máxima 50 mg/min en adultos (25 mg/min o menos en adultos mayores) y 1–3 mg/kg/min en niños, con ECG y PA. Lavar con SF antes y después.', 'fuente': C('fenitoina', '4.2 Forma de administración; 6.2')},
        [dosis('Status epiléptico: carga (a ≤ 50 mg/min)', 'adulto', 'mg/kg', C('fenitoina', '4.2: carga aprox. 18 mg/kg'), mn=18, mx=18),
         dosis('Mantención desde las 24 h (en 3–4 dosis)', 'adulto', 'mg/kg/24 h', C('fenitoina', '4.2: 5–7 mg/kg/día'), mn=5, mx=7),
         dosis('Status epiléptico: carga (niños)', 'pediatrico', 'mg/kg', C('fenitoina', '4.2 Neonatos y niños pequeños: 15–20 mg/kg'), mn=15, mx=20, tope=(1260, 'mg'))],
        {'fuente': C('fenitoina', '6.3 (no informa estabilidad de la dilución)')},
        [ix('Inhibidores del CYP2C9/2C19', 'Aumento importante de la concentración de fenitoína: toxicidad', C('fenitoina', '4.5')),
         ix('Fármacos metabolizados por enzimas hepáticas', 'Fenitoína es inductor potente: reduce sus niveles', C('fenitoina', '4.5'))],
        ea(['Mareo', 'Nistagmo', 'Cefalea'], ['Colapso cardiovascular y arritmias con administración rápida', 'Depresión del SNC', 'Necrosis por extravasación (síndrome del guante púrpura)'], ['ECG y PA durante la infusión', 'Sitio de punción'], C('fenitoina', '4.8')),
        [ALTO, 'Diluir solo en SF. No superar 50 mg/min.'],
        discrepancias=[{'campo': 'tope pediátrico', 'valores': ['CIMA adulto: 18 mg/kg (≈1260 mg en 70 kg)'], 'decision': 'Tope adulto de la carga pediátrica fijado en 1260 mg (18 mg/kg × 70 kg); confirmar en revisión.'}],
    )

    F['levetiracetam'] = ficha(
        'levetiracetam', 'Levetiracetam', 'anticonvulsivante', URG_H, False,
        [pres('vial-500mg-5ml', 'vial', 500, 'mg', 5, C('levetiracetam', 'Concentrado 100 mg/ml, vial de 5 ml'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': [dil('500 mg en 100 ml (perfusión de 15 min)', 500, 'mg', 100, C('levetiracetam', '6.6 Tabla 1')),
                      dil('1.500 mg en 100 ml (perfusión de 15 min)', 1500, 'mg', 100, C('levetiracetam', '6.6 Tabla 1'))]},
        {'vias': ['infusion_intermitente'], 'texto': 'Diluir en 100 ml de SF, Ringer lactato o SG5 % y perfundir en 15 minutos, dos veces al día. Paso oral ↔ IV sin cambiar la dosis.', 'tiempoMinimoMin': 15, 'fuente': C('levetiracetam', '4.2; 6.6')},
        [dosis('Crisis epilépticas, dos veces al día', 'adulto', 'mg', C('levetiracetam', '4.2: 500 mg c/12 h, hasta 1.500 mg c/12 h'), mn=500, mx=1500),
         dosis('Crisis epilépticas 4–17 años (< 50 kg), dos veces al día', 'pediatrico', 'mg/kg', C('levetiracetam', '4.2: 10 mg/kg c/12 h, hasta 30 mg/kg c/12 h'), mn=10, mx=30, tope=(1500, 'mg'))],
        {'refrigeradoH': 24, 'fuente': C('levetiracetam', '6.3: microbiológicamente usar de inmediato; máximo 24 h a 2–8 °C')},
        [],
        ea(['Somnolencia', 'Cefalea', 'Fatiga', 'Mareo'], ['Alteraciones conductuales y psiquiátricas', 'Ideación suicida'], ['Estado de conciencia y conducta'], C('levetiracetam', '4.8')),
        [],
        discrepancias=[{'campo': 'fuente chilena / status epiléptico', 'valores': ['Pucón 2022 no incluye levetiracetam', 'CIMA no incluye dosis de status epiléptico'], 'decision': 'Solo se registran dosis de ficha técnica; la dosis de carga en status depende del protocolo local.'}],
    )

    F['diazepam'] = ficha(
        'diazepam', 'Diazepam', 'anticonvulsivante', URG_H, True,
        [pres('amp-10mg-2ml', 'ampolla', 10, 'mg', 2, C('diazepam', '2: ampolla de 2 ml con 10 mg'))],
        {'sueros': ['SF', 'SG5'], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Inyección IV muy lenta (aprox. 0,5–1 ml/min) en vena de grueso calibre: la administración rápida puede causar apnea. Preferir sin diluir; el PVC adsorbe diazepam.', 'fuente': C('diazepam', '4.2; 6.2')},
        [dosis('Estatus epiléptico (repetible cada 10–15 min)', 'adulto', 'mg/kg', C('diazepam', '4.2: 0,15–0,25 mg/kg; máx. 3 mg/kg en 24 h'), mn=0.15, mx=0.25),
         dosis('Ansiedad media/grave', 'adulto', 'mg', C('diazepam', '4.2: 2–10 mg, repetible a las 3–4 h'), mn=2, mx=10),
         dosis('Crisis o estatus epiléptico, lactantes > 30 días y niños', 'pediatrico', 'mg/kg', PED('diazepam', '0,1–0,3 mg/kg/dosis (máx. 10 mg), en 3–5 min'), mn=0.1, mx=0.3, tope=(10, 'mg'))],
        {'ambienteH': 24, 'fuente': C('diazepam', '6.3: estabilidad en uso de 24 h a temperatura ambiente')},
        [ix('Opioides y otros depresores del SNC', 'Sedación profunda, depresión respiratoria, coma y muerte', C('diazepam', '4.4')),
         ix('Inhibidores del CYP3A4 y CYP2C19', 'Aumentan el efecto del diazepam', C('diazepam', '4.5'))],
        ea(['Somnolencia', 'Fatiga', 'Debilidad muscular'], ['Apnea con inyección rápida', 'Hipotensión', 'Depresión respiratoria'], ['Frecuencia respiratoria y SatO2', 'Nivel de conciencia'], C('diazepam', '4.8')),
        [ALTO, 'Tener flumazenilo y apoyo ventilatorio disponibles.'],
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Protocolo Pucón 2022 no incluye diazepam'], 'decision': 'Ficha basada en CIMA y Pediamécum.'}],
    )

    F['naloxona'] = ficha(
        'naloxona', 'Naloxona', 'antidoto', URG, False,
        [pres('amp-0.4mg-1ml', 'ampolla', 0.4, 'mg', 1, P('Anexo 6, Naloxona: 0,4 mg/ml'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': [dil('2 mg en 500 ml (4 mcg/ml), infusión', 2, 'mg', 500, C('naloxona', '6.6: 5 ampollas (2 mg) en 500 ml = 4 mcg/ml')),
                      dil('2 mg en 50 ml (40 mcg/ml), infusión', 2, 'mg', 50, P('Anexo 6, Naloxona: infusión 2 mg en 50 ml'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolos IV repetibles cada 2 minutos hasta respiración y conciencia satisfactorias; perfusión si el opioide es de acción prolongada. Su efecto puede durar menos que el del opioide: vigilar la resedación.', 'fuente': C('naloxona', '4.2.1')},
        [dosis('Depresión respiratoria por opioides: bolo inicial (repetir 0,1 mg c/2 min)', 'adulto', 'mg', C('naloxona', '4.2.1: 0,1–0,2 mg IV'), mn=0.1, mx=0.2),
         dosis('Depresión por opioides (niños), cada 2–3 min', 'pediatrico', 'mg/kg', C('naloxona', '4.2.1 Población pediátrica: 0,01–0,02 mg/kg'), mn=0.01, mx=0.02, tope=(0.2, 'mg'))],
        {'ambienteH': 24, 'fuente': C('naloxona', '6.3: diluida estable 30 h (se registran 24 h por criterio conservador)')},
        [ix('Opioides en pacientes dependientes', 'Síndrome de abstinencia intenso: hipertensión, arritmias, edema pulmonar, paro', C('naloxona', '4.5'))],
        ea(['Náuseas', 'Vómitos', 'Taquicardia'], ['Arritmias ventriculares', 'Edema pulmonar', 'Hipertensión'], ['Frecuencia respiratoria', 'Resedación tras terminar el efecto'], P('Anexo 6, Naloxona: RAM')),
        [],
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: 0,01–0,02 mg/kg', 'Pediamécum (PALS): 0,1 mg/kg hasta 2 mg en reversión total'], 'decision': 'Se registra la pauta de ficha técnica (conservadora); la de PALS queda para revisión.'}],
    )

    F['flumazenil'] = ficha(
        'flumazenil', 'Flumazenilo', 'antidoto', URG, False,
        [pres('amp-0.5mg-5ml', 'ampolla', 0.5, 'mg', 5, P('Anexo 6, Flumazenil: 0,5 mg/5 ml'))],
        {'sueros': ['SF', 'SG5'], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV en 15 segundos; no requiere dilución. Repetir 0,1 mg cada 60 s según conciencia. En perfusión, diluir solo en SF o SG5 %.', 'fuente': C('flumazenil', '4.2; 6.6')},
        [dosis('Reversión en anestesia: inicial 0,2 mg, luego 0,1 mg c/60 s', 'adulto', 'mg', C('flumazenil', '4.2: máx. 1 mg'), mn=0.2, mx=0.2, maxima=1),
         dosis('Cuidados intensivos: inicial 0,3 mg, luego 0,1 mg c/60 s', 'adulto', 'mg', C('flumazenil', '4.2: hasta 2 mg en total'), mn=0.3, mx=0.3, maxima=2),
         dosis('Perfusión si reaparece la somnolencia', 'adulto', 'mg/h', C('flumazenil', '4.2: 0,1–0,4 mg/h'), mn=0.1, mx=0.4),
         dosis('Reversión de benzodiazepinas (niños)', 'pediatrico', 'mg/kg', PED('flumazenil', '0,01 mg/kg (máx. 0,2 mg), repetible; máx. acumulado 0,05 mg/kg o 1 mg'), mn=0.01, mx=0.01, tope=(0.2, 'mg'))],
        {'ambienteH': 24, 'fuente': C('flumazenil', '6.3: diluido 24 h a 25 °C; no refrigerar')},
        [ix('Benzodiazepinas en uso prolongado', 'Síndrome de abstinencia y convulsiones', C('flumazenil', '4.4'))],
        ea(['Náuseas', 'Vómitos'], ['Convulsiones', 'Arritmias'], ['Resedación', 'Convulsiones'], P('Anexo 6, Flumazenil: RAM')),
        ['Su efecto es más corto que el de muchas benzodiazepinas: vigilar resedación.'],
    )

    F['acido-tranexamico'] = ficha(
        'acido-tranexamico', 'Ácido tranexámico', 'hematologico', URG_H, False,
        [pres('amp-1g-10ml', 'ampolla', 1, 'g', 10, P('Anexo 6, Ácido tranexámico: 1 g/10 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(10, 'mg', P('Anexo 6, Ácido tranexámico: dilución 10 mg/ml')),
         'estandar': [dil('1 g en 100 ml (10 mg/ml)', 1, 'g', 100, P('Anexo 6, Ácido tranexámico: 10 mg/ml'))]},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Inyección IV lenta (no más de 1 ml/min, es decir 100 mg/min). La inyección rápida puede causar hipotensión. No añadir a sangre para transfusión ni a soluciones con penicilina.', 'fuente': C('acido-tranexamico', '4.2.1; 6.2')},
        [dosis('Fibrinólisis general, cada 6–8 h (≈15 mg/kg)', 'adulto', 'g', C('acido-tranexamico', '4.2.1: 1 g IV lenta'), mn=1, mx=1),
         dosis('Niños > 1 año (cada 6–8 h)', 'pediatrico', 'mg/kg', PED('acido-tranexamico', 'IV 10–15 mg/kg/dosis cada 6–8 h'), mn=10, mx=15, tope=(1, 'g'))],
        {'fuente': C('acido-tranexamico', '6.3: usar inmediatamente tras abrir la ampolla')},
        [ix('Anticoagulantes y fármacos que actúan sobre la hemostasia', 'Usar con precaución; riesgo teórico de trombosis', C('acido-tranexamico', '4.5'))],
        ea(['Náuseas', 'Diarrea'], ['Hipotensión con inyección rápida', 'Trombosis', 'Convulsiones'], ['PA durante la inyección'], P('Anexo 6, Ácido tranexámico: RAM')),
        ['Reducir dosis en insuficiencia renal.'],
    )

    F['heparina'] = ficha(
        'heparina', 'Heparina sódica', 'hematologico', URG_H, True,
        [pres('fa-25000ui-5ml', 'frasco ampolla', 25000, 'UI', 5, C('heparina', '2: 5.000 UI/ml, vial de 5 ml = 25.000 UI (Pucón Anexo 4: heparina 25.000 UI FA)')),
         pres('fa-5000ui-5ml', 'frasco ampolla', 5000, 'UI', 5, C('heparina', '2: 1.000 UI/ml, vial de 5 ml = 5.000 UI'))],
        {'sueros': ['SF', 'SG5'],
         'estandar': [dil('25.000 UI en 250 ml (100 UI/ml)', 25000, 'UI', 250, C('heparina', '4.2: infusión IV continua ajustada por TTPA'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV seguido de infusión continua por bomba, ajustada por TTPA (1,5–2,5 veces el control), con control a las 4–6 h de iniciar y de cada cambio. No mezclar con otras soluciones. No usar vía IM.', 'requiereBomba': True, 'fuente': C('heparina', '4.2; 6.2')},
        [dosis('Tromboembolismo: bolo inicial', 'adulto', 'UI/kg', C('heparina', '4.2: 80 UI/kg; hasta 120 UI/kg en TEP grave'), mn=80, mx=80, maxima=120),
         dosis('Tromboembolismo: mantención', 'adulto', 'UI/kg/h', C('heparina', '4.2: 18 UI/kg/h ajustada por TTPA'), mn=18, mx=18),
         dosis('Angina inestable o IAM sin trombolisis: bolo', 'adulto', 'UI', C('heparina', '4.2: bolo de 5.000 UI, luego 32.000 UI/24 h'), mn=5000, mx=5000),
         dosis('Anticoagulación: bolo (niños)', 'pediatrico', 'UI/kg', C('heparina', '4.2 Población pediátrica: 80 UI/kg en bolo'), mn=80, mx=80, tope=(5000, 'UI')),
         dosis('Anticoagulación: mantención (niños)', 'pediatrico', 'UI/kg/h', C('heparina', '4.2 Población pediátrica: 18 UI/kg/h'), mn=18, mx=18)],
        {'fuente': C('heparina', '6.3: una vez abierto el vial, administrar inmediatamente')},
        [ix('Anticoagulantes, antiagregantes, fibrinolíticos, AINE', 'Potencian el efecto: riesgo de hemorragia', C('heparina', '4.5'))],
        ea([], ['Hemorragias', 'Trombocitopenia inducida por heparina'], ['TTPA', 'Plaquetas', 'Signos de sangrado'], C('heparina', '4.8')),
        [ALTO, 'Existen frascos de 1.000 y 5.000 UI/ml: verificar la concentración antes de cargar.'],
        discrepancias=[{'campo': 'tope pediátrico y dilución', 'valores': ['CIMA: 80 UI/kg en bolo sin tope explícito', 'Pediamécum (otras fuentes): 75 UI/kg y 20 UI/kg/h', 'Dilución 25.000 UI/250 ml no está en las fuentes; es un ejemplo de 100 UI/ml'], 'decision': 'Tope del bolo pediátrico = bolo adulto fijo de 5.000 UI; confirmar dilución con el protocolo local.'}],
    )

    F['insulina-cristalina'] = ficha(
        'insulina-cristalina', 'Insulina cristalina (regular)', 'metabolico', URG_H, True,
        [pres('fa-1000ui-10ml', 'frasco ampolla', 1000, 'UI', 10, C('insulina-cristalina', '2: vial de 10 ml con 100 UI/ml (Pucón Anexo 4: insulina cristalina 100 UI/ml FA)'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMin': conc(0.05, 'UI', C('insulina-cristalina', '4.2: 0,05 a 1,0 UI/ml')), 'concentracionMax': conc(1, 'UI', C('insulina-cristalina', '4.2: 0,05 a 1,0 UI/ml')),
         'estandar': [dil('100 UI en 100 ml de SF (1 UI/ml)', 100, 'UI', 100, C('insulina-cristalina', '4.2: concentraciones de 0,05 a 1,0 UI/ml en SF o SG'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Vía IV solo por profesionales, con vial (no plumas), en bolsa de polipropileno y bomba de infusión, con control frecuente de glicemia y potasio. Antes de usar purgar el equipo (la insulina se adsorbe al plástico).', 'requiereBomba': True, 'fuente': C('insulina-cristalina', '4.2 Administración intravenosa')},
        [dosis('Requerimiento total diario habitual (vía SC; referencia)', 'adulto', 'UI/kg/24 h', C('insulina-cristalina', '4.2: 0,3–1,0 UI/kg/día'), mn=0.3, mx=1)],
        {'ambienteH': 24, 'fuente': C('insulina-cristalina', '4.2: diluida 0,05–1 UI/ml estable 24 h a temperatura ambiente')},
        [ix('Betabloqueadores', 'Pueden enmascarar los síntomas de hipoglicemia', C('insulina-cristalina', '4.5')),
         ix('Glucocorticoides y tiazidas', 'Aumentan las necesidades de insulina', C('insulina-cristalina', '4.5'))],
        ea([], ['Hipoglicemia', 'Hipokalemia (vía IV)'], ['Glicemia capilar frecuente', 'Potasio'], C('insulina-cristalina', '4.8')),
        [ALTO, 'Solo insulina cristalina (regular) por vía EV.', 'Rotular siempre UI/ml de la dilución.'],
        discrepancias=[{'campo': 'dosis EV', 'valores': ['CIMA no indica dosis EV por indicación (cetoacidosis, hiperkalemia)'], 'decision': 'Sin dosis EV por indicación: seguir el protocolo local de la institución.'}],
    )

    F['cloruro-de-potasio'] = ficha(
        'cloruro-de-potasio', 'Cloruro de potasio 10 %', 'electrolito', URG_H, True,
        [pres('amp-10pct-10ml', 'ampolla 10 % (1 g)', 13.41, 'mEq', 10, P('Anexo 6, Cloruro de potasio 10 %: ampolla de 10 ml, 1 g = 13,41 mEq de K'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(0.04, 'mEq', P('Anexo 6, Cloruro de potasio: máximo por vía periférica 40 mEq/L (central 80 mEq/L)')),
         'estandar': [dil('20 mEq en 500 ml (40 mEq/L), vía periférica', 20, 'mEq', 500, P('Anexo 6, Cloruro de potasio: máximo periférico 40 mEq/L'))]},
        {'vias': ['infusion_intermitente', 'infusion_continua'], 'texto': 'NUNCA en bolo ni sin diluir: la inyección directa puede causar paro cardíaco instantáneo. Mezclar completamente en el suero, infundir por bomba y con ECG si la velocidad es alta. En críticos preferir SF (la glucosa puede bajar el potasio).', 'requiereBomba': True, 'fuente': fu('FDA-POTASIO', 'Warnings; Dosage and administration')},
        [dosis('Reposición con K sérico > 2,5 mEq/L', 'adulto', 'mEq/h', fu('FDA-POTASIO', 'Hasta 10 mEq/h, concentración hasta 40 mEq/L; máx. 200 mEq/24 h'), mx=10),
         dosis('Urgente: K < 2,0 mEq/L con cambios en ECG o parálisis (monitor continuo)', 'adulto', 'mEq/h', fu('FDA-POTASIO', 'Hasta 40 mEq/h; hasta 400 mEq/24 h'), mx=40),
         dosis('Dosis diaria máxima habitual', 'adulto', 'mEq/24 h', fu('FDA-POTASIO', 'No exceder 200 mEq/24 h (400 en urgencia)'), mx=200, maxima=400)],
        {'fuente': fu('FDA-POTASIO', 'Dosage and administration (no informa estabilidad de la dilución)')},
        [ix('Digitálicos', 'Guiar la terapia con ECG seriados', fu('FDA-POTASIO', 'Precautions'))],
        ea(['Dolor o flebitis en el sitio de infusión'], ['Hiperkalemia', 'Arritmias y paro cardíaco con infusión rápida o sin diluir'], ['ECG', 'Potasio sérico', 'Diuresis', 'Sitio de infusión'], fu('FDA-POTASIO', 'Adverse reactions')),
        [ALTO, 'NUNCA en bolo. Diluir siempre y agitar la mezcla.', 'Máximo 40 mEq/L por vía periférica y 80 mEq/L por vía central.'],
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['Pucón y FDA no indican dosis pediátrica'], 'decision': 'Sin dosis pediátrica: usar el protocolo pediátrico local.'}],
    )

    F['bicarbonato-de-sodio'] = ficha(
        'bicarbonato-de-sodio', 'Bicarbonato de sodio 8,4 %', 'electrolito', URG, False,
        [pres('amp-10meq-10ml', 'ampolla 8,4 % (1 M)', 10, 'mEq', 10, C('bicarbonato-de-sodio', '2: 840 mg = 10 mmol (10 mEq) por ampolla de 10 ml'))],
        {'sueros': ['SG5', 'SF'], 'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Inyección IV lenta de la solución hipertónica sin diluir o diluida en perfusión, asegurando ventilación adecuada. Incompatible con muchos fármacos (catecolaminas, calcio): lavar la vía antes y después.', 'fuente': C('bicarbonato-de-sodio', '4.2; 6.2; 6.6')},
        [dosis('Paro cardíaco: dosis inicial', 'adulto', 'mEq/kg', C('bicarbonato-de-sodio', '4.2: 1 mEq/kg (1 ml/kg de 8,4 %)'), mn=1, mx=1),
         dosis('Acidosis grave menos crítica (perfusión en 4–8 h)', 'adulto', 'mEq/kg', C('bicarbonato-de-sodio', '4.2: 2–5 mEq/kg'), mn=2, mx=5),
         dosis('Dosis inicial (niños), IV lenta', 'pediatrico', 'mEq/kg', C('bicarbonato-de-sodio', '4.2: 1 mEq/kg'), mn=1, mx=1, tope=(70, 'mEq'))],
        {'fuente': C('bicarbonato-de-sodio', '6.3: usar inmediatamente tras abrir')},
        [ix('Corticoides con acción mineralocorticoide o ACTH', 'Retención de agua y sodio', C('bicarbonato-de-sodio', '4.5')),
         ix('Litio', 'Aumenta la excreción renal de litio', C('bicarbonato-de-sodio', '4.5'))],
        ea([], ['Alcalosis metabólica', 'Hipokalemia', 'Hipocalcemia', 'Hipernatremia e hiperosmolaridad', 'Necrosis por extravasación'], ['Gases arteriales', 'Potasio y calcio', 'Sitio de punción'], C('bicarbonato-de-sodio', '4.8')),
        ['No administrar por la misma vía que catecolaminas o calcio sin lavar.'],
        discrepancias=[{'campo': 'fuente chilena / tope pediátrico', 'valores': ['Pucón 2022 no incluye bicarbonato', 'CIMA: 1 mEq/kg en niños sin tope'], 'decision': 'Tope adulto de 70 mEq (1 mEq/kg × 70 kg) fijado para el cálculo; confirmar presentación (ampolla 8,4 % de 10 o 20 ml).'}],
    )

    F['gluconato-de-calcio'] = ficha(
        'gluconato-de-calcio', 'Gluconato de calcio 10 %', 'electrolito', URG_H, True,
        [pres('amp-10pct-10ml', 'ampolla 10 %', 1, 'g', 10, fu('FDA-GLUCONATO-CALCIO', '100 mg/ml; vial de 10 ml = 1.000 mg (Pucón: ampolla de 10 ml al 10 %)'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(50, 'mg', fu('FDA-GLUCONATO-CALCIO', '2.1: bolo diluido a 10–50 mg/ml')),
         'estandar': [dil('1 g en 20 ml (50 mg/ml), bolo lento', 1, 'g', 20, P('Anexo 6, Calcio gluconato 10 %: dilución 50 mg/ml')),
                      dil('1 g en 100 ml (10 mg/ml), infusión', 1, 'g', 100, fu('FDA-GLUCONATO-CALCIO', '2.1: infusión continua 5,8–10 mg/ml'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Diluir en SG5 % o SF. Bolo lento sin superar 200 mg/min en adultos y 100 mg/min en niños, con ECG. Vía IV segura (necrosis y calcinosis por extravasación). No mezclar con fosfato ni bicarbonato; nunca con ceftriaxona en neonatos.', 'fuente': fu('FDA-GLUCONATO-CALCIO', '2.1; 2.5')},
        [dosis('Hipocalcemia: bolo (repetible cada 6 h)', 'adulto', 'mg', fu('FDA-GLUCONATO-CALCIO', 'Tabla 1: 1.000–2.000 mg'), mn=1000, mx=2000),
         dosis('Hipocalcemia: infusión continua inicial', 'adulto', 'mg/kg/h', fu('FDA-GLUCONATO-CALCIO', 'Tabla 1: 5,4–21,5 mg/kg/h'), mn=5.4, mx=21.5),
         dosis('Hipocalcemia: bolo (> 1 mes a < 17 años)', 'pediatrico', 'mg/kg', fu('FDA-GLUCONATO-CALCIO', 'Tabla 1: 29–60 mg/kg'), mn=29, mx=60, tope=(2000, 'mg')),
         dosis('Hipocalcemia: infusión inicial (niños)', 'pediatrico', 'mg/kg/h', fu('FDA-GLUCONATO-CALCIO', 'Tabla 1: 8–13 mg/kg/h'), mn=8, mx=13)],
        {'fuente': fu('FDA-GLUCONATO-CALCIO', '2.1: usar la dilución inmediatamente')},
        [ix('Digoxina', 'Arritmias sinérgicas', fu('FDA-GLUCONATO-CALCIO', '7.1')),
         ix('Ceftriaxona', 'Precipitados de ceftriaxona-calcio; contraindicado en neonatos', fu('FDA-GLUCONATO-CALCIO', '2.5'))],
        ea(['Vasodilatación', 'Sensación de calor'], ['Bradicardia, hipotensión y arritmias', 'Necrosis y calcinosis por extravasación'], ['ECG durante el bolo', 'Calcemia', 'Sitio de punción'], P('Anexo 6, Calcio gluconato 10 %: RAM')),
        [ALTO, 'No confundir con cloruro de calcio 10 % (tres veces más calcio).'],
        discrepancias=[{'campo': 'composición', 'valores': ['Pucón: ampolla de 10 ml; 0,47 mEq de calcio (por ml)', 'FDA: 100 mg/ml = 0,465 mEq/ml de calcio elemental'], 'decision': 'Concordantes; se registra en mg de gluconato (1 g/10 ml).'}],
    )

    F['glucosa-30'] = ficha(
        'glucosa-30', 'Glucosa 30 %', 'metabolico', URG_H, False,
        [pres('fco-30pct-500ml', 'frasco 30 % (500 ml)', 150, 'g', 500, C('glucosa-30', '2: 300 mg/ml; 150 g en 500 ml'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Hipertónica: preferir vía central; en hipoglicemia puede pasarse lento por vena periférica. Tomar glicemia antes, sin retrasar el tratamiento.', 'fuente': C('glucosa-30', '4.2 Forma de administración')},
        [dosis('Hipoglicemia por insulina (repetible)', 'adulto', 'g', fu('FDA-DEXTROSA-50', '10–25 g IV lenta'), mn=10, mx=25),
         dosis('Aporte máximo', 'adulto', 'g/kg/h', C('glucosa-30', '4.2: hasta 0,3 g/kg/h'), mx=0.3)],
        {'fuente': C('glucosa-30', '6.3 (no informa estabilidad tras abrir)')},
        [ix('Insulina y antidiabéticos', 'Antagonismo del efecto hipoglicemiante', C('glucosa-30', '4.5')),
         ix('Digoxina', 'Aumento de la actividad digitálica (hipokalemia)', C('glucosa-30', '4.5'))],
        ea([], ['Hiperglicemia', 'Síndrome hiperosmolar con administración rápida', 'Flebitis y trombosis venosa'], ['Glicemia', 'Potasio, magnesio y fósforo', 'Sitio de punción'], C('glucosa-30', '4.8')),
        ['Solución hipertónica: riesgo de flebitis por vía periférica.'],
        discrepancias=[{'campo': 'presentación', 'valores': ['CIMA: frasco de 500 ml al 30 %', 'En Chile es habitual la ampolla de 20 ml al 30 % (6 g), no confirmada en fuente chilena'], 'decision': 'Se registra la de CIMA; confirmar la presentación local. «Volumen a cargar» usa 300 mg/ml en ambos casos.'}],
    )

    F['propofol'] = ficha(
        'propofol', 'Propofol 1 %', 'anestesico', URG, True,
        [pres('amp-200mg-20ml', 'ampolla 1 %', 200, 'mg', 20, P('Anexo 6, Propofol 1 %: ampolla de 20 ml y FA de 50 ml (10 mg/ml)')),
         pres('fa-500mg-50ml', 'frasco ampolla 1 %', 500, 'mg', 50, P('Anexo 6, Propofol 1 %: ampolla de 20 ml y FA de 50 ml (10 mg/ml)'))],
        {'sueros': ['SG5'], 'concentracionMin': conc(2, 'mg', C('propofol', '6.6 Tabla 1: 1 parte con hasta 4 partes de SG5 % (≥ 2 mg/ml)')),
         'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Agitar antes de usar. Inducción en bolo lento (≈ 40 mg cada 10 s) o perfusión; mantención por bomba. Preferir vena gruesa o CVC y máxima asepsia (emulsión lipídica). Solo la presentación al 1 % puede diluirse, y únicamente en SG5 %.', 'requiereBomba': True, 'fuente': C('propofol', '4.2.1; 6.2')},
        [dosis('Inducción anestésica (< 55 años)', 'adulto', 'mg/kg', C('propofol', '4.2.1: 1,5–2,5 mg/kg'), mn=1.5, mx=2.5),
         dosis('Mantención de la anestesia', 'adulto', 'mg/kg/h', C('propofol', '4.2.1: 4–12 mg/kg/h'), mn=4, mx=12),
         dosis('Sedación en UCI (ventilación mecánica)', 'adulto', 'mg/kg/h', C('propofol', '4.2.1: 0,3–4 mg/kg/h; no superar 4 mg/kg/h'), mn=0.3, mx=4),
         dosis('Inducción anestésica (> 8 años; 1 mes–3 años hasta 4 mg/kg)', 'pediatrico', 'mg/kg', C('propofol', '4.2.1 Población pediátrica: 2,5 mg/kg (2,5–4 en menores)'), mn=2.5, mx=4, tope=(200, 'mg'))],
        {'ambienteH': 6, 'fuente': C('propofol', '6.3: diluido, usar dentro de 6 h')},
        [ix('Depresores del SNC (opioides, benzodiazepinas)', 'Depresión respiratoria y circulatoria aditiva', C('propofol', '4.5'))],
        ea(['Hipotensión', 'Dolor en el sitio de inyección', 'Apnea transitoria'], ['Bradicardia', 'Síndrome de perfusión por propofol (> 4 mg/kg/h por más de 48 h)', 'Anafilaxia'], ['PA, FC, SatO2 y ventilación', 'Triglicéridos en uso prolongado'], C('propofol', '4.8; 4.4')),
        [ALTO, 'Contraindicado para sedación en UCI en menores de 16 años.', 'Desechar la emulsión sobrante.'],
        discrepancias=[{'campo': 'tope pediátrico', 'valores': ['CIMA adulto: 1,5–2,5 mg/kg (≈ 175 mg en 70 kg)'], 'decision': 'Tope adulto de 200 mg fijado para el cálculo; confirmar.'}],
    )

    F['etomidato'] = ficha(
        'etomidato', 'Etomidato', 'anestesico', URG, True,
        [pres('amp-20mg-10ml', 'ampolla', 20, 'mg', 10, P('Anexo 4 y 6, Etomidato: 20 mg/10 ml'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo'], 'texto': 'Sin diluir, IV lenta en unos 30 segundos. Agitar la ampolla. No mezclar con otros fármacos. Precaución con hipotensión.', 'tiempoMinimoMin': 0.5, 'fuente': P('Anexo 6, Etomidato: 0,3 mg/kg en 30 segundos; no requiere dilución')},
        [dosis('Inducción / secuencia rápida', 'adulto', 'mg/kg', C('etomidato', '4.2.1: 0,3 mg/kg; no exceder 3 ampollas (60 mg)'), mn=0.3, mx=0.3, maxima=60),
         dosis('Inducción (niños)', 'pediatrico', 'mg/kg', PED('etomidato', '0,15–0,3 mg/kg; hasta 0,4 mg/kg'), mn=0.15, mx=0.3, tope=(60, 'mg'))],
        {'fuente': C('etomidato', '6.3: usar inmediatamente una vez abierto')},
        [ix('Opioides, sedantes, neurolépticos, alcohol', 'Potencian el efecto hipnótico', C('etomidato', '4.5'))],
        ea(['Mioclonías', 'Dolor en el sitio de inyección', 'Náuseas y vómitos'], ['Supresión suprarrenal', 'Depresión respiratoria'], ['PA', 'Ventilación'], C('etomidato', '4.8')),
        [ALTO],
    )

    F['rocuronio'] = ficha(
        'rocuronio', 'Rocuronio', 'bloqueador-neuromuscular', URG, True,
        [pres('fa-50mg-5ml', 'frasco ampolla', 50, 'mg', 5, C('rocuronio', '2: 10 mg/ml'))],
        {'sueros': ['SF', 'SG5'], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV; perfusión por bomba (compatible a 0,5–2 mg/ml en SF o SG5 %). Solo con manejo avanzado de vía aérea y ventilación. Monitorizar el bloqueo (tren de cuatro).', 'fuente': C('rocuronio', '4.2; 6.6')},
        [dosis('Secuencia rápida de intubación', 'adulto', 'mg/kg', fu('URGENCIA-UC-SRI-2015', 'Rocuronio 1–1,2 mg/kg (CIMA 4.2: 1,0 mg/kg)'), mn=1, mx=1.2),
         dosis('Mantención (bolos)', 'adulto', 'mg/kg', C('rocuronio', '4.2: 0,15 mg/kg'), mn=0.15, mx=0.15),
         dosis('Perfusión continua', 'adulto', 'mg/kg/h', C('rocuronio', '4.2: 0,3–0,6 mg/kg/h'), mn=0.3, mx=0.6),
         dosis('Secuencia rápida de intubación (niños)', 'pediatrico', 'mg/kg', PED('rocuronio', 'SRI 0,9–1,2 mg/kg'), mn=0.9, mx=1.2, tope=(84, 'mg'))],
        {'fuente': C('rocuronio', '6.3: diluido, estabilidad en uso 72 h a 30 °C; microbiológicamente usar de inmediato')},
        [ix('Anestésicos volátiles halogenados', 'Potencian el bloqueo neuromuscular', C('rocuronio', '4.5'))],
        ea(['Dolor en el sitio de inyección'], ['Anafilaxia', 'Bloqueo neuromuscular prolongado'], ['Ventilación asegurada', 'Tren de cuatro'], C('rocuronio', '4.8')),
        [ALTO, 'Paraliza la respiración: solo con vía aérea y ventilación aseguradas.', 'Incompatible en Y con varios fármacos (p. ej., cefazolina, dexametasona, diazepam, furosemida).'],
        discrepancias=[{'campo': 'tope pediátrico', 'valores': ['Urgencia UC: 1–1,2 mg/kg (≈ 84 mg con 1,2 mg/kg × 70 kg)'], 'decision': 'Tope adulto de 84 mg fijado para el cálculo; confirmar.'}],
    )

    F['succinilcolina'] = ficha(
        'succinilcolina', 'Succinilcolina (suxametonio)', 'bloqueador-neuromuscular', URG, True,
        [pres('amp-100mg-2ml', 'ampolla', 100, 'mg', 2, C('succinilcolina', '2: 50 mg/ml; ampolla de 2 ml = 100 mg'))],
        {'sueros': ['SG5', 'SF'], 'concentracionMax': conc(2, 'mg', C('succinilcolina', '4.2: perfusión al 0,1–0,2 % (1–2 mg/ml)')),
         'estandar': [dil('500 mg en 500 ml (0,1 %, 1 mg/ml)', 500, 'mg', 500, C('succinilcolina', '4.2: solución al 0,1 %'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV para intubación; perfusión al 0,1–0,2 % a 2,5–4 mg/min. Solo con manejo de vía aérea y ventilación. No mezclar con soluciones alcalinas (barbitúricos).', 'fuente': C('succinilcolina', '4.2; 6.2')},
        [dosis('Intubación traqueal', 'adulto', 'mg/kg', C('succinilcolina', '4.2: 1 mg/kg; dosis total máx. 500 mg'), mn=1, mx=1, maxima=500),
         dosis('Perfusión', 'adulto', 'mg/min', C('succinilcolina', '4.2: 2,5–4 mg/min'), mn=2.5, mx=4),
         dosis('Intubación, niños 1–12 años', 'pediatrico', 'mg/kg', C('succinilcolina', '4.2: 1–2 mg/kg (lactantes 2 mg/kg)'), mn=1, mx=2, tope=(150, 'mg'))],
        {'fuente': C('succinilcolina', '6.3: usar inmediatamente una vez abierto')},
        [ix('Lidocaína, procainamida, quinidina, verapamilo', 'Potencian la relajación muscular', C('succinilcolina', '4.5')),
         ix('Aminoglucósidos', 'Potencian el bloqueo', C('succinilcolina', '4.5'))],
        ea(['Fasciculaciones', 'Aumento de la presión intraocular', 'Bradicardia o taquicardia'], ['Hiperkalemia con arritmias o paro', 'Hipertermia maligna', 'Anafilaxia'], ['ECG', 'Temperatura', 'Ventilación asegurada'], C('succinilcolina', '4.8')),
        [ALTO, 'Contraindicada con antecedente de hipertermia maligna e hiperkalemia.'],
        discrepancias=[{'campo': 'fuente chilena / tope pediátrico', 'valores': ['Pucón 2022 no incluye succinilcolina', 'Pediamécum: dosis total no superior a 150 mg'], 'decision': 'Ficha basada en CIMA; tope pediátrico de 150 mg según Pediamécum.'}],
    )

    F['clorfenamina'] = ficha(
        'clorfenamina', 'Clorfenamina', 'antihistaminico', URG_H, False,
        [pres('amp-10mg-2ml', 'ampolla', 10, 'mg', 2, P('Anexo 6, Clorfenamina: 10 mg/2 ml'))],
        {'sueros': ['SF'], 'estandar': [dil('10 mg en 10 ml de SF (bolo)', 10, 'mg', 10, P('Anexo 6, Clorfenamina: bolo directo diluido en 10 cc de SF 0,9 %'))]},
        {'vias': ['bolo'], 'texto': 'Bolo directo diluido en 10 ml de SF, administrado en 1 a 3 minutos. También IM.', 'tiempoMinimoMin': 1, 'fuente': P('Anexo 6, Clorfenamina: administrar en 1–3 min')},
        [],
        {'fuente': P('Anexo 6, Clorfenamina (no informa estabilidad)')},
        [],
        ea(['Somnolencia', 'Disminución de la acción refleja'], [], ['Nivel de conciencia'], P('Anexo 6, Clorfenamina: RAM')),
        ['Las fuentes revisadas no indican dosis: seguir la indicación médica.'],
        discrepancias=[{'campo': 'dosis', 'valores': ['Pucón: sin dosis', 'CIMA solo tiene dexclorfeniramina (otra molécula)', 'Pediamécum sin ficha de clorfenamina'], 'decision': 'Ficha sin dosis; buscar una fuente chilena con dosis en la revisión.'}],
    )

    return F
