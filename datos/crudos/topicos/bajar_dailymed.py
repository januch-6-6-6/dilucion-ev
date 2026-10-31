"""DailyMed (FDA) para las moléculas sin ficha CIMA. Se busca por nombre en inglés y se exige que el título sea de la vía tópica (OPHTHALMIC/OTIC/NASAL o DROPS)
y que contenga TODOS los componentes (y no otros), para no repetir el error de los orales (fármaco equivocado)."""
import json, subprocess, os, re, html, urllib.parse
D=os.path.dirname(os.path.abspath(__file__)); O=os.path.join(D,'dailymed'); os.makedirs(O,exist_ok=True)
def curl(u): return subprocess.run(['curl','-sL','--max-time','90',u],capture_output=True,text=True).stdout
API='https://dailymed.nlm.nih.gov/dailymed/services/v2'
# molécula ISP → (consulta, componentes en inglés que el título debe traer, vía)
Q={
 'PROPARACAINA':('proparacaine',['PROPARACAINE'],'ojo'),
 'LOTEPREDNOL':('loteprednol',['LOTEPREDNOL'],'ojo'),
 'LOTEPREDNOL + TOBRAMICINA':('loteprednol tobramycin',['LOTEPREDNOL','TOBRAMYCIN'],'ojo'),
 'BEPOTASTINA':('bepotastine',['BEPOTASTINE'],'ojo'),
 'LEVOFLOXACINO':('levofloxacin',['LEVOFLOXACIN'],'ojo'),
 'NAFAZOLINA':('naphazoline',['NAPHAZOLINE'],'ojo'),
 'FENIRAMINA + NAFAZOLINA':('naphazoline pheniramine',['NAPHAZOLINE','PHENIRAMINE'],'ojo'),
 'CIPROFLOXACINO + DEXAMETASONA':('ciprofloxacin dexamethasone',['CIPROFLOXACIN','DEXAMETHASONE'],'oido'),
 'BACITRACINA + NEOMICINA + POLIMIXINA B':('neomycin and polymyxin b sulfates and bacitracin zinc',['NEOMYCIN','POLYMYXIN','BACITRACIN'],'ojo'),
 'CALCITONINA':('calcitonin',['CALCITONIN'],'nariz'),
 'CROMOGLICATO':('cromolyn',['CROMOLYN'],'ojo'),
 'DEXTRANO + HIPROMELOSA':('dextran hypromellose',['DEXTRAN','HYPROMELLOSE'],'ojo'),
 'DEXTRANO + HIPROMELOSA + NAFAZOLINA':('naphazoline dextran',['NAPHAZOLINE','DEXTRAN','HYPROMELLOSE'],'ojo'),
 'HIALURONATO':('sodium hyaluronate',['HYALURON'],'ojo'),
 'BETAMETASONA':('betamethasone ophthalmic',['BETAMETHASONE'],'ojo'),
 'GATIFLOXACINO + PREDNISOLONA':('gatifloxacin',['GATIFLOXACIN'],'ojo'),  # en EE. UU. solo gatifloxacino solo
}
VIA={'ojo':r'OPHTHALMIC|EYE|SOLUTION/ DROPS|SUSPENSION/ DROPS|OINTMENT','oido':r'OTIC|EAR|DROPS','nariz':r'NASAL|SPRAY'}
NO=['HYDROCORTISONE','GLYCERIN','PHENIRAMINE','VETERINARY','HOMEOPATH','KETOGLUTARIC']  # componentes/productos que no corresponden
def txt(x):
    x=re.sub(r'(?is)<(script|style).*?</\1>','',x); x=re.sub(r'(?i)</(paragraph|title|item|tr)>','\n',x)
    return re.sub(r'\n\s*\n+','\n',re.sub(r'[ \t]+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))))
for mol,(q,comp,via) in Q.items():
    slug=re.sub(r'[^a-z0-9]+','-',mol.lower()).strip('-'); out=os.path.join(O,slug+'.txt')
    if os.path.exists(out) or os.path.exists(out+'.sin'): continue
    d=json.loads(curl(f'{API}/spls.json?drug_name={urllib.parse.quote(q)}&pagesize=100') or '{}').get('data',[])
    ok=[s for s in d if all(c in s['title'].upper() for c in comp) and not any(x in s['title'].upper() for x in NO if x not in ' '.join(comp)) and re.search(VIA[via],s['title'].upper())]
    if not ok: open(out+'.sin','w').write(json.dumps([s['title'] for s in d[:15]],indent=1)); print('SIN',mol,len(d),flush=True); continue
    s=ok[0]; t=txt(curl(f"{API}/spls/{s['setid']}.xml"))
    open(out,'w').write(f"{s['title']}\nhttps://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={s['setid']}\n"+t[:40000])
    print('OK',mol,'|',s['title'][:80],flush=True)
