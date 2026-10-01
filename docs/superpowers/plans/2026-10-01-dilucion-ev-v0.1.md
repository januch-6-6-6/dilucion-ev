# Dilución EV v0.1 — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar una PWA funcional sin internet con calculadoras probadas y 10 medicamentos EV de la tanda 1, cada dato con fuente.

**Architecture:** Fichas YAML en `datos/` validadas con un esquema (zod) antes de compilar; cálculos como funciones puras en `src/calculos/` con pruebas; pantallas React que solo leen fichas ya validadas y llaman a las funciones de cálculo. Sin servidor.

**Tech Stack:** Node 24 (nvm), Vite, React 19, TypeScript estricto, react-router-dom (`HashRouter`), zod, yaml (eemeli), vite-plugin-pwa, Vitest + @testing-library/react + jsdom, tsx.

**Spec:** `docs/superpowers/specs/2026-10-01-dilucion-ev-design.md`

## Global Constraints

- Idioma de la interfaz, del código de dominio y de los mensajes: español de Chile.
- Aviso exacto (spec §5.6): "Material de formación. No reemplaza el protocolo local ni la indicación médica. Verifique siempre con la fuente y la normativa de su institución."
- Todo valor clínico numérico en una ficha lleva unidad y `fuente: { ref, detalle }`; `ref` debe existir en `datos/fuentes.yaml`.
- Si falta un dato: mostrar "sin datos en las fuentes"; nunca un valor por defecto.
- Macrogotero = 20 gotas/ml; microgotero = 60 gotas/ml.
- Redondeo (half-up, mostrado): ml/h → 1 decimal; gotas/min → entero; volumen a cargar → 2 decimales.
- Alertas fuera de rango: en rojo, avisan, no bloquean.
- Pediatría: dosis por kg con tope de dosis de adulto; si la ficha no tiene dosis pediátrica, no se calcula y se muestra "sin dosis pediátrica en la fuente". Neonatos fuera de alcance.
- Sin cuentas ni almacenamiento de datos de pacientes (el peso no se guarda; solo se guarda la lista de "últimos consultados" con ids de medicamento).
- Nunca copiar tablas o textos completos de guías: solo datos con cita.
- Comandos de Node con el PATH de nvm (`source ~/.nvm/nvm.sh` antes de `npm`).

## Review Focus

1. **Números escritos a la chilena** ("70,5", " 70 ", "", "abc", "0", "-3"): se acepta la coma decimal; vacío, texto, cero y negativos dan un mensaje de qué falta, nunca `NaN` en pantalla → test `parsearNumero` en Task 2 y test de error en Task 3.
2. **Mezclar UI con unidades de masa** (insulina/heparina en UI contra concentración en mg): error explícito, no un número → test en Task 2 (`convertirMasa`) y Task 3.
3. **Medicamento sin dosis pediátrica**: la calculadora pediátrica muestra el texto fijo y no calcula → test en Task 10.
4. **Ruido de coma flotante en el redondeo** (26,25 → 26,3; 0,1 × 3 → 0,3): half-up real → test en Task 2.
5. **Recarga en una ruta profunda y uso sin internet** (GitHub Pages + PWA): `HashRouter` y manifiesto/service worker presentes en el build → test de build en Task 11.

---

### Task 1: Esqueleto del proyecto

**Files:**
- Create: `package.json`, `vite.config.ts`, `tsconfig.json`, `index.html`, `src/main.tsx`, `src/app/App.tsx`, `src/app/App.test.tsx`, `src/test/setup.ts`, `.gitignore`

**Interfaces:**
- Produces: scripts `npm run dev`, `npm test` (vitest run), `npm run build` (con `prebuild: npm run validar`), `npm run validar` (definido en Task 5; en esta task apunta a `echo ok`). Componente `App` con `HashRouter`.

