"""Tanda 3: hospitalarios (22). Valores citados; compatibilidad en Y la llena la matriz global."""
from .comun import C, P, PED, fu, fuente_cima, fuente_pediamecum
from .tanda1b import ALTO, conc, dil, dosis, ea, ficha, ix, pres

HOSP = ['upc', 'hospitalizacion']
URG_H = ['urgencia', 'upc', 'hospitalizacion']
FDA = lambda k, d: fu(f'FDA-{k}', d)  # noqa: E731

CIMA = {
    'omeprazol': ('67270', 'Omeprazol Normon 40 mg polvo para solución para perfusión'),
    'paracetamol': ('75594', 'Paracetamol B. Braun 10 mg/ml solución para perfusión'),
    'ketoprofeno': ('55857', 'Orudis 100 mg solución inyectable (ketoprofeno)'),
    'dexmedetomidina': ('84372', 'Dexmedetomidina Altan 100 microgramos/ml concentrado para solución para perfusión'),
    'remifentanilo': ('79906', 'Remifentanilo Noridem 1 mg polvo para concentrado para solución inyectable y para perfusión'),
    'cisatracurio': ('76000', 'Cisatracurio Normon 2 mg/ml solución inyectable y para perfusión'),
    'haloperidol': ('58345', 'Haloperidol Esteve 5 mg/ml solución inyectable'),
    'digoxina': ('34753', 'Digoxina Kern Pharma 0,25 mg/ml solución inyectable'),
    'manitol': ('43560', 'Osmofundina concentrada 20 % solución para perfusión (manitol)'),
    'fitomenadiona': ('27262', 'Konakion 10 mg/ml solución oral/solución inyectable (fitomenadiona)'),
    'tiamina': ('17464', 'Benerva 100 mg/ml solución inyectable (tiamina)'),
    'octreotido': ('69524', 'Octreotida GP-Pharm 0,1 mg/ml solución inyectable y para perfusión'),
    'fosfato-de-potasio': ('63546', 'Fosfato dipotásico 1M Fresenius Kabi 174,2 mg/ml solución inyectable'),
    'acetilcisteina': ('58931', 'Hidonac antídoto 200 mg/ml concentrado para solución para perfusión (acetilcisteína)'),
    'neostigmina': ('36384', 'Neostigmina Braun 0,5 mg/ml solución inyectable'),
    'esmolol': ('72349', 'Brevibloc 10 mg/ml solución inyectable (esmolol)'),
    'nimodipino': ('67042', 'Nimodipino Altan 0,2 mg/ml solución para perfusión'),
    'metoprolol': ('56989', 'Beloken 1 mg/ml solución inyectable (metoprolol)'),
}
PEDIAMECUM = {'dexmedetomidina': 'Dexmedetomidina', 'cisatracurio': 'Cisatracurio', 'vecuronio': 'Vecuronio',
              'manitol': 'Manitol', 'tiamina': 'Tiamina', 'esmolol': 'Esmolol'}

FUENTES_EXTRA = [
    {
        'id': 'FDA-VECURONIO',
        'titulo': 'Vecuronium bromide for injection — Prescribing information (Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=582c7f44-b614-18df-e063-6294a90a74b6',
        'anio': 2026,
        'consultado': '2026-10-01',
    },
    {
        'id': 'FDA-ENALAPRILATO',
        'titulo': 'Enalaprilat injection 1,25 mg/ml — Prescribing information (Dosage and administration)',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=5d398da1-020c-ccb1-a775-ce8e0b29d621',
        'anio': 2024,
        'consultado': '2026-10-01',
    },
    {
        'id': 'FDA-NACL-3',
        'titulo': '3 % Sodium chloride injection (hipertónica) — Prescribing information',
        'institucion': 'U.S. FDA / DailyMed',
        'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=a8058593-48af-457a-b0f0-166935c7d10c',
        'anio': 2021,
        'consultado': '2026-10-01',
    },
]


def fuentes():
    lista = [fuente_cima(k, nreg, nombre) for k, (nreg, nombre) in CIMA.items()]
    lista += [fuente_pediamecum(k, n) for k, n in PEDIAMECUM.items()]
    return lista + FUENTES_EXTRA


