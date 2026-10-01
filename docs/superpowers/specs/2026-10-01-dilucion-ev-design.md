# Dilución EV — Documento de diseño

**Fecha:** 2026-10-01
**Autor:** Héctor Salvo Agüero (TENS, 13 años en urgencias, SAMU y pabellón; Ingeniero en Informática)
**Estado:** borrador para revisión

## 1. Propósito

Aplicación de referencia y formación para preparar y administrar medicamentos
endovenosos (EV) usados en Chile: dilución, velocidad de infusión,
compatibilidad en Y, interacciones graves, efectos adversos y calculadoras de
dosis.

**Usos acordados:**

- **Ahora:** portafolio (búsqueda de empleo en salud digital) y material de
  formación para TENS, estudiantes y personal de enfermería.
- **Después (opcional):** uso en terreno, solo si un químico farmacéutico
  valida los datos. El diseño debe permitir ese paso sin rehacer la app.

**No es:** una herramienta de prescripción ni reemplaza el protocolo local o la
indicación médica. La app lo declara siempre (ver §5.6).

**Criterios de éxito:**

1. Un reclutador abre un enlace y usa la app en segundos, también sin internet.
2. Cada dato clínico numérico tiene una fuente citada y verificable.
3. Las calculadoras tienen pruebas automáticas con casos calculados a mano.
4. Héctor puede revisar un medicamento leyendo un solo archivo.

## 2. Alcance

### 2.1 Medicamentos

Entre 80 y 100 medicamentos EV en la versión 1.0, organizados en tres tandas:

| Tanda | Contenido | Cantidad aprox. |
|---|---|---|
| 1 | Núcleo de urgencia, SAMU (móvil avanzado) y paciente crítico | 40 |
| 2 | Antibióticos EV | 25 |
| 3 | Resto de lo hospitalario frecuente: protección gástrica, analgesia, antieméticos, electrolitos, sueros, sedoanalgesia de UPC | 25 |

Ejemplos de la tanda 1: adrenalina, amiodarona, atropina, adenosina, midazolam,
fentanilo, morfina, ketamina, noradrenalina, dopamina, dobutamina, sulfato de
magnesio, gluconato de calcio, bicarbonato de sodio, glucosa 30 %, furosemida,
metoclopramida, ondansetrón, ketorolaco, tramadol, metamizol, hidrocortisona,
fenitoína, ácido tranexámico, heparina, insulina cristalina en infusión,
cloruro de potasio.

La lista definitiva de cada tanda sale de la investigación (§6).

### 2.2 Población

- **Adultos.**
- **Pediatría:** dosis por kg con tope de dosis de adulto, solo cuando la
  fuente entrega dosis pediátrica explícita. Sin fuente pediátrica, la app no
  calcula y lo dice.
- **Neonatos (< 28 días): fuera de la versión 1.**

### 2.3 Interacciones

- **Compatibilidad en Y / misma vía:** completa entre los medicamentos de la app.
- **Interacciones farmacológicas:** solo las graves y conocidas, como
  advertencia dentro de la ficha (no hay un buscador de interacciones
  farmacológicas).

### 2.4 Fuera de alcance (versión 1)

Neonatos, cuentas de usuario, almacenamiento de datos de pacientes,
sincronización en línea, panel de edición, publicación en Play Store.

## 3. Enfoque elegido

**Datos en archivos dentro del proyecto + app web estática (PWA)**, empaquetable
después como APK/AAB con Capacitor.

Enfoques descartados para esta etapa:

- **Planilla compartida como fuente:** los datos anidados (compatibilidades,
  dosis por indicación) se rompen fácil en una planilla.
- **Base de datos en línea (Supabase) con panel:** complica el uso sin internet
  y agrega servidor y cuentas. Queda como posible etapa futura, cuando existan
  revisores externos.

## 4. La ficha de cada medicamento

Un archivo YAML por medicamento en `datos/medicamentos/`. Todo valor numérico
lleva unidad y una referencia a fuente (`fuente: <código>`, más sección o
página).

