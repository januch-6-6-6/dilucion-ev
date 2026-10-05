"""Genera datos/fuentes-orales.yaml y datos/orales/*.yaml. Uso: python3 scripts/generar-orales.py"""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orales import tanda1  # noqa: E402

MODULOS = [tanda1]
for nombre in ('tanda2', 'tanda3'):
    try:
        MODULOS.append(__import__(f'orales.{nombre}', fromlist=[nombre]))
    except ImportError:
        pass

RAIZ = Path(__file__).resolve().parent.parent


def volcar(ruta, datos):
    with open(ruta, 'w') as f:
        yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False, width=120)


def main():
    fuentes, vistos, fichas = [], set(), {}
    for m in MODULOS:
        for f in m.fuentes():
            if f['id'] not in vistos:
                vistos.add(f['id'])
                fuentes.append(f)
        fichas.update(m.fichas())
    (RAIZ / 'datos' / 'orales').mkdir(exist_ok=True)
    volcar(RAIZ / 'datos' / 'fuentes-orales.yaml', fuentes)
    for k, ficha in fichas.items():
        volcar(RAIZ / 'datos' / 'orales' / f'{k}.yaml', ficha)
    print(f'{len(fichas)} fichas orales, {len(fuentes)} fuentes')


if __name__ == '__main__':
    main()
