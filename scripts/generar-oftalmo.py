"""Genera datos/fuentes-oftalmo.yaml y datos/oftalmo/*.yaml (pabellón oftalmológico).

Uso: python3 scripts/generar-oftalmo.py
Los datos se escriben a mano en scripts/oftalmo/loteN.py a partir de datos/crudos/oftalmo/ (ver su ESTADO.md).
"""
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oftalmo import comun  # noqa: E402

LOTES = []
for n in range(1, 10):
    try:
        LOTES.append(__import__(f'oftalmo.lote{n}', fromlist=[f'lote{n}']))
    except ModuleNotFoundError as e:
        if e.name != f'oftalmo.lote{n}':
            raise

RAIZ = Path(__file__).resolve().parent.parent


def volcar(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False, width=120)


def main():
    fichas = {}
    for m in LOTES:
        nuevas = m.fichas()
        repetidas = set(nuevas) & set(fichas)
        if repetidas:
            raise SystemExit(f'ficha repetida entre lotes: {sorted(repetidas)}')
        fichas.update(nuevas)
    candidatos = json.load(open(comun.CRUDOS / 'candidatos.json', encoding='utf-8'))
    pabellon = {c['id'] for fam, lista in candidatos.items() if not fam.startswith('_') and fam != 'oral' for c in lista}
    desconocidas = set(fichas) - pabellon
    if desconocidas:
        raise SystemExit(f'fichas que no están en candidatos.json (pabellón): {sorted(desconocidas)}')
    dir_ = RAIZ / 'datos' / 'oftalmo'
    dir_.mkdir(exist_ok=True)
    volcar(RAIZ / 'datos' / 'fuentes-oftalmo.yaml', sorted(comun.FUENTES.values(), key=lambda f: f['id']))
    for viejo in dir_.glob('*.yaml'):
        if viejo.stem not in fichas:
            viejo.unlink()
    for k, ficha in fichas.items():
        volcar(dir_ / f'{k}.yaml', ficha)
    print(f'{len(fichas)} fichas oculares, {len(comun.FUENTES)} fuentes')
    faltan = sorted(pabellon - set(fichas))
    if faltan:
        print(f'Sin ficha todavía ({len(faltan)}): {", ".join(faltan)}')


if __name__ == '__main__':
    main()
