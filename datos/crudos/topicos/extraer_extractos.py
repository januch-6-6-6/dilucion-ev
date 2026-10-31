"""Extractos lado a lado por molécula para el informe de discrepancias → extractos.md.
Por molécula: presentaciones ISP, CIMA 4.2 (posología) + 4.3 (contraindicaciones) + 6.3 (validez tras apertura),
DailyMed DOSAGE AND ADMINISTRATION + CONTRAINDICATIONS + HOW SUPPLIED/STORAGE, y Pediamécum «Dosis y Pautas» por componente."""
import glob, json, os, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__))

def n(x): return ''.join(c for c in unicodedata.normalize('NFD', x.lower()) if unicodedata.category(c) != 'Mn')
def slug(m): return re.sub(r'[^a-z0-9]+', '-', n(m)).strip('-')
def limpio(t, tope):
    t = re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n', t)).strip()
    return t if len(t) <= tope else t[:tope] + ' […recortado]'
def corte(t, ini, fin, tope):
    m = re.search(r'(?:' + ini + r')(?P<c>.*?)(?=' + fin + r'|\Z)', t, re.S | re.I)
    return limpio(m.group('c'), tope) if m else None

def cima(s):
    out = []
    for f in sorted(glob.glob(os.path.join(D, 'cima', s + '__*.txt'))):
        t = open(f, encoding='utf8', errors='ignore').read()
        cab = t.split('\n')[:2]
        out.append(f'**{cab[0]}** — {cab[1]}')
        for tit, ini, fin, tope in (('4.2 Posología', r'\n\s*4\.2\.?\s', r'\n\s*4\.3\.?\s', 3500),
                                    ('4.3 Contraindicaciones', r'\n\s*4\.3\.?\s', r'\n\s*4\.4\.?\s', 700),
                                    ('6.3 Validez', r'\n\s*6\.3\.?\s', r'\n\s*6\.5\.?\s', 600)):
            x = corte(t, ini, fin, tope)
            if x: out.append(f'*{tit}:* {x}')
    return out

def dailymed(s):
    f = os.path.join(D, 'dailymed', s + '.txt')
    if not os.path.exists(f): return []
    t = open(f, encoding='utf8', errors='ignore').read()
    cab = t.split('\n')[:2]
    out = [f'**{cab[0]}** — {cab[1]}']
    for tit, ini, fin, tope in (('Dosage', r'DOSAGE (AND|&) ADMINISTRATION|DIRECTIONS', r'DOSAGE FORMS|CONTRAINDICATIONS|WARNINGS|OTHER INFORMATION|INACTIVE', 2500),
                                ('Contraindications', r'\n\s*(\d+\s*)?CONTRAINDICATIONS', r'WARNINGS|ADVERSE', 600),
                                ('Storage', r'HOW SUPPLIED|STORAGE AND HANDLING|OTHER INFORMATION', r'PATIENT COUNSELING|INACTIVE|QUESTIONS|PACKAGE LABEL', 600)):
        x = corte(t, ini, fin, tope)
        if x: out.append(f'*{tit}:* {x}')
    return out

def pediamecum(comp):
    out = []
    for c in comp:
        f = os.path.join(D, 'pediamecum', slug(c) + '.txt')
        if c.strip().lower() == 'azelastina':
            fs = [os.path.join(D, 'pediamecum', 'azelastina-oftalmica.txt'), f]
        else:
            fs = [f]
        for f in fs:
            if not os.path.exists(f): continue
            t = open(f, encoding='utf8', errors='ignore').read()
            x = corte(t, r'Dosis y Pautas de Administraci[oó]n', r'\n\s*Contraindicaciones', 2500)
            out.append(f'**{c.strip()}** — {t.split(chr(10))[0]}\n{x or "(sin sección de dosis)"}')
    return out

L = json.load(open(os.path.join(D, 'lista-isp.json')))
with open(os.path.join(D, 'extractos.md'), 'w') as o:
    o.write('# Extractos por molécula (generado por extraer_extractos.py)\n\n')
    for x in L:
        m = x['molecula']; s = slug(m)
        o.write(f"\n---\n\n## {m.title()}  (`{s}` · vía: {'/'.join(x['vias'])})\n\n")
        o.write('### ISP — presentaciones vigentes en Chile\n' + '\n'.join(f"- {r['Producto']} · {r['Nombre']} · {r['Titular']}" for r in x['registros'][:8])
                + (f"\n- … y {x['n']-8} más" if x['n'] > 8 else '') + '\n\n')
        for tit, partes in (('CIMA (España)', cima(s)), ('DailyMed (EE. UU.)', dailymed(s)), ('Pediamécum (pediatría)', pediamecum(m.split('+')))):
            o.write(f'### {tit}\n' + ('\n\n'.join(partes) if partes else '(sin fuente)') + '\n\n')
print(os.path.getsize(os.path.join(D, 'extractos.md')))
