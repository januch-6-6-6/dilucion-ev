"""DailyMed (FDA) para productos de pabellón sin ficha CIMA ocular. Se exige que el título traiga el término clave."""
import json, subprocess, os, re, html, urllib.parse
D = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(D, 'dailymed')
def curl(u): return subprocess.run(['curl', '-sL', '--max-time', '90', u], capture_output=True, text=True).stdout
API = 'https://dailymed.nlm.nih.gov/dailymed/services/v2'
# id → (consulta, términos que el título debe traer)
Q = {
 'carbacol': ('miostat', ['CARBACHOL']),
 'acetilcolina': ('miochol', ['ACETYLCHOLINE']),
 'azul-tripano': ('visionblue', ['TRYPAN']),
 'fenilefrina-ketorolaco': ('omidria', ['PHENYLEPHRINE', 'KETOROLAC']),
 'triamcinolona': ('triesence', ['TRIAMCINOLONE']),
 'verde-indocianina': ('indocyanine green', ['INDOCYANINE']),
 'azul-brillante': ('brilliant blue', ['BRILLIANT']),
 'faricimab': ('vabysmo', ['FARICIMAB']),
 'ocriplasmina': ('jetrea', ['OCRIPLASMIN']),
 'hialuronidasa': ('hylenex', ['HYALURONIDASE']),
 'metazolamida': ('methazolamide', ['METHAZOLAMIDE']),
 'glicerol': ('osmoglyn', ['GLYCERIN']),
 'adrenalina': ('epinephrine intraocular', ['EPINEPHRINE']),
 'moxifloxacino': ('moxifloxacin intracameral', ['MOXIFLOXACIN']),
 'dexametasona-intraocular': ('dexycu', ['DEXAMETHASONE']),
 'anfotericina-b': ('amphotericin b', ['AMPHOTERICIN']),
 'lidocaina': ('lidocaine hydrochloride jelly ophthalmic', ['LIDOCAINE']),
}
def txt(x):
    x = re.sub(r'(?is)<(script|style).*?</\1>', '', x); x = re.sub(r'(?i)</(paragraph|title|item|tr)>', '\n', x)
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))))
for k, (q, comp) in Q.items():
    out = os.path.join(O, k + '.txt')
    if os.path.exists(out) or os.path.exists(out + '.sin'): continue
    d = json.loads(curl(f'{API}/spls.json?drug_name={urllib.parse.quote(q)}&pagesize=100') or '{}').get('data', [])
    ok = [s for s in d if all(c in s['title'].upper() for c in comp)]
    if not ok: open(out + '.sin', 'w').write(json.dumps([s['title'] for s in d[:15]], indent=1)); print('SIN', k, len(d), flush=True); continue
    s = ok[0]; t = txt(curl(f"{API}/spls/{s['setid']}.xml"))
    open(out, 'w').write(f"{s['title']}\nhttps://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={s['setid']}\n" + t[:40000])
    print('OK', k, '|', s['title'][:90], flush=True)
