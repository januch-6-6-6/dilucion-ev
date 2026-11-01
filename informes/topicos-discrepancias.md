# Tópicos ojo/oído/nariz: revisión de fuentes y discrepancias (31-oct-2026)

> **Material de formación, no de prescripción.** Este informe cierra la Fase 0 de los tópicos y reemplaza al borrador de Antigravity (`datos/crudos/topicos/INFORME-BORRADOR-agy.md`). Claude revisó las 80 moléculas una por una contra los extractos (`extractos-condensados.md`) y contra los `.txt` completos de CIMA, DailyMed y Pediamécum.

## 1. Resumen

| | Fichas |
|---|---:|
| Moléculas o combinaciones registradas en el ISP (universo) | **80** |
| Con pauta **contrastada** (una pauta respaldada por 2 instituciones) | **13** |
| Con pauta de **una sola fuente** (se publican con aviso) | **51** |
| **Sin pauta**: ficha informativa (presentación, alertas y motivo) | **16** |
| Con alguna pauta pediátrica **off-label** | 7 |
| Marcadas como **alto riesgo** | 10 |

Por vía: ojo 65, nariz 10 y oído 7 (el ciprofloxacino y otras tienen más de una vía).
Por pediatría: con dosis 40, no establecida 22, sin datos 15 y contraindicada 3.

Fuentes: 99 en total. Son 57 fichas técnicas de CIMA (AEMPS), 28 de Pediamécum (AEP), 13 de DailyMed (FDA) y el registro del ISP, que se usa para las presentaciones chilenas.

**Contrastadas (13):** atropina, azelastina, budesonida, ciclopentolato, dorzolamida, ganciclovir, ipratropio, mometasona, mupirocina, olopatadina, tetrizolina, timolol y tropicamida.

**Sin pauta (16):** antazolina + bacitracina + neomicina + xilometazolina, betametasona, betametasona + gentamicina, betametasona + neomicina, betametasona + neomicina + polimixina B, betaxolol, bimatoprost + brimonidina + timolol, brimonidina + dorzolamida + timolol, cromoglicato, dexametasona + moxifloxacino, dextrano + hipromelosa + nafazolina, fenazona + lidocaína, gatifloxacino + prednisolona, ketorolaco, levofloxacino y lidocaína + sulfatiazol.

**Alto riesgo (10):** atropina, ciclopentolato, fenilefrina, tropicamida, brimonidina y sus 3 combinaciones (con brinzolamida, con timolol y con dorzolamida + timolol), bimatoprost + brimonidina + timolol y timolol. El criterio fue toxicidad sistémica grave en niños pequeños por absorción nasolagrimal: crisis anticolinérgica, hipertensión, depresión del SNC o apnea, o broncoespasmo y bradicardia en el caso de los betabloqueantes.

## 2. Reglas de datos (decisiones de Héctor, 31-oct)

Están detalladas en `datos/crudos/topicos/DECISIONES.md`.

1. **Fuente única → se publica con aviso**, igual que en orales.
2. **Concentración:** la pauta se ata a la concentración registrada en Chile. Una pauta de otra concentración va solo a *discrepancias*.
3. **Combinaciones solo chilenas** sin fuente para la combinación → **ficha informativa sin pauta**.
4. **Pediatría** no autorizada en la ficha técnica pero con pauta en Pediamécum → **se muestran ambas**, y la de Pediamécum va como **off-label** con alerta.

Reglas operativas que salieron de la revisión:

- Una fuente de **un solo componente no valida una combinación**.
- Una fuente de la **vía equivocada se excluye** y se registra como discrepancia.
- Una fuente se acepta para la forma farmacéutica chilena solo si es de **la misma forma**. Por ejemplo, una pomada no respalda un colirio.
- **No se inventan frecuencias.** «Cada 3–4 h» o «según necesidad» no se convierten en veces al día para la calculadora.
- Validez «un mes» tras abrir → la calculadora usa **28 días**.
- **Contrastada** = al menos una pauta trae una segunda fuente concordante (campo `tambien`) de otra institución. Una pauta adulta de CIMA y otra pediátrica de Pediamécum **no** cuentan como contraste, porque son pautas distintas. Esta regla es más estricta que la de orales.

## 3. Correcciones al borrador de Antigravity

El borrador contaba 🔴 6, 🟡 22, 🟢 16, ⚪ 32 y ⚠️ 8 sobre **84** moléculas. Le faltaban las exclusiones de Héctor: calcitonina, desmopresina, esketamina y Mentholatum. Además tenía estos errores:

### 3.1 Pediamécum de la vía equivocada (el borrador los contaba como segunda fuente)

| Molécula | Lo que había en Pediamécum |
|---|---|
| azelastina + fluticasona (nasal) | azelastina en colirio |
| cromoglicato (ungüento oftálmico) | cromoglicato nebulizado o nasal |
| ciprofloxacino | ciprofloxacino IV u oral |
| betametasona y sus combinaciones oftálmicas | betametasona cutánea o inyectable |
| prednisolona (colirio) | prednisolona oral |
| tobramicina (oftálmica) | tobramicina sistémica o inhalada |
| mometasona + olopatadina (nasal) | olopatadina en colirio |

