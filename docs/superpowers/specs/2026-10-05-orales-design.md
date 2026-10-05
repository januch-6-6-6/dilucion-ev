# Medicamentos orales (APS) — Documento de diseño

**Fecha:** 2026-10-05
**Autor:** Héctor Salvo Agüero (TENS, Ingeniero en Informática)
**Estado:** borrador para revisión
**Depende de:** Dilución EV v0.2 (`2026-10-01-dilucion-ev-design.md`)
**Insumo clínico:** `informes/orales-discrepancias-cima-pediamecum.md` (80 fármacos, análisis CIMA vs Pediamécum)

## 1. Propósito

Sumar a Dilución EV una sección **«Orales»** con los 80 medicamentos orales más usados del arsenal de
atención primaria (base: Arsenal Farmacoterapéutico Básico APS del Servicio de Salud Atacama, Res. CP16.328,
12-ago-2026), con dosis, presentaciones y una **calculadora por peso con conversión a la forma real**
(ml de jarabe, gotas, comprimidos).

**Propósito acordado (heredado del EV):** portafolio y formación. **No es una herramienta de prescripción**;
el aviso de formación está siempre visible. Su uso en terreno dependería de que lo valide después un
químico farmacéutico.

**Principios que no se negocian:**

1. **Cada dato cita su fuente.** Donde dos fuentes difieren, se muestran ambas y se calcula con la más
   conservadora (más baja).
2. **Una sola fuente se avisa.** Los 16 fármacos con una única fuente se publican **con un aviso visible
   en la ficha** (decisión de Héctor, 5-oct-2026).
3. **Lo que ninguna fuente respalda no se calcula.** Sin dosis pediátrica en los fármacos donde la ficha
   la desaconseja o hay alerta de seguridad.
4. **La calculadora nunca copia un «ml» de una ficha.** Convierte siempre por la concentración de la
   presentación elegida.
5. **El módulo EV no cambia.** Orales es un módulo aparte que reutiliza la interfaz.

**Criterios de éxito:**

1. Un usuario encuentra un oral por nombre genérico o comercial y ve su ficha en menos de tres toques.
2. Para un niño de peso X y un jarabe de concentración Y, la calculadora entrega la dosis por toma en mg y
   en ml, respeta los topes y avisa cuando los alcanza.
3. Las 16 fichas de fuente única muestran el aviso; ninguna ficha `solo_adulto` ofrece calculadora pediátrica.
4. `npm test` y `npm run validar` fallan si una ficha viola una regla de coherencia (sección 8).
5. Las 89 fichas EV y sus pruebas siguen pasando sin cambios.

## 2. Alcance

**Dentro de v1:** 80 fichas orales; rutas `/orales`; calculadora por peso con conversión líquida;
avisos; tabla de discrepancias por ficha; favoritos y recientes propios; estado de registro en Chile.

**Fuera de v1** (no se investigó o se decidió dejar para después):
- Ajuste renal o hepático calculado (queda como texto informativo).
- Dosis por superficie corporal (los fármacos que la usan muestran la pauta como texto).
- Interacciones, efectos adversos y contraindicaciones detalladas.
- Búsqueda unificada EV + oral (son dos buscadores).
- Inyectables, tópicos, inhalados y vacunas del arsenal.
- Neonatos (igual que el EV).
- Sección «Comunidad / Prácticas locales» para orales.

## 3. Decisiones de diseño

| # | Decisión | Quién / cuándo |
|---|---|---|
| 1 | Esquema propio `FichaOral` dentro de la misma app y el mismo repo (enfoque A) | Héctor, 5-oct |
| 2 | v1 con calculadora por peso + conversión líquida; sin ajuste renal/hepático | Héctor, 5-oct |
| 3 | Fármacos de fuente única se publican con aviso visible | Héctor, 5-oct |
| 4 | Sin dosis pediátrica para domperidona, venlafaxina y ácido acetilsalicílico | Supuesto presentado y aceptado en el diseño |
| 5 | Ante topes distintos, se muestra y calcula el más bajo | Supuesto presentado y aceptado (aplica a paracetamol y metamizol adulto) |
| 6 | Registro en Chile solo como «presentación registrada»; parte en `sin_verificar` | Supuesto presentado y aceptado |
| 7 | Rama `orales-v1` desde `main`, independiente de `comunidad-etapa-1` | Propuesta aceptada |
| 8 | 80 fichas cargadas en 3 tandas con una sola revisión al final; `meta.revisadoPor` vacío | Heredado del EV |

## 4. Modelo de datos: `FichaOral`

