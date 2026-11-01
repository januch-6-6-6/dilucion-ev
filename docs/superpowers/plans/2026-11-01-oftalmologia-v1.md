# Oftalmología v1: plan de implementación

> **Para agentes:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development (recomendado) o superpowers:executing-plans para ejecutar este plan tarea por tarea. Los pasos usan casillas (`- [ ]`).

**Objetivo:** agregar a Dilución EV el centro `/oftalmologia` (Pabellón · Orales · Colirios) con 41 fichas `FichaOcular`, 11 orales marcados y un verificador de concentración.

**Arquitectura:**
- Es una sección independiente con el patrón de Tópicos:
  - datos YAML generados con Python por lotes
  - esquema zod con validador
  - cargador con `import.meta.glob`
  - UI lazy bajo `src/app/oftalmo/`
- El verificador es una función pura en `src/calculos/verificadorOcular.ts`.
- Los orales no se duplican: `FichaOral` gana `usos` y `DosisOral` gana `oftalmica`.

**Stack:** React 19 + react-router 7, zod 4, vitest + Testing Library, Vite, y Python 3 + PyYAML para generar los datos.

**Spec:** `docs/superpowers/specs/2026-11-01-oftalmologia-design.md` (leerla entera antes de empezar). Decisiones en `datos/crudos/oftalmo/DECISIONES.md`; crudos y su mapa en `datos/crudos/oftalmo/ESTADO.md`.

## Restricciones globales

- Todo el texto de la UI va en español de Chile. Va en **todas** las fichas de pabellón: «Material de formación, no de prescripción» y «Verifica el protocolo de tu pabellón».
- **Nunca** proponer preparaciones. Los pasos salen solo de la fuente citada, y el verificador compara sin sugerir correcciones.
- Tolerancia del verificador: **±5 %** para dosis puntual; para un rango, dentro de [min, max].
- Todas las fichas de pabellón llevan `altoRiesgo: true`. Lo sin registro en Chile lleva `registroChile: no_registrado` y el aviso «No registrado en Chile (puede usarse por importación o uso compasivo)».
- Los favoritos y recientes usan el prefijo `oft:` en las claves existentes.
- **Nunca `git add -A`**: hay `.env.supabase` y carpetas sin seguimiento (`supabase/`, `datos/crudos/orales/`). Agregar los archivos por nombre.
- No usar `rm` ni `cp` directos (están aliasados a `-i`): usar `\rm` y `\cp -f`.
- No hacer push ni unir a `main` sin el OK de Héctor: el push publica el sitio.
- No citar el PPP de cierre angular, la conversión del ONTT ni ZEDS hasta cotejarlos con el original (spec §8).

## Foco de la revisión

1. **Coma decimal:** escribir «7,5» en el verificador debe leerse como 7,5 (usar `parsearNumero` de `src/calculos/numeros.ts`), nunca como 75 ni como un error mudo.
2. **Unidades mezcladas:** un frasco en mg con una dosis objetivo en mcg (moxifloxacino, alteplasa, voriconazol) debe convertirse antes de comparar. Comparar 0,15 mg con 150 mcg da «coincide».
3. **Unidades no convertibles:** con UI o U frente a mg, el verificador devuelve un error explícito y no un falso «coincide».
4. **Fichas sin verificador:** en una ficha `informativa` o con todas sus presentaciones `usoDirecto`, la ruta `/verificar` escrita a mano muestra «Esta ficha no tiene verificador» y no una calculadora vacía.
5. **Un rojo no debe sugerir nada:** el mensaje rojo no contiene cifras de corrección («agrega X ml»). Se prueba con un texto exacto.

---

### Tarea 1: esquema `FichaOcular`

**Archivos:**
- Crear: `src/esquema/ficha-ocular.ts`
- Probar: `src/esquema/ficha-ocular.test.ts`
- Agregar fixtures en `src/esquema/__fixtures__/` si las usan las otras pruebas del directorio.

