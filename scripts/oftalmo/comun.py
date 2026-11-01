"""Utilidades de los generadores de fichas oculares (pabellón oftalmológico).

Las fuentes se registran solas: cada cita (`cima`, `dm`, `ped`, `sefh_pnt`, `consenso`, `web`, `isp`) lee el crudo
en `datos/crudos/oftalmo/` y lo agrega a `FUENTES`. Así cada cita apunta a un archivo que existe y no hay ids de
fuente escritos a mano. Reglas: `datos/crudos/oftalmo/DECISIONES.md` y spec 2026-11-01-oftalmologia-design.md.
"""
import glob
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
CRUDOS = RAIZ / 'datos' / 'crudos' / 'oftalmo'
CONSULTA = '2026-10-31'

INST_CIMA = 'AEMPS — CIMA (España)'
INST_DM = 'U.S. National Library of Medicine — DailyMed (FDA)'
INST_PED = 'Asociación Española de Pediatría'
INST_ISP = 'Instituto de Salud Pública de Chile'
INST_SEFH = 'Sociedad Española de Farmacia Hospitalaria (SEFH)'

FUENTES = {}
ISP_REF = 'ISP-REGISTRO-OFTALMO'


def fu(ref, detalle):
    return {'ref': ref, 'detalle': detalle}


def _lineas(ruta):
    return Path(ruta).read_text(encoding='utf-8', errors='ignore').split('\n')


def _agregar(ref, titulo, institucion, url, anio):
    if ref not in FUENTES:
        FUENTES[ref] = {'id': ref, 'titulo': titulo, 'institucion': institucion, 'url': url, 'anio': anio, 'consultado': CONSULTA}


# ---------------------------------------------------------------- registro ISP

def _cargar_isp():
    codigos = {}
    for ruta in glob.glob(str(CRUDOS / 'isp*' / '*.json')):
        for fila in json.load(open(ruta, encoding='utf-8')):
            codigos[fila['Producto']] = fila['Nombre']
    return codigos


_ISP = _cargar_isp()


def isp(detalle):
    _agregar(ISP_REF, 'Registro sanitario de productos farmacéuticos (búsqueda por principio activo y por nombre)', INST_ISP,
             'https://registrosanitario.ispch.gob.cl/', 2026)
    return fu(ISP_REF, detalle)


def _verificar_registros(codigos):
    for c in codigos:
        if c not in _ISP:
            raise SystemExit(f'Registro ISP {c}: no aparece en datos/crudos/oftalmo/isp*/ (¿está vigente y bien escrito?)')


# ---------------------------------------------------------------- fuentes

def cima(slug, nreg, detalle):
    """Cita la ficha técnica CIMA `cima/<slug>__<via>__<nreg>.txt` (título en la línea 1, URL en la 2)."""
    archivos = glob.glob(str(CRUDOS / 'cima' / f'{slug}__*__{nreg}.txt'))
    if len(archivos) != 1:
        raise SystemExit(f'CIMA {slug} {nreg}: se esperaba 1 archivo, hay {len(archivos)}')
    ref = f'CIMA-OFT-{slug.upper()}-{nreg}'
    lineas = _lineas(archivos[0])
    _agregar(ref, f'Ficha técnica: {lineas[0].split(" | ")[0].strip()}', INST_CIMA, lineas[1].strip(), 2026)
    return fu(ref, detalle)


def dm(slug, detalle):
    """Cita la etiqueta de DailyMed `dailymed/<slug>.txt` (título en la línea 1, URL en la 2)."""
    ruta = CRUDOS / 'dailymed' / f'{slug}.txt'
    if not ruta.exists():
        raise SystemExit(f'DailyMed {slug}: no existe {ruta}')
    lineas = _lineas(ruta)
    ref = f'DAILYMED-OFT-{slug.upper()}'
    _agregar(ref, f'Etiqueta FDA (DailyMed): {lineas[0].strip()[:150]}', INST_DM, lineas[1].strip(), 2026)
    return fu(ref, detalle)


