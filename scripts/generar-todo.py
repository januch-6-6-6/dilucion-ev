"""Genera datos/fuentes.yaml y todas las fichas. Uso: python3 scripts/generar-todo.py"""
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fichas import tanda1, tanda1b, tanda2, tanda3  # noqa: E402
from fichas.comun import compat_desde_matriz  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
STAB_T1 = RAIZ / 'datos' / 'crudos' / 'stabilis-y-2026-10-01.json'
STAB_GLOBAL = RAIZ / 'datos' / 'crudos' / 'stabilis-y-global-2026-10-01.json'
MODULOS = [tanda1, tanda1b, tanda2, tanda3]


def main():
    stab = json.load(open(STAB_T1))
    fuentes, vistos, fichas = [], set(), {}
    for m in MODULOS:
        for f in m.fuentes():
            if f['id'] not in vistos:
                vistos.add(f['id'])
                fuentes.append(f)
        fichas.update(m.fichas(stab))
    matriz = json.load(open(STAB_GLOBAL))
    for k, ficha in fichas.items():
        ficha['compatibilidad'] = compat_desde_matriz(matriz, k, list(fichas))
    with open(RAIZ / 'datos' / 'fuentes.yaml', 'w') as f:
        yaml.safe_dump(fuentes, f, allow_unicode=True, sort_keys=False, width=120)
    for k, ficha in fichas.items():
        with open(RAIZ / 'datos' / 'medicamentos' / f'{k}.yaml', 'w') as f:
            yaml.safe_dump(ficha, f, allow_unicode=True, sort_keys=False, width=120)
    print(f'{len(fichas)} fichas, {len(fuentes)} fuentes')


if __name__ == '__main__':
    main()