**Interfaces que produce:**
- `UnidadOcular` = `z.enum(['mg','mcg','UI','U'])`.
- `CantidadOcular = {valor, unidad}`.
- `RangoOcular = {min, max, unidad}`.
- `DosisFinal = {cantidad: CantidadOcular | RangoOcular, volumenMl}`.
- `PresentacionOcular`, `DosisOcular`, `Paso` (unión discriminada por `tipo`: `reconstituir | diluir | cargar | texto`), `ProtocoloOcular` y `FichaOcular`, con exactamente los campos de la tabla §4 de la spec.
- Se reutilizan `FuenteRef` (de `ficha.ts`) y `RegistroChile` (de `ficha-oral.ts`; en las presentaciones solo se usan `verificado` y `no_registrado`).
- Se exportan los tipos con `z.infer`.

- [ ] **Paso 1: pruebas que fallan** (una por regla de §4):
  - `acepta la ficha mínima de cefuroxima` (1 presentación de polvo 750 mg, 1 dosis intracameral de 1 mg/0,1 ml, 1 protocolo con resultado de 1 mg/0,1 ml).
  - `rechaza modo intraocular sin dosis con final`.
  - `rechaza protocolo cuyo resultado difiere >5 % de dosis.final` (resultado 1,1 mg frente a 1 mg).
  - `acepta protocolo dentro del 5 %` (1,04 mg).
  - `rechaza protocolo con dosis o partida inexistente`.
  - `rechaza usoDirecto sin volumenMl`.
  - `rechaza verificado sin registrosIsp`.
  - `acepta informativa sin final ni protocolos`.
  - `rechaza sinPauta con dosis`.
  - `rechaza altoRiesgo false`.
- [ ] **Paso 2:** `npx vitest run src/esquema/ficha-ocular.test.ts` debe dar FAIL (no existe el módulo).
- [ ] **Paso 3: implementar.** Las reglas cruzadas van en `superRefine`, como en `ficha-topica.ts`. La comparación de ±5 % entre `resultado` y `final` usa `convertirMasa` (`src/calculos/unidades.ts`) cuando las unidades son de masa. Si no son convertibles, se exige la misma unidad.
- [ ] **Paso 4:** el mismo comando debe dar PASS.
- [ ] **Paso 5:** commit `feat(oftalmo): esquema FichaOcular`.

### Tarea 2: validador y verificación de fuentes

**Archivos:**
- Crear: `src/esquema/validar-oculares.ts`
- Probar: `src/esquema/validar-oculares.test.ts`

**Interfaces:**
- **Consume:** `FichaOcular` y `Fuente`.
- **Produce:**
  - `validarOculares(fichas: unknown[], fuentes: unknown[]): string[]`: errores con el formato de `validarTopicos`.
  - `verificacionOcular(ficha: FichaOcular, fuentes: Fuente[]): 'contrastada' | 'fuente_unica' | 'sin_pauta'`.

- [ ] **Paso 1: pruebas que fallan:**
  - `fuente inexistente en dosis, tambien, protocolo y discrepancia → error con ruta`.
  - `id repetido → error`.
  - `contrastada si tambien es de otra institución`.
  - `fuente_unica si tambien es de la misma institución`.
- [ ] **Paso 2:** `npx vitest run src/esquema/validar-oculares.test.ts` debe dar FAIL.
- [ ] **Paso 3: implementar** copiando la estructura de `validar-topicos.ts`. Conviene extraer `refsDeFuente` a un módulo común solo si queda idéntico; si no, se duplica.
- [ ] **Paso 4:** debe dar PASS.
- [ ] **Paso 5:** commit `feat(oftalmo): validador de fichas oculares`.

### Tarea 3: verificador puro

**Archivos:**
- Crear: `src/calculos/verificadorOcular.ts`
- Probar: `src/calculos/verificadorOcular.test.ts`

