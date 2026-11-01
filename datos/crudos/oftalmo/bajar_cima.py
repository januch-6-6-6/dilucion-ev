"""Fase 0 oftalmología: fichas técnicas CIMA por candidato. Para pabellón se exige una vía ocular de inyección
(intraocular, intravítrea, intracameral, retro/peribulbar, subconjuntival, subtenoniana); para orales, vía oral.
Si no hay producto con vía ocular, se guarda igual el mejor producto parenteral (marcado 'parenteral') para conocer el frasco de partida."""
import json, subprocess, os, re, html, unicodedata, urllib.parse
D = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(D, 'cima')
def n(x): return ''.join(c for c in unicodedata.normalize('NFD', x.upper()) if unicodedata.category(c) != 'Mn')
def curl(u): return subprocess.run(['curl', '-sL', '--max-time', '60', u], capture_output=True, text=True).stdout
def texto(h):
    h = re.sub(r'(?is)<(script|style).*?</\1>', '', h)
    h = re.sub(r'(?i)<br\s*/?>|</p>|</tr>|</h\d>|</li>', '\n', h); h = re.sub(r'(?i)</t[dh]>', ' | ', h)
    h = html.unescape(re.sub(r'<[^>]+>', '', h))
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t\xa0]+', ' ', h))
def secciones(t):
    out = []
    for a, b in ((r'\n\s*4\.1\.? ', r'\n\s*5\.1\.? '), (r'\n\s*6\.2\.? ', r'\n\s*7\.? ')):
        m = re.search(a, t); e = re.search(b, t[m.end():]) if m else None
        if m: out.append(t[m.start():m.end() + e.start()] if e else t[m.start():m.start() + 20000])
    return '\n'.join(out) if out else t[:30000]
OCULAR = r'INTRAOCULAR|INTRAVITRE|INTRACAMERAL|RETROBULBAR|PERIBULBAR|SUBCONJUNTIVAL|SUBTENON|OFTALM'
# nombre de principio activo en CIMA cuando difiere
PA = {'EPINEFRINA': 'adrenalina', 'TRIPANO': 'azul tripan', 'INDOCIANINA': 'verde de indocianina', 'AZUL BRILLANTE': 'azul brillante',
      'BOTULINICA': 'toxina botulinica', 'TRANEXAMICO': 'tranexamico', 'SULFAMETOXAZOL': 'sulfametoxazol', 'GLICEROL': 'glicerol',
      'ANFOTERICINA': 'anfotericina b', 'FOSCARNET': 'foscarnet'}
def vias(m): return ' '.join(n(x['nombre']) for x in m.get('viasAdministracion', [])) + ' ' + n(m['formaFarmaceutica']['nombre'])
def con_html(m): return next((d['urlHtml'] for d in m.get('docs', []) if d['tipo'] == 1 and d.get('urlHtml')), None)
if __name__ == '__main__':
    cand = json.load(open(os.path.join(D, 'candidatos.json')))
    for fam, lista in cand.items():
        if fam.startswith('_'): continue
        for c in lista:
            idx = os.path.join(O, f"{c['id']}.json")
            if os.path.exists(idx): continue
            q = PA.get(c['pa'], c['pa'].lower())
            res = []
            for pag in (1, 2, 3):
                try: r = json.loads(curl(f'https://cima.aemps.es/cima/rest/medicamentos?practiv1={urllib.parse.quote(q)}&pagesize=200&pagina={pag}') or '{}')
                except Exception: r = {}
                res += r.get('resultados', [])
                if len(r.get('resultados', [])) < 200: break
            if fam == 'oral': ok = [m for m in res if re.search(r'ORAL', vias(m))]; tipo = 'oral'
            else:
                ok = [m for m in res if re.search(OCULAR, vias(m)) and not re.search(r'COLIRIO|POMADA OFTALM|GOTAS', n(m['formaFarmaceutica']['nombre']))]; tipo = 'ocular'
                if not ok: ok = [m for m in res if re.search(r'INTRAVENOS|PARENTERAL|INYECT|PERFUS|INTRAMUSC|INFILTR|PERINEURAL|EPIDURAL', vias(m))]; tipo = 'parenteral'
            ok.sort(key=lambda m: (con_html(m) is None, not m.get('comerc'), m['nregistro']))
            sel = []
            for m in ok[:2 if tipo == 'ocular' else 1]:
                url = con_html(m)
                s = {'nregistro': m['nregistro'], 'nombre': m['nombre'], 'vias': vias(m), 'url': url, 'tipo': tipo}
                if url: open(os.path.join(O, f"{c['id']}__{tipo}__{m['nregistro']}.txt"), 'w').write(m['nombre'] + ' | ' + s['vias'] + '\n' + url + '\n' + secciones(texto(curl(url))))
                sel.append(s)
            json.dump({'id': c['id'], 'familia': fam, 'resultados': len(res), 'tipo': tipo if sel else None, 'sel': sel}, open(idx, 'w'), ensure_ascii=False, indent=1)
            print(f"{fam:12} {c['id'][:30]:30} res={len(res):3} {tipo if sel else 'NADA':10} {[s['nombre'][:45] for s in sel]}", flush=True)