- [ ] **Step 1:** `npm create vite@latest . -- --template react-ts`, luego instalar `react-router-dom zod yaml` y como dev `vitest @testing-library/react @testing-library/jest-dom jsdom vite-plugin-pwa tsx`.
- [ ] **Step 2: Write the failing test** `App.test.tsx` → `renders el título "Dilución EV"`: `render(<App />)`; `expect(screen.getByRole('heading', { name: 'Dilución EV' })).toBeInTheDocument()`.
- [ ] **Step 3:** Run `npm test` → FAIL (el template no tiene ese título).
- [ ] **Step 4:** `App` con `HashRouter` y un `<h1>Dilución EV</h1>`; vitest con `environment: 'jsdom'`, `setupFiles: ['src/test/setup.ts']`, `base: './'` en Vite.
- [ ] **Step 5:** Run `npm test` → PASS; `npm run build` → sale sin errores.
- [ ] **Step 6:** Commit `chore: esqueleto Vite + React + Vitest`.

### Task 2: Unidades, números y redondeo

**Files:**
- Create: `src/calculos/unidades.ts`, `src/calculos/redondeo.ts`, `src/calculos/numeros.ts` y sus `*.test.ts`

**Interfaces:**
- Produces:
  - `type UnidadMasa = 'g' | 'mg' | 'mcg' | 'UI'`; `type Cantidad = { valor: number; unidad: UnidadMasa }`
  - `convertirMasa(valor: number, de: UnidadMasa, a: UnidadMasa): number` — lanza `Error('No se puede convertir UI a unidades de masa')` si solo uno de los dos es `'UI'`.
  - `redondear(valor: number, decimales: number): number` — half-up.
  - `parsearNumero(texto: string): number | null` — acepta coma o punto; `null` si vacío, no numérico, o ≤ 0.

- [ ] **Step 1: Tests**
  - `convertirMasa(1, 'mg', 'mcg') === 1000`; `convertirMasa(2500, 'mcg', 'mg') === 2.5`; `convertirMasa(1, 'g', 'mg') === 1000`; `convertirMasa(5, 'UI', 'UI') === 5`; `expect(() => convertirMasa(1, 'UI', 'mg')).toThrow('No se puede convertir UI a unidades de masa')`.
  - `redondear(26.25, 1) === 26.3`; `redondear(0.1 * 3, 1) === 0.3`; `redondear(66.666, 0) === 67`; `redondear(1.005, 2) === 1.01`.
  - `parsearNumero('70,5') === 70.5`; `parsearNumero(' 70 ') === 70`; `parsearNumero('') === null`; `parsearNumero('abc') === null`; `parsearNumero('0') === null`; `parsearNumero('-3') === null`.
