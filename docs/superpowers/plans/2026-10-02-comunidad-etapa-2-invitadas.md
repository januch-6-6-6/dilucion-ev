# Comunidad de prácticas locales — Etapa 2: invitadas — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Que una persona invitada por Héctor pueda entrar a la app con un enlace enviado a su correo, elegir su hospital, proponer una práctica local, votar las de otras y ver el estado de las suyas. Sin Supabase configurado, la app se ve y funciona exactamente como hoy.

**Architecture:** Una capa delgada `src/comunidad/api.ts` (interfaz `ComunidadApi` + implementación sobre `@supabase/supabase-js`) aísla todo lo que habla con el servidor. Un `ComunidadProvider` la expone por contexto; las pantallas nuevas dependen solo de la interfaz, así que sus pruebas inyectan una API falsa. La implementación real se prueba contra el proyecto Supabase de pruebas (ya existente, Etapa 1). Acceso por enlace mágico con flujo PKCE (`?code=…`, compatible con `HashRouter`).

**Tech Stack:** React 19 + TypeScript + Vite + `react-router-dom` (HashRouter), `@supabase/supabase-js` (pasa a dependencia de ejecución), Vitest + Testing Library, pytest para el script de invitación.

**Spec:** `docs/superpowers/specs/2026-10-02-comunidad-practicas-locales-design.md` (§4, §6.2, §7, §8, §10-Etapa 2). Servidor de la Etapa 1: `docs/supabase.md`. Esta etapa continúa sobre la rama `comunidad-etapa-1`.

## Prerrequisitos de Héctor (antes de la Task 1)

1. **Un servicio de correo propio para Supabase.** El correo incluido en Supabase está limitado a 2–4 mensajes por hora y no sirve para invitadas reales. Elegir una opción y crearla:
   - **A (recomendada para partir):** SMTP de Gmail con una *contraseña de aplicación* de `hectorsalvo32@gmail.com` (Cuenta de Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones). Gratis, hasta ~500 correos al día; el remitente aparece con la dirección de Gmail.
   - **B:** Resend con un dominio propio verificado (≈ USD 10 al año el dominio). Resend sin dominio solo entrega a la cuenta dueña.
2. **Pegar la configuración SMTP en el panel de Supabase** de **ambos** proyectos (Authentication → SMTP Settings): host, puerto, usuario, contraseña de aplicación, remitente. Esta contraseña no se le entrega a Claude.

## Global Constraints

- Sin `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY` la app compila y se comporta como hoy: ningún enlace, botón ni pantalla de comunidad. Las 241 pruebas actuales siguen pasando sin esas variables.
- La comunidad requiere internet; los datos clínicos y las calculadoras nunca dependen de ella.
- Las notas son texto de **1 a 500 caracteres sin contar espacios al inicio y al final**, contados como la base de datos (`char_length` = puntos de código Unicode), no como `String.length`.
- Todo texto visible en español de Chile. Mensajes exactos de la spec: «Este correo no tiene invitación», «Proponer práctica local», «De acuerdo» / «No de acuerdo», «Mis propuestas», «Las prácticas locales se proponen desde hospitales chilenos; puedes votar», «Tu acceso está suspendido».
- La clave pública (`sb_publishable_…`) puede ir en el código compilado; la de servicio (`sb_secret_…`) nunca va a la app.
- El registro público de cuentas sigue desactivado: solo entra quien Héctor invitó.
- Accesibilidad: cada control tiene nombre accesible; los estados de carga y error se anuncian (`role="status"` / `role="alert"`); contraste AA en tema claro y oscuro, como el resto de la app.

## Review Focus

1. **Enlace mágico con HashRouter:** al volver del correo la persona debe aterrizar en `/comunidad` con sesión iniciada y la URL sin `?code=`. → prueba en Task 3.
2. **Conteo de caracteres con emoji y saltos de línea:** 500 caracteres exactos con emoji deben aceptarse y 501 rechazarse antes de enviar. → prueba en Task 5.
3. **Fallo de red o sesión vencida al proponer o votar:** mensaje claro y el texto escrito no se pierde. → pruebas en Task 5 y 6.
4. **Doble clic o dos toques seguidos en «De acuerdo»:** un solo voto y botón deshabilitado mientras se envía. → prueba en Task 6.
5. **Persona suspendida, o recién invitada sin hospital:** ve mensajes comprensibles en vez de errores técnicos y no ve controles que no puede usar. → pruebas en Task 3, 4 y 5.

