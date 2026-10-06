# Revisión Clínica Pendiente — Medicamentos Orales APS (v1)

**Fecha:** 5 de octubre de 2026  
**Rama:** `orales-v1`  
**Revisor:** Héctor Salvo Agüero (TENS e Ingeniero en Informática)  
**Propósito:** Documento de entrega para revisión clínica antes de autorizar la fusión a `main` y publicación en GitHub Pages.

---

## 1. Resumen de la Implementación

- **79 fichas de medicamentos orales** transcritas y validadas según el arsenal de Atención Primaria de Salud (APS) de Chile (80 menos clorfenamina oral, excluida por falta de posología contrastable).
- **Módulo Orales totalmente desacoplado:** Las 89 fichas EV preexistentes y sus 241 pruebas permanecen 100% intactas y funcionales.
- **Calculadoras orales incorporadas:**
  - Pediátrica por peso corporal (mg/kg por toma o por día con número de tomas y tope por toma / diario).
  - Pediátrica por tramos de edad (`por_edad`).
  - Dosis fija para adultos y adolescentes.
  - Conversión automática a volumen (ml) para presentaciones líquidas (jarabes, soluciones y suspensiones) y conteo de gotas para soluciones orales en gotas.
- **Regla del tope más bajo:** En discrepancias numéricas de dosis máxima entre CIMA (AEMPS) y Pediamécum (AEP), la calculadora aplica siempre la cifra más conservadora para seguridad del paciente.

---

## 2. Fichas de Fuente Única (15)

Estas fichas no pudieron contrastarse con una segunda fuente independiente debido a que no cuentan con monografía en Pediamécum o no disponen de ficha técnica complementaria en las bases consultadas. Se muestran en la aplicación con el distintivo:  
> *«Esta ficha se apoya en una sola fuente y no se pudo contrastar con otra.»*

| # | Medicamento | Id | Fuente única citada | Motivo clínico / Observación |
|---|---|---|---|---|
| 1 | Carbamazepina | `carbamazepina` | CIMA (España) | Pediamécum no posee monografía independiente. |
| 2 | Ciclobenzaprina | `ciclobenzaprina` | CIMA (España) | Miorrelajante de uso exclusivo en adultos; sin monografía pediátrica. |
| 3 | Empagliflozina | `empagliflozina` | CIMA (España) | iSGLT2 para diabetes tipo 2 en adultos; sin indicación pediátrica. |
| 4 | Escitalopram | `escitalopram` | CIMA (España) | Antidepresivo ISRS sin aprobación pediátrica en ficha técnica CIMA. |
| 5 | Flucloxacilina | `flucloxacilina` | CIMA (España) | Isoxazolilpenicilina antiestafilocócica; sin ficha en Pediamécum. |
| 6 | Gemfibrozilo | `gemfibrozilo` | CIMA (España) | Fibrato hipolipemiante de indicación exclusiva en adultos. |
| 7 | Isosorbide | `isosorbide` | CIMA (España) | Vasodilatador coronario de uso exclusivo en cardiopatía isquémica adulta. |
| 8 | Mirtazapina | `mirtazapina` | CIMA (España) | Antidepresivo noradrenérgico/serotoninérgico (`solo_adulto`). |
| 9 | Paracetamol + Tramadol | `paracetamol-tramadol` | CIMA (España) | Combinación fija analgésica de uso en adultos y adolescentes >12 años. |
| 10 | Quetiapina | `quetiapina` | CIMA (España) | Antipsicótico atípico; liberación inmediata (`solo_adulto`). |
| 11 | Sertralina | `sertralina` | CIMA (España) | Sin monografía separada en Pediamécum para APS. |
| 12 | Tramadol | `tramadol` | CIMA (España) | Opioide menor (`altoRiesgo`); ficha CIMA para gotas y cápsulas. |
| 13 | Trimebutino | `trimebutino` | Pediamécum (AEP) | Sin ficha técnica CIMA disponible; solo monografía Pediamécum. |
| 14 | Vildagliptina | `vildagliptina` | CIMA (España) | iDPP4 antidiabético oral (`solo_adulto`). |
| 15 | Zopiclona | `zopiclona` | CIMA (España) | Hipnótico no benzodiacepínico (`solo_adulto`). |

---

## 3. Discrepancias Clínicas entre Fuentes (🔴)

A continuación se listan las discrepancias detectadas entre las fichas oficiales (CIMA / DailyMed / MINSAL) y las guías pediátricas (Pediamécum), indicando la cifra o conducta adoptada y la alternativa.


### 1. Aciclovir (`aciclovir`)

#### Discrepancia: Método de dosificación en niños
- **Cifra / criterio mostrado en la app:** `Se muestran las pautas de ficha técnica como autorizadas y las de Pediamécum, por peso, como off-label`
- **Fundamento clínico adoptado:** Diferencia de método (dosis fija por edad frente a mg/kg), no un conflicto numérico de un mismo régimen.
- **Valores por fuente contrastada:**
  - **CIMA-ACICLOVIR-59226:** CIMA: dosis fijas por edad (herpes simple 100 o 200 mg cinco veces al día; varicela 200, 400 u 800 mg cuatro veces al día)
  - **PEDIAMECUM-ACICLOVIR:** Pediamécum: dosis por peso (varicela 80 mg/kg/día cada 6 h, máx. 800 mg/dosis; gingivoestomatitis 60 mg/kg/día, máx. 200 mg/dosis); "Las dosis recomendadas aceptadas por la comunidad científica no siempre coinciden con las dosis aprobadas en ficha técnica"


### 2. Ácido acetilsalicílico (`acido-acetilsalicilico`)

#### Discrepancia: Uso en menores de 16 años
- **Cifra / criterio mostrado en la app:** `No se muestra dosis pediátrica`
- **Fundamento clínico adoptado:** Decisión del proyecto: solo dosis de adulto; las pautas pediátricas son de uso especializado y nunca como analgésico o antipirético común.
- **Valores por fuente contrastada:**
  - **CIMA-ACIDO-ACETILSALICILICO:** Contraindicado en niños menores de 16 años por su relación con el síndrome de Reye (CIMA)
  - **PEDIAMECUM-ACIDO-ACETILSALICILICO:** Pautas pediátricas especializadas: dolor, artritis idiopática juvenil, fiebre reumática, Kawasaki y antiagregación (Pediamécum)