**Interfaces:**
- **Consume:** `PresentacionOcular`, `DosisFinal` y `convertirMasa`.
- **Produce:**
  - `type PasoNumerico = {tipo:'reconstituir', volumenMl:number} | {tipo:'diluir', tomarMl:number, llevarAMl:number}`
  - `type Comparacion = {dosis: DosisFinal, estado:'coincide'|'no_coincide', diferenciaPct:number|null}`
  - `verificar(e:{presentacion: PresentacionOcular, pasos: PasoNumerico[], objetivos: DosisFinal[]}): {ok:true, porMl: CantidadOcular, porVolumenObjetivo: CantidadOcular[], volumenDisponibleMl:number, comparaciones: Comparacion[], algunaCoincide:boolean} | {ok:false, error:string}`
  - `tieneVerificador(f: FichaOcular): boolean`: `modo === 'intraocular'`, al menos una dosis con `final` y al menos una presentación con `usoDirecto: false`.
  - `objetivosDe(f: FichaOcular, presentacionId: string): DosisFinal[]`

- [ ] **Paso 1: pruebas que fallan** (con los valores de la spec §5 y §7):
  - `cefuroxima 750 mg + 7,5 ml → 100 mg/ml; diluir 1→10 → 10 mg/ml = 1 mg/0,1 ml, coincide`.
  - `Arshinoff: solución 5 mg/ml, diluir 3→10 → 1,5 mg/ml = 150 mcg/0,1 ml; coincide con objetivo 150 mcg y no con 500 mcg; algunaCoincide true`.
  - `alteplasa rango 6–25 mcg/0,1 ml: 50 mg + 50 ml → 1 mg/ml; diluir 1→10 → 0,1 mg/ml = 10 mcg/0,1 ml, coincide`.
  - `fuera de rango (30 mcg) → no_coincide`.
  - `1,06 mg frente a 1 mg → no_coincide (6 %)`; `1,04 mg → coincide`.
  - Errores:
    - `tomar 2 ml cuando hay 1 ml → error "No puedes tomar más volumen del que tienes"`
    - `llevarAMl < tomarMl → error`
    - `volumen 0 → error`
    - `más de 4 pasos → error`
    - `polvo sin paso reconstituir antes de diluir → error`
  - `U frente a mg → error "Unidades no comparables"` (foco 3).
  - Si la presentación es una solución, se parte de `cantidad/volumenMl` sin reconstituir.
- [ ] **Paso 2:** `npx vitest run src/calculos/verificadorOcular.test.ts` debe dar FAIL.
- [ ] **Paso 3: implementar.** La concentración se lleva en la unidad del frasco; antes de comparar se convierte a la unidad del objetivo. Supuesto de la reconstitución: el volumen final es igual al volumen de diluyente.
- [ ] **Paso 4:** debe dar PASS.
- [ ] **Paso 5:** commit `feat(oftalmo): verificador de concentración`.

### Tarea 4: marca oftalmológica en orales

**Archivos:**
- Modificar: `src/esquema/ficha-oral.ts` (agregar `usos: z.array(z.literal('oftalmologia')).optional()` a la ficha y `oftalmica: z.literal(true).optional()` a `DosisOral`).
- Probar: `src/esquema/ficha-oral.test.ts`.

- [ ] **Paso 1: pruebas que fallan:**
  - `acepta usos: ['oftalmologia']`.
  - `rechaza usos: ['otro']`.
  - `acepta dosis con oftalmica: true`.
  - `rechaza oftalmica: true si la ficha no tiene usos oftalmologia` (`superRefine`).
- [ ] **Paso 2:** debe dar FAIL. **Paso 3:** implementar. **Paso 4:** `npx vitest run src/esquema` debe dar PASS y `npm run validar` debe seguir pasando con los 79 orales actuales.
- [ ] **Paso 5:** commit `feat(orales): marca de uso oftalmológico`.

### Tarea 5: generador, cargador y lote piloto (cefuroxima y moxifloxacino)

