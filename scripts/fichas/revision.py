"""Decisiones de la revisión clínica v0.2 (Héctor Salvo Agüero, TENS, 2026-10-02).

Se aplican sobre las fichas ya generadas para que cada cambio quede en un solo lugar y sea auditable.
El detalle de cada decisión está en informes/v0.2-decisiones-revision.md. Las fichas NO se firman
(meta.revisadoPor queda vacío): la revisión del autor no reemplaza la validación de un químico farmacéutico.
"""
from .comun import CONSULTA, fu
from .tanda1b import dil, dosis, pres

FECHA = '2026-10-02'
QUIEN = f'Revisión clínica (Héctor Salvo Agüero, TENS, {FECHA})'
REV = lambda d: fu('REVISION-CLINICA-2026-10-02', d)  # noqa: E731

TOPE_ESTIMADO = 'tope = dosis de adulto en 70 kg aceptado; la app lo muestra como «calculado, no de fuente».'


def fuentes():
    return [
        {
            'id': 'REVISION-CLINICA-2026-10-02',
            'titulo': 'Revisión clínica v0.2: decisiones documentadas (confirmación por experiencia clínica, no por fuente publicada)',
            'institucion': 'Héctor Salvo Agüero, TENS (autor); no reemplaza la validación de un químico farmacéutico',
            'url': 'https://github.com/januch-6-6-6/dilucion-ev/blob/main/informes/v0.2-decisiones-revision.md',
            'anio': 2026,
            'consultado': FECHA,
        },
        {
            'id': 'FDA-SOLU-CORTEF',
            'titulo': 'Solu-Cortef (hydrocortisone sodium succinate) — Prescribing information (Dosage and administration)',
            'institucion': 'U.S. FDA / DailyMed',
            'url': 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=65eefd58-b166-4d71-ade6-45c8fdf86922',
            'anio': 2026,
            'consultado': FECHA,
        },
        {
            'id': 'ADA-CRISIS-HIPERGLICEMICAS-2024',
            'titulo': 'Hyperglycemic Crises in Adults With Diabetes: A Consensus Report (Diabetes Care 2024;47(8):1257–1275)',
            'institucion': 'ADA, EASD, JBDS, AACE y DTS',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11272983/',
            'anio': 2024,
            'consultado': FECHA,
        },
        {
            'id': 'UKKA-HIPERKALEMIA-2026',
            'titulo': 'Clinical Practice Guideline: Management of Hyperkalaemia in Adults (actualizada julio 2026)',
            'institucion': 'UK Kidney Association',
            'url': 'https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf',
            'anio': 2026,
            'consultado': FECHA,
        },
        {
            'id': 'ESETT-2019',
            'titulo': 'Randomized Trial of Three Anticonvulsant Medications for Status Epilepticus (ESETT; N Engl J Med 2019;381:2103–2113)',
            'institucion': 'Kapur J, et al. — NINDS / NETT, PECARN',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7098487/',
            'anio': 2019,
            'consultado': FECHA,
        },
    ]


def _decidir(f, campo, texto):
    """Agrega la decisión de la revisión a la discrepancia cuyo campo empieza con `campo`."""
    hits = [d for d in f['meta']['discrepancias'] if d['campo'].startswith(campo)]
    assert hits, f"{f['id']}: no hay discrepancia «{campo}»"
    for d in hits:
        d['decision'] = d['decision'].replace(' REVISAR PRIMERO.', '').replace('REVISAR PRIMERO.', '').strip()
        d['decision'] += f' {QUIEN}: {texto}'


def _dosis(f, indicacion_inicio):
    hits = [d for d in f['dosis'] if d['indicacion'].startswith(indicacion_inicio)]
    assert len(hits) == 1, f"{f['id']}: dosis «{indicacion_inicio}» encontrada {len(hits)} veces"
    return hits[0]