def ped(slug, detalle):
    """Cita Pediamécum `pediamecum/<slug>.txt` (URL en la línea 1, nombre en la 2 tras «Volver»)."""
    ruta = CRUDOS / 'pediamecum' / f'{slug}.txt'
    if not ruta.exists():
        raise SystemExit(f'Pediamécum {slug}: no existe {ruta}')
    url, nombre = [x.strip() for x in _lineas(ruta)[:2]]
    nombre = nombre.replace('Volver', '').strip() or slug
    ref = f'PEDIAMECUM-OFT-{slug.upper()}'
    _agregar(ref, f'Pediamécum: {nombre} (Dosis y pautas de administración)', INST_PED, url, 2026)
    return fu(ref, detalle)


def sefh_pnt(stem, detalle, enlace=None):
    """Cita un PNT de la SEFH `sefh/<stem>.txt`; la URL sale de `sefh/indice.html` y el año de «FECHA ÚLTIMA REVISIÓN».

    `enlace` solo si el PDF se llama distinto del .txt guardado (p. ej. CEFTAZIDIMA.txt ↔ CEFTAZIDIMA_2MG_01ML_…_PNT.pdf)."""
    ruta = CRUDOS / 'sefh' / f'{stem}.txt'
    if not ruta.exists():
        raise SystemExit(f'SEFH {stem}: no existe {ruta}')
    lineas = [x.strip() for x in _lineas(ruta)]
    titulo = next(x for x in lineas if x)
    indice = (CRUDOS / 'sefh' / 'indice.html').read_text(encoding='utf-8', errors='ignore')
    m = re.search(rf'href="([^"]*{re.escape(enlace or stem)}\.pdf)"', indice, re.I)
    if not m:
        raise SystemExit(f'SEFH {stem}: no hay enlace en sefh/indice.html')
    url = m.group(1)
    if url.startswith('/'):
        url = 'https://gruposdetrabajo.sefh.es' + url
    i = next((k for k, x in enumerate(lineas) if x.startswith('FECHA ÚLTIMA REVISIÓN')), None)
    anio = int(re.search(r'(20\d\d)', ' '.join(lineas[i:i + 3])).group(1)) if i is not None else None
    if anio is None:
        raise SystemExit(f'SEFH {stem}: no se encontró la fecha de revisión')
    ref = 'SEFH-PNT-' + re.sub(r'[^A-Z0-9]+', '-', stem.upper()).strip('-')
    _agregar(ref, f'PNT SEFH: {titulo}', INST_SEFH, url, anio)
    return fu(ref, detalle)


def consenso(detalle):
    """Consenso SEFH-SEO-SERV 2025 sobre preparaciones intraoculares (`sefh/consenso-2025.txt`)."""
    ref = 'CONSENSO-SEFH-SEO-SERV-2025'
    _agregar(ref, 'Consenso sobre preparaciones de medicamentos intraoculares (Farm Hosp 2025;49:99-108)',
             'SERV, SEFH y SEO (Farmacia Hospitalaria)', 'https://doi.org/10.1016/j.farma.2024.11.010', 2025)
    return fu(ref, detalle)


def web(archivo, clave, institucion, detalle, anio=None):
    """Cita un bloque de `web/<archivo>.txt` (bloques separados por «---»: URL en la línea 1, referencia en la 2).

    `clave` es un trozo único de la URL del bloque (p. ej. «PMC12577578»). `anio` solo si la referencia no trae «AAAA;».
    """
    ruta = CRUDOS / 'web' / f'{archivo}.txt'
    bloques = [b.strip().split('\n') for b in ruta.read_text(encoding='utf-8').split('\n---\n')]
    hallados = [b for b in bloques if clave in b[0]]
    if len(hallados) != 1:
        raise SystemExit(f'web/{archivo}: la clave {clave} encontró {len(hallados)} bloques')
    url, cita = hallados[0][0].strip(), hallados[0][1].strip()
    m = re.search(r'\.\s*((?:19|20)\d\d);', cita)
    if not m and anio is None:
        raise SystemExit(f'web/{archivo} {clave}: no se pudo leer el año de la referencia; pásalo con anio=')
    ref = f'WEB-OFT-{archivo.upper()}-{clave.upper()}'
    _agregar(ref, re.split(r' \((?:Solo|Resumen|Texto)', cita)[0][:240], institucion, url, anio or int(m.group(1)))
    return fu(ref, detalle)


