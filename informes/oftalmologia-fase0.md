# Oftalmología (pabellón + orales) — informe de la Fase 0 (BORRADOR, 31-oct-2026)

> **Material de formación, no de prescripción.** Borrador para que Héctor lo revise antes de la spec. Las cifras salen de las fuentes crudas de `datos/crudos/oftalmo/`: CIMA, DailyMed, SEFH, Pediamécum y `web/` con citas textuales. **Todavía no hubo revisión molécula por molécula como en tópicos**; eso se hace al escribir los lotes de datos.

## 1. Resumen

- **56 candidatos:** 13 intracamerales, 16 intravítreos, 12 perioculares o bloqueos y 15 orales. Están en `candidatos.json`, y la tabla completa en `datos/crudos/oftalmo/COBERTURA.md`.
- **Con registro vigente en Chile:** 43.
- **Sin registro en Chile (12):** carbacol (**Miostat**), acetilcolina (**Miochol**), Omidria, azul tripano (VisionBlue), azul brillante, brolucizumab (Beovu), anfotericina B, ocriplasmina (Jetrea), ropivacaína, metazolamida, glicerol oral y famciclovir.
  - Ojo: el ISP no siempre deja buscar los dispositivos médicos, como los colorantes de cápsula. Que no aparezcan **no prueba** que no se usen en Chile; pueden entrar como dispositivo o por importación.
- **Sin ninguna fuente:** isosorbida. Se **descarta**: en Chile solo existe el nitrato (Ismo), no el osmótico.
- **Columna vertebral para pabellón:** el **Consenso SEFH-SEO-SERV 2025** sobre preparaciones intraoculares (Farm Hosp 2025;49:99–108) y los **PNT de la SEFH**, que traen los pasos de preparación. Son fuentes españolas, publicadas y de sociedades científicas.

## 2. Hallazgos importantes

1. **Miostat y Miochol no están registrados en Chile**, aunque Héctor los nombra como típicos. Hay ficha de la FDA para Miostat (0,5 ml intracameral, carbacol 0,01 %) y de CIMA para la acetilcolina Cusí 10 mg/ml. → **Decisión 1.**
2. **Actilyse sí está en Chile** (B-936/25). El ISP lo registra como «activador del plasminógeno tisular humano recombinante», no como alteplasa. Todo uso ocular es **off-label**:
   - Intracameral: 6–25 µg en 0,1 ml (EyeWiki/AAO).
   - Intravítreo: 25 µg/0,1 ml (tabla 4 del consenso).
   - Subretiniano: 25–50 µg en 0,1–0,2 ml (EyeWiki).
   - Preparación (EyeWiki): reconstituir a 1 mg/ml, diluir con suero sin conservantes y usar de inmediato. **El riesgo principal es la hemorragia (hipema)**, que depende de la dosis.
3. **Cefuroxima intracameral: en Chile está APROKAM** (F-25555/25), listo para 1 mg/0,1 ml (ficha CIMA de Prokam/Ximaract: «NO INYECTAR MÁS DE LA DOSIS RECOMENDADA»). El PNT de la SEFH describe la alternativa desde un frasco de 750 mg: reconstituir con 7,5 ml (100 mg/ml), tomar 1 ml y llevar a 10 ml (10 mg/ml), lo que da 1 mg/0,1 ml. Es el ejemplo ideal para el verificador.
4. **Moxifloxacino intracameral, discrepancia grande.** Los 160 µg/0,1 ml (Fenniri 2026, no el consenso) son **intravítreos**. Para la cámara anterior las fuentes van de 150 a 500 µg:
   - ASCRS: 0,5 mg.
   - Arshinoff 2016: 150 µg/0,1 ml (3 ml de Vigamox + 7 ml de BSS).
   - Con 100 µg hubo un fracaso.
   - → **Decisión 2.** (Corrección del 1-nov: el consenso SEFH no menciona moxifloxacino; los 160 µg/0,1 ml intravítreos salen de Fenniri 2026.)
5. **Mydrane está en Chile** (F-25730/25): 0,2 ml intracameral, dosis única, sin dosis adicionales porque aumenta la pérdida endotelial (CIMA Fydrane).
6. **Anti-VEGF:**
   - Lucentis: 0,5 mg/0,05 ml; 0,2 mg/0,02 ml en recién nacidos pretérmino con ROP.
   - Eylia: 2 mg/0,05 ml, y 8 mg/0,07 ml registrado en Chile.
   - Vabysmo: 6 mg/0,05 ml.
   - Avastin: 1,25 mg/0,05 ml, **off-label** y fraccionado (PNT SEFH 25 mg/ml).
   - Alerta: **la jeringa trae más volumen que la dosis; hay que eliminar el exceso** (CIMA).
