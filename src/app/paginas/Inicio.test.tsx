import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import Inicio from './Inicio'
import Lista from './Lista'

function montar(ruta = '/') {
  return render(
    <MemoryRouter initialEntries={[ruta]}>
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/ambito/:ambito" element={<Lista />} />
        <Route path="/grupo/:grupo" element={<Lista />} />
      </Routes>
    </MemoryRouter>,
  )
}

afterEach(() => vi.restoreAllMocks())

describe('Inicio', () => {
  it('buscar "nora" muestra Noradrenalina', async () => {
    montar()
    await userEvent.type(screen.getByRole('searchbox', { name: /buscar/i }), 'nora')
    expect(screen.getByRole('link', { name: /Noradrenalina/ })).toHaveAttribute('href', '/m/noradrenalina')
  })

  it('el acceso Prehospitalario lista solo medicamentos de ese ámbito', async () => {
    montar()
    await userEvent.click(screen.getByRole('link', { name: 'Prehospitalario' }))
    const lista = screen.getByRole('list', { name: /medicamentos/i })
    expect(within(lista).getByRole('link', { name: /Adrenalina/ })).toBeInTheDocument()
    expect(within(lista).queryByRole('link', { name: /Adenosina/ })).not.toBeInTheDocument()
  })

  it('los favoritos aparecen primero, antes de los últimos consultados', () => {
    localStorage.setItem('dilucion-ev:favoritos', JSON.stringify(['fentanilo', 'no-existe']))
    localStorage.setItem('dilucion-ev:recientes', JSON.stringify(['atropina']))
    montar()
    const titulos = screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent)
    expect(titulos.indexOf('Mis favoritos')).toBeGreaterThanOrEqual(0)
    expect(titulos.indexOf('Mis favoritos')).toBeLessThan(titulos.indexOf('Últimos consultados'))
    const lista = screen.getByRole('list', { name: 'Medicamentos favoritos' })
    expect(within(lista).getByRole('link', { name: /Fentanilo/ })).toBeInTheDocument()
    expect(within(lista).getAllByRole('link')).toHaveLength(1)
  })

  it('sin favoritos no muestra la sección', () => {
    montar()
    expect(screen.queryByText('Mis favoritos')).not.toBeInTheDocument()
  })

  it('marca los medicamentos de alto riesgo', () => {
    montar('/grupo/vasoactivo')
    const item = screen.getByRole('link', { name: /Adrenalina/ })
    expect(within(item).getByText('Alto riesgo')).toBeInTheDocument()
  })

  it('cada medicamento lleva el color de su grupo', () => {
    montar('/grupo/vasoactivo')
    expect(screen.getByRole('link', { name: /Adrenalina/ })).toHaveAttribute('data-color', 'naranjo')
  })

  it('funciona aunque localStorage falle', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('bloqueado')
    })
    montar()
    expect(screen.getByRole('searchbox', { name: /buscar/i })).toBeInTheDocument()
  })
})