def aplicar(F):
    # --- Bloque 1: vías fuera de ficha técnica y pediatría ---
    f = F['haloperidol']
    f['alertas'] = ['Uso EV fuera de ficha técnica (en CIMA solo IM): riesgo de QT largo y torsade de pointes; monitorizar ECG.']
    _decidir(f, 'vía', 'se mantiene la vía EV de Pucón, con alerta de QT largo y monitorización ECG.')

    _decidir(F['ketoprofeno'], 'vía', 'se mantiene la infusión EV de Pucón, con la alerta de que la ficha española no la autoriza.')
    _decidir(F['ketorolaco'], 'dosis pediátrica', 'se mantiene la pauta de Pediamécum rotulada «fuera de ficha técnica».')

    f = F['naloxona']
    _dosis(f, 'Depresión por opioides (niños)')['indicacion'] = 'Depresión respiratoria postoperatoria por opioides (niños), cada 2–3 min'
    f['dosis'].append(dosis('Intoxicación por opioides / reversión total (niños, pauta PALS)', 'pediatrico', 'mg/kg',
                            fu('PEDIAMECUM-NALOXONA', 'PALS: 0,1 mg/kg hasta 2 mg en reversión total'), mn=0.1, mx=0.1, tope=(2, 'mg')))
    _decidir(f, 'dosis pediátrica', 'se muestran ambas pautas, cada una con su indicación.')

    # --- Bloque 2: topes calculados y presentaciones ---
    for k in ['cisatracurio', 'fenitoina', 'lidocaina', 'propofol', 'rocuronio', 'manitol', 'heparina', 'bicarbonato-de-sodio']:
        _decidir(F[k], next(d['campo'] for d in F[k]['meta']['discrepancias'] if 'tope' in d['campo']), TOPE_ESTIMADO)
    _decidir(F['fenilefrina'], 'dosis pediátrica', TOPE_ESTIMADO + ' Pauta pediátrica de Pediamécum aceptada.')
    _decidir(F['vecuronio'], 'fuente y reconstitución', 'reconstitución con 10 ml (1 mg/ml) confirmada por experiencia clínica; ' + TOPE_ESTIMADO)

    f = F['glucosa-30']
    f['presentaciones'] = [pres('amp-30pct-20ml', 'ampolla 30 % (20 ml)', 6, 'g', 20,
                                REV('Ampolla de 20 ml al 30 % (6 g), la habitual en Chile'))]
    _decidir(f, 'presentación', 'se usa la ampolla de 20 ml al 30 % (6 g).')

    _decidir(F['furosemida'], 'presentación', 'ampolla de 20 mg/2 ml (10 mg/ml) confirmada.')

    # --- Bloque 3: presentaciones locales y dosis de hidrocortisona ---
    f = F['metamizol']
    f['presentaciones'] = [pres('amp-1g-2ml', 'ampolla', 1, 'g', 2, REV('Ampolla de 1 g/2 ml (500 mg/ml); Pucón: ampolla de 1 g'))]
    _decidir(f, 'presentación', 'ampolla de 1 g/2 ml (500 mg/ml).')

    _decidir(F['bicarbonato-de-sodio'], 'fuente chilena / tope pediátrico', 'ampolla de 10 ml (10 mEq) confirmada.')

    f = F['manitol']
    f['presentaciones'].append(pres('fco-20pct-500ml', 'frasco 20 % (500 ml)', 100, 'g', 500, REV('Frasco de 500 ml al 20 % (100 g), además del de 250 ml')))
    _decidir(f, 'tope pediátrico y presentación', 'se usan ambos frascos, 250 ml (50 g) y 500 ml (100 g).')

    f = F['hidrocortisona']
    f['dosis'] = [d for d in f['dosis'] if d['poblacion'] != 'adulto']
    f['dosis'].insert(0, dosis('Dosis inicial (crisis suprarrenal: 100 mg EV en bolo), repetible cada 2, 4 o 6 h', 'adulto', 'mg',
                               fu('FDA-SOLU-CORTEF', 'Dosage and administration: dosis inicial de 100 a 500 mg según la indicación; repetible cada 2, 4 o 6 h'),
                               mn=100, mx=500))
    _decidir(f, 'presentación y dosis adulto', 'se reemplaza la dosis de la otra sal (CIMA) por la de succinato de FDA (Solu-Cortef), 100 mg EV en crisis suprarrenal.')

    # --- Bloque 4: reglas pediátricas, fichas sin dosis y decisiones conservadoras ---
    for k in ['amiodarona', 'dopamina', 'linezolid']:
        _decidir(F[k], 'dosis pediátrica', 'se acepta la pauta de Pediamécum con la advertencia de la ficha técnica visible.')
    _decidir(F['clorfenamina'], 'dosis', 'queda sin dosis (solo preparación y compatibilidad).')

    f = F['insulina-cristalina']
    f['dosis'] += [
        dosis('Cetoacidosis diabética: infusión de tasa fija', 'adulto', 'UI/kg/h',
              fu('ADA-CRISIS-HIPERGLICEMICAS-2024', 'Insulin therapy: fixed-rate intravenous insulin infusion started at 0.1 units/kg/h'), mn=0.1, mx=0.1),
        dosis('Cetoacidosis: al bajar la glicemia de 250 mg/dl (agregar dextrosa 5–10 %)', 'adulto', 'UI/kg/h',
              fu('ADA-CRISIS-HIPERGLICEMICAS-2024', 'reduce the insulin infusion rate to 0.05 units/kg/h'), mn=0.05, mx=0.05),
        dosis('Hiperkalemia: 10 UI en 25 g de glucosa EV en 15–30 min (controlar glicemia)', 'adulto', 'UI',
              fu('UKKA-HIPERKALEMIA-2026', '10 units soluble insulin in 25 g glucose by intravenous infusion over 15–30 min'), mn=10, mx=10),
    ]
    _decidir(f, 'dosis EV', 'se agregan las dosis EV de cetoacidosis (ADA 2024) e hiperkalemia (UKKA 2026); fuentes extranjeras.')

    f = F['levetiracetam']
    f['dosis'] += [
        dosis('Status epiléptico refractario a benzodiacepinas: carga única en 10 min (máx. 4500 mg)', 'adulto', 'mg/kg',
              fu('ESETT-2019', 'levetiracetam 60 mg per kilogram (maximum, 4500 mg), infused over 10 minutes'), mn=60, mx=60),
        dosis('Status epiléptico refractario a benzodiacepinas (≥ 2 años): carga única en 10 min', 'pediatrico', 'mg/kg',
              fu('ESETT-2019', 'levetiracetam 60 mg per kilogram (maximum, 4500 mg); pacientes de 2 años o más'), mn=60, mx=60, tope=(4500, 'mg')),
    ]
    _decidir(f, 'fuente chilena / status epiléptico', 'se agrega la carga de status de ESETT (NEJM 2019), fuente extranjera.')

    _decidir(F['cloruro-de-potasio'], 'dosis pediátrica', 'la búsqueda no encontró fuente citable (FDA: no usar en niños); sigue «protocolo local».')
    for k in ['cloruro-de-sodio-10', 'cloruro-de-sodio-3']:
        _decidir(F[k], F[k]['meta']['discrepancias'][0]['campo'], 'la búsqueda no encontró una fuente chilena citable; sigue sin dosis.')

    for k, campo in [('omeprazol', 'dilución'), ('morfina', 'compatibilidad'), ('ketamina', 'estabilidad'),
                     ('vancomicina', 'concentración'), ('furosemida', 'suero'), ('fosfato-de-potasio', 'concentración máxima')]:
        _decidir(F[k], campo, 'criterio conservador aprobado.')

    # --- Bloque 5: presentaciones y antibióticos ---
    _decidir(F['metilprednisolona'], 'fuente chilena', 'viales de 40, 125, 500 y 1000 mg confirmados; solo se registran 20 y 40 mg porque no hay fuente para el volumen de reconstitución de los demás.')
    _decidir(F['cotrimoxazol'], 'presentación', 'ampolla de 400/80 mg en 5 ml confirmada.')
    _decidir(F['metoprolol'], 'presentación y pediatría', 'ampolla de 5 mg/5 ml NO confirmada: verificar el rotulado local.')

    f = F['remifentanilo']
    c = lambda d: fu('CIMA-REMIFENTANILO', d)  # noqa: E731
    f['presentaciones'] = [
        pres('fa-2mg', 'frasco ampolla (polvo)', 2, 'mg', 2, REV('Vial de 2 mg (en Chile); CIMA: 1 mg/ml tras reconstituir')),
        pres('fa-5mg', 'frasco ampolla (polvo)', 5, 'mg', 5, REV('Vial de 5 mg (en Chile); CIMA: 1 mg/ml tras reconstituir')),
    ]
    f['reconstitucion'] = {'diluyente': 'Agua para inyectables o suero, 1 ml por cada mg (vial de 2 mg; el de 5 mg lleva 5 ml)', 'volumenMl': 2,
                           'fuente': c('2: cada ml reconstituido contiene 1 mg')}
    f['dilucion']['estandar'] = [
        dil('2 mg en 40 ml (50 mcg/ml, recomendada en adultos)', 2, 'mg', 40, c('4.2: 50 mcg/ml es la dilución recomendada para adultos')),
        dil('5 mg en 100 ml (50 mcg/ml, recomendada en adultos)', 5, 'mg', 100, c('4.2: 50 mcg/ml es la dilución recomendada para adultos')),
    ]
    _decidir(f, 'dosis pediátrica y presentación', 'viales de 2 y 5 mg (los de Chile); la dilución estándar se mantiene en 50 mcg/ml.')

    for k, campo in [('ampicilina', 'fuente de dosis'), ('ceftriaxona', 'concentración'), ('cloxacilina', 'reconstitución'), ('meropenem', 'reconstitución')]:
        _decidir(F[k], campo, 'aprobado; revisar con el protocolo local.')

    assert CONSULTA  # la fecha de consulta de las fuentes originales no cambia
