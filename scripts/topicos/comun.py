"""Utilidades de los generadores de fichas tópicas (ojo, oído y nariz).

Las fuentes se registran solas: cada referencia (`cima`, `dm`, `ped`, `isp`) lee la cabecera del crudo en
`datos/crudos/topicos/` (título en la línea 1, URL en la línea 2) y la agrega a `FUENTES`. Así cada cita
apunta a un archivo que existe y no hay ids de fuente escritos a mano.

Reglas de datos (decisiones de Héctor, 31-oct-2026; `datos/crudos/topicos/DECISIONES.md`):
1. Fuente única: se publica con aviso (la app lo calcula por instituciones distintas en las pautas).
2. La ficha se ata a la concentración registrada en el ISP; una pauta de otra concentración va a `discrepancias`.
3. Combinaciones solo chilenas sin fuente de la combinación: `sin_pauta` con motivo, sin dosis.
4. Pediatría no autorizada en la ficha técnica pero con pauta en Pediamécum: ambas, Pediamécum como off-label.
"""
import glob
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
CRUDOS = RAIZ / 'datos' / 'crudos' / 'topicos'
CONSULTA = '2026-10-30'

INST_CIMA = 'AEMPS — CIMA (España)'
INST_DM = 'U.S. National Library of Medicine — DailyMed (FDA)'
INST_PED = 'Asociación Española de Pediatría'
INST_ISP = 'Instituto de Salud Pública de Chile'

FUENTES = {}
ISP_REF = 'ISP-REGISTRO-TOPICOS'
_ISP = {x['molecula']: x for x in json.load(open(CRUDOS / 'lista-isp.json', encoding='utf-8'))}


def fu(ref, detalle):
    return {'ref': ref, 'detalle': detalle}


def _cabecera(ruta):
    lineas = Path(ruta).read_text(encoding='utf-8', errors='ignore').split('\n')
    return lineas[0].strip(), lineas[1].strip()


def _anio(titulo):
    return 2026


def cima(slug, nreg, detalle):
    """Cita la ficha técnica CIMA `cima/<slug>__<via>__<nreg>.txt`."""
    archivos = glob.glob(str(CRUDOS / 'cima' / f'{slug}__*__{nreg}.txt'))
    if len(archivos) != 1:
        raise SystemExit(f'CIMA {slug} {nreg}: se esperaba 1 archivo, hay {len(archivos)}')
    ref = f'CIMA-TOP-{slug.upper()}-{nreg}'
    if ref not in FUENTES:
        titulo, url = _cabecera(archivos[0])
        FUENTES[ref] = {'id': ref, 'titulo': f'Ficha técnica: {titulo.split(" | ")[0]}', 'institucion': INST_CIMA,
                        'url': url, 'anio': 2026, 'consultado': CONSULTA}
    return fu(ref, detalle)


def dm(slug, detalle):
    """Cita la etiqueta de DailyMed `dailymed/<slug>.txt`."""
    ruta = CRUDOS / 'dailymed' / f'{slug}.txt'
    if not ruta.exists():
        raise SystemExit(f'DailyMed {slug}: no existe {ruta}')
    ref = f'DAILYMED-TOP-{slug.upper()}'
    if ref not in FUENTES:
        titulo, url = _cabecera(ruta)
        FUENTES[ref] = {'id': ref, 'titulo': f'Etiqueta FDA (DailyMed): {titulo[:150]}', 'institucion': INST_DM,
                        'url': url, 'anio': 2026, 'consultado': CONSULTA}
    return fu(ref, detalle)


def ped(slug, detalle):
    """Cita Pediamécum `pediamecum/<slug>.txt` (URL en la línea 1, nombre en la 2 tras «Volver»)."""
    ruta = CRUDOS / 'pediamecum' / f'{slug}.txt'
    if not ruta.exists():
        raise SystemExit(f'Pediamécum {slug}: no existe {ruta}')
    ref = f'PEDIAMECUM-TOP-{slug.upper()}'
    if ref not in FUENTES:
        url, nombre = _cabecera(ruta)
        nombre = nombre.replace('Volver', '').strip() or slug
        FUENTES[ref] = {'id': ref, 'titulo': f'Pediamécum: {nombre} (Dosis y pautas de administración)',
                        'institucion': INST_PED, 'url': url, 'anio': 2026, 'consultado': CONSULTA}
    return fu(ref, detalle)


