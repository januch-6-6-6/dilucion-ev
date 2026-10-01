import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import Ficha from './Ficha'

function montar(id: string) {
  return render(
    <MemoryRouter initialEntries={[`/m/${id}`]}>
      <Routes>
        <Route path="/m/:id" element={<Ficha />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('Ficha', () => {
  it('muestra las cinco pestañas', () => {
    montar('noradrenalina')
    for (const nombre of ['Preparar', 'Administrar', 'Compatibilidad', 'Seguridad', 'Fuentes']) {
      expect(screen.getByRole('tab', { name: nombre })).toBeInTheDocument()
    }
  })

  it('un dato ausente muestra "sin datos en las fuentes"', () => {
    montar('noradrenalina')
    expect(screen.getAllByText('sin datos en las fuentes').length).toBeGreaterThan(0)
  })

  it('compatibilidad: incompatible y sin datos se distinguen', async () => {
    montar('amiodarona')
    await userEvent.click(screen.getByRole('tab', { name: 'Compatibilidad' }))
    expect(screen.getByRole('row', { name: /SF.*Incompatible/ })).toBeInTheDocument()
    expect(screen.getByRole('row', { name: /adenosina.*Sin datos/i })).toBeInTheDocument()
  })

  it('id inexistente muestra "Medicamento no encontrado"', () => {
    montar('no-existe')
    expect(screen.getByText('Medicamento no encontrado')).toBeInTheDocument()
  })

  it('registra el medicamento en recientes', () => {
    montar('atropina')
    expect(localStorage.getItem('dilucion-ev:recientes')).toContain('atropina')
  })

  it('tiene botón para calcular', () => {
    montar('noradrenalina')
    expect(screen.getByRole('link', { name: 'Calcular' })).toHaveAttribute('href', '/m/noradrenalina/calcular')
  })
})