### 3.2 Fuente de un componente no valida la combinación

Varias combinaciones que COBERTURA.md marcaba con «2 fuentes» solo tenían fuente de un componente. Pasan a fuente única o a sin pauta: brimonidina + brinzolamida, brimonidina + timolol, brinzolamida + timolol, bimatoprost + timolol, dorzolamida + timolol, latanoprost + timolol, timolol + travoprost, dexametasona + tobramicina, loteprednol + tobramicina y las triples con brimonidina.

### 3.3 Concentración chilena distinta de la ficha

| Molécula | Chile | Fuente | Resultado |
|---|---|---|---|
| betaxolol | 0,5 % solución | CIMA 0,25 % suspensión | sin pauta |
| ketorolaco | 0,4 % | CIMA 0,5 % | sin pauta |
| levofloxacino | 0,5 % | CIMA 1,5 % | sin pauta |
| fenilefrina | 2,5 % | CIMA 10 % | solo la pauta pediátrica de Pediamécum (2,5 %), off-label |
| bimatoprost | 0,01 %, 0,03 % y gel 0,1 mg/g | CIMA 0,1 mg/ml | pauta solo para 0,01 % |
| brimonidina | 0,15 %, 0,2 % y uno sin concentración | CIMA 0,2 % | pauta solo para 0,2 % |
| ketotifeno | 0,025 % y 0,05 % | CIMA 0,25 mg/ml | pauta solo para 0,025 % |
| loteprednol | 0,2 % y 0,5 % | CIMA 0,2 % | pauta solo para 0,2 % |
| fluticasona nasal | propionato 50 mcg y furoato 27,5 mcg | CIMA furoato | pauta solo para furoato 27,5 mcg |
| ipratropio nasal | 21 y 42 mcg | CIMA 21 mcg | pauta solo para 21 mcg |
| olopatadina | 0,1 % y 0,2 % | CIMA 0,1 % | pauta solo para 0,1 % |
| pilocarpina | 2 % y 4 % | CIMA 2 % | pauta solo para 2 % |
| nafazolina | 0,012 % y 0,1 % | sin concentración | pauta asociada a 0,012 %; la de 0,1 % queda sin pauta |

### 3.4 Forma farmacéutica distinta

- **Cromoglicato:** en Chile es ungüento oftálmico y la fuente FDA es en gotas → sin pauta.
- **Dexametasona:** en Chile hay 0,15 % unidosis y la ficha CIMA es de otra forma → solo queda la pauta pediátrica de Pediamécum, off-label.
- **Gentamicina:** solo el ungüento tiene pauta.
- **Cloranfenicol:** la pomada se respalda con CIMA y el colirio pediátrico con Pediamécum.
- **Ciprofloxacino:** el ungüento no tiene pauta (solo la solución oftálmica y la ótica).
- **Tobramicina:** solo el ungüento 0,3 % tiene pauta; la solución queda sin pauta.
- **Oximetazolina nasal:** la pauta de CIMA es para pulverizador. Los registros que dicen «solución nasal» sin indicar si son gotas o pulverizador quedan sin pauta.

### 3.5 Otras correcciones

- **Bacitracina + neomicina + polimixina B:** el borrador ponía 6 veces al día a partir de «cada 3–4 h». Se quitó: la calculadora no usa frecuencias inventadas.
- **Ciclopentolato:** la dosis de examen no es diaria, así que no lleva veces al día.
- **Dexametasona:** la conservación citaba a Pediamécum; ahora cita el registro ISP.
- **Tetrizolina:** CIMA dice «nunca más de una semana» y Pediamécum «no más de 72 h». Se muestra **72 h**, la cifra más baja.
- **Ciprofloxacino + fluocinolona:** CIMA indica 6–8 gotas cada 12 h y Pediamécum 4–6 gotas cada 8 h. Se muestra CIMA y la otra cifra queda en discrepancias.
- **Hialuronato y nafazolina en DailyMed:** se consideran fuentes débiles. El producto de nafazolina de la FDA trae propilenglicol; se usa solo para la frecuencia de adulto, que coincide con Pediamécum.
- **Atropina 1 %:** CIMA autoriza desde los 3 años; Pediamécum da pauta de 1 a 3 años, que se muestra como off-label (decisión 4).

## 4. Pendiente para una revisión clínica

- Que un profesional revise el campo `meta.revisadoPor` de cada ficha, que hoy está vacío. La app muestra «Revisión clínica: pendiente».
- Buscar fichas técnicas de las 16 sin pauta, por ejemplo en EMA, FDA o del fabricante chileno.
- El volumen del envase no está en el nombre del ISP. La calculadora le pide el volumen al usuario.