**Archivos:**
- Crear:
  - `scripts/oftalmo/__init__.py`
  - `scripts/oftalmo/comun.py`
  - `scripts/oftalmo/lote1.py`
  - `scripts/generar-oftalmo.py`
  - `src/datos/cargarOculares.ts`
  - `src/datos/oculares.test.ts`
- Modificar: `scripts/validar-datos.ts` (bloque de oftalmo igual al de tópicos) y `scripts/generar-todo.py` si llama a cada generador.

**Interfaces:**
- **`comun.py`** sigue `scripts/topicos/comun.py`:
  - Helpers que registran la fuente leyendo la cabecera del crudo (título en la línea 1 y URL en la línea 2): `fu`, `cima(...)`, `dm(...)`, `sefh_pnt(nombre)`, `consenso(detalle)`, `web(archivo, detalle)`, `isp(registros)`.
  - `CRUDOS = datos/crudos/oftalmo`.
  - Si un crudo no tiene URL en la línea 2, se abre la cabecera a mano antes de citarlo.
- **`generar-oftalmo.py`** escribe `datos/oftalmo/*.yaml` y `datos/fuentes-oftalmo.yaml` y borra los YAML huérfanos.
  - Verifica que cada registro ISP citado aparezca en `isp/` o `isp2/` (o en `datos/crudos/topicos/lista-isp.json` para colirios de partida como Vigamox), o que la presentación sea `no_registrado`.
  - Imprime `N fichas oculares, M fuentes` y lista los candidatos de pabellón de `candidatos.json` que todavía no tienen ficha.
- **`cargarOculares.ts`** exporta `oculares: FichaOcular[]`, `fuentesOculares`, `obtenerOcular(id)` y `verificacionDeOcular(f)`.

- [ ] **Paso 1:** prueba de datos que falla: `src/datos/oculares.test.ts` con `todas las fichas parsean` y `validarOculares sin errores`.
- [ ] **Paso 2: escribir `lote1.py`** solo con `cefuroxima` y `moxifloxacino`, desde `sefh/` (el PNT de cefuroxima), `cima/` (Prokam/Ximaract), `isp/` (Aprokam F-25555/25) y `web/moxifloxacino-ic*`. Moxifloxacino lleva:
  - 2 dosis intracamerales con estatus `off_label`: ASCRS 500 mcg/0,1 ml y Arshinoff 150 mcg/0,1 ml.
  - El protocolo de Arshinoff: partida Vigamox 5 mg/ml, `diluir` 3→10 con BSS.
  - Una discrepancia que explica que los 160 µg/0,1 ml del consenso son intravítreos.
- [ ] **Paso 3:** `python3 scripts/generar-oftalmo.py` debe decir «2 fichas oculares» y `npm run validar` debe pasar con la línea nueva «2 fichas oculares validadas».
- [ ] **Paso 4:** `npx vitest run src/datos/oculares.test.ts` debe dar PASS.
- [ ] **Paso 5:** commit `feat(oftalmo): generador, cargador y lote piloto`.

### Tareas 6 a 8: lotes de datos (revisión molécula por molécula)

Las tres tareas tienen la misma forma. En cada molécula:
1. Abrir los crudos citados.
2. Cotejar la cita con el original; las de WebFetch vienen recortadas (spec §8).
3. Cargar la ficha.
4. Anotar en `informes/oftalmologia-revision.md` (crear en la Tarea 6) una fila: `| id | dosis mostrada | fuente | 2.ª fuente | pasos sí/no | registro | notas |`.