Archivo nuevo `src/esquema/ficha-oral.ts` (zod, `strictObject`, como `ficha.ts`). Los YAML viven en
`datos/orales/<id>.yaml`.

```
FichaOral
  id                  slug (único dentro de orales)
  nombre, comerciales[], grupo, ambitos[] (hoy ['aps'])
  altoRiesgo          boolean (opioides, benzodiacepinas, etc.)
  presentaciones[]
    id, forma         comprimido | capsula | jarabe | suspension | gotas | sobre | comprimido_efervescente
    cantidad          { valor, unidad }           // por unidad (comprimido, cápsula, sobre)
    concentracion?    { valor, unidad, porMl }    // líquidos: mg por ml
    gotasPorMl?       number                      // obligatorio si forma = gotas
    partible          no | mitades | cuartos
    liberacionProlongada  boolean
    elemental?        { valor, unidad, de }       // p. ej. 80 mg de hierro elemental
    registroChile     verificado | sin_verificar | no_registrado
    fuente
  dosis[]
    indicacion, poblacion (adulto | pediatrico)
    regimen           fija | por_peso | por_edad | por_superficie
    min?, max?, unidad, intervaloH?, tomasPorDia?
    topePorToma?, topeDiario?
    estatus           autorizada | off_label
    fuente
  pediatria           { estado: con_dosis | solo_adulto, motivo? }
  verificacion        dos_fuentes | fuente_unica
  discrepancias[]     { campo, valores[{fuente, valor}], mostrado, motivo }
  administracion      { comida: ayunas | con_comida | indiferente | antes | despues, texto, noTriturar?, fuente }
  ajusteRenalHepatico { renal?: texto, hepatico?: texto, fuente }   // informativo
  alertas[]
  meta                { revisadoPor?, fechaRevision? }
```

`verificacion` **se calcula** al cargar (menos de dos fuentes distintas ⇒ `fuente_unica`) en lugar de
declararse a mano, para que nadie pueda olvidar el aviso.

## 5. Calculadora: `src/calculos/oral.ts`

Funciones puras con pruebas; reutiliza `redondeo.ts` y `numeros.ts`.

**Por peso (pediátrica).** Entradas: peso, fármaco, indicación y presentación.
1. Falta peso, indicación o presentación (o concentración en líquidos) ⇒ no calcula y dice qué falta.
2. Dosis por toma = mg/kg × peso, limitada por `topePorToma` y por `topeDiario / tomas`; nunca supera el
   tope de adulto de la ficha. Si se alcanza un tope, **el resultado lo dice**.
3. Si dos fuentes difieren, usa la más baja y muestra el rango de la otra.
4. Convierte a la forma real: **ml** (líquidos), **gotas** (con `gotasPorMl`), **comprimidos o fracción**.

**Ida y vuelta líquida.** mg → ml y ml → mg, siempre por concentración.

**Dosis fija de adulto.** Número de unidades por toma y por día; verifica `topeDiario`.

**Fracciones imposibles.** Si la dosis exige una fracción que la presentación no permite (`partible: no`,
liberación prolongada), no la ofrece y propone una presentación líquida o declara que no hay forma de darla.

**Pediatría `solo_adulto`.** Calculadora pediátrica desactivada, con el motivo a la vista.

## 6. Interfaz

- **Cabecera:** dos pestañas, «EV» (sin cambios) y «Orales».
- **Rutas:** `/orales` (lista con buscador, grupos, favoritos y recientes), `/orales/m/:id` (ficha),
  `/orales/m/:id/calcular` (calculadora).
