# Dilución EV v0.2 — Medicamentos restantes — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pasar de 10 a ~89 medicamentos EV (resto de la tanda 1, tandas 2 y 3) con fuentes citadas, compatibilidad en Y global y un informe único para la revisión clínica de Héctor, y publicarlo.

**Architecture:** Igual que v0.1: fichas YAML generadas por scripts Python a partir de valores citados, validadas por `npm run validar` antes de compilar; la app no cambia salvo unidades nuevas (mEq, mmol) y colores para grupos nuevos. La compatibilidad en Y sale de una matriz Stabilis única para todos los medicamentos.

**Tech Stack:** Lo existente (React 19 + TS + Vite + zod + Vitest; Python 3 + PyYAML + Pillow para generadores); fuentes: CIMA (API REST), protocolo Pucón 2022, guía de antiinfecciosos del Hospital de Iquique, openFDA, Stabilis, Pediamécum, Urgencia UC.

**Spec:** `docs/superpowers/specs/2026-10-01-dilucion-ev-design.md` (§2.1 tandas, §4 ficha, §6 investigación, §9 etapas 0.2–0.3)

## Global Constraints

- Todo lo de v0.1 sigue vigente (plan `2026-10-01-dilucion-ev-v0.1.md`, Global Constraints): español de Chile, aviso exacto, cada número con unidad y `fuente`, «sin datos en las fuentes» en vez de valores por defecto, rojo solo para alertas y alto riesgo.
- Datos críticos (dosis, concentración máxima, tiempo mínimo, incompatibilidades) con ≥2 fuentes; si no coinciden, `meta.discrepancias` y valor más conservador.
- Prioridad de fuentes (spec §6.1): chilenas (Pucón, Iquique, ISP, MINSAL, Urgencia UC) → CIMA/DailyMed → Stabilis → Pediamécum. Una fuente extranjera usada por falta de chilena se marca en el título de la fuente como «FUENTE EXTRANJERA (país)».
- Presentación en polvo: `volumenMl` = volumen tras la reconstitución recomendada (igual al de `reconstitucion.volumenMl`), para que «volumen a cargar» use la concentración reconstituida.
- Nombres comerciales: solo si se verifican en una fuente chilena; si no, `[]`.
- `meta.revisadoPor` vacío en todas las fichas nuevas hasta la revisión de Héctor (no se marca nada como revisado sin él).
- Comandos: `source ~/.nvm/nvm.sh` antes de `npm`; en esta máquina usar `\rm -f` y `\cp -f`; no usar `pkill -f` con un patrón que aparezca en el propio comando.

## Lista de medicamentos (ids = nombre de archivo)

- **Tanda 1, resto (32):** dopamina, dobutamina, fenilefrina, nitroglicerina, labetalol, lidocaina, furosemida, metoclopramida, ondansetron, ketorolaco, tramadol, metamizol, hidrocortisona, dexametasona, metilprednisolona, fenitoina, levetiracetam, diazepam, naloxona, flumazenil, acido-tranexamico, heparina, insulina-cristalina, cloruro-de-potasio, bicarbonato-de-sodio, gluconato-de-calcio, glucosa-30, propofol, etomidato, rocuronio, succinilcolina, clorfenamina.
- **Tanda 2, antiinfecciosos (25):** cefazolina, ceftriaxona, cefotaxima, ceftazidima, cefepime, ampicilina, ampicilina-sulbactam, cloxacilina, penicilina-g-sodica, piperacilina-tazobactam, imipenem, meropenem, ertapenem, vancomicina, clindamicina, metronidazol, gentamicina, amikacina, ciprofloxacino, levofloxacino, cotrimoxazol, fluconazol, aciclovir, linezolid, azitromicina.
- **Tanda 3, hospitalarios (22):** omeprazol, paracetamol, ketoprofeno, dexmedetomidina, remifentanilo, cisatracurio, vecuronio, haloperidol, digoxina, manitol, fitomenadiona, tiamina, octreotido, cloruro-de-sodio-10, cloruro-de-sodio-3, fosfato-de-potasio, acetilcisteina, neostigmina, esmolol, enalaprilato, nimodipino, metoprolol.