| Tarea | Archivo | Fichas | Puntos fijos de la spec |
|---|---|---|---|
| 6 | `scripts/oftalmo/lote1.py` (completar) | las 11 intracamerales que faltan | carbacol, acetilcolina, Omidria, azul tripano y azul brillante `no_registrado`; Mydrane `usoDirecto` 0,2 ml con alerta «sin dosis adicionales»; alteplasa en rango 6–25 mcg/0,1 ml, `off_label`, alerta de hipema, conservación «usar de inmediato»; lidocaína y triamcinolona con todas sus vías en una sola ficha; adrenalina y lidocaína con el frasco elegido a mano (ampolla 1 mg/ml; 1–2 % sin conservantes) |
| 7 | `scripts/oftalmo/lote2.py` | 16 intravítreas | Lucentis, Eylia, Vabysmo y Ozurdex `usoDirecto` con la alerta «la jeringa trae más volumen que la dosis: elimina el exceso»; Lucentis con una 2.ª dosis pediátrica de 0,2 mg/0,02 ml (ROP); bevacizumab de 1,25 mg/0,05 ml, `off_label`; ceftazidima de **2 mg/0,1 ml** (SEFH) con una discrepancia frente a 2,25 mg; vancomicina con la alerta HORV (Witkin 2017) para la vía intracameral; amikacina con la alerta de infarto macular; amikacina, anfotericina, clindamicina, foscarnet y metotrexato con `protocolos: []`; brolucizumab, anfotericina B y ocriplasmina `no_registrado` |
| 8 | `scripts/oftalmo/lote3.py` | 9 `informativa` + 3 antifibróticos y toxina | ropivacaína `no_registrado`; los volúmenes de bloqueo de EyeWiki (retrobulbar 2–5 ml, peribulbar 6–10 ml, subtenoniano 2–5 ml) como texto; mitomicina, 5-FU y toxina con la alerta «La dosis y el tiempo de aplicación los define el cirujano»; la toxina en `U` con la alerta «unidades no intercambiables entre marcas»; mitomicina sin protocolo de reconstitución |

En cada tarea:
- [ ] **Paso 1:** escribir el lote.
- [ ] **Paso 2:** `python3 scripts/generar-oftalmo.py && npm run validar` deben pasar sin errores.
- [ ] **Paso 3:** agregar a `src/datos/oculares.test.ts` las pruebas de los puntos fijos del lote, por ejemplo:
  - `ceftazidima muestra 2 mg/0,1 ml y registra la discrepancia con 2,25`
  - `cada protocolo cuadra con verificar()`: se recorren todos los protocolos, se convierten sus pasos a `PasoNumerico` y `algunaCoincide` debe ser true
  - `las no_registrado del lote son exactamente [...]`
- [ ] **Paso 4:** `npx vitest run src/datos` debe dar PASS.
- [ ] **Paso 5:** commit `feat(oftalmo): lote N (familia)`, incluido el informe de revisión.

Si una fuente no sostiene una dosis, la ficha queda `sinPauta` con su motivo y se anota. **No se inventa.**

### Tarea 9: orales oftalmológicos

**Archivos:**
- Crear: `scripts/orales/tanda4.py` (7 nuevos).
- Modificar: los lotes de `scripts/orales/` donde están aciclovir, azitromicina, prednisona y cotrimoxazol (agregar `usos` y las dosis `oftalmica: True`).
- Modificar: `scripts/generar-orales.py` si la lista de tandas está escrita a mano.
- Probar: `src/datos/orales.test.ts`.

- [ ] **Paso 1: cotejar antes de citar** el PPP de cierre angular (acetazolamida), el ONTT (prednisona/metilprednisolona) y ZEDS (valaciclovir). Si ZEDS está «withdrawn», no se cita. Anotarlo en `informes/oftalmologia-revision.md`.
- [ ] **Paso 2: escribir los datos:**
  - acetazolamida 500 mg y luego 250 mg c/6 h; pediátrica 10–20 mg/kg/día
  - aciclovir 400 mg c/12 h, profilaxis HEDS
  - doxiciclina y minociclina con la contraindicación en <8 años y en el embarazo
  - pirimetamina y cotrimoxazol para toxoplasmosis (CDC)
  - metazolamida y famciclovir con `registroChile: no_registrado`
