"""Correcciones a mano de bajar_cima.py (31-oct): productos mal elegidos → se reemplaza por el frasco de partida correcto
(buscado por nombre en CIMA) o se descarta. Reescribe cima/<id>.json y borra los .txt equivocados."""
import json, os, glob, re, urllib.parse
from bajar_cima import curl, texto, secciones, vias, con_html, O
# id → (consulta por nombre CIMA, regex que el nombre debe cumplir, tipo) ; None = sin fuente CIMA útil
FIX = {
 'adrenalina': ('adrenalina', r'^ADRENALINA .*(INYECT|AMPOLLA)', 'parenteral'),
 'lidocaina': ('lidocaina', r'^LIDOCA[IÍ]NA .*(10|20) ?MG/ML .*INYECT', 'parenteral'),
 'ganciclovir': ('cymevene', r'CYMEVENE', 'parenteral'),
 'dexametasona-implante': ('ozurdex', r'OZURDEX', 'ocular'),
 'dexametasona': ('dexametasona', r'^DEXAMETASONA .*(INYECT)', 'parenteral'),
 'ceftazidima': ('ceftazidima', r'^CEFTAZIDIMA .*1 ?G', 'parenteral'),
 'metotrexato': ('metotrexato', r'^METOTREXATO .*(25 ?MG/ML|50 ?MG).*INYECT', 'parenteral'),
 'cotrimoxazol': ('septrin', r'SEPTRIN', 'oral'),
 'isosorbida': None,
 'glicerol': None,
 'fenilefrina-tropicamida-lidocaina': ('fydrane', r'FYDRANE', 'ocular'),
 'fenilefrina-ketorolaco': None,
 'triamcinolona': ('triesence', r'TRIESENCE', 'ocular'),
}
for cid, f in FIX.items():
    for t in glob.glob(os.path.join(O, cid + '__*.txt')): os.remove(t)
    sel = []
    if f:
        q, rx, tipo = f
        res = json.loads(curl('https://cima.aemps.es/cima/rest/medicamentos?nombre=' + urllib.parse.quote(q) + '&pagesize=200') or '{}').get('resultados', [])
        ok = sorted([m for m in res if re.search(rx, m['nombre'].upper())], key=lambda m: (con_html(m) is None, not m.get('comerc'), m['nregistro']))
        for m in ok[:1]:
            url = con_html(m); s = {'nregistro': m['nregistro'], 'nombre': m['nombre'], 'vias': vias(m), 'url': url, 'tipo': tipo}
            if url: open(os.path.join(O, f"{cid}__{tipo}__{m['nregistro']}.txt"), 'w').write(m['nombre'] + ' | ' + s['vias'] + '\n' + url + '\n' + secciones(texto(curl(url))))
            sel.append(s)
    d = json.load(open(os.path.join(O, cid + '.json'))); d['sel'] = sel; d['tipo'] = sel[0]['tipo'] if sel else None; d['corregido'] = True
    json.dump(d, open(os.path.join(O, cid + '.json'), 'w'), ensure_ascii=False, indent=1)
    print(cid, '→', [s['nombre'][:60] for s in sel] or 'SIN CIMA')