def isp(detalle):
    if ISP_REF not in FUENTES:
        FUENTES[ISP_REF] = {
            'id': ISP_REF,
            'titulo': 'Registro sanitario de productos farmacéuticos (búsqueda por nombre: OFTÁLMICA, ÓTICA/ÓTICO, NASAL)',
            'institucion': INST_ISP, 'url': 'https://registrosanitario.ispch.gob.cl/', 'anio': 2026,
            'consultado': CONSULTA,
        }
    return fu(ISP_REF, detalle)


def registros(molecula):
    return _ISP[molecula]['registros']


# ---------------------------------------------------------------- piezas de la ficha

NC = 'concentración no indicada en el registro'


def _slug_conc(conc):
    if conc == NC:
        return 'sc'
    plano = ''.join(ch for ch in unicodedata.normalize('NFD', conc.lower()) if unicodedata.category(ch) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', plano.split(' por ')[0]).strip('-')[:40] or 'x'


FORMA_ISP = {
    'solucion': 'SOLUCI', 'suspension': 'SUSPENSI', 'emulsion': 'EMULSI', 'unguento': 'UNG', 'gel': 'GEL',
}


def pres(forma, concentracion, via, *codigos, unidosis=False, sin_conservantes=False, nota=None):
    """Presentación registrada en Chile. `codigos` = registros ISP (F-xxxx/aa) que la componen."""
    if not codigos:
        raise SystemExit(f'presentación {forma} {concentracion} sin registros ISP')
    p = {'forma': forma, 'via': via, 'concentracion': concentracion, 'registrosIsp': list(codigos)}
    if unidosis:
        p['unidosis'] = True
    if sin_conservantes:
        p['sinConservantes'] = True
    if nota:
        p['nota'] = nota
    return p


def dosis(indicacion, poblacion, texto, fuente, *, cantidad=None, unidad=None, veces_dia=None, sitio=None,
          duracion=None, estatus='autorizada', condicion=None, presentaciones=None, tambien=()):
    """Pauta. `cantidad`/`unidad`/`veces_dia`/`sitio` alimentan la calculadora de duración del envase
    (solo se ponen cuando la fuente da cifras fijas; con rango se usa el máximo y se dice en el texto).
    `tambien` = otras citas que dan la MISMA pauta (concordancia); cuentan para la verificación de fuentes."""
    d = {'indicacion': indicacion, 'poblacion': poblacion, 'texto': texto}
    if cantidad is not None:
        d['cantidad'] = cantidad
        d['unidad'] = unidad
    if veces_dia is not None:
        d['vecesAlDia'] = veces_dia
    if sitio is not None:
        d['porSitio'] = sitio
    if duracion:
        d['duracion'] = duracion
    d['estatus'] = estatus
    if condicion:
        d['condicion'] = condicion
    if presentaciones:
        d['presentaciones'] = list(presentaciones)
    d['fuente'] = fuente
    if tambien:
        d['tambien'] = list(tambien)
    return d


def disc(campo, valores, mostrado, motivo):
    """`valores` = lista de (ref, texto); ref es el id de fuente (usar `.ref` de una cita: c['ref'])."""
    return {'campo': campo, 'valores': [{'fuente': r, 'valor': t} for r, t in valores], 'mostrado': mostrado, 'motivo': motivo}


def conserv(texto, fuente, dias=None, presentaciones=None):
    """Conservación y validez tras abrir. `presentaciones` = ids a los que aplica (None = todas)."""
    c = {}
    if presentaciones:
        c['presentaciones'] = list(presentaciones)
    if dias is not None:
        c['validezAbiertoDias'] = dias
    c['texto'] = texto
    c['fuente'] = fuente
    return c


GENERICOS = re.compile(r'^(ACICLOVIR|ATROPINA|BIMATOPROST|BRIMONIDINA|BRINZOLAMIDA|CICLOPENTOLATO|CLORANFENICOL|DORZOLAMIDA|'
                       r'FENILEFRINA|GENTAMICINA|LATANOPROST|MOMETASONA|MOXIFLOXACINO|NAFAZOLINA|OLOPATADINA|PILOCARPINA|'
                       r'PREDNISOLONA|TIMOLOL|TOBRAMICINA|TRAVOPROST|TROPICAMIDA|BETAXOLOL)\b', re.I)
CORTE = re.compile(r'\s+(SOLUCI|SUSPENSI|UNG|GEL|EMULSI|SPRAY|SOLUCION)', re.I)


def comerciales_de(molecula):
    """Nombres de fantasía del ISP (sin los genéricos), en orden y sin repetir."""
    vistos = []
    for r in registros(molecula):
        nom = r['Nombre'].strip()
        if GENERICOS.match(nom) or '/' in nom.split(' ')[0]:
            continue
        m = CORTE.search(nom)
        corto = (nom[:m.start()] if m else nom).strip().title()
        if corto and corto not in vistos:
            vistos.append(corto)
    return vistos


def ficha(id, molecula, nombre, grupo, presentaciones, dosis_, *, componentes=None, pediatria, conservacion=None,
          administracion=None, contraindicaciones=(), alertas=(), discrepancias=(), sin_pauta=None,
          alto_riesgo=False, comerciales=None):
    """Arma la ficha y verifica que las presentaciones cubran exactamente los registros ISP de la molécula.

    `pediatria` = (estado, motivo) o (estado, motivo, edadMinima); estado ∈ con_dosis | no_establecida |
    contraindicada | sin_datos.
    """
    codigos_isp = {r['Producto'] for r in registros(molecula)}
    usados = [c for p in presentaciones for c in p['registrosIsp']]
    if sorted(usados) != sorted(codigos_isp):
        faltan = codigos_isp - set(usados)
        sobran = set(usados) - codigos_isp
        raise SystemExit(f'{id}: registros ISP no cuadran (faltan {sorted(faltan)}, sobran {sorted(sobran)}, '
                         f'repetidos {len(usados) - len(set(usados))})')
    nombres = {r['Producto']: r['Nombre'] for r in registros(molecula)}
    salida_pres = []
    for i, p in enumerate(presentaciones):
        clave = FORMA_ISP.get(p['forma'])
        for c in p['registrosIsp']:
            nom = nombres[c].upper()
            if clave and clave not in nom and not (p['forma'] == 'spray'):
                raise SystemExit(f'{id}: {c} «{nombres[c]}» no parece {p["forma"]}')
        pid = f"{p['via']}-{p['forma']}-{_slug_conc(p['concentracion'])}"
        if any(x['id'] == pid for x in salida_pres):
            pid = f'{pid}-{i}'
        detalle = '; '.join(f'{c} {nombres[c]}' for c in p['registrosIsp'])
        salida_pres.append({'id': pid, **p, 'fuente': isp(detalle)})
    ped_ = {'estado': pediatria[0], 'motivo': pediatria[1]}
    if len(pediatria) > 2 and pediatria[2]:
        ped_['edadMinima'] = pediatria[2]
    f = {
        'id': id,
        'nombre': nombre,
        'comerciales': comerciales if comerciales is not None else comerciales_de(molecula),
        'grupo': grupo,
        'vias': sorted({p['via'] for p in presentaciones}),
        'componentes': list(componentes) if componentes else [],
        'altoRiesgo': alto_riesgo,
        'presentaciones': salida_pres,
        'dosis': list(dosis_),
        'sinPauta': {'motivo': sin_pauta} if sin_pauta else None,
        'pediatria': ped_,
        'conservacion': ([] if conservacion is None else list(conservacion) if isinstance(conservacion, list) else [conservacion]),
        'administracion': administracion,
        'contraindicaciones': list(contraindicaciones),
        'alertas': list(alertas),
        'discrepancias': list(discrepancias),
        'meta': {},
    }
    return f


def slug_molecula(molecula):
    plano = ''.join(ch for ch in unicodedata.normalize('NFD', molecula.lower()) if unicodedata.category(ch) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', plano).strip('-')