- [ ] **Paso 3:** `python3 scripts/generar-orales.py && npm run validar` debe dar «86 fichas orales validadas» (79 + 7).
- [ ] **Paso 4:** prueba `11 orales con usos oftalmologia; cada uno con ≥1 dosis oftalmica`, y debe dar PASS.
- [ ] **Paso 5:** commit `feat(orales): orales de uso oftalmológico`.

### Tarea 10: conteos finales y grupos

**Archivos:**
- Modificar:
  - `src/datos/oculares.test.ts`
  - `src/app/etiquetas.ts`, `src/app/colores.ts` y sus pruebas
  - `src/app/etiquetas.test.ts`

- [ ] **Paso 1: pruebas:**
  - `41 fichas oculares`.
  - Por familia, `intracameral 13, intravitreo 16, bloqueo 4, periocular 5, antifibrotico 3`. Las fichas con varias familias cuentan en su familia principal = `familias[0]`.
  - `9 no_registrado`.
  - `todas altoRiesgo`.
  - `todo grupo ocular tiene etiqueta y color`.
- [ ] **Paso 2:** agregar los grupos de §4 a `etiquetas.ts` y `colores.ts` (con los colores de la paleta existente) hasta que pase `npx vitest run src/datos src/app/etiquetas.test.ts src/app/colores.test.ts`.
- [ ] **Paso 3:** cerrar `informes/oftalmologia-revision.md` con los conteos calculados desde los YAML (contrastadas, fuente única, sin pauta y sin pasos).
- [ ] **Paso 4:** commit `feat(oftalmo): grupos y conteos finales`.

### Tarea 11: UI del centro y de la ficha

**Archivos:**
- Crear en `src/app/oftalmo/`:
  - `guardadoOculares.ts`: copia de `guardadoTopicos.ts` con `PREFIJO = 'oft:'`.
  - `textos.ts`: avisos fijos.
  - `CentroOftalmologia.tsx`: pestañas.
  - `FichaOcular.tsx`.
  - `Oftalmo.test.tsx`.

**Interfaces:**
- **Consume:** `oculares`, `obtenerOcular`, `verificacionDeOcular`, `tieneVerificador`, `topicos` (filtrados por `vias.includes('ojo')`) y `orales` (de `cargarOrales.ts`, filtrados por `usos?.includes('oftalmologia')`).
- **Textos exactos en `textos.ts`:**
  - `AVISO_FORMACION = 'Material de formación, no de prescripción.'`
  - `AVISO_PABELLON = 'Verifica el protocolo de tu pabellón.'`
  - `AVISO_NO_REGISTRADO = 'No registrado en Chile (puede usarse por importación o uso compasivo).'`
  - `AVISO_SIN_PASOS = 'La fuente no publica pasos de preparación; usa el protocolo de tu pabellón.'`
  - `AVISO_CIRUJANO = 'La dosis y el tiempo de aplicación los define el cirujano.'`

- [ ] **Paso 1: pruebas que fallan:**
  - `centro muestra las 3 pestañas y Pabellón agrupa por familia`.
  - `pestaña Orales lista 11 y enlaza a /orales/m/:id`.
  - `pestaña Colirios solo trae tópicos con vía ojo`.
  - `ficha de cefuroxima muestra el protocolo con fuente y el botón Verificar mi preparación`.
  - `ficha informativa (bupivacaína) no muestra Verificar`.
  - `ficha usoDirecto (ranibizumab) no muestra Verificar y sí la alerta de eliminar el exceso`.
  - `carbacol muestra AVISO_NO_REGISTRADO`.
  - `amikacina muestra AVISO_SIN_PASOS`.
  - `mitomicina muestra AVISO_CIRUJANO`.
  - `toda ficha muestra AVISO_FORMACION y AVISO_PABELLON`.
