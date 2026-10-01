"""Tanda 1, parte 1 (10 medicamentos). Valores citados; ver informes/tanda-1-parte-1.md."""
from .comun import CONSULTA, C, P, PED, ajustar, fu, meta  # noqa: F401

CIMA = {
    'adrenalina': ('80831', 'Adrenalina Aguettant 0,1 mg/ml solución inyectable en jeringa precargada'),
    'noradrenalina': ('62002', 'Noradrenalina B. Braun 0,5 mg/ml concentrado para solución para perfusión'),
    'amiodarona': ('54723', 'Trangorex 150 mg/3 ml solución inyectable'),
    'atropina': ('85535', 'Atropina Accord 0,1 mg/ml solución inyectable en jeringa precargada'),
    'adenosina': ('81545', 'Adenosina Accord 6 mg/2 ml solución inyectable'),
    'midazolam': ('63936', 'Midazolam Normon 1 mg/ml solución inyectable y para perfusión'),
    'fentanilo': ('88464', 'Fentanilo Basi 50 microgramos/ml solución inyectable'),
    'morfina': ('82748', 'Morfina B. Braun 1 mg/ml solución inyectable'),
    'ketamina': ('47034', 'Ketolar 50 mg/ml solución inyectable'),
    'sulfato-de-magnesio': ('78350', 'Sulfato de Magnesio Altan 150 mg/ml solución inyectable y para perfusión'),
}

FUENTES = [
    {
        'id': 'PUCON-2022',
        'titulo': 'Protocolo de administración de medicamentos endovenosos GCL 1.2.6, 2.ª edición (Anexo 4: alto riesgo; Anexo 6: tabla de dilución)',
        'institucion': 'Hospital San Francisco de Pucón (Chile)',
        'url': 'https://www.hospitalsanfranciscodepucon.cl/wp-content/uploads/2023/04/GCL-1.2.6-Protocolo-Administracio%CC%81n-de-Medicamentos-ev-2-edicio%CC%81n-2022-RAC.pdf',
        'anio': 2022,
        'consultado': CONSULTA,
    },
    {
        'id': 'STABILIS-Y',
        'titulo': 'Tabla de compatibilidades en Y con solventes usuales (generada para los 84 medicamentos de la app que figuran en Stabilis)',
        'institucion': 'Stabilis / Infostab',
        'url': 'https://www.stabilis.org/TableIncompatibilites.php',
        'anio': 2026,
        'consultado': CONSULTA,
    },
    {
        'id': 'FDA-EPINEFRINA',
        'titulo': 'Epinephrine injection — Prescribing information (sección 2, Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=0172280c-f7d6-4613-9dbd-f94d3ae5825a',
        'anio': 2026,
        'consultado': CONSULTA,
    },
    {
        'id': 'FDA-NOREPINEFRINA',
        'titulo': 'Norepinephrine bitartrate injection — Prescribing information (sección 2, Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=0ea48ab6-e166-df31-b132-70ef982a2d02',
        'anio': 2025,
        'consultado': CONSULTA,
    },
    {
        'id': 'URGENCIA-UC-SRI-2015',
        'titulo': 'Secuencia rápida de intubación en el Servicio de Urgencia (Series clínicas de Medicina de Urgencia; Maluenda, Aguilera, Kripper, Navea, Basaure). Rev Chil Med Intensiva 2015;30(1):23-32',
        'institucion': 'Programa de Medicina de Urgencia, Pontificia Universidad Católica de Chile',
        'url': 'https://urgencia.uc.cl/htdocs/content/uploads/2021/04/secuencia-rapida-de-intubacion-servicio-de-urgencia-series-clinicas-urgencia-uc-articulo-2015.pdf',
        'anio': 2015,
        'consultado': CONSULTA,
    },
    {
        'id': 'ES-RIOJA-SEDOANALGESIA-2024',
        'titulo': 'FUENTE EXTRANJERA (España) — Sedoanalgesia para procedimientos en urgencias, versión 1 (19-04-2024)',
        'institucion': 'Servicio de Urgencias, Hospital Universitario San Pedro (Logroño, La Rioja, España)',
        'url': 'https://www.riojasalud.es/files/content/servicios/urgencias/profesionales/Sedoanalgesia%20para%20procedimientos%20en%20urgencias.pdf',
        'anio': 2024,
        'consultado': CONSULTA,
    },
    {
        'id': 'FDA-ADENOSINA',
        'titulo': 'Adenosine injection — Prescribing information (Dosage and administration, adult patients)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=296af833-5724-3e23-e063-6394a90a6251',
        'anio': 2024,
        'consultado': CONSULTA,
    },
]
for k, (nreg, nombre) in CIMA.items():
    FUENTES.append({
        'id': f'CIMA-{k.upper()}',
        'titulo': f'Ficha técnica: {nombre}',
        'institucion': 'AEMPS — CIMA (España)',
        'url': f'https://cima.aemps.es/cima/dochtml/ft/{nreg}/FT_{nreg}.html',
        'anio': 2026,
        'consultado': CONSULTA,
    })
for k in ['fentanilo', 'morfina', 'ketamina', 'amiodarona']:
    FUENTES.append({
        'id': f'PEDIAMECUM-{k.upper()}',
        'titulo': f'Pediamécum: {k.capitalize()} (Dosis y pautas de administración)',
        'institucion': 'Asociación Española de Pediatría',
        'url': f'https://www.aeped.es/comite-medicamentos/pediamecum/{k}',
        'anio': 2026,
        'consultado': CONSULTA,
    })


# --- Compatibilidad en Y desde Stabilis ---
COL = {'SF': 'SF', 'SG5': 'SG5', 'adenosina': 'adenosina', 'amiodarona': 'amiodarona', 'atropina': 'atropina',
       'adrenalina': 'adrenalina', 'fentanilo': 'fentanilo', 'ketamina': 'ketamina', 'magnesio': 'sulfato-de-magnesio',
       'midazolam': 'midazolam', 'morfina': 'morfina', 'noradrenalina': 'noradrenalina'}