### 3. Ácido fólico (`acido-folico`)

#### Discrepancia: Dosis en estados carenciales (adultos vs niños)
- **Cifra / criterio mostrado en la app:** `1 mg/día en pediatría / 5 mg/día en adultos`
- **Fundamento clínico adoptado:** CIMA sólo dispone de la presentación de 5 mg con pauta adulta de 5-15 mg/día; en pediatría la dosis de consenso es de 1 mg/día (respaldada por el comprimido de 1 mg del arsenal chileno). No debe administrarse el comprimido de 5 mg a pacientes pediátricos.
- **Valores por fuente contrastada:**
  - **CIMA-ACIDO-FOLICO:** Adultos: 5-15 mg/día (comprimidos de 5 mg)
  - **PEDIAMECUM-ACIDO-FOLICO:** Niños: 1 mg/día independiente de la edad


### 4. Ácido valproico (`acido-valproico`)

#### Discrepancia: Dosis de mantenimiento pediátrica
- **Cifra / criterio mostrado en la app:** `30 mg/kg/día`
- **Fundamento clínico adoptado:** CIMA fija 30 mg/kg/día para lactantes y niños (28 días a 11 años); Pediamécum amplía el rango a 30-60 mg/kg/día señalando que niños con inductores enzimáticos pueden requerir dosis mayores. Se muestra la cifra más conservadora.
- **Valores por fuente contrastada:**
  - **CIMA-ACIDO-VALPROICO-48827:** 30 mg/kg/día
  - **PEDIAMECUM-ACIDO-VALPROICO:** 30-60 mg/kg/día


### 5. Alopurinol (`alopurinol`)

#### Discrepancia: Tope diario pediátrico
- **Cifra / criterio mostrado en la app:** `400 mg/día`
- **Fundamento clínico adoptado:** Mismo régimen y población (niños, por peso): se muestra el tope más bajo. En la tabla por edad de Pediamécum (<6 años 150, 6-10 años 300, >10 años 600-800 mg/día) solo la fila >10 años supera ese tope; la tabla no se carga como dosis.
- **Valores por fuente contrastada:**
  - **CIMA-ALOPURINOL:** 400 mg/día: niños <15 años, 10-20 mg/kg/día o 100-400 mg diarios (CIMA)
  - **PEDIAMECUM-ALOPURINOL:** 800 mg/día: 10-20 mg/kg/día cada 8 h; por edad >10 años y adolescentes 600-800 mg/día (Pediamécum)


### 6. Amlodipino (`amlodipino`)

#### Discrepancia: Dosis máxima en 6-17 años
- **Cifra / criterio mostrado en la app:** `5 mg/día`
- **Fundamento clínico adoptado:** Regla del tope más bajo para la misma población y pauta.
- **Valores por fuente contrastada:**
  - **CIMA-AMLODIPINO:** 5 mg diarios: no se han estudiado dosis superiores en pacientes pediátricos (CIMA)
  - **PEDIAMECUM-AMLODIPINO:** 10 mg/día: "Hay estudios con una dosis máxima de hasta 10 mg/día"; >5 mg/día es off-label (Pediamécum)


### 7. Amoxicilina + ácido clavulánico (`amoxicilina-clavulanico`)

#### Discrepancia: Dosis pediátrica alta (otitis, sinusitis, infección respiratoria baja)
- **Cifra / criterio mostrado en la app:** `70 mg/kg/día de amoxicilina`
- **Fundamento clínico adoptado:** Mismo régimen (dosis alta en infección respiratoria y ORL) y población: se muestra la cifra más baja. En la tabla de Pediamécum la pauta de 80-90 mg/kg/día está en la columna «8:1 (susp) / 7:1 (comp, sobres)»; para pasar de 70 mg/kg/día la ficha aconseja elegir otra formulación.
- **Valores por fuente contrastada:**
  - **CIMA-AMOXICILINA-CLAVULANICO-59515:** 70 mg/kg/día de amoxicilina (10 mg/kg/día de clavulánico) en 2 dosis, proporción 7:1 (CIMA, Augmentine 875/125)
  - **PEDIAMECUM-AMOXICILINA-CLAVULANICO:** 80-90 mg/kg/día de amoxicilina (9-15 mg/kg/día de clavulánico) en 2-3 dosis, con alta tasa de resistencia de S. pneumoniae (Pediamécum)

#### Discrepancia: Tope diario de amoxicilina en niños
- **Cifra / criterio mostrado en la app:** `2625 mg/día de amoxicilina en las pautas 7:1 (equivale a 375 mg/día de clavulánico)`
- **Fundamento clínico adoptado:** Cifra derivada: se aplica el máximo de clavulánico de Pediamécum (375 mg/día), más restrictivo que ambas cifras de amoxicilina; en proporción 7:1 corresponde a 2625 mg de amoxicilina, la misma cifra que la ficha da para 875/125 tres veces al día.
- **Valores por fuente contrastada:**
  - **CIMA-AMOXICILINA-CLAVULANICO-59515:** 2800 mg/día: máximo que aporta la formulación 7:1 en niños <40 kg ("1 000 – 2 800 mg de amoxicilina/143 - 400 mg de ácido clavulánico")
  - **PEDIAMECUM-AMOXICILINA-CLAVULANICO:** 3000 mg/día de amoxicilina, "sin superar dosis máxima de ácido clavulánico" (15 mg/kg/día, sin superar 375 mg/día) (Pediamécum)


### 8. Amoxicilina (`amoxicilina`)

#### Discrepancia: Dosis pediátrica en faringoamigdalitis estreptocócica
- **Cifra / criterio mostrado en la app:** `50 mg/kg/día, con máximo de 500 mg por toma`
- **Fundamento clínico adoptado:** Mismo régimen y población: se muestra la cifra más baja (Pediamécum), que además trae tope en mg.
- **Valores por fuente contrastada:**
  - **CIMA-AMOXICILINA-62880:** hasta 90 mg/kg/día: "De 40 a 90 mg/kg/día en dosis divididas" en amigdalitis y faringitis (CIMA)
  - **PEDIAMECUM-AMOXICILINA:** hasta 50 mg/kg/día: 40-50 mg/kg/día cada 12 o 24 h, máximo 500 mg/12 h o 1 g/24 h (Pediamécum)


