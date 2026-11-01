# Oftalmología (pabellón + orales + colirios): documento de diseño

- **Fecha:** 1-nov-2026
- **Rama:** `oftalmologia-v1`
- **Antecedentes:**
  - `datos/crudos/oftalmo/DECISIONES.md`: alcance del 31-oct y las 5 decisiones del 1-nov.
  - `informes/oftalmologia-fase0.md`: hallazgos de la Fase 0.
  - `datos/crudos/oftalmo/COBERTURA.md`: registro ISP y fuentes por candidato.
  - `docs/superpowers/specs/2026-10-31-topicos-design.md`: el patrón que se replica.
- **Material de formación, no de prescripción.** Todo lo de pabellón lleva «verifica el protocolo de tu pabellón».

## 1. Propósito

Agregar a Dilución EV un centro **Oftalmología** para el equipo de pabellón oftalmológico en formación: pabelloneras, arsenaleras, técnicos de anestesia y TENS. Va en línea con el Aula Pabellón. Reúne en un solo lugar:

1. **Pabellón:** medicamentos intraoculares y perioculares, con la dosis final, los pasos de preparación **solo si una fuente publicada los trae** y un **verificador** que compara la concentración que preparó el usuario con la citada.
2. **Orales** de uso oftalmológico, que viven en la sección Orales con una marca.
3. **Colirios:** las fichas de Tópicos con la vía ojo, que ya están publicadas.

## 2. Alcance

### Incluye

**Pabellón: 41 fichas nuevas** (`datos/crudos/oftalmo/candidatos.json`, menos los orales)

| Familia | Fichas | Modo |
|---|---|---|
| Intracamerales (13) | carbacol, acetilcolina, cefuroxima, moxifloxacino, adrenalina, lidocaína, fenilefrina+tropicamida+lidocaína (Mydrane), fenilefrina+ketorolaco (Omidria), azul tripano, alteplasa, triamcinolona, verde de indocianina, azul brillante | `intraocular` |
| Intravítreos (16) | bevacizumab, ranibizumab, aflibercept, faricimab, brolucizumab, implante de dexametasona, vancomicina, ceftazidima, amikacina, anfotericina B, voriconazol, ganciclovir, foscarnet, clindamicina, metotrexato, ocriplasmina | `intraocular` |
| Bloqueos (4) | bupivacaína, ropivacaína, mepivacaína, hialuronidasa | `informativa` |
| Subconjuntivales y subtenonianos (5) | cefazolina, gentamicina, metilprednisolona, betametasona, dexametasona | `informativa` |
| Antifibróticos y toxina (3) | mitomicina C, fluorouracilo, toxina botulínica | `intraocular`, alto riesgo, «según el protocolo del cirujano» |

- Lidocaína y triamcinolona tienen usos en dos familias. Van en **una sola ficha** con dosis de varias vías.

**Sin registro en Chile, se muestran con aviso (decisión 1):**
- **Pabellón (9):** carbacol, acetilcolina, Omidria, azul tripano, azul brillante, brolucizumab, anfotericina B, ocriplasmina y ropivacaína.
- **Orales (2):** metazolamida y famciclovir.
- Cada una lleva la etiqueta «No registrado en Chile (puede usarse por importación o uso compasivo)» y su ficha FDA o CIMA como fuente.

**Orales: 11 en total**
- **Ya existen (4) y se marcan:** aciclovir, azitromicina, prednisona y cotrimoxazol. Se les agregan las pautas oftálmicas con su guía (AAO, HEDS, TFOS, CDC).
- **Nuevos (7):** acetazolamida, valaciclovir, doxiciclina, minociclina, pirimetamina, metazolamida (`no_registrado`) y famciclovir (`no_registrado`).

**Colirios:** no hay datos nuevos. Es la lista de Tópicos filtrada por `vias` ∋ `ojo`.

### No incluye (v1)

- Orales con evidencia débil (decisión 4): ácido tranexámico en el hipema, ivermectina en el Demodex y glicerol oral.
- Isosorbida: en Chile solo existe el nitrato.
- Cálculo de dosis por peso en pabellón. Las dosis intraoculares son fijas por ojo; la excepción pediátrica (Lucentis 0,2 mg en ROP) va como dosis aparte, no se calcula.
- Proponer preparaciones. El verificador **solo compara**, nunca sugiere pasos.