1. **Identificación:** nombre genérico, nombres comerciales en Chile, grupo
   terapéutico, ámbitos de uso (SAMU, urgencia, UPC, hospitalización, APS).
2. **Presentaciones chilenas:** forma, cantidad de principio activo, volumen,
   concentración resultante.
3. **Reconstitución** (si es polvo): diluyente, volumen, concentración final.
4. **Dilución:** sueros compatibles, volúmenes típicos, concentración mínima y
   máxima, diluciones estándar con su concentración.
5. **Administración:** vías (bolo, infusión intermitente, infusión continua),
   tiempo o velocidad recomendada, si exige vía central o bomba.
6. **Dosis por indicación:** adulto y pediátrica, con unidad (mg, mg/kg,
   mcg/kg/min, etc.), rango, dosis máxima y dosis tope. Campo explícito para
   "sin dosis pediátrica en la fuente".
7. **Estabilidad:** duración de la preparación a temperatura ambiente y
   refrigerada, protección de la luz.
8. **Compatibilidad en Y / misma vía:** por cada otro medicamento o suero:
   `compatible`, `incompatible` o `sin_datos`, con fuente.
9. **Interacciones graves:** lista breve con el efecto (depresión respiratoria,
   QT largo, síndrome serotoninérgico, hiperkalemia, etc.).
10. **Efectos adversos y vigilancia:** frecuentes, graves y qué monitorizar.
11. **Alertas:** medicamento de alto riesgo, errores típicos, nombres o envases
    que se confunden.
12. **Metadatos:** fecha de última revisión, revisado por, discrepancias
    abiertas.

Las fuentes se registran una sola vez en `datos/fuentes.yaml` (código, título,
institución, enlace, año, fecha de consulta) y las fichas las citan por código.

## 5. La aplicación

### 5.1 Calculadoras

Se abren precargadas con la presentación y la dilución estándar del
medicamento, o en modo libre.

1. **Concentración:** cantidad de medicamento + volumen final → mg/ml o mcg/ml.
2. **Volumen a cargar:** dosis + presentación → ml a aspirar y número de
   ampollas o frascos.
3. **Velocidad de infusión:**
   - por tiempo: volumen + tiempo → ml/h, gotas/min (macrogotero 20 gotas/ml,
     microgotero 60 gotas/ml);
   - por dosis: dosis por hora + concentración → ml/h.
4. **Dosis por peso (adulto y pediátrica):**
   - dosis → velocidad: peso + dosis (mcg/kg/min, mg/kg/h…) + concentración →
     ml/h;
   - velocidad → dosis: ml/h + concentración + peso → dosis recibida.
5. **Pediatría:** dosis por kg con tope de dosis de adulto; solo para
   medicamentos con dosis pediátrica en la fuente.

**Reglas de seguridad:**

- Unidades siempre visibles; conversión automática mg ↔ mcg y min ↔ h.
- Alerta en rojo si el resultado sale del rango de la ficha (dosis máxima,
  concentración máxima, velocidad máxima). La app avisa, no bloquea.
- En pediatría, si la dosis calculada supera la de adulto, se limita al tope y
  se avisa.
- Redondeo visible: ml/h a 1 decimal, gotas/min a entero, volumen a cargar a 2
  decimales.
- Se muestra la fórmula y el paso a paso.
- Si falta un dato necesario (concentración, peso), la calculadora dice qué
  falta en vez de mostrar un número.

### 5.2 Pantallas

1. **Inicio:** buscador tolerante a errores (genérico o comercial), accesos por
   ámbito (SAMU, urgencia, UPC, hospitalización, APS), últimos consultados.
2. **Lista por grupo terapéutico**, con etiqueta roja para alto riesgo.
3. **Ficha** en pestañas: Preparar · Administrar · Compatibilidad · Seguridad ·
   Fuentes.
4. **Calculadora** precargada, con resultado grande y paso a paso.
5. **Compatibilidad entre varios:** tabla en Y entre dos o más medicamentos
   elegidos (verde compatible, rojo incompatible, gris sin datos).
6. **Acerca de:** aviso legal, versión de datos, fecha y fuentes generales.

