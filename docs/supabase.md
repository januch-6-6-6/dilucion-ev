# Supabase — cómo trabajar con el servidor de la comunidad

Dos proyectos: `dilucion-ev` (real) y `dilucion-ev-pruebas` (pruebas), con «Allow new users to sign up» desactivado.

## Credenciales
Van en `.env.supabase` (ignorado por git; ver `.env.supabase.ejemplo`) y, en CI, como secretos de GitHub.
Nunca se pasan por argumentos de línea de comandos (quedarían visibles en la salida de npm).

## Migraciones
- `npm run db:aplicar -- prueba` aplica las migraciones al proyecto de pruebas; `-- real` al real.
- Una migración ya aplicada no se edita: toda corrección va en una migración nueva.
- Primero siempre al proyecto de pruebas, con sus pruebas en verde; recién después al real.

## Pruebas de permisos
`npm run test:supabase` corre `supabase/pruebas/*.test.ts` contra el proyecto de pruebas. Cada archivo crea sus
propios datos con un sufijo aleatorio y no borra nada (la bitácora es inmutable). `npm test` no usa Supabase.
