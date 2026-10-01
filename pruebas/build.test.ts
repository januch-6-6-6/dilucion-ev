// @vitest-environment node
import { execSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { beforeAll, describe, expect, it } from 'vitest'

const dist = join(import.meta.dirname, '..', 'dist')

describe('build de producción (PWA)', () => {
  beforeAll(() => {
    execSync('npx vite build', { cwd: join(import.meta.dirname, '..'), stdio: 'pipe' })
  }, 120_000)

  it('genera el manifiesto con el nombre de la app', () => {
    const manifiesto = JSON.parse(readFileSync(join(dist, 'manifest.webmanifest'), 'utf8'))
    expect(manifiesto.name).toBe('Dilución EV')
    expect(manifiesto.lang).toBe('es-CL')
  })
  it('genera el service worker', () => expect(existsSync(join(dist, 'sw.js'))).toBe(true))
  it('index.html enlaza el manifiesto', () => expect(readFileSync(join(dist, 'index.html'), 'utf8')).toContain('manifest.webmanifest'))
})