def fichas(stab=None):
    F = {}

    F['omeprazol'] = ficha(
        'omeprazol', 'Omeprazol', 'protector-gastrico', URG_H, False,
        [pres('fa-40mg', 'frasco ampolla (polvo)', 40, 'mg', 10, P('Anexo 6, Omeprazol: 40 mg FA; reconstitución 10 ml de suero por 40 mg (4 mg/ml)'))],
        {'sueros': ['SF', 'SG5'], 'estandar': [dil('40 mg en 100 ml', 40, 'mg', 100, C('omeprazol', '6.6: disolver y diluir hasta 100 ml de SF o SG5 %'))]},
        {'vias': ['infusion_intermitente'], 'texto': 'Perfusión IV de 20 a 30 minutos. Diluir solo en SF o SG5 % hasta 100 ml (el pH afecta su estabilidad). No administrar otros medicamentos por la misma vía; lavar al terminar.', 'tiempoMinimoMin': 20, 'fuente': C('omeprazol', '4.2.2; 6.6')},
        [dosis('Alternativa a la vía oral, una vez al día', 'adulto', 'mg', C('omeprazol', '4.2.1: 40 mg una vez al día'), mn=40, mx=40)],
        {'fuente': C('omeprazol', '6.3 (usar la solución preparada según 6.6)')},
        [ix('Clopidogrel', 'Posible reducción de su efecto; desaconsejado', C('omeprazol', '4.4'))],
        ea(['Cefalea', 'Dolor abdominal', 'Diarrea'], ['Hipomagnesemia (uso prolongado)', 'Reacciones de hipersensibilidad'], [], C('omeprazol', '4.8')),
        [], reconstitucion={'diluyente': 'Suero fisiológico', 'volumenMl': 10, 'fuente': P('Anexo 6, Omeprazol: 10 ml de suero por 40 mg')},
        discrepancias=[{'campo': 'dilución', 'valores': ['Pucón: «dilución 0,04 mg/ml» y «40 mg/100 ml» (0,4 mg/ml)', 'CIMA: 40 mg en 100 ml'], 'decision': 'Se registra 40 mg en 100 ml; el «0,04 mg/ml» de Pucón parece un error de tipeo.'},
                       {'campo': 'dosis pediátrica', 'valores': ['CIMA: sin datos IV en niños'], 'decision': 'Sin dosis pediátrica.'}],
    )

    F['paracetamol'] = ficha(
        'paracetamol', 'Paracetamol', 'analgesico-no-opioide', URG_H, False,
        [pres('fco-1g-100ml', 'frasco 10 mg/ml', 1, 'g', 100, P('Anexo 6, Paracetamol: 10 mg/ml'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['infusion_intermitente'], 'texto': 'No requiere dilución. Infusión de 15 minutos (Pucón: 15 a 30 min). El volumen y el frasco dependen del peso: no superar la dosis calculada.', 'tiempoMinimoMin': 15, 'fuente': P('Anexo 6, Paracetamol: no requiere dilución; administrar en 15–30 minutos')},
        [dosis('> 50 kg: cada 6 h (máx. 4 g/día)', 'adulto', 'g', C('paracetamol', '4.2.1: 1 g por administración'), mn=1, mx=1, maxima=4),
         dosis('33–50 kg: cada 6 h (máx. 60 mg/kg/día, sin exceder 3 g)', 'adulto', 'mg/kg', C('paracetamol', '4.2.1: 15 mg/kg'), mn=15, mx=15),
         dosis('Niños > 10 kg hasta 33 kg: cada 6 h (máx. 60 mg/kg/día, sin exceder 2 g)', 'pediatrico', 'mg/kg', C('paracetamol', '4.2.1: 15 mg/kg'), mn=15, mx=15, tope=(1, 'g')),
         dosis('Lactantes ≤ 10 kg: cada 6 h (máx. 30 mg/kg/día)', 'pediatrico', 'mg/kg', C('paracetamol', '4.2.1: 7,5 mg/kg'), mn=7.5, mx=7.5, tope=(1, 'g'))],
        {'fuente': C('paracetamol', '6.3 (usar tras abrir)')},
        [ix('Probenecid', 'Reduce casi a la mitad el aclaramiento de paracetamol', C('paracetamol', '4.5'))],
        ea([], ['Hepatotoxicidad por sobredosis', 'Hipotensión'], ['Dosis acumulada diaria', 'Función hepática'], P('Anexo 6, Paracetamol: RAM')),
        ['Riesgo de sobredosis por error de volumen en niños: calcular por peso.', 'Antídoto: acetilcisteína.'],
    )

    F['ketoprofeno'] = ficha(
        'ketoprofeno', 'Ketoprofeno', 'analgesico-no-opioide', URG_H, False,
        [pres('fa-100mg', 'frasco ampolla', 100, 'mg', 2, C('ketoprofeno', 'Orudis 100 mg (ampolla de 2 ml; Pucón: ketoprofeno 100 mg FA)'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMin': conc(1, 'mg', P('Anexo 6, Ketoprofeno: 1 a 2 mg/ml')), 'concentracionMax': conc(2, 'mg', P('Anexo 6, Ketoprofeno: 1 a 2 mg/ml')),
         'estandar': [dil('100 mg en 100 ml (1 mg/ml)', 100, 'mg', 100, P('Anexo 6, Ketoprofeno: habitual 100 mg/100 ml')),
                      dil('300 mg en 250 ml (1,2 mg/ml), infusión continua', 300, 'mg', 250, P('Anexo 6, Ketoprofeno: 300 mg/250 ml'))]},
        {'vias': ['infusion_intermitente', 'infusion_continua'], 'texto': 'Solo en infusión diluida: en bolo es muy venoirritante (flebitis y dolor).', 'fuente': P('Anexo 6, Ketoprofeno: la administración directa en bolo puede provocar flebitis')},
        [dosis('Dosis diaria (en 2 dosis, intervalo mínimo 6 h)', 'adulto', 'mg/24 h', C('ketoprofeno', '4.2: 100–200 mg al día; máx. 200 mg/día'), mn=100, mx=200)],
        {'fuente': P('Anexo 6, Ketoprofeno (no informa estabilidad)')},
        [ix('Otros AINE y salicilatos en dosis altas', 'Mayor riesgo de úlcera y hemorragia digestiva', C('ketoprofeno', '4.5'))],
        ea(['Náuseas', 'Irritación gastrointestinal', 'Cefalea'], ['Hemorragia digestiva (melena, hematemesis)', 'Hematuria'], ['Signos de sangrado', 'Función renal'], P('Anexo 6, Ketoprofeno: RAM')),
        ['En la ficha técnica española la ampolla de 100 mg es solo para uso intramuscular: verificar que la presentación local esté autorizada para vía EV.'],
        discrepancias=[{'campo': 'vía', 'valores': ['Pucón: infusión EV intermitente y continua', 'CIMA (Orudis): no debe administrarse por vía intravenosa'], 'decision': 'Se registra la preparación EV de Pucón con alerta; la dosis diaria se cita de CIMA. REVISAR PRIMERO.'},
                       {'campo': 'dosis pediátrica', 'valores': ['CIMA: no usar en menores de 3 años; sin dosis pediátrica'], 'decision': 'Sin dosis pediátrica.'}],
    )

    F['dexmedetomidina'] = ficha(
        'dexmedetomidina', 'Dexmedetomidina', 'sedante', HOSP, True,
        [pres('amp-200mcg-2ml', 'ampolla', 200, 'mcg', 2, C('dexmedetomidina', '2: 100 mcg/ml; ampolla de 2 ml = 200 mcg'))],
        {'sueros': ['SF', 'SG5'], 'estandar': [dil('200 mcg en 50 ml (4 mcg/ml)', 200, 'mcg', 50, C('dexmedetomidina', '6.6: concentración de 4 mcg/ml')),
                                                dil('400 mcg en 50 ml (8 mcg/ml)', 400, 'mcg', 50, C('dexmedetomidina', '6.6: concentración de 8 mcg/ml'))]},
        {'vias': ['infusion_continua'], 'texto': 'Perfusión continua por bomba, diluida a 4 u 8 mcg/ml. No se recomienda dosis de carga en UCI. Tras cada ajuste, el nuevo equilibrio tarda 1 hora.', 'requiereBomba': True, 'fuente': C('dexmedetomidina', '4.2; 6.6')},
        [dosis('Sedación en UCI (inicio 0,7; máx. 1,4 mcg/kg/h)', 'adulto', 'mcg/kg/h', C('dexmedetomidina', '4.2: 0,2–1,4 mcg/kg/h'), mn=0.2, mx=1.4),
         dosis('Mantención (niños; datos limitados)', 'pediatrico', 'mcg/kg/h', PED('dexmedetomidina', '0,2–0,7 mcg/kg/h; descrito hasta 1'), mn=0.2, mx=0.7)],
        {'ambienteH': 24, 'fuente': C('dexmedetomidina', '6.3: diluida, estabilidad en uso de 24 h a 25 °C; microbiológicamente usar de inmediato')},
        [ix('Anestésicos, sedantes, hipnóticos y opioides', 'Aumento de efectos sedantes, anestésicos y cardiorrespiratorios', C('dexmedetomidina', '4.5'))],
        ea(['Hipotensión', 'Bradicardia', 'Hipertensión'], ['Bradicardia grave y paro sinusal'], ['FC y PA continuas'], C('dexmedetomidina', '4.8')),
        [ALTO],
    )

    F['remifentanilo'] = ficha(
        'remifentanilo', 'Remifentanilo', 'analgesico-opioide', HOSP, True,
        [pres('fa-1mg', 'frasco ampolla (polvo)', 1, 'mg', 1, C('remifentanilo', '2: tras reconstituir, 1 mg/ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMin': conc(20, 'mcg', C('remifentanilo', '4.2: diluir a 20–250 mcg/ml')), 'concentracionMax': conc(250, 'mcg', C('remifentanilo', '4.2: diluir a 20–250 mcg/ml')),
         'estandar': [dil('1 mg en 20 ml (50 mcg/ml, recomendada en adultos)', 1, 'mg', 20, C('remifentanilo', '4.2: 50 mcg/ml es la dilución recomendada para adultos'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Solo IV, con bomba calibrada y vía conectada cerca de la cánula (mínimo espacio muerto). Bolo de no menos de 30 segundos. Purgar la vía al terminar. Solo con soporte ventilatorio disponible.', 'requiereBomba': True, 'fuente': C('remifentanilo', '4.2')},
        [dosis('Inducción anestésica (perfusión)', 'adulto', 'mcg/kg/min', C('remifentanilo', '4.2: 0,5–1 mcg/kg/min'), mn=0.5, mx=1),
         dosis('Bolo inicial opcional (≥ 30 s)', 'adulto', 'mcg/kg', C('remifentanilo', '4.2: 1 mcg/kg'), mn=1, mx=1),
         dosis('Mantención en paciente ventilado', 'adulto', 'mcg/kg/min', C('remifentanilo', '4.2: 0,05–2 mcg/kg/min'), mn=0.05, mx=2)],
        {'fuente': C('remifentanilo', '6.3 (no informa estabilidad de la dilución en este extracto)')},
        [ix('Benzodiazepinas y otros depresores del SNC', 'Depresión respiratoria aditiva', C('remifentanilo', '4.5'))],
        ea(['Náuseas', 'Hipotensión', 'Bradicardia'], ['Depresión respiratoria y apnea', 'Rigidez muscular'], ['Ventilación', 'FC y PA'], C('remifentanilo', '4.8')),
        [ALTO, 'Efecto muy corto: planificar la analgesia antes de suspender.'],
        reconstitucion={'diluyente': 'Agua para inyectables o suero', 'volumenMl': 1, 'fuente': C('remifentanilo', '2: cada ml reconstituido contiene 1 mg')},
        discrepancias=[{'campo': 'dosis pediátrica y presentación', 'valores': ['CIMA: vial de 1 mg; en Chile existen viales de 2 y 5 mg', 'Pediamécum: pauta pediátrica según ficha técnica (1–12 años)'], 'decision': 'Sin dosis pediátrica en esta versión; confirmar presentación local.'}],
    )

    F['cisatracurio'] = ficha(
        'cisatracurio', 'Cisatracurio', 'bloqueador-neuromuscular', HOSP, True,
        [pres('vial-10mg-5ml', 'vial', 10, 'mg', 5, C('cisatracurio', '2: 2 mg/ml; viales de 2,5 y 5 ml'))],
        {'sueros': ['SF', 'SG5'], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Bolo IV o perfusión por bomba. No mezclar en la misma jeringa ni por la misma aguja con propofol o soluciones alcalinas. Solo con vía aérea y ventilación aseguradas.', 'requiereBomba': True, 'fuente': C('cisatracurio', '4.2')},
        [dosis('Intubación traqueal', 'adulto', 'mg/kg', C('cisatracurio', '4.2: 0,15 mg/kg'), mn=0.15, mx=0.15),
         dosis('Mantención (bolos)', 'adulto', 'mg/kg', C('cisatracurio', '4.2: 0,03 mg/kg'), mn=0.03, mx=0.03),
         dosis('Perfusión (inicio 3 mcg/kg/min)', 'adulto', 'mcg/kg/min', C('cisatracurio', '4.2: 3 mcg/kg/min; intervalo 0,5–10,2'), mn=0.5, mx=10.2),
         dosis('Intubación (niños)', 'pediatrico', 'mg/kg', PED('cisatracurio', '0,15 mg/kg en 5–10 s'), mn=0.15, mx=0.15, tope=(10.5, 'mg'), estimado=True)],
        {'fuente': C('cisatracurio', '6.3 (sin conservante: uso en un solo paciente)')},
        [ix('Anestésicos inhalatorios (isoflurano, halotano)', 'Incrementan el bloqueo neuromuscular', C('cisatracurio', '4.5'))],
        ea([], ['Bloqueo prolongado', 'Bradicardia', 'Anafilaxia'], ['Ventilación', 'Tren de cuatro'], C('cisatracurio', '4.8')),
        [ALTO, 'Paraliza la respiración: solo con vía aérea y ventilación aseguradas.'],
        discrepancias=[{'campo': 'tope pediátrico', 'valores': ['Adulto 0,15 mg/kg × 70 kg = 10,5 mg'], 'decision': 'Tope fijado en 10,5 mg; confirmar.'}],
    )

    F['vecuronio'] = ficha(
        'vecuronio', 'Vecuronio', 'bloqueador-neuromuscular', HOSP, True,
        [pres('fa-10mg', 'frasco ampolla (polvo)', 10, 'mg', 10, FDA('VECURONIO', 'Vial de 10 mg'))],
        {'sueros': ['SF', 'SG5'], 'estandar': [dil('10 mg en 100 ml (0,1 mg/ml) para perfusión', 10, 'mg', 100, FDA('VECURONIO', 'Infusión: 0,1 mg/ml (10 mg en 100 ml)'))]},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Solo IV, por o bajo supervisión de clínicos expertos. Monitorizar la respuesta al estimulador de nervio periférico. Iniciar la infusión solo tras evidencia de recuperación espontánea del bolo.', 'requiereBomba': True, 'fuente': FDA('VECURONIO', 'Dosage and administration')},
        [dosis('Intubación (dosis inicial)', 'adulto', 'mg/kg', FDA('VECURONIO', '0,08–0,1 mg/kg en bolo'), mn=0.08, mx=0.1),
         dosis('Mantención (bolos)', 'adulto', 'mg/kg', FDA('VECURONIO', '0,01–0,015 mg/kg'), mn=0.01, mx=0.015),
         dosis('Perfusión continua', 'adulto', 'mcg/kg/min', FDA('VECURONIO', '1 mcg/kg/min'), mn=1, mx=1),
         dosis('Lactantes > 7 semanas–1 año (repetible cada hora)', 'pediatrico', 'mg/kg', PED('vecuronio', '0,1 mg/kg/dosis'), mn=0.1, mx=0.1, tope=(7, 'mg'), estimado=True)],
        {'refrigeradoH': 24, 'fuente': FDA('VECURONIO', 'Reconstituido con agua estéril: refrigerar y usar dentro de 24 h')},
        [ix('Anestésicos inhalatorios y succinilcolina previa', 'Potencian el bloqueo', FDA('VECURONIO', 'Dosage and administration'))],
        ea([], ['Bloqueo prolongado', 'Debilidad o parálisis persistente'], ['Ventilación', 'Tren de cuatro'], FDA('VECURONIO', 'Adverse reactions')),
        [ALTO, 'Paraliza la respiración: solo con vía aérea y ventilación aseguradas.'],
        reconstitucion={'diluyente': 'Agua para inyectables', 'volumenMl': 10, 'fuente': FDA('VECURONIO', 'Reconstituir con agua estéril (volumen no indicado en la etiqueta; se asumen 10 ml = 1 mg/ml)')},
        discrepancias=[{'campo': 'fuente y reconstitución', 'valores': ['No hay vecuronio en CIMA ni en Pucón', 'FDA no indica el volumen de reconstitución en el extracto revisado'], 'decision': 'Fuente FDA; se asumen 10 ml (1 mg/ml), práctica habitual: confirmar. Tope pediátrico 7 mg (0,1 mg/kg × 70 kg).'}],
    )

    F['haloperidol'] = ficha(
        'haloperidol', 'Haloperidol', 'antipsicotico', URG_H, False,
        [pres('amp-5mg-1ml', 'ampolla', 5, 'mg', 1, P('Anexo 6, Haloperidol: 5 mg/ml'))],
        {'sueros': ['SG5'], 'concentracionMin': conc(1, 'mg', P('Anexo 6, Haloperidol: 1 a 5 mg/ml')), 'concentracionMax': conc(5, 'mg', P('Anexo 6, Haloperidol: 1 a 5 mg/ml')), 'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'Pucón permite EV directa e infusión; la ficha técnica española la autoriza solo IM. Por vía EV vigilar ECG (QT).', 'fuente': P('Anexo 6, Haloperidol: EV directa, infusión intermitente y continua')},
        [dosis('Síndrome confusional agudo (repetible cada 2–4 h)', 'adulto', 'mg', C('haloperidol', '4.2.1: 1–10 mg (vía IM en la ficha)'), mn=1, mx=10),
         dosis('Agitación psicomotora grave (repetible cada hora; máx. 20 mg/día)', 'adulto', 'mg', C('haloperidol', '4.2.1: 5 mg (vía IM en la ficha)'), mn=5, mx=5, maxima=20)],
        {'fuente': P('Anexo 6, Haloperidol (no informa estabilidad)')},
        [ix('Fármacos que prolongan el QT (antiarrítmicos IA y III, otros)', 'Contraindicado: riesgo de arritmia', C('haloperidol', '4.5'))],
        ea(['Sedación', 'Reacciones extrapiramidales (distonía)'], ['Prolongación del QT y torsade de pointes', 'Síndrome neuroléptico maligno', 'Hipotensión'], ['ECG', 'Movimientos anormales'], P('Anexo 6, Haloperidol: RAM')),
        ['Uso EV fuera de ficha técnica en España: requiere monitorización ECG.'],
        discrepancias=[{'campo': 'vía', 'valores': ['Pucón: EV directa, intermitente y continua', 'CIMA: solo intramuscular'], 'decision': 'Se registra la preparación EV de Pucón con alerta; dosis de CIMA (IM). REVISAR PRIMERO.'}],
    )

    F['digoxina'] = ficha(
        'digoxina', 'Digoxina', 'antiarritmico', URG_H, True,
        [pres('amp-0.5mg-2ml', 'ampolla', 0.5, 'mg', 2, C('digoxina', '2: ampolla de 2 ml con 0,5 mg (0,25 mg/ml)'))],
        {'sueros': ['SF', 'SG5'], 'estandar': [dil('0,5 mg en 500 ml', 0.5, 'mg', 500, C('digoxina', 'Dilución: ampolla de 2 ml (500 mcg) en 500 ml; estable 48 h'))]},
        {'vias': ['infusion_intermitente'], 'texto': 'Cada dosis en infusión IV de 10 a 20 minutos. La carga se divide: la mitad primero y el resto cada 4–8 h según respuesta. Reducir la dosis al menos 33 % al pasar de oral a IV.', 'tiempoMinimoMin': 10, 'fuente': C('digoxina', '4.2')},
        [dosis('Dosis de carga IV total (dividida)', 'adulto', 'mg', C('digoxina', '4.2: 0,5–1 mg según edad, peso y función renal'), mn=0.5, mx=1),
         dosis('Carga IV en 24 h, niños 2–5 años (dividida)', 'pediatrico', 'mcg/kg/24 h', C('digoxina', '4.2: 35 mcg/kg en 24 h'), mx=35),
         dosis('Carga IV en 24 h, niños 5–10 años (dividida)', 'pediatrico', 'mcg/kg/24 h', C('digoxina', '4.2: 25 mcg/kg en 24 h'), mx=25)],
        {'ambienteH': 48, 'fuente': C('digoxina', 'Dilución: estable hasta 48 h a temperatura ambiente')},
        [ix('Amiodarona y otros (quinidina, propafenona, espironolactona)', 'Aumentan la digoxinemia: toxicidad', C('digoxina', '4.5')),
         ix('Calcio IV', 'Arritmias sinérgicas', fu('FDA-GLUCONATO-CALCIO', '7.1'))],
        ea(['Náuseas', 'Anorexia'], ['Arritmias por toxicidad digitálica', 'Bloqueo AV', 'Alteraciones visuales'], ['FC y ECG', 'Potasio', 'Digoxinemia', 'Función renal'], C('digoxina', '4.8')),
        [ALTO, 'La hipokalemia aumenta la toxicidad.'],
    )

    F['manitol'] = ficha(
        'manitol', 'Manitol 20 %', 'diuretico', URG_H, False,
        [pres('fco-20pct-250ml', 'frasco 20 % (250 ml)', 50, 'g', 250, C('manitol', '2: 200 mg/ml'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['infusion_intermitente'], 'texto': 'Hipertensión intracraneal: infundir en 30–60 minutos. Usar sistema de perfusión con filtro (puede cristalizar). Vigilar diuresis y osmolaridad.', 'tiempoMinimoMin': 30, 'fuente': C('manitol', '4.2')},
        [dosis('Hipertensión intracraneal (en 30–60 min)', 'adulto', 'g/kg', C('manitol', '4.2: 1,5–2 g/kg'), mn=1.5, mx=2),
         dosis('Test de infusión en oliguria (bolo)', 'adulto', 'g/kg', C('manitol', '4.2: 0,2 g/kg'), mn=0.2, mx=0.2),
         dosis('Hipertensión intracraneal (niños), en 20–30 min', 'pediatrico', 'g/kg', PED('manitol', '0,5–1 g/kg (máx. 1,5 g/kg/día)'), mn=0.5, mx=1, tope=(100, 'g'), estimado=True)],
        {'fuente': C('manitol', '6.3 (no informa estabilidad tras abrir)')},
        [ix('Glucósidos cardíacos', 'Alteración de la digoxinemia por cambios de potasio', C('manitol', '4.5')),
         ix('Diuréticos', 'Ajustar la dosis', C('manitol', '4.5'))],
        ea([], ['Sobrecarga de volumen y edema pulmonar', 'Alteraciones electrolíticas', 'Insuficiencia renal'], ['Diuresis', 'Electrolitos y osmolaridad'], C('manitol', '4.8')),
        ['Presentación del 20 %: puede cristalizar con frío.'],
        discrepancias=[{'campo': 'tope pediátrico y presentación', 'valores': ['Tope 100 g = 1,5 g/kg × 70 kg (aprox.)', 'Volumen de frasco de 250 ml no confirmado en la ficha (Osmofundina)'], 'decision': 'Confirmar presentación local (250 o 500 ml).'}],
    )

    F['fitomenadiona'] = ficha(
        'fitomenadiona', 'Fitomenadiona (vitamina K1)', 'hematologico', URG_H, False,
        [pres('amp-10mg-1ml', 'ampolla', 10, 'mg', 1, C('fitomenadiona', '2: ampolla de 10 mg en 1 ml (Pucón: 10 mg/ml)'))],
        {'sueros': ['SG5'], 'concentracionMin': conc(1, 'mg', P('Anexo 6, Fitomenadiona: 1–2 mg/ml')), 'concentracionMax': conc(2, 'mg', P('Anexo 6, Fitomenadiona: 1–2 mg/ml')), 'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'IV lenta (al menos 30 segundos). La vía IV se reserva para cuando otras vías no son posibles.', 'fuente': C('fitomenadiona', '4.2')},
        [dosis('Hemorragia grave con anticoagulante cumarínico (con PFC o CCP)', 'adulto', 'mg', C('fitomenadiona', '4.2: 5–10 mg IV lenta'), mn=5, mx=10),
         dosis('INR 5–9 sin hemorragia grave (warfarina)', 'adulto', 'mg', C('fitomenadiona', '4.2 tabla: 0,5–1 mg IV'), mn=0.5, mx=1)],
        {'fuente': C('fitomenadiona', '6.3 (no informa estabilidad de la dilución)')},
        [ix('Anticoagulantes cumarínicos (acenocumarol, warfarina)', 'Antagoniza su efecto', C('fitomenadiona', '4.5'))],
        ea(['Dolor en el sitio de inyección'], ['Reacciones anafilactoides con la vía IV', 'Hipotensión'], ['PA durante la administración'], P('Anexo 6, Fitomenadiona: RAM')),
        ['En neonatos y menores de 1 año usar la presentación pediátrica de 2 mg/0,2 ml.'],
    )

    F['tiamina'] = ficha(
        'tiamina', 'Tiamina (vitamina B1)', 'metabolico', URG_H, False,
        [pres('amp-100mg-1ml', 'ampolla', 100, 'mg', 1, C('tiamina', '2: ampolla de 1 ml con 100 mg'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente'], 'texto': 'IV lenta o perfusión corta. No mezclar con otros productos parenterales en la misma solución.', 'fuente': C('tiamina', '4.2 Forma de administración')},
        [dosis('Síndrome de Wernicke / urgencia (IV lenta, 3 días)', 'adulto', 'mg', C('tiamina', '4.2: 100 mg/día (200 mg si es necesario)'), mn=100, mx=200),
         dosis('Beriberi grave, niños hasta 2 años (dosis inicial IV)', 'pediatrico', 'mg', PED('tiamina', '25–50 mg iniciales IV'), mn=25, mx=50)],
        {'fuente': C('tiamina', '6.3 (no informa estabilidad)')},
        [ix('5-fluorouracilo, capecitabina, tegafur', 'Inhiben el efecto de la tiamina', C('tiamina', '4.5'))],
        ea([], ['Reacciones anafilácticas (vía IV)'], ['Signos de alergia'], C('tiamina', '4.8')),
        [],
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Protocolo Pucón 2022 no incluye tiamina'], 'decision': 'Ficha basada en CIMA y Pediamécum.'}],
    )

    F['octreotido'] = ficha(
        'octreotido', 'Octreótido', 'protector-gastrico', HOSP, False,
        [pres('amp-0.1mg-1ml', 'ampolla', 0.1, 'mg', 1, C('octreotido', '2: 0,1 mg/1 ml'))],
        {'sueros': ['SF'], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Para uso IV, diluir en suero fisiológico. En perfusión IV continua no superar 50 mcg/h.', 'requiereBomba': True, 'fuente': C('octreotido', '4.2; 4.4')},
        [dosis('Varices gastroesofágicas sangrantes: perfusión IV continua durante 5 días', 'adulto', 'mcg/h', C('octreotido', '4.2: 25 microgramos/hora durante 5 días; tolerado hasta 50 mcg/h'), mn=25, mx=25, maxima=50)],
        {'fuente': C('octreotido', '6.3 (no informa estabilidad de la dilución en este extracto)')},
        [ix('Betabloqueadores, antagonistas del calcio, fármacos del balance hidroelectrolítico', 'Puede requerir ajuste de sus dosis', C('octreotido', '4.5'))],
        ea(['Dolor abdominal', 'Náuseas', 'Diarrea'], ['Bradicardia', 'Colelitiasis', 'Hiper o hipoglicemia'], ['FC', 'Glicemia'], C('octreotido', '4.8; 4.4')),
        [],
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Pucón 2022 no incluye octreótido'], 'decision': 'Ficha basada en CIMA; confirmar protocolo local de hemorragia variceal.'}],
    )

    F['cloruro-de-sodio-10'] = ficha(
        'cloruro-de-sodio-10', 'Cloruro de sodio 10 %', 'electrolito', URG_H, True,
        [pres('amp-10pct-10ml', 'ampolla 10 % (1 g)', 17.1, 'mEq', 10, P('Anexo 6, Cloruro de sodio 10 %: ampolla 10 ml; 10 g/100 ml = 1.710 mEq/L de sodio'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo', 'infusion_intermitente', 'infusion_continua'], 'texto': 'EV directa solo en bolo por vía central. En infusión intermitente o continua, diluido según la necesidad y el objetivo terapéutico; infusión intermitente en 15 a 30 minutos.', 'requiereViaCentral': True, 'fuente': P('Anexo 6, Cloruro de sodio 10 %')},
        [],
        {'fuente': P('Anexo 6, Cloruro de sodio 10 % (no informa estabilidad)')},
        [],
        ea([], ['Hipernatremia', 'Sobrecarga de volumen', 'Mielinólisis osmótica por corrección rápida'], ['Balance de fluidos', 'Electrolitos (sodio seriado)', 'Estado ácido-base'], P('Anexo 6, Cloruro de sodio 10 %: evaluar balance, electrolitos y ácido-base')),
        [ALTO, 'Solución hipertónica: no confundir con suero fisiológico.', 'Las fuentes no indican dosis: seguir la indicación médica.'],
        discrepancias=[{'campo': 'dosis', 'valores': ['Pucón: «según necesidad y objetivo terapéutico», sin dosis'], 'decision': 'Ficha sin dosis.'}],
    )

    F['cloruro-de-sodio-3'] = ficha(
        'cloruro-de-sodio-3', 'Cloruro de sodio 3 % (hipertónico)', 'electrolito', ['urgencia', 'upc', 'hospitalizacion'], True,
        [pres('bolsa-3pct-500ml', 'bolsa 3 % (500 ml)', 256.5, 'mEq', 500, fu('FDA-NACL-3', '500 ml; 513 mEq/L de sodio (15 g de NaCl)'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['infusion_intermitente', 'infusion_continua'], 'texto': 'Dosis, velocidad y duración individualizadas según indicación, peso y controles de laboratorio. Usar inmediatamente tras abrir; descartar lo no usado.', 'requiereBomba': True, 'fuente': fu('FDA-NACL-3', 'Dosage and administration')},
        [],
        {'fuente': fu('FDA-NACL-3', 'Usar inmediatamente tras abrir el envase')},
        [],
        ea([], ['Hipernatremia', 'Mielinólisis osmótica por corrección rápida', 'Sobrecarga de volumen'], ['Sodio seriado', 'Estado neurológico', 'Balance hídrico'], fu('FDA-NACL-3', 'Description; Dosage and administration')),
        [ALTO, 'Las fuentes no indican dosis: seguir el protocolo de hiponatremia de la institución.'],
        discrepancias=[{'campo': 'fuente chilena y preparación', 'valores': ['No se encontró fuente chilena para NaCl 3 %', 'En Chile suele prepararse a partir de NaCl 10 %; no hay receta citable'], 'decision': 'Ficha con la presentación comercial de FDA; sin dosis ni receta de preparación.'}],
    )

    F['fosfato-de-potasio'] = ficha(
        'fosfato-de-potasio', 'Fosfato de potasio', 'electrolito', HOSP, True,
        [pres('amp-10mmol-10ml', 'ampolla 1 M (10 ml)', 10, 'mmol', 10, C('fosfato-de-potasio', '2: 1 mmol de fosfato y 2 mEq de K por ml; ampollas de 10 ml'))],
        {'sueros': ['SF', 'SG5'], 'concentracionMax': conc(0.02, 'mmol', P('Anexo 6, Cloruro de potasio: máximo periférico 40 mEq/L de K (0,02 mmol/ml de fosfato dipotásico = 40 mEq/L de K)')), 'estandar': []},
        {'vias': ['infusion_intermitente'], 'texto': 'Siempre diluido, en perfusión IV (p. ej., 0,08 mmol/kg en 6 h). Aporta potasio: 1 ml = 2 mEq de K. En cetoacidosis no superar 5 mEq/h.', 'requiereBomba': True, 'fuente': C('fosfato-de-potasio', '4.2; 6.6')},
        [dosis('Hipofosfatemia reciente no complicada (en 6 h)', 'adulto', 'mmol/kg', C('fosfato-de-potasio', '4.2.1: 0,08 mmol/kg; puede duplicarse'), mn=0.08, mx=0.16),
         dosis('Pauta alternativa según fósforo inicial', 'adulto', 'mmol/kg', C('fosfato-de-potasio', '4.2.1: 0,25 mmol/kg (P > 0,5 mg/dl) o 0,5 mmol/kg (P < 0,5)'), mn=0.25, mx=0.5),
         dosis('Niños: según requerimiento de potasio (2–3 mEq de K/kg/día)', 'pediatrico', 'mmol/kg/24 h', C('fosfato-de-potasio', '4.2.1: 2–3 mEq de K/kg/día; 1 ml = 1 mmol de fosfato = 2 mEq de K, es decir 1–1,5 mmol/kg/día'), mn=1, mx=1.5)],
        {'fuente': C('fosfato-de-potasio', '6.6: compatible 24 h a 22 °C con nutrición parenteral')},
        [ix('Digitálicos (con bloqueo cardíaco)', 'Riesgo de hiperkalemia; no recomendado', C('fosfato-de-potasio', '4.5'))],
        ea([], ['Hiperkalemia', 'Hipocalcemia', 'Arritmias con infusión rápida'], ['Fósforo, potasio y calcio', 'ECG'], C('fosfato-de-potasio', '4.8')),
        [ALTO, 'NUNCA en bolo. Contiene potasio (2 mEq/ml).'],
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Protocolo Pucón 2022 no incluye fosfato de potasio'], 'decision': 'Ficha basada en CIMA (fosfato dipotásico 1 M); confirmar la sal disponible en Chile.'},
                       {'campo': 'concentración máxima', 'valores': ['CIMA: diluir al menos 1:1 (hasta 1000 mEq/L de K)', 'Pucón (KCl): máximo periférico 40 mEq/L de K'], 'decision': 'Se aplica el límite de potasio periférico de Pucón (0,02 mmol/ml), el más conservador.'}],
    )

    F['acetilcisteina'] = ficha(
        'acetilcisteina', 'Acetilcisteína (antídoto)', 'antidoto', URG_H, False,
        [pres('vial-5g-25ml', 'vial 200 mg/ml', 5, 'g', 25, C('acetilcisteina', 'Hidonac antídoto 200 mg/ml'))],
        {'sueros': ['SG5', 'SF'], 'estandar': []},
        {'vias': ['infusion_intermitente'], 'texto': 'Tres perfusiones consecutivas sin descanso: 150 mg/kg en 200 ml en 1 h; 50 mg/kg en 500 ml en 4 h; 100 mg/kg en 1 L en 16 h. Preferir SG5 %. Iniciar idealmente dentro de 8 h de la ingesta de paracetamol.', 'requiereBomba': True, 'fuente': C('acetilcisteina', '4.2')},
        [dosis('Intoxicación por paracetamol: 1.ª perfusión (1 h)', 'adulto', 'mg/kg', C('acetilcisteina', '4.2: 150 mg/kg en 200 ml'), mn=150, mx=150),
         dosis('2.ª perfusión (4 h)', 'adulto', 'mg/kg', C('acetilcisteina', '4.2: 50 mg/kg en 500 ml'), mn=50, mx=50),
         dosis('3.ª perfusión (16 h)', 'adulto', 'mg/kg', C('acetilcisteina', '4.2: 100 mg/kg en 1 L'), mn=100, mx=100)],
        {'fuente': C('acetilcisteina', '6.3 (no informa estabilidad de la dilución en este extracto)')},
        [ix('Nitroglicerina', 'Hipotensión significativa y vasodilatación', C('acetilcisteina', '4.5'))],
        ea(['Náuseas', 'Vómitos', 'Rubor'], ['Reacciones anafilactoides (sobre todo en la 1.ª perfusión)', 'Broncoespasmo'], ['Signos de reacción durante la 1.ª hora'], C('acetilcisteina', '4.8; 4.4')),
        [],
        discrepancias=[{'campo': 'pediatría', 'valores': ['CIMA indica las mismas dosis por kg en niños con volúmenes menores (tabla por peso)'], 'decision': 'Sin dosis pediátrica separada en esta versión: usar la tabla por peso de la ficha técnica.'},
                       {'campo': 'fuente chilena', 'valores': ['Pucón 2022 no incluye acetilcisteína'], 'decision': 'Ficha basada en CIMA (Hidonac antídoto).'}],
    )

    F['neostigmina'] = ficha(
        'neostigmina', 'Neostigmina', 'antidoto', HOSP, False,
        [pres('amp-0.5mg-1ml', 'ampolla', 0.5, 'mg', 1, P('Anexo 6, Neostigmina: 0,5 mg/1 ml'))],
        {'sueros': ['SF'], 'estandar': []},
        {'vias': ['bolo'], 'texto': 'IV lenta, con atropina (0,6–1,2 mg) antes o al mismo tiempo en jeringa separada y disponible para bloquear efectos muscarínicos. No requiere dilución (si se diluye: 0,167 mg/ml).', 'fuente': C('neostigmina', '4.2')},
        [dosis('Reversión del bloqueo neuromuscular (repetir; total máx. 5 mg)', 'adulto', 'mg', C('neostigmina', '4.2: 0,5–2 mg IV lenta'), mn=0.5, mx=2, maxima=5)],
        {'fuente': C('neostigmina', '6.3 (no informa estabilidad)')},
        [ix('Aminoglucósidos, anestésicos inhalatorios, lidocaína IV', 'Antagonizan su efecto', C('neostigmina', '4.5'))],
        ea(['Náuseas', 'Hiperperistaltismo', 'Sialorrea'], ['Bradicardia', 'Bloqueo AV y asistolia'], ['FC y ECG'], P('Anexo 6, Neostigmina: RAM')),
        ['Tener atropina preparada.'],
    )

    F['esmolol'] = ficha(
        'esmolol', 'Esmolol', 'antiarritmico', HOSP, False,
        [pres('vial-100mg-10ml', 'vial 10 mg/ml', 100, 'mg', 10, C('esmolol', '2: vial de 10 ml con 100 mg'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo', 'infusion_continua'], 'texto': 'Solución lista para usar (10 mg/ml). Carga de 500 mcg/kg/min durante 1 minuto y luego mantención por bomba, ajustando según FC y PA.', 'requiereBomba': True, 'fuente': C('esmolol', '4.2')},
        [dosis('Taquiarritmia supraventricular: carga (1 min)', 'adulto', 'mcg/kg/min', C('esmolol', '4.2: 500 mcg/kg/min durante 1 minuto'), mn=500, mx=500),
         dosis('Mantención', 'adulto', 'mcg/kg/min', C('esmolol', '4.2: 50–200 mcg/kg/min'), mn=50, mx=200),
         dosis('TSV (niños): infusión tras carga de 100–500 mcg/kg', 'pediatrico', 'mcg/kg/min', PED('esmolol', 'Infusión 200 mcg/kg/min, ajustable; máx. 1000'), mn=200, mx=1000)],
        {'fuente': C('esmolol', '6.3 (no informa estabilidad en este extracto)')},
        [ix('Verapamilo IV', 'No administrar dentro de 48 h tras suspender verapamilo', C('esmolol', '4.3')),
         ix('Otros fármacos que causan hipotensión o bradicardia', 'Efectos aditivos', C('esmolol', '4.5'))],
        ea(['Hipotensión', 'Sudoración'], ['Bradicardia', 'Broncoespasmo', 'Necrosis por extravasación'], ['FC y PA continuas'], C('esmolol', '4.8')),
        [],
        discrepancias=[{'campo': 'fuente chilena', 'valores': ['Protocolo Pucón 2022 no incluye esmolol'], 'decision': 'Ficha basada en CIMA y Pediamécum.'}],
    )

    F['enalaprilato'] = ficha(
        'enalaprilato', 'Enalaprilato', 'antihipertensivo', HOSP, False,
        [pres('vial-1.25mg-1ml', 'vial 1,25 mg/ml', 1.25, 'mg', 1, FDA('ENALAPRILATO', 'Enalaprilat injection 1,25 mg/ml'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo'], 'texto': 'IV en 5 minutos. Respuesta en unos 15 minutos; efecto máximo de la 1.ª dosis hasta 4 h.', 'tiempoMinimoMin': 5, 'fuente': FDA('ENALAPRILATO', 'Dosage and administration')},
        [dosis('Hipertensión: cada 6 h', 'adulto', 'mg', FDA('ENALAPRILATO', '1,25 mg cada 6 h; hasta 5 mg cada 6 h'), mn=1.25, mx=5),
         dosis('Paciente con diuréticos: dosis inicial', 'adulto', 'mg', FDA('ENALAPRILATO', '0,625 mg'), mn=0.625, mx=0.625)],
        {'fuente': FDA('ENALAPRILATO', 'Dosage and administration (no informa estabilidad)')},
        [ix('Diuréticos', 'Hipotensión excesiva tras la primera dosis', FDA('ENALAPRILATO', 'Drug interactions')),
         ix('AINE', 'Deterioro de la función renal; menor efecto antihipertensivo', FDA('ENALAPRILATO', 'Drug interactions'))],
        ea([], ['Hipotensión', 'Angioedema', 'Hiperkalemia'], ['PA', 'Potasio y creatinina'], FDA('ENALAPRILATO', 'Warnings')),
        [],
        discrepancias=[{'campo': 'fuente', 'valores': ['No está en CIMA ni en Pucón'], 'decision': 'Fuente FDA; confirmar disponibilidad en Chile.'}],
    )

    F['nimodipino'] = ficha(
        'nimodipino', 'Nimodipino', 'antihipertensivo', HOSP, False,
        [pres('fco-10mg-50ml', 'frasco 0,2 mg/ml', 10, 'mg', 50, C('nimodipino', '2: frasco de 50 ml con 10 mg'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['infusion_continua'], 'texto': 'Infusión IV continua por catéter central con bomba, mediante llave de tres vías junto con otra solución. Proteger de la luz.', 'requiereBomba': True, 'requiereViaCentral': True, 'fuente': C('nimodipino', '4.2.2')},
        [dosis('Inicio (2 h), luego 2 mg/h si se tolera', 'adulto', 'mg/h', C('nimodipino', '4.2.1: 1 mg/h 2 h, luego 2 mg/h; 0,5 mg/h si < 70 kg o PA inestable'), mn=0.5, mx=2)],
        {'protegerLuz': True, 'fuente': C('nimodipino', '6.4: proteger de la luz; evitar luz solar directa durante la infusión')},
        [ix('Cimetidina y ácido valproico', 'Aumentan la concentración de nimodipino', C('nimodipino', '4.5'))],
        ea(['Hipotensión', 'Cefalea', 'Rubor'], ['Hipotensión grave', 'Flebitis'], ['PA'], C('nimodipino', '4.8')),
        ['Contiene etanol.'],
        discrepancias=[{'campo': 'pediatría y fuente chilena', 'valores': ['CIMA: no establecido en menores de 18 años', 'Pucón 2022 no incluye nimodipino'], 'decision': 'Sin dosis pediátrica; ficha basada en CIMA.'}],
    )

    F['metoprolol'] = ficha(
        'metoprolol', 'Metoprolol', 'antiarritmico', URG_H, False,
        [pres('amp-5mg-5ml', 'ampolla 1 mg/ml', 5, 'mg', 5, C('metoprolol', '2: 1 mg/ml; dosis IV de 5 mg'))],
        {'sueros': [], 'estandar': []},
        {'vias': ['bolo'], 'texto': 'Bolo IV a 1–2 mg/min, repetible cada 5 minutos según respuesta. Monitorizar FC y PA.', 'fuente': C('metoprolol', '4.2')},
        [dosis('Arritmias: bolo (repetible cada 5 min; total habitual 10–15 mg)', 'adulto', 'mg', C('metoprolol', '4.2: hasta 5 mg; total 10–15 mg; ≥ 20 mg sin beneficio'), mn=5, mx=5, maxima=20),
         dosis('Infarto agudo: 3 bolos cada 2 min', 'adulto', 'mg', C('metoprolol', '4.2: 5 mg por bolo, total 15 mg'), mn=5, mx=5, maxima=15)],
        {'fuente': C('metoprolol', '6.3 (no informa estabilidad)')},
        [ix('Verapamilo IV', 'No administrar a pacientes con betabloqueadores', C('metoprolol', '4.4')),
         ix('Inhibidores del CYP2D6', 'Aumentan el nivel de metoprolol', C('metoprolol', '4.5'))],
        ea(['Fatiga', 'Mareo', 'Bradicardia'], ['Bradicardia grave y bloqueo AV', 'Hipotensión', 'Broncoespasmo'], ['FC y PA'], C('metoprolol', '4.8')),
        [],
        discrepancias=[{'campo': 'presentación y pediatría', 'valores': ['CIMA: 1 mg/ml (volumen de ampolla no confirmado en el extracto)', 'Pediamécum solo tiene pautas orales'], 'decision': 'Se registra ampolla de 5 ml (5 mg); sin dosis pediátrica IV.'}],
    )

    return F
