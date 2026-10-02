# Comunidad de prácticas locales — Documento de diseño

**Fecha:** 2026-10-02
**Autor:** Héctor Salvo Agüero (TENS, Ingeniero en Informática)
**Estado:** borrador para revisión
**Depende de:** Dilución EV v0.2 (`2026-10-01-dilucion-ev-design.md`)

## 1. Propósito

Permitir que profesionales invitados registren **cómo se hace en la práctica, en su hospital**,
algo que la app muestra desde las fuentes (por ejemplo: «en el Hospital X la ceftriaxona se diluye en
100 ml de SF y se pasa en 30 min»). Las colegas del mismo hospital votan, y cuando hay consenso la
propuesta llega a Héctor, que es **el único que puede publicarla**.

**Principios que no se negocian:**

1. **Nada se publica sin la aprobación de Héctor.** El consenso solo lleva una propuesta a su bandeja.
2. **Las notas nunca cambian los datos clínicos ni las calculadoras.** Son texto aparte, rotulado
   «Práctica local», y la app sigue mostrando los datos con fuente citada como hasta ahora.
3. **La app pública sigue funcionando igual sin este sistema**: sin cuenta, sin internet o con el
   servidor caído.
4. **Todo queda registrado** en una bitácora privada que solo ve Héctor y que nadie puede borrar.

**Criterios de éxito:**

1. Una invitada entra con su correo, propone una nota y vota en menos de un minuto.
2. Ninguna persona distinta de Héctor puede publicar, aunque modifique la app en su teléfono:
   los permisos los hace cumplir la base de datos.
3. Una nota aprobada aparece en la ficha de todos los usuarios, también sin internet (última copia).
4. Ante un mal uso (votos coordinados, notas falsas, cambiarse de hospital para votar), la bitácora
   muestra quién hizo qué y cuándo.

## 2. Alcance

### 2.1 Incluido

- Invitación a mano por Héctor; acceso por enlace mágico al correo (sin contraseña).
- Cada invitada declara su hospital, elegido desde el catálogo oficial del DEIS, o indica que trabaja
  fuera de Chile (con su país): en ese caso puede votar pero no proponer.
- Propuestas de texto libre (máximo 500 caracteres) asociadas a un medicamento y un hospital.
- Votación *De acuerdo / No de acuerdo*, con umbral configurable.
- Bandeja de Héctor: aprobar, rechazar con comentario, editar antes de aprobar, retirar notas
  publicadas.
- Gestión de personas: invitar, suspender, reactivar; historial de hospitales.
- Bitácora privada inmutable.
- Recuadro público «Prácticas locales» en cada ficha, con copia para uso sin internet.

### 2.2 Fuera de alcance (esta versión)

- Cambios estructurados a datos (volúmenes, concentraciones, velocidades) por hospital.
- Registro abierto o verificación de profesionales en la Superintendencia de Salud.
- Filtro «Mi hospital» para el público (todos ven todas las notas aprobadas).
- Comentarios o conversación dentro de una propuesta.
- Notificaciones por correo o push (Héctor revisa la bandeja cuando entra).
- Más de un administrador.

## 3. Decisiones tomadas (con Héctor, 2-oct-2026)

| Tema | Decisión |
|---|---|
| Quién participa | Solo personas que Héctor invita a mano |
| Qué se propone | Nota de texto libre por medicamento y hospital; nunca cambia datos ni cálculos |
| Consenso | Umbral fijo y configurable: **3 votos a favor de personas de ese mismo hospital** y más votos a favor que en contra |
| Hospital de cada invitada | Lo elige ella al entrar; los cambios quedan en el historial |
| Invitadas que trabajan fuera de Chile | Eligen «Trabajo fuera de Chile» y su país; **votan pero no proponen**. Su voto no cuenta para el umbral del mismo hospital, sí para el total a favor/en contra |
| Lista de hospitales | Catálogo oficial de establecimientos del DEIS (MINSAL) |
| Quién ve las notas | Todos los usuarios, sin cuenta, todas las notas aprobadas |
| Autoría en público | No se muestra el nombre; solo hospital, fecha de aprobación y votos a favor |
| Registro de autoría | Bitácora privada, inmutable, solo para Héctor |
| Arquitectura | Supabase; la app pública lee las notas aprobadas en vivo y guarda una copia local |

## 4. Arquitectura