- **Ficha oral**, de arriba abajo: aviso de formación → **aviso de fuente única** (cuando aplica) → dosis
  adulto y pediátrica (marca *autorizada*/*off-label*; motivo si es `solo_adulto`) → presentaciones (partible,
  liberación prolongada, registro en Chile) → administración y alertas → **tabla de discrepancias**.
- **Colores:** colores por grupo en `colores.ts`; el rojo sigue reservado a alertas y alto riesgo.
- **Favoritos y recientes:** los ids de orales y EV **se repiten** (ketorolaco, ondansetrón, metoclopramida,
  haloperidol, diazepam, fenitoína…). Los orales se guardan con prefijo (`oral:<id>`); los datos EV existentes
  no se migran.
- **Reutiliza:** aviso inicial, tema oscuro, contador de visitas (la ruta se registra sola) y precache offline
  de la PWA.

## 7. Generación de datos

Scripts Python `scripts/fichas/orales/*.py` escriben `datos/orales/*.yaml` desde el informe y los textos en
`datos/crudos/orales/` (que no se versionan por tamaño; el script de extracción sí). Tres tandas:

1. Analgésicos, antiinflamatorios, antihistamínicos, corticoides y antiinfecciosos.
2. Cardiovascular, digestivo y endocrino.
3. Neurología, psiquiatría, anticoncepción, vitaminas y hierro.

Una revisión única de las discrepancias al final. Las fuentes se registran en `datos/fuentes.yaml` **a nivel de
producto** (CIMA con nº de registro, Pediamécum por ficha, DailyMed/EMC para flucloxacilina, glibenclamida e
hidroclorotiazida, guías MINSAL para DM2, depresión e hipotiroidismo).

**Registro en Chile:** todo parte en `sin_verificar`. Un script aparte lo sube a `verificado` con los JSON del
ISP (hoy 30 de 80; el sitio bloquea la IP tras muchas consultas: reintentar con un solo proceso y pausas largas).

**Correcciones del informe que entran como datos:** morfina en gotas (10 mg/ml en CIMA vs 20 mg/ml en el
arsenal chileno: la concentración es siempre dato obligatorio); lactulosa 10 g ≈ 15 ml (no 20); quetiapina y
venlafaxina de liberación inmediata; hierro en mg de hierro elemental.

## 8. Validación

`npm run validar` y pruebas, además del esquema:

- Presentación líquida ⇒ `concentracion` obligatoria; forma `gotas` ⇒ `gotasPorMl` obligatorio.
- Menos de dos fuentes ⇒ `fuente_unica` automático.
- `pediatria.estado = solo_adulto` ⇒ `motivo` obligatorio y ninguna dosis pediátrica con régimen `por_peso`.
- Dosis pediátrica ≤ tope de adulto de la misma ficha.
- Cada discrepancia declara el valor `mostrado`, que debe ser el más bajo.
- Los ids de orales no pueden usar el prefijo `oral:` (reservado para favoritos y recientes).
- Una prueba recorre las 80 fichas reales y falla si alguna viola una regla.

## 9. Pruebas

- **`oral.test.ts`:** casos del informe — paracetamol 15 mg/kg c/6 h con jarabe de 100 mg/ml; lactulosa 10 g →
  ≈15 ml a 667 mg/ml; haloperidol en gotas (1 gota = 0,1 mg); ondansetrón 2 mg con comprimido de 4 mg →
  rechazado; topes por toma y diario; que nunca supere el tope de adulto; redondeos.
- **Esquema y coherencia:** fixtures válidos e inválidos para cada regla de la sección 8.
- **Datos reales:** las 80 fichas.
- **Interfaz:** aviso en las 16 fichas de fuente única; `solo_adulto` sin calculadora pediátrica; favoritos y
  recientes de orales separados de EV.
- **Regresión:** las 241 pruebas actuales y las 89 fichas EV pasan sin modificarse.

## 10. Errores en pantalla

Falta peso o concentración: el botón no calcula y dice qué falta. Fracción imposible: ofrece la forma líquida o
explica que no hay forma de dar esa dosis. Dosis sobre un tope: se muestra **en el resultado**, no en una nota.

## 11. Entrega y rama

Rama `orales-v1` desde `main` (independiente de `comunidad-etapa-1`, que sigue sin mergear). Se publica por el
flujo actual (push a `main` → pruebas → Pages) **solo después de la revisión de discrepancias por Héctor** y con el
aviso de formación visible. El repo es público: la copia del informe en `informes/` no incluye datos personales.

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Ninguna de las dos fuentes es chilena: no se sabe cuál rige aquí | Aviso visible; mostrar ambas; registro en Chile como dato aparte |
| Errores de unidad o concentración (el más peligroso en líquidos) | Concentración obligatoria; conversión solo por concentración; pruebas con los casos del informe |
| Ficha CIMA del producto equivocado (ya ocurrió 8 veces) | Filtro por `vtm` exacto y exclusión de liberación prolongada al descargar; prueba que cruza fármaco y presentación |
| 16 fichas de una sola fuente | Aviso visible y automático; segunda fuente (DailyMed/ISP) cuando se consiga |
| ISP bloquea la consulta | Un proceso, pausas largas; estado `sin_verificar` mientras tanto |
| Alguien lo use como prescripción | Aviso de formación; sin firma de fichas; propósito declarado en «Acerca» |

## 13. Preguntas abiertas

- Redacción exacta del aviso de fuente única (propuesta: «Esta ficha se apoya en una sola fuente. Contrástala
  antes de usarla»).
- Qué fármacos llevan `altoRiesgo` (propuesta: morfina, tramadol, benzodiacepinas y fenobarbital).
- Si la nota sobre unidades de hierro/levotiroxina va en la ficha o en la calculadora.
