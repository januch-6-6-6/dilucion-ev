# Comunidad de prácticas locales — Etapa 1: servidor — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dejar funcionando en Supabase la base de datos de la comunidad (tablas, reglas del consenso, permisos por fila, bitácora inmutable, catálogos DEIS y de medicamentos), con pruebas de permisos que corren en CI y bloquean la publicación si fallan. La app no cambia.

**Architecture:** Migraciones SQL versionadas en `supabase/migrations/`, aplicadas con la CLI de Supabase (`npx supabase db push`) primero al proyecto de prueba y después al real. No hay Docker en esta máquina: las pruebas corren contra el proyecto Supabase **de prueba** (remoto) usando `@supabase/supabase-js` desde Vitest, con usuarios sembrados por la clave de servicio. Cada archivo de prueba crea sus propios datos con un sufijo aleatorio y no borra nada (la bitácora no se puede borrar por diseño).

**Tech Stack:** Supabase (PostgreSQL 15, Auth, RLS), CLI `supabase` (npm, dev), `@supabase/supabase-js` (dev en esta etapa), Vitest 5, Python 3 + `urllib` para la carga de catálogos, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-02-comunidad-practicas-locales-design.md` (secciones 4, 5, 9, 10-Etapa 1 y 11).

## Global Constraints

- Nada se publica sin el administrador: los cambios de estado `en_bandeja → aprobada | rechazada` y `aprobada → retirada` solo ocurren dentro de funciones que verifican `es_admin()`.
- Las notas son texto: `texto` y `texto_publicado` tienen entre 1 y 500 caracteres **sin contar espacios al inicio y al final** (`char_length(btrim(texto)) between 1 and 500`).
- Umbral por defecto: `3` votos a favor de personas del mismo hospital **y** total a favor > total en contra.
- La `bitacora` solo admite INSERT; UPDATE y DELETE fallan para cualquier rol, también `service_role` y el administrador (disparador que lanza excepción, no solo RLS).
- La clave de servicio nunca va al navegador ni al repositorio: vive en `.env.supabase` (ignorado por git) y en secretos de GitHub.
- `npm test` (las 241 pruebas actuales) no debe depender de Supabase ni de red: las pruebas de Supabase viven aparte y se corren con `npm run test:supabase`.
- Nombres de tablas, columnas, estados y acciones de bitácora: exactamente los de la spec §5.1 (en español, minúsculas, con guion bajo).
- Todo texto visible o mensaje de error en español de Chile.

## Review Focus

1. **Invitada recién creada, todavía sin hospital ni país**: no puede proponer ni votar (error claro), en vez de crear filas con hospital nulo que rompan el conteo. → prueba en Task 4 y Task 5.
2. **Votos después de llegar a bandeja o en propuestas ya resueltas**: se rechazan; la propuesta no retrocede de estado aunque cambien los votos. → prueba en Task 5.
3. **Persona suspendida con votos previos**: sus votos se conservan (Héctor los ve) pero no cuentan en evaluaciones posteriores, y no puede votar ni proponer. → prueba en Task 5.
4. **Texto solo con espacios o de 501 caracteres**: lo rechaza la base de datos aunque la app no valide. → prueba en Task 4.
5. **Recargar el catálogo de medicamentos o DEIS cuando una ficha o un establecimiento desaparece**: la carga solo inserta o actualiza (y marca `vigente = false`), nunca borra filas con propuestas asociadas. → prueba en Task 7.

---

## Estructura de archivos

| Archivo | Responsabilidad |
|---|---|
| `supabase/config.toml` | Config de la CLI (`npx supabase init`). |
| `supabase/migrations/20261002000001_esquema.sql` | Tablas, restricciones, índices, `ajustes` con su fila. |
| `supabase/migrations/20261002000002_personas_bitacora.sql` | `es_admin()`, `persona_activa()`, bitácora inmutable, historial de hospital. |
| `supabase/migrations/20261002000003_propuestas.sql` | Reglas de propuestas, vista `propuestas_comunidad`, `retirar_propuesta`. |
| `supabase/migrations/20261002000004_votos_consenso.sql` | Votos, `evaluar_umbral`. |
| `supabase/migrations/20261002000005_administracion.sql` | Funciones de administrador y vista `notas_publicadas`. |
| `supabase/migrations/20261002000006_rls.sql` | `enable row level security`, políticas y `grant`s de todo lo anterior. |
| `supabase/pruebas/escenario.ts` | Crea usuarios, hospitales y clientes por rol para cada archivo de prueba. |
| `supabase/pruebas/*.test.ts` | Pruebas de permisos y reglas (una por tema). |
| `vitest.supabase.config.ts` | Config de Vitest solo para `supabase/pruebas`. |
| `scripts/supabase/cargar_catalogos.py` | Carga/actualiza `establecimientos` (DEIS) y `medicamentos` (desde `datos/medicamentos/*.yaml`). |
| `scripts/supabase/test_cargar_catalogos.py` | Pruebas de la transformación del catálogo (sin red). |
| `.github/workflows/publicar.yml` | Nuevo job `supabase` que aplica migraciones al proyecto de prueba y corre las pruebas; `publicar` depende de él. |
| `docs/supabase.md` | Cómo aplicar migraciones al proyecto real, secretos y ajustes manuales del panel. |

Las políticas de RLS se escriben juntas en la migración 6 para revisarlas en un solo lugar; cada Task que crea una tabla agrega sus políticas a ese archivo (las migraciones aún no aplicadas al proyecto real se pueden editar; tras el Task 8 toda corrección va en una migración nueva).

---

### Task 1: Proyectos Supabase, CLI y arnés de pruebas

**Files:**
- Create: `supabase/config.toml`, `supabase/migrations/20261002000001_esquema.sql` (solo `ajustes` en este task), `supabase/pruebas/escenario.ts`, `supabase/pruebas/humo.test.ts`, `vitest.supabase.config.ts`, `.env.supabase.ejemplo`
- Modify: `package.json` (scripts y devDependencies), `vite.config.ts` (excluir `supabase/**` de `npm test`), `.gitignore` (`.env.supabase`)

**Interfaces:**
- Produces:
  - Variables en `.env.supabase` (y secretos CI): `SUPABASE_PRUEBA_URL`, `SUPABASE_PRUEBA_ANON_KEY`, `SUPABASE_PRUEBA_SERVICE_KEY`, `SUPABASE_PRUEBA_REF`, `SUPABASE_PRUEBA_DB_PASSWORD`, `SUPABASE_REAL_REF`, `SUPABASE_REAL_DB_PASSWORD`, `SUPABASE_ACCESS_TOKEN`.
  - `escenario.ts`:
    - `clienteServicio(): SupabaseClient`
    - `clientePublico(): SupabaseClient` (anon, sin sesión)
    - `crearUsuario(rol: { nombre: string; establecimiento?: string; pais?: string; admin?: boolean; suspendida?: boolean }): Promise<{ id: string; cliente: SupabaseClient }>` — crea el usuario con contraseña aleatoria vía `auth.admin.createUser({ email_confirm: true })`, inserta su fila en `personas` con la clave de servicio, inicia sesión con contraseña y devuelve el cliente autenticado. Correo: `prueba+<sufijo>-<nombre>@dilucion-ev.test`.
    - `crearHospital(nombre: string): Promise<string>` — inserta un establecimiento de prueba con código `PRUEBA-<sufijo>-<nombre>` y devuelve el código.
    - `medicamentoDePrueba(): Promise<string>` — asegura y devuelve el id `prueba-medicamento`.
    - `sufijo: string` — aleatorio por archivo de prueba.
  - Script npm `test:supabase`: `vitest run --config vitest.supabase.config.ts`.

- [ ] **Step 1: Prerrequisito manual de Héctor (documentarlo en `docs/supabase.md`)** — crear en supabase.com dos proyectos gratuitos, `dilucion-ev` (real) y `dilucion-ev-pruebas`, región São Paulo; generar un *access token* personal; copiar URL, anon key, service key, ref y contraseña de base de datos de cada uno a `.env.supabase` siguiendo `.env.supabase.ejemplo`. En ambos proyectos: Authentication → Sign In / Providers → desactivar «Allow new users to sign up». Resultado comprobable: `npx supabase projects list` muestra los dos proyectos.

- [ ] **Step 2: Instalar dependencias y config** — `npm i -D supabase @supabase/supabase-js dotenv`; `npx supabase init`; excluir `supabase/**` en `test.exclude` de `vite.config.ts` (manteniendo los excludes por defecto de Vitest).

- [ ] **Step 3: Escribir la prueba de humo `supabase/pruebas/humo.test.ts`**

```ts
it('el público no lee ajustes y el servicio sí', async () => {
  const { data: publico } = await clientePublico().from('ajustes').select('*')
  expect(publico).toEqual([])
  const { data } = await clienteServicio().from('ajustes').select('umbral_votos').single()
  expect(data?.umbral_votos).toBe(3)
})
```

- [ ] **Step 4: Ejecutar y verificar que falla** — `npm run test:supabase -- humo`. Esperado: FAIL, «relation "public.ajustes" does not exist».

- [ ] **Step 5: Migración 1 (parcial)** — tabla `ajustes(id smallint primary key default 1 check (id = 1), umbral_votos int not null default 3 check (umbral_votos between 1 and 50))`, insertar su única fila; en la migración 6 (crearla ahora con solo esto): `alter table ajustes enable row level security;` sin políticas para anon/authenticated. Aplicar: `npx supabase db push --project-ref $SUPABASE_PRUEBA_REF --password $SUPABASE_PRUEBA_DB_PASSWORD`.

- [ ] **Step 6: Ejecutar y verificar que pasa** — `npm run test:supabase -- humo` → PASS. `npm test` → 241 passed (no toca Supabase).

- [ ] **Step 7: Commit** — `git commit -m "chore(supabase): proyecto, CLI y arnés de pruebas"`

### Task 2: Esquema completo

**Files:**
- Modify: `supabase/migrations/20261002000001_esquema.sql`, `supabase/migrations/20261002000006_rls.sql`
- Test: `supabase/pruebas/esquema.test.ts`

**Interfaces:**
- Produces: tablas `establecimientos`, `medicamentos`, `personas`, `administradores`, `historial_hospital`, `propuestas`, `votos`, `bitacora` con las columnas de la spec §5.1. Tipos: enum `estado_propuesta` (`en_votacion`, `en_bandeja`, `aprobada`, `rechazada`, `retirada`), enum `estado_persona` (`activa`, `suspendida`). Ids `uuid default gen_random_uuid()` salvo `establecimientos.codigo text` y `medicamentos.id text`. Fechas `timestamptz default now()`.

Restricciones que fija este task:
- `personas.id` FK a `auth.users(id)`; `check (establecimiento is null or pais_extranjero is null)`.
- `establecimientos`: `codigo text pk, nombre, tipo, comuna, region text, vigente boolean not null default true`.
- `propuestas.medicamento` FK `medicamentos(id) on delete restrict`; `propuestas.establecimiento` FK `on delete restrict`; check de longitud de `texto` y `texto_publicado` (Global Constraints).
- `votos`: `unique (propuesta, persona)`.
- `bitacora.detalle jsonb not null default '{}'`.

- [ ] **Step 1: Prueba** `esquema.test.ts`: con la clave de servicio, (a) insertar una persona con `establecimiento` y `pais_extranjero` a la vez falla con código `23514`; (b) insertar una propuesta para un medicamento inexistente falla con `23503`; (c) borrar un medicamento que tiene una propuesta falla con `23503`.
- [ ] **Step 2: Ejecutar → FAIL** (tablas inexistentes).
- [ ] **Step 3: Escribir las tablas en la migración 1 y `enable row level security` de todas en la migración 6** (sin políticas todavía). Aplicar al proyecto de prueba con `db push`.
- [ ] **Step 4: Ejecutar → PASS.** Agregar al test de humo: el público no lee `personas`, `propuestas`, `votos` ni `bitacora` (listas vacías).
- [ ] **Step 5: Commit** — `feat(supabase): esquema de la comunidad`

### Task 3: Administrador, personas activas, historial de hospital y bitácora inmutable

**Files:**
- Create: `supabase/migrations/20261002000002_personas_bitacora.sql`
- Modify: `supabase/migrations/20261002000006_rls.sql`
- Test: `supabase/pruebas/personas.test.ts`, `supabase/pruebas/bitacora.test.ts`

**Interfaces:**
- Produces:
  - `es_admin() returns boolean` — `security definer`, `stable`, `search_path = public`: existe `administradores.persona = auth.uid()`.
  - `persona_activa() returns boolean` — la fila `personas` de `auth.uid()` existe y su `estado = 'activa'`.
  - `registrar(accion text, objeto text, detalle jsonb) returns void` — `security definer`; inserta en `bitacora` con `actor = auth.uid()`. La usan los disparadores y funciones de Tasks 4–6.
  - Disparador `bitacora_inmutable` (BEFORE UPDATE OR DELETE on `bitacora`) que hace `raise exception 'La bitácora no se puede modificar'`.
  - Disparador sobre `personas` (AFTER UPDATE OF `establecimiento`, `pais_extranjero`): inserta en `historial_hospital` (`desde`/`hacia` como código DEIS o `'extranjero: <país>'`) y `registrar('cambio_hospital', persona, {desde, hacia})`.
  - Políticas: una persona lee su propia fila de `personas` y su `historial_hospital`; actualiza **solo** `establecimiento` y `pais_extranjero` de su fila si `persona_activa()` (`grant update (establecimiento, pais_extranjero) on personas to authenticated` + política `using (id = auth.uid())`). El admin lee todas las `personas`, `historial_hospital` y `bitacora`. `establecimientos` y `medicamentos`: lectura para `anon` y `authenticated`.

- [ ] **Step 1: Pruebas** `personas.test.ts`:
  - invitada A cambia su hospital de X a Y → su `historial_hospital` tiene una fila `X → Y` y la bitácora (leída por el admin) tiene `cambio_hospital` con actor A;
  - A elige «fuera de Chile» (`establecimiento = null, pais_extranjero = 'Perú'`) → historial `Y → extranjero: Perú`;
  - A intenta cambiar su `estado` o su `nombre` → error (sin permiso de columna);
  - A no lee la fila de B; la suspendida no puede cambiar su hospital.
  `bitacora.test.ts`:
  - A no lee la bitácora; el admin sí;
  - el admin intenta `update` y `delete` sobre una fila de bitácora → error con «La bitácora no se puede modificar»;
  - la clave de servicio intenta `delete` → el mismo error.
- [ ] **Step 2: Ejecutar → FAIL.**
- [ ] **Step 3: Implementar la migración 2 y sus políticas en la migración 6; aplicar.**
- [ ] **Step 4: Ejecutar → PASS** (`npm run test:supabase`).
- [ ] **Step 5: Commit** — `feat(supabase): personas, historial de hospital y bitácora inmutable`

### Task 4: Propuestas

**Files:**
- Create: `supabase/migrations/20261002000003_propuestas.sql`
- Modify: `supabase/migrations/20261002000006_rls.sql`
- Test: `supabase/pruebas/propuestas.test.ts`

**Interfaces:**
- Consumes: `persona_activa()`, `es_admin()`, `registrar()` (Task 3).
- Produces:
  - Disparador BEFORE INSERT en `propuestas`: fuerza `autora = auth.uid()`, `establecimiento` = el de la persona (ignora lo que mande el cliente), `estado = 'en_votacion'`, `texto_publicado = null`; si la persona no está activa → `raise exception 'Tu acceso está suspendido'`; si no tiene `establecimiento` (sin hospital o fuera de Chile) → `raise exception 'Las prácticas locales se proponen desde hospitales chilenos'`. AFTER INSERT → `registrar('propuso', id, {medicamento, establecimiento})`.
  - `retirar_propuesta(p uuid) returns void` — `security definer`; solo la autora, solo si `en_votacion`; pasa a `retirada` y registra `retiro`.
  - Vista `propuestas_comunidad` (dueño `postgres`, **sin** `security_invoker`): columnas `id, medicamento, establecimiento, nombre_establecimiento, texto, estado, creada_el, a_favor, en_contra, es_mia boolean, mi_voto boolean null`. Filas visibles: si `persona_activa()` → las `en_votacion` y `en_bandeja` de todos, más las propias en cualquier estado; si no → ninguna. **No expone la autora.** `grant select` a `authenticated`.
  - Políticas: `insert` en `propuestas` para `authenticated` con `persona_activa()`; ningún `update`/`delete` directo para `authenticated`; el admin lee todas las propuestas (tabla).

- [ ] **Step 1: Pruebas** `propuestas.test.ts`:
  - A (hospital X) propone para `prueba-medicamento` mandando `establecimiento = Y` y `estado = 'aprobada'` → la fila queda con X y `en_votacion`;
  - D (fuera de Chile) y E (recién invitada, sin hospital) proponen → error «Las prácticas locales se proponen desde hospitales chilenos»;
  - la suspendida propone → error «Tu acceso está suspendido»;
  - texto `'   '` y texto de 501 caracteres → error `23514`; texto de 500 caracteres → OK;
  - B ve la propuesta de A en `propuestas_comunidad` con `es_mia = false` y **sin** columna de autora; el público no ve nada;
  - A retira su propuesta → `retirada`; B intenta retirarla → error; A intenta `update` directo de `texto` → error.
- [ ] **Step 2: Ejecutar → FAIL.**
- [ ] **Step 3: Implementar migración 3 y políticas; aplicar.**
- [ ] **Step 4: Ejecutar → PASS.**
- [ ] **Step 5: Commit** — `feat(supabase): propuestas y vista de la comunidad`

### Task 5: Votos y consenso

**Files:**
- Create: `supabase/migrations/20261002000004_votos_consenso.sql`
- Modify: `supabase/migrations/20261002000006_rls.sql`
- Test: `supabase/pruebas/consenso.test.ts`

**Interfaces:**
- Consumes: `persona_activa()`, `registrar()`, `propuestas_comunidad` (Tasks 3–4).
- Produces:
  - Disparador BEFORE INSERT OR UPDATE en `votos`: fuerza `persona = auth.uid()` y copia `establecimiento_al_votar` / `pais_al_votar` desde `personas` (ignora valores del cliente); rechaza si la persona no está activa («Tu acceso está suspendido»), si no tiene hospital ni país («Elige tu hospital antes de votar»), si es la autora («No puedes votar tu propia propuesta») o si la propuesta no está `en_votacion` («La votación de esta propuesta está cerrada»). En UPDATE solo puede cambiar `a_favor`. Registra `voto` o `cambio_voto`.
  - `evaluar_umbral(p uuid) returns void` — `security definer`, llamada AFTER INSERT OR UPDATE en `votos`. Cuenta solo votos de personas **activas**: `a_favor_local` = a favor con `establecimiento_al_votar` = el de la propuesta; `total_a_favor`, `total_en_contra` = todos (incluidos los de fuera de Chile). Si la propuesta está `en_votacion` y `a_favor_local >= ajustes.umbral_votos` y `total_a_favor > total_en_contra` → `en_bandeja` (y registra `paso_a_bandeja` con actor nulo vía `registrar`). Nunca retrocede.
  - Políticas: `insert` y `update` de `votos` para `authenticated`; cada persona lee solo sus votos; el admin lee todos.

- [ ] **Step 1: Pruebas** `consenso.test.ts` (umbral 3; A propone en X; B, F, G de X; C de Y; D de Perú; S que luego se suspende):
  - B y F votan a favor → sigue `en_votacion` (2 locales);
  - C y D votan a favor → sigue `en_votacion` (no son locales);
  - G vota a favor → pasa a `en_bandeja` exactamente en ese voto;
  - con otra propuesta: 3 locales a favor y 4 en contra (C, D y dos más) → sigue `en_votacion`;
  - votar o cambiar voto en una propuesta `en_bandeja` → «La votación de esta propuesta está cerrada»; cambiar votos a «en contra» antes de eso no hace retroceder una que ya pasó;
  - S vota a favor, luego el admin la suspende (con la clave de servicio en este task; con `suspender()` en el Task 6) → el voto de S sigue en la tabla pero no cuenta: con S + otros 2 locales, la propuesta no pasa;
  - A vota su propia propuesta → error; B vota dos veces (insert) → `23505`; B cambia su voto (update) → OK y la bitácora tiene `cambio_voto`;
  - E (sin hospital) vota → «Elige tu hospital antes de votar»;
  - B manda `establecimiento_al_votar = Y` al votar → la fila queda con X;
  - B no ve el voto de F (select a `votos` devuelve solo el propio); `propuestas_comunidad` muestra los conteos correctos.
- [ ] **Step 2: Ejecutar → FAIL.**
- [ ] **Step 3: Implementar migración 4 y políticas; aplicar.**
- [ ] **Step 4: Ejecutar → PASS.**
- [ ] **Step 5: Commit** — `feat(supabase): votos y regla de consenso`

### Task 6: Funciones del administrador y notas publicadas

**Files:**
- Create: `supabase/migrations/20261002000005_administracion.sql`
- Modify: `supabase/migrations/20261002000006_rls.sql`
- Test: `supabase/pruebas/administracion.test.ts`

**Interfaces:**
- Consumes: `es_admin()`, `registrar()`, `evaluar_umbral()`.
- Produces (todas `security definer`, empiezan con `if not es_admin() then raise exception 'Solo el administrador puede hacer esto'`, y registran en la bitácora en la misma transacción):
  - `aprobar(p uuid, texto_final text default null) returns void` — desde `en_votacion` o `en_bandeja`; `texto_publicado = coalesce(texto_final, texto)`; acción `aprobo` o `edito_y_aprobo` (si `texto_final` difiere, `detalle` guarda antes y después); `resuelta_el = now()`.
  - `rechazar(p uuid, comentario text) returns void` — comentario obligatorio (1–500); desde `en_votacion` o `en_bandeja`; acción `rechazo`.
  - `retirar_nota(p uuid, motivo text) returns void` — solo desde `aprobada`; pasa a `retirada`; acción `retiro`.
  - `suspender(persona uuid) returns void`, `reactivar(persona uuid) returns void` — acciones `suspendio`, `reactivo`; el admin no puede suspenderse a sí mismo.
  - `cambiar_umbral(n int) returns void` — acción `cambio_umbral` con antes y después; no reevalúa propuestas existentes.
  - Vista `notas_publicadas` (dueño `postgres`): `id, medicamento, establecimiento, nombre_establecimiento, texto_publicado, resuelta_el, votos_a_favor` de las `aprobada`; **sin autora**; `grant select to anon, authenticated`.
  - `grant execute` de estas funciones a `authenticated` (la verificación está dentro); `revoke` de `anon`.

- [ ] **Step 1: Pruebas** `administracion.test.ts`:
  - B (invitada) llama `aprobar`, `rechazar`, `suspender` y `cambiar_umbral` → «Solo el administrador puede hacer esto»; el público también;
  - el admin aprueba una `en_bandeja` con texto editado → `notas_publicadas` (leída por el **público**) tiene la nota con el texto editado y `votos_a_favor` correcto, y no tiene columna de autora; la bitácora tiene `edito_y_aprobo` con antes y después;
  - el admin aprueba una `en_votacion` sin umbral → OK (la decisión final es suya);
  - rechazar sin comentario → error; rechazar con comentario → la autora ve `rechazada` en `propuestas_comunidad` (fila propia);
  - `retirar_nota` → desaparece de `notas_publicadas`; retirar algo que no está `aprobada` → error;
  - `suspender(S)` → S no puede votar; `reactivar(S)` → puede; el admin no puede suspenderse;
  - `cambiar_umbral(2)` → una propuesta nueva pasa a bandeja con 2 votos locales; una anterior con 2 votos no cambia hasta que reciba otro voto.
- [ ] **Step 2: Ejecutar → FAIL.**
- [ ] **Step 3: Implementar migración 5 y grants; aplicar.**
- [ ] **Step 4: Ejecutar → PASS** (toda la suite `npm run test:supabase`).
- [ ] **Step 5: Commit** — `feat(supabase): funciones del administrador y notas publicadas`

### Task 7: Carga de catálogos (DEIS y medicamentos)

**Files:**
- Create: `scripts/supabase/cargar_catalogos.py`, `scripts/supabase/test_cargar_catalogos.py`, `scripts/supabase/__init__.py`

**Interfaces:**
- Consumes: tablas `establecimientos` y `medicamentos` (Task 2); `SUPABASE_*_URL` y `SUPABASE_*_SERVICE_KEY`.
- Produces:
  - `filas_medicamentos(carpeta: Path) -> list[dict]` — `{'id': <id>}` por cada `datos/medicamentos/*.yaml`.
  - `filas_establecimientos(crudo: list[dict]) -> list[dict]` — normaliza el listado DEIS a `{codigo, nombre, tipo, comuna, region, vigente}`; descarta filas sin código; deduplica por código.
  - `subir(url: str, clave: str, tabla: str, filas: list[dict], conflicto: str) -> int` — upsert por PostgREST (`POST /rest/v1/<tabla>?on_conflict=<conflicto>` con `Prefer: resolution=merge-duplicates`), en lotes de 500.
  - `marcar_no_vigentes(url, clave, codigos_actuales: set[str]) -> int` — `vigente = false` para los establecimientos que ya no vienen en el listado (nunca borra).
  - CLI: `python3 scripts/supabase/cargar_catalogos.py --destino prueba|real [--deis <archivo>]`.

- [ ] **Step 1: Confirmar la fuente DEIS** — encontrar la descarga oficial vigente del listado de establecimientos de salud (DEIS / datos.gob.cl), anotar en `docs/supabase.md` la URL, el formato (CSV o XLSX) y las columnas reales que se mapean a `codigo, nombre, tipo, comuna, region, vigente`. Guardar una muestra de 5 filas en `scripts/supabase/muestra_deis.csv` para las pruebas.
- [ ] **Step 2: Pruebas** `test_cargar_catalogos.py` (pytest, sin red):
  - `filas_medicamentos(Path('datos/medicamentos'))` devuelve 89 filas e incluye `{'id': 'ceftriaxona'}`;
  - `filas_establecimientos` sobre la muestra: mapea las columnas, descarta la fila sin código y deja un solo registro cuando el código se repite;
  - `marcar_no_vigentes` se prueba con `subir`/`urllib` simulados: el cuerpo enviado es un PATCH con `vigente=false` filtrado por `codigo=not.in.(...)`, y nunca hay un DELETE.
- [ ] **Step 3: Ejecutar → FAIL** (`python3 -m pytest scripts/supabase -q`).
- [ ] **Step 4: Implementar.** Validar que en el proyecto de prueba, tras cargar, una propuesta existente sobre un medicamento sigue intacta (los upsert no tocan FKs).
- [ ] **Step 5: Ejecutar → PASS**; cargar en el proyecto de prueba: `python3 scripts/supabase/cargar_catalogos.py --destino prueba` → imprime cuántos establecimientos y medicamentos se cargaron (89 medicamentos).
- [ ] **Step 6: Commit** — `feat(supabase): carga de catálogos DEIS y medicamentos`

### Task 8: CI y proyecto real

**Files:**
- Modify: `.github/workflows/publicar.yml`
- Create: `docs/supabase.md` (completar)

**Interfaces:**
- Consumes: todo lo anterior; secretos de GitHub con los nombres de Task 1.

- [ ] **Step 1: Job `supabase` en `publicar.yml`** — corre en cada push a `main`; si no existe el secreto `SUPABASE_PRUEBA_REF`, termina con éxito y un aviso (para no bloquear publicaciones si se borran los secretos). Si existe: `npm ci`, `npx supabase db push --project-ref … --password …` al proyecto de prueba, `npm run test:supabase`, `python3 -m pytest scripts/supabase -q`. `publicar` pasa a `needs: [construir, supabase]`.
- [ ] **Step 2: Cargar los secretos** en GitHub (`gh secret set` con los valores de `.env.supabase`, sin imprimirlos) y hacer push. Esperado: el workflow termina `success` y la app sigue publicada igual.
- [ ] **Step 3: Verificar que bloquea** — en una rama, cambiar temporalmente una política para que el público lea `personas`; abrir el workflow con `workflow_dispatch` sobre esa rama → el job `supabase` falla y `publicar` no corre. Descartar la rama.
- [ ] **Step 4: Aplicar al proyecto real** — `npx supabase db push --project-ref $SUPABASE_REAL_REF …`; `python3 scripts/supabase/cargar_catalogos.py --destino real`; con la clave de servicio, crear la fila de Héctor en `personas` (con su correo hectorsalvo32@gmail.com, invitado desde el panel de Supabase) y en `administradores`. Comprobar con el cliente público que `notas_publicadas` responde `[]` y que `personas` responde `[]`.
- [ ] **Step 5: Documentar en `docs/supabase.md`** — orden de aplicación (prueba → real), cómo correr las pruebas, dónde están los secretos, la casilla «Allow new users to sign up» desactivada, la pausa por inactividad del plan gratis y cómo reactivarla, y que tras esta etapa las migraciones ya aplicadas no se editan.
- [ ] **Step 6: Commit** — `ci(supabase): pruebas de permisos antes de publicar`