---

## Estructura de archivos

| Archivo | Responsabilidad |
|---|---|
| `src/comunidad/tipos.ts` | Tipos del dominio (`Persona`, `Establecimiento`, `Propuesta`, `MiPropuesta`, `ErrorComunidad`) y `contarCaracteres`. |
| `src/comunidad/api.ts` | `ComunidadApi` y `crearApi(cliente)` sobre supabase-js. Único lugar que conoce tablas, vistas y mensajes del servidor. |
| `src/comunidad/cliente.ts` | `crearClienteSupabase()`: lee `import.meta.env`, configura PKCE y persistencia; devuelve `null` si faltan las variables. |
| `src/comunidad/ComunidadProvider.tsx` | Contexto: `disponible`, sesión, perfil, `api`; hook `useComunidad()`. |
| `src/comunidad/paginas/Entrar.tsx`, `ElegirHospital.tsx`, `Proponer.tsx`, `Comunidad.tsx`, `MisPropuestas.tsx`, `Privacidad.tsx` | Pantallas. |
| `src/comunidad/fake.ts` | `crearApiFalsa()` para pruebas de pantallas (en memoria, con la misma interfaz). |
| `src/app/App.tsx`, `src/app/paginas/Ficha.tsx`, `src/app/paginas/Acerca.tsx` | Rutas nuevas, botón «Proponer práctica local», enlaces de pie y de privacidad. |
| `supabase/pruebas/api.test.ts`, `supabase/pruebas/auth.test.ts` | La API real contra el proyecto de pruebas; acceso de correos no invitados. |
| `scripts/supabase/invitar.py`, `scripts/supabase/test_invitar.py` | Invitar personas (script local de Héctor). |
| `.github/workflows/publicar.yml` | Variables `VITE_*` en el job de compilación. |

---

### Task 1: Configuración de acceso en Supabase y verificación del correo

**Files:**
- Create: `supabase/pruebas/auth.test.ts`
- Modify: `docs/supabase.md`

**Interfaces:**
- Produces: ambos proyectos con `site_url = https://januch-6-6-6.github.io/dilucion-ev/` y lista de redirecciones que incluye `https://januch-6-6-6.github.io/dilucion-ev/**` y `http://localhost:5173/**`; correo propio configurado (prerrequisito 2).

- [ ] **Step 1: Prueba** `auth.test.ts`: `clientePublico().auth.signInWithOtp({ email: 'nadie+<sufijo>@dilucion-ev.test', options: { shouldCreateUser: false } })` devuelve un error con `status` 422 (no envía correo); `signUp` sigue rechazado. Ejecutar: `npm run test:supabase -- auth`. Expected: PASS (el registro está desactivado desde la Etapa 1); anotar en el ledger el texto exacto de `error.message` y `error.code`, que `api.ts` usará para reconocer «sin invitación».
- [ ] **Step 2: Configurar las URL permitidas** en los dos proyectos con la API de gestión (`PATCH /v1/projects/{ref}/config/auth` con `site_url` y `uri_allow_list`), leyendo la configuración con `GET` antes y después. Verificar con el `GET` que el valor quedó. No tocar ningún campo de SMTP.
- [ ] **Step 3: Verificar el correo de punta a punta, una sola vez y a mano:** con la clave de servicio crear (o reutilizar) a Héctor como usuario en **pruebas**, pedir un enlace a `hectorsalvo32@gmail.com` y confirmar que llega en menos de un minuto, desde el remitente configurado y no en spam. Si no llega, parar y revisar el prerrequisito 2.
- [ ] **Step 4: Documentar** en `docs/supabase.md` la configuración de acceso (URL, PKCE, límites de correo del proveedor elegido).
- [ ] **Step 5: Commit** — `docs(supabase): configuración de acceso por enlace mágico`

### Task 2: Cliente y capa de API

**Files:**
- Create: `src/comunidad/tipos.ts`, `src/comunidad/cliente.ts`, `src/comunidad/api.ts`, `supabase/pruebas/api.test.ts`
- Modify: `package.json` (mover `@supabase/supabase-js` a `dependencies`), `vitest.supabase.config.ts` (permitir importar desde `src/`)

