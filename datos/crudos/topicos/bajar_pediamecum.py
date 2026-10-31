"""Pediamécum por componente de lista-isp.json (las combinaciones se buscan por cada principio activo).
Ojo: una ficha inexistente devuelve una página genérica (~131 KB), no 404; por eso se exige que el slug coincida con el componente."""
import subprocess, re, html, os, json, unicodedata
D=os.path.dirname(os.path.abspath(__file__)); O=os.path.join(D,'pediamecum'); os.makedirs(O,exist_ok=True)
B='https://www.aeped.es/comites/cm/pediamecum/principios-activos'
def curl(u): return subprocess.run(['curl','-sL','--max-time','60',u],capture_output=True,text=True).stdout
def n(x): return ''.join(c for c in unicodedata.normalize('NFD',x.lower()) if unicodedata.category(c)!='Mn')
def texto(h):
    t=re.sub(r'(?is)<(script|style).*?</\1>','',h); t=re.sub(r'<br\s*/?>|</p>|</li>|</tr>|</h\d>','\n',t); t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
    t=re.sub(r'[ \t\xa0]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    i=t.find('Volver'); return t[i:] if i>0 else t
# término de búsqueda cuando el nombre ISP no sirve
ALT={'cloruro de sodio':'sodio','hialuronato':'hialur','cromoglicato':'cromogl','salicilato metilo':'salicilato','polimixina b':'polimixina','fenazona':'fenazona'}
# slug elegido a mano cuando hay ficha específica de la vía tópica, o None si Pediamécum no la tiene (revisado 30-oct-2026)
SLUG={'atropina':'atropina-topica-oftalmica','budesonida':'budesonida-nasal','mometasona':'mometasona-furoato-nasal','dexametasona':'dexametasona-topica-oftalmica',
'prednisolona':'prednisolona','neomicina':'neomicina','cloruro de sodio':None,'fenazona':None,'feniramina':None,'fluticasona':None}
EXTRA={'azelastina':['azelastina-oftalmica']}
comp=sorted({c.strip().lower() for x in json.load(open(os.path.join(D,'lista-isp.json'))) for c in x['molecula'].split('+')})
for c in comp:
    slug0=re.sub(r'[^a-z0-9]+','-',n(c)).strip('-'); out=os.path.join(O,slug0+'.txt')
    if os.path.exists(out) or os.path.exists(out+'.sin'): continue
    for e in EXTRA.get(c,[]):
        o2=os.path.join(O,e+'.txt')
        if not os.path.exists(o2): open(o2,'w').write(f'{B}/{e}\n'+texto(curl(f'{B}/{e}'))); print('OK',c,e,flush=True)
    if c in SLUG:
        if SLUG[c] is None: open(out+'.sin','w').write('sin ficha tópica'); print('SIN',c,flush=True); continue
        t=texto(curl(f'{B}/{SLUG[c]}')); open(out,'w').write(f'{B}/{SLUG[c]}\n'+t); print('OK',c,SLUG[c],len(t),flush=True); continue
    q=ALT.get(c,c.split()[0])
    h=curl(f'{B}?texto={q}')
    slugs=[s for s in dict.fromkeys(re.findall(r'principios-activos/([a-z0-9-]+)',h)) if not s.startswith('page-')]
    key=n(q)[:6]; cand=[s for s in slugs if key in n(s)]
    if not cand: open(out+'.sin','w').write(json.dumps(slugs[:10])); print('SIN',c,slugs[:5],flush=True); continue
    s=cand[0]; t=texto(curl(f'{B}/{s}'))
    open(out,'w').write(f'{B}/{s}\n'+t); print('OK',c,s,len(t),flush=True)
