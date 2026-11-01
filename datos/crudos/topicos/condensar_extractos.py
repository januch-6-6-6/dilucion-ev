"""Versión condensada de extractos.md para la revisión molécula por molécula → extractos-condensados.md.
Igual que extraer_extractos.py, pero de Pediamécum solo deja las líneas de vía tópica (oftálmica, ótica, nasal)
y recorta CIMA/DailyMed. No reemplaza a extractos.md: ante cualquier duda se lee el .txt completo."""
import json, os, re
from extraer_extractos import D, slug, cima, dailymed, corte

CLAVE = re.compile(r'oft[aá]lm|[oó]tic|o[ií]do|nasal|nariz|fosa|gota|colirio|pomada|ung[uü]ento|pulveriz|aplicaci|t[oó]pic|instil|conjunt|saco|ojo|nebuliz|spray|gel', re.I)

def pedia(comp):
    out = []
    for c in comp:
        nom = 'azelastina-oftalmica' if c.strip().lower() == 'azelastina' else slug(c)
        f = os.path.join(D, 'pediamecum', nom + '.txt')
        if not os.path.exists(f): continue
        t = open(f, encoding='utf8', errors='ignore').read()
        x = corte(t, r'Dosis y Pautas de Administraci[oó]n', r'\n\s*Contraindicaciones', 20000) or ''
        lineas = [l.strip() for l in x.split('\n') if CLAVE.search(l)]
        out.append(f'**{c.strip()}** ({nom}): ' + (' | '.join(lineas)[:1500] or '(sin líneas tópicas)'))
    return out

L = json.load(open(os.path.join(D, 'lista-isp.json')))
with open(os.path.join(D, 'extractos-condensados.md'), 'w') as o:
    for x in L:
        m = x['molecula']; s = slug(m)
        o.write(f"\n## {m.title()} (`{s}` · {'/'.join(x['vias'])})\n")
        o.write('ISP: ' + '; '.join(f"{r['Nombre']} [{r['Producto']}]" for r in x['registros'][:10]) + (f' … +{x["n"]-10}' if x['n'] > 10 else '') + '\n')
        for tit, partes in (('CIMA', cima(s)), ('DM', dailymed(s)), ('PED', pedia(m.split('+')))):
            for p in partes:
                o.write(f'{tit}: ' + re.sub(r'\s+', ' ', p)[:2600] + '\n')
print(os.path.getsize(os.path.join(D, 'extractos-condensados.md')))
