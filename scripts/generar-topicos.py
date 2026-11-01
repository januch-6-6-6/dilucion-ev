"""Genera datos/fuentes-topicos.yaml y datos/topicos/*.yaml (ojo, oído y nariz).

Uso: python3 scripts/generar-topicos.py
Los datos se escriben a mano en scripts/topicos/loteN.py a partir de datos/crudos/topicos/ (ver su ESTADO.md).
"""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topicos import comun  # noqa: E402

LOTES = []
for n in range(1, 10):
    try:
        LOTES.append(__import__(f'topicos.lote{n}', fromlist=[f'lote{n}']))
    except ModuleNotFoundError as e:
        if e.name != f'topicos.lote{n}':
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
    faltan = {comun.slug_molecula(x) for x in comun._ISP} - set(fichas)
    dir_ = RAIZ / 'datos' / 'topicos'
    dir_.mkdir(exist_ok=True)
    volcar(RAIZ / 'datos' / 'fuentes-topicos.yaml', sorted(comun.FUENTES.values(), key=lambda f: f['id']))
    for viejo in dir_.glob('*.yaml'):
        if viejo.stem not in fichas:
            viejo.unlink()
    for k, ficha in fichas.items():
        volcar(dir_ / f'{k}.yaml', ficha)
    print(f'{len(fichas)} fichas tópicas, {len(comun.FUENTES)} fuentes')
    if faltan:
        print(f'Sin ficha todavía ({len(faltan)}): {", ".join(sorted(faltan))}')


if __name__ == '__main__':
    main()
