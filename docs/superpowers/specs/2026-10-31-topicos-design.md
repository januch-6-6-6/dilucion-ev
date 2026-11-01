# Tópicos ojo/oído/nariz — Documento de diseño

- **Fecha:** 31-oct-2026
- **Rama:** `topicos-v1`
- **Antecedentes:** `datos/crudos/topicos/DECISIONES.md` (alcance y reglas), `informes/topicos-discrepancias.md` (revisión de las 80) y `docs/superpowers/specs/2026-10-05-orales-design.md` (el patrón que se replica).
- **Material de formación, no de prescripción.**

## 1. Propósito

Agregar a Dilución EV una tercera sección, **Tópicos**, con los colirios, ungüentos oftálmicos, gotas óticas y sprays o gotas nasales registrados en el ISP. Cada ficha muestra qué concentraciones hay en Chile, la pauta que respalda una fuente de la misma concentración y forma, las alertas y el tiempo que dura el envase abierto. También trae una calculadora de **duración del envase**.

## 2. Alcance

- **Incluye:** 80 moléculas o combinaciones (`lista-isp.json`), con las vías ojo, oído y nariz.
- **No incluye:** tópicos de piel, vaginales o rectales; calcitonina, desmopresina y esketamina nasales (son sistémicas); Mentholatum. Tampoco cálculo de dosis por peso: en tópicos no aplica.

## 3. Decisiones de diseño

1. La sección es independiente, como orales: sus propios datos (`datos/topicos/*.yaml`, `datos/fuentes-topicos.yaml`), esquema, cargador y rutas `/topicos…`. La UI se carga de forma diferida (lazy).
2. Las 4 reglas de Héctor del 31-oct (en `DECISIONES.md`): fuente única con aviso, atadas a la concentración chilena, combinaciones sin fuente → sin pauta, y pediatría de Pediamécum como off-label.
3. **Contrastada** = al menos una dosis tiene una fuente en `tambien` de una institución distinta a la de su `fuente`. Sin eso, la ficha lleva el aviso de fuente única. Las fichas sin pauta llevan su propio aviso y no el de fuente única.
4. Los datos se generan con Python (`scripts/generar-topicos.py` + `scripts/topicos/lote1..4.py`). El generador verifica que las presentaciones cubran exactamente los registros ISP de la molécula y que la forma coincida con el nombre del registro.
5. Favoritos y recientes se guardan en las mismas claves que EV y orales, con el prefijo `top:`.

## 4. Modelo de datos: `FichaTopica` (`src/esquema/ficha-topica.ts`)

| Campo | Tipo | Notas |
|---|---|---|
| `id` | slug | igual al nombre del archivo |
| `nombre`, `comerciales[]`, `grupo` | texto | el grupo debe tener etiqueta en `etiquetas.ts` |
| `vias[]` | `ojo \| oido \| nariz` | ≥1 |
| `componentes[]` | texto | vacío si es monofármaco |
| `altoRiesgo` | bool | |
| `presentaciones[]` | `{id, forma, via, concentracion, registrosIsp[], unidosis?, sinConservantes?, nota?, fuente}` | `forma`: solucion, suspension, emulsion, unguento, gel, spray |
| `dosis[]` | `{indicacion, poblacion, texto, cantidad?, unidad?, vecesAlDia?, porSitio?, duracion?, estatus, condicion?, presentaciones?[], fuente, tambien?[]}` | `unidad`: gota, cm, pulverizacion, aplicacion; `porSitio`: ojo, oido, fosa |
| `sinPauta` | `null \| {motivo}` | si no es null, `dosis` debe ir vacío |
| `pediatria` | `{estado, motivo, edadMinima?}` | `estado`: con_dosis, no_establecida, contraindicada, sin_datos |
| `conservacion[]` | `{presentaciones?[], validezAbiertoDias?, texto, fuente}` | |
| `administracion` | `null \| {texto, fuente}` | |
| `contraindicaciones[]`, `alertas[]` | texto | |
| `discrepancias[]` | igual que en orales | |
| `meta` | `{revisadoPor?, fechaRevision?}` | |

Reglas de coherencia del esquema:

- `con_dosis` exige al menos una dosis pediátrica.
- `contraindicada` prohíbe las dosis pediátricas.
- Cada id en `dosis.presentaciones` y `conservacion.presentaciones` debe existir en la ficha.
- Con `sinPauta`, las dosis van vacías; sin `sinPauta`, debe haber al menos una dosis.
- `cantidad` exige `unidad`. `vecesAlDia` puede ir solo (p. ej., mupirocina: «pequeña cantidad 2–3 veces al día»); en ese caso la dosis no es calculable.

`validarTopicos` (`src/esquema/validar-topicos.ts`) valida además: fuentes que existen (incluye `tambien` y `discrepancias.valores[].fuente`), ids sin repetir y la vía de la presentación incluida en `vias`.

## 5. Calculadora: `src/calculos/duracionEnvase.ts`

Entradas: la presentación, la dosis (cantidad, unidad, veces al día), los sitios (1 o 2 ojos, oídos o fosas) y el contenido del envase. El contenido es en ml para gotas o en pulverizaciones para sprays, y el usuario lo ingresa porque el ISP no lo informa. Para gotas también se usa `gotasPorMl`, editable, con 20 por defecto como supuesto declarado.

- Unidades totales = ml × gotas/ml, o pulverizaciones por envase.
- Consumo diario = cantidad × veces al día × sitios.
- Días por contenido = ⌊total ÷ consumo⌋.
- Días efectivos = mín(días por contenido, validez tras abrir); se informa cuál de los dos limita.
- **No aplica** a ungüentos o pomadas (`unidad = cm`), a unidosis (se descarta cada envase) ni a dosis sin `vecesAlDia`. En esos casos la UI explica por qué no se calcula.

## 6. Interfaz

- Rutas: `/topicos` (lista), `/topicos/m/:id` (ficha) y `/topicos/m/:id/calcular`. Hay un enlace «Tópicos» en la navegación.
- La lista tiene buscador (nombre y comerciales), favoritos, recientes y grupos. Etiquetas: alto riesgo, una sola fuente y sin pauta.
- La ficha tiene las pestañas Dosis · Presentaciones · Conservación · Administración · Discrepancias · Fuentes. Cada pauta muestra la etiqueta autorizada u off-label, las concentraciones a las que aplica y la segunda fuente concordante cuando la hay.
- El botón «Calculadora» solo aparece si alguna dosis es calculable.
- «Acerca» explica la sección, la regla de concentración y las fuentes.

## 7. Pruebas

- Esquema y validador: casos válidos e inválidos.
- `duracionEnvase`: gotas, spray, el tope por validez, los casos que no aplican y las entradas inválidas.
- Datos reales: 80 fichas, ninguna con errores, las 16 sin pauta, las 13 contrastadas y los grupos con etiqueta.
- UI: la lista, la ficha (aviso de fuente única o sin pauta, off-label) y la calculadora.

## 8. Riesgos

- La gota estándar (20 gotas/ml) es un supuesto. Se rotula así y se puede editar.
- El volumen del envase es un dato del usuario. Si se equivoca, la duración sale mal.
- Una ficha de una sola fuente puede estar desactualizada. Por eso lleva aviso y el enlace a la fuente.
