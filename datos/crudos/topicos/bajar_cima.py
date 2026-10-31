"""Fichas técnicas CIMA por molécula de lista-isp.json: el vtm debe coincidir EXACTO (lección de orales: practiv1 parcial trae el fármaco equivocado).
Guarda secciones 4.1-4.9 (posología, contraindicaciones, alertas) y 6.3-6.6 (validez tras apertura, conservación, manejo)."""
import json, subprocess, os, re, html, unicodedata, urllib.parse
D=os.path.dirname(os.path.abspath(__file__)); O=os.path.join(D,'cima'); os.makedirs(O,exist_ok=True)
def n(x): return ''.join(c for c in unicodedata.normalize('NFD',x.upper()) if unicodedata.category(c)!='Mn')
def curl(u): return subprocess.run(['curl','-sL','--max-time','60',u],capture_output=True,text=True).stdout
def clave(m): return frozenset(re.sub(r'\s+',' ',p).strip() for p in n(m).split('+') if p.strip())
# nombre CIMA cuando difiere del ISP
ALIAS={'ATROPINA':'ATROPINA SULFATO','IPRATROPIO':'BROMURO IPRATROPIO','HIALURONATO':'ACIDO HIALURONICO','CROMOGLICATO':'CROMOGLICICO ACIDO','CLORURO DE SODIO':'SODIO CLORURO'}
def via_cima(m):
    f=n(m['formaFarmaceutica']['nombre']); v=' '.join(n(x['nombre']) for x in m.get('viasAdministracion',[]))
    if 'OTIC' in f or 'OTIC' in v: return 'oido'
    if 'NASAL' in f or 'NASAL' in v: return 'nariz'
    if 'OFTALM' in f or 'COLIRIO' in f or 'OFTALM' in v: return 'ojo'
    return None
def texto(h):
    h=re.sub(r'(?is)<(script|style).*?</\1>','',h)
    h=re.sub(r'(?i)<br\s*/?>|</p>|</tr>|</h\d>|</li>','\n',h); h=re.sub(r'(?i)</t[dh]>',' | ',h)
    h=html.unescape(re.sub(r'<[^>]+>','',h))
    return re.sub(r'\n\s*\n+','\n',re.sub(r'[ \t\xa0]+',' ',h))
def secciones(t):
    out=[]
    for a,b in ((r'\n\s*4\.1\.? ',r'\n\s*5\.1\.? '),(r'\n\s*6\.3\.? ',r'\n\s*7\.? ')):
        m=re.search(a,t); e=re.search(b,t[m.end():]) if m else None
        if m: out.append(t[m.start():m.end()+e.start()] if e else t[m.start():m.start()+15000])
    return '\n'.join(out) if out else t[:30000]
def buscar(mol):
    """Candidatos: primero el universo ATC ya bajado; si no, la API por principio activo."""
    k=clave(ALIAS.get(mol,mol))
    U=json.load(open(os.path.join(D,'cima-universo.json')))
    c=[m for m in U if clave((m.get('vtm') or {}).get('nombre','')) == k]
    if not c:
        ps=sorted(k); q='practiv1='+urllib.parse.quote(ps[0].lower())+('&practiv2='+urllib.parse.quote(ps[1].lower()) if len(ps)>1 else '')
        try: c=[m for m in json.loads(curl('https://cima.aemps.es/cima/rest/medicamentos?'+q+'&pagesize=100')).get('resultados',[]) if clave((m.get('vtm') or {}).get('nombre',''))==k]
        except Exception: c=[]
    return [m for m in c if via_cima(m)]
L=json.load(open(os.path.join(D,'lista-isp.json')))
for x in L:
    mol=x['molecula']; slug=re.sub(r'[^a-z0-9]+','-',n(mol).lower()).strip('-')
    idx=os.path.join(O,slug+'.json')
    if os.path.exists(idx): continue
    c=buscar(mol); sel=[]
    for v in x['vias']:
        cv=sorted([m for m in c if via_cima(m)==v], key=lambda m:(not any(d['tipo']==1 and d.get('urlHtml') for d in m.get('docs',[])), not m.get('comerc'), m['nregistro']))
        for m in cv[:1]:
            url=next((d['urlHtml'] for d in m.get('docs',[]) if d['tipo']==1 and d.get('urlHtml')),None)
            s={'via':v,'nregistro':m['nregistro'],'nombre':m['nombre'],'forma':m['formaFarmaceutica']['nombre'],'url':url}
            if url:
                open(os.path.join(O,f"{slug}__{v}__{m['nregistro']}.txt"),'w').write(m['nombre']+' | '+s['forma']+'\n'+url+'\n'+secciones(texto(curl(url))))
            sel.append(s)
    json.dump({'molecula':mol,'vias_isp':x['vias'],'candidatos':len(c),'sel':sel},open(idx,'w'),ensure_ascii=False,indent=1)
    print(f"{mol[:45]:45} cand={len(c):3} sel={[s['via'] for s in sel]}",flush=True)
