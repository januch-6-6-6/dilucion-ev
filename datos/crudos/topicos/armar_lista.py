"""Lista de moléculas/combinaciones tópicas ojo/oído/nariz desde el registro ISP vigente (F-, B-, FX-; sin homeopáticos H- ni cosméticos)."""
import json,re,collections,unicodedata,os
D=os.path.dirname(os.path.abspath(__file__))
def n(x): return ''.join(c for c in unicodedata.normalize('NFD',x.upper()) if unicodedata.category(c)!='Mn')
SAL=r'\b(CLORHIDRATO|MALEATO|TARTRATO|ACETATO|ACETONIDO|FUROATO|PROPIONATO|FOSFATO( SODICO| DISODICO)?|SODICO|SULFATO|TROMETAMOL|BESILATO|ETABONATO|BROMURO( DE)?|DE|CLORURO|\(COMO\)|COMO|FORMA I|MICRONIZADO|70)\b'
# nombre comercial sin PA en el ISP → PA deducido del nombre (FX-: Saval)
SINPA={'LATOF T':'LATANOPROST//TIMOLOL','LATOF':'LATANOPROST','BRIMOF T':'BRIMONIDINA//TIMOLOL','DORZOLAMIDA':'DORZOLAMIDA'}
def molec(pa,nom):
    if not pa:
        N=n(nom)
        for k,v in SINPA.items():
            if N.startswith(k): pa=v; break
    if not pa: return None
    partes=re.split(r'//|;|/',n(pa))
    out=set()
    for p in partes:
        p=re.sub(r'\(.*?\)','',p); p=re.sub(SAL,' ',p); p=re.sub(r'\s+',' ',p).strip()
        if p in ('BENZALCONIO',''): continue  # conservante declarado como PA
        out.add({'HIDROXIPROPILMETILCELULOSA':'HIPROMELOSA','DEXTRAN':'DEXTRANO','SODIO':'CLORURO DE SODIO','SODIO CROMOGLICATO':'CROMOGLICATO'}.get(p,p))
    return ' + '.join(sorted(out))
def via(nom):
    N=n(nom); v=set()
    if re.search(r'\bOFTALMIC',N): v.add('ojo')
    if re.search(r'\bOTIC',N): v.add('oido')
    if re.search(r'\b(INTRA)?NASAL',N): v.add('nariz')
    return v
def forma(nom):
    N=n(nom)
    for k in ['UNGUENTO','GEL','SUSPENSION','EMULSION','PULVERIZACION','NEBULIZACION','SPRAY','SOLUCION','GOTAS']:
        if k in N: return k.lower()
    return '?'
# decisión de Héctor 30-oct-2026 (DECISIONES.md); Otoseptil no entra porque no tiene PA en el ISP
EXCLUIR={'CALCITONINA','DESMOPRESINA','ESKETAMINA','ALCANFOR + MENTOL + SALICILATO METILO'}
u=json.load(open(os.path.join(D,'isp-universo.json')))
g=collections.defaultdict(lambda:{'vias':set(),'formas':set(),'registros':[]})
sinpa=[]
for r in u:
    if not re.match(r'(F|B|FX)-',r['Producto']): continue
    v=via(r['Nombre'])
    if not v: continue
    m=molec(r['PA'],r['Nombre'])
    if not m: sinpa.append(r); continue
    if m in EXCLUIR: continue
    e=g[m]; e['vias']|=v; e['formas'].add(forma(r['Nombre'])); e['registros'].append({k:r[k] for k in ('Producto','Nombre','Titular','FechaRegistro')})
L=[{'molecula':k,'vias':sorted(e['vias']),'formas':sorted(e['formas']),'n':len(e['registros']),'registros':e['registros']} for k,e in sorted(g.items())]
json.dump(L,open(os.path.join(D,'lista-isp.json'),'w'),ensure_ascii=False,indent=1)
for x in L: print(f"{x['n']:3} {'/'.join(x['vias']):10} {x['molecula'][:55]:55} {','.join(x['formas'])}")
print(len(L),'moléculas/combos;', 'sin PA:',[r['Nombre'] for r in sinpa])