```
App pública (GitHub Pages, igual que hoy)
 ├─ datos clínicos YAML (sin cambios, sin servidor)
 ├─ recuadro «Prácticas locales» ──lee──► Supabase: vista notas_publicadas (solo lectura, sin cuenta)
 │                                   └─ copia en localStorage para uso sin internet
 ├─ /comunidad (invitadas con sesión) ──► Supabase: propuestas, votos (con permisos por fila)
 └─ /admin (solo Héctor)            ──► Supabase: bandeja, personas, bitácora, ajustes
                                          └─ función de servidor «invitar» (clave de servicio)
```

- **Supabase** aporta la base de datos PostgreSQL, las cuentas (Auth con enlace mágico) y los
  permisos por fila (RLS). Plan gratuito al inicio.
- La app usa `@supabase/supabase-js` con la clave pública (anon). La clave de servicio **nunca**
  llega al navegador: solo la usa la función de servidor `invitar`.
- La URL y la clave pública van en variables de entorno de compilación (`VITE_SUPABASE_URL`,
  `VITE_SUPABASE_ANON_KEY`), guardadas como secretos de GitHub Actions.
- Si esas variables no existen, la app compila y funciona como hoy, sin el recuadro ni la comunidad.
- El registro público de cuentas queda **desactivado** en Supabase: solo entra quien fue invitado.

## 5. Datos

### 5.1 Tablas

**`establecimientos`** — catálogo DEIS. `codigo` (PK, código DEIS), `nombre`, `tipo`, `comuna`,
`region`, `vigente`. Se carga y actualiza con un script desde el archivo oficial; nadie lo edita a mano.

**`medicamentos`** — `id` de cada ficha publicada (p. ej. `ceftriaxona`). La carga el mismo script
que el catálogo DEIS, leyendo `datos/medicamentos/*.yaml`; se vuelve a cargar cuando se agregan fichas.

**`personas`** — una fila por invitada, ligada a su cuenta de Auth. `id` (= `auth.users.id`),
`correo`, `nombre`, `profesion` (texto que escribe Héctor al invitar), `establecimiento` (FK, nulo
hasta que lo elige o si trabaja fuera de Chile), `pais_extranjero` (texto, nulo salvo que trabaje fuera
de Chile; es excluyente con `establecimiento`), `estado` (`activa` | `suspendida`), `invitada_el`.

**`administradores`** — `persona` (FK). Contiene solo a Héctor. La función `es_admin()` consulta
esta tabla y todas las reglas de administración dependen de ella.

**`historial_hospital`** — `persona`, `desde` y `hacia` (código DEIS o «extranjero: país»; `desde`
nulo la primera vez), `fecha`. Se llena solo, mediante un disparador, cada vez que cambia
`personas.establecimiento` o `personas.pais_extranjero`.

**`propuestas`** — `id`, `medicamento` (FK a `medicamentos`), `establecimiento` (FK), `texto` (1–500 caracteres), `autora` (FK),
`creada_el`, `estado` (`en_votacion` | `en_bandeja` | `aprobada` | `rechazada` | `retirada`),
`texto_publicado` (el texto final, por si Héctor lo editó), `comentario_admin`, `resuelta_el`.

**`votos`** — `propuesta`, `persona`, `a_favor` (booleano), `establecimiento_al_votar` (copia del
hospital de la persona en ese momento; nulo si trabaja fuera de Chile), `pais_al_votar` (copia del
país si trabaja fuera de Chile), `fecha`. Clave única (`propuesta`, `persona`).

**`ajustes`** — una sola fila: `umbral_votos` (por defecto 3).

**`bitacora`** — `id`, `fecha`, `actor` (persona), `accion` (texto corto: `propuso`, `voto`,
`cambio_voto`, `cambio_hospital`, `aprobo`, `edito_y_aprobo`, `rechazo`, `retiro`, `invito`,
`suspendio`, `reactivo`, `cambio_umbral`), `objeto` (id afectado), `detalle` (JSON con antes y
después). **Solo se insertan filas**: no hay permiso de UPDATE ni DELETE para nadie, ni siquiera
para el administrador desde la app.

**Vista `notas_publicadas`** — propuestas `aprobada`: `id`, `medicamento`, nombre del
establecimiento, `texto_publicado`, `resuelta_el` y cantidad de votos a favor. **No incluye la autora.**

### 5.2 Reglas del consenso

