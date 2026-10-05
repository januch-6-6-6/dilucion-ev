import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Link, MemoryRouter, Route, Routes } from 'react-router-dom'
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
const jarabe50 = { ...jarabe100, id: 'jarabe-50', concentracion: { valor: 50, unidad: 'mg' } }
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

  it('cambiar de medicamento en la misma ruta reinicia el estado (sin caerse)', async () => {
    crear('corta', { presentaciones: [jarabe50] })
    render(
      <MemoryRouter initialEntries={['/orales/m/para/calcular']}>
        <Link to="/orales/m/corta/calcular">ir</Link>
        <Link to="/orales/m/adulto/calcular">ir-adulto</Link>
        <Routes>
          <Route path="/orales/m/:id/calcular" element={<CalculadoraOral />} />
        </Routes>
      </MemoryRouter>,
    )
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '10')
    await userEvent.click(screen.getByText('ir'))
    expect(screen.getByLabelText('Concentración del frasco (mg/ml)')).toHaveValue('50')
    expect(screen.getByLabelText('Peso (kg)')).toHaveValue('')
    await userEvent.click(screen.getByText('ir-adulto'))
    expect(screen.queryByLabelText('Peso (kg)')).not.toBeInTheDocument()
    expect(screen.getByText(/No hay dosis pediátrica en la fuente/)).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: 'Por peso' })).toBeDisabled()
  })

  it('tope de adulto más bajo entre unidades mezcladas (omite las no comparables)', async () => {
    const adultos = [1000, 5, 500].map((v, i) => ({ ...dosisAdulto, indicacion: `A${i}`, topePorToma: { valor: v, unidad: i === 1 ? 'UI' : 'mg' } }))
    crear('mixto', { presentaciones, dosis: [...adultos, dosisPeso] })
    montar('mixto')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '70')
    expect(within(screen.getByTestId('resultado')).getByRole('alert')).toHaveTextContent('tope de adulto por toma')
    expect(screen.getByTestId('resultado')).toHaveTextContent('500 mg')
  })

  it('error de presentación sólida sugiere la presentación líquida', async () => {
    montar('para')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '1')
    expect(screen.getByRole('status')).toHaveTextContent('no permite esa dosis')
    expect(screen.getByText('Prueba con la presentación líquida (jarabe) de esta ficha')).toBeInTheDocument()
  })

  it('dosis solo con texto no muestra undefined en el selector', async () => {
    const porEdad = { indicacion: 'Lactante', poblacion: 'pediatrico', regimen: 'por_edad', unidad: 'mg', texto: 'según edad', estatus: 'autorizada', fuente: f }
    crear('edad', { dosis: [dosisAdulto, porEdad] })
    montar('edad')
    expect(screen.getByLabelText('Dosis')).not.toHaveTextContent('undefined')
    expect(screen.getByLabelText('Dosis')).toHaveTextContent('según edad')
  })

  it('gotas: el resultado muestra gotas', async () => {
    const gotas = { id: 'gotas-2', forma: 'gotas', concentracion: { valor: 2, unidad: 'mg' }, gotasPorMl: 20, partible: 'no', liberacionProlongada: false, registroChile: 'verificado', fuente: f }
    crear('gotero', { presentaciones: [gotas] })
    montar('gotero')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '2')
    expect(screen.getByTestId('resultado')).toHaveTextContent('gotas')
  })

  it('muestra limitadaPor dentro del resultado', async () => {
    montar('tope')
    await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'jarabe-100')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '10')
    expect(screen.getByTestId('resultado')).toHaveTextContent('Limitada por: tope por toma')
  })
})
