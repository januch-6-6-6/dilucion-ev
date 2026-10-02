"""Tanda 2: antiinfecciosos (25). Preparación y administración: guía del Hospital de Iquique (adultos) y Pucón;
dosis: CIMA y Pediamécum. Compatibilidad en Y la llena la matriz global; las incompatibilidades de Iquique van como alerta."""
from .comun import C, P, PED, fu, fuente_cima, fuente_pediamecum
from .tanda1b import conc, dil, dosis, ea, ficha, ix, pres

I = lambda d: fu('IQUIQUE-2020', d)  # noqa: E731
AMB = ['urgencia', 'upc', 'hospitalizacion']

FDA = lambda k, d: fu(f'FDA-{k}', d)  # noqa: E731

FUENTES_EXTRA = [{
    'id': 'FDA-AMPICILINA',
    'titulo': 'Ampicillin for injection — Prescribing information (Dosage and administration)',
    'institucion': 'U.S. FDA / DailyMed',
    'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=06ca924c-5f3a-4924-90f4-5ba623daaa0e',
    'anio': 2026,
    'consultado': '2026-10-01',
}, {
    'id': 'FDA-UNASYN',
    'titulo': 'Unasyn (ampicillin sodium/sulbactam sodium) — Prescribing information (Dosage and administration)',
    'institucion': 'U.S. FDA / DailyMed',
    'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=12eeb72a-403d-41be-bae4-4cb930862884',
    'anio': 2026,
    'consultado': '2026-10-01',
}, {
    'id': 'IQUIQUE-2020',
    'titulo': 'Recomendaciones de administración de antiinfecciosos intravenosos en pacientes adultos',
    'institucion': 'Unidad de Farmacia y Prótesis, Hospital Dr. Ernesto Torres Galdames (Iquique, Chile)',
    'url': 'https://www.hospitaliquique.cl/images/FARMACIA/Recomendaciones_adultos.pdf',
    'anio': 2020,
    'consultado': '2026-10-01',
}]

CIMA = {
    'cefazolina': ('83507', 'Cefazolina Qilu 1 g polvo para solución inyectable y para perfusión'),
    'ceftriaxona': ('64538', 'Ceftriaxona Fresenius Kabi 1 g polvo para solución inyectable intravenosa'),
    'cefotaxima': ('57720', 'Cefotaxima Normon 1 g polvo y disolvente para solución inyectable'),
    'ceftazidima': ('67007', 'Ceftazidima Normon 1 g polvo y disolvente para solución inyectable'),
    'cefepime': ('75148', 'Cefepima Accord 1 g polvo para solución inyectable y para perfusión'),
    'cloxacilina': ('63636', 'Cloxacilina Normon 1 g polvo para solución inyectable y para perfusión'),
    'penicilina-g-sodica': ('33580', 'Penilevel 1.000.000 UI polvo y disolvente para solución inyectable (bencilpenicilina sódica)'),
    'piperacilina-tazobactam': ('71286', 'Piperacilina/Tazobactam Sandoz 4 g/0,5 g polvo para solución para perfusión'),
    'imipenem': ('72637', 'Imipenem/Cilastatina Aurovitas 500 mg/500 mg polvo para solución para perfusión'),
    'meropenem': ('84438', 'Meropenem Hikma 1 g polvo para solución inyectable y para perfusión'),
    'ertapenem': ('83011', 'Ertapenem Aurovitas 1 g polvo para concentrado para solución para perfusión'),
    'vancomicina': ('85651', 'Vancomicina Normon 1.000 mg polvo para concentrado para solución para perfusión'),
    'clindamicina': ('63667', 'Clindamicina Normon 300 mg/2 ml solución inyectable'),
    'metronidazol': ('68091', 'Metronidazol Altan 5 mg/ml solución para perfusión'),
    'gentamicina': ('63854', 'Gentamicina Braun 3 mg/ml solución para perfusión'),
    'amikacina': ('57012', 'Amikacina Normon 500 mg/2 ml solución inyectable y para perfusión'),
    'ciprofloxacino': ('67554', 'Ciprofloxacino Altan 2 mg/ml solución para perfusión'),
    'levofloxacino': ('68867', 'Levofloxacino Altan 5 mg/ml solución para perfusión'),
    'cotrimoxazol': ('54920', 'Soltrim 160 mg/800 mg polvo y solución para solución inyectable (trimetoprim/sulfametoxazol)'),
    'fluconazol': ('67818', 'Fluconazol Altan 2 mg/ml solución para perfusión'),
    'aciclovir': ('85222', 'Aciclovir Accord 25 mg/ml concentrado para solución para perfusión'),
    'linezolid': ('80258', 'Linezolid Altan 2 mg/ml solución para perfusión'),
    'azitromicina': ('85006', 'Azitromicina Tecnigen 500 mg polvo para solución para perfusión'),
}
PEDIAMECUM = {'meropenem': 'Meropenem', 'fluconazol': 'Fluconazol', 'linezolid': 'Linezolid', 'aciclovir': 'Aciclovir'}
PEDIAMECUM_SLUG = {}


def fuentes():
    lista = [fuente_cima(k, nreg, nombre) for k, (nreg, nombre) in CIMA.items()]
    for k, n in PEDIAMECUM.items():
        f = fuente_pediamecum(k, n)
        if k in PEDIAMECUM_SLUG:
            f['url'] = f'https://www.aeped.es/comite-medicamentos/pediamecum/{PEDIAMECUM_SLUG[k]}'
        lista.append(f)
    return lista + FUENTES_EXTRA


def incompatibles(texto):
    return f'Incompatible en Y según la guía de Iquique con: {texto}.'


def polvo(k, nombre, pres_, recon_ml, recon_txt, sueros, estandar, vias, texto, dosis_, estab, inter, efectos, incompat,
          tmin=None, cmax=None, cmin=None, alertas=(), discrepancias=(), proteger_luz=None):
    """Ficha de antiinfeccioso; si recon_ml, las presentaciones son polvos reconstituidos a ese volumen."""
    dl = {'sueros': sueros, 'estandar': estandar}
    if cmin:
        dl['concentracionMin'] = cmin
    if cmax:
        dl['concentracionMax'] = cmax
    adm = {'vias': vias, 'texto': texto, 'fuente': I('Tiempo y detalles de administración')}
    if tmin:
        adm['tiempoMinimoMin'] = tmin
    if proteger_luz:
        estab = {**estab, 'protegerLuz': True}
    rec = {'diluyente': recon_txt, 'volumenMl': recon_ml, 'fuente': I(f'Reconstitución: {recon_ml} ml de {recon_txt}')} if recon_ml else None
    return ficha(k, nombre, 'antiinfeccioso', AMB, False, pres_, dl, adm, dosis_, estab, inter, efectos,
                 [incompatibles(incompat), *alertas] if incompat else list(alertas), reconstitucion=rec, discrepancias=discrepancias)