## 3. Decisiones de diseño

1. **Sección independiente, como Tópicos:**
   - Datos en `datos/oftalmo/*.yaml` y `datos/fuentes-oftalmo.yaml`.
   - Esquema `FichaOcular`, validador `validarOculares` y cargador `cargarOculares`.
   - Rutas `/oftalmologia…` y UI con carga diferida (lazy).
2. **Reglas heredadas de Tópicos:**
   - Una ficha con una sola fuente lleva el aviso de fuente única.
   - Las dosis quedan atadas a la presentación chilena.
   - Si no hay fuente, la ficha queda sin pauta.
   - Lo off-label va marcado.
   - **Contrastada** = al menos una dosis con `tambien` de una institución distinta.
3. **Regla de pabellón (31-oct):** muchos usos intraoculares son off-label por naturaleza (bevacizumab, alteplasa, moxifloxacino, vancomicina). Se muestran con la etiqueta off-label y su fuente, **nunca sin fuente**. Todas las fichas de pabellón llevan `altoRiesgo: true`.
4. **Pasos solo citados:**
   - Un protocolo de preparación existe solo si la fuente trae los pasos (PNT SEFH, ficha técnica, EyeWiki/AAO, Arshinoff).
   - Si la fuente trae solo la dosis final (amikacina, anfotericina, clindamicina, foscarnet, metotrexato, mitomicina), `protocolos` va vacío y la ficha dice «La fuente no publica pasos de preparación; usa el protocolo de tu pabellón». El verificador funciona igual: compara la concentración.
5. **Moxifloxacino (decisión 2):**
   - Dos protocolos citados: ASCRS 0,5 mg/0,1 ml y Arshinoff 150 µg/0,1 ml (3 ml de Vigamox + 7 ml de BSS).
   - Se muestra el rango publicado, 150–500 µg/0,1 ml.
   - El verificador da verde si calza con **cualquiera** de los dos.
   - Lleva una discrepancia registrada que explica que los 160 µg/0,1 ml del consenso son intravítreos.
6. **Fichas `informativa`** (bloqueos y subconjuntivales, decisión 3):
   - Muestran los volúmenes y las concentraciones como texto citado.
   - **No tienen verificador** ni botón «Verificar».
7. **Antifibróticos y toxina (decisión 5):**
   - Llevan el aviso fijo «La dosis y el tiempo de aplicación los define el cirujano».
   - La toxina usa la unidad `U` (unidades del fabricante, no intercambiables entre marcas) y lo dice en una alerta.
8. **Orales sin duplicar:**
   - `FichaOral` gana el campo opcional `usos?: ['oftalmologia']`.
   - `DosisOral` gana `oftalmica?: true`, que marca las pautas oftálmicas dentro de una ficha general (p. ej., aciclovir 400 mg c/12 h de profilaxis HEDS).
   - La pestaña Orales del centro lista las fichas con `usos` ∋ `oftalmologia` y enlaza a `/orales/m/:id`.
9. **Datos generados con Python**, como en Tópicos:
   - Los scripts son `scripts/generar-oftalmo.py` y `scripts/oftalmo/lote1..N.py`.
   - El generador verifica que cada presentación cite un registro ISP vigente o lleve `registroChile: no_registrado`.
10. **Favoritos y recientes** van en las mismas claves de siempre, con el prefijo `oft:`.

## 4. Modelo de datos: `FichaOcular` (`src/esquema/ficha-ocular.ts`)

