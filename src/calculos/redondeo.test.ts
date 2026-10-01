import { describe, expect, it } from 'vitest'
import { redondear } from './redondeo'

describe('redondear (half-up)', () => {
  it('26,25 a 1 decimal es 26,3', () => expect(redondear(26.25, 1)).toBe(26.3))
  it('0,1 × 3 a 1 decimal es 0,3', () => expect(redondear(0.1 * 3, 1)).toBe(0.3))
  it('66,666 a entero es 67', () => expect(redondear(66.666, 0)).toBe(67))
  it('1,005 a 2 decimales es 1,01', () => expect(redondear(1.005, 2)).toBe(1.01))
  it('valores muy pequeños no dan NaN', () => expect(redondear(1e-7, 3)).toBe(0))
})