EA_BL = lambda k: ea(['Diarrea', 'Exantema', 'Flebitis en el sitio de infusión'], ['Anafilaxia', 'Colitis por Clostridioides difficile'], ['Signos de alergia en la primera dosis', 'Deposiciones'], C(k, '4.8; 4.4'))  # noqa: E731


def fichas(stab=None):
    F = {}

    F['cefazolina'] = polvo(
        'cefazolina', 'Cefazolina',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 10, I('Cefazolina: FA 1 g'))], 10, 'suero fisiológico',
        ['SF'], [dil('1 g en 10 ml (bolo de 3–5 min)', 1, 'g', 10, I('Cefazolina: 1 g en 10 ml, bolo 3 a 5 minutos (profilaxis)'))],
        ['bolo', 'infusion_intermitente'], 'Bolo IV de 3 a 5 minutos (profilaxis quirúrgica 30–60 min antes de la incisión).',
        [dosis('Dosis diaria total (en 2–4 dosis); hasta 6 g/día en infecciones graves', 'adulto', 'g/24 h', C('cefazolina', '4.2: 1–2 g/día (sensibles), 3–4 g/día (menos sensibles), hasta 6 g/día'), mn=1, mx=4, maxima=6),
         dosis('Profilaxis quirúrgica (30–60 min antes)', 'adulto', 'g', C('cefazolina', '4.2: 1–2 g IV'), mn=1, mx=2),
         dosis('Niños > 1 mes (en 2–4 dosis)', 'pediatrico', 'mg/kg/24 h', C('cefazolina', '4.2 Población pediátrica: 25–50 mg/kg/día; hasta 100 mg/kg/día'), mn=25, mx=50, maxima=100)],
        {'refrigeradoH': 24, 'fuente': I('Cefazolina: reconstituida 24 h en refrigeración')},
        [ix('Antibióticos bacteriostáticos (tetraciclinas, eritromicina, cloranfenicol)', 'Posible antagonismo', C('cefazolina', '4.5')),
         ix('Probenecid', 'Reduce el aclaramiento renal de cefazolina', C('cefazolina', '4.5'))],
        EA_BL('cefazolina'), 'amiodarona, anfotericina B y vancomicina', tmin=3)

    F['ceftriaxona'] = polvo(
        'ceftriaxona', 'Ceftriaxona',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 10, I('Ceftriaxona: FA 1 g'))], 10, 'suero fisiológico',
        ['SF', 'SG5'], [dil('1 g en 10 ml (bolo de 3–5 min)', 1, 'g', 10, I('Ceftriaxona: 1 g en 10 ml, bolo 3 a 5 minutos'))],
        ['bolo', 'infusion_intermitente'], 'Bolo IV de 3 a 5 minutos. Nunca reconstituir ni diluir con soluciones que contengan calcio (Ringer, Hartmann).',
        [dosis('Una vez al día (2–4 g en meningitis, endocarditis o neutropenia febril)', 'adulto', 'g/24 h', C('ceftriaxona', '4.2.1: 1–2 g una vez al día; hasta 4 g'), mn=1, mx=2, maxima=4),
         dosis('Niños de 15 días a 12 años (< 50 kg), una vez al día', 'pediatrico', 'mg/kg/24 h', C('ceftriaxona', '4.2.1: 50–80 mg/kg; 80–100 mg/kg en meningitis (máx. 4 g)'), mn=50, mx=100)],
        {'refrigeradoH': 24, 'fuente': I('Ceftriaxona: reconstituida 24 h en refrigeración')},
        [ix('Soluciones con calcio (Ringer, Hartmann, gluconato de calcio)', 'Precipitado de ceftriaxona-calcio; contraindicado en neonatos', C('ceftriaxona', '4.5'))],
        EA_BL('ceftriaxona'), 'anfotericina B, aciclovir, amiodarona, fluconazol, gluconato de calcio, heparina, labetalol, linezolid, morfina, propofol, remifentanilo y vancomicina',
        tmin=3, alertas=['No administrar con soluciones que contengan calcio.'],
        discrepancias=[{'campo': 'concentración', 'valores': ['Iquique: bolo de 1 g en 10 ml (100 mg/ml)', 'Pucón: reconstituir a 100 mg/ml y diluir a 10–40 mg/ml'], 'decision': 'Se registra el bolo de Iquique; la concentración de infusión depende del protocolo local.'}])

    F['cefotaxima'] = polvo(
        'cefotaxima', 'Cefotaxima',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 10, I('Cefotaxima: FA 1 g'))], 10, 'suero fisiológico',
        ['SF'], [dil('1 g en 10 ml (bolo de 3–5 min)', 1, 'g', 10, I('Cefotaxima: 1 g en 10 ml, bolo 3 a 5 minutos'))],
        ['bolo', 'infusion_intermitente'], 'Bolo IV de 3 a 5 minutos.',
        [dosis('Por dosis, cada 12 h (cada 6–8 h en infecciones graves; máx. 12 g/día)', 'adulto', 'g', C('cefotaxima', '4.2: 1–2 g cada 12 h; hasta 12 g/día'), mn=1, mx=2),
         dosis('Lactantes y niños < 12 años (en dosis cada 6–12 h)', 'pediatrico', 'mg/kg/24 h', C('cefotaxima', '4.2: 50–100 mg/kg/día (hasta 150; 200 en riesgo vital)'), mn=50, mx=100, maxima=200)],
        {'refrigeradoH': 24, 'fuente': I('Cefotaxima: reconstituida 24 h en refrigeración')},
        [ix('Antibióticos bacteriostáticos', 'Antagonismo in vitro; no combinar', C('cefotaxima', '4.5')),
         ix('Probenecid', 'Duplica aproximadamente la exposición a cefotaxima', C('cefotaxima', '4.5'))],
        EA_BL('cefotaxima'), 'filgrastim, fluconazol, midazolam y vancomicina', tmin=3,
        cmax=conc(100, 'mg', P('Anexo 6, Cefotaxima: 20–60 mg/ml, hasta un máximo de 100 mg/ml')))

    F['ceftazidima'] = polvo(
        'ceftazidima', 'Ceftazidima',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 10, I('Ceftazidima: FA 1 g'))], 10, 'suero fisiológico',
        ['SF'], [dil('1 g en 50 ml', 1, 'g', 50, I('Ceftazidima: 1 g en 50 ml')), dil('2 g en 100 ml', 2, 'g', 100, I('Ceftazidima: 2 g en 100 ml'))],
        ['infusion_intermitente'], 'Infusión prolongada de 3 horas según la guía de Iquique.',
        [dosis('Por dosis, cada 8 h (máx. 9 g/día)', 'adulto', 'g', C('ceftazidima', '4.2 Tabla 1: 1–2 g cada 8 h'), mn=1, mx=2),
         dosis('Lactantes > 2 meses y niños < 40 kg (en 3 dosis)', 'pediatrico', 'mg/kg/24 h', C('ceftazidima', '4.2 Tabla 2: 100–150 mg/kg/día, máx. 6 g/día'), mn=100, mx=150)],
        {'refrigeradoH': 24, 'fuente': I('Ceftazidima: reconstituida 24 h en refrigeración')},
        [ix('Medicamentos nefrotóxicos en dosis altas', 'Puede empeorar la función renal', C('ceftazidima', '4.5'))],
        EA_BL('ceftazidima'), 'amiodarona, aminofilina, bicarbonato de sodio, anfotericina B, dobutamina, fluconazol, midazolam, propofol y vancomicina')

    F['cefepime'] = polvo(
        'cefepime', 'Cefepime',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 10, I('Cefepime: FA 1 g'))], 10, 'suero fisiológico',
        ['SF', 'SG5'], [dil('1 g en 50 ml', 1, 'g', 50, I('Cefepime: 1 g en 50 ml')), dil('2 g en 100 ml', 2, 'g', 100, I('Cefepime: 2 g en 100 ml'))],
        ['infusion_intermitente'], 'Infusión prolongada de 3 horas según la guía de Iquique.',
        [dosis('Infecciones graves, cada 12 h (muy graves cada 8 h)', 'adulto', 'g', C('cefepime', '4.2: 2 g cada 12 u 8 horas'), mn=2, mx=2),
         dosis('Niños > 2 meses (≤ 40 kg), cada 12 h (graves cada 8 h)', 'pediatrico', 'mg/kg', C('cefepime', '4.2: 50 mg/kg'), mn=50, mx=50, tope=(2, 'g'))],
        {'refrigeradoH': 24, 'fuente': I('Cefepime: reconstituido 24 h en refrigeración')},
        [ix('Anticoagulantes cumarínicos', 'Posible potenciación del efecto anticoagulante', C('cefepime', '4.5'))],
        EA_BL('cefepime'), 'aciclovir, anfotericina B, ciprofloxacino, diazepam, dobutamina, dopamina, fenitoína, haloperidol, sulfato de magnesio, metoclopramida, midazolam, morfina, ondansetrón, propofol y vancomicina')

    F['ampicilina'] = polvo(
        'ampicilina', 'Ampicilina',
        [pres('fa-500mg', 'frasco ampolla (polvo)', 500, 'mg', 10, I('Ampicilina: FA 500 mg'))], 10, 'suero fisiológico',
        ['SF'], [dil('Hasta 1 g en 50 ml', 1, 'g', 50, I('Ampicilina: ≤ 1 g en 50 ml; > 1 g en 100 ml'))],
        ['bolo', 'infusion_intermitente'], 'Infusión intermitente de 10 a 15 minutos.',
        [dosis('Infecciones respiratorias y de partes blandas (≥ 40 kg), cada 6 h', 'adulto', 'mg', fu('FDA-AMPICILINA', '250–500 mg cada 6 h'), mn=250, mx=500),
         dosis('Meningitis bacteriana (adultos y niños), en dosis cada 3–4 h', 'adulto', 'mg/kg/24 h', fu('FDA-AMPICILINA', '150–200 mg/kg/día'), mn=150, mx=200),
         dosis('Niños < 40 kg (cada 6–8 h)', 'pediatrico', 'mg/kg/24 h', fu('FDA-AMPICILINA', '25–50 mg/kg/día'), mn=25, mx=50),
         dosis('Meningitis bacteriana (niños), en dosis cada 3–4 h', 'pediatrico', 'mg/kg/24 h', fu('FDA-AMPICILINA', '150–200 mg/kg/día'), mn=150, mx=200)],
        {'refrigeradoH': 8, 'fuente': I('Ampicilina: reconstituida 8 h en refrigeración')},
        [],
        ea(['Exantema', 'Diarrea'], ['Anafilaxia', 'Colitis por Clostridioides difficile'], ['Signos de alergia'], P('Anexo 6, Ampicilina: RAM')),
        'clindamicina, anfotericina B, ciprofloxacino, epinefrina, fluconazol, midazolam, ondansetrón, gluconato de calcio, vancomicina y aminoglucósidos',
        discrepancias=[{'campo': 'fuente de dosis', 'valores': ['CIMA no tiene ficha técnica de ampicilina IV disponible', 'Pucón: bolo a 100 mg/ml', 'Iquique: infusión de 10–15 min'], 'decision': 'Dosis desde FDA; las dosis de adulto de FDA son bajas para infecciones graves: revisar con protocolo local.'}])

    F['ampicilina-sulbactam'] = polvo(
        'ampicilina-sulbactam', 'Ampicilina/sulbactam', 
        [pres('fa-1.5g', 'frasco ampolla (polvo) 1 g/0,5 g', 1.5, 'g', 10, I('Ampicilina/sulbactam: FA 1 g/0,5 g'))], 10, 'suero fisiológico',
        ['SF'], [dil('1,5 g en 100 ml', 1.5, 'g', 100, I('Ampicilina/sulbactam: 1 g/0,5 g en 100 ml'))],
        ['infusion_intermitente'], 'Infusión intermitente de 15 a 30 minutos.',
        [dosis('Cada 6 h (dosis total ampicilina + sulbactam; sulbactam máx. 4 g/día)', 'adulto', 'g', fu('FDA-UNASYN', '1,5–3 g cada 6 h'), mn=1.5, mx=3),
         dosis('Niños ≥ 1 año (en 4 dosis; total ampicilina + sulbactam)', 'pediatrico', 'mg/kg/24 h', fu('FDA-UNASYN', '300 mg/kg/día'), mn=300, mx=300)],
        {'fuente': I('Ampicilina/sulbactam: utilizar inmediatamente tras reconstituir')},
        [ix('Aminoglucósidos', 'Inactivación in vitro: no reconstituir ni mezclar juntos', fu('FDA-UNASYN', 'Drug interactions')),
         ix('Alopurinol', 'Aumenta la incidencia de exantema', fu('FDA-UNASYN', 'Drug interactions'))],
        ea(['Dolor en el sitio de inyección', 'Diarrea', 'Exantema'], ['Anafilaxia', 'Colitis por Clostridioides difficile'], ['Signos de alergia'], fu('FDA-UNASYN', 'Adverse reactions')),
        'clindamicina, anfotericina B, ciprofloxacino, epinefrina, fluconazol, midazolam, ondansetrón, gluconato de calcio, vancomicina y aminoglucósidos',
        discrepancias=[{'campo': 'fuente', 'valores': ['No hay ficha técnica en CIMA (no comercializado en España)'], 'decision': 'Dosis desde FDA (Unasyn).'}])

    F['cloxacilina'] = polvo(
        'cloxacilina', 'Cloxacilina',
        [pres('fa-500mg', 'frasco ampolla (polvo)', 500, 'mg', 10, I('Cloxacilina: FA 500 mg'))], 10, 'suero fisiológico',
        ['SF'], [dil('Hasta 1 g en 100 ml', 1, 'g', 100, I('Cloxacilina: ≤ 1000 mg en 100 ml; > 1000 mg en 250 ml'))],
        ['bolo', 'infusion_intermitente'], 'Infusión intermitente de 30 a 60 minutos (CIMA permite IV directa lenta de 3–4 min).',
        [dosis('Cada 6–8 h', 'adulto', 'mg', C('cloxacilina', '4.2: 500 mg–1 g cada 6–8 h'), mn=500, mx=1000),
         dosis('Niños > 2 años, cada 6–8 h', 'pediatrico', 'mg/kg', C('cloxacilina', '4.2: 12,5–25 mg/kg'), mn=12.5, mx=25, tope=(1, 'g'))],
        {'refrigeradoH': 24, 'fuente': I('Cloxacilina: reconstituida 24 h en refrigeración')},
        [ix('Antibióticos bacteriostáticos', 'Antagonizan su acción bactericida', C('cloxacilina', '4.5'))],
        EA_BL('cloxacilina'), 'gentamicina y amikacina', cmax=conc(50, 'mg', P('Anexo 6, Cloxacilina: dilución 10–50 mg/ml')),
        discrepancias=[{'campo': 'reconstitución', 'valores': ['Iquique: 10 ml de SF (50 mg/ml)', 'Pucón: 100 mg/ml'], 'decision': 'Se registra la de Iquique.'}])

    F['penicilina-g-sodica'] = polvo(
        'penicilina-g-sodica', 'Penicilina G sódica',
        [pres('fa-1mui', 'frasco ampolla (polvo) 1.000.000 UI', 1000000, 'UI', 10, P('Anexo 6, Penicilina sódica: FAL 1.000.000 UI')),
         pres('fa-2mui', 'frasco ampolla (polvo) 2.000.000 UI', 2000000, 'UI', 10, I('Penicilina sódica: FA 1–2 millones'))], 10, 'suero fisiológico',
        ['SF', 'SG5'], [dil('Hasta 3 millones UI en 50 ml', 3000000, 'UI', 50, I('Penicilina sódica: ≤ 3 millones en 50 ml; > 3 millones en 100 ml'))],
        ['infusion_intermitente'], 'Infusión intermitente de 30 a 60 minutos.',
        [dosis('Dosis diaria en dosis cada 4 h (hasta 24 MUI/día en infecciones graves)', 'adulto', 'UI/24 h', C('penicilina-g-sodica', '4.2: 1–3 MUI/día; infecciones respiratorias 5–24 MUI/día'), mn=1000000, mx=24000000),
         dosis('Niños hasta 12 años (cada 4–6 h; máx. 24 MUI/día)', 'pediatrico', 'UI/kg/24 h', C('penicilina-g-sodica', '4.2: 100.000–300.000 UI/kg/día'), mn=100000, mx=300000)],
        {'refrigeradoH': 24, 'fuente': I('Penicilina sódica: reconstituida 24 h en refrigeración')},
        [ix('Metotrexato', 'Reduce su excreción: toxicidad; evitar', C('penicilina-g-sodica', '4.5'))],
        EA_BL('penicilina-g-sodica'), 'anfotericina B, clorpromazina, heparina, metilprednisolona y cloruro de potasio',
        cmax=conc(100000, 'UI', P('Anexo 6, Penicilina sódica: dilución 50.000–100.000 UI/ml')))

    F['piperacilina-tazobactam'] = polvo(
        'piperacilina-tazobactam', 'Piperacilina/tazobactam',
        [pres('fa-4.5g', 'frasco ampolla (polvo) 4 g/0,5 g', 4.5, 'g', 20, I('Piperacilina/tazobactam: FA 4 g/0,5 g'))], 20, 'suero fisiológico',
        ['SF', 'SG5'], [dil('4,5 g en 100 ml', 4.5, 'g', 100, I('Piperacilina/tazobactam: 4,5 g en 100 ml'))],
        ['infusion_intermitente'], 'Infusión prolongada de 4 horas según la guía de Iquique.',
        [dosis('Cada 8 h (cada 6 h en neumonía grave o neutropenia febril)', 'adulto', 'g', C('piperacilina-tazobactam', '4.2: 4 g/0,5 g'), mn=4.5, mx=4.5),
         dosis('Niños 2–12 años, cada 8 h (dosis total 100 mg + 12,5 mg por kg)', 'pediatrico', 'mg/kg', C('piperacilina-tazobactam', '4.2 Población pediátrica: 100 mg de piperacilina/12,5 mg de tazobactam por kg'), mn=112.5, mx=112.5, tope=(4.5, 'g'))],
        {'refrigeradoH': 24, 'fuente': I('Piperacilina/tazobactam: reconstituida 24 h en refrigeración')},
        [ix('Relajantes musculares no despolarizantes (vecuronio)', 'Prolongación del bloqueo neuromuscular', C('piperacilina-tazobactam', '4.5'))],
        EA_BL('piperacilina-tazobactam'), 'bicarbonato de sodio, amikacina, aciclovir, amiodarona, anfotericina B, dobutamina, fluconazol, gentamicina, haloperidol, ondansetrón y vancomicina')

    F['imipenem'] = polvo(
        'imipenem', 'Imipenem/cilastatina',
        [pres('fa-500mg', 'frasco ampolla (polvo) 500 mg/500 mg', 500, 'mg', 10, I('Imipenem-cilastatina: FA 500 mg'))], 10, 'suero fisiológico',
        ['SF'], [dil('500 mg en 100 ml', 500, 'mg', 100, I('Imipenem: 500 mg en 100 ml')), dil('1 g en 250 ml', 1, 'g', 250, I('Imipenem: 1 g en 250 ml'))],
        ['infusion_intermitente'], 'Infusión de 2 horas; diluir solo en SF por mayor estabilidad.',
        [dosis('500 mg cada 6 h o 1 g cada 6–8 h (máx. 4 g/día)', 'adulto', 'mg', C('imipenem', '4.2'), mn=500, mx=1000),
         dosis('Niños ≥ 1 año, cada 6 h', 'pediatrico', 'mg/kg', C('imipenem', '4.2: 15/15 o 25/25 mg/kg'), mn=15, mx=25, tope=(1, 'g'))],
        {'refrigeradoH': 24, 'fuente': I('Imipenem: reconstituido 24 h en refrigeración')},
        [ix('Ganciclovir', 'Convulsiones generalizadas', C('imipenem', '4.5')),
         ix('Ácido valproico', 'Descenso de sus niveles bajo el rango terapéutico', C('imipenem', '4.5'))],
        EA_BL('imipenem'), 'anfotericina B, amiodarona, bicarbonato de sodio, fluconazol, lorazepam, midazolam y milrinona')

    F['meropenem'] = polvo(
        'meropenem', 'Meropenem',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 20, I('Meropenem: FA 1 g en 20 ml de SF')),
         pres('fa-500mg', 'frasco ampolla (polvo)', 500, 'mg', 10, I('Meropenem: FA 500 mg en 10 ml de SF'))], 20, 'suero fisiológico',
        ['SF'], [dil('Hasta 2 g en 100 ml', 2, 'g', 100, I('Meropenem: ≤ 2 g en 100 ml'))],
        ['bolo', 'infusion_intermitente', 'infusion_continua'], 'Infusión prolongada de 4 horas (Iquique); CIMA: perfusión de 15–30 min o bolo de hasta 1 g en 5 min. Diluir solo en SF.',
        [dosis('Cada 8 h (2 g en meningitis)', 'adulto', 'g', C('meropenem', '4.2: 500 mg–2 g cada 8 h'), mn=0.5, mx=2),
         dosis('Niños 3 meses–11 años (≤ 50 kg), cada 8 h (mayoría de infecciones)', 'pediatrico', 'mg/kg', PED('meropenem', '10–20 mg/kg cada 8 h'), mn=10, mx=20, tope=(1, 'g')),
         dosis('Meningitis bacteriana o fibrosis quística (niños), cada 8 h', 'pediatrico', 'mg/kg', PED('meropenem', '40 mg/kg cada 8 h'), mn=40, mx=40, tope=(2, 'g'))],
        {'refrigeradoH': 24, 'fuente': I('Meropenem: reconstituido 24 h en refrigeración')},
        [ix('Probenecid', 'Aumenta la concentración de meropenem', C('meropenem', '4.5'))],
        EA_BL('meropenem'), 'aciclovir, anfotericina B, cloruro de potasio, gluconato de calcio, diazepam, metronidazol y ondansetrón',
        discrepancias=[{'campo': 'reconstitución', 'valores': ['Iquique: 500 mg en 10 ml y 1 g en 20 ml (ambos 50 mg/ml)'], 'decision': 'Ambas presentaciones a 50 mg/ml; la ficha registra 20 ml (frasco de 1 g) como volumen de reconstitución.'}])

    F['ertapenem'] = polvo(
        'ertapenem', 'Ertapenem',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 10, I('Ertapenem: FA 1 g'))], 10, 'suero fisiológico',
        ['SF'], [dil('1 g en 50 ml', 1, 'g', 50, I('Ertapenem: 1 g en 50 ml'))],
        ['infusion_intermitente'], 'Infusión de 30 minutos. No usar soluciones con dextrosa; no mezclar con otros fármacos.',
        [dosis('Una vez al día', 'adulto', 'g', C('ertapenem', '4.2: 1 g una vez al día'), mn=1, mx=1),
         dosis('Lactantes y niños 3 meses–12 años, cada 12 h (máx. 1 g/día)', 'pediatrico', 'mg/kg', C('ertapenem', '4.2: 15 mg/kg dos veces al día'), mn=15, mx=15, tope=(500, 'mg'))],
        {'fuente': I('Ertapenem: utilizar inmediatamente')},
        [ix('Ácido valproico', 'Reducción de sus niveles bajo el rango terapéutico', C('ertapenem', '4.5'))],
        EA_BL('ertapenem'), 'soluciones con dextrosa y cualquier otro medicamento por la misma vía', tmin=30)

    F['vancomicina'] = polvo(
        'vancomicina', 'Vancomicina',
        [pres('fa-1g', 'frasco ampolla (polvo)', 1, 'g', 20, I('Vancomicina: FA 1 g en 20 ml de SF')),
         pres('fa-500mg', 'frasco ampolla (polvo)', 500, 'mg', 10, I('Vancomicina: FA 500 mg en 10 ml de SF'))], 20, 'suero fisiológico',
        ['SF', 'SG5'], [dil('500 mg en 100 ml (5 mg/ml)', 500, 'mg', 100, C('vancomicina', '4.2: al menos 100 ml por 500 mg')),
                        dil('1 g en 250 ml', 1, 'g', 250, I('Vancomicina: > 1 g en 250 ml'))],
        ['infusion_intermitente'], 'Infusión de al menos 60 minutos y no más de 10 mg/min (dosis > 1 g en 2 h): la infusión rápida causa reacciones (enrojecimiento, hipotensión).',
        [dosis('≥ 12 años: cada 8–12 h (máx. 2 g por dosis)', 'adulto', 'mg/kg', C('vancomicina', '4.2: 15–20 mg/kg'), mn=15, mx=20),
         dosis('Dosis de carga en paciente grave', 'adulto', 'mg/kg', C('vancomicina', '4.2: 25–30 mg/kg'), mn=25, mx=30),
         dosis('Lactantes y niños 1 mes–12 años, cada 6 h', 'pediatrico', 'mg/kg', C('vancomicina', '4.2: 10–15 mg/kg'), mn=10, mx=15, tope=(2, 'g'))],
        {'refrigeradoH': 24, 'fuente': I('Vancomicina: reconstituida 24 h en refrigeración')},
        [ix('Anestésicos', 'Eritema, enrojecimiento histaminoide y reacciones anafilactoides', C('vancomicina', '4.5')),
         ix('Fármacos nefrotóxicos u ototóxicos (aminoglucósidos)', 'Toxicidad aditiva', C('vancomicina', '4.4'))],
        ea(['Flebitis', 'Exantema'], ['Reacción a la infusión rápida (enrojecimiento, hipotensión)', 'Nefrotoxicidad', 'Ototoxicidad'], ['Niveles plasmáticos', 'Función renal', 'Velocidad de infusión'], C('vancomicina', '4.8; 4.4')),
        'albúmina, anfotericina B, aminofilina, ampicilina, cefazolina, cefepime, cefotaxima, ceftazidima, ceftriaxona, ciprofloxacino, heparina, omeprazol, piperacilina-tazobactam y propofol',
        tmin=60, cmax=conc(10, 'mg', C('vancomicina', '4.2: con restricción de líquidos 500 mg/50 ml (10 mg/ml)')),
        discrepancias=[{'campo': 'concentración', 'valores': ['CIMA: al menos 100 ml por 500 mg (5 mg/ml); 10 mg/ml solo con restricción de líquidos', 'Iquique: ≤ 1 g en 100 ml (10 mg/ml)'], 'decision': 'Máximo registrado 10 mg/ml; la dilución habitual de 5 mg/ml es la de CIMA.'}])

    F['clindamicina'] = polvo(
        'clindamicina', 'Clindamicina',
        [pres('amp-600mg-4ml', 'ampolla', 600, 'mg', 4, I('Clindamicina: 600 mg/4 ml'))], None, None,
        ['SF', 'SG5'], [dil('600 mg en 100 ml (6 mg/ml)', 600, 'mg', 100, I('Clindamicina: ≤ 600 mg en 100 ml; > 600 mg en 250 ml'))],
        ['infusion_intermitente'], 'Infusión de 30 a 60 minutos; no infundir rápido (máx. 30 mg/min).',
        [dosis('Dosis diaria (en 2–4 dosis); máx. recomendada 2,7 g/día', 'adulto', 'g/24 h', C('clindamicina', '4.2: 1,2–1,8 g/día; graves 2,4–2,7 g/día'), mn=1.2, mx=2.7, maxima=4.8),
         dosis('Lactantes y niños (en 3–4 dosis)', 'pediatrico', 'mg/kg/24 h', C('clindamicina', '4.2 Población pediátrica: 20–40 mg/kg/día'), mn=20, mx=40)],
        {'fuente': I('Clindamicina: diluida, preparar y administrar')},
        [ix('Relajantes musculares no despolarizantes y anestésicos inhalatorios', 'Potencia el bloqueo neuromuscular', C('clindamicina', '4.5'))],
        ea(['Diarrea', 'Tromboflebitis'], ['Colitis por Clostridioides difficile', 'Hipotensión o arritmia con infusión rápida'], ['Deposiciones', 'Velocidad de infusión'], P('Anexo 6, Clindamicina: RAM')),
        'aminofilina, ampicilina, fenobarbital, fenitoína, fluconazol y gluconato de calcio', tmin=30,
        cmax=conc(12, 'mg', P('Anexo 6, Clindamicina: dilución 6–12 mg/ml')))

    F['metronidazol'] = polvo(
        'metronidazol', 'Metronidazol',
        [pres('fco-500mg-100ml', 'frasco listo para usar', 500, 'mg', 100, I('Metronidazol: 500 mg/100 ml'))], None, None,
        [], [], ['infusion_intermitente'], 'No requiere dilución. Infusión de 30 a 60 minutos (CIMA: 5 ml/min).',
        [dosis('Cada 8 h', 'adulto', 'mg', C('metronidazol', '4.2: 100 ml (500 mg) cada 8 h'), mn=500, mx=500),
         dosis('Niños < 12 años (en 2–3 perfusiones)', 'pediatrico', 'mg/kg/24 h', C('metronidazol', '4.2: 20–30 mg/kg/día'), mn=20, mx=30)],
        {'ambienteH': 24, 'fuente': I('Metronidazol: 24 h a temperatura ambiente en circuito cerrado')},
        [ix('Alcohol', 'Reacción disulfirámica (hasta un día después del tratamiento)', C('metronidazol', '4.5')),
         ix('Disulfiram', 'Reacciones psicóticas', C('metronidazol', '4.5'))],
        ea(['Cefalea', 'Náuseas', 'Sabor metálico'], ['Neuropatía periférica', 'Convulsiones'], ['Síntomas neurológicos'], P('Anexo 6, Metronidazol: RAM')),
        'anfotericina B, dopamina, filgrastim y meropenem', tmin=30, proteger_luz=True)

    F['gentamicina'] = polvo(
        'gentamicina', 'Gentamicina',
        [pres('amp-80mg-2ml', 'ampolla', 80, 'mg', 2, I('Gentamicina: 80 mg/2 ml'))], None, None,
        ['SF', 'SG5'], [dil('Hasta 160 mg en 100 ml', 160, 'mg', 100, I('Gentamicina: ≤ 160 mg en 100 ml; ≥ 240 mg en 250 ml'))],
        ['infusion_intermitente'], 'Infusión de 30 a 60 minutos, preferentemente en dosis única diaria.',
        [dosis('Dosis diaria (única, preferente)', 'adulto', 'mg/kg/24 h', C('gentamicina', '4.2: 3–6 mg/kg/día'), mn=3, mx=6),
         dosis('Niños 2–12 años (2–2,5 mg/kg cada 8 h)', 'pediatrico', 'mg/kg/24 h', C('gentamicina', '4.2: 6–7,5 mg/kg/día'), mn=6, mx=7.5)],
        {'fuente': I('Gentamicina: diluida, preparar y administrar')},
        [ix('Relajantes musculares', 'Potencian el bloqueo neuromuscular', C('gentamicina', '4.5')),
         ix('Diuréticos de asa y otros nefro/ototóxicos', 'Mayor nefrotoxicidad y ototoxicidad', C('furosemida', '4.5'))],
        ea([], ['Nefrotoxicidad', 'Ototoxicidad', 'Bloqueo neuromuscular'], ['Función renal', 'Niveles plasmáticos', 'Audición'], C('gentamicina', '4.8; 4.4')),
        'anfotericina B, furosemida, heparina, fenitoína, filgrastim, piperacilina-tazobactam y propofol', tmin=30)

    F['amikacina'] = polvo(
        'amikacina', 'Amikacina',
        [pres('amp-500mg-2ml', 'ampolla', 500, 'mg', 2, I('Amikacina: 500 mg/2 ml'))], None, None,
        ['SF'], [dil('Hasta 1 g en 100 ml', 1, 'g', 100, I('Amikacina: ≤ 1 g en 100 ml; > 1 g en 250 ml'))],
        ['infusion_intermitente'], 'Infusión de 30 a 60 minutos.',
        [dosis('Dosis diaria (única o en 2–3 dosis); máx. 1,5 g/día', 'adulto', 'mg/kg/24 h', C('amikacina', '4.2: 15 mg/kg/día'), mn=15, mx=15),
         dosis('Niños < 12 años (única o en 2–3 dosis)', 'pediatrico', 'mg/kg/24 h', C('amikacina', '4.2: 15 mg/kg/día'), mn=15, mx=15)],
        {'fuente': I('Amikacina: diluida, preparar y administrar')},
        [ix('Betalactámicos en la misma mezcla', 'Inactivación mutua', C('amikacina', '4.5'))],
        ea([], ['Nefrotoxicidad', 'Ototoxicidad', 'Neurotoxicidad'], ['Función renal', 'Niveles plasmáticos', 'Audición'], P('Anexo 6, Amikacina: RAM')),
        'anfotericina B, ampicilina, furosemida, heparina, cefazolina y propofol', tmin=30,
        cmax=conc(10, 'mg', P('Anexo 6, Amikacina: dilución 0,25–5 mg/ml; nunca exceder 10 mg/ml')),
        alertas=['Pucón recomienda 0,25–5 mg/ml; 10 mg/ml es el máximo absoluto.'])

    F['ciprofloxacino'] = polvo(
        'ciprofloxacino', 'Ciprofloxacino',
        [pres('fco-200mg-100ml', 'frasco listo para usar', 200, 'mg', 100, I('Ciprofloxacino: 200 mg/100 ml'))], None, None,
        [], [], ['infusion_intermitente'], 'No requiere dilución. Infusión de 30 a 60 minutos (200 mg).',
        [dosis('Cada 8–12 h', 'adulto', 'mg', C('ciprofloxacino', '4.2: 400 mg dos o tres veces al día'), mn=400, mx=400),
         dosis('ITU complicada o pielonefritis (niños), cada 8 h', 'pediatrico', 'mg/kg', C('ciprofloxacino', '4.2 Población pediátrica: 6–10 mg/kg, máx. 400 mg por dosis'), mn=6, mx=10, tope=(400, 'mg'))],
        {'ambienteH': 24, 'fuente': I('Ciprofloxacino: 24 h a temperatura ambiente en circuito cerrado')},
        [ix('Fármacos que prolongan el QT', 'Prolongación aditiva del QT', C('ciprofloxacino', '4.5'))],
        ea(['Náuseas', 'Diarrea'], ['Tendinitis y rotura tendinosa', 'Prolongación del QT', 'Convulsiones'], ['ECG si hay riesgo de QT largo'], C('ciprofloxacino', '4.8; 4.4')),
        'aminofilina, ampicilina, bicarbonato de sodio, cefepime, dexametasona, fenitoína, furosemida, heparina, hidrocortisona, metilprednisolona, propofol, clindamicina, sulfato de magnesio y vancomicina',
        tmin=30, proteger_luz=True)

    F['levofloxacino'] = polvo(
        'levofloxacino', 'Levofloxacino',
        [pres('fco-500mg-100ml', 'bolsa lista para usar', 500, 'mg', 100, C('levofloxacino', '2: 500 mg en 100 ml'))], None, None,
        [], [], ['infusion_intermitente'], 'Perfusión IV lenta: mínimo 60 minutos para 500 mg (30 min para 250 mg).',
        [dosis('Una o dos veces al día', 'adulto', 'mg', C('levofloxacino', '4.2.1: 500 mg una o dos veces al día'), mn=500, mx=500)],
        {'fuente': C('levofloxacino', '6.3 (no informa estabilidad tras abrir)')},
        [ix('AINE y teofilina', 'Disminución marcada del umbral convulsivo', C('levofloxacino', '4.5'))],
        ea(['Náuseas', 'Diarrea'], ['Tendinitis y rotura tendinosa', 'Prolongación del QT', 'Convulsiones'], ['ECG si hay riesgo de QT largo'], C('levofloxacino', '4.8; 4.4')),
        None, tmin=60, alertas=['Contraindicado en niños y adolescentes en crecimiento.'],
        discrepancias=[{'campo': 'fuente chilena / pediatría', 'valores': ['La guía de Iquique no incluye levofloxacino', 'CIMA: contraindicado en niños', 'Pediamécum: 10 mg/kg cada 12–24 h'], 'decision': 'Sin dosis pediátrica (se respeta la contraindicación de la ficha técnica).'}])

    F['cotrimoxazol'] = polvo(
        'cotrimoxazol', 'Cotrimoxazol (sulfametoxazol/trimetoprim)',
        [pres('amp-80mg-5ml', 'ampolla 400/80 mg (expresada en trimetoprim)', 80, 'mg', 5, I('Cotrimoxazol: 400 mg/80 mg en 5 ml'))], None, None,
        ['SG5'], [dil('80 mg de trimetoprim (1 ampolla) en 125 ml', 80, 'mg', 125, I('Cotrimoxazol: 400/80 mg en 125 ml')),
                  dil('160 mg de trimetoprim (2 ampollas) en 250 ml', 160, 'mg', 250, I('Cotrimoxazol: 800/160 mg en 250 ml'))],
        ['infusion_intermitente'], 'Diluir solo en SG5 %. Infusión de 60 minutos (90 min si ≥ 1200/240 mg). No refrigerar.',
        [dosis('Dosis en trimetoprim, cada 12 h (graves: 320 mg cada 6–12 h)', 'adulto', 'mg', C('cotrimoxazol', '4.2.1: 160 mg de trimetoprim cada 12 h'), mn=160, mx=320),
         dosis('Niños 2 meses–12 años, en trimetoprim, cada 12 h', 'pediatrico', 'mg/kg', C('cotrimoxazol', '4.2.1: 3,2 mg/kg de trimetoprim'), mn=3.2, mx=3.2, tope=(160, 'mg'))],
        {'fuente': I('Cotrimoxazol: preparar y administrar; no refrigerar')},
        [ix('Ciclosporina', 'Mayor nefrotoxicidad y menor nivel de ciclosporina', C('cotrimoxazol', '4.5')),
         ix('Antiarrítmicos (procainamida y otros)', 'Prolongación del QT', C('cotrimoxazol', '4.5'))],
        ea(['Náuseas', 'Exantema'], ['Reacciones cutáneas graves (Stevens-Johnson)', 'Hiperkalemia', 'Discrasias sanguíneas'], ['Piel', 'Potasio', 'Hemograma'], C('cotrimoxazol', '4.8; 4.4')),
        'fluconazol, linezolid y midazolam', tmin=60,
        alertas=['Dosis expresadas en trimetoprim (1 ampolla = 80 mg de trimetoprim + 400 mg de sulfametoxazol).'],
        discrepancias=[{'campo': 'presentación', 'valores': ['Iquique: ampolla 400/80 mg en 5 ml', 'CIMA (Soltrim): vial 800/160 mg'], 'decision': 'Presentación de Iquique; dosis de CIMA en trimetoprim.'}])

    F['fluconazol'] = polvo(
        'fluconazol', 'Fluconazol',
        [pres('fco-200mg-100ml', 'frasco listo para usar', 200, 'mg', 100, I('Fluconazol: 200 mg/100 ml'))], None, None,
        [], [], ['infusion_intermitente'], 'No requiere dilución. Infusión de 200 mg en 30 a 60 minutos.',
        [dosis('Candidiasis invasiva: carga el 1.er día', 'adulto', 'mg', C('fluconazol', '4.2: 800 mg el primer día'), mn=800, mx=800),
         dosis('Candidiasis invasiva: luego una vez al día', 'adulto', 'mg', C('fluconazol', '4.2: 400 mg una vez al día'), mn=400, mx=400),
         dosis('Candidiasis sistémica (28 días a 11 años), una vez al día (máx. 400 mg/día)', 'pediatrico', 'mg/kg/24 h', PED('fluconazol', '6–12 mg/kg/día'), mn=6, mx=12)],
        {'ambienteH': 24, 'fuente': I('Fluconazol: 24 h a temperatura ambiente en circuito cerrado')},
        [ix('Cisaprida y otros fármacos que prolongan el QT', 'Torsade de pointes; uso contraindicado', C('fluconazol', '4.5'))],
        ea(['Cefalea', 'Náuseas', 'Dolor abdominal'], ['Hepatotoxicidad', 'Prolongación del QT'], ['Función hepática'], C('fluconazol', '4.8; 4.4')),
        'anfotericina B, ampicilina, gluconato de calcio, cefotaxima, ceftazidima, ceftriaxona, clindamicina, cotrimoxazol, diazepam, furosemida, haloperidol, imipenem y piperacilina-tazobactam', tmin=30)

    F['aciclovir'] = polvo(
        'aciclovir', 'Aciclovir',
        [pres('amp-250mg-10ml', 'ampolla', 250, 'mg', 10, I('Aciclovir: 250 mg/10 ml'))], None, None,
        ['SF', 'SG5'], [dil('250 mg en 50 ml', 250, 'mg', 50, I('Aciclovir: 250 mg en 50 ml')), dil('500 mg en 100 ml', 500, 'mg', 100, I('Aciclovir: 500 mg en 100 ml')),
                        dil('750 mg en 250 ml', 750, 'mg', 250, I('Aciclovir: ≥ 750 mg en 250 ml'))],
        ['infusion_intermitente'], 'Perfusión lenta de 1 hora; nunca en bolo. Hidratar al paciente para reducir la nefrotoxicidad.',
        [dosis('Herpes simple o varicela-zóster (inmunocompetente), cada 8 h', 'adulto', 'mg/kg', C('aciclovir', '4.2: 5 mg/kg cada 8 h'), mn=5, mx=5),
         dosis('Encefalitis herpética o zóster en inmunodeprimido, cada 8 h', 'adulto', 'mg/kg', C('aciclovir', '4.2: 10 mg/kg cada 8 h'), mn=10, mx=10),
         dosis('Niños < 12 años: herpes simple o varicela (inmunocompetente), cada 8 h', 'pediatrico', 'mg/kg', C('aciclovir', '4.2: 10 mg/kg cada 8 h'), mn=10, mx=10),
         dosis('Encefalitis herpética (3 meses–12 años), cada 8 h', 'pediatrico', 'mg/kg', PED('aciclovir', '60 mg/kg/día cada 8 h (20 mg/kg/dosis)'), mn=20, mx=20)],
        {'fuente': I('Aciclovir: preparar y administrar; no refrigerar')},
        [ix('Probenecid y cimetidina', 'Aumentan la concentración de aciclovir', C('aciclovir', '4.5'))],
        ea(['Flebitis', 'Náuseas'], ['Insuficiencia renal (cristaluria)', 'Encefalopatía'], ['Hidratación y diuresis', 'Creatinina'], C('aciclovir', '4.8; 4.4')),
        'cefepime, ceftriaxona, dobutamina, dopamina, gentamicina, meropenem, metoclopramida, morfina, ondansetrón y piperacilina-tazobactam', tmin=60)

    F['linezolid'] = polvo(
        'linezolid', 'Linezolid',
        [pres('bolsa-600mg-300ml', 'bolsa lista para usar', 600, 'mg', 300, I('Linezolid: 600 mg/300 ml'))], None, None,
        [], [], ['infusion_intermitente'], 'No requiere dilución. Infusión de 2 horas (Iquique); CIMA: 30–120 min. Proteger de la luz.',
        [dosis('Cada 12 h (máx. 28 días)', 'adulto', 'mg', C('linezolid', '4.2.1: 600 mg dos veces al día'), mn=600, mx=600),
         dosis('Lactantes y niños, cada 8 h', 'pediatrico', 'mg/kg', PED('linezolid', '10 mg/kg/dosis cada 8 h'), mn=10, mx=10, tope=(600, 'mg'))],
        {'fuente': I('Linezolid: preparar y administrar')},
        [ix('IMAO y fármacos serotoninérgicos o adrenérgicos', 'Linezolid es IMAO: síndrome serotoninérgico o crisis hipertensiva', C('linezolid', '4.5'))],
        ea(['Diarrea', 'Cefalea', 'Náuseas'], ['Mielosupresión (uso > 2 semanas)', 'Neuropatía óptica y periférica', 'Acidosis láctica'], ['Hemograma semanal'], C('linezolid', '4.8; 4.4')),
        'anfotericina B, clorpromazina, diazepam, fenitoína y cotrimoxazol', proteger_luz=True,
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: no establecida en menores de 18 años', 'Pediamécum: 10 mg/kg cada 8 h'], 'decision': 'Se registra la de Pediamécum.'}])

    F['azitromicina'] = polvo(
        'azitromicina', 'Azitromicina',
        [pres('fa-500mg', 'frasco ampolla (polvo)', 500, 'mg', 5, I('Azitromicina: FA 500 mg'))], 5, 'agua bidestilada',
        ['SF', 'SG5'], [dil('500 mg en 250 ml (2 mg/ml)', 500, 'mg', 250, I('Azitromicina: 500 mg en 250 ml')), dil('500 mg en 500 ml (1 mg/ml)', 500, 'mg', 500, I('Azitromicina: 500 mg en 500 ml (3 h)'))],
        ['infusion_intermitente'], 'Infusión prolongada de 3 horas (Iquique); CIMA: al menos 60 minutos. Nunca en bolo ni IM.',
        [dosis('Neumonía adquirida en la comunidad, una vez al día', 'adulto', 'mg', C('azitromicina', '4.2: 500 mg una vez al día'), mn=500, mx=500)],
        {'ambienteH': 24, 'fuente': I('Azitromicina: reconstituida 24 h a temperatura ambiente')},
        [ix('Fármacos que prolongan el QT', 'Prolongación del QT y torsade de pointes', C('azitromicina', '4.4'))],
        ea(['Diarrea', 'Náuseas', 'Dolor en el sitio de infusión'], ['Prolongación del QT', 'Hepatotoxicidad'], ['ECG si hay riesgo de QT largo'], C('azitromicina', '4.8; 4.4')),
        'amikacina, cefotaxima, ceftazidima, ceftriaxona, ciprofloxacino, clindamicina, cloxacilina, gentamicina, fentanilo, furosemida, imipenem, ketorolaco, morfina, piperacilina-tazobactam y potasio', tmin=60,
        discrepancias=[{'campo': 'dosis pediátrica', 'valores': ['CIMA: seguridad IV no establecida en niños'], 'decision': 'Sin dosis pediátrica IV.'}])

    return F