# ---------------------------------------------------------------- piezas de la ficha

def _sin_none(d):
    return {k: v for k, v in d.items() if v is not None}


def cant(valor, unidad):
    return {'valor': valor, 'unidad': unidad}


def final(valor, unidad, volumen_ml):
    return {'cantidad': cant(valor, unidad), 'volumenMl': volumen_ml}


def final_rango(minimo, maximo, unidad, volumen_ml):
    return {'cantidad': {'min': minimo, 'max': maximo, 'unidad': unidad}, 'volumenMl': volumen_ml}


def pres(id, forma, valor, unidad, fuente, *, volumen=None, isp_codigos=(), uso_directo=False, sin_conservantes=None, nota=None):
    _verificar_registros(isp_codigos)
    return _sin_none({
        'id': id, 'forma': forma, 'cantidad': cant(valor, unidad), 'volumenMl': volumen,
        'registrosIsp': list(isp_codigos), 'usoDirecto': uso_directo, 'sinConservantes': sin_conservantes,
        'nota': nota, 'fuente': fuente,
    })


def dosis(indicacion, via, texto, fin, fuente, *, estatus, poblacion='adulto', condicion=None, presentaciones=None, tambien=None):
    return _sin_none({
        'indicacion': indicacion, 'via': via, 'poblacion': poblacion, 'final': fin, 'texto': texto, 'estatus': estatus,
        'condicion': condicion, 'presentaciones': presentaciones, 'fuente': fuente, 'tambien': tambien,
    })


def reconstituir(diluyente, volumen_ml):
    return {'tipo': 'reconstituir', 'diluyente': diluyente, 'volumenMl': volumen_ml}


def diluir(tomar_ml, llevar_a_ml, diluyente):
    return {'tipo': 'diluir', 'tomarMl': tomar_ml, 'llevarAMl': llevar_a_ml, 'diluyente': diluyente}


def cargar(volumen_ml):
    return {'tipo': 'cargar', 'volumenMl': volumen_ml}


def texto(t):
    return {'tipo': 'texto', 'texto': t}


def protocolo(id, indice_dosis, titulo, partida, pasos, resultado, fuente):
    """`resultado` = (valor, unidad, volumen_ml) que deja la preparación; el esquema lo compara con la dosis final."""
    valor, unidad, vol = resultado
    return {'id': id, 'dosis': indice_dosis, 'titulo': titulo, 'partida': partida, 'pasos': pasos,
            'resultado': {'valor': valor, 'unidad': unidad, 'volumenMl': vol}, 'fuente': fuente}


def conserv(t, fuente, horas=None):
    return _sin_none({'texto': t, 'horas': horas, 'fuente': fuente})


def disc(campo, valores, mostrado, motivo):
    """`valores` = [(ref_de_fuente, valor_que_dice)]."""
    return {'campo': campo, 'valores': [{'fuente': f, 'valor': v} for f, v in valores], 'mostrado': mostrado, 'motivo': motivo}


def ficha(id, nombre, grupo, familias, presentaciones, dosis_, *, modo='intraocular', comerciales=(), componentes=(),
          registro='verificado', protocolos=(), sin_pauta=None, pediatria, conservacion=(), contraindicaciones=(),
          alertas=(), discrepancias=()):
    """`pediatria` = (estado, motivo)."""
    return {
        'id': id, 'nombre': nombre, 'comerciales': list(comerciales), 'grupo': grupo, 'familias': list(familias),
        'modo': modo, 'componentes': list(componentes), 'altoRiesgo': True, 'registroChile': registro,
        'presentaciones': presentaciones, 'dosis': dosis_, 'protocolos': list(protocolos),
        'sinPauta': {'motivo': sin_pauta} if sin_pauta else None,
        'pediatria': {'estado': pediatria[0], 'motivo': pediatria[1]},
        'conservacion': list(conservacion), 'contraindicaciones': list(contraindicaciones), 'alertas': list(alertas),
        'discrepancias': list(discrepancias), 'meta': {},
    }
