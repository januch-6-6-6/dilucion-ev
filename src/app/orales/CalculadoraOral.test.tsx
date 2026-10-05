import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fichaOralValida } from '../../esquema/__fixtures__/orales'
import { FichaOral as EsquemaFichaOral } from '../../esquema/ficha-oral'
import CalculadoraOral from './CalculadoraOral'

const { fichas } = vi.hoisted(() => ({ fichas: new Map<string, unknown>() }))

vi.mock('../../datos/cargarOrales', () => ({
  obtenerOral: (id: string) => fichas.get(id),
}))

const f = { ref: 'F1', detalle: 'p. 1' }
const jarabe100 = {
  id: 'jarabe-100',
  forma: 'jarabe',
  concentracion: { valor: 100, unidad: 'mg' },
  partible: 'no',
  liberacionProlongada: false,
  registroChile: 'verificado',
  fuente: f,
}
const dosisAdulto = { indicacion: 'Dolor', poblacion: 'adulto', regimen: 'fija', base: 'toma', unidad: 'mg', min: 500, max: 1000, tomasPorDia: 4, estatus: 'autorizada', fuente: f }
const dosisPeso = { indicacion: 'Dolor', poblacion: 'pediatrico', regimen: 'por_peso', base: 'toma', unidad: 'mg/kg', min: 10, max: 15, intervaloH: 6, estatus: 'autorizada', fuente: f }

const crear = (id: string, extra: Record<string, unknown> = {}) => fichas.set(id, EsquemaFichaOral.parse(fichaOralValida(id, extra)))

function montar(id: string) {
  return render(
    <MemoryRouter initialEntries={[`/orales/m/${id}/calcular`]}>
      <Routes>
        <Route path="/orales/m/:id/calcular" element={<CalculadoraOral />} />
      </Routes>
    </MemoryRouter>,
  )
}

const presentaciones = (fichaOralValida().presentaciones as unknown[]).concat([jarabe100])

beforeEach(() => {
  fichas.clear()
  crear('para', { presentaciones })
  crear('tope', { presentaciones, dosis: [dosisAdulto, { ...dosisPeso, topePorToma: { valor: 100, unidad: 'mg' } }] })
  crear('adulto', {
    dosis: [dosisAdulto],
    pediatria: { estado: 'solo_adulto', motivo: 'No hay dosis pediátrica en la fuente' },
  })
})

describe('CalculadoraOral', () => {
  it('id inexistente: medicamento no encontrado', () => {
    montar('nada')
    expect(screen.getByText('Medicamento no encontrado')).toBeInTheDocument()
  })

  it('por peso: 10 kg, 15 mg/kg, 100 mg/ml da 150 mg y 1,5 ml', async () => {
    montar('para')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    expect(screen.getByLabelText('Concentración del frasco (mg/ml)')).toHaveValue('100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '10')
    const r = screen.getByTestId('resultado')
    expect(r).toHaveTextContent('150 mg')
    expect(r).toHaveTextContent('1,5 ml')
    expect(r).toHaveTextContent('[F1]')
  })

  it('acepta el peso con coma', async () => {
    montar('para')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '12,5')
    expect(screen.getByTestId('resultado')).toHaveTextContent('187,5 mg')
  })

  it('peso vacío: dice Falta el peso y no hay resultado', async () => {
    montar('para')
    expect(screen.getByRole('status')).toHaveTextContent('Falta el peso')
    expect(screen.queryByTestId('resultado')).not.toBeInTheDocument()
  })

  it('concentración borrada: Falta la concentración y no hay resultado', async () => {
    montar('para')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '10')
    await userEvent.clear(screen.getByLabelText('Concentración del frasco (mg/ml)'))
    expect(screen.getByRole('status')).toHaveTextContent('Falta la concentración')
    expect(screen.queryByTestId('resultado')).not.toBeInTheDocument()
  })

  it('concentración editada se usa en el cálculo', async () => {
    montar('para')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '10')
    await userEvent.clear(screen.getByLabelText('Concentración del frasco (mg/ml)'))
    await userEvent.type(screen.getByLabelText('Concentración del frasco (mg/ml)'), '50')
    expect(screen.getByTestId('resultado')).toHaveTextContent('3 ml')
  })

  it('presentación sólida: unidades y sin campo de concentración', async () => {
    montar('para')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '70')
    expect(screen.queryByLabelText('Concentración del frasco (mg/ml)')).not.toBeInTheDocument()
    expect(screen.getByTestId('resultado')).toHaveTextContent('2 ')
  })

  it('superar un tope muestra la alerta dentro del bloque de resultado', async () => {
    montar('tope')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '10')
    const r = screen.getByTestId('resultado')
    expect(within(r).getByRole('alert')).toHaveTextContent('tope por toma')
    expect(r).toHaveTextContent('100 mg')
  })

  it('solo adulto: Por peso deshabilitado con el motivo; Dosis fija disponible', async () => {
    montar('adulto')
    expect(screen.getByRole('tab', { name: 'Por peso' })).toBeDisabled()
    expect(screen.getByText(/No hay dosis pediátrica en la fuente/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('tab', { name: 'Dosis fija' }))
    expect(screen.getByTestId('resultado')).toHaveTextContent('mg')
  })

  it('mg ↔ ml en ambos sentidos con la misma concentración', async () => {
    montar('para')
    await userEvent.click(screen.getByRole('tab', { name: 'mg ↔ ml' }))
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Dosis (mg)'), '150')
    expect(screen.getByRole('status')).toHaveTextContent('1,5 ml')
    await userEvent.clear(screen.getByLabelText('Dosis (mg)'))
    await userEvent.type(screen.getByLabelText('Volumen (ml)'), '1,5')
    expect(screen.getByRole('status')).toHaveTextContent('150 mg')
  })
})