### 9. Atenolol (`atenolol`)

#### Discrepancia: Uso en niños
- **Cifra / criterio mostrado en la app:** `Se muestra la pauta de Pediamécum como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Discrepancia de población: la ficha no lo recomienda en niños.
- **Valores por fuente contrastada:**
  - **CIMA-ATENOLOL:** No se ha establecido la seguridad y eficacia en niños: no se recomienda su empleo (CIMA)
  - **PEDIAMECUM-ATENOLOL:** Todas las indicaciones pediátricas son off-label, con pauta por peso (Pediamécum)


### 10. Atorvastatina (`atorvastatina`)

#### Discrepancia: Dosis máxima en niños de 4 a 10 años
- **Cifra / criterio mostrado en la app:** `40 mg/día`
- **Fundamento clínico adoptado:** Regla del tope más bajo dentro de la misma fuente y población.
- **Valores por fuente contrastada:**
  - **PEDIAMECUM-ATORVASTATINA:** 40 mg/día: máximo recomendado (Pediamécum)
  - **PEDIAMECUM-ATORVASTATINA:** 80 mg/día: "en algunos casos se ha aumentado hasta 80 mg/día" (Pediamécum)

#### Discrepancia: Uso en menores de 10 años
- **Cifra / criterio mostrado en la app:** `Se muestra la pauta de Pediamécum como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Discrepancia de población. Pediamécum advierte que la seguridad con dosis >20 mg (≈0,5 mg/kg) en niños es limitada.
- **Valores por fuente contrastada:**
  - **CIMA-ATORVASTATINA:** No está indicada en pacientes de menos de 10 años; no se puede hacer una recomendación posológica (CIMA)
  - **PEDIAMECUM-ATORVASTATINA:** Pauta para niños de 4 a 10 años (Pediamécum)


### 11. Captopril (`captopril`)

#### Discrepancia: Tope diario
- **Cifra / criterio mostrado en la app:** `150 mg/día como tope de adulto (la calculadora lo aplica también a las pautas pediátricas por peso)`
- **Fundamento clínico adoptado:** Regla del tope más bajo. La pauta pediátrica de Pediamécum conserva su propio máximo de 450 mg/día, pero la calculadora limita además al tope de adulto de la ficha.
- **Valores por fuente contrastada:**
  - **CIMA-CAPTOPRIL:** 150 mg/día: dosis máxima diaria recomendada de la ficha (adultos)
  - **PEDIAMECUM-CAPTOPRIL:** 450 mg/día: hipertensión en niños y adolescentes (otras publicaciones; en insuficiencia cardíaca, 150 mg/día)

#### Discrepancia: Relación con las comidas
- **Cifra / criterio mostrado en la app:** `Se muestran ambas indicaciones`
- **Fundamento clínico adoptado:** La ficha técnica permite tomarlo con comida; Pediamécum recomienda separarlo de las comidas.
- **Valores por fuente contrastada:**
  - **CIMA-CAPTOPRIL:** Antes, durante y después de las comidas (CIMA)
  - **PEDIAMECUM-CAPTOPRIL:** Una hora antes de las comidas o dos horas después: el alimento dificulta la absorción (Pediamécum)


### 12. Carvedilol (`carvedilol`)

#### Discrepancia: Uso en menores de 18 años
- **Cifra / criterio mostrado en la app:** `Se muestran las pautas de Pediamécum como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Discrepancia de población: la ficha no establece su uso en <18 años.
- **Valores por fuente contrastada:**
  - **CIMA-CARVEDILOL:** No se ha establecido la seguridad y eficacia en niños y adolescentes menores de 18 años (CIMA)
  - **PEDIAMECUM-CARVEDILOL:** Pautas off-label con variabilidad importante entre fuentes (Pediamécum)


### 13. Cefadroxilo (`cefadroxilo`)

#### Discrepancia: Dosis diaria máxima del adulto
- **Cifra / criterio mostrado en la app:** `2000 mg/día (la pauta de la ficha, 1000 mg cada 12 h)`
- **Fundamento clínico adoptado:** Misma población adulta: se muestra la cifra más baja (informe §2). No se carga un topeDiario de adulto: 2000 es el total de la pauta, no un máximo declarado, y el de 4 g/día de Pediamécum es más alto.
- **Valores por fuente contrastada:**
  - **CIMA-CEFADROXILO-55730:** 2000 mg/día: 1000 mg dos veces al día (CIMA, Duracef)
  - **PEDIAMECUM-CEFADROXILO:** 4000 mg/día: "Dosis máxima en adultos 4 g al día"; dosis habitual 1-2 g al día en 1 o 2 dosis (Pediamécum)

#### Discrepancia: Dosis pediátrica diaria
- **Cifra / criterio mostrado en la app:** `30 mg/kg/día`
- **Fundamento clínico adoptado:** La ficha de la suspensión trae dos tablas orientativas; se muestra la cifra más baja, que es la de la tabla por indicación y la de Pediamécum.
- **Valores por fuente contrastada:**
  - **CIMA-CEFADROXILO-55731:** 50 mg/kg/día: tabla "Recomendaciones generales de dosificación basadas en 50 mg/kg/día" (CIMA, Duracef suspensión)
  - **CIMA-CEFADROXILO-55731:** 30 mg/kg/día en dos dosis, máximo 2 g/día: tabla por indicación de la misma ficha; Pediamécum coincide


### 14. Celecoxib (`celecoxib`)

#### Discrepancia: Población pediátrica
- **Cifra / criterio mostrado en la app:** `Se muestra la dosis pediátrica de Pediamécum, marcada como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Contradicción de población, no de cifra. Pediamécum advierte que las cápsulas disponibles dificultan dosificar a niños pequeños.
- **Valores por fuente contrastada:**
  - **CIMA-CELECOXIB:** CIMA: no está indicado el uso de celecoxib en niños
  - **PEDIAMECUM-CELECOXIB:** Pediamécum: artritis idiopática juvenil 50 mg cada 12 h (10-25 kg) o 100 mg cada 12 h (>25 kg), off-label


