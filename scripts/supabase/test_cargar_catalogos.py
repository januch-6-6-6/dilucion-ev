"""Pruebas de la carga de catálogos (sin red). Correr: python3 -m pytest scripts/supabase -q"""
import json
import re
from pathlib import Path

from scripts.supabase import cargar_catalogos as cc

RAIZ = Path(__file__).resolve().parents[2]
MUESTRA = Path(__file__).with_name('muestra_deis.csv')


class RedFalsa:
    """Registra las peticiones y responde con lo que se le indique; nunca toca la red."""

    def __init__(self, existentes=()):
        self.llamadas = []
        self.existentes = list(existentes)

    def __call__(self, metodo, url, clave, cuerpo=None):
        self.llamadas.append((metodo, url, cuerpo))
        if metodo == 'GET':
            return 200, [{'codigo': c} for c in self.existentes]
        return 204, None


def test_medicamentos_salen_de_las_fichas():
    filas = cc.filas_medicamentos(RAIZ / 'datos' / 'medicamentos')
    ids = {f['id'] for f in filas}
    assert len(filas) == len(ids) == 89
    assert 'ceftriaxona' in ids
    assert all(re.fullmatch(r'[a-z0-9-]+', i) for i in ids)


def test_establecimientos_se_normalizan_descartan_filas_sin_codigo_y_deduplican():
    filas = cc.filas_establecimientos(cc.leer_deis(MUESTRA))
    por_codigo = {f['codigo']: f for f in filas}
    assert len(filas) == len(por_codigo) == 3  # 5 filas: una sin código y una repetida
    assert por_codigo['114101'] == {
        'codigo': '114101',
        'nombre': 'Complejo Hospitalario Dr. Sótero del Río (Santiago, Puente Alto)',
        'tipo': 'Hospital',
        'comuna': 'Puente Alto',
        'region': por_codigo['114101']['region'],
        'vigente': True,
    }
    assert por_codigo['114101']['region'].startswith('Metropolitana')
    assert [f['vigente'] for f in filas].count(False) == 1  # el «Cerrado»
    assert all(set(f) == {'codigo', 'nombre', 'tipo', 'comuna', 'region', 'vigente'} for f in filas)


def test_subir_hace_upsert_por_lotes_de_500_y_nunca_borra():
    red = RedFalsa()
    filas = [{'id': f'm{i}'} for i in range(1201)]
    total = cc.subir('https://x.supabase.co', 'clave', 'medicamentos', filas, 'id', http=red)
    assert total == 1201
    assert [len(c[2]) for c in red.llamadas] == [500, 500, 201]
    assert all(m == 'POST' and 'on_conflict=id' in u for m, u, _ in red.llamadas)
    assert not any(m == 'DELETE' for m, _, _ in red.llamadas)


def test_marcar_no_vigentes_solo_actualiza_los_que_desaparecieron_y_respeta_los_de_prueba():
    red = RedFalsa(existentes=['A', 'B', 'C', 'PRUEBA-1f2e3d-x'])
    n = cc.marcar_no_vigentes('https://x.supabase.co', 'clave', {'A'}, http=red)
    assert n == 2
    parches = [(u, c) for m, u, c in red.llamadas if m == 'PATCH']
    assert len(parches) == 1
    url, cuerpo = parches[0]
    assert cuerpo == {'vigente': False}
    assert re.search(r'codigo=in\.\(B,C\)|codigo=in\.\(C,B\)', url)
    assert 'PRUEBA' not in url
    assert not any(m == 'DELETE' for m, _, _ in red.llamadas)


def test_marcar_no_vigentes_no_hace_nada_si_no_falta_ninguno():
    red = RedFalsa(existentes=['A', 'B'])
    assert cc.marcar_no_vigentes('https://x.supabase.co', 'clave', {'A', 'B', 'Z'}, http=red) == 0
    assert [m for m, _, _ in red.llamadas] == ['GET']


def test_las_peticiones_a_supabase_no_se_hacen_pasar_por_un_navegador(monkeypatch):
    """Supabase rechaza la clave secreta si la petición parece venir de un navegador (HTTP 401)."""
    vistas = []

    class Respuesta:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b'[]'

    def falso_urlopen(req, timeout=None):
        vistas.append(req)
        return Respuesta()

    monkeypatch.setattr(cc.urllib.request, 'urlopen', falso_urlopen)
    cc._http('GET', 'https://x.supabase.co/rest/v1/medicamentos', 'sb_secret_x')
    ua = vistas[0].get_header('User-agent')
    assert ua and 'Mozilla' not in ua