**Interfaces:**
- Produces (en `tipos.ts`):
  - `type EstadoPropuesta = 'en_votacion' | 'en_bandeja' | 'aprobada' | 'rechazada' | 'retirada'`
  - `interface Persona { id: string; nombre: string; establecimiento: string | null; paisExtranjero: string | null; estado: 'activa' | 'suspendida'; esAdmin: boolean }`
  - `interface Establecimiento { codigo: string; nombre: string; tipo: string; comuna: string; region: string }`
  - `interface Propuesta { id: string; medicamento: string; establecimiento: string; nombreEstablecimiento: string; texto: string; estado: EstadoPropuesta; creadaEl: string; aFavor: number; enContra: number; esMia: boolean; miVoto: boolean | null }`
  - `interface MiPropuesta { id: string; medicamento: string; establecimiento: string; texto: string; estado: EstadoPropuesta; comentarioAdmin: string | null; creadaEl: string }`
  - `type MotivoError = 'suspendida' | 'sin_hospital' | 'texto' | 'cerrada' | 'propia' | 'sin_sesion' | 'red' | 'otro'`; `class ErrorComunidad extends Error { motivo: MotivoError }`
  - `contarCaracteres(texto: string): number` — puntos de código del texto sin espacios en los extremos (`[...texto.trim()].length`).
- Produces (en `api.ts`):
  - `interface ComunidadApi` con: `sesion(): Promise<{ correo: string } | null>`, `alCambiarSesion(cb: (hay: boolean) => void): () => void`, `enviarEnlace(correo: string): Promise<{ ok: true } | { ok: false; motivo: 'sin_invitacion' | 'limite' | 'red' }>`, `salir(): Promise<void>`, `perfil(): Promise<Persona | null>`, `buscarEstablecimientos(texto: string): Promise<Establecimiento[]>`, `elegirHospital(destino: { codigo: string } | { pais: string }): Promise<void>`, `proponer(medicamento: string, texto: string): Promise<{ id: string }>`, `propuestas(filtro: { medicamento?: string; establecimiento?: string }): Promise<Propuesta[]>`, `votar(propuesta: string, aFavor: boolean, yaVoto: boolean): Promise<void>`, `misPropuestas(): Promise<MiPropuesta[]>`, `retirar(propuesta: string): Promise<void>`.
  - `crearApi(cliente: SupabaseClient): ComunidadApi`.
- Produces (en `cliente.ts`): `crearClienteSupabase(env = import.meta.env): SupabaseClient | null` — `null` si falta cualquiera de las dos variables; con `auth: { flowType: 'pkce', detectSessionInUrl: true, persistSession: true }`.

- [ ] **Step 1: Pruebas** en `api.test.ts` contra el proyecto de pruebas, con usuarios de `escenario.ts` envueltos con `crearApi`:
  - `enviarEnlace` a un correo no invitado → `{ ok: false, motivo: 'sin_invitacion' }`;
  - `perfil()` de una invitada devuelve `{ nombre, establecimiento, paisExtranjero, estado: 'activa', esAdmin: false }`, y `esAdmin: true` para el administrador;
  - `buscarEstablecimientos('sótero')` incluye el código `114101`, devuelve a lo sumo 20 y solo vigentes; con menos de 2 letras devuelve `[]` sin consultar;
  - `elegirHospital({ codigo })` y `elegirHospital({ pais: 'Perú' })` cambian el perfil y el segundo deja `establecimiento: null`;
  - `proponer` crea la propuesta y devuelve su id; cada error del servidor se traduce a su `motivo` (`sin_hospital`, `suspendida`, `texto` con 501 caracteres);
  - `propuestas({ medicamento })` devuelve `aFavor`/`enContra`/`miVoto` correctos tras `votar`; `votar(p, false, true)` cambia un voto existente (`yaVoto = true` usa UPDATE, `false` usa INSERT); votar lo propio → `motivo: 'propia'`; propuesta en bandeja → `'cerrada'`;
  - `misPropuestas()` trae solo las propias, con `comentarioAdmin` tras un rechazo;
  - `retirar` pasa a `retirada`.
  Plus unitarias sin red de `contarCaracteres`: `'a'.repeat(500)` → 500; `'😀'.repeat(500)` → 500 (no 1000); `'  hola \n'` → 4; `''` → 0.
