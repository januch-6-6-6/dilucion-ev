# Decisiones de Héctor — tópicos ojo/oído/nariz

## 30-oct-2026 — alcance (brainstorming)

- **Universo:** opción C, todo lo registrado en el ISP como oftálmico, ótico o nasal (no solo el arsenal APS, que trae solo gentamicina, cloranfenicol y proparacaína).
- **Formas:** opción C, todo lo tópico de ojo, oído y nariz: gotas, ungüentos y geles oftálmicos, y sprays nasales.
- **Calculadora:** opción C, fichas informativas + calculadora de duración del frasco. Los colirios reforzados quedan fuera de la v1.
- **Arquitectura:** enfoque 1, esquema propio `FichaTopica`, rutas `/topicos` y favoritos con prefijo `top:`.
- **Orden:** Fase 0 de investigación (estos crudos) antes de la spec.

## 30-oct-2026 — exclusiones de la lista ISP (84 → 80)

Quedan fuera:

| Molécula | Motivo |
|---|---|
| Calcitonina nasal | vía nasal con efecto sistémico (osteoporosis), no es tratamiento tópico |
| Desmopresina nasal | vía nasal con efecto sistémico (diabetes insípida/enuresis) |
| Esketamina (Spravato) | vía nasal con efecto sistémico; uso psiquiátrico bajo supervisión |
| Alcanfor + mentol + salicilato de metilo (Mentholatum) | sin fuente de posología; producto de inhalación en tórulas, no es gota ni spray |
| Otoseptil (B-779/25) | el ISP no declara su principio activo |

Se aplican en `armar_lista.py` (`EXCLUIR`). Otoseptil nunca estuvo entre las 84 (sin principio activo, `armar_lista.py` ya lo dejaba fuera), por eso el total es 80.

## 31-oct-2026 — reglas de datos (antes del informe final)

1. **Fuente única:** se publica con aviso visible («se apoya en una sola fuente»), igual que en orales.
2. **Concentración:** la ficha se ata a la concentración registrada en el ISP. Una pauta de otra concentración (fenilefrina 10 %, betaxolol 0,25 %, ketorolaco 0,5 %, levofloxacino 1,5 %) no se muestra como pauta; queda como nota de discrepancia.
3. **Combinaciones solo chilenas sin fuente de la combinación:** ficha informativa sin pauta, con presentación, componentes, alertas por componente y aviso «sin fuente de posología para la combinación».
4. **Pediatría no autorizada en la ficha técnica pero con pauta en Pediamécum:** se muestran ambas; el límite de la ficha como autorizado y la pauta de Pediamécum como «off-label» con alerta (ej. atropina 1 %: CIMA ≥3 años, Pediamécum ≥1 año).
