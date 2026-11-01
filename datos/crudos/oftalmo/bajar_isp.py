"""Fase 0 oftalmología: busca cada candidato por principio activo en el ISP (tipo 1). Retomable."""
import json, os, time, sys
from isp import buscar
d = json.load(open('candidatos.json'))
vistos = set()
for fam, lista in d.items():
    if fam.startswith('_'): continue
    for c in lista:
        pa = c['pa']
        if pa in vistos: continue
        vistos.add(pa)
        sal = f"isp/{pa.replace(' ', '_')}.json"
        if os.path.exists(sal): continue
        for intento in range(3):
            try:
                filas = buscar(pa, tipo=1)
                json.dump(filas, open(sal, 'w'), ensure_ascii=False, indent=1)
                print(f'{pa}: {len(filas)}', flush=True)
                break
            except Exception as e:
                print(f'{pa}: error {e}', flush=True); time.sleep(20)
        time.sleep(4)
print('FIN', flush=True)