| Campo | Tipo | Notas |
|---|---|---|
| `id` | slug | igual al nombre del archivo |
| `nombre`, `comerciales[]`, `grupo` | texto | `grupo` con etiqueta en `etiquetas.ts` (anestesico-local, antibiotico, antifungico, antiviral, anti-vegf, corticoide, midriatico, miotico, colorante, fibrinolitico, enzima, antifibrotico, toxina) |
| `familias[]` | `intracameral \| intravitreo \| bloqueo \| periocular \| antifibrotico` | ≥1 |
| `modo` | `intraocular \| informativa` | `informativa` = sin verificador |
| `componentes[]` | texto | vacío si es monofármaco |
| `altoRiesgo` | `true` | siempre en pabellón |
| `registroChile` | `verificado \| no_registrado` | igual que en orales; `no_registrado` muestra el aviso |
| `presentaciones[]` | `{id, forma, cantidad: {valor, unidad}, volumenMl?, registrosIsp[], usoDirecto, sinConservantes?, nota?, fuente}` | `forma`: polvo, solucion, suspension, implante, jeringa_precargada. `usoDirecto: true` = ya viene a la concentración de uso (Lucentis, Eylia, Vabysmo, Ozurdex, Mydrane) |
| `dosis[]` | `{indicacion, via, poblacion, final: {cantidad: {valor, unidad} \| {min, max, unidad}, volumenMl}, texto, estatus, condicion?, presentaciones?[], fuente, tambien?[]}` | `via`: intracameral, intravitrea, subconjuntival, subtenoniana, retrobulbar, peribulbar, intralesional, topica_intraoperatoria. `final` es obligatorio en `modo: intraocular`; en `informativa` es opcional y no se verifica |
| `protocolos[]` | `{id, dosis: indice, titulo, partida: presentacionId, pasos: Paso[], resultado: {valor, unidad, volumenMl}, fuente}` | vacío si la fuente no trae pasos |
| `Paso` | `{tipo: 'reconstituir', diluyente, volumenMl} \| {tipo: 'diluir', tomarMl, llevarAMl, diluyente} \| {tipo: 'cargar', volumenMl} \| {tipo: 'texto', texto}` | `texto` para indicaciones sin cifra («usar de inmediato») |
| `sinPauta` | `null \| {motivo}` | si no es null, `dosis` va vacío |
| `pediatria` | `{estado, motivo}` | igual que en Tópicos |
| `conservacion[]` | `{texto, horas?, fuente}` | estabilidad tras preparar |
| `contraindicaciones[]`, `alertas[]` | texto | p. ej., HORV con vancomicina intracameral; eliminar el exceso de la jeringa |
| `discrepancias[]` | igual que en orales | |
| `meta` | `{revisadoPor?, fechaRevision?}` | |

`UnidadOcular` = `mg | mcg | UI | U`.

**Reglas de coherencia del esquema:**
- `modo: intraocular` sin `sinPauta` exige al menos una dosis con `final`.
- Cada `protocolos[].dosis` apunta a una dosis existente, y `partida` a una presentación existente.
- `protocolos[].resultado` debe coincidir con `dosis.final` (±5 %). **El dato se valida contra su propia fuente.**
- `usoDirecto: true` exige `volumenMl`.
- `registroChile: verificado` exige `registrosIsp` no vacío en alguna presentación.
- Las reglas de pediatría y `sinPauta` son las de Tópicos.

`validarOculares` valida además que las fuentes existan (incluidos `tambien` y `discrepancias`) y que los ids no se repitan.

## 5. Verificador: `src/calculos/verificadorOcular.ts`

Es una función pura.

```
verificar({ presentacion, pasos: PasoNumerico[], dosisObjetivo: DosisFinal[] })
  → { ok: true, concentracion: {porMl, por01ml, unidad}, volumenDisponibleMl, comparaciones: [{dosis, estado: 'coincide'|'no_coincide', diferenciaPct}] }
  | { ok: false, error }
```

- **Partida:** la masa de la presentación (p. ej., 750 mg). Si la presentación es una solución, su concentración en mg/ml.
- **Reconstituir V ml:** la concentración pasa a masa ÷ V.
  - Supuesto declarado: el volumen final es igual al volumen de diluyente; no se corrige por el desplazamiento del polvo.
  - Si la ficha técnica da otro volumen final, el protocolo citado lo usa como dato.
- **Diluir: tomar Y ml y llevar a Z ml:** la concentración se multiplica por Y ÷ Z.
  - Error si Y es mayor que el volumen disponible, si Z < Y o si algún valor es ≤ 0.
  - Se permiten hasta 4 pasos.
- **Comparación:** la concentración por 0,1 ml (o por el `volumenMl` de la dosis) se compara con cada dosis objetivo.
  - Dosis puntual: «coincide» si |diferencia| ≤ 5 %.
  - Dosis con rango: «coincide» si cae dentro de [min, max].
  - Moxifloxacino tiene dos dosis objetivo y basta con que calce una.
- **UI:**
  - **Verde:** «Coincide con [fuente]».
  - **Roja:** «NO coincide: obtuviste X; la fuente dice Y. No administres; revisa los pasos».
  - Siempre va el aviso «verifica el protocolo de tu pabellón».
  - El verificador **no muestra cómo corregir**.
