import { afterEach, describe, expect, it, vi } from 'vitest'
import { INTERVALO_MS, debeRevisar, vigilarActualizaciones } from './actualizacion'

const volverAPrimerPlano = () => document.dispatchEvent(new Event('visibilitychange'))

afterEach(() => vi.restoreAllMocks())

describe('debeRevisar', () => {
  it('sin revisión previa, revisa', () => expect(debeRevisar(1000, null)).toBe(true))
  it('antes de 6 h no revisa; desde las 6 h sí', () => {
    expect(debeRevisar(INTERVALO_MS - 1, 0)).toBe(false)
    expect(debeRevisar(INTERVALO_MS, 0)).toBe(true)
  })
})

describe('vigilarActualizaciones', () => {
  it('al volver a primer plano revisa solo si pasaron 6 h desde la carga o la última revisión', () => {
    let ahora = 0
    const update = vi.fn().mockResolvedValue(undefined)
    const dejar = vigilarActualizaciones({ update }, () => ahora)
    ahora = INTERVALO_MS - 1
    volverAPrimerPlano()
    expect(update).not.toHaveBeenCalled()
    ahora = INTERVALO_MS
    volverAPrimerPlano()
    expect(update).toHaveBeenCalledTimes(1)
    volverAPrimerPlano()
    expect(update).toHaveBeenCalledTimes(1)
    dejar()
  })

  it('sin internet no revisa', () => {
    let ahora = 0
    const update = vi.fn().mockResolvedValue(undefined)
    vi.spyOn(navigator, 'onLine', 'get').mockReturnValue(false)
    const dejar = vigilarActualizaciones({ update }, () => ahora)
    ahora = INTERVALO_MS * 2
    volverAPrimerPlano()
    expect(update).not.toHaveBeenCalled()
    dejar()
  })

  it('un fallo de red al revisar no rompe la app', async () => {
    let ahora = 0
    const update = vi.fn().mockRejectedValue(new Error('sin red'))
    const dejar = vigilarActualizaciones({ update }, () => ahora)
    ahora = INTERVALO_MS
    expect(() => volverAPrimerPlano()).not.toThrow()
    await Promise.resolve()
    dejar()
  })
})