Si un medicamento no tiene presentación EV comercializada que se pueda confirmar en una fuente chilena ni en CIMA/FDA, se omite y se anota en el informe (no se reemplaza por otro sin decírselo a Héctor).

## Grupos terapéuticos y color (ids exactos)

| grupo | color | | grupo | color |
|---|---|---|---|---|
| vasoactivo | naranjo | | antiemetico | lima |
| antiarritmico | violeta | | protector-gastrico | lima |
| antihipertensivo | violeta | | corticoide | lima |
| diuretico | violeta | | electrolito | verde |
| sedante | indigo | | metabolico | verde |
| anticonvulsivante | indigo | | hematologico | neutro |
| antipsicotico | indigo | | antiinfeccioso | cian |
| analgesico-opioide | azul | | antidoto | ambar |
| analgesico-no-opioide | azul | | antihistaminico | ambar |
| anestesico | turquesa | | anticolinergico | ambar |
| bloqueador-neuromuscular | turquesa | | | |

## Review Focus

1. **Unidades no convertibles** (potasio y bicarbonato en mEq, fosfato en mmol, heparina e insulina en UI): las calculadoras deben operar en la misma unidad y dar error explícito al mezclar con mg → tests en Task 1.
2. **Concentración de presentaciones en %** (glucosa 30 %, NaCl 10 %, KCl 10 %): la ficha debe expresar la cantidad real por volumen (p. ej., KCl 10 % 10 ml = 1 g = 13,4 mEq) y «volumen a cargar» debe dar el valor correcto → test con la ficha real de cloruro-de-potasio en Task 2.
3. **Antibióticos en polvo**: «volumen a cargar» usa la concentración reconstituida → test con la ficha real de cefazolina en Task 3.
4. **Grupo sin color**: cualquier grupo usado en `datos/` que no esté en la tabla caería en neutro sin aviso → test que recorre todas las fichas reales en Task 1 (falla si un grupo no está mapeado, salvo hematologico).
5. **Matriz de compatibilidad incompleta o asimétrica entre tandas**: el validador ya exige simetría; además, cada par de medicamentos de la app debe tener entrada (aunque sea `sin_datos`) → test en Task 5.

---

### Task 1: Unidades mEq/mmol y colores para grupos nuevos

**Files:**
- Modify: `src/calculos/unidades.ts`, `src/esquema/ficha.ts`, `src/app/colores.ts`, `src/index.css`
- Test: `src/calculos/unidades.test.ts`, `src/calculos/calculadoras.test.ts`, `src/app/colores.test.ts`

**Interfaces:**
- Produces: `UnidadMasa = 'g' | 'mg' | 'mcg' | 'UI' | 'mEq' | 'mmol'` (zod igual); `convertirMasa` lanza `Error('No se puede convertir <de> a <a>')` si alguna de las dos es UI/mEq/mmol y son distintas (el mensaje de UI existente se mantiene para UI↔masa); `parsearUnidadDosis` acepta `mEq|mmol`; `ColorGrupo` suma `'cian' | 'lima'`; `colorGrupo` con la tabla de grupos de arriba.

- [ ] **Step 1: Tests**
  - `convertirMasa(10, 'mEq', 'mEq') === 10`; `expect(() => convertirMasa(1, 'mEq', 'mg')).toThrow()`; `parsearUnidadDosis('mEq/h')` → `{ masa: 'mEq', porKg: false, tiempo: 'h' }`; `parsearUnidadDosis('mEq/kg')` → porKg true.
  - Calculadora en UI: heparina `dosisAVelocidad({ pesoKg: 70, dosis: { valor: 18, unidad: 'UI', tiempo: 'h' }, concentracionPorMl: { valor: 100, unidad: 'UI' } })` → 12,6. Potasio: `velocidadPorDosis({ valor: 10, unidad: 'mEq' }, { valor: 0.2, unidad: 'mEq' })` → 50.
  - `colorGrupo` para cada fila de la tabla; test que importa `medicamentos` de `src/datos/cargar` y verifica que todo grupo usado tiene color distinto de `neutro` salvo `hematologico`.