- **No aparece** en las fichas `informativa` ni cuando todas las presentaciones son `usoDirecto`. En ese caso la ficha muestra «Viene lista para usar: carga X ml y elimina el exceso» si la fuente lo dice.
- **Caso de oro (PNT SEFH):** cefuroxima 750 mg + 7,5 ml → 100 mg/ml; tomar 1 ml y llevar a 10 ml → 10 mg/ml, o sea **1 mg/0,1 ml**, que coincide.

## 6. Interfaz

- **Rutas:**
  - `/oftalmologia`: centro con las pestañas Pabellón · Orales · Colirios.
  - `/oftalmologia/m/:id`: ficha.
  - `/oftalmologia/m/:id/verificar`: verificador.
  - Se agrega el enlace «Oftalmología» en la navegación.
- **Pabellón:**
  - Buscador por nombre y comerciales.
  - Agrupado por familia (intracameral, intravítreo, bloqueos, perioculares, antifibróticos y toxina).
  - Favoritos y recientes.
  - Etiquetas: alto riesgo, off-label, no registrado en Chile, una sola fuente, sin pasos publicados.
- **Ficha:**
  - Pestañas Dosis · Preparación · Conservación · Alertas · Discrepancias · Fuentes.
  - Cada dosis muestra la vía, la dosis final por volumen y el estatus.
  - «Preparación» muestra los protocolos paso a paso con su fuente, o el aviso de que no hay pasos publicados.
  - El botón «Verificar mi preparación» aparece según §5.
- **Orales:** la lista de fichas marcadas. Al abrir una se va a la ficha oral y las pautas `oftalmica` se resaltan con la etiqueta «Oftalmología».
- **Colirios:** la lista de Tópicos con vía ojo, que enlaza a `/topicos/m/:id`.
- **Acerca:** un párrafo nuevo con el propósito, la regla de pasos citados, el verificador y sus límites.

## 7. Pruebas

- **Esquema y validador:** casos válidos e inválidos, en especial `protocolo.resultado ≠ dosis.final`, protocolo con dosis o partida inexistente, `verificado` sin registros ISP e `informativa` con verificador.
- **Verificador:**
  - El caso de oro de la cefuroxima.
  - Arshinoff (3 ml de Vigamox 5 mg/ml + 7 ml → 1,5 mg/ml = 150 µg/0,1 ml).
  - Dosis con rango (alteplasa).
  - Moxifloxacino con dos objetivos.
  - Errores: tomar más de lo disponible, Z < Y, ceros.
  - Conversión de unidades mg↔mcg.
- **Datos reales:**
  - 41 fichas de pabellón sin errores, con el conteo por familia de §2.
  - Las 9 sin registro marcadas.
  - Cada protocolo cuadra con su dosis.
  - 11 orales con `usos: oftalmologia`.
  - Todos los grupos con etiqueta.
- **UI:**
  - Las 3 pestañas.
  - La ficha intraocular con verificador, la `informativa` sin él y la de uso directo.
  - Las alertas verde y roja.
  - Las etiquetas de no registrado y off-label.

## 8. Riesgos y verificaciones previas a los datos

- **De memoria de los agentes (no citar hasta cotejar):** los autores del PPP de cierre angular (AAO), la conversión de metilprednisolona del ONTT y el posible «withdrawn» del estudio ZEDS.
- **Citas de WebFetch recortadas** (~125 caracteres): se cotejan con el original al escribir cada lote.
- **Ceftazidima:** 2 mg/0,1 ml (SEFH) frente a 2,25 mg (borrador). Se registra como discrepancia y se muestra lo que dice la SEFH.
- **Frasco de partida de adrenalina y lidocaína:** se elige a mano (ampolla de 1 mg/ml; lidocaína al 1–2 % sin conservantes) porque el filtro del ISP se cuela con productos dentales.
- **El supuesto de reconstitución sin desplazamiento** se rotula en la UI.
- **Un verde no garantiza nada:** solo dice que la cuenta calza con la fuente; la preparación real puede fallar. Lo dice el aviso.
- **Las fuentes son españolas y de EE. UU.:** las marcas o los frascos pueden no calzar con Chile. Por eso las presentaciones van atadas al ISP.
- **Revisión clínica pendiente**, como en Tópicos: lo ideal es la enfermera de oftalmología del Aula Pabellón.