### 15. Clonazepam (`clonazepam`)

#### Discrepancia: Tope pediátrico en adolescentes 10-16 años
- **Cifra / criterio mostrado en la app:** `Mantenimiento 3-6 mg/día`
- **Fundamento clínico adoptado:** Pediamécum indica dosis máxima 20 mg/día para 10-16 años, cifra idéntica al tope de adultos; se trata como advertencia clínica no confirmada para no inducir sobredosis en adolescentes.
- **Valores por fuente contrastada:**
  - **CIMA-CLONAZEPAM-79769:** Mantenimiento 3-6 mg/día (máximo no especificado en niños)
  - **PEDIAMECUM-CLONAZEPAM:** Dosis máxima 20 mg/día


### 16. Cotrimoxazol (trimetoprima + sulfametoxazol) (`cotrimoxazol`)

#### Discrepancia: Dosis pediátrica diaria en infecciones ORL, respiratorias y urinarias (mg de trimetoprima)
- **Cifra / criterio mostrado en la app:** `6 mg de trimetoprima/kg/día`
- **Fundamento clínico adoptado:** Mismo régimen y población: se muestra la cifra más baja (Pediamécum da entre 1,3 y 2 veces más). La propia ficha da 5/25 mg/kg cada 12 h durante 3 días como alternativa en infección urinaria no complicada y diarrea infecciosa.
- **Valores por fuente contrastada:**
  - **CIMA-COTRIMOXAZOL:** 6 mg de trimetoprima/kg/día (30 mg de sulfametoxazol/kg/día) en 2 tomas (CIMA, Septrin)
  - **PEDIAMECUM-COTRIMOXAZOL:** 8-12 mg de trimetoprima/kg/día: "20-30/4-6 mg/kg/12 h" en notación SMX/TMP, es decir 4-6 mg de trimetoprima/kg cada 12 h (Pediamécum)


### 17. Desloratadina (`desloratadina`)

#### Discrepancia: Población pediátrica (menores de 1 año)
- **Cifra / criterio mostrado en la app:** `Se muestra la dosis pediátrica de Pediamécum, marcada como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Contradicción de población, no de cifra; en el resto de edades ambas fuentes coinciden.
- **Valores por fuente contrastada:**
  - **CIMA-DESLORATADINA-00160065:** CIMA: no se ha establecido la seguridad y eficacia en niños menores de 1 año
  - **PEDIAMECUM-DESLORATADINA:** Pediamécum: lactantes de 6 a 11 meses, 1 mg/24 h (off-label)


### 18. Dexametasona (`dexametasona`)

#### Discrepancia: Forma de dosificar en niños
- **Cifra / criterio mostrado en la app:** `Se muestra la dosis oral de crup de Pediamécum, marcada como off-label`
- **Fundamento clínico adoptado:** Diferencia de método (superficie corporal frente a mg/kg), no de cifra.
- **Valores por fuente contrastada:**
  - **CIMA-DEXAMETASONA:** CIMA: no da mg/kg; la dosis pediátrica se ajusta en función de la superficie corporal
  - **PEDIAMECUM-DEXAMETASONA:** Pediamécum: dosis por indicación en mg/kg (crup, edema cerebral, edema de vía aérea, etc.)


### 19. Diazepam (`diazepam`)

#### Discrepancia: Techo pediátrico oral
- **Cifra / criterio mostrado en la app:** `0,3 mg/kg/día`
- **Fundamento clínico adoptado:** CIMA establece como norma general pediátrica 0,1-0,3 mg/kg/día; Pediamécum autoriza hasta 0,8 mg/kg/día en ansiedad y 1 mg/kg/día en convulsiones febriles (3 veces el techo de la ficha). Se muestra el límite conservador de CIMA (0,3 mg/kg/día).
- **Valores por fuente contrastada:**
  - **CIMA-DIAZEPAM-80699:** 0,3 mg/kg/día: norma general máxima al día (CIMA)
  - **PEDIAMECUM-DIAZEPAM:** 0,8 mg/kg/día: dosis máxima en ansiedad (Pediamécum); 1 mg/kg/día en convulsiones febriles


### 20. Diclofenaco (`diclofenaco`)

#### Discrepancia: Población pediátrica
- **Cifra / criterio mostrado en la app:** `Se muestra la dosis pediátrica de Pediamécum, marcada como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Contradicción de población, no de cifra: la ficha técnica no respalda la dosis en <14 años. El rango por peso es amplio (6 veces).
- **Valores por fuente contrastada:**
  - **CIMA-DICLOFENACO:** CIMA: debido a la dosis del comprimido no se recomienda en niños ni adolescentes menores de 14 años
  - **PEDIAMECUM-DICLOFENACO:** Pediamécum: 0,5-3 mg/kg/día en 2-4 dosis (máx. 150 mg/día) desde 1 año; autorizado (A) solo en mayores de 14 años

#### Discrepancia: Tope diario del adulto
- **Cifra / criterio mostrado en la app:** `100 mg/día`
- **Fundamento clínico adoptado:** La ficha da un rango para el máximo; se muestra el extremo conservador y se avisa que permite hasta 150 mg/día.
- **Valores por fuente contrastada:**
  - **CIMA-DICLOFENACO:** 100 mg/día: extremo inferior de "La dosis máxima diaria recomendada es de 100 a 150 mg"
  - **CIMA-DICLOFENACO:** 150 mg/día: extremo superior del mismo rango


### 21. Domperidona (`domperidona`)

#### Discrepancia: Uso en menores de 12 años o de 35 kg
- **Cifra / criterio mostrado en la app:** `No se muestra dosis pediátrica`
- **Fundamento clínico adoptado:** Decisión del proyecto: solo la dosis de adultos y adolescentes ≥12 años y ≥35 kg.
- **Valores por fuente contrastada:**
  - **CIMA-DOMPERIDONA-55411:** No debe utilizarse en niños menores de 12 años ni en adolescentes de menos de 35 kg (sin eficacia) (CIMA)
  - **PEDIAMECUM-DOMPERIDONA:** 0,25 mg/kg cada 8 h como off-label en lactantes y niños <12 años o <35 kg, con alerta de seguridad: supresión de la indicación en Pediatría (Pediamécum)