- [ ] **Step 2:** `npx vitest run src/calculos src/app/colores.test.ts` → FAIL.
- [ ] **Step 3:** Implementar; tokens `--cian` (#0891b2 / suave #cffafe / texto #155e75) y `--lima` (#65a30d / #ecfccb / #3f6212) en claro, y sus equivalentes oscuros; reglas `[data-color='cian']` y `[data-color='lima']`; correr el chequeo de contraste (script del rediseño) → 0 fallas.
- [ ] **Step 4:** Tests → PASS; `npm test` completo verde.
- [ ] **Step 5:** Commit `feat: unidades mEq/mmol y colores para grupos nuevos`.

### Task 2: Fichas del resto de la tanda 1 (32)

**Files:**
- Create: `scripts/fichas/comun.py` (helpers `fu`, `meta`, `compat_desde_matriz` y registro de fuentes extraídos de `generar-tanda1.py`), `scripts/fichas/tanda1b.py`, `datos/medicamentos/<id>.yaml` × 32
- Modify: `scripts/generar-tanda1.py` (importa los helpers de `comun.py`, mismo resultado byte a byte), `datos/fuentes.yaml`
- Test: `src/datos/cargar.test.ts`

**Interfaces:**
- Produces: `scripts/fichas/comun.py` con `fu(ref, detalle)`, `meta(discrepancias)`, `registrar_fuente(dict)`, `compat_desde_matriz(matriz, id, ids)`; cada `tandaX.py` expone `fichas() -> dict[id, ficha]` y `fuentes() -> list`. `scripts/generar-todo.py` (creado aquí) escribe todas las fichas y `fuentes.yaml` deduplicado.

- [ ] **Step 1:** Refactor: `python3 scripts/generar-todo.py` debe reproducir exactamente las 10 fichas actuales (`git diff --exit-code datos/` → sin cambios).
- [ ] **Step 2:** Investigar cada medicamento (fuentes en orden de prioridad; CIMA por API como en v0.1; Pucón ya descargado). Compatibilidad: dejar `[]` aquí (la llena Task 5).
- [ ] **Step 3: Test** en `cargar.test.ts`: `obtenerFicha('cloruro-de-potasio')` existe, es `altoRiesgo: true`, y `volumenACargar({ valor: 20, unidad: 'mEq' }, presentación de 10 ml al 10 %)` da el volumen que corresponde a la concentración registrada (13,4 mEq/10 ml → 14,93 ml, 2 ampollas) — ajustar al valor de la fuente si difiere y anotarlo.
- [ ] **Step 4:** `npm run validar` → 42 fichas validadas; `npm test` verde.
- [ ] **Step 5:** Commit `datos: resto de la tanda 1 (32 medicamentos)`.

### Task 3: Fichas de la tanda 2, antiinfecciosos (25)

**Files:** Create `scripts/fichas/tanda2.py`, `datos/medicamentos/<id>.yaml` × 25; Modify `datos/fuentes.yaml`, `scripts/generar-todo.py`; Test `src/datos/cargar.test.ts`.

- [ ] **Step 1:** Fuente chilena base: guía de antiinfecciosos del Hospital Dr. Ernesto Torres Galdames (Iquique) — presentación, reconstitución, dilución, tiempo, estabilidad, incompatibilidades; contrastar con CIMA. Dosis adulto/pediátrica desde CIMA y Pediamécum.
- [ ] **Step 2: Test:** `volumenACargar` con la ficha real de cefazolina (polvo 1 g reconstituido según la fuente) devuelve el volumen coherente con la concentración reconstituida registrada.
- [ ] **Step 3:** `npm run validar` → 67 fichas; `npm test` verde.
- [ ] **Step 4:** Commit `datos: tanda 2, antiinfecciosos (25)`.

### Task 4: Fichas de la tanda 3, hospitalarios (22)

**Files:** Create `scripts/fichas/tanda3.py`, `datos/medicamentos/<id>.yaml` × 22; Modify `datos/fuentes.yaml`, `scripts/generar-todo.py`.

- [ ] **Step 1:** Investigar y generar; omitir con nota en el informe los que no tengan presentación EV confirmable.
- [ ] **Step 2:** `npm run validar` → ~89 fichas; `npm test` verde.
- [ ] **Step 3:** Commit `datos: tanda 3, hospitalarios`.

### Task 5: Matriz de compatibilidad en Y global

**Files:** Create `scripts/stabilis_matriz.py`, `datos/crudos/stabilis-y-global-<fecha>.json`; Modify `scripts/fichas/comun.py` (usa la matriz global), Test `src/esquema/validar.test.ts` o nuevo `src/datos/compatibilidad.test.ts`.

**Interfaces:**
- Produces: `stabilis_matriz.py <ids Stabilis…> --salida X.json` que pide la tabla «AVEC solvants usuels» por POST, la convierte a PNG y lee cada celda por color (verde/rojo/amarillo/blanco) detectando la grilla; JSON `{fila: {columna: 'G'|'R'|'Y'|'.'}}`.

- [ ] **Step 1: Test** `todo par de medicamentos de la app tiene entrada de compatibilidad (compatible/incompatible/sin_datos) en ambas fichas`.
- [ ] **Step 2:** Run → FAIL (las fichas nuevas tienen `[]`).
- [ ] **Step 3:** Mapear cada id de la app a su molécula Stabilis (los que no existan en Stabilis quedan `sin_datos` con detalle «no figura en Stabilis»). Generar la tabla con todos; si Stabilis no la genera o la grilla no se puede leer, usar tres tercios A, B, C y las tablas A∪B, A∪C, B∪C. Mantener las reglas de v0.1: amarillo → incompatible (conservador); CIMA 6.2 manda si declara incompatibilidad que Stabilis no tiene.
- [ ] **Step 4:** Regenerar todo; `npm run validar` (simetría) y `npm test` → verde. Verificar 3 pares a mano contra la imagen (incluido noradrenalina–sulfato de magnesio = incompatible).
- [ ] **Step 5:** Commit `datos: compatibilidad en Y global (Stabilis)`.

### Task 6: Informe consolidado para la revisión clínica

**Files:** Create `informes/v0.2-revision-clinica.md`, `scripts/informe_revision.py`.

- [ ] **Step 1:** `informe_revision.py` genera una tabla por tanda con, para cada medicamento: presentación, dilución estándar, dosis adulto, dosis pediátrica (o «sin dosis pediátrica»), tiempo mínimo, incompatibilidades clave, fuentes usadas y discrepancias. Arriba, una sección «Para revisar primero» con todas las discrepancias y todas las fuentes extranjeras.
- [ ] **Step 2:** Verificar que el informe lista los ~89 medicamentos y que cada discrepancia de `meta` aparece.
- [ ] **Step 3:** Commit `docs: informe consolidado para revisión clínica v0.2`.

### Task 7: Verificación visual y publicación

- [ ] **Step 1:** `npm run build`, vista previa local y capturas en celular (claro/oscuro) de: lista de antiinfecciosos (color cian), ficha de cefazolina (reconstitución), calculadora de potasio en mEq.
- [ ] **Step 2:** Revisión final independiente de la rama (como en v0.1) con foco en: unidades mEq/UI, presentaciones en % y en polvo, citas de fuentes y compatibilidad.
- [ ] **Step 3:** Pase de correcciones con TDD para hallazgos críticos/importantes.
- [ ] **Step 4:** Fusionar a `main`, push, esperar el workflow en verde y verificar en la URL pública 3 fichas nuevas.
- [ ] **Step 5:** Actualizar README (cantidad de medicamentos) y la memoria del proyecto.
