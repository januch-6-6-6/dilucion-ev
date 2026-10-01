# Dilución EV

Aplicación web instalable (PWA) para **preparar y administrar medicamentos endovenosos usados en Chile**: presentaciones, dilución, velocidad de infusión, compatibilidad en Y, interacciones graves, efectos adversos y calculadoras de dosis (ml/h, gotas/min, dosis por peso y pediatría con tope).

**App publicada:** https://januch-6-6-6.github.io/dilucion-ev/ (se puede instalar en el celular y funciona sin internet).

> **Material de formación. No reemplaza el protocolo local ni la indicación médica. Verifique siempre con la fuente y la normativa de su institución.**

## Qué la hace distinta

- **Cada dato clínico tiene fuente citada** (protocolo chileno, ficha técnica oficial, etiqueta FDA, Stabilis, Pediamécum) y la app muestra las discrepancias entre fuentes.
- **Las fórmulas están cubiertas por pruebas automáticas** con casos calculados a mano.
- **Un validador bloquea la publicación** si una ficha no tiene fuente, tiene rangos incoherentes o compatibilidad asimétrica.
- **Funciona sin internet** una vez abierta (útil en un móvil SAMU o en pabellón sin señal).

## Estado

Versión 0.1: 10 medicamentos de urgencia y prehospitalario (adrenalina, noradrenalina, amiodarona, atropina, adenosina, midazolam, fentanilo, morfina, ketamina, sulfato de magnesio). Ver `informes/` para fuentes, discrepancias y estado de la revisión clínica.

## Desarrollo

```bash
npm install
npm run dev        # servidor local
npm test           # pruebas (cálculos, validador, pantallas y build PWA)
npm run validar    # valida datos/medicamentos/*.yaml contra datos/fuentes.yaml
npm run build      # valida datos y compila
```

### Agregar un medicamento

1. Registrar las fuentes en `datos/fuentes.yaml`.
2. Crear `datos/medicamentos/<id>.yaml` con la estructura de `src/esquema/ficha.ts`; cada número con unidad y `fuente: { ref, detalle }`.
3. `npm run validar` hasta que no haya errores.

## Autor

Héctor Salvo Agüero — Técnico en Enfermería (13 años en urgencias, SAMU y pabellón) e Ingeniero en Informática.