- El voto de una persona cuenta para el umbral solo si su `establecimiento_al_votar` es el mismo
  de la propuesta. Así, cambiarse de hospital después de votar no altera votos anteriores, y
  cambiarse para votar queda visible en el historial.
- Al insertar o cambiar un voto, un disparador recalcula: si una propuesta `en_votacion` tiene
  `a_favor` del mismo hospital ≥ `umbral_votos` **y** total a favor > total en contra, pasa a
  `en_bandeja`.
- Una propuesta en bandeja **no vuelve atrás** aunque cambien los votos; Héctor ve el conteo actual.
- Los votos de quien trabaja fuera de Chile cuentan en el total a favor/en contra, pero nunca para
  el umbral del mismo hospital.
- Solo quien tiene un hospital chileno puede proponer (para su propio hospital).
- Nadie vota su propia propuesta. Una persona suspendida no propone ni vota (sus votos previos se
  conservan y Héctor los ve marcados).
- Mientras está `en_votacion`, la autora puede retirarla; no puede editarla.
- Cambiar el umbral afecta las votaciones siguientes; no mueve propuestas ya evaluadas.

### 5.3 Permisos (RLS)

| Quién | Puede |
|---|---|
| Público (sin sesión) | Leer `notas_publicadas`. Nada más |
| Invitada activa | Leer y editar su propia fila de `personas` (solo `establecimiento`); leer `establecimientos`; leer propuestas `en_votacion` y `en_bandeja` y sus conteos; leer sus propias propuestas en cualquier estado; crear propuestas (solo con hospital chileno); votar y cambiar su voto mientras la propuesta esté `en_votacion`; retirar una propuesta propia `en_votacion` |
| Invitada suspendida | Leer `notas_publicadas` como el público |
| Administrador (Héctor) | Todo lo anterior, más: leer todo (incluida la autoría y quién votó qué); aprobar, editar y aprobar, rechazar, retirar notas publicadas; suspender y reactivar; cambiar el umbral; leer la bitácora |
| Nadie | Modificar o borrar la `bitacora`; cambiar el `estado` de una propuesta salvo por las funciones descritas |

Los cambios de estado de Héctor se hacen con funciones SQL (`aprobar`, `rechazar`, `retirar_nota`,
`suspender`, `reactivar`, `cambiar_umbral`) que verifican `es_admin()` y escriben la bitácora en la
misma transacción.

## 6. Pantallas

### 6.1 Público (sin cuenta)

- **Ficha → recuadro «Prácticas locales»**, debajo de los datos con fuente, solo si hay notas:
  - aviso fijo: «Práctica informada por profesionales de cada hospital y revisada por el autor.
    No reemplaza el protocolo local.»;
  - cada nota: «**Hospital X** · aprobada el 12-oct-2026 · 5 votos a favor» y el texto.
- Las notas se piden al abrir la app (una consulta para todas) y se guardan en `localStorage`
  con su fecha. Sin internet se muestra la copia y «actualizado el …». Si nunca hubo copia, el
  recuadro no aparece.

### 6.2 Invitadas

- **Entrar** (`/comunidad/entrar`): correo → enlace mágico. Si el correo no está invitado,
  Supabase no envía enlace y la app dice «Este correo no tiene invitación».
- **Elegir hospital** (primera vez, y luego desde «Mi perfil»): buscador sobre el catálogo DEIS, o
  la opción «Trabajo fuera de Chile» con el país.
- **Proponer**: botón «Proponer práctica local» en cada ficha (solo con sesión); texto ≤ 500
  caracteres; el hospital es el de su perfil. Para quien trabaja fuera de Chile el botón aparece
  desactivado: «Las prácticas locales se proponen desde hospitales chilenos; puedes votar».
- **Comunidad** (`/comunidad`): propuestas en votación, filtrables por hospital y medicamento;
  botones *De acuerdo / No de acuerdo*; se ve el conteo, no quién votó.
- **Mis propuestas**: estado de cada una y el comentario de Héctor si fue rechazada.

### 6.3 Héctor (administrador)

- **Bandeja** (`/admin`): primero las propuestas que alcanzaron el umbral; luego, en otra lista,
  todas las que siguen en votación. Cada una muestra autora, texto, votos con nombre y hospital (o país, si votó desde fuera de Chile).
  Acciones: **Aprobar**, **Editar y aprobar**, **Rechazar con comentario**.