- [ ] **Step 2: Ejecutar** `npm run test:supabase -- api` y `npx vitest run src/comunidad`. Expected: FAIL (módulos inexistentes).
- [ ] **Step 3: Implementar** `tipos.ts`, `cliente.ts` y `api.ts`. La traducción de errores del servidor a `MotivoError` se hace en una sola función con los mensajes exactos de la Etapa 1 («Tu acceso está suspendido», «Las prácticas locales se proponen desde hospitales chilenos», «Elige tu hospital antes de votar», «No puedes votar tu propia propuesta», «La votación de esta propuesta está cerrada», código `23514` → `texto`); un `fetch` fallido → `'red'`.
- [ ] **Step 4: Ejecutar** ambas suites + `npm test` + `npm run lint` + `npm run build`. Expected: todo en verde; `npm run build` sin variables `VITE_*` compila.
- [ ] **Step 5: Commit** — `feat(comunidad): cliente Supabase y capa de API`

### Task 3: Provider, sesión, Entrar y enlaces de pie

**Files:**
- Create: `src/comunidad/ComunidadProvider.tsx`, `src/comunidad/fake.ts`, `src/comunidad/paginas/Entrar.tsx`, `src/comunidad/ComunidadProvider.test.tsx`, `src/comunidad/paginas/Entrar.test.tsx`
- Modify: `src/app/App.tsx`, `src/index.css`

**Interfaces:**
- Consumes: `ComunidadApi`, tipos, `crearClienteSupabase`, `crearApi` (Task 2).
- Produces:
  - `useComunidad(): { disponible: boolean; cargando: boolean; sesion: { correo: string } | null; perfil: Persona | null; api: ComunidadApi; recargarPerfil(): Promise<void> }`
  - `<ComunidadProvider api?: ComunidadApi>` — sin `api`, crea la real si `crearClienteSupabase()` no es `null`; con `disponible = false` el resto de la app no cambia.
  - `crearApiFalsa(inicial?: { sesion?: boolean; perfil?: Partial<Persona>; propuestas?: Propuesta[] }): ComunidadApi & { llamadas: Record<string, unknown[][]> }` — guarda en memoria; permite forzar errores con `fallarCon(metodo, motivo)`.
  - Rutas: `/comunidad/entrar`, `/comunidad`, `/comunidad/hospital`, `/comunidad/mis-propuestas`, `/privacidad`.

- [ ] **Step 1: Pruebas** (con `crearApiFalsa`):
  - sin `disponible` (provider sin API y sin variables), `App` no muestra ningún enlace «Comunidad» ni «Entrar» (las 241 pruebas existentes cubren el resto);
  - con API y sin sesión: el pie muestra «Entrar a la comunidad» → `/comunidad/entrar`; con sesión muestra «Comunidad» y «Mis propuestas» y un botón «Salir»;
  - **Entrar:** escribir un correo y enviar llama a `api.enviarEnlace` y muestra «Te enviamos un enlace a <correo>. Ábrelo en este dispositivo»; con `sin_invitacion` muestra, en `role="alert"`, «Este correo no tiene invitación»; con `limite` «Pediste muchos enlaces seguidos; espera unos minutos»; con `red` «Sin conexión; intenta más tarde»; el botón queda deshabilitado mientras envía y hay un «Reenviar enlace» que aparece tras el primer envío;
  - un correo vacío o sin `@` no llama a la API;
  - **Review Focus 1:** con una URL que trae `?code=abc#/comunidad/entrar` y una API que ya tiene sesión, tras montar la app se navega a `/comunidad` y `window.location.search` queda vacío.
  - **Review Focus 5:** con `perfil.estado = 'suspendida'`, `/comunidad` muestra «Tu acceso está suspendido» y ninguna acción; con perfil sin hospital ni país, redirige a `/comunidad/hospital`.
- [ ] **Step 2: Ejecutar** `npx vitest run src/comunidad` → FAIL.
- [ ] **Step 3: Implementar** provider, hook, pantalla `Entrar`, rutas y enlaces de pie. El pie añade los enlaces solo si `disponible`. El flujo de retorno usa `api.alCambiarSesion` y `useNavigate`; la limpieza del `?code=` la hace supabase-js (`detectSessionInUrl`), el provider solo reemplaza la URL con `history.replaceState` cuando aparece la sesión.
- [ ] **Step 4: Ejecutar** `npm test` (todas) + lint + build → verde. **Commit** — `feat(comunidad): sesión y pantalla de entrada`

### Task 4: Elegir hospital

