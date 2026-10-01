import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { medicamentos } from '../../datos/cargar'
import { CalculadoraVista } from './Calculadora'
import Ficha from './Ficha'

describe('todas las fichas reales', () => {
  it.each(medicamentos.map((m) => [m.id, m] as const))('%s: la ficha y la calculadora se muestran sin errores', (id, m) => {
    const { unmount } = render(
      <MemoryRouter initialEntries={[`/m/${id}`]}>
        <Routes>
          <Route path="/m/:id" element={<Ficha />} />
        </Routes>
      </MemoryRouter>,
    )
    expect(screen.getByRole('heading', { level: 2, name: new RegExp(m.nombre.replace(/[()]/g, '.')) })).toBeInTheDocument()
    unmount()
    render(
      <MemoryRouter>
        <CalculadoraVista ficha={m} />
      </MemoryRouter>,
    )
    expect(screen.getAllByRole('tab').length).toBeGreaterThan(0)
  })
})