- **Notas publicadas**: listado con **Retirar** (pide motivo).
- **Personas**: invitar (correo, nombre, profesión), suspender o reactivar, historial de hospitales.
- **Registro**: bitácora con búsqueda por persona, medicamento y fecha.
- **Ajustes**: umbral de votos.

Los enlaces a «Comunidad» y «Admin» aparecen en el pie de página solo con sesión iniciada.

## 7. Manejo de errores

| Situación | Comportamiento |
|---|---|
| Sin internet o Supabase caído | La app funciona; notas desde la copia; Comunidad y Admin muestran «sin conexión, intenta más tarde» |
| Proyecto Supabase pausado (plan gratis tras 7 días sin uso) | Igual que caído; Héctor lo reactiva desde el panel de Supabase |
| Enlace mágico vencido o no llega | Botón «Reenviar enlace» (respeta el límite de envíos de Supabase) |
| Suspendida intenta votar | El servidor lo rechaza; la app avisa «Tu acceso está suspendido» |
| Voto duplicado o simultáneo | La clave única lo impide; la app muestra el voto vigente |
| Texto vacío o > 500 caracteres | Lo bloquea la app y también la base de datos |
| Medicamento inexistente en la propuesta | La base de datos lo rechaza (FK a `medicamentos`) |
| Variables de Supabase ausentes en la compilación | La app compila sin comunidad ni recuadro (modo actual) |

## 8. Privacidad y aviso

- Se guarda solo lo necesario: correo, nombre, profesión y hospital de las invitadas.
- Página «Privacidad» enlazada desde «Acerca de» y desde «Entrar»: qué se guarda, para qué,
  quién lo ve (solo Héctor la autoría), cómo pedir la eliminación de la cuenta.
- El público no deja datos: leer notas no requiere cuenta. El contador GoatCounter sigue igual.
- Eliminación a pedido: Héctor desactiva la cuenta y anonimiza nombre y correo; la bitácora
  conserva las acciones con el id, sin datos personales.

## 9. Pruebas

1. **Permisos (las más importantes):** pruebas automáticas contra un proyecto Supabase de prueba
   separado del real, con usuarios sembrados (público, invitada A y B del mismo hospital, invitada
   C de otro hospital, D que trabaja fuera de Chile, suspendida, administrador). Casos mínimos:
   - el público no lee propuestas, votos, personas ni bitácora;
   - una invitada no aprueba, no lee la autoría ajena ni la bitácora;
   - nadie vota dos veces ni su propia propuesta; una suspendida no vota;
   - el voto de otro hospital o de fuera de Chile no cuenta para el umbral, pero sí en el total;
   - quien trabaja fuera de Chile no puede proponer;
   - la bitácora no se puede modificar ni borrar, tampoco como administrador;
   - el umbral mueve la propuesta a bandeja exactamente al cumplirse.
2. **Pantallas:** pruebas con Vitest y Testing Library usando un cliente Supabase simulado.
3. **Sin Supabase:** la app compila y las 241 pruebas actuales siguen pasando sin variables.
4. Las pruebas de permisos corren en GitHub Actions con las claves del proyecto de prueba como
   secretos; si fallan, no se publica.

## 10. Etapas

Cada etapa se publica y prueba por separado.

1. **Etapa 1 — Servidor.** Proyecto Supabase (real y de prueba), tablas, disparadores, funciones,
   RLS y bitácora; carga del catálogo DEIS (la etapa empieza confirmando la URL vigente del listado
   oficial de establecimientos); pruebas de permisos. Sin cambios visibles en la app.
2. **Etapa 2 — Invitadas.** Entrar con enlace mágico, elegir hospital, proponer, Comunidad, votar,
   Mis propuestas; función `invitar`; página de privacidad.
3. **Etapa 3 — Administración.** Bandeja, Notas publicadas, Personas, Registro, Ajustes.
4. **Etapa 4 — Público.** Recuadro «Prácticas locales» en la ficha, con copia para uso sin internet.

## 11. Costos y límites

- Supabase gratis: 50.000 usuarios activos al mes y 500 MB de base de datos, sobra para el grupo
  de invitadas. Pausa tras 7 días sin actividad; plan Pro ≈ USD 25/mes si se vuelve habitual.
- Correos de acceso: el servicio incluido tiene un límite bajo por hora; si se invita a muchas
  personas a la vez se conecta un proveedor SMTP (Resend, ya usado en el SPQ).
- Dos proyectos Supabase (real y de prueba) caben en el plan gratuito.
