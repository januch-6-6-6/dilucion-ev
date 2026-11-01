"""Segunda pasada ISP: variantes con tilde / otro nombre de PA (tipo 1) y nombres comerciales (tipo 0). Retomable."""
import json, os, time
from isp import buscar
PA = ['ROPIVACAÍNA', 'LIDOCAÍNA', 'BUPIVACAÍNA', 'MEPIVACAÍNA', 'ANFOTERICINA B', 'CARBACHOL', 'ADRENALINA', 'ALTEPLASA RECOMBINANTE',
      'ACTIVADOR', 'AZUL TRIPANO', 'AZUL DE TRIPANO', 'VERDE DE INDOCIANINA', 'TOXINA BOTULÍNICA', 'ÁCIDO TRANEXÁMICO', 'GLICERINA',
      'CEFTAZIDIMA', 'METAZOLAMIDA', 'ACETAZOLAMIDA', 'FAMCICLOVIR', 'VALACICLOVIR', 'DOXICICLINA', 'MINOCICLINA', 'IVERMECTINA', 'PIRIMETAMINA']
COM = ['MIOSTAT', 'MIOCHOL', 'ACTILYSE', 'VISIONBLUE', 'VISION BLUE', 'OZURDEX', 'JETREA', 'BEOVU', 'VABYSMO', 'EYLEA', 'LUCENTIS', 'AVASTIN',
       'TRIESENCE', 'APROKAM', 'MYDRANE', 'OMIDRIA', 'BRILLIANT', 'DIAMOX', 'HYLASE', 'VITRASE', 'BOTOX', 'DYSPORT']
os.makedirs('isp2', exist_ok=True)
for tipo, lista in ((1, PA), (0, COM)):
    for t in lista:
        sal = f"isp2/{tipo}_{t.replace(' ', '_')}.json"
        if os.path.exists(sal): continue
        for intento in range(3):
            try:
                f = buscar(t, tipo=tipo); json.dump(f, open(sal, 'w'), ensure_ascii=False, indent=1)
                print(f'{tipo} {t}: {len(f)}', flush=True); break
            except Exception as e:
                print(f'{tipo} {t}: error {e}', flush=True); time.sleep(20)
        time.sleep(4)
print('FIN', flush=True)
