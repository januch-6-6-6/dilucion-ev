import { defineConfig } from 'vitest/config'

// Pruebas de permisos y reglas contra el proyecto Supabase de PRUEBAS (remoto).
// Se corren aparte de `npm test`: npm run test:supabase
export default defineConfig({
  test: {
    environment: 'node',
    include: ['supabase/pruebas/**/*.test.ts'],
    testTimeout: 30_000,
    hookTimeout: 60_000,
    fileParallelism: false, // un archivo a la vez: comparten el proyecto de pruebas
  },
})
