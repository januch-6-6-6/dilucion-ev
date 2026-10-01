"""Utilidades comunes de los generadores de fichas."""
CONSULTA = '2026-10-01'


def fu(ref, detalle):
    return {'ref': ref, 'detalle': detalle}


def meta(discrepancias=()):
    return {'discrepancias': list(discrepancias)}


def ajustar(lista, con, estado, fuente):
    for c in lista:
        if c['con'] == con:
            c['estado'], c['fuente'] = estado, fuente


P = lambda d: fu('PUCON-2022', d)  # noqa: E731
C = lambda k, d: fu(f'CIMA-{k.upper()}', d)  # noqa: E731
PED = lambda k, d: fu(f'PEDIAMECUM-{k.upper()}', d)  # noqa: E731


def fuente_cima(k, nreg, nombre, anio=2026):
    return {
        'id': f'CIMA-{k.upper()}',
        'titulo': f'Ficha técnica: {nombre}',
        'institucion': 'AEMPS — CIMA (España)',
        'url': f'https://cima.aemps.es/cima/dochtml/ft/{nreg}/FT_{nreg}.html',
        'anio': anio,
        'consultado': CONSULTA,
    }


def fuente_pediamecum(k, nombre=None):
    return {
        'id': f'PEDIAMECUM-{k.upper()}',
        'titulo': f'Pediamécum: {nombre or k.capitalize()} (Dosis y pautas de administración)',
        'institucion': 'Asociación Española de Pediatría',
        'url': f'https://www.aeped.es/comite-medicamentos/pediamecum/{k}',
        'anio': 2026,
        'consultado': CONSULTA,
    }


# --- Compatibilidad en Y desde la matriz Stabilis global ---
STABILIS = {
    'adenosina': 'Adenosin', 'amiodarona': 'Amiodarone hydrochloride', 'atropina': 'Atropine sulfate',
    'adrenalina': 'Epinephrine hydrochloride', 'fentanilo': 'Fentanyl citrate', 'ketamina': 'Ketamine hydrochloride',
    'sulfato-de-magnesio': 'Magnesium sulfate', 'midazolam': 'Midazolam hydrochloride', 'morfina': 'Morphine hydrochloride',
    'noradrenalina': 'Norepinephrine bitartrate', 'dopamina': 'Dopamine hydrochloride', 'dobutamina': 'Dobutamine hydrochloride',
    'fenilefrina': 'Phenylephrine hydrochloride', 'nitroglicerina': 'Nitroglycerin', 'labetalol': 'Labetalol hydrochloride',
    'lidocaina': 'Lidocaine hydrochloride', 'furosemida': 'Furosemide', 'metoclopramida': 'Metoclopramide hydrochloride',
    'ondansetron': 'Ondansetron hydrochloride', 'ketorolaco': 'Ketorolac tromethamine', 'tramadol': 'Tramadol hydrochloride',
    'metamizol': 'Metamizol sodium', 'hidrocortisona': 'Hydrocortisone sodium succinate', 'dexametasona': 'Dexamethasone sodium phosphate',
    'metilprednisolona': 'Methylprednisolone sodium succinate', 'fenitoina': 'Phenytoin sodium', 'levetiracetam': 'Levetiracetam',
    'diazepam': 'Diazepam', 'naloxona': 'Naloxone hydrochloride', 'flumazenil': 'Flumazenil', 'acido-tranexamico': 'Tranexamic acid',
    'heparina': 'Heparin sodium', 'insulina-cristalina': 'Insulin', 'cloruro-de-potasio': 'Potassium chloride',
    'bicarbonato-de-sodio': 'Sodium bicarbonate', 'gluconato-de-calcio': 'Calcium gluconate', 'propofol': 'Propofol',
    'etomidato': 'Etomidate', 'rocuronio': 'Rocuronium bromide', 'succinilcolina': 'Suxamethonium chloride',
    'cefazolina': 'Cefazolin sodium', 'ceftriaxona': 'Ceftriaxone disodium', 'cefotaxima': 'Cefotaxime sodium', 'ceftazidima': 'Ceftazidime',
    'cefepime': 'Cefepime dihydrochloride', 'ampicilina': 'Ampicillin sodium', 'ampicilina-sulbactam': 'Ampicillin sodium - sulbactam sodium',
    'cloxacilina': 'Cloxacillin sodium', 'penicilina-g-sodica': 'Penicillin G sodium', 'piperacilina-tazobactam': 'Piperacillin sodium / tazobactam',
    'imipenem': 'Imipenem - cilastatin sodium', 'meropenem': 'Meropenem', 'ertapenem': 'Ertapenem', 'vancomicina': 'Vancomycin hydrochloride',
    'clindamicina': 'Clindamycin phosphate', 'metronidazol': 'Metronidazole', 'gentamicina': 'Gentamicin sulfate', 'amikacina': 'Amikacin sulfate',
    'ciprofloxacino': 'Ciprofloxacin lactate', 'levofloxacino': 'Levofloxacine', 'fluconazol': 'Fluconazole', 'aciclovir': 'Aciclovir sodium',
    'linezolid': 'Linezolid', 'azitromicina': 'Azithromycine', 'omeprazol': 'Omeprazole sodium', 'paracetamol': 'Paracetamol',
    'ketoprofeno': 'Ketoprofene', 'dexmedetomidina': 'Dexmedetomidine', 'remifentanilo': 'Remifentanil hydrochloride',
    'cisatracurio': 'Cisatracurium besylate', 'vecuronio': 'Vecuronium bromide', 'haloperidol': 'Haloperidol lactate', 'digoxina': 'Digoxin',
    'manitol': 'Mannitol', 'fitomenadiona': 'Phytomenadione', 'tiamina': 'Thiamine hydrochloride', 'octreotido': 'Octreotide acetate',
    'fosfato-de-potasio': 'Potassium phosphate', 'acetilcisteina': 'N-acetylcysteine', 'neostigmina': 'Neostigmine methylsulfate',
    'esmolol': 'Esmolol hydrochloride', 'enalaprilato': 'Enalaprilate', 'nimodipino': 'Nimodipine', 'metoprolol': 'Metoprolol tartrate',
}
SOLVENTE = {'SF': 'Chlorure de sodium 0,9%', 'SG5': 'Glucose 5%'}
_ST = lambda d: fu('STABILIS-Y', d)  # noqa: E731
_CASILLA = {
    'G': ('compatible', 'Compatibilidad física en Y (casilla verde)'),
    'R': ('incompatible', 'Incompatibilidad en Y (casilla roja)'),
    'Y': ('incompatible', 'Datos contradictorios en la literatura (casilla amarilla); se registra como incompatible por criterio conservador'),
    '.': ('sin_datos', 'Sin datos de compatibilidad (casilla blanca)'),
}