- [ ] **Step 2:** Run `npx vitest run src/calculos` → FAIL (módulos inexistentes).
- [ ] **Step 3:** Implementar. Para `redondear` usar `Math.round((valor + Number.EPSILON) * 10 ** d) / 10 ** d` y verificar el caso 1.005 (si falla, usar `Number(Math.round(Number(valor + 'e' + d)) + 'e-' + d)`).
- [ ] **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: unidades, redondeo y lectura de números`.

### Task 3: Calculadoras

**Files:**
- Create: `src/calculos/calculadoras.ts`, `src/calculos/calculadoras.test.ts`

**Interfaces:**
- Consumes: Task 2 (`Cantidad`, `convertirMasa`, `redondear`).
- Produces (todas puras):
  - `type Resultado<T> = { ok: true; valor: T; pasos: string[] } | { ok: false; error: string }`
  - `concentracion(cantidad: Cantidad, volumenFinalMl: number, unidadSalida: UnidadMasa): Resultado<number>` (unidad de salida por ml)
  - `volumenACargar(dosis: Cantidad, presentacion: { cantidad: Cantidad; volumenMl: number }): Resultado<{ ml: number; unidades: number }>` — `ml` a 2 decimales; `unidades = ceil(ml / volumenMl)`.
  - `velocidadPorTiempo(volumenMl: number, tiempoMin: number): Resultado<{ mlh: number; gotasMacro: number; gotasMicro: number }>`
  - `velocidadPorDosis(dosisPorHora: Cantidad, concentracionPorMl: Cantidad): Resultado<number>` (ml/h)
  - `type DosisPorPeso = { valor: number; unidad: UnidadMasa; tiempo: 'min' | 'h' | null }`
  - `dosisAVelocidad(p: { pesoKg: number; dosis: DosisPorPeso; concentracionPorMl: Cantidad }): Resultado<number>` (ml/h; `tiempo` no puede ser null)
  - `velocidadADosis(p: { pesoKg: number; mlh: number; concentracionPorMl: Cantidad; unidadSalida: UnidadMasa; tiempo: 'min' | 'h' }): Resultado<number>` (redondeo a 3 decimales)
  - `dosisPediatrica(p: { pesoKg: number; dosisPorKg: Cantidad; topeAdulto: Cantidad }): Resultado<{ dosis: Cantidad; limitada: boolean }>`
  - Entradas ≤ 0, `NaN` o mezcla UI/masa → `{ ok: false, error }` con mensajes: `'Falta el peso'`, `'Falta el volumen'`, `'Falta el tiempo'`, `'Falta la concentración'`, `'Falta la dosis'`, `'No se puede convertir UI a unidades de masa'`.
  - `pasos[0]` es la fórmula en texto (p. ej. `'ml/h = dosis × peso × 60 ÷ concentración'`).

- [ ] **Step 1: Tests (valores calculados a mano)**
  - `concentracion({valor:4,unidad:'mg'}, 250, 'mcg')` → 16.
  - `volumenACargar({valor:300,unidad:'mg'}, {cantidad:{valor:150,unidad:'mg'}, volumenMl:3})` → `{ ml: 6, unidades: 2 }`; adrenalina `({valor:1,unidad:'mg'}, {cantidad:{valor:1,unidad:'mg'}, volumenMl:1})` → `{ ml: 1, unidades: 1 }`.
  - `velocidadPorTiempo(100, 30)` → `{ mlh: 200, gotasMacro: 67, gotasMicro: 200 }`; `velocidadPorTiempo(500, 480)` → `{ mlh: 62.5, gotasMacro: 21, gotasMicro: 63 }`.
  - `velocidadPorDosis({valor:100,unidad:'mcg'}, {valor:10,unidad:'mcg'})` → 10.
  - Noradrenalina: `dosisAVelocidad({ pesoKg:70, dosis:{valor:0.1,unidad:'mcg',tiempo:'min'}, concentracionPorMl:{valor:16,unidad:'mcg'} })` → 26.3.
  - Midazolam: `dosisAVelocidad({ pesoKg:80, dosis:{valor:0.05,unidad:'mg',tiempo:'h'}, concentracionPorMl:{valor:1,unidad:'mg'} })` → 4.
  - Ida y vuelta: `velocidadADosis({ pesoKg:70, mlh:26.25, concentracionPorMl:{valor:16,unidad:'mcg'}, unidadSalida:'mcg', tiempo:'min' })` → 0.1.
  - `dosisPediatrica({ pesoKg:20, dosisPorKg:{valor:0.01,unidad:'mg'}, topeAdulto:{valor:1,unidad:'mg'} })` → `{ dosis:{valor:0.2,unidad:'mg'}, limitada:false }`; con `pesoKg:150` → `{ dosis:{valor:1,unidad:'mg'}, limitada:true }`.
  - Errores: `dosisAVelocidad` con `pesoKg: 0` → `{ ok:false, error:'Falta el peso' }`; `velocidadPorDosis({valor:2,unidad:'UI'}, {valor:1,unidad:'mg'})` → `{ ok:false, error:'No se puede convertir UI a unidades de masa' }`.
  - `pasos[0]` no vacío en cada resultado ok.
- [ ] **Step 2:** Run `npx vitest run src/calculos/calculadoras.test.ts` → FAIL.
- [ ] **Step 3:** Implementar; convertir todo a la unidad de la concentración antes de dividir; aplicar `redondear` según Global Constraints.
- [ ] **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: calculadoras de dilución y velocidad`.

