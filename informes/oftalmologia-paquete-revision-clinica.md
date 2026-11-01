# Oftalmología (Dilución EV): paquete de revisión clínica

> Para la enfermera/o de pabellón oftalmológico y, si se puede, un oftalmólogo. Material de formación, no de prescripción. Nada de esto se ha publicado: la sección vive en la rama `oftalmologia-v1`.
> El detalle ficha por ficha está en `oftalmologia-revision.md` (tabla completa con fuentes). Aquí solo van las cosas donde un error pesa más.

## Qué hace la sección (30 segundos)

- **41 fichas de pabellón** (13 intracamerales, 16 intravítreas, 4 bloqueos, 5 perioculares, 3 antifibróticos/toxina) + **11 orales** de uso oftálmico, todas con la marca «Alto riesgo» y el aviso «Verifica el protocolo de tu pabellón».
- La app **muestra lo que dice la fuente publicada** (ficha técnica, PNT de la SEFH, consenso SEFH-SEO-SERV 2025, EyeWiki…) con su cita. **No propone preparaciones.**
- El **verificador** solo compara: la persona escribe los pasos que hizo (volumen tras disolver, tomar X ml y llevar a Y ml) y la app dice si la concentración por 0,1 ml coincide (±5 %) con la fuente. Si no coincide: «NO coincide… No administres; revisa los pasos».
- Hay 12 fichas con protocolo de preparación citado (verificables); el resto son solo informativas.

## Lo que más necesita ojos clínicos (por prioridad)

### 1. Toxina botulínica (`toxina-botulinica`) — fuente única
- La ficha usa la etiqueta FDA (vial de 100 U; diluciones con 8, 4 y 2 ml) y muestra **rangos de dosis en U por 0,1 ml**.
- **Duda:** «1,25–2,5 U por 0,1 ml» puede estar leyendo como rango de *concentración* lo que la etiqueta da como rango de *dosis por sitio/músculo* (0,05–0,15 ml por músculo). ¿Se entiende bien así en pabellón, o conviene mostrar solo la dosis por sitio?
- ¿Se usa en tu pabellón con otra marca u otra dilución?

### 2. Moxifloxacino intracameral — sin dosis única aceptada
- Se muestran **dos protocolos**: ASCRS 2023 (0,5 mg = 0,1 ml al 0,5 % sin diluir, o 0,5 ml al 0,1 %) y Arshinoff (3 ml → 10 ml, 150 µg/0,1 ml; se inyectan 0,3–0,4 ml). Rango publicado: 150–500 µg.
- **Duda 1:** ¿cuál usa tu pabellón? ¿Se muestran bien los dos?
- **Duda 2 (conocida):** la alternativa «0,5 ml al 0,1 %» del ASCRS hoy sale **en rojo** en el verificador aunque es válida (queda pendiente de arreglar).
- La presentación modelada (Megrelan 0,5 %, 15 mg/3 ml) es un supuesto: el ISP no informa el contenido del envase. ¿Es el envase real?

### 3. Antifibróticos: mitomicina C y 5-FU — alto riesgo, «según el protocolo del cirujano»
- Mitomicina esponja: **0,1–0,5 mg/ml** (corregido en la revisión final). 5-FU: 2 dosis off-label.
- **No hay pasos de preparación** (ninguna fuente aceptable los da); el verificador solo compara concentraciones.
- ¿Las concentraciones coinciden con lo que se usa? ¿Falta alguna indicación usual (trabeculectomía, pterigión)?

### 4. Dosis marcadas «off-label» (hay 36 en 23 fichas)
Las más delicadas: adrenalina intracameral (tres autores con concentraciones distintas, ficha con discrepancia), lidocaína intracameral (4), alteplasa (5), mitomicina (3), anfotericina B (no registrada), foscarnet/ganciclovir (2 mg/0,1 ml del PNT frente a 200/400 µg de una tabla de estabilidad del consenso), voriconazol y ceftazidima (la fuente indica 9,4 ml y 19 ml de agua para dejar 10 y 20 ml).
- ¿Hay alguna cifra que te suene fuera de lo habitual?

### 5. Productos sin registro en Chile (9, se muestran con aviso)
acetilcolina (Miochol-E), carbacol, azul brillante, azul tripano, brolucizumab, fenilefrina-ketorolaco, ocriplasmina, ropivacaína, anfotericina B.
- ¿Alguno se usa realmente por importación/uso compasivo en tu pabellón? ¿Alguno sobra?

### 6. Fichas sin cifras
- `mepivacaina` y `verde-indocianina`: sin pauta (ninguna fuente aceptable). ¿Prefieres sacarlas o dejarlas como ficha informativa?

## Preguntas generales para cerrar

1. ¿Falta algún medicamento de pabellón que uses a menudo?
2. ¿El orden de pestañas (Dosis · Preparación · Conservación · Alertas · Discrepancias · Fuentes) te sirve en la práctica?
3. ¿El verificador te parece útil, o riesgoso por dar sensación de seguridad? (Si lo ves riesgoso, se puede dejar solo la ficha.)
4. ¿Los textos de alerta y de aviso son claros para una pabellonera o un TENS?

## Qué se espera de la revisión
Marcar cada punto con **OK / corregir (qué) / sacar**. Con eso se corrige y recién ahí se decide publicar. La ficha dice «Revisión clínica: pendiente» hasta que alguien firme (`meta.revisadoPor`).

## Para Héctor (no es para la enfermera)
- Antes de publicar: borrar la rama de respaldo `oftalmologia-v1-respaldo` (guarda los crudos con copyright) y decidir merge a main.
- Pendientes de verificar antes de citar: estudio ZEDS (valaciclovir en herpes zóster oftálmico, «withdrawn»), autores de la PPP de cierre angular de la AAO y la conversión de metilprednisolona del ONTT. Hoy **no se citan** en la app.
- Minors diferidos M1–M7 (verificador y accesibilidad) están en el resumen de la sesión del 1-nov.