def compatibilidad(stab, fila):
    res = []
    for col, con in COL.items():
        if con == (COL[fila] if fila in COL else fila):
            continue
        k = stab[fila][col]
        if k == 'G':
            res.append({'con': con, 'estado': 'compatible', 'fuente': fu('STABILIS-Y', 'Compatibilidad física en Y (casilla verde)')})
        elif k == 'R':
            res.append({'con': con, 'estado': 'incompatible', 'fuente': fu('STABILIS-Y', 'Incompatibilidad en Y (casilla roja)')})
        elif k == 'Y':
            res.append({'con': con, 'estado': 'incompatible', 'fuente': fu('STABILIS-Y', 'Datos contradictorios en la literatura (casilla amarilla); se registra como incompatible por criterio conservador')})
        else:
            res.append({'con': con, 'estado': 'sin_datos', 'fuente': fu('STABILIS-Y', 'Sin datos de compatibilidad (casilla blanca)')})
    return res





def fichas(stab):
    F = {}

    F['adrenalina'] = {
        'id': 'adrenalina', 'nombre': 'Adrenalina (epinefrina)', 'comerciales': [], 'grupo': 'vasoactivo',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': True,
        'presentaciones': [{'id': 'amp-1mg-1ml', 'forma': 'ampolla', 'cantidad': {'valor': 1, 'unidad': 'mg'}, 'volumenMl': 1, 'fuente': P('Anexo 6, Adrenalina: 1 mg/1 ml')}],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SG5', 'SF'],
            'estandar': [
                {'descripcion': '1 mg en 10 ml de SF (0,1 mg/ml, 1:10.000) para bolo', 'cantidad': {'valor': 1, 'unidad': 'mg'}, 'volumenFinalMl': 10, 'fuente': P('Anexo 6, Adrenalina: dilución estándar 1 mg/10 ml SF')},
                {'descripcion': '4 mg en 100 ml (40 mcg/ml) para infusión', 'cantidad': {'valor': 4, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Adrenalina: habitual 4 mg en 100 ml')},
            ],
        },
        'administracion': {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV/IO en paro; infusión continua diluida en solución glucosada, en vena de grueso calibre. La FDA no recomienda diluir solo en suero fisiológico (pérdida de potencia por oxidación).', 'fuente': fu('FDA-EPINEFRINA', '2.2 Hypotension associated with septic shock')},
        'dosis': [
            {'indicacion': 'Paro cardiorrespiratorio (cada 3–5 min)', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 1, 'max': 1, 'fuente': C('adrenalina', '4.2 Reanimación cardiopulmonar')},
            {'indicacion': 'Anafilaxia aguda (bolos IV según respuesta)', 'poblacion': 'adulto', 'unidad': 'mcg', 'min': 50, 'max': 50, 'fuente': C('adrenalina', '4.2 Anafilaxia aguda: bolos de 0,05 mg')},
            {'indicacion': 'Hipotensión en shock séptico (infusión)', 'poblacion': 'adulto', 'unidad': 'mcg/kg/min', 'min': 0.05, 'max': 2, 'fuente': fu('FDA-EPINEFRINA', '2.2: 0.05 to 2 mcg/kg/min')},
            {'indicacion': 'Paro cardíaco (> 5 kg), cada 3–5 min', 'poblacion': 'pediatrico', 'unidad': 'mcg/kg', 'max': 10, 'topeAdulto': {'valor': 1, 'unidad': 'mg'}, 'fuente': C('adrenalina', '4.2 Paro cardiaco en niños: 10 mcg/kg, máx. 1 mg')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('adrenalina', '6.3 Periodo de validez (no informa estabilidad de la dilución)')},
        'compatibilidad': compatibilidad(stab, 'adrenalina'),
        'interaccionesGraves': [
            {'con': 'Anestésicos halogenados volátiles', 'efecto': 'Arritmia ventricular grave', 'fuente': C('adrenalina', '4.5')},
            {'con': 'Antidepresivos tipo imipramina (tricíclicos)', 'efecto': 'Hipertensión arterial paroxística', 'fuente': C('adrenalina', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': [], 'graves': ['Hemorragia cerebrovascular y arritmias con administración rápida', 'Necrosis por extravasación'], 'vigilar': ['Monitorización continua', 'Sitio de infusión (extravasación)'], 'fuente': P('Anexo 6, Adrenalina: precauciones y RAM')},
        'alertas': ['Medicamento de alto riesgo.', 'No confundir la ampolla 1 mg/ml (1:1.000) con la dilución 0,1 mg/ml (1:10.000).'],
        'meta': meta(),
    }

    F['noradrenalina'] = {
        'id': 'noradrenalina', 'nombre': 'Noradrenalina (norepinefrina)', 'comerciales': [], 'grupo': 'vasoactivo',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': True,
        'presentaciones': [{'id': 'amp-4mg-4ml', 'forma': 'ampolla', 'cantidad': {'valor': 4, 'unidad': 'mg'}, 'volumenMl': 4, 'fuente': P('Anexo 6, Norepinefrina: 4 mg/4 ml')}],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SG5'],
            'concentracionMax': {'valor': 160, 'unidad': 'mcg', 'fuente': P('Anexo 6, Norepinefrina: en restricción de volumen hasta 160 mcg/ml')},
            'estandar': [
                {'descripcion': '4 mg en 100 ml (40 mcg/ml)', 'cantidad': {'valor': 4, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Norepinefrina: habitual 4 mg/100 ml')},
                {'descripcion': '8 mg en 200 ml (40 mcg/ml)', 'cantidad': {'valor': 8, 'unidad': 'mg'}, 'volumenFinalMl': 200, 'fuente': P('Anexo 6, Norepinefrina: 8 mg/200 ml')},
                {'descripcion': '16 mg en 100 ml (160 mcg/ml), restricción de volumen', 'cantidad': {'valor': 16, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Norepinefrina: 16 mg/100 ml')},
                {'descripcion': '4 mg en 1.000 ml de SG5 % (4 mcg/ml)', 'cantidad': {'valor': 4, 'unidad': 'mg'}, 'volumenFinalMl': 1000, 'fuente': fu('FDA-NOREPINEFRINA', '2.3 Preparation of diluted solution')},
            ],
        },
        'administracion': {'vias': ['infusion_continua'], 'texto': 'Infusión continua por bomba en vena de grueso calibre. Diluir en solución glucosada (la dextrosa reduce la oxidación); no se recomienda suero fisiológico solo. Controlar la PA cada 2 min hasta el efecto y luego cada 5 min. Retirar gradualmente.', 'requiereBomba': True, 'fuente': fu('FDA-NOREPINEFRINA', '2.1–2.3')},
        'dosis': [
            {'indicacion': 'Dosis inicial y mantención (adulto)', 'poblacion': 'adulto', 'unidad': 'mcg/min', 'min': 2, 'max': 12, 'fuente': fu('FDA-NOREPINEFRINA', '2.2: inicial 8–12 mcg/min; mantención 2–4 mcg/min')},
            {'indicacion': 'Shock séptico', 'poblacion': 'adulto', 'unidad': 'mcg/kg/min', 'max': 1, 'fuente': C('noradrenalina', '4.2: alrededor de 0,5 hasta un máximo de 1 mcg/kg/min')},
            {'indicacion': 'Infusión pediátrica', 'poblacion': 'pediatrico', 'unidad': 'mcg/kg/min', 'min': 0.1, 'max': 1, 'fuente': C('noradrenalina', '4.2 Población pediátrica')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('noradrenalina', '6.3: administrar inmediatamente tras la apertura')},
        'compatibilidad': compatibilidad(stab, 'noradrenalina'),
        'interaccionesGraves': [
            {'con': 'Anestésicos (ciclopropano, halotano)', 'efecto': 'Arritmias; uso contraindicado', 'fuente': C('noradrenalina', '4.5')},
            {'con': 'Antidepresivos tricíclicos o maprotilina', 'efecto': 'Potenciación del efecto presor', 'fuente': C('noradrenalina', '4.5')},
            {'con': 'Inhibidores de la monoaminooxidasa (IMAO)', 'efecto': 'Riesgo de crisis hipertensiva', 'fuente': C('noradrenalina', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': ['Cefalea', 'Ansiedad'], 'graves': ['Hipertensión', 'Arritmia', 'Bradicardia o taquicardia', 'Dificultad respiratoria'], 'vigilar': ['Presión arterial cada 2–5 min', 'Sitio de infusión'], 'fuente': P('Anexo 6, Norepinefrina: RAM')},
        'alertas': ['Medicamento de alto riesgo.', 'Incompatible en Y con sulfato de magnesio.'],
        'meta': meta([{'campo': 'presentaciones / dosis', 'valores': ['CIMA expresa la dosis como noradrenalina base (1 mg de bitartrato = 0,5 mg de base)', 'FDA: ampolla 4 mg/4 ml = 4 mg de base'], 'decision': 'Presentación 4 mg/4 ml confirmada en revisión clínica (Héctor Salvo Agüero, TENS, 2026-10-01). Se asume expresada como base; verificar el rotulado del producto local.'}]),
    }

    F['amiodarona'] = {
        'id': 'amiodarona', 'nombre': 'Amiodarona', 'comerciales': [], 'grupo': 'antiarritmico',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': False,
        'presentaciones': [{'id': 'amp-150mg-3ml', 'forma': 'ampolla', 'cantidad': {'valor': 150, 'unidad': 'mg'}, 'volumenMl': 3, 'fuente': P('Anexo 6, Amiodarona: 150 mg/3 ml')}],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SG5'],
            'concentracionMin': {'valor': 0.6, 'unidad': 'mg', 'fuente': C('amiodarona', '6.6: no emplear concentraciones menores de 600 mg/litro')},
            'estandar': [
                {'descripcion': '300 mg en 20 ml de SG5 % (paro: FV/TV sin pulso)', 'cantidad': {'valor': 300, 'unidad': 'mg'}, 'volumenFinalMl': 20, 'fuente': C('amiodarona', '4.2 Resucitación cardiopulmonar')},
                {'descripcion': '600 mg en 250 ml de SG5 % (mantención 24 h)', 'cantidad': {'valor': 600, 'unidad': 'mg'}, 'volumenFinalMl': 250, 'fuente': C('amiodarona', '4.2 Dosis de mantenimiento en 250 ml de dextrosa al 5 %')},
            ],
        },
        'administracion': {'vias': ['bolo', 'infusion_intermitente', 'infusion_continua'], 'texto': 'Diluir solo en SG5 %. Inyección IV nunca en menos de 3 min (salvo paro: inyección rápida); no repetir la inyección antes de 15 min. Carga en perfusión de 20 min a 2 h. Evitar extravasación.', 'tiempoMinimoMin': 3, 'fuente': C('amiodarona', '4.2 y 6.6')},
        'dosis': [
            {'indicacion': 'FV/TV sin pulso resistente a desfibrilación (adicional 150 mg)', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 150, 'max': 300, 'fuente': C('amiodarona', '4.2 Resucitación cardiopulmonar')},
            {'indicacion': 'Dosis de carga (perfusión 20 min–2 h)', 'poblacion': 'adulto', 'unidad': 'mg/kg', 'max': 5, 'fuente': C('amiodarona', '4.2 Perfusión intravenosa: 5 mg/kg')},
            {'indicacion': 'Mantención', 'poblacion': 'adulto', 'unidad': 'mg/24 h', 'min': 600, 'max': 800, 'maximaAbsoluta': 1200, 'fuente': C('amiodarona', '4.2: 600–800 mg/24 h, límite 1.200 mg/24 h')},
            {'indicacion': 'TV sin pulso o FV', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'max': 5, 'topeAdulto': {'valor': 300, 'unidad': 'mg'}, 'fuente': PED('amiodarona', 'Administración i.v.: 5 mg/kg (máximo 300 mg/dosis)')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('amiodarona', '6.3 (no informa estabilidad de la dilución)')},
        'compatibilidad': compatibilidad(stab, 'amiodarona'),
        'interaccionesGraves': [
            {'con': 'Fármacos que pueden inducir torsade de pointes', 'efecto': 'Prolongación del QT y torsade de pointes (contraindicado)', 'fuente': C('amiodarona', '4.3 y 4.5')},
            {'con': 'Digoxina', 'efecto': 'Bradicardia y trastornos de conducción; aumenta digoxinemia', 'fuente': C('amiodarona', '4.5')},
            {'con': 'Warfarina', 'efecto': 'Potencia el efecto anticoagulante', 'fuente': C('amiodarona', '4.5')},
            {'con': 'Betabloqueantes, verapamilo, diltiazem', 'efecto': 'Bradicardia y trastornos de conducción', 'fuente': C('amiodarona', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': ['Cefalea', 'Temblores', 'Fatiga'], 'graves': ['Neuropatía periférica', 'Ataxia'], 'vigilar': ['ECG y frecuencia cardíaca', 'Presión arterial', 'Sitio de infusión (extravasación)'], 'fuente': P('Anexo 6, Amiodarona: RAM')},
        'alertas': ['Diluir solo en SG5 %: incompatible con SF 0,9 % en Y.', 'Usar preferentemente equipos sin DEHP.'],
        'meta': meta([{'campo': 'dosis pediátrica', 'valores': ['CIMA: seguridad y eficacia no establecidas en pediatría', 'Pediamécum: 5 mg/kg (máx. 300 mg) en TV sin pulso/FV'], 'decision': 'Se registra la dosis de Pediamécum con la advertencia de CIMA.'}]),
    }

    F['atropina'] = {
        'id': 'atropina', 'nombre': 'Atropina', 'comerciales': [], 'grupo': 'anticolinergico',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': False,
        'presentaciones': [{'id': 'amp-1mg-1ml', 'forma': 'ampolla', 'cantidad': {'valor': 1, 'unidad': 'mg'}, 'volumenMl': 1, 'fuente': P('Anexo 6, Atropina: 1 mg/1 ml')}],
        'reconstitucion': None,
        'dilucion': {'sueros': ['SF'], 'estandar': [{'descripcion': '1 mg en 10 ml de SF (0,1 mg/ml)', 'cantidad': {'valor': 1, 'unidad': 'mg'}, 'volumenFinalMl': 10, 'fuente': P('Anexo 6, Atropina: dilución estándar')}]},
        'administracion': {'vias': ['bolo'], 'texto': 'Bolo IV rápido: la administración lenta puede provocar bradicardia paradojal.', 'fuente': P('Anexo 6, Atropina: precauciones')},
        'dosis': [
            {'indicacion': 'Bradicardia sinusal (cada 2–5 min)', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 0.5, 'max': 0.5, 'fuente': C('atropina', '4.2')},
            {'indicacion': 'Bloqueo AV (cada 3–5 min, máx. 3 mg)', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 0.5, 'max': 0.5, 'maximaAbsoluta': 3, 'fuente': C('atropina', '4.2')},
            {'indicacion': 'Intoxicación por organofosforados (repetir según signos)', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 0.5, 'max': 2, 'fuente': C('atropina', '4.2')},
            {'indicacion': 'Bradicardia con compromiso hemodinámico', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'max': 0.02, 'topeAdulto': {'valor': 0.6, 'unidad': 'mg'}, 'fuente': C('atropina', '4.2: 0,02 mg/kg dosis única, máx. 0,6 mg')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('atropina', '6.3 (no informa estabilidad de la dilución)')},
        'compatibilidad': compatibilidad(stab, 'atropina'),
        'interaccionesGraves': [{'con': 'Otros anticolinérgicos (tricíclicos, antihistamínicos H1, fenotiazinas, neurolépticos)', 'efecto': 'Suma de efectos anticolinérgicos', 'fuente': C('atropina', '4.5')}],
        'efectosAdversos': {'frecuentes': ['Taquicardia', 'Cefalea', 'Náuseas'], 'graves': ['Arritmia', 'Hipotensión', 'Delirium', 'Ataxia'], 'vigilar': ['Frecuencia cardíaca y ECG'], 'fuente': P('Anexo 6, Atropina: RAM')},
        'alertas': [],
        'meta': meta(),
    }

    F['adenosina'] = {
        'id': 'adenosina', 'nombre': 'Adenosina', 'comerciales': [], 'grupo': 'antiarritmico',
        'ambitos': ['urgencia', 'upc'], 'altoRiesgo': False,
        'presentaciones': [{'id': 'amp-6mg-2ml', 'forma': 'ampolla', 'cantidad': {'valor': 6, 'unidad': 'mg'}, 'volumenMl': 2, 'fuente': P('Anexo 6, Adenosina: 6 mg/2 ml')}],
        'reconstitucion': None,
        'dilucion': {'sueros': [], 'estandar': []},
        'administracion': {'vias': ['bolo'], 'texto': 'Bolo IV rápido sin diluir (1–2 s), lo más proximal posible, seguido de 10 ml de SF en bolo por llave de 3 pasos. Con monitorización ECG continua.', 'fuente': P('Anexo 6, Adenosina')},
        'dosis': [{'indicacion': 'TPSV: 6 mg en bolo rápido; si no cede en 1–2 min, 12 mg', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 6, 'max': 12, 'fuente': fu('FDA-ADENOSINA', 'Adult patients: initial dose 6 mg; repeat 12 mg')},
                  {'indicacion': 'TPSV: primer bolo (incrementos de 0,1 mg/kg hasta máx. 12 mg)', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'max': 0.1, 'topeAdulto': {'valor': 6, 'unidad': 'mg'}, 'fuente': C('adenosina', '4.2 Población pediátrica: 0,1 mg/kg, primer bolo máx. 6 mg')}],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('adenosina', '6.3: utilizar inmediatamente tras abrir')},
        'compatibilidad': compatibilidad(stab, 'adenosina'),
        'interaccionesGraves': [
            {'con': 'Dipiridamol', 'efecto': 'Potencia la adenosina; reducir considerablemente la dosis', 'fuente': C('adenosina', '4.5')},
            {'con': 'Teofilina, aminofilina, cafeína (xantinas)', 'efecto': 'Antagonizan la adenosina; evitar 24 h antes', 'fuente': C('adenosina', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': ['Sofoco', 'Náuseas', 'Mareos', 'Cefalea', 'Sabor metálico'], 'graves': ['Dolor torácico'], 'vigilar': ['Monitorización ECG continua'], 'fuente': P('Anexo 6, Adenosina: RAM y precauciones')},
        'alertas': ['Tener equipo de reanimación disponible durante la administración.'],
        'meta': meta([{'campo': 'dosis adulto', 'valores': ['CIMA: primera dosis 3 mg, luego 6 mg y 12 mg', 'FDA y práctica chilena: 6 mg, luego 12 mg'], 'decision': 'Revisión clínica (Héctor Salvo Agüero, TENS, 2026-10-01): se usa 6 → 12 mg, respaldado por la etiqueta FDA.'}]),
    }

    F['midazolam'] = {
        'id': 'midazolam', 'nombre': 'Midazolam', 'comerciales': [], 'grupo': 'sedante',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': False,
        'presentaciones': [
            {'id': 'amp-5mg-1ml', 'forma': 'ampolla', 'cantidad': {'valor': 5, 'unidad': 'mg'}, 'volumenMl': 1, 'fuente': P('Anexo 6, Midazolam: 5 mg/1 ml')},
            {'id': 'amp-15mg-3ml', 'forma': 'ampolla', 'cantidad': {'valor': 15, 'unidad': 'mg'}, 'volumenMl': 3, 'fuente': P('Anexo 6, Midazolam: 15 mg/3 ml')},
            {'id': 'amp-50mg-10ml', 'forma': 'ampolla', 'cantidad': {'valor': 50, 'unidad': 'mg'}, 'volumenMl': 10, 'fuente': P('Anexo 6, Midazolam: 50 mg/10 ml')},
        ],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SF', 'SG5', 'SG10', 'Ringer', 'Hartmann'],
            'estandar': [
                {'descripcion': '100 mg en 100 ml (1 mg/ml)', 'cantidad': {'valor': 100, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Midazolam: habitual 100 mg/100 ml')},
                {'descripcion': '250 mg en 250 ml (1 mg/ml)', 'cantidad': {'valor': 250, 'unidad': 'mg'}, 'volumenFinalMl': 250, 'fuente': P('Anexo 6, Midazolam: 250 mg/250 ml')},
            ],
        },
        'administracion': {'vias': ['bolo', 'infusion_intermitente', 'infusion_continua'], 'texto': 'Administración lenta y ajustada a la respuesta; no inyectar rápido en una sola embolada.', 'fuente': C('midazolam', '4.2')},
        'dosis': [
            {'indicacion': 'Sedación consciente: dosis inicial (total 3,5–7,5 mg)', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 2, 'max': 2.5, 'maximaAbsoluta': 7.5, 'fuente': C('midazolam', '4.2 tabla, adultos < 60 años')},
            {'indicacion': 'Inducción de la anestesia', 'poblacion': 'adulto', 'unidad': 'mg/kg', 'min': 0.15, 'max': 0.2, 'fuente': C('midazolam', '4.2 tabla, adultos < 60 años')},
            {'indicacion': 'Sedación en UCI: mantención', 'poblacion': 'adulto', 'unidad': 'mg/kg/h', 'min': 0.03, 'max': 0.2, 'fuente': C('midazolam', '4.2 tabla')},
            {'indicacion': 'Sedación consciente 6 meses–5 años: dosis inicial (total < 6 mg)', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'min': 0.05, 'max': 0.1, 'topeAdulto': {'valor': 6, 'unidad': 'mg'}, 'fuente': C('midazolam', '4.2 tabla, población pediátrica')},
            {'indicacion': 'Sedación en UCI > 6 meses: mantención', 'poblacion': 'pediatrico', 'unidad': 'mg/kg/h', 'min': 0.06, 'max': 0.12, 'fuente': C('midazolam', '4.2 tabla, población pediátrica')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'ambienteH': 24, 'refrigeradoH': 72, 'fuente': C('midazolam', '6.3: diluido 24 h a temperatura ambiente o 3 días a 2–8 °C')},
        'compatibilidad': compatibilidad(stab, 'midazolam'),
        'interaccionesGraves': [
            {'con': 'Opioides y otros depresores del SNC', 'efecto': 'Potenciación de la sedación y depresión respiratoria', 'fuente': C('midazolam', '4.5')},
            {'con': 'Antifúngicos azólicos (ketoconazol, itraconazol, fluconazol)', 'efecto': 'Aumentan la concentración de midazolam', 'fuente': C('midazolam', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': [], 'graves': ['Disminución del volumen corriente o de la frecuencia respiratoria', 'Apnea', 'Variaciones de la presión arterial', 'Bradicardia'], 'vigilar': ['Frecuencia respiratoria y SatO2', 'Presión arterial', 'Nivel de sedación'], 'fuente': P('Anexo 6, Midazolam: RAM')},
        'alertas': ['Antagonista: flumazenil.', 'No mezclar con soluciones alcalinas.'],
        'meta': meta(),
    }

    F['fentanilo'] = {
        'id': 'fentanilo', 'nombre': 'Fentanilo', 'comerciales': [], 'grupo': 'analgesico-opioide',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': True,
        'presentaciones': [
            {'id': 'amp-0.1mg-2ml', 'forma': 'ampolla', 'cantidad': {'valor': 100, 'unidad': 'mcg'}, 'volumenMl': 2, 'fuente': P('Anexo 6, Fentanilo: 0,1 mg/2 ml')},
            {'id': 'amp-0.5mg-10ml', 'forma': 'ampolla', 'cantidad': {'valor': 500, 'unidad': 'mcg'}, 'volumenMl': 10, 'fuente': P('Anexo 6, Fentanilo: 0,5 mg/10 ml')},
        ],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SF', 'SG5'],
            'estandar': [
                {'descripcion': '1 mg en 100 ml (10 mcg/ml)', 'cantidad': {'valor': 1, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Fentanilo: habitual 1 mg/100 ml')},
                {'descripcion': '2,5 mg en 250 ml (10 mcg/ml)', 'cantidad': {'valor': 2.5, 'unidad': 'mg'}, 'volumenFinalMl': 250, 'fuente': P('Anexo 6, Fentanilo: 2,5 mg/250 ml')},
            ],
        },
        'administracion': {'vias': ['bolo', 'infusion_intermitente', 'infusion_continua'], 'texto': 'Solo donde se pueda controlar la vía aérea. Inyección IV lenta (reduce efectos adversos).', 'fuente': C('fentanilo', '4.2')},
        'dosis': [
            {'indicacion': 'Analgésico complementario en anestesia, procedimientos menores', 'poblacion': 'adulto', 'unidad': 'mcg/kg', 'max': 2, 'fuente': C('fentanilo', '4.2: dosis bajas 2 mcg/kg')},
            {'indicacion': 'Analgesia para procedimientos dolorosos en urgencia, titulable cada 1–2 min (fuente extranjera: España)', 'poblacion': 'adulto', 'unidad': 'mcg/kg', 'min': 0.5, 'max': 1, 'fuente': fu('ES-RIOJA-SEDOANALGESIA-2024', 'Fentanilo — Dosis: dosis única de 0,5 a 1 mcg/kg IV, titulable cada 1–2 minutos')},
            {'indicacion': 'Premedicación en secuencia rápida de intubación (3 min antes de la inducción)', 'poblacion': 'adulto', 'unidad': 'mcg/kg', 'min': 2, 'max': 3, 'fuente': fu('URGENCIA-UC-SRI-2015', 'Fentanilo: dosis recomendada 2–3 µg/kg tres minutos antes de la inducción')},
            {'indicacion': 'Dolor agudo/posoperatorio grave (cada 1–2 h si es necesario)', 'poblacion': 'pediatrico', 'unidad': 'mcg/kg', 'min': 1, 'max': 2, 'fuente': PED('fentanilo', 'Manejo del dolor agudo: 1–2 µg/kg/dosis')},
            {'indicacion': 'Dolor agudo: infusión IV', 'poblacion': 'pediatrico', 'unidad': 'mcg/kg/h', 'min': 0.5, 'max': 3, 'fuente': PED('fentanilo', 'Infusión IV: 0,5–3 µg/kg/h')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'ambienteH': 24, 'fuente': C('fentanilo', '6.3: diluido, estable 24 h a 25 °C')},
        'compatibilidad': compatibilidad(stab, 'fentanilo'),
        'interaccionesGraves': [
            {'con': 'Benzodiacepinas, barbitúricos y otros depresores del SNC', 'efecto': 'Depresión respiratoria, sedación profunda, coma', 'fuente': C('fentanilo', '4.5')},
            {'con': 'Fármacos serotoninérgicos (ISRS, IRSN, IMAO)', 'efecto': 'Síndrome serotoninérgico', 'fuente': C('fentanilo', '4.5')},
            {'con': 'Inhibidores potentes del CYP3A4', 'efecto': 'Aumentan el efecto y la depresión respiratoria', 'fuente': C('fentanilo', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': [], 'graves': ['Depresión respiratoria', 'Hipotensión', 'Bradicardia', 'Rigidez muscular'], 'vigilar': ['Frecuencia respiratoria y SatO2', 'Presión arterial y frecuencia cardíaca'], 'fuente': P('Anexo 6, Fentanilo: RAM')},
        'alertas': ['Medicamento de alto riesgo.', 'Antagonista: naloxona.', 'Cuidado con mcg y mg: 0,1 mg = 100 mcg.'],
        'meta': meta([{'campo': 'dosis adulto en urgencia', 'valores': ['CIMA solo informa dosis en anestesia', 'Urgencia UC (2015): 2–3 µg/kg como premedicación en secuencia rápida de intubación'], 'decision': 'Revisión clínica (Héctor Salvo Agüero, TENS, 2026-10-01): usar protocolos de Medicina de Urgencia UC o U. de Chile. Se agrega la dosis de intubación de Urgencia UC; la dosis de analgesia en adultos se toma, por decisión de Héctor, de una fuente extranjera (Hospital Universitario San Pedro, España, 2024: 0,5–1 mcg/kg) hasta obtener la serie «Sedación y analgesia en la unidad de emergencia» (Urgencia UC, 2013), que no está disponible en línea.'}]),
    }

    F['morfina'] = {
        'id': 'morfina', 'nombre': 'Morfina', 'comerciales': [], 'grupo': 'analgesico-opioide',
        'ambitos': ['samu', 'urgencia', 'upc', 'hospitalizacion'], 'altoRiesgo': True,
        'presentaciones': [{'id': 'amp-10mg-1ml', 'forma': 'ampolla', 'cantidad': {'valor': 10, 'unidad': 'mg'}, 'volumenMl': 1, 'fuente': P('Anexo 6, Morfina: 10 mg/ml')}],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SF', 'Agua estéril'],
            'concentracionMin': {'valor': 0.5, 'unidad': 'mg', 'fuente': P('Anexo 6, Morfina: 0,5–5 mg/ml')},
            'concentracionMax': {'valor': 5, 'unidad': 'mg', 'fuente': P('Anexo 6, Morfina: 0,5–5 mg/ml')},
            'estandar': [
                {'descripcion': '50 mg en 100 ml (0,5 mg/ml)', 'cantidad': {'valor': 50, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Morfina: habitual 50 mg/100 ml')},
                {'descripcion': '125 mg en 250 ml (0,5 mg/ml)', 'cantidad': {'valor': 125, 'unidad': 'mg'}, 'volumenFinalMl': 250, 'fuente': P('Anexo 6, Morfina: 125 mg/250 ml')},
            ],
        },
        'administracion': {'vias': ['bolo', 'infusion_continua'], 'texto': 'Inyección IV lenta. Diluir con agua estéril o SF.', 'fuente': C('morfina', '4.2 y 6.6')},
        'dosis': [
            {'indicacion': 'Dolor agudo: inyección IV lenta', 'poblacion': 'adulto', 'unidad': 'mg', 'min': 2, 'max': 15, 'fuente': C('morfina', '4.2 Administración intravenosa')},
            {'indicacion': 'Dolor agudo: perfusión tras la dosis inicial', 'poblacion': 'adulto', 'unidad': 'mg/h', 'min': 2.5, 'max': 5, 'fuente': C('morfina', '4.2 Administración intravenosa')},
            {'indicacion': 'IV lenta (máx. 15 mg/24 h)', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'min': 0.05, 'max': 0.1, 'fuente': PED('morfina', 'Vía intravenosa lenta: 0,05–0,1 mg/kg, máx. 15 mg/24 h')},
            {'indicacion': 'Analgesia posoperatoria: infusión', 'poblacion': 'pediatrico', 'unidad': 'mg/kg/h', 'min': 0.01, 'max': 0.04, 'fuente': PED('morfina', 'En analgesia posoperatoria 0,01–0,04 mg/kg/h')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('morfina', '6.3: usar inmediatamente tras abrir la ampolla')},
        'compatibilidad': compatibilidad(stab, 'morfina'),
        'interaccionesGraves': [
            {'con': 'Benzodiacepinas y otros sedantes', 'efecto': 'Sedación profunda, depresión respiratoria, coma', 'fuente': C('morfina', '4.5')},
            {'con': 'Alcohol', 'efecto': 'Potenciación de la depresión del SNC', 'fuente': C('morfina', '4.5')},
            {'con': 'IMAO', 'efecto': 'Usar con precaución y en dosis reducida', 'fuente': C('morfina', '4.5')},
        ],
        'efectosAdversos': {'frecuentes': ['Constipación', 'Retención urinaria', 'Somnolencia', 'Náuseas y vómitos', 'Sudoración'], 'graves': ['Depresión del SNC y respiratoria', 'Hipotensión'], 'vigilar': ['Frecuencia respiratoria y SatO2', 'Nivel de sedación', 'Presión arterial'], 'fuente': P('Anexo 6, Morfina: RAM e intoxicación')},
        'alertas': ['Medicamento de alto riesgo.', 'Antagonista: naloxona.'],
        'meta': meta([{'campo': 'compatibilidad con sulfato de magnesio', 'valores': ['Stabilis: sin datos', 'CIMA morfina 6.2: incompatible con sales de magnesio'], 'decision': 'Se registra incompatible (criterio conservador).'}]),
    }
    ajustar(F['morfina']['compatibilidad'], 'sulfato-de-magnesio', 'incompatible', C('morfina', '6.2: incompatible con sales de magnesio'))

    F['ketamina'] = {
        'id': 'ketamina', 'nombre': 'Ketamina', 'comerciales': [], 'grupo': 'anestesico',
        'ambitos': ['samu', 'urgencia', 'upc'], 'altoRiesgo': True,
        'presentaciones': [{'id': 'fa-500mg-10ml', 'forma': 'frasco ampolla', 'cantidad': {'valor': 500, 'unidad': 'mg'}, 'volumenMl': 10, 'fuente': P('Anexo 6, Ketamina: 500 mg/10 ml')}],
        'reconstitucion': None,
        'dilucion': {
            'sueros': ['SF', 'SG5'],
            'concentracionMax': {'valor': 50, 'unidad': 'mg', 'fuente': P('Anexo 6, Ketamina: 50 mg/ml máxima concentración para bolo')},
            'estandar': [
                {'descripcion': '500 mg en 500 ml (1 mg/ml)', 'cantidad': {'valor': 500, 'unidad': 'mg'}, 'volumenFinalMl': 500, 'fuente': C('ketamina', '6.6 Dilución: 10 ml en 500 ml')},
                {'descripcion': '500 mg en 250 ml (2 mg/ml), restricción de volumen', 'cantidad': {'valor': 500, 'unidad': 'mg'}, 'volumenFinalMl': 250, 'fuente': C('ketamina', '6.6: 250 ml, 2 mg/ml')},
                {'descripcion': '400 mg en 100 ml (4 mg/ml)', 'cantidad': {'valor': 400, 'unidad': 'mg'}, 'volumenFinalMl': 100, 'fuente': P('Anexo 6, Ketamina: habitual 400 mg/100 ml')},
            ],
        },
        'administracion': {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV lento, en al menos 60 s (más rápido puede causar depresión respiratoria). No mezclar en la misma jeringa con barbitúricos ni diazepam.', 'tiempoMinimoMin': 1, 'fuente': C('ketamina', '4.2 y 6.2')},
        'dosis': [
            {'indicacion': 'Inducción de anestesia general (media 2 mg/kg)', 'poblacion': 'adulto', 'unidad': 'mg/kg', 'min': 1, 'max': 4.5, 'fuente': C('ketamina', '4.2 Vía intravenosa')},
            {'indicacion': 'Inducción de anestesia (bolo)', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'min': 1, 'max': 2, 'fuente': PED('ketamina', 'Inducción: bolo 1–2 mg/kg IV')},
            {'indicacion': 'Sedación: infusión', 'poblacion': 'pediatrico', 'unidad': 'mcg/kg/min', 'min': 5, 'max': 20, 'fuente': PED('ketamina', 'Sedación: 5–20 µg/kg/min IV')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'fuente': C('ketamina', '6.3: tras la dilución, usar inmediatamente')},
        'compatibilidad': compatibilidad(stab, 'ketamina'),
        'interaccionesGraves': [
            {'con': 'Teofilina o aminofilina', 'efecto': 'Disminución del umbral convulsivo', 'fuente': C('ketamina', '4.5')},
            {'con': 'Hormonas tiroideas (terapia de reemplazo)', 'efecto': 'Riesgo aumentado de hipertensión y taquicardia', 'fuente': C('ketamina', '4.4')},
        ],
        'efectosAdversos': {'frecuentes': ['Hipertensión', 'Taquicardia'], 'graves': ['Hipotensión', 'Bradicardia', 'Aumento de la presión intracraneana'], 'vigilar': ['Presión arterial y frecuencia cardíaca', 'Vía aérea y respiración'], 'fuente': P('Anexo 6, Ketamina: RAM')},
        'alertas': ['Medicamento de alto riesgo.', 'Incompatible en Y con Ringer lactato.'],
        'meta': meta([{'campo': 'estabilidad de la dilución', 'valores': ['CIMA 6.3: usar inmediatamente', 'CIMA 6.6: la solución 1 mg/ml es estable 24 h'], 'decision': 'Se registra «usar inmediatamente» (criterio conservador).'}]),
    }

    F['sulfato-de-magnesio'] = {
        'id': 'sulfato-de-magnesio', 'nombre': 'Sulfato de magnesio', 'comerciales': [], 'grupo': 'electrolito',
        'ambitos': ['samu', 'urgencia', 'upc', 'hospitalizacion'], 'altoRiesgo': False,
        'presentaciones': [{'id': 'amp-25pct-5ml', 'forma': 'ampolla 25 %', 'cantidad': {'valor': 1.25, 'unidad': 'g'}, 'volumenMl': 5, 'fuente': P('Anexo 6, Sulfato de magnesio 25 %: 5 ml = 1,25 g')}],
        'reconstitucion': None,
        'dilucion': {'sueros': ['SF', 'SG5'], 'estandar': [{'descripcion': '4 g en 250 ml', 'cantidad': {'valor': 4, 'unidad': 'g'}, 'volumenFinalMl': 250, 'fuente': C('sulfato-de-magnesio', '6.6 Perfusión IV: 4–5 g en 250 ml')}]},
        'administracion': {'vias': ['bolo', 'infusion_intermitente', 'infusion_continua'], 'texto': 'Diluir en 100 a 500 ml de suero. La perfusión debe mantenerse en general bajo 2 g/h, salvo torsade de pointes o eclampsia. La administración rápida puede causar hipotensión y asistolia.', 'fuente': C('sulfato-de-magnesio', '4.2')},
        'dosis': [
            {'indicacion': 'Torsade de pointes: 2 g en 1–2 min (repetible, total 6 g)', 'poblacion': 'adulto', 'unidad': 'g', 'min': 2, 'max': 2, 'maximaAbsoluta': 6, 'fuente': C('sulfato-de-magnesio', '4.2')},
            {'indicacion': 'Eclampsia: carga en 5–10 min', 'poblacion': 'adulto', 'unidad': 'g', 'min': 4, 'max': 4, 'fuente': C('sulfato-de-magnesio', '4.2')},
            {'indicacion': 'Eclampsia: perfusión continua', 'poblacion': 'adulto', 'unidad': 'g/h', 'min': 1, 'max': 4, 'fuente': C('sulfato-de-magnesio', '4.2')},
            {'indicacion': 'Torsade de pointes (bolo lento sin pulso; 10–20 min con pulso)', 'poblacion': 'pediatrico', 'unidad': 'mg/kg', 'min': 25, 'max': 50, 'topeAdulto': {'valor': 2, 'unidad': 'g'}, 'fuente': C('sulfato-de-magnesio', '4.2 Población pediátrica: máx. 2 g')},
        ],
        'sinDosisPediatrica': False,
        'estabilidad': {'ambienteH': 24, 'refrigeradoH': 24, 'fuente': C('sulfato-de-magnesio', '6.3: diluido al 2 %, 24 h a 20–25 °C y a 2–8 °C')},
        'compatibilidad': compatibilidad(stab, 'magnesio'),
        'interaccionesGraves': [
            {'con': 'Bloqueantes neuromusculares (suxametonio, vecuronio)', 'efecto': 'Potencia y prolonga el bloqueo; riesgo de depresión respiratoria', 'fuente': C('sulfato-de-magnesio', '4.5')},
            {'con': 'Sales de calcio', 'efecto': 'Efecto antagonista; no administrar juntas', 'fuente': C('sulfato-de-magnesio', '4.4 y 4.5')},
        ],
        'efectosAdversos': {'frecuentes': ['Rubor', 'Somnolencia', 'Diarrea'], 'graves': ['Hipotensión y asistolia con administración rápida', 'Depresión del SNC'], 'vigilar': ['Presión arterial', 'Reflejos osteotendíneos y frecuencia respiratoria', 'ECG en dosis altas'], 'fuente': P('Anexo 6, Sulfato de magnesio: RAM')},
        'alertas': ['La ampolla chilena es al 25 % (250 mg/ml); otras presentaciones son al 15 % o al 50 %.', 'Incompatible en Y con noradrenalina.'],
        'meta': meta(),
    }
    ajustar(F['sulfato-de-magnesio']['compatibilidad'], 'morfina', 'incompatible', C('morfina', '6.2: incompatible con sales de magnesio'))
    return F




def fuentes():
    return FUENTES
