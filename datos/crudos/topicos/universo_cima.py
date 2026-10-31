"""Universo tópico ojo/oído/nariz: todos los productos CIMA de ATC S01, S02, S03 y R01A (curl; urllib se cuelga con CIMA)."""
import json, subprocess, sys, os
D=os.path.dirname(os.path.abspath(__file__))
def get(url):
    return json.loads(subprocess.run(['curl','-s','-m','60',url],capture_output=True,text=True).stdout)
todo=[]
for atc in ['S01','S02','S03','R01A']:
    p=1
    while True:
        d=get(f'https://cima.aemps.es/cima/rest/medicamentos?atc={atc}&pagina={p}')
        r=d.get('resultados',[])
        for x in r: x['_atc_q']=atc
        todo+=r
        if p*d.get('tamanioPagina',25)>=d.get('totalFilas',0) or not r: break
        p+=1
    print(atc,'ok',file=sys.stderr)
json.dump(todo,open(os.path.join(D,'cima-universo.json'),'w'),ensure_ascii=False,indent=1)
print(len(todo))