**Files:**
- Create: `src/comunidad/paginas/ElegirHospital.tsx`, `src/comunidad/paginas/ElegirHospital.test.tsx`

**Interfaces:**
- Consumes: `useComunidad`, `api.buscarEstablecimientos`, `api.elegirHospital`.

- [ ] **Step 1: Pruebas:** escribir «sótero» en el buscador llama a `buscarEstablecimientos` (con una espera de 300 ms entre pulsaciones: varias teclas seguidas hacen **una** llamada) y lista nombre, comuna y región; elegir uno llama a `elegirHospital({ codigo })`, recarga el perfil y navega a `/comunidad`; la opción «Trabajo fuera de Chile» muestra un campo de país obligatorio y llama a `elegirHospital({ pais })`; un país vacío o de solo espacios no envía; sin resultados muestra «No encontramos ese hospital. Prueba con otra parte del nombre»; un fallo de red muestra «Sin conexión; intenta más tarde» y deja lo escrito.
- [ ] **Step 2: Ejecutar → FAIL. Step 3: Implementar** la pantalla. **Step 4:** `npm test` → verde. **Step 5: Commit** — `feat(comunidad): elegir hospital`

### Task 5: Proponer una práctica local

**Files:**
- Create: `src/comunidad/paginas/Proponer.tsx`, `src/comunidad/paginas/Proponer.test.tsx`
- Modify: `src/app/paginas/Ficha.tsx` (botón), `src/app/App.tsx` (ruta `/m/:id/proponer`)

**Interfaces:**
- Consumes: `useComunidad`, `api.proponer`, `contarCaracteres`, `obtenerFicha`.

- [ ] **Step 1: Pruebas:**
  - en la ficha, con sesión, perfil activo y hospital chileno aparece el enlace «Proponer práctica local»; **no** aparece sin sesión, sin `disponible`, con perfil suspendido, ni con país extranjero (en ese caso se ve el texto «Las prácticas locales se proponen desde hospitales chilenos; puedes votar» en lugar del botón);
  - el formulario muestra el contador «N / 500»; **Review Focus 2:** 500 caracteres exactos, y 500 emojis, habilitan «Enviar»; 501 lo deshabilita y marca el contador en rojo; un texto de solo espacios lo deshabilita;
  - enviar llama `api.proponer(medicamento, texto)` y muestra «Gracias. Tu propuesta quedó en votación entre tus colegas»; el texto se limpia solo en éxito;
  - **Review Focus 3:** si la API falla con `red`, `suspendida` o `sin_sesion`, se muestra el mensaje correspondiente en `role="alert"` y el texto escrito permanece;
  - el hospital que se muestra («Se publicará como práctica de: <nombre>») es el del perfil.
- [ ] **Step 2: Ejecutar → FAIL. Step 3: Implementar.** El nombre del hospital del perfil se obtiene con `buscarEstablecimientos` por código exacto o guardándolo en `Persona` (decisión del implementador: lo más simple que no agregue una consulta por render; registrar en el ledger). **Step 4:** `npm test` → verde. **Step 5: Commit** — `feat(comunidad): proponer prácticas locales`

### Task 6: Comunidad (votar) y Mis propuestas

**Files:**
- Create: `src/comunidad/paginas/Comunidad.tsx`, `src/comunidad/paginas/MisPropuestas.tsx`, y sus `.test.tsx`

**Interfaces:**
- Consumes: `api.propuestas`, `api.votar`, `api.misPropuestas`, `api.retirar`, `obtenerFicha`, `medicamentos`.

- [ ] **Step 1: Pruebas — Comunidad:** lista las propuestas con medicamento (nombre de la ficha), hospital, texto, conteo «N a favor · M en contra» y botones «De acuerdo» / «No de acuerdo»; el voto vigente aparece con `aria-pressed="true"`; filtros por medicamento y por hospital llaman a `api.propuestas` con el filtro; los botones de propuestas propias no aparecen (se muestra «Es tuya»); **Review Focus 4:** dos clics seguidos en «De acuerdo» llaman a `votar` **una** vez y el botón está deshabilitado mientras dura; cambiar de «De acuerdo» a «No de acuerdo» llama `votar(id, false, true)`; un error `cerrada` muestra «La votación de esta propuesta ya se cerró» y recarga la lista; un error `red` conserva la lista y avisa; lista vacía → «Todavía no hay propuestas en votación».
- [ ] **Step 2: Pruebas — Mis propuestas:** muestra cada una con su estado en palabras («En votación», «En revisión del autor», «Aprobada», «Rechazada», «Retirada»), el comentario de Héctor si fue rechazada, y «Retirar» solo mientras está en votación (pide confirmación; tras retirar pasa a «Retirada»).
- [ ] **Step 3: Ejecutar → FAIL. Step 4: Implementar. Step 5:** `npm test` → verde. **Step 6: Commit** — `feat(comunidad): votar y mis propuestas`