### 22. Famotidina (`famotidina`)

#### Discrepancia: Uso en niños
- **Cifra / criterio mostrado en la app:** `Se muestran las pautas pediátricas de Pediamécum como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Solo Pediamécum respalda la dosis pediátrica.
- **Valores por fuente contrastada:**
  - **CIMA-FAMOTIDINA:** La ficha solo da posología de adultos
  - **PEDIAMECUM-FAMOTIDINA:** No se ha establecido la eficacia y seguridad en niños: todos los usos son off-label (Pediamécum)


### 23. Fenitoína (`fenitoina`)

#### Discrepancia: Dosis pediátrica de mantenimiento en niños mayores
- **Cifra / criterio mostrado en la app:** `4-8 mg/kg/día`
- **Fundamento clínico adoptado:** Pediamécum amplía el mantenimiento en niños mayores hasta 8-10 mg/kg/día, lo que a pesos intermedios puede saturar la cinética no lineal de Michaelis-Menten. Se conserva la recomendación de 4-8 mg/kg/día con tope de 300 mg/día.
- **Valores por fuente contrastada:**
  - **CIMA-FENITOINA:** Mantenimiento 4-8 mg/kg/día, máximo 300 mg/día
  - **PEDIAMECUM-FENITOINA:** En niños más mayores se recomienda 8-10 mg/kg/día (máximo 300 mg/día)


### 24. Fenobarbital (`fenobarbital`)

#### Discrepancia: Dosis máxima en adultos
- **Cifra / criterio mostrado en la app:** `200 mg/día`
- **Fundamento clínico adoptado:** Pediamécum fija como dosis máxima en adultos 200 mg/día, mientras CIMA sitúa el mantenimiento hasta 250 mg/día. Se muestra el tope más conservador (200 mg/día).
- **Valores por fuente contrastada:**
  - **CIMA-FENOBARBITAL:** 250 mg/día: dosis máxima de mantenimiento recomendada (CIMA)
  - **PEDIAMECUM-FENOBARBITAL:** 200 mg/día: dosis máxima en adultos (Pediamécum)


### 25. Fluconazol (`fluconazol`)

#### Discrepancia: Tope diario pediátrico
- **Cifra / criterio mostrado en la app:** `400 mg/día`
- **Fundamento clínico adoptado:** Misma población pediátrica: se muestra el tope más bajo.
- **Valores por fuente contrastada:**
  - **CIMA-FLUCONAZOL-58804:** 400 mg/día: "En la población pediátrica, no debe excederse una dosis máxima de 400 mg al día" (CIMA)
  - **PEDIAMECUM-FLUCONAZOL:** 800 mg/día: no sobrepasar la dosis máxima diaria de adultos (Pediamécum, que añade que la ficha técnica no recomienda superar 400-600 mg/día)


### 26. Fluoxetina (`fluoxetina`)

#### Discrepancia: Techo pediátrico en depresión y TOC
- **Cifra / criterio mostrado en la app:** `20 mg/día`
- **Fundamento clínico adoptado:** CIMA sitúa el límite pediátrico avalado en 20 mg/día señalando experiencia mínima por encima de esa cifra; Pediamécum recoge pautas de expertos hasta 40-60 mg/día. Se muestra el tope oficial conservador de 20 mg/día.
- **Valores por fuente contrastada:**
  - **CIMA-FLUOXETINA-63499:** 20 mg/día en depresión pediátrica (experiencia mínima con >20 mg)
  - **PEDIAMECUM-FLUOXETINA:** Hasta 40 mg/día en depresión (dosis alternativa de expertos); 20-60 mg/día en TOC


### 27. Furosemida (`furosemida`)

#### Discrepancia: Tope diario pediátrico
- **Cifra / criterio mostrado en la app:** `40 mg/día`
- **Fundamento clínico adoptado:** Regla del tope más bajo para la misma población y vía; es la mayor diferencia del bloque cardiovascular.
- **Valores por fuente contrastada:**
  - **CIMA-FUROSEMIDA:** 40 mg por día de furosemida por vía oral (CIMA, niños)
  - **PEDIAMECUM-FUROSEMIDA:** 600 mg/día: uso crónico, subiendo hasta 6 mg/kg/día (Pediamécum); uso agudo hasta 6 mg/kg/dosis y 200 mg/dosis


### 28. Glibenclamida (`glibenclamida`)

#### Discrepancia: Dosis diaria máxima
- **Cifra / criterio mostrado en la app:** `15 mg/día`
- **Fundamento clínico adoptado:** Regla del tope más bajo.
- **Valores por fuente contrastada:**
  - **DAILYMED-GLIBENCLAMIDA:** 20 mg/día: "Daily doses of more than 20 mg are not recommended" (prospecto de EE. UU.)
  - **PEDIAMECUM-GLIBENCLAMIDA:** 15 mg/día: "la dosis máxima recomendada es de 15 mg/día", sin más de 10 mg por toma (Pediamécum)


### 29. Haloperidol (`haloperidol`)

#### Discrepancia: Dosis máxima en adolescentes >13 años
- **Cifra / criterio mostrado en la app:** `5 mg/día`
- **Fundamento clínico adoptado:** CIMA establece un techo estricto de 5 mg/día en adolescentes para limitar el riesgo de distonías y síntomas extrapiramidales; Pediamécum contempla hasta 15 mg/día. Se muestra el límite oficial de 5 mg/día.
- **Valores por fuente contrastada:**
  - **CIMA-HALOPERIDOL-58355:** Máximo 5 mg/día en adolescentes 13-17 años
  - **PEDIAMECUM-HALOPERIDOL:** Máximo 15 mg/día repartidos en 2-3 dosis


### 30. Hidroclorotiazida (`hidroclorotiazida`)

#### Discrepancia: Estatus pediátrico
- **Cifra / criterio mostrado en la app:** `Se muestra la pauta pediátrica como autorizada por la ficha de EE. UU.`
- **Fundamento clínico adoptado:** Las cifras coinciden (1-2 mg/kg/día; 37,5 y 100 mg/día); difiere el estatus regulatorio entre países.
- **Valores por fuente contrastada:**
  - **DAILYMED-HIDROCLOROTIAZIDA:** El prospecto de EE. UU. da pauta pediátrica basada en uso empírico y literatura publicada (sin ensayos controlados)
  - **PEDIAMECUM-HIDROCLOROTIAZIDA:** Sin ninguna indicación aprobada en población pediátrica en España: off-label (Pediamécum)


### 31. Ibuprofeno (`ibuprofeno`)

#### Discrepancia: Tope diario
- **Cifra / criterio mostrado en la app:** `1200 mg/día como tope de adulto`
- **Fundamento clínico adoptado:** Regla del tope más bajo para el adulto/adolescente ≥40 kg con dosis fija cada 6-8 h. La pauta por peso de Pediamécum (40 mg/kg/día, ≥6 meses) es otro régimen con su propio máximo de 2400 mg/día (Ruling 9): no se reemplaza; la calculadora aplica además el tope de adulto (1200 mg/día).
- **Valores por fuente contrastada:**
  - **CIMA-IBUPROFENO-88314:** 1200 mg/24 h: adultos y adolescentes ≥12 años y ≥40 kg, 400 mg cada 6-8 h (CIMA, Difenadol 400 mg)
  - **PEDIAMECUM-IBUPROFENO:** 2400 mg/día: adolescentes, 400-600 mg cada 6-8 h (Pediamécum, párrafo de dismenorrea primaria)

#### Discrepancia: Tabla por peso de Pediamécum (20-29 kg, 30-39 kg, ≥40 kg)
- **Cifra / criterio mostrado en la app:** `No se carga como dosis oral`
- **Fundamento clínico adoptado:** En el texto de Pediamécum esa tabla pertenece a la vía intravenosa (dolor moderado-grave y fiebre en >6 años y >20 kg), no a la oral; el informe la había leído como una segunda pauta oral.
- **Valores por fuente contrastada:**
  - **PEDIAMECUM-IBUPROFENO:** 20-30 mg/kg/día en 3-4 dosis con topes de 600, 800 y 1200 mg/día por peso: aparece bajo el epígrafe «Intravenoso»


### 32. Ketorolaco (`ketorolaco`)

#### Discrepancia: Población pediátrica
- **Cifra / criterio mostrado en la app:** `Se muestra la dosis pediátrica de Pediamécum, marcada como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Coinciden en el tope (40 mg/día) y en la duración máxima; difieren en la edad mínima.
- **Valores por fuente contrastada:**
  - **CIMA-KETOROLACO:** CIMA: eficacia y seguridad no establecidas en niños; no se recomienda en menores de 16 años
  - **PEDIAMECUM-KETOROLACO:** Pediamécum: oral 1 mg/kg/dosis en 2-16 años (off-label)


