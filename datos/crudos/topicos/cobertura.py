"""Matriz de cobertura de fuentes por molécula → COBERTURA.md."""
import json,glob,os,re,unicodedata
D=os.path.dirname(os.path.abspath(__file__))
def n(x): return ''.join(c for c in unicodedata.normalize('NFD',x.lower()) if unicodedata.category(c)!='Mn')
def slug(m): return re.sub(r'[^a-z0-9]+','-',n(m)).strip('-')
L=json.load(open(os.path.join(D,'lista-isp.json')))
SIST={'CALCITONINA','DESMOPRESINA','ESKETAMINA'}  # vía nasal con efecto sistémico
rows=[];tot={'cima':0,'dm':0,'ped':0,'dos':0,'una':0,'cero':0}
for x in L:
    m=x['molecula']; s=slug(m)
    cj=os.path.join(D,'cima',s+'.json'); cima=os.path.exists(cj) and any(z['url'] for z in json.load(open(cj))['sel'])
    dm=os.path.exists(os.path.join(D,'dailymed',s+'.txt'))
    comps=[slug(c) for c in m.split('+')]
    ped=[c for c in comps if os.path.exists(os.path.join(D,'pediamecum',c+'.txt'))]
    inst=1+cima+dm  # ISP siempre (presentación registrada)
    dosis=cima+dm+bool(ped)  # fuentes con posología
    tot['cima']+=cima; tot['dm']+=dm; tot['ped']+=bool(ped)
    k='dos' if dosis>=2 else 'una' if dosis==1 else 'cero'; tot[k]+=1
    rows.append(f"| {m.title()} | {'/'.join(x['vias'])} | {', '.join(x['formas'])} | {x['n']} | {'✔' if cima else '—'} | {'✔' if dm else '—'} | {f'{len(ped)}/{len(comps)}' if ped else '—'} | {dosis} | {'sistémico' if m in SIST else ''} |")
out=["# Cobertura de fuentes — tópicos ojo/oído/nariz","",f"Generado por `cobertura.py`. Universo = registros ISP vigentes (F-, B-, FX-) con OFTÁLMICA/ÓTICA/NASAL en el nombre: **{len(L)} moléculas o combinaciones**.","",
f"- CIMA (ficha técnica española, vtm exacto): **{tot['cima']}**",f"- DailyMed (FDA) para las que no están en CIMA: **{tot['dm']}**",f"- Pediamécum (al menos un componente): **{tot['ped']}**",
f"- Con ≥2 fuentes de posología: **{tot['dos']}** · con 1: **{tot['una']}** · **sin ninguna: {tot['cero']}** (solo registro ISP)","",
"Pediamécum es por principio activo: «2/3» = 2 de 3 componentes con ficha (no siempre trae la vía tópica; ver el informe).","",
"| Molécula | Vía | Formas | Reg. ISP | CIMA | DailyMed | Pediamécum | Fuentes de dosis | Nota |","|---|---|---|---|---|---|---|---|---|"]+rows
open(os.path.join(D,'COBERTURA.md'),'w').write('\n'.join(out)+'\n'); print('\n'.join(out[:9]))
print([r.split('|')[1] for r in rows if r.split('|')[8].strip()=='0'])