### Task 4: Alertas fuera de rango

**Files:**
- Create: `src/calculos/alertas.ts`, `src/calculos/alertas.test.ts`

**Interfaces:**
- Consumes: Task 2.
- Produces: `type Alerta = { nivel: 'rojo'; mensaje: string }`;
  - `alertaConcentracion(concPorMl: Cantidad, maxPorMl?: Cantidad): Alerta[]`
  - `alertaDosis(dosis: number, unidad: string, rango: { min?: number; max?: number; maximaAbsoluta?: number }): Alerta[]`
  - `alertaTiempo(tiempoMin: number, tiempoMinimoMin?: number): Alerta[]`
  - Sin límite definido (`undefined`) → `[]`.

- [ ] **Step 1: Tests**
  - `alertaConcentracion({valor:64,unidad:'mcg'}, {valor:32,unidad:'mcg'})` → 1 alerta con mensaje que contiene `'supera la concentración máxima'`; con 16 → `[]`; sin máximo → `[]`.
  - `alertaDosis(3, 'mcg/kg/min', {max:1})` → 1 alerta `'supera la dosis máxima'`; `alertaDosis(0.01, 'mcg/kg/min', {min:0.05})` → 1 alerta `'bajo la dosis mínima'`.
  - `alertaTiempo(10, 30)` → 1 alerta `'más rápido que lo recomendado'`; `alertaTiempo(30, 30)` → `[]`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar. **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: alertas fuera de rango`.

### Task 5: Esquema y validación de fichas

**Files:**
- Create: `src/esquema/ficha.ts`, `src/esquema/validar.ts`, `src/esquema/validar.test.ts`, `src/esquema/__fixtures__/` (ficha válida, ficha sin fuente, ficha con min > max, par de fichas con compatibilidad asimétrica, fuentes.yaml de prueba), `scripts/validar-datos.ts`
- Modify: `package.json` (`"validar": "tsx scripts/validar-datos.ts"`)

**Interfaces:**
- Produces:
  - zod `FuenteRef = { ref: string; detalle: string }`; `Fuente = { id, titulo, institucion, url, anio: number, consultado: 'YYYY-MM-DD' }`.
  - zod `Ficha` con los bloques del spec §4 (nombres de campo): `id, nombre, comerciales[], grupo, ambitos[] ('samu'|'urgencia'|'upc'|'hospitalizacion'|'aps'), altoRiesgo, presentaciones[{id, forma, cantidad: Cantidad, volumenMl, fuente}], reconstitucion (null | {diluyente, volumenMl, fuente}), dilucion {sueros[], concentracionMin?, concentracionMax? (Cantidad + fuente), estandar[{descripcion, cantidad, volumenFinalMl, fuente}]}, administracion {vias[] ('bolo'|'infusion_intermitente'|'infusion_continua'), texto, tiempoMinimoMin?, requiereViaCentral, requiereBomba, fuente}, dosis[{indicacion, poblacion ('adulto'|'pediatrico'), unidad, min?, max?, maximaAbsoluta?, topeAdulto?: Cantidad, fuente}], sinDosisPediatrica: boolean, estabilidad {ambienteH?, refrigeradoH?, protegerLuz, fuente}, compatibilidad[{con, estado ('compatible'|'incompatible'|'sin_datos'), fuente}], interaccionesGraves[{con, efecto, fuente}], efectosAdversos {frecuentes[], graves[], vigilar[], fuente}, alertas[], meta {revisadoPor?, fechaRevision?, discrepancias[{campo, valores[], decision}]}`.
  - `validarDatos(fichas: unknown[], fuentes: unknown[]): string[]` — lista de errores legibles (vacía = OK). Revisa: esquema zod; cada `fuente.ref` existe; `min ≤ max`; valores > 0; compatibilidad simétrica entre fichas (A incompatible con B ⇒ B incompatible con A); `sinDosisPediatrica` coherente (true ⇔ no hay dosis `pediatrico`).
  - `scripts/validar-datos.ts`: lee `datos/medicamentos/*.yaml` y `datos/fuentes.yaml`, imprime errores y sale con código 1 si hay alguno.

- [ ] **Step 1: Tests** con los fixtures: ficha válida → `[]`; sin fuente → error que contiene `'fuente'`; `ref` inexistente → contiene `'no existe en fuentes.yaml'`; min > max → contiene `'min mayor que max'`; asimetría → contiene `'compatibilidad asimétrica'`; `sinDosisPediatrica: true` con dosis pediátrica → contiene `'sinDosisPediatrica'`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar. **Step 4:** Run → PASS.
- [ ] **Step 5:** `npm run validar` sobre carpetas vacías → sale 0 con `0 fichas validadas`.
- [ ] **Step 6:** Commit `feat: esquema y validación de fichas`.

### Task 6: Investigación y fichas de los 10 primeros medicamentos

**Files:**
- Create: `datos/fuentes.yaml`, `datos/medicamentos/{adrenalina,noradrenalina,amiodarona,atropina,adenosina,midazolam,fentanilo,morfina,ketamina,sulfato-de-magnesio}.yaml`, `informes/tanda-1-parte-1.md`

**Interfaces:**
- Consumes: esquema de Task 5.
- Produces: 10 fichas que pasan `npm run validar`; ids = nombre del archivo.

- [ ] **Step 1:** Buscar y registrar en `fuentes.yaml` (con fecha de consulta): folletos ISP de los productos chilenos de cada medicamento; Formulario Nacional de Medicamentos (MINSAL); al menos una guía de dilución EV de hospital o servicio de salud chileno; fichas técnicas CIMA; DailyMed; Stabilis; Pediamécum.
- [ ] **Step 2:** Por cada medicamento, llenar la ficha. Datos críticos (dosis, concentración máxima, tiempo mínimo, incompatibilidades) con ≥2 fuentes; si no coinciden, registrar en `meta.discrepancias` y usar el valor más conservador. Compatibilidad: entre los 10 y con SF 0,9 % y SG 5 %; lo que no esté en fuentes = `sin_datos`. Dejar `meta.revisadoPor` vacío.
- [ ] **Step 3:** Run `npm run validar` → `10 fichas validadas`, sin errores.
- [ ] **Step 4:** Escribir `informes/tanda-1-parte-1.md`: medicamentos, fuentes usadas por cada uno, discrepancias y decisiones.
- [ ] **Step 5:** Commit `datos: tanda 1 parte 1 (10 medicamentos, sin revisión clínica)`.
- [ ] **Step 6: Gate de revisión clínica.** Presentar el informe a Héctor. Aplicar sus correcciones, completar `meta.revisadoPor: "Héctor Salvo Agüero (TENS)"` y `meta.fechaRevision`, `npm run validar` → OK, commit `datos: revisión clínica tanda 1 parte 1`. No continuar a Task 12 sin esta revisión.

### Task 7: Carga de datos y búsqueda

**Files:**
- Create: `src/datos/cargar.ts`, `src/busqueda/buscar.ts`, `src/busqueda/buscar.test.ts`

**Interfaces:**
- Consumes: `Ficha` (Task 5), fichas (Task 6).
- Produces:
  - `medicamentos: Ficha[]` y `fuentes: Fuente[]` (de `import.meta.glob('/datos/medicamentos/*.yaml', { query: '?raw', import: 'default', eager: true })` + `yaml.parse` + `Ficha.parse`), ordenados por `nombre`.
  - `obtenerFicha(id: string): Ficha | undefined`
  - `buscar(texto: string, lista: Ficha[]): Ficha[]` — sin distinguir mayúsculas ni tildes; busca en `nombre` y `comerciales`; coincidencia por prefijo o substring, y tolerancia a errores de tipeo con distancia de Levenshtein ≤ 2 contra cada palabra (solo si el texto tiene ≥ 5 letras); orden: prefijo > substring > tolerancia.

- [ ] **Step 1: Tests** con 3 fichas de prueba (noradrenalina con comercial "Levophed", adrenalina, amiodarona): `buscar('nora')[0].id === 'noradrenalina'`; `buscar('LEVOPHED')[0].id === 'noradrenalina'`; `buscar('adrenalína')[0].id === 'adrenalina'`; `buscar('noradrenalia')[0].id === 'noradrenalina'`; `buscar('')` → `[]`; `buscar('xyz')` → `[]`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar. **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: carga de fichas y búsqueda tolerante`.

### Task 8: Inicio y lista por grupo

**Files:**
- Create: `src/app/paginas/Inicio.tsx`, `src/app/paginas/Inicio.test.tsx`, `src/app/recientes.ts`
- Modify: `src/app/App.tsx` (rutas `/`, `/grupo/:grupo`, `/ambito/:ambito`, `/m/:id`, `/m/:id/calcular`, `/acerca`)

**Interfaces:**
- Consumes: `medicamentos`, `buscar` (Task 7).
- Produces: `registrarReciente(id: string): void`, `leerRecientes(): string[]` (localStorage `dilucion-ev:recientes`, máx. 8, con try/catch). Enlaces `href="#/m/<id>"`.

- [ ] **Step 1: Tests:** escribir "nora" en el buscador → aparece el enlace "Noradrenalina"; los medicamentos con `altoRiesgo` muestran la etiqueta "Alto riesgo"; hacer clic en el acceso "SAMU" lista solo fichas con ámbito `samu`; con localStorage que lanza error, la página igual renderiza.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar (diseño móvil, letras grandes, buscador arriba, accesos por ámbito, grupos y recientes). **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: pantalla de inicio y listas`.

### Task 9: Ficha en pestañas

**Files:**
- Create: `src/app/paginas/Ficha.tsx`, `src/app/paginas/Ficha.test.tsx`, `src/app/componentes/Dato.tsx`

**Interfaces:**
- Consumes: `obtenerFicha`, `fuentes` (Task 7), `registrarReciente` (Task 8).
- Produces: `Dato` — muestra valor + unidad y un enlace a la fuente; si el valor no existe muestra exactamente "sin datos en las fuentes".

- [ ] **Step 1: Tests:** pestañas "Preparar", "Administrar", "Compatibilidad", "Seguridad", "Fuentes" visibles; en Compatibilidad, un `incompatible` lleva la clase/etiqueta "Incompatible" y `sin_datos` muestra "Sin datos"; un campo ausente (p. ej. `estabilidad.refrigeradoH`) muestra "sin datos en las fuentes"; un id inexistente muestra "Medicamento no encontrado"; abrir la ficha llama a `registrarReciente`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar; botón "Calcular" → `#/m/<id>/calcular`; las discrepancias de `meta` se muestran en la pestaña Fuentes. **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: ficha del medicamento en pestañas`.

### Task 10: Calculadora precargada

**Files:**
- Create: `src/app/paginas/Calculadora.tsx`, `src/app/paginas/Calculadora.test.tsx`

**Interfaces:**
- Consumes: calculadoras (Task 3), alertas (Task 4), `parsearNumero` (Task 2), `obtenerFicha` (Task 7).
- Produces: modos "Concentración", "Volumen a cargar", "Velocidad por tiempo", "Velocidad por dosis", "Dosis → velocidad", "Velocidad → dosis", "Pediátrica"; precarga presentación y primera dilución estándar de la ficha; ruta `#/calcular` = modo libre sin ficha.

- [ ] **Step 1: Tests**
  - Noradrenalina precargada (4 mg en 250 ml), peso "70", dosis "0,1" mcg/kg/min → muestra "26,3 ml/h" y la fórmula.
  - Dosis por encima del `max` de la ficha → aparece una alerta con rol `alert` y texto "supera la dosis máxima".
  - Peso vacío → muestra "Falta el peso" y ningún número de resultado.
  - Ficha con `sinDosisPediatrica: true` → el modo "Pediátrica" muestra exactamente "sin dosis pediátrica en la fuente" y no tiene botón de calcular.
  - Pediátrica sobre el tope → muestra el resultado limitado y el aviso "limitada a la dosis de adulto".
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar; el peso vive solo en el estado del componente (no se guarda). **Step 4:** Run → PASS.
- [ ] **Step 5:** Commit `feat: calculadora precargada con alertas`.

### Task 11: Aviso, Acerca de, tema y PWA sin internet

**Files:**
- Create: `src/app/paginas/Acerca.tsx`, `src/app/componentes/AvisoInicial.tsx`, `src/app/tema.ts`, tests `Acerca.test.tsx`, `AvisoInicial.test.tsx`, `src/build.test.ts`
- Modify: `vite.config.ts` (vite-plugin-pwa: `registerType: 'autoUpdate'`, manifiesto con `name: 'Dilución EV'`, `lang: 'es-CL'`, íconos 192/512, precache de todo el build), `src/app/App.tsx`

**Interfaces:**
- Produces: `AvisoInicial` (se muestra si no existe `dilucion-ev:aviso-aceptado` en localStorage; botón "Entendido" lo guarda); `tema.ts` con `aplicarTema('claro' | 'oscuro' | 'sistema')` y preferencia en localStorage.

- [ ] **Step 1: Tests:** primera apertura muestra el aviso exacto de Global Constraints y al pulsar "Entendido" desaparece y no vuelve a salir; Acerca muestra el aviso, la versión (`package.json`) y la lista de `fuentes`; cambiar a tema oscuro pone `data-theme="oscuro"` en `<html>`. `build.test.ts` (corre `vite build` una vez en `beforeAll`): `dist/manifest.webmanifest` existe y tiene `"name": "Dilución EV"`; `dist/sw.js` existe; `dist/index.html` referencia el manifiesto.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implementar. **Step 4:** Run → PASS.
- [ ] **Step 5:** Verificación manual: `npm run build && npx vite preview`; en el navegador cargar, cortar la red (DevTools → Offline), recargar `#/m/noradrenalina` → la ficha se ve.
- [ ] **Step 6:** Commit `feat: aviso, acerca de, tema oscuro y PWA offline`.

### Task 12: Repositorio y publicación

**Files:**
- Create: `.github/workflows/publicar.yml`, `README.md`

**Interfaces:**
- Consumes: todo lo anterior; requiere Task 6 Step 6 (revisión clínica) completa.

- [ ] **Step 1: Decisión de Héctor (antes de ejecutar):** GitHub Pages gratis exige repositorio **público**. Opciones: (a) hacer público el repo y publicar en GitHub Pages; (b) repo privado y publicar en Cloudflare Pages (gratis). Ejecutar la opción elegida.
- [ ] **Step 2:** Crear el repo `januch-6-6-6/dilucion-ev` con `gh repo create` (visibilidad según Step 1) y hacer push de `main`.
- [ ] **Step 3:** Workflow: en push a `main` → `npm ci && npm test && npm run build` → publicar `dist/`. Si cualquier paso falla, no se publica.
- [ ] **Step 4:** `README.md`: qué es, aviso de formación, cómo correrlo, cómo agregar una ficha, fuentes y estado de revisión.
- [ ] **Step 5:** Verificar: el workflow termina en verde y la URL pública abre la app, muestra el aviso y funciona en el celular (instalar como app).
- [ ] **Step 6:** Commit `ci: publicación automática` y anotar la URL en el README.
