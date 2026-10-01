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