### 33. Lactulosa (`lactulosa`)

#### Discrepancia: Equivalencia g → ml en niños de 7 a 14 años
- **Cifra / criterio mostrado en la app:** `10 g = 15 ml con la solución de 667 mg/ml (la calculadora convierte por concentración)`
- **Fundamento clínico adoptado:** Error de conversión en Pediamécum: con 667 mg/ml, 10 g son ≈15 ml, no 20 ml. No se copia ningún «ml» de las fichas.
- **Valores por fuente contrastada:**
  - **CIMA-LACTULOSA:** 10 g (correspondiente a 15 ml/día de solución oral) (CIMA, solución de 667 mg/ml)
  - **PEDIAMECUM-LACTULOSA:** 10 g/día (20 ml/día) (Pediamécum)


### 34. Levonorgestrel (anticoncepción de emergencia) (`levonorgestrel`)

#### Discrepancia: Uso en adolescentes
- **Cifra / criterio mostrado en la app:** `Solo pauta de adulto (sin dosis pediátrica)`
- **Fundamento clínico adoptado:** Decisión del proyecto: anticoncepción de emergencia solo con la pauta de adulto.
- **Valores por fuente contrastada:**
  - **CIMA-LEVONORGESTREL:** No adecuado en niñas en edad prepuberal (CIMA)
  - **PEDIAMECUM-LEVONORGESTREL:** Autorizado en mayores de 16 años; no recomendado en menores de 16 (off-label) (Pediamécum)


### 35. Levotiroxina sódica (`levotiroxina`)

#### Discrepancia: Unidad de la dosis pediátrica de mantenimiento
- **Cifra / criterio mostrado en la app:** `Se muestran ambas tablas como texto; no se calcula`
- **Fundamento clínico adoptado:** Las dos fuentes usan unidades distintas: no son comparables cifra a cifra.
- **Valores por fuente contrastada:**
  - **CIMA-LEVOTIROXINA:** Por superficie corporal (por m²) e inicio en µg/día (CIMA)
  - **PEDIAMECUM-LEVOTIROXINA:** Por kg y edad, con equivalente en µg/día (Pediamécum)


### 36. Mebendazol (`mebendazol`)

#### Discrepancia: Población: menores de 2 años
- **Cifra / criterio mostrado en la app:** `No se carga dosis para menores de dos años`
- **Fundamento clínico adoptado:** Ninguna fuente da una posología para menores de 2 años.
- **Valores por fuente contrastada:**
  - **CIMA-MEBENDAZOL-51200:** CIMA: no establecida en menores de 2 años y no se puede hacer una recomendación posológica; no usar en menores de 1 año
  - **PEDIAMECUM-MEBENDAZOL:** Pediamécum: en menores de 2 años solo cuando la parasitosis interfiera significativamente con el estado nutricional y el desarrollo


### 37. Meloxicam (`meloxicam`)

#### Discrepancia: Población pediátrica
- **Cifra / criterio mostrado en la app:** `No se carga la pauta de artritis idiopática juvenil; solo la de adolescentes de dieciséis años o más`
- **Fundamento clínico adoptado:** Donde la ficha técnica dice «contraindicado» no se carga dosis (regla de datos 4). El «>50 kg» de Pediamécum no habilita a menores de 16 años.
- **Valores por fuente contrastada:**
  - **CIMA-MELOXICAM:** CIMA: contraindicado en niños y adolescentes menores de 16 años (4.2 y 4.3)
  - **PEDIAMECUM-MELOXICAM:** Pediamécum: artritis idiopática juvenil 0,125 mg/kg una vez al día, dosis máxima 7,5 mg/día (off-label; FDA desde 2 años)