# Incompatibilidades declaradas en la ficha técnica (6.2) o FDA que mandan sobre Stabilis (simétricas).
AJUSTES = [
    ('morfina', 'sulfato-de-magnesio', fu('CIMA-MORFINA', '6.2: incompatible con sales de magnesio')),
    ('dopamina', 'bicarbonato-de-sodio', fu('CIMA-DOPAMINA', '6.2: no añadir a soluciones alcalinas como bicarbonato sódico')),
    *[('dobutamina', x, fu('CIMA-DOBUTAMINA', '6.2: incompatible o no administrar por la misma línea'))
      for x in ['bicarbonato-de-sodio', 'furosemida', 'fenitoina', 'heparina', 'hidrocortisona', 'cefazolina']],
    ('labetalol', 'bicarbonato-de-sodio', fu('CIMA-LABETALOL', '6.2: incompatible con bicarbonato sódico 4,2 %')),
    ('metoclopramida', 'bicarbonato-de-sodio', fu('CIMA-METOCLOPRAMIDA', '6.2: incompatible con bicarbonato sódico')),
    *[('tramadol', x, fu('CIMA-TRAMADOL', '6.2: incompatible (inmiscible)')) for x in ['diazepam', 'midazolam', 'nitroglicerina']],
    ('ceftriaxona', 'gluconato-de-calcio', fu('FDA-GLUCONATO-CALCIO', '2.5: no mezclar con ceftriaxona (precipitado)')),
]


def compat_desde_matriz(matriz, id_, ids):
    """Entradas de compatibilidad de id_ contra SF, SG5 y cada id de ids (excepto sí mismo)."""
    fila = matriz.get(STABILIS.get(id_, ''))
    res = []
    for con in ['SF', 'SG5', *sorted(i for i in ids if i != id_)]:
        col = SOLVENTE.get(con) or STABILIS.get(con)
        if fila is None or col is None:
            quien = id_ if fila is None else con
            res.append({'con': con, 'estado': 'sin_datos', 'fuente': _ST(f'Sin datos: {quien} no figura en Stabilis')})
            continue
        estado, detalle = _CASILLA[fila[col]]
        res.append({'con': con, 'estado': estado, 'fuente': _ST(detalle)})
    for a, b, fuente in AJUSTES:
        if id_ in (a, b):
            otro = b if id_ == a else a
            for c in res:
                if c['con'] == otro:
                    c['estado'], c['fuente'] = 'incompatible', fuente
    return res
