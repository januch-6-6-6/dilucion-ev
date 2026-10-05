"""Utilidades de los generadores de fichas orales (sección «Orales»)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fichas.comun import fu  # noqa: E402,F401

CONSULTA = '2026-10-05'
CIMA_INSTITUCION = 'AEMPS — CIMA (España)'
PEDIAMECUM_INSTITUCION = 'Asociación Española de Pediatría'


def _cantidad(valor, unidad='mg'):
    return {'valor': valor, 'unidad': unidad}


def pres(id, forma, *, mg=None, mg_ml=None, gotas_por_ml=None, partible='no', retard=False, elemental=None,
         fuente, registro_chile='sin_verificar'):
    """Presentación oral. `mg` = por unidad (sólidos); `mg_ml` = por 1 ml (líquidos)."""
    p = {'id': id, 'forma': forma}
    if mg is not None:
        p['cantidad'] = _cantidad(mg)
    if mg_ml is not None:
        p['concentracion'] = _cantidad(mg_ml)
    if gotas_por_ml is not None:
        p['gotasPorMl'] = gotas_por_ml
    p['partible'] = partible
    p['liberacionProlongada'] = retard
    if elemental is not None:
        p['elemental'] = elemental
    p['registroChile'] = registro_chile
    p['fuente'] = fuente
    return p


def dosis(indicacion, poblacion, regimen, unidad, *, base=None, min=None, max=None, tomas=None, intervalo_h=None,
          tope_toma=None, tope_dia=None, estatus='autorizada', condicion=None, texto=None, fuente):
    """Dosis oral. `tope_toma`/`tope_dia` = (valor, unidad) o None."""
    d = {'indicacion': indicacion, 'poblacion': poblacion, 'regimen': regimen}
    if base is not None:
        d['base'] = base
    d['unidad'] = unidad
    for k, v in (('min', min), ('max', max), ('tomasPorDia', tomas), ('intervaloH', intervalo_h)):
        if v is not None:
            d[k] = v
    if tope_toma is not None:
        d['topePorToma'] = _cantidad(*tope_toma)
    if tope_dia is not None:
        d['topeDiario'] = _cantidad(*tope_dia)
    d['estatus'] = estatus
    if condicion is not None:
        d['condicion'] = condicion
    if texto is not None:
        d['texto'] = texto
    d['fuente'] = fuente
    return d


def discrepancia(campo, valores, mostrado, motivo):
    """`valores` = lista de (ref_fuente, texto)."""
    return {'campo': campo, 'valores': [{'fuente': r, 'valor': t} for r, t in valores], 'mostrado': mostrado, 'motivo': motivo}


def ficha_oral(id, nombre, grupo, presentaciones, dosis, administracion, *, comerciales=(), alto_riesgo=False,
               pediatria='con_dosis', motivo_solo_adulto=None, discrepancias=(), renal=None, hepatico=None,
               fuente_ajuste=None, alertas=()):
    ped = {'estado': pediatria}
    if motivo_solo_adulto:
        ped['motivo'] = motivo_solo_adulto
    ajuste = None
    if renal or hepatico:
        ajuste = {}
        if renal:
            ajuste['renal'] = renal
        if hepatico:
            ajuste['hepatico'] = hepatico
        ajuste['fuente'] = fuente_ajuste
    return {
        'id': id,
        'nombre': nombre,
        'comerciales': list(comerciales),
        'grupo': grupo,
        'ambitos': ['aps'],
        'altoRiesgo': alto_riesgo,
        'presentaciones': list(presentaciones),
        'dosis': list(dosis),
        'pediatria': ped,
        'discrepancias': list(discrepancias),
        'administracion': administracion,
        'ajusteRenalHepatico': ajuste,
        'alertas': list(alertas),
        'meta': {},
    }


def fuente_cima(k, nreg, nombre, *, varios=False, anio=2026):
    """Id `CIMA-<K>` o `CIMA-<K>-<NREG>` si el fármaco tiene varios productos."""
    sufijo = f'-{nreg}' if varios else ''
    return {
        'id': f'CIMA-{k.upper()}{sufijo}',
        'titulo': f'Ficha técnica: {nombre}',
        'institucion': CIMA_INSTITUCION,
        'url': f'https://cima.aemps.es/cima/dochtml/ft/{nreg}/FT_{nreg}.html',
        'anio': anio,
        'consultado': CONSULTA,
    }


def fuente_pediamecum_oral(k, nombre=None, anio=None, slug=None):
    """`slug` = nombre del archivo en datos/crudos/orales/pediamecum/ (por defecto k)."""
    return {
        'id': f'PEDIAMECUM-{k.upper()}',
        'titulo': f'Pediamécum: {nombre or k.capitalize()} (Dosis y pautas de administración)',
        'institucion': PEDIAMECUM_INSTITUCION,
        'url': f'https://www.aeped.es/comites/cm/pediamecum/principios-activos/{slug or k}',
        'anio': anio or 2026,
        'consultado': CONSULTA,
    }


def fuente_externa(id, titulo, institucion, url, anio):
    return {'id': id, 'titulo': titulo, 'institucion': institucion, 'url': url, 'anio': anio, 'consultado': CONSULTA}


ARSENAL = 'ARSENAL-APS-ATACAMA'


def fuente_arsenal():
    """Arsenal farmacoterapéutico de APS de Atacama (datos/crudos/orales/arsenal-atacama-2026-08-12.txt).

    La URL se arma con el número de edición (44.523) y el CVE (2850499) que figuran en el propio texto.
    """
    return fuente_externa(
        ARSENAL,
        'Arsenal farmacoterapéutico básico de APS, Región de Atacama (Res. exenta CP16.328; Diario Oficial 12-ago-2026, CVE 2850499)',
        'Servicio de Salud Atacama',
        'https://www.diariooficial.interior.gob.cl/publicaciones/2026/08/12/44523/01/2850499.pdf',
        2026,
    )