### 5.3 Uso

- Diseño para celular primero; también funciona en PC o tablet.
- Tema claro y oscuro.
- Funciona sin internet desde la primera carga (PWA con service worker).
- Sin cuentas y sin guardar datos de pacientes (el peso no se almacena).

### 5.4 Manejo de errores

Si un dato no existe en las fuentes, la app muestra "sin datos en las fuentes".
Nunca rellena con valores por defecto.

### 5.5 Tecnología

- React + TypeScript + Vite.
- Datos YAML convertidos y validados al compilar.
- PWA publicada en GitHub Pages.
- Más adelante, APK/AAB con Capacitor (mismo código).

### 5.6 Aviso de seguridad

Visible en la primera apertura y siempre en "Acerca de": "Material de
formación. No reemplaza el protocolo local ni la indicación médica. Verifique
siempre con la fuente y la normativa de su institución."

## 6. Investigación

### 6.1 Fuentes, en orden de prioridad

1. **Chilenas oficiales:** ISP (registro sanitario y folletos para
   profesionales), MINSAL (Formulario Nacional de Medicamentos, guías clínicas,
   orientaciones SAMU), guías de dilución publicadas por hospitales y servicios
   de salud chilenos.
2. **Fichas técnicas oficiales:** CIMA (AEMPS, España) y DailyMed (FDA, EE. UU.).
3. **Compatibilidad en Y:** Stabilis y las fichas técnicas.
4. **Pediatría:** Pediamécum (Asociación Española de Pediatría) y guías
   pediátricas chilenas.

Las bases de pago (Micromedex, Lexicomp, Trissel's) quedan fuera; pueden
cruzarse más adelante si un revisor tiene acceso.

### 6.2 Proceso

- Por tandas (§2.1).
- Datos críticos (dosis, concentración máxima, velocidad, incompatibilidades)
  confirmados con al menos 2 fuentes.
- Si las fuentes no coinciden: se marca "discrepancia", se muestran ambos
  valores y se prefiere el más conservador.
- Cada dato guarda fuente, sección o página y fecha de consulta.
- Héctor revisa cada tanda con criterio clínico antes de que entre a la app; la
  ficha registra "revisado por" y la fecha.
- Se extraen datos con cita; no se copian tablas ni textos completos de guías
  protegidas por derechos de autor.
- Un informe por tanda en `informes/`: lista de medicamentos, fuentes usadas,
  discrepancias.

## 7. Estructura del proyecto

```
dilucion-ev/
  datos/
    medicamentos/      # un YAML por medicamento
    fuentes.yaml       # registro de fuentes
  src/
    calculos/          # funciones puras + pruebas
    esquema/           # validación de fichas
    app/               # pantallas React
  informes/            # informes de investigación por tanda
  docs/
```

Repositorio en GitHub (`januch-6-6-6`), privado hasta que Héctor decida
publicarlo.

## 8. Pruebas y controles

Se ejecutan antes de cada publicación; si alguno falla, no se publica.

1. **Validación de fichas:** campos obligatorios, unidad y fuente en cada
   número, rangos coherentes (mínimo ≤ máximo, valores positivos).
2. **Compatibilidad simétrica:** si A es incompatible con B, B debe serlo con A;
   cualquier diferencia se reporta.
3. **Calculadoras:** casos calculados a mano para cada fórmula, conversiones de
   unidades, redondeo, tope pediátrico y alertas fuera de rango.
4. **Pantallas clave:** buscar un medicamento, abrir la calculadora precargada,
   ver la alerta roja cuando corresponde.

## 9. Etapas

| Versión | Contenido |
|---|---|
| 0.1 | Estructura, calculadoras con pruebas, unos 10 medicamentos de la tanda 1, PWA publicada. Ya sirve para el portafolio. |
| 0.2 | Tanda 1 completa (unos 40) y pantalla de compatibilidad entre varios. |
| 0.3 | Tandas 2 y 3 (total 80 a 100). |
| 1.0 | Revisión completa, informe final, APK con Capacitor. |
| Futuro | Play Store, panel de revisión con Supabase, neonatos. |