7. **Antibióticos intravítreos de endoftalmitis** (consenso y PNT SEFH):
   - Vancomicina 1 mg/0,1 ml + ceftazidima 2 mg/0,1 ml. **Ojo: el borrador de candidatos decía 2,25 mg; la SEFH dice 2 mg**, así que hay discrepancia de fuentes.
   - Amikacina 0,4 mg/0,1 ml, con **riesgo de infarto macular**.
   - Antifúngicos: voriconazol 100 µg/0,1 ml (PNT); anfotericina 5–10 µg/0,1 ml.
   - **Vancomicina intracameral: HORV** (vasculitis retiniana oclusiva hemorrágica, 33 de 36 ojos en Witkin 2017) → alerta roja.
8. **Bloqueos:** la guía RCoA/RCOphth 2012 **no trae dosis**. Los volúmenes salen de EyeWiki y artículos: retrobulbar 2–5 ml, peribulbar 6–10 ml, subtenoniano 2–5 ml; lidocaína 2 % ± bupivacaína 0,5–0,75 %; hialuronidasa en dosis variable. → **Decisión 3.**
9. **Orales:**
   - Herpes (AAO-OMIG 2014, HEDS): aciclovir 400 mg c/12 h de profilaxis; dosis de tratamiento de queratitis y zóster.
   - Blefaritis: doxiciclina 50–100 mg (TFOS), azitromicina en pulsos, ivermectina 200 µg/kg en Demodex. **Contraindicadas las tetraciclinas en menores de 8 años y en el embarazo.**
   - Toxoplasmosis (CDC y Dunay 2018).
   - Glaucoma agudo: acetazolamida 500 mg y luego 250 mg c/6 h; pediátrica 10–20 mg/kg/día.
   - Hipema: tranexámico 75 mg/kg/día; Cochrane encuentra menos resangrado sin mejor visión.
   - Corticoides en uveítis, ONTT y arteritis de células gigantes.
   - Muchas de estas pautas **no están en la ficha técnica** y se mostrarían como uso oftálmico con su guía como fuente.

## 3. Pendiente de verificación (lo marcaron los agentes)

- Autores del PPP de cierre angular de la AAO y conversión de metilprednisolona del ONTT: los escribió de memoria un agente. **No usarlos hasta cotejarlos.**
- Estudio ZEDS (valaciclovir en el zóster oftálmico): un repositorio lo marca como «withdrawn». Hay que verificarlo antes de citarlo.
- Las citas obtenidas con WebFetch (EyeWiki, CDC, NHS) quedaron recortadas a unos 125 caracteres; cotejarlas con el original.
- El filtro del ISP para adrenalina y lidocaína se cuela con productos dentales (Alphacaine…). Hay que elegir a mano el frasco de partida: adrenalina 1 mg/ml en ampolla y lidocaína al 1–2 % sin conservantes.
- No hay fuente aceptable con **pasos** para amikacina, anfotericina, clindamicina, foscarnet, metotrexato ni para reconstituir la mitomicina. En esos casos se muestra solo la dosis final y el verificador compara solo la concentración.

## 4. Decisiones para Héctor

1. **Miostat y Miochol (sin registro en Chile):** ¿se muestran como «no registrado en Chile», con la ficha FDA o CIMA, porque en el pabellón se usan (importación o uso compasivo), o se dejan fuera? Pasa lo mismo con VisionBlue, azul brillante, Omidria, Beovu, Jetrea y ropivacaína.
2. **Moxifloxacino intracameral:** ¿se muestra el rango publicado (150–500 µg/0,1 ml) con la dosis de la ASCRS (0,5 mg) como referencia, o se deja sin pauta por la discrepancia?
3. **Bloqueos y subconjuntivales:** ¿fichas con volúmenes como texto informativo (sin verificador), o se dejan fuera de la v1?
4. **Orales con evidencia débil** (tranexámico en el hipema, glicerol oral sin registro, ivermectina en Demodex): ¿se incluyen con aviso o se dejan fuera?
5. **Antifibróticos y toxina botulínica** (mitomicina, 5-FU, Botox): son muy delicados y cambian según el protocolo del cirujano. ¿Van en la v1?

**Respuestas de Héctor (1-nov-2026):** 1) se muestran con aviso «No registrado en Chile»; 2) rango + los 2 protocolos; 3) bloqueos y subconjuntivales sí, como texto sin verificador; 4) orales de evidencia débil fuera de la v1; 5) antifibróticos y toxina sí, como alto riesgo. Detalle en `datos/crudos/oftalmo/DECISIONES.md`.

## 5. Siguiente paso

Con las decisiones de Héctor: spec (`FichaOcular` + verificador + marca `oftalmologia` + centro `/oftalmologia`) → plan → lotes de datos con revisión molécula por molécula, igual que en tópicos.
