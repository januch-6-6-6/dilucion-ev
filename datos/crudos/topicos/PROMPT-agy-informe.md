Usa SOLO las herramientas de leer, listar y escribir archivos. NO ejecutes comandos de terminal (no tienes permiso y la tarea se corta si lo intentas).

# Tarea: borrador del informe de discrepancias — tópicos ojo/oído/nariz (app Dilución EV)

Contexto: la app «Dilución EV» (material de FORMACIÓN, no de prescripción) suma medicamentos tópicos de ojo, oído y nariz. Ya se reunieron las fuentes de 84 moléculas o combinaciones registradas en Chile (ISP). Tu trabajo es leer las fuentes de cada una y redactar un BORRADOR de informe que después revisa un humano línea por línea. No inventes datos: todo lo que escribas debe salir textual de los extractos.

## Archivos (todos en /home/h/dilucion-ev/datos/crudos/topicos/)

- `extractos.md` — UNA sección `## Molécula` por cada una de las 84, con: presentaciones ISP vigentes en Chile, CIMA (ficha técnica española: 4.2 posología, 4.3 contraindicaciones, 6.3 validez tras abrir), DailyMed (FDA, en inglés) y Pediamécum (guía pediátrica española, por componente). Es largo: léelo por partes.
- `COBERTURA.md` — qué fuentes tiene cada molécula.
- Modelo de formato y tono (léelo primero, sus primeras ~120 líneas): `/home/h/dilucion-ev/informes/orales-discrepancias-cima-pediamecum.md`.
- Si un extracto dice «[…recortado]» y necesitas el resto, el texto completo está en `cima/<slug>__<via>__<nregistro>.txt`, `dailymed/<slug>.txt` o `pediamecum/<componente>.txt`.

## Qué comparar en cada molécula

1. **Posología adulto**: nº de gotas (o aplicaciones / pulverizaciones / cm de ungüento), en qué ojo/oído/fosa, frecuencia, duración máxima del tratamiento.
2. **Pediatría**: edad mínima autorizada, pauta pediátrica, y si Pediamécum da una pauta que la ficha técnica no autoriza (off-label).
3. **Validez tras abrir el envase** (días) y conservación (nevera sí/no). Esto alimenta una calculadora de «cuántos días dura el frasco», así que anota también volumen del envase si aparece.
4. **Alertas graves** solamente: efectos sistémicos (betabloqueantes en asma/bradicardia, vasoconstrictores nasales en <6 años o >5–7 días por efecto rebote, anestésicos oftálmicos que NO se entregan al paciente, corticoides oftálmicos y glaucoma/herpes, aminoglucósidos óticos con tímpano perforado, etc.).
5. **Concentración**: ¿la de Chile (ISP) coincide con la de la ficha CIMA/DailyMed? Si no, márcalo (la pauta puede depender de la concentración).
6. **Fuente equivocada**: si la ficha bajada NO corresponde a la molécula o a la vía (por ejemplo, un nasal en vez de oftálmico, o un producto con un componente extra como glicerina), márcalo con ⚠️ — esto pasó en el proyecto anterior y es el hallazgo más valioso.

## Formato de salida

Escribe el archivo `/home/h/dilucion-ev/datos/crudos/topicos/INFORME-BORRADOR-agy.md`:

- Encabezado como el modelo (título, fecha 30-oct-2026, «borrador generado por Antigravity, pendiente de revisión», leyenda 🟢🟡🔴⚪⚠️).
- Sección «Resumen» con los conteos por color (calcúlalos al final) y la lista de 🔴 y de ⚠️.
- Una sección por grupo: **Glaucoma** (prostaglandinas, betabloqueantes, inhibidores de anhidrasa carbónica, alfa-agonistas y sus combinaciones), **Antiinfecciosos oftálmicos**, **Corticoides y combinaciones antibiótico+corticoide oftálmicas**, **Antialérgicos y vasoconstrictores oftálmicos**, **AINE oftálmicos**, **Midriáticos/ciclopléjicos y anestésicos**, **Lubricantes y otros oftálmicos**, **Óticos**, **Nasales tópicos**, **Nasales de efecto sistémico** (calcitonina, desmopresina, esketamina), **Otros**.
- Por molécula, un ítem así:
  `- **Nombre** 🟢/🟡/🔴/⚪/⚠️ — Adulto: … (fuente). Pediatría: … (fuente). Validez tras abrir: … . Alertas: … . Diferencias: … .` (2 a 6 líneas; cita la fuente de cada dato entre paréntesis: CIMA, FDA, Pediamécum, ISP).
- Las 84 moléculas deben aparecer exactamente una vez. Si alguna no tiene fuente de posología, ponla ⚪ y dilo.
- Al final: «Reglas que se desprenden para el diseño» y «Decisiones que necesita Héctor», igual que el modelo.

Trabaja por partes: escribe el archivo con las primeras secciones y luego ve agregando el resto (reescribiendo el archivo completo cada vez), para que si te cortas quede lo avanzado. Al terminar responde solo con: cuántas moléculas cubriste y cuántas de cada color.