### Task 7: Página de privacidad

**Files:**
- Create: `src/comunidad/paginas/Privacidad.tsx`, `src/comunidad/paginas/Privacidad.test.tsx`
- Modify: `src/app/paginas/Acerca.tsx`, `src/comunidad/paginas/Entrar.tsx`

- [ ] **Step 1: Pruebas:** `/privacidad` existe y responde aunque la comunidad no esté disponible; dice qué se guarda (correo, nombre, profesión y hospital de las invitadas), para qué, que el público no deja datos, que solo el autor ve quién propuso y votó, que se registra una bitácora de acciones, que el contador de visitas es anónimo y cómo pedir la eliminación (escribir a hectorsalvo32@gmail.com); «Acerca de» y «Entrar» enlazan a ella.
- [ ] **Step 2: Ejecutar → FAIL. Step 3: Implementar** (texto de la spec §8, sin promesas que el sistema no cumple). **Step 4:** `npm test` → verde. **Step 5: Commit** — `docs(comunidad): página de privacidad`

### Task 8: Script para invitar personas

**Files:**
- Create: `scripts/supabase/invitar.py`, `scripts/supabase/test_invitar.py`

**Interfaces:**
- Produces: `invitar(url: str, clave: str, correo: str, nombre: str, profesion: str, http=…) -> str` (id de la persona; idempotente: si el correo ya existe actualiza nombre y profesión y no duplica; nunca cambia el estado ni el hospital); `normalizar_correo(correo: str) -> str` (minúsculas y sin espacios; error si no tiene `@`). CLI: `python3 scripts/supabase/invitar.py --destino prueba|real --correo X --nombre "Y" --profesion "Z"`.

- [ ] **Step 1: Pruebas (pytest, sin red):** crea al usuario de Auth con `email_confirm: true` y sin contraseña y la fila de `personas`; invitar dos veces el mismo correo no duplica; un correo inválido falla antes de llamar a la red; normaliza `' Ana@Correo.CL '` → `'ana@correo.cl'`; no envía ningún correo (el enlace lo pide la propia persona en la app).
- [ ] **Step 2: Ejecutar** `python3 -m pytest scripts/supabase -q` → FAIL. **Step 3: Implementar** reutilizando el cliente HTTP de `cargar_catalogos.py` (User-Agent neutro). **Step 4:** pytest → verde. **Step 5: Commit** — `feat(supabase): script para invitar personas`

### Task 9: Publicación y prueba de punta a punta

**Files:**
- Modify: `.github/workflows/publicar.yml`, `docs/supabase.md`, `.gitignore` (ya cubre `*.local`)

- [ ] **Step 1: Variables de compilación:** definir como *variables* de GitHub (no secretos; la clave pública es pública por diseño) `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY` del proyecto **real**, y pasarlas solo al paso `npm run build` del job `construir`. Verificar con `gh variable list`.
- [ ] **Step 2: Prueba local contra el proyecto de pruebas:** crear `.env.local` (ignorado por git) con las variables del proyecto de **pruebas**, `npm run dev`, y recorrer con el navegador automatizado: entrar con el correo de Héctor (invitado a pruebas con `invitar.py`), elegir un hospital, proponer, votar con una segunda cuenta, ver el estado en «Mis propuestas». Capturas de las 5 pantallas en tema claro y oscuro, en ancho móvil.
- [ ] **Step 3: Compilar sin variables** (`npm run build` con el entorno limpio) y verificar con el navegador automatizado que la portada y una ficha no muestran nada de comunidad.
- [ ] **Step 4: Documentar** en `docs/supabase.md`: cómo invitar a alguien (`invitar.py`), cómo probar localmente y qué ve la persona al recibir el enlace.
- [ ] **Step 5: Commit** — `ci(comunidad): variables de Supabase en la compilación y guía de uso`. **No** se mezcla con `main` ni se publica sin la confirmación de Héctor.
