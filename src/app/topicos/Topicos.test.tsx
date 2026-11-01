import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it } from 'vitest'
import CalculadoraTopica from './CalculadoraTopica'
import FichaTopica from './FichaTopica'
import { esFavoritoTopico } from './guardadoTopicos'
import ListaTopicos from './ListaTopicos'

// Usa los datos reales (datos/topicos): así la prueba cubre también el cargador.
function montar(ruta: string) {
  return render(
    <MemoryRouter initialEntries={[ruta]}>
      <Routes>
        <Route path="/topicos" element={<ListaTopicos />} />
        <Route path="/topicos/m/:id" element={<FichaTopica />} />
        <Route path="/topicos/m/:id/calcular" element={<CalculadoraTopica />} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => localStorage.clear())

describe('ListaTopicos', () => {
  it('busca por nombre comercial y filtra por vía', async () => {
    montar('/topicos')
    await userEvent.type(screen.getByRole('searchbox'), 'nasonex')
    expect(screen.getByRole('link', { name: /Mometasona nasal/ })).toBeInTheDocument()
    await userEvent.clear(screen.getByRole('searchbox'))
    await userEvent.click(screen.getByRole('button', { name: 'Ótico' }))
    expect(screen.queryByRole('link', { name: /Timolol oftálmico/ })).not.toBeInTheDocument()
    expect(screen.getAllByRole('link').length).toBeGreaterThan(3)
  })
})

describe('FichaTopica', () => {
  it('ficha sin pauta: muestra el motivo y no ofrece calculadora', () => {
    montar('/topicos/m/betaxolol')
    expect(screen.getAllByText(/Ficha informativa/).length).toBeGreaterThan(0)
    expect(screen.getByText(/regla de concentración/)).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Cuánto dura/ })).not.toBeInTheDocument()
  })
  it('atropina: alto riesgo, pauta off-label y segunda fuente concordante', () => {
    montar('/topicos/m/atropina')
    expect(screen.getByText('Alto riesgo')).toBeInTheDocument()
    expect(screen.getAllByText('Off-label').length).toBeGreaterThan(0)
    expect(screen.queryByText(/una sola fuente/)).not.toBeInTheDocument()
  })
  it('fuente única muestra el aviso; favorito se guarda con prefijo top:', async () => {
    montar('/topicos/m/moxifloxacino')
    expect(screen.getByText(/una sola fuente/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Favorito' }))
    expect(esFavoritoTopico('moxifloxacino')).toBe(true)
  })
  it('pestaña Conservación muestra la validez tras abrir', async () => {
    montar('/topicos/m/timolol')
    await userEvent.click(screen.getByRole('tab', { name: 'Conservación' }))
    expect(screen.getByText(/validez abierto: 28 días/)).toBeInTheDocument()
  })
})

describe('CalculadoraTopica', () => {
  it('timolol 5 ml, 2 ojos, 2 veces al día → 25 días por contenido', async () => {
    montar('/topicos/m/timolol/calcular')
    await userEvent.selectOptions(screen.getByLabelText('Sitios'), '2')
    await userEvent.type(screen.getByLabelText('Volumen del frasco (ml)'), '5')
    expect(screen.getByRole('status')).toHaveTextContent('Alcanza para 25 días')
  })
  it('la validez tras abrir limita: timolol 10 ml en un ojo → 28 días', async () => {
    montar('/topicos/m/timolol/calcular')
    await userEvent.type(screen.getByLabelText('Volumen del frasco (ml)'), '10')
    expect(screen.getByRole('status')).toHaveTextContent('Alcanza para 28 días')
    expect(screen.getByRole('status')).toHaveTextContent('limita la validez')
  })
  it('spray nasal pide pulverizaciones y no gotas por ml', async () => {
    montar('/topicos/m/mometasona/calcular')
    expect(screen.queryByLabelText('Gotas por ml')).not.toBeInTheDocument()
    await userEvent.selectOptions(screen.getByLabelText('Sitios'), '2')
    await userEvent.type(screen.getByLabelText('Pulverizaciones por envase'), '120')
    expect(screen.getByRole('status')).toHaveTextContent('Alcanza para 30 días')
  })
  it('sin volumen avisa qué falta', () => {
    montar('/topicos/m/timolol/calcular')
    expect(screen.getByRole('status')).toHaveTextContent('Falta el volumen')
  })
})
