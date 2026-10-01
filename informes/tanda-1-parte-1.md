# Tanda 1, parte 1 — Informe de investigación

**Fecha de consulta de fuentes:** 2026-10-01
**Medicamentos (10):** adrenalina, noradrenalina, amiodarona, atropina, adenosina,
midazolam, fentanilo, morfina, ketamina, sulfato de magnesio.
**Estado:** pendiente de revisión clínica (Héctor Salvo Agüero, TENS).

Las fichas están en `datos/medicamentos/` y se generan con
`python3 scripts/generar-tanda1.py datos/crudos/stabilis-y-2026-10-01.json`.
Cada dato numérico cita su fuente y sección.

## Fuentes usadas

| Código | Fuente | Para qué se usó |
|---|---|---|
| PUCON-2022 | Protocolo GCL 1.2.6, Hospital San Francisco de Pucón (vigente hasta 2027) | Presentaciones chilenas, diluciones habituales, concentraciones, lista de alto riesgo, RAM |
| CIMA-* | Fichas técnicas oficiales de la AEMPS (España), una por medicamento | Dosis (4.2), interacciones (4.5), incompatibilidades (6.2), estabilidad (6.3), preparación (6.6) |
| FDA-EPINEFRINA / FDA-NOREPINEFRINA | Etiquetas oficiales FDA (DailyMed) | Infusión de adrenalina en shock séptico; dosis y preparación de noradrenalina; equivalencia sal/base |
| STABILIS-Y | Tabla de compatibilidad en Y de Stabilis, generada para estos 10 medicamentos + SF y SG5 % | Compatibilidad en Y |
| PEDIAMECUM-* | Pediamécum (Asociación Española de Pediatría) | Dosis pediátricas de fentanilo, morfina, ketamina y amiodarona |

Fuentes buscadas que no se pudieron usar:
- **Folletos del ISP:** el buscador del registro sanitario no se puede consultar
  de forma automatizada. Las presentaciones chilenas se tomaron del protocolo de
  Pucón. **Por eso los nombres comerciales quedaron vacíos.**
- **Guía de Iquique:** solo cubre antiinfecciosos; se usará en la tanda 2.

## Compatibilidad en Y (Stabilis)

- **Incompatibles:** noradrenalina–sulfato de magnesio, amiodarona–SF 0,9 %,
  ketamina–Ringer lactato.
- **Datos contradictorios → registrados como incompatibles (criterio
  conservador):** amiodarona con fentanilo, sulfato de magnesio, midazolam y
  noradrenalina; midazolam–morfina.
- **Morfina–sulfato de magnesio:** Stabilis no tiene datos, pero la ficha CIMA de
  morfina (6.2) la declara incompatible con sales de magnesio → incompatible.
- **Adenosina:** sin datos frente a los otros 9 (solo compatible con SF, SG5 % y
  Ringer lactato). Se administra sola y sin diluir.
- Atropina–SG5 %: sin datos en Stabilis.

## Discrepancias y decisiones

1. **Noradrenalina, sal o base:** CIMA expresa las dosis como base
   (1 mg de bitartrato = 0,5 mg de base); FDA indica que la ampolla de 4 mg/4 ml
   equivale a 4 mg de base. Se asumió la ampolla chilena 4 mg/4 ml como base.
   **Verificar el rotulado del producto que se usa en Chile.**
2. **Adenosina, primera dosis en adultos:** CIMA indica 3 mg → 6 mg → 12 mg; los
   protocolos de reanimación de uso habitual parten con 6 mg. Se registró el
   esquema de CIMA (más conservador). **Revisar con el protocolo local.**
3. **Amiodarona en pediatría:** CIMA dice que la seguridad no está establecida;
   Pediamécum da 5 mg/kg (máx. 300 mg) en TV sin pulso o FV. Se registró la de
   Pediamécum con la advertencia.
4. **Ketamina, estabilidad diluida:** CIMA 6.3 dice «usar inmediatamente» y 6.6
   dice 24 h para 1 mg/ml. Se registró «usar inmediatamente».
5. **Fentanilo en adultos:** la ficha CIMA solo trae dosis de anestesia. No se
   registró dosis de analgesia en urgencia para adultos hasta tener una fuente.
6. **Morfina pediátrica:** Pediamécum da un máximo diario (15 mg/24 h), no un tope
   por dosis; la dosis queda sin tope por dosis.
7. **Adrenalina y noradrenalina en SF:** Stabilis las da como compatibles, pero FDA
   no recomienda diluirlas solo en SF (pérdida de potencia por oxidación). Se
   indica en el texto de administración.

## Para la revisión clínica

Revisar especialmente:
- Presentaciones y diluciones habituales (¿calzan con lo que se usa en SAMU y
  urgencias?).
- Las 7 discrepancias de arriba.
- Dosis faltantes que harían falta en terreno (por ejemplo, analgesia con
  fentanilo en adultos) y la fuente que conviene usar.
