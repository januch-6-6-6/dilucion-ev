"""Genera informes/v0.2-revision-clinica.md a partir de las fichas YAML. Uso: python3 scripts/informe_revision.py"""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fichas import tanda1, tanda1b, tanda2, tanda3  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def ids_de(modulo, stab=None):
    import json
    if modulo is tanda1:
        stab = json.load(open(RAIZ / 'datos' / 'crudos' / 'stabilis-y-2026-10-01.json'))
    return list(modulo.fichas(stab))


def num(v):
    return ('%g' % v).replace('.', ',')


def rango(d):
    if 'min' in d and 'max' in d and d['min'] != d['max']:
        r = f"{num(d['min'])}–{num(d['max'])}"
    else:
        r = num(d.get('max', d.get('min')))
    extra = f" (máx. {num(d['maximaAbsoluta'])})" if 'maximaAbsoluta' in d else ''
    tope = f" [tope {num(d['topeAdulto']['valor'])} {d['topeAdulto']['unidad']}]" if 'topeAdulto' in d else ''
    return f"{r} {d['unidad']}{extra}{tope}"


def celda(texto):
    return str(texto).replace('|', '/').replace('\n', ' ')


def fila(f):
    pres = '; '.join(f"{num(p['cantidad']['valor'])} {p['cantidad']['unidad']}/{num(p['volumenMl'])} ml" for p in f['presentaciones'])
    if f['reconstitucion']:
        pres += f" (reconst. {num(f['reconstitucion']['volumenMl'])} ml)"
    dil = '; '.join(e['descripcion'] for e in f['dilucion']['estandar']) or '—'
    adu = '<br>'.join(f"{d['indicacion']}: {rango(d)}" for d in f['dosis'] if d['poblacion'] == 'adulto') or 'sin dosis en las fuentes'
    ped = '<br>'.join(f"{d['indicacion']}: {rango(d)}" for d in f['dosis'] if d['poblacion'] == 'pediatrico') or 'sin dosis pediátrica'
    tmin = f"{num(f['administracion']['tiempoMinimoMin'])} min" if 'tiempoMinimoMin' in f['administracion'] else '—'
    inc = [c['con'] for c in f['compatibilidad'] if c['estado'] == 'incompatible']
    inc_txt = (', '.join(inc[:6]) + (f' y {len(inc) - 6} más' if len(inc) > 6 else '')) if inc else '—'
    refs = sorted({f['administracion']['fuente']['ref'], f['efectosAdversos']['fuente']['ref'], *(d['fuente']['ref'] for d in f['dosis']),
                   *(p['fuente']['ref'] for p in f['presentaciones'])})
    disc = len(f['meta']['discrepancias'])
    alto = ' ⚠' if f['altoRiesgo'] else ''
    return '| ' + ' | '.join(celda(x) for x in [f"**{f['nombre']}**{alto}", pres, dil, adu, ped, tmin, inc_txt, ', '.join(refs), disc or '—']) + ' |'


def main():
    fuentes = {x['id']: x for x in yaml.safe_load(open(RAIZ / 'datos' / 'fuentes.yaml'))}
    fichas = {p.stem: yaml.safe_load(open(p)) for p in sorted((RAIZ / 'datos' / 'medicamentos').glob('*.yaml'))}
    tandas = [('Tanda 1 — urgencia / SAMU', ids_de(tanda1) + ids_de(tanda1b)),
              ('Tanda 2 — antiinfecciosos', ids_de(tanda2)),
              ('Tanda 3 — hospitalarios', ids_de(tanda3))]
    L = ['# Dilución EV v0.2 — Informe para la revisión clínica', '',
         f'{len(fichas)} medicamentos. Generado por `scripts/informe_revision.py` desde las fichas YAML (no editar a mano).',
         'Ninguna ficha está marcada como revisada: `meta.revisadoPor` queda vacío hasta la revisión de Héctor.', '',
         '## Para revisar primero', '', '### Discrepancias entre fuentes y decisiones tomadas', '']
    todas = [(f, d) for f in sorted(fichas.values(), key=lambda f: f['nombre']) for d in f['meta']['discrepancias']]
    todas.sort(key=lambda fd: 'REVISAR PRIMERO' not in fd[1]['decision'])
    for n, (f, d) in enumerate(todas, 1):
        prio = ' **(REVISAR PRIMERO)**' if 'REVISAR PRIMERO' in d['decision'] else ''
        L.append(f"{n}. **{f['nombre']}** — {d['campo']}{prio}: " + '; '.join(d['valores']) + f". → *{d['decision']}*")
    n = len(todas)
    L += ['', '### Fuentes extranjeras y no chilenas usadas', '',
          'Todas las fichas técnicas CIMA (España), etiquetas FDA (EE. UU.) y Pediamécum (España) son extranjeras; se usan como',
          'segunda fuente o cuando no hay fuente chilena (ver discrepancias «fuente chilena»). Marcadas explícitamente como extranjeras:', '']
    for x in fuentes.values():
        if 'EXTRANJERA' in x['titulo']:
            L.append(f"- `{x['id']}` — {x['titulo']} ({x['institucion']})")
    otras = sorted({x['id'].split('-')[0] for x in fuentes.values() if x['id'].split('-')[0] in ('CIMA', 'FDA', 'PEDIAMECUM')})
    L.append(f"- Además: {', '.join(otras)} ({sum(1 for x in fuentes.values() if x['id'].split('-')[0] in otras)} documentos).")
    L += ['', '### Fichas sin dosis en las fuentes', '']
    L += [f"- {f['nombre']}" for f in fichas.values() if not f['dosis']]
    for titulo, ids in tandas:
        L += ['', f'## {titulo} ({len(ids)})', '',
              '| Medicamento | Presentación | Dilución estándar | Dosis adulto | Dosis pediátrica | Tiempo mín. | Incompatibles en Y | Fuentes | Discrep. |',
              '|---|---|---|---|---|---|---|---|---|']
        L += [fila(fichas[k]) for k in sorted(ids, key=lambda i: fichas[i]['nombre'])]
    L += ['', '⚠ = alto riesgo. «Incompatibles en Y» incluye casillas amarillas de Stabilis (criterio conservador) y las de ficha técnica.', '']
    (RAIZ / 'informes' / 'v0.2-revision-clinica.md').write_text('\n'.join(L))
    print(f'{len(fichas)} medicamentos, {n} discrepancias')


if __name__ == '__main__':
    main()