### 38. Metamizol (dipirona) (`metamizol`)

#### Discrepancia: Tope diario del adulto
- **Cifra / criterio mostrado en la app:** `3450 mg/día`
- **Fundamento clínico adoptado:** Misma sal (la cápsula Metamizol Cinfa 575 mg es metamizol magnésico) y misma población (≥15 años, >53 kg): se aplica la regla del tope más bajo y se muestran 3450 mg/día. En CIMA, los 4000 mg/día corresponden al uso oral de la ampolla en el dolor oncológico (media ampolla hasta 4 veces al día, máximo 7 días): otra presentación e indicación.
- **Valores por fuente contrastada:**
  - **CIMA-METAMIZOL:** 3450 mg/día: cápsulas de 575 mg, adultos y adolescentes ≥15 años (>53 kg) (CIMA); Pediamécum da el mismo máximo para esta población
  - **PEDIAMECUM-METAMIZOL:** 4000 mg/día: "En general, la dosis oral máxima de metamizol magnésico es de 4000 mg/día" (Pediamécum)


### 39. Metoclopramida (`metoclopramida`)

#### Discrepancia: Vía de la pauta pediátrica en Pediamécum
- **Cifra / criterio mostrado en la app:** `Se muestra la pauta oral de la ficha técnica`
- **Fundamento clínico adoptado:** Pediamécum no trae una pauta oral propia: no se usa como fuente de dosis, por lo que la ficha queda con una sola institución.
- **Valores por fuente contrastada:**
  - **CIMA-METOCLOPRAMIDA-69266:** Pauta oral de la ficha: 0,1-0,15 mg/kg hasta tres veces al día, máximo 0,5 mg/kg/24 h
  - **PEDIAMECUM-METOCLOPRAMIDA:** La misma pauta descrita para la vía intravenosa; la nota de seguridad de la AEMPS limita a 0,5 mg/kg/24 h y 5 días


### 40. Metronidazol (`metronidazol`)

#### Discrepancia: Infecciones por anaerobios en niños: frecuencia y tope
- **Cifra / criterio mostrado en la app:** `22,5 mg/kg/día (7,5 mg/kg cada 8 horas)`
- **Fundamento clínico adoptado:** Mismo régimen y población: se muestra la pauta de la ficha (cada 8 h), la más baja. 4 g/día (Pediamécum) es el único tope del régimen; con 7,5 mg/kg cada 8 h solo se alcanzaría con unos 178 kg, así que nunca se alcanza antes que la dosis de adulto. El tope de 2400 mg/día de CIMA es de la amebiasis.
- **Valores por fuente contrastada:**
  - **CIMA-METRONIDAZOL-62223:** 22,5 mg/kg/día: 7,5 mg/kg cada 8 h (dosis diaria 20-30 mg/kg, hasta 40 según gravedad), sin tope en mg (CIMA)
  - **PEDIAMECUM-METRONIDAZOL:** 30 mg/kg/día divididos cada 6 h, máximo 4 g/día (Pediamécum, lactantes y niños)

#### Discrepancia: Giardiasis en niños
- **Cifra / criterio mostrado en la app:** `15 mg/kg/día`
- **Fundamento clínico adoptado:** Mismo régimen y población: se muestra la cifra más baja, con el tope de Pediamécum.
- **Valores por fuente contrastada:**
  - **CIMA-METRONIDAZOL-62223:** 40 mg/kg/día como extremo superior de "15 a 40 mg/kg por día divididos en 2-3 dosis", sin tope en mg (CIMA)
  - **PEDIAMECUM-METRONIDAZOL:** 15 mg/kg/día cada 8 h, máximo 500 mg/día (Pediamécum)

#### Discrepancia: Amebiasis en niños
- **Cifra / criterio mostrado en la app:** `35-50 mg/kg/día, máximo 2400 mg/día`
- **Fundamento clínico adoptado:** Se muestra la pauta de la ficha (rango inferior más bajo y con tope).
- **Valores por fuente contrastada:**
  - **CIMA-METRONIDAZOL-47656:** 35-50 mg/kg/día en 3 dosis, sin exceder 2400 mg/día (CIMA)
  - **PEDIAMECUM-METRONIDAZOL:** 40-50 mg/kg/día cada 6-8 h durante 10 días, sin tope (Pediamécum)


### 41. Morfina (`morfina`)

#### Discrepancia: Concentración de las gotas orales
- **Cifra / criterio mostrado en la app:** `Solo se carga la concentración del arsenal chileno como presentación; elegir siempre la concentración del frasco`
- **Fundamento clínico adoptado:** Riesgo de error de concentración (doble). Dropizol no se carga como presentación porque es antidiarreico y ninguna dosis de la ficha la usa.
- **Valores por fuente contrastada:**
  - **CIMA-MORFINA-83323:** Dropizol (CIMA): 10 mg/ml
  - **ARSENAL-APS-ATACAMA:** Arsenal de APS de Atacama: solución para gotas orales 20 mg/mL

#### Discrepancia: Población de las gotas
- **Cifra / criterio mostrado en la app:** `Se muestra la tabla por edad de Pediamécum para liberación normal; Dropizol no se usa como pauta analgésica`
- **Fundamento clínico adoptado:** La restricción de edad de Dropizol corresponde a otra indicación (antidiarreico), no al uso analgésico.
- **Valores por fuente contrastada:**
  - **CIMA-MORFINA-83323:** Dropizol (CIMA): no usar en menores de 18 años; indicado solo en diarrea aguda del adulto
  - **PEDIAMECUM-MORFINA:** Pediamécum: formas orales de liberación normal desde 1 año (dolor)


### 42. Nistatina (`nistatina`)

#### Discrepancia: Recién nacidos
- **Cifra / criterio mostrado en la app:** `No se cargan dosis neonatales (fuera del alcance de esta versión)`
- **Fundamento clínico adoptado:** Diferencia solo en el recién nacido a término; en lactantes, niños y adultos las fuentes coinciden.
- **Valores por fuente contrastada:**
  - **CIMA-NISTATINA:** CIMA: recién nacidos y lactantes con bajo peso al nacer, 100.000 UI (1 ml) cada 6 horas
  - **PEDIAMECUM-NISTATINA:** Pediamécum: neonatos a término 200.000 UI (2 ml) cada 6 horas; pretérmino 100.000 UI (1 ml) cada 6 horas


