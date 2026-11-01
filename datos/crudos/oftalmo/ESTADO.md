# Oftalmología (pabellón + orales) — estado de la Fase 0

Rama: **`oftalmologia-v1`** (desde main f9a1ff7). Decisiones de Héctor en [`DECISIONES.md`](DECISIONES.md). **Material de formación, no de prescripción.**

## Hecho (31-oct-2026, noche)

1. **Candidatos:** `candidatos.json`, con 56 en 4 familias: 13 intracamerales, 16 intravítreos, 12 perioculares o bloqueos y 15 orales.
2. **ISP:**
   - `bajar_isp.py` → `isp/` (1.ª pasada por principio activo).
   - `bajar_isp2.py` → `isp2/` (2.ª pasada con variantes con tilde y por nombre comercial: MIOSTAT, ACTILYSE, etc.).
   - Lección: el ISP distingue la tilde (ROPIVACAÍNA ≠ ROPIVACAINA).
   - Lección: no encadenar con `pgrep -f nombre_script`, porque se encuentra a sí mismo.
3. **CIMA:**
   - `bajar_cima.py` → `cima/`. Elige un producto con vía ocular de inyección; si no lo hay, el frasco parenteral de partida; para orales, la vía oral.
   - `corregir_cima.py` corrige 13 selecciones equivocadas (isosorbida mononitrato, geles, Zavicefta, etc.).
4. **DailyMed:** `bajar_dailymed.py` → `dailymed/`. Trae Miostat, Miochol-E, VisionBlue, Omidria, Triesence, TissueBlue, verde de indocianina, Vabysmo, Hylenex, metazolamida y anfotericina liposomal.
5. **SEFH (columna vertebral de pabellón):** en `sefh/`.
   - **Consenso SEFH-SEO-SERV 2025** (Farm Hosp 2025;49:99–108) → `consenso-2025.txt`. Su tabla 4 trae dosis y estabilidad de las intravítreas.
   - **PNT** de cefuroxima intracameral; ceftazidima, vancomicina, voriconazol y ganciclovir intravítreos; bevacizumab, ranibizumab y aflibercept. Traen los pasos de preparación.
6. **Pediamécum:** `bajar_pediamecum.py` → `pediamecum/`, para los orales y algunos inyectables.
7. **Web (2 agentes + Claude):** `web/`. Cada archivo trae URL, referencia y citas textuales.
   - Intraoculares: moxifloxacino, adrenalina y lidocaína intracamerales; bloqueos; subconjuntivales; amikacina, anfotericina, clindamicina, foscarnet y metotrexato intravítreos; antifibróticos; toxina botulínica; alteplasa (EyeWiki).
   - Orales: herpes, blefaritis, Demodex, toxoplasmosis, glaucoma agudo, hipema y corticoides.
   - Los PDF de los agentes están en `pdf/`.
8. **Cobertura:** `cobertura.py` → `COBERTURA.md`.

## Hallazgos para el informe

- **Registrado en Chile:** Aprokam (F-25555/25, cefuroxima intracameral), Mydrane, Eylia, Vabysmo, Lucentis, Hylase 150 UI, verde de indocianina, triamcinolona 40 mg/ml y mitomicina.
- **Moxifloxacino:** los 160 µg/0,1 ml del consenso son **intravítreos**. Intracameral: ASCRS 0,5 mg; Arshinoff 150 µg/0,1 ml (3 ml de Vigamox + 7 ml de BSS); rango publicado de 150 a 500 µg → discrepancia.
- **Alteplasa:** solo EyeWiki (AAO), 6–25 µg/0,1 ml intracameral, y la tabla 4 del consenso (25 µg/0,1 ml intravítreo) → off-label.
- **Guía RCoA/RCOphth 2012 de anestesia:** NO trae dosis. Los volúmenes de bloqueo salen de EyeWiki y artículos.
- **Pendiente de verificar** (lo marcaron los agentes):
  - Autores del PPP de cierre angular (escritos de memoria).
  - Conversión de metilprednisolona del ONTT (de memoria).
  - Posible retractación («withdrawn») del estudio ZEDS.
  - Las citas por WebFetch van recortadas a unos 125 caracteres; cotejarlas con el original.
- **Sin fuente publicada aceptable para los pasos:** amikacina, anfotericina, clindamicina, foscarnet, metotrexato y la reconstitución de mitomicina. Solo hay dosis final, así que el verificador compara solo la concentración.

## Lo que sigue (en orden)

1. Revisar `COBERTURA.md` final (después de la 2.ª pasada del ISP).
2. Escribir `extractos` por candidato y el **informe Fase 0** en `informes/oftalmologia-fase0.md`: tabla de dosis, fuentes, registro ISP, pasos sí/no, discrepancias y estado propuesto (contrastada, fuente única o sin pauta).
3. **Decisiones que le tocan a Héctor:**
   - Qué candidatos sin registro en Chile mostrar (por ejemplo, Miostat si no está).
   - Moxifloxacino: qué dosis mostrar.
   - Si los bloqueos van como fichas o como texto informativo.
   - Si entran los orales con evidencia débil (tranexámico en el hipema, glicerol).
4. Spec en `docs/superpowers/specs/AAAA-MM-DD-oftalmologia-design.md`: `FichaOcular`, verificador de dilución, marca `oftalmologia` en orales y centro `/oftalmologia`. **Héctor la aprueba** → plan → implementación.
