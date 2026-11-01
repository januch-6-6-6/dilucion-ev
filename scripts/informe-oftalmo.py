"""Genera informes/oftalmologia-revision.md con los conteos y la tabla, calculados desde datos/oftalmo/*.yaml.

Uso: python3 scripts/informe-oftalmo.py
"""
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from oftalmo.notas import NOTAS  # noqa: E402

FAMILIAS = ['intracameral', 'intravitreo', 'bloqueo', 'periocular', 'antifibrotico']


def cargar():
    fuentes = {f['id']: f for f in yaml.safe_load(open(RAIZ / 'datos' / 'fuentes-oftalmo.yaml', encoding='utf-8'))}
    fichas = [yaml.safe_load(open(p, encoding='utf-8')) for p in sorted((RAIZ / 'datos' / 'oftalmo').glob('*.yaml'))]
    return fichas, fuentes


def estado(f, fuentes):
    if f['sinPauta']:
        return 'sin pauta'
    for d in f['dosis']:
        propia = fuentes[d['fuente']['ref']]['institucion']
        if any(fuentes[t['ref']]['institucion'] != propia for t in d.get('tambien', [])):
            return 'contrastada'
    return 'fuente única'


def dosis_txt(f):
    partes = []
    for d in f['dosis']:
        fin = d.get('final')
        if not fin:
            partes.append(f"{d['via']}: texto")
            continue
        c = fin['cantidad']
        cant = f"{c['min']}–{c['max']} {c['unidad']}" if 'min' in c else f"{c['valor']} {c['unidad']}"
        partes.append(f"{d['via']}: {cant}/{fin['volumenMl']} ml")
    return '; '.join(partes) if partes else '—'


def orales_oftalmicos():
    """Secciones del informe para los orales con `usos: [oftalmologia]` (fichas de datos/orales/)."""
    fichas = [yaml.safe_load(open(p, encoding='utf-8')) for p in sorted((RAIZ / 'datos' / 'orales').glob('*.yaml'))]
    fichas = [f for f in fichas if 'oftalmologia' in f.get('usos', [])]
    L = ['', '## Orales de uso oftalmológico', '',
         f'- Orales marcados con uso oftalmológico: **{len(fichas)}** (7 fichas nuevas en `scripts/orales/tanda4.py` y 4 ya existentes '
         'a las que `tanda4.marcar` suma dosis oftálmicas sin tocar las anteriores).',
         '- Cada ficha nueva carga solo el uso oftalmológico del fármaco; las demás indicaciones no se cargan.',
         '- **No se citan** hasta cotejar con el original: los autores del PPP de cierre angular de la AAO, la conversión de '
         'metilprednisolona del ONTT (en prednisona solo hay una alerta con el resultado de prednisona oral sola) y el estudio ZEDS '
         '(valaciclovir en zóster oftálmico; un repositorio lo marca «withdrawn»).',
         '- Evidencia débil fuera de la v1 (decisión 4 de Héctor): tranexámico en hipema, ivermectina en Demodex, glicerol oral, isosorbida osmótica.',
         '', '| id | dosis oftálmicas | registro | pediatría | notas |', '|---|---|---|---|---|']
    for f in fichas:
        n = sum(1 for d in f['dosis'] if d.get('oftalmica'))
        reg = 'NO registrado' if any(p['registroChile'] == 'no_registrado' for p in f['presentaciones']) else 'sin verificar'
        L.append(f"| {f['id']} | {n} | {reg} | {f['pediatria']['estado']} | {len(f['alertas'])} alertas; {len(f['discrepancias'])} discrepancias |")
    return L


def main():
    fichas, fuentes = cargar()
    est = {f['id']: estado(f, fuentes) for f in fichas}
    L = ['# Oftalmología (pabellón): revisión molécula por molécula', '',
         '> Generado por `scripts/informe-oftalmo.py` desde `datos/oftalmo/*.yaml`; las notas están en `scripts/oftalmo/notas.py`. '
         'Material de formación, no de prescripción.', '',
         '## Conteos', '', f'- Fichas de pabellón: **{len(fichas)}**.']
    for fam in FAMILIAS:
        n = sum(1 for f in fichas if f['familias'][0] == fam)
        if n:
            L.append(f'  - {fam}: {n}')
    L += [f"- Sin registro en Chile: **{sum(f['registroChile'] == 'no_registrado' for f in fichas)}** "
          f"({', '.join(f['id'] for f in fichas if f['registroChile'] == 'no_registrado')}).",
          f"- Contrastadas: **{sum(v == 'contrastada' for v in est.values())}**; fuente única: **{sum(v == 'fuente única' for v in est.values())}**; "
          f"sin pauta: **{sum(v == 'sin pauta' for v in est.values())}**.",
          f"- Con protocolo de preparación citado: **{sum(bool(f['protocolos']) for f in fichas)}**; sin pasos publicados: "
          f"**{sum(not f['protocolos'] and not f['sinPauta'] and f['modo'] == 'intraocular' and not all(p['usoDirecto'] for p in f['presentaciones']) for f in fichas)}**.",
          f"- Fuentes distintas: **{len(fuentes)}**.", '',
          '## Tabla', '', '| id | dosis mostrada | fuente | pasos | registro | estado | notas |', '|---|---|---|---|---|---|---|']
    for f in fichas:
        d0 = f['dosis'][0] if f['dosis'] else None
        fu = fuentes[d0['fuente']['ref']]['institucion'] if d0 else '—'
        tam = ' + '.join(sorted({fuentes[t['ref']]['institucion'] for d in f['dosis'] for t in d.get('tambien', [])})) or '—'
        L.append(f"| {f['id']} | {dosis_txt(f)} | {fu}; 2.ª: {tam} | {'sí' if f['protocolos'] else 'no'} | "
                 f"{'ISP' if f['registroChile'] == 'verificado' else 'NO registrado'} | {est[f['id']]} | {NOTAS.get(f['id'], '')} |")
    L += orales_oftalmicos()
    (RAIZ / 'informes' / 'oftalmologia-revision.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print(f'{len(fichas)} fichas en el informe')


if __name__ == '__main__':
    main()
