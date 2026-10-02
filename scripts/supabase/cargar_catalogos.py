"""Carga los catálogos de la comunidad en Supabase: establecimientos (DEIS) y medicamentos (fichas).

Uso: python3 scripts/supabase/cargar_catalogos.py --destino prueba|real [--deis archivo.csv]

Solo inserta o actualiza (upsert): nunca borra. Un establecimiento que desaparece del listado se marca
`vigente = false` (puede tener propuestas asociadas). Las credenciales salen de .env.supabase o del entorno.
"""
import argparse
import csv
import io
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
LOTE = 500
LOTE_PARCHE = 100
# Supabase rechaza (401) la clave secreta si la petición parece de un navegador: a Supabase va un agente neutro.
UA_SUPABASE = 'dilucion-ev-catalogos/1.0'
# datos.gob.cl, en cambio, bloquea a los clientes que no parecen navegador.
UA_DATOS = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36'
CKAN = 'https://datos.gob.cl/api/3/action/package_show?id=establecimientos-de-salud-vigentes'


def leer_deis(ruta):
    """Lee el CSV oficial del DEIS (UTF-8, separado por «;»)."""
    crudo = Path(ruta).read_bytes()
    try:
        texto = crudo.decode('utf-8-sig')
    except UnicodeDecodeError:
        texto = crudo.decode('latin-1')
    return list(csv.DictReader(io.StringIO(texto), delimiter=';'))


def filas_establecimientos(crudo):
    """Normaliza el listado DEIS: descarta filas sin código y deduplica por código (queda la primera)."""
    vistos, filas = set(), []
    for r in crudo:
        codigo = (r.get('EstablecimientoCodigo') or '').strip()
        if not codigo or codigo in vistos:
            continue
        vistos.add(codigo)
        filas.append({
            'codigo': codigo,
            'nombre': (r.get('EstablecimientoGlosa') or '').strip(),
            'tipo': (r.get('TipoEstablecimientoGlosa') or '').strip(),
            'comuna': (r.get('ComunaGlosa') or '').strip(),
            'region': (r.get('RegionGlosa') or '').strip(),
            'vigente': (r.get('EstadoFuncionamiento') or '').strip().lower().startswith('vigente'),
        })
    return filas


def filas_medicamentos(carpeta):
    return [{'id': yaml.safe_load(f.read_text(encoding='utf-8'))['id']} for f in sorted(Path(carpeta).glob('*.yaml'))]


def _http(metodo, url, clave, cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    cab = {'apikey': clave, 'Authorization': f'Bearer {clave}', 'Content-Type': 'application/json', 'User-Agent': UA_SUPABASE}
    if metodo in ('POST', 'PATCH'):
        cab['Prefer'] = 'resolution=merge-duplicates,return=minimal'
    peticion = urllib.request.Request(url, data=datos, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(peticion, timeout=60) as r:
            cuerpo_resp = r.read()
            return r.status, (json.loads(cuerpo_resp) if cuerpo_resp else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors='replace')[:300]


def subir(url, clave, tabla, filas, conflicto, http=_http):
    """Upsert por lotes. Devuelve cuántas filas envió."""
    for i in range(0, len(filas), LOTE):
        estado, resp = http('POST', f'{url}/rest/v1/{tabla}?on_conflict={conflicto}', clave, filas[i:i + LOTE])
        if estado >= 300:
            raise RuntimeError(f'{tabla}: HTTP {estado} {resp}')
    return len(filas)


def marcar_no_vigentes(url, clave, codigos_actuales, http=_http):
    """Marca vigente=false los establecimientos guardados que ya no vienen en el listado. Nunca borra.

    Ignora los de prueba (código PRUEBA-…). Devuelve cuántos marcó."""
    existentes, pagina = [], 1000
    while True:
        estado, filas = http('GET', f'{url}/rest/v1/establecimientos?select=codigo&vigente=eq.true&limit={pagina}&offset={len(existentes)}', clave)
        if estado >= 300:
            raise RuntimeError(f'establecimientos: HTTP {estado} {filas}')
        existentes += [f['codigo'] for f in filas]
        if len(filas) < pagina:
            break
    faltantes = sorted(c for c in existentes if c not in codigos_actuales and not c.startswith('PRUEBA-'))
    for i in range(0, len(faltantes), LOTE_PARCHE):
        lote = ','.join(faltantes[i:i + LOTE_PARCHE])
        estado, resp = http('PATCH', f'{url}/rest/v1/establecimientos?codigo=in.({urllib.parse.quote(lote, safe=",-")})', clave, {'vigente': False})
        if estado >= 300:
            raise RuntimeError(f'establecimientos: HTTP {estado} {resp}')
    return len(faltantes)


def _cargar_env():
    ruta = RAIZ / '.env.supabase'
    if ruta.exists():
        for linea in ruta.read_text().splitlines():
            if '=' in linea and not linea.startswith('#'):
                k, v = linea.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())


def _descargar_deis():
    """Baja el CSV vigente más reciente desde datos.gob.cl (CKAN) a un archivo temporal."""
    req = urllib.request.Request(CKAN, headers={'User-Agent': UA_DATOS})
    recursos = json.load(urllib.request.urlopen(req, timeout=60))['result']['resources']
    url = next(r['url'] for r in recursos if (r.get('format') or '').lower() == 'csv')
    destino = Path(tempfile.gettempdir()) / 'establecimientos_deis.csv'
    destino.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA_DATOS}), timeout=120).read())
    return destino


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--destino', choices=['prueba', 'real'], required=True)
    ap.add_argument('--deis', help='CSV del DEIS ya descargado (si no, se baja de datos.gob.cl)')
    args = ap.parse_args(argv)
    _cargar_env()
    n = args.destino.upper()
    url, clave = os.environ[f'SUPABASE_{n}_URL'], os.environ[f'SUPABASE_{n}_SERVICE_KEY']
    meds = filas_medicamentos(RAIZ / 'datos' / 'medicamentos')
    ests = filas_establecimientos(leer_deis(args.deis or _descargar_deis()))
    print(f'medicamentos: {subir(url, clave, "medicamentos", meds, "id")}')
    print(f'establecimientos: {subir(url, clave, "establecimientos", ests, "codigo")}')
    print(f'marcados como no vigentes: {marcar_no_vigentes(url, clave, {e["codigo"] for e in ests})}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
