# Tópicos ojo/oído/nariz — estado de la Fase 0 (cierre del 30-oct-2026)

Ampliación de Dilución EV con medicamentos tópicos de ojo, oído y nariz. Las decisiones de alcance están en [`DECISIONES.md`](DECISIONES.md). **Material de formación, no de prescripción.**

## Dónde quedamos

**Hecho:**

1. **Universo chileno:** se buscó por nombre de producto en el ISP (`bajar_isp_nombres.py` → `isp-nombres/`, `isp-universo.json`, 374 registros). `armar_lista.py` filtra los prefijos F-, B- y FX- y aplica las exclusiones de Héctor. Resultado: **`lista-isp.json` = 80 moléculas o combinaciones**.
2. **Fuentes por molécula:**
   - CIMA: `bajar_cima.py` → `cima/`, 56 moléculas, con el principio activo exacto y prefiriendo productos con ficha técnica HTML.
   - DailyMed: `bajar_dailymed.py` → `dailymed/`, 13 moléculas.
   - Pediamécum: `bajar_pediamecum.py` → `pediamecum/`, 60 moléculas con al menos un componente. Los slugs se corrigieron a mano.
   - Universo de referencia por ATC: `universo_cima.py` → `cima-universo.json`.
3. **Cobertura:** `cobertura.py` → [`COBERTURA.md`](COBERTURA.md). 49 moléculas con ≥2 fuentes de dosis, 31 con 1 y ninguna sin fuente.
4. **Extractos:** `extraer_extractos.py` → `extractos.md`, con ISP, CIMA (4.2, 4.3, 6.3), DailyMed y Pediamécum lado a lado.
5. **Borrador de Antigravity:** `INFORME-BORRADOR-agy.md`, hecho con el prompt de `PROMPT-agy-informe.md`. Sus conteos fueron 🔴 6, 🟡 22, 🟢 16, ⚪ 32 y ⚠️ 8. **Ojo: lo hizo con 84 moléculas**, antes de las exclusiones; hay que sacar calcitonina, desmopresina, esketamina y Mentholatum. Claude verificó al azar fenilefrina, betaxolol, ketorolaco, atropina y tetrizolina, y todas estaban bien. **Falta la revisión completa.**

## Lo que sigue (en orden)

1. **Revisar el borrador molécula por molécula** contra `extractos.md`, y contra los `.txt` completos cuando el extracto esté recortado. El informe de Antigravity no es evidencia: hay que confirmar cada cifra y cada color. Hay que poner atención en:
   - Las 8 ⚠️: concentración chilena distinta de la ficha (fenilefrina 2,5 vs 10 %, betaxolol 0,5 vs 0,25 %, ketorolaco 0,4 vs 0,5 %, levofloxacino 0,5 vs 1,5 %) y fuentes de la vía equivocada (cromoglicato nebulizado, betametasona cutánea, gatifloxacino sin prednisolona).
   - Nafazolina en DailyMed: el producto de la FDA trae glicerina o propilenglicol.
   - Hialuronato en DailyMed: el producto es de un vendedor chino, una fuente débil.
   - Las combinaciones que solo existen en Chile, que solo tienen fuente por componente.
2. **Escribir el informe final** en `informes/topicos-discrepancias.md`, con el formato del de orales. Debe tener el resumen con los conteos de las 80, las reglas de diseño y las decisiones para Héctor.
3. **Decisiones que probablemente le tocan a Héctor** (las confirma el informe):
   - Publicar o no las 31 de una sola fuente, con aviso, como se hizo en orales.
   - Si la ficha debe atarse a la concentración registrada en Chile y no mostrar pautas de otra concentración.
   - Qué hacer con las combinaciones solo chilenas sin fuente para la combinación.
   - Cuál pauta pediátrica gana cuando la ficha técnica no la autoriza (atropina 1 %: CIMA desde 3 años contra Pediamécum desde 1 año).
4. **Brainstorming → diseño por secciones → spec** en `docs/superpowers/specs/AAAA-MM-DD-topicos-design.md`, con el esquema `FichaTopica`, las rutas `/topicos`, la calculadora de duración del frasco y la regla de concentración.
5. **Plan** (skill writing-plans) → Héctor elige el método de ejecución.

## Cómo volver a generar todo

```bash
cd ~/dilucion-ev/datos/crudos/topicos
python3 armar_lista.py && python3 bajar_cima.py && python3 bajar_dailymed.py && python3 bajar_pediamecum.py
python3 cobertura.py && python3 extraer_extractos.py
```

Las descargas se saltan lo que ya existe. Para rehacer algo, hay que borrar su archivo.

## Lecciones técnicas

- **ISP:** el certificado no valida (`ssl` sin verificar). Hay que correr un solo proceso con pausas, porque bloquea la IP si se paraleliza. La búsqueda por nombre es por subcadena: trae «OSMÓTICA» y «PREBIÓTICA», y hay que buscar con tilde («COLIRIO» y «OTICA» sin tilde dan 0).
- **CIMA:** se usa curl, porque urllib se cuelga. Hay que filtrar por el nombre exacto del principio activo (`vtm`); con coincidencia parcial trae el fármaco equivocado.
- **Pediamécum:** una ficha que no existe devuelve una página genérica de unos 131 KB, no un 404. Hay que preferir los slugs `-oftalmica` o `-nasal`.
- **Antigravity (`agy -p`):** necesita `--settings '{"permissions":{"allow":["read_file(/ruta/abs)","write_file(/ruta/abs)"]}}'`, con ruta de directorio y sin comodines. Si no, se corta sin escribir nada. Tampoco puede correr comandos.