### 43. Omeprazol (`omeprazol`)

#### Discrepancia: Ficha CIMA cargada
- **Cifra / criterio mostrado en la app:** `Se muestra la dosis de venta libre para adultos y las pautas pediátricas de Pediamécum`
- **Fundamento clínico adoptado:** No hay ficha de prescripción para adultos en las fuentes: la úlcera, la esofagitis del adulto y la erradicación de H. pylori en adultos no tienen dosis cargada.
- **Valores por fuente contrastada:**
  - **CIMA-OMEPRAZOL:** Gastromel es de venta libre: solo cubre el ardor y la regurgitación en adultos, 20 mg/día durante 14 días
  - **PEDIAMECUM-OMEPRAZOL:** Indicaciones pediátricas autorizadas (esofagitis, ERGE y H. pylori) con pautas por peso


### 44. Paracetamol (acetaminofén) (`paracetamol`)

#### Discrepancia: Tope diario según régimen
- **Cifra / criterio mostrado en la app:** `Cada régimen se muestra con su propio tope`
- **Fundamento clínico adoptado:** Los dos topes pertenecen a regímenes distintos (dosis por toma y población diferentes); no son un conflicto numérico.
- **Valores por fuente contrastada:**
  - **CIMA-PARACETAMOL-85780:** Antidol 1 g, adultos y adolescentes >16 años o >50 kg, 1 g cada 6-8 h: máximo 3 g/24 h (CIMA)
  - **PEDIAMECUM-PARACETAMOL:** >43 kg (adolescentes >13 años), 650 mg cada 4-6 h: máximo 2600 mg/24 h (Pediamécum)


### 45. Sulfato ferroso (`sulfato-ferroso`)

#### Discrepancia: Presentaciones retard en pediatría
- **Cifra / criterio mostrado en la app:** `Dosificación en hierro elemental con gotas orales en <28 kg`
- **Fundamento clínico adoptado:** Los comprimidos retard contienen dosis altas (80-105 mg Fe) no fraccionables; en lactantes y niños <28 kg debe emplearse estrictamente la formulación en gotas.
- **Valores por fuente contrastada:**
  - **CIMA-SULFATO-FERROSO-52994:** Contraindicado en niños con peso inferior a 28 kg (aproximadamente menores de 9-10 años)
  - **PEDIAMECUM-SULFATO-FERROSO:** Dosis pediátricas calculadas en mg de hierro elemental desde el periodo neonatal


### 46. Terbinafina (`terbinafina`)

#### Discrepancia: Población pediátrica
- **Cifra / criterio mostrado en la app:** `Se muestran las pautas pediátricas de Pediamécum, marcadas como uso fuera de ficha técnica (off-label)`
- **Fundamento clínico adoptado:** Contradicción de población, no de cifra: la ficha técnica no respalda el uso en niños.
- **Valores por fuente contrastada:**
  - **CIMA-TERBINAFINA:** CIMA: "La experiencia con Lamisil comprimidos en niños es limitada y por consiguiente su utilización no puede ser recomendada"
  - **PEDIAMECUM-TERBINAFINA:** Pediamécum: pautas por peso en tinea capitis (niños >4 años) y onicomicosis, uso off-label


### 47. Trimebutino (trimebutina) (`trimebutino`)

#### Discrepancia: Dosis de adultos y >12 años (síndrome del colon irritable)
- **Cifra / criterio mostrado en la app:** `No se carga dosis de adulto`
- **Fundamento clínico adoptado:** Inconsistencia interna de la única fuente disponible; sin ficha técnica ni fuente chilena que la resuelva.
- **Valores por fuente contrastada:**
  - **PEDIAMECUM-TRIMEBUTINO:** 300-400 mg/día de inicio y luego 200 mg/día (Pediamécum)
  - **PEDIAMECUM-TRIMEBUTINO:** 200 mg cada 8 h, es decir 600 mg/día, en la frase siguiente de la misma ficha (Pediamécum)

---

## 4. Preguntas Abiertas para Héctor Salvo Agüero (Spec §14)

1. **Unidades de Hierro y Levotiroxina (Ficha vs Calculadora):**
   - **Hierro (Sulfato ferroso):** Las dosis pediátricas y de prevención se expresan estrictamente en **mg de hierro elemental (Fe²⁺)**. La calculadora calcula sobre los 80 mg o 105 mg de hierro elemental de los comprimidos retard o las gotas. ¿Debe incluirse un banner prominente de advertencia dentro de la misma calculadora además de la ficha?
   - **Levotiroxina:** Las dosis pediátricas se expresan en **µg/kg/día** según tramos de edad. La calculadora requiere conversión a microgramos (µg). ¿Se prefiere mantener como tabla por edad o habilitar cálculo numérico continuo?

2. **Registro Sanitario ISP Chile:**
   - Actualmente todas las presentaciones orales se encuentran etiquetadas como `registroChile: "sin_verificar"`.
   - Se completaron 30 de 80 consultas preliminares debido a bloqueos de IP del portal del ISP.
   - Decisión pendiente: completar la verificación cuando se disponga de conexión con IP residencial o rotativa.

3. **Revisión y Firma de Fichas:**
   - En conformidad con la directriz previa, el campo `meta.revisadoPor` se mantiene vacío en las 79 fichas (ninguna ficha queda firmada).
   - ¿Se autoriza la publicación en la rama `main` bajo la leyenda de formación y uso pedagógico?

---

## 5. Verificación Técnica y Estado de la Suite

- **Fichas EV (Urgencia/Prehospitalario):** 89 fichas validadas, 137 fuentes (intactas).
- **Fichas Orales (APS):** 79 fichas validadas, 177 fuentes orales.
- **Pruebas unitarias:** 403 pruebas pasando con éxito en Vitest (0 fallos).
- **Reglas cubiertas:** Invariantes de los 15 ids de fuente única, 13 solo adulto, 6 de alto riesgo, validación cruzada de concentraciones líquidas y conversión exacta de lactulosa y morfina.
