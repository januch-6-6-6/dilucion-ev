"""Universo chileno: registros ISP vigentes cuyo nombre contiene términos de ojo/oído/nariz. Un proceso, pausas largas (el ISP bloquea si se paraleliza)."""
import isp, json, os, time
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'isp-nombres'); os.makedirs(D,exist_ok=True)
T=['OFTALMICA','OFTÁLMICA','OFTALMICO','OFTÁLMICO','OFTALMICAS','OFTÁLMICAS','OFTÁLMICOS','OFTALMOLÓGICA','COLIRIO','ÓTICA','OTICA','ÓTICO','OTICO','ÓTICAS','NASAL','NASALES','INTRANASAL']
for t in T:
    out=os.path.join(D,t+'.json')
    if os.path.exists(out): continue
    for i in range(5):
        try:
            r=isp.buscar(t,0); json.dump(r,open(out,'w'),ensure_ascii=False,indent=1); print(t,len(r),flush=True); break
        except Exception as e:
            print(t,'error',e,flush=True); time.sleep(60*(i+1))
    time.sleep(10)