- [ ] **Paso 2:** `npx vitest run src/app/oftalmo` debe dar FAIL.
- [ ] **Paso 3: implementar** reutilizando los componentes y estilos de `src/app/topicos/FichaTopica.tsx` y `ListaTopicos.tsx`, como `AvisoFuenteUnica` y `TablaDiscrepancias`. Pestañas de la ficha: Dosis · Preparación · Conservación · Alertas · Discrepancias · Fuentes. En la ficha oral, las dosis `oftalmica` llevan la etiqueta «Oftalmología»: modificar `src/app/orales/FichaOral.tsx` con su prueba en `FichaOral.test.tsx`.
- [ ] **Paso 4:** debe dar PASS. **Paso 5:** commit `feat(oftalmo): centro y ficha`.

### Tarea 12: página del verificador

**Archivos:**
- Crear: `src/app/oftalmo/VerificadorOcular.tsx`.
- Probar: `src/app/oftalmo/Verificador.test.tsx`.

- [ ] **Paso 1: pruebas que fallan** (con user-event):
  - `cefuroxima: elegir frasco 750 mg, reconstituir 7,5, diluir 1→10 → texto "Coincide con"`. Se escribe «7,5» con coma (foco 1).
  - `diluir 1→8 → "NO coincide"`, y el texto rojo es exactamente `NO coincide: obtuviste {X}; la fuente dice {Y}. No administres; revisa los pasos.` sin otras cifras (foco 5).
  - `moxifloxacino 3→10 → coincide con Arshinoff`.
  - `ruta /oftalmologia/m/bupivacaina/verificar → "Esta ficha no tiene verificador"` (foco 4).
  - `se muestra el supuesto "el volumen final se toma igual al diluyente agregado"`.
  - `AVISO_PABELLON siempre visible`.
- [ ] **Paso 2:** debe dar FAIL. **Paso 3: implementar.**
  - Selector de presentación: solo las que no son `usoDirecto`.
  - Lista de pasos editable (agregar o quitar, máximo 4).
  - Los números se leen con `parsearNumero`.
  - El cálculo se hace con `verificar(...)`.
  - Se muestra la concentración por ml y por el volumen objetivo.
- [ ] **Paso 4:** debe dar PASS. **Paso 5:** commit `feat(oftalmo): verificador en la interfaz`.

### Tarea 13: rutas, navegación, Acerca y README

**Archivos:**
- Modificar:
  - `src/app/App.tsx`: 3 rutas lazy de §6 y `NavLink` «Oftalmología» después de «Tópicos».
  - `src/app/paginas/Acerca.tsx` y `Acerca.test.tsx`: un párrafo de propósito, la regla de pasos citados, el verificador y sus límites.
  - `README.md`: la sección Oftalmología y cómo regenerar con `python3 scripts/generar-oftalmo.py`.
  - `src/app/App.test.tsx`.

- [ ] **Paso 1:** pruebas `navegación tiene Oftalmología` y `/oftalmologia/m/cefuroxima renderiza la ficha`.
- [ ] **Paso 2:** implementar hasta que pasen.
- [ ] **Paso 3:** `npm test`, `npm run lint` y `npm run build` sin errores.
- [ ] **Paso 4:** commit `feat(oftalmo): rutas, navegación y documentación`.

### Tarea 14: prueba en el navegador y cierre

- [ ] **Paso 1:** abrir `npm run build && npm run preview` con Playwright (MCP, `--browser chromium`) en ancho de 390 px:
  - el centro con las 3 pestañas
  - la ficha de cefuroxima
  - el verificador en verde y en rojo
  - la ficha de bupivacaína
  - la de ranibizumab
  - la de carbacol

  Guardar las capturas en `docs/capturas/oftalmo/`.
- [ ] **Paso 2:** actualizar `datos/crudos/oftalmo/ESTADO.md` (qué se hizo y qué falta: la revisión clínica de la enfermera de oftalmología) y la memoria `project_dilucion_oftalmologia.md`.
- [ ] **Paso 3:** commit `docs(oftalmo): capturas y estado`.
- [ ] **Paso 4:** **preguntar a Héctor** antes de unir a `main` y hacer push, porque eso publica el sitio.
