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
export SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:?}"
npx supabase link --project-ref "$ref" >/dev/null
npx supabase db push --yes
