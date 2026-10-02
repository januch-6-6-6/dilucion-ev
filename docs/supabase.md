# Supabase — servidor de la comunidad de prácticas locales

Dos proyectos gratuitos: **`dilucion-ev`** (real) y **`dilucion-ev-pruebas`** (pruebas). En ambos está desactivado
«Allow new users to sign up»: solo entra quien Héctor invita. Spec: `docs/superpowers/specs/2026-10-02-comunidad-practicas-locales-design.md`.

## Credenciales
- Locales: `.env.supabase` (ignorado por git; plantilla en `.env.supabase.ejemplo`).
- CI: secretos de GitHub `SUPABASE_PRUEBA_REF`, `_URL`, `_ANON_KEY`, `_SERVICE_KEY` y `_DB_PASSWORD`
  (solo del proyecto de **pruebas**). **CI no tiene el token de la API de gestión** (`SUPABASE_ACCESS_TOKEN`): ese token
  sirve también sobre el proyecto real y una dependencia comprometida podría usarlo. Cada paso recibe solo los secretos que necesita.
- Nunca se pasan por argumentos de línea de comandos: npm los imprime. Los scripts leen el entorno.
- La clave secreta (`sb_secret_…`) la rechaza Supabase (HTTP 401) si la petición se identifica como navegador.
- El access token vence a los 90 días (31-dic-2026): se genera otro, gratis, en Account → Access Tokens.

## Migraciones (`supabase/migrations/`)
1. `ajustes` · 2. `esquema` · 3. `personas_bitacora` · 4. `propuestas` · 5. `votos_consenso` · 6. `administracion` · 7. `bloqueos_votos`
- Aplicar: `npm run db:aplicar -- prueba` y, con las pruebas en verde, `npm run db:aplicar -- real` (usa el token local).
  En CI el script entra solo con la contraseña de la base de pruebas (`SUPABASE_PRUEBA_POOLER_HOST`, `--db-url`).
- **Una migración ya aplicada no se edita**: toda corrección va en una migración nueva.

## Pruebas
- `npm run test:supabase` — permisos, reglas, concurrencia (votos simultáneos) y escalada directa contra el proyecto de pruebas (cada archivo crea sus datos con un sufijo
  aleatorio y no borra nada: la bitácora es inmutable). `npm test` no usa Supabase.
- `python3 -m pytest scripts/supabase -q` — el cargador de catálogos (sin red).
- En CI (`.github/workflows/publicar.yml`, job `supabase`): aplica migraciones, sincroniza medicamentos, corre ambas
  suites; **`publicar` espera a este job**, así que un permiso roto bloquea la publicación. Sin secretos se omite con un aviso.

## Catálogos
`python3 scripts/supabase/cargar_catalogos.py --destino prueba|real [--deis archivo.csv] [--solo-medicamentos]`
- Medicamentos: ids de `datos/medicamentos/*.yaml`. Volver a correrlo cuando se agreguen fichas.
- Establecimientos: dataset «Establecimientos de Salud vigentes» de datos.gob.cl (CKAN
  `package_show?id=establecimientos-de-salud-vigentes`; CSV `;` UTF-8; código `EstablecimientoCodigo`,
  vigente = `EstadoFuncionamiento` que empieza con «Vigente»). 5.743 filas al 29-sep-2026. Se recarga a mano de vez en cuando.
- Solo inserta o actualiza: nunca borra. Los que desaparecen se marcan `vigente = false`.

## Administrador
`scripts/supabase/crear_admin.py` crea a Héctor (correo confirmado, sin enviar mensajes) como persona y administrador
del proyecto **real**. Se corrió una vez el 2-oct-2026. Entra con enlace mágico desde la Etapa 2.

## Cosas que conviene saber
- El plan gratis **pausa** un proyecto tras 7 días sin actividad; se reactiva con un clic en el panel.
- Verificar permisos a mano: con la clave pública, `notas_publicadas` responde `[]` y las demás tablas vacío o «permission denied».
