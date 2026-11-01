"""Cruce Fase 0 oftalmología: por candidato, registros ISP pertinentes (filtrados por forma: inyectable para pabellón, oral para orales)
y fuentes disponibles (CIMA ocular/parenteral/oral, DailyMed, SEFH PNT, consenso 2025, Pediamécum, web/*). Escribe COBERTURA.md."""
import json, glob, os, re, unicodedata
def n(x): return ''.join(c for c in unicodedata.normalize('NFD', x.upper()) if unicodedata.category(c) != 'Mn')
cand = json.load(open('candidatos.json'))
isp = {}
for f in glob.glob('isp/*.json') + glob.glob('isp2/*.json'):
    for x in json.load(open(f)):
        if re.match(r'^(F|B|FX)-', x.get('Producto', '')): isp[x['Producto']] = x
consenso = n(open('sefh/consenso-2025.txt').read())
pnt = {os.path.basename(p) for p in glob.glob('sefh/*.txt')}
web = {os.path.basename(p)[:-4] for p in glob.glob('web/*.txt')}
# términos para filtrar el ISP por candidato (nombre del PA en el registro o nombre comercial)
TERM = {'carbacol': ['CARBACOL', 'CARBACHOL', 'MIOSTAT'], 'acetilcolina': ['ACETILCOLINA', 'MIOCHOL'], 'alteplasa': ['ALTEPLASA', 'ACTILYSE'],
        'adrenalina': ['EPINEFRINA', 'ADRENALINA'], 'fenilefrina-tropicamida-lidocaina': ['MYDRANE'], 'fenilefrina-ketorolaco': ['OMIDRIA'],
        'azul-tripano': ['TRIPANO', 'VISIONBLUE', 'VISION BLUE'], 'verde-indocianina': ['INDOCIANINA'], 'azul-brillante': ['BRILLIANT', 'AZUL BRILLANTE'],
        'dexametasona-implante': ['OZURDEX'], 'anfotericina-b': ['ANFOTERICINA'], 'toxina-botulinica': ['BOTUL', 'BOTOX', 'DYSPORT'],
        'acido-tranexamico': ['TRANEX'], 'glicerol': ['GLICER'], 'cotrimoxazol': ['SULFAMETOXAZOL', 'COTRIMOXAZOL']}
FORMA = {'oral': r'COMPRIMID|CAPSUL|SUSPENSION ORAL|SOLUCION ORAL|JARABE|GRAGEA|POLVO PARA SUSPENSION ORAL|SOBRE',
         'otro': r'INYECT|INTRAV|LIOFILIZ|POLVO PARA SOLUCION|CONCENTRADO|IMPLANTE|PERFUS|SOLUCION ESTERIL|IRRIGAC|INTRAOCULAR'}
NO_PABELLON = r'DENTAL|ESPINAL|HIPERBAR|ARTICAINA|CREMA|GEL |UNGUENTO|SUPOSITOR|OFTALMIC|OTIC|VAGINAL|TOPIC|DERMIC|NASAL|PARCHE|EMULSION INYECT|NUTRI'
filas = []
for fam, lista in cand.items():
    if fam.startswith('_'): continue
    for c in lista:
        terms = TERM.get(c['id'], [n(c['pa'])])
        regs = [x for x in isp.values() if any(t in n(x.get('PA', '') + ' ' + x['Nombre']) for t in terms)]
        if fam == 'oral': regs = [x for x in regs if re.search(FORMA['oral'], n(x['Nombre']))]
        else: regs = [x for x in regs if re.search(FORMA['otro'], n(x['Nombre'])) and not re.search(NO_PABELLON, n(x['Nombre']))]
        ci = json.load(open(f"cima/{c['id']}.json")) if os.path.exists(f"cima/{c['id']}.json") else {}
        fuentes = []
        if ci.get('sel'): fuentes.append(f"CIMA-{ci['tipo']}: " + '; '.join(s['nombre'][:40] for s in ci['sel']))
        if os.path.exists(f"dailymed/{c['id']}.txt"): fuentes.append('DailyMed: ' + open(f"dailymed/{c['id']}.txt").readline()[:50].strip())
        clave = n(c['pa'].split()[0])[:8]
        if any(clave in n(p) for p in pnt if p != 'consenso-2025.txt'): fuentes.append('PNT SEFH')
        if fam != 'oral' and clave in consenso: fuentes.append('Consenso SEFH-SEO-SERV 2025')
        if os.path.exists(f"pediamecum/{c['id']}.txt"): fuentes.append('Pediamécum')
        w = [x for x in web if x.startswith(c['id'][:6]) or (c['id'] == 'alteplasa' and x == 'eyewiki-tpa')]
        if w: fuentes.append('web: ' + ', '.join(sorted(w)))
        filas.append((fam, c['id'], c['uso'], len(regs), '; '.join(sorted({x['Nombre'][:55] for x in regs})[:3]), ' | '.join(fuentes) or '—'))
with open('COBERTURA.md', 'w') as o:
    o.write('# Cobertura Fase 0 — oftalmología (pabellón + orales)\n\nGenerado por `cobertura.py`. ISP: registros vigentes F-/B-/FX- filtrados por forma (inyectable/implante para pabellón; oral para orales).\n\n')
    for fam in ('intracameral', 'intravitreo', 'periocular', 'oral'):
        o.write(f'\n## {fam}\n\n| id | uso | ISP (n) | productos ISP (muestra) | fuentes |\n|---|---|---:|---|---|\n')
        for f in filas:
            if f[0] == fam: o.write(f'| {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} |\n')
    sin_isp = [f[1] for f in filas if f[3] == 0]; sin_f = [f[1] for f in filas if f[5] == '—']
    o.write(f'\n## Resumen\n\n- Candidatos: {len(filas)}\n- Sin registro ISP pertinente ({len(sin_isp)}): {", ".join(sin_isp)}\n- Sin ninguna fuente ({len(sin_f)}): {", ".join(sin_f) or "ninguno"}\n')
print(open('COBERTURA.md').read()[-900:])
