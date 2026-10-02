#!/usr/bin/env bash
# Aplica las migraciones de supabase/migrations al proyecto indicado.
# Uso: scripts/supabase/aplicar.sh prueba|real
# Las credenciales salen de .env.supabase (o del entorno en CI); nunca se pasan por argumentos.
set -euo pipefail
cd "$(dirname "$0")/../.."
[ -f .env.supabase ] && { set -a; . ./.env.supabase; set +a; }
destino="${1:?Uso: aplicar.sh prueba|real}"
case "$destino" in
  prueba) ref="${SUPABASE_PRUEBA_REF:?}"; export SUPABASE_DB_PASSWORD="${SUPABASE_PRUEBA_DB_PASSWORD:?}" ;;
  real)   ref="${SUPABASE_REAL_REF:?}";   export SUPABASE_DB_PASSWORD="${SUPABASE_REAL_DB_PASSWORD:?}" ;;
  *) echo "Destino inválido: $destino" >&2; exit 2 ;;
esac
supabase="$PWD/node_modules/.bin/supabase" # directo, no por npx/npm: así ninguna URL con contraseña se imprime
if [ -n "${SUPABASE_PRUEBA_POOLER_HOST:-}" ] && [ "$destino" = prueba ] && [ -z "${SUPABASE_ACCESS_TOKEN:-}" ]; then
  # Modo CI: solo la contraseña de la base de pruebas; no hace falta ningún token de la API de gestión
  # (que serviría también sobre el proyecto real).
  clave="$(python3 -c 'import os,urllib.parse;print(urllib.parse.quote(os.environ["SUPABASE_DB_PASSWORD"],safe=""))')"
  "$supabase" db push --yes --db-url "postgresql://postgres.${ref}:${clave}@${SUPABASE_PRUEBA_POOLER_HOST}:5432/postgres"
else
  export SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:?}"
  "$supabase" link --project-ref "$ref" >/dev/null
  "$supabase" db push --yes
fi
