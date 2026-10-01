import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { obtenerFicha } from '../../datos/cargar'
import { fichaValida } from '../../esquema/__fixtures__/fichas'
import type { Ficha } from '../../esquema/ficha'
import { CalculadoraVista } from './Calculadora'

function montar(ficha?: Ficha) {
  return render(
    <MemoryRouter>
      <CalculadoraVista ficha={ficha} />
    </MemoryRouter>,
  )
}

const nora = () => obtenerFicha('noradrenalina')!

describe('Calculadora', () => {
  it('noradrenalina precargada (4 mg en 100 ml): 0,1 mcg/kg/min en 70 kg = 10,5 ml/h', async () => {
    montar(nora())
    await userEvent.click(screen.getByRole('tab', { name: 'Dosis → velocidad' }))
    expect(screen.getByLabelText('Concentración')).toHaveValue('40')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '70')
    await userEvent.type(screen.getByLabelText('Dosis'), '0,1')
    expect(screen.getByRole('status')).toHaveTextContent('10,5 ml/h')
    expect(screen.getByText(/ml\/h = dosis × peso × 60 ÷ concentración/)).toBeInTheDocument()
  })

  it('dosis sobre la máxima de la ficha muestra alerta', async () => {
    montar(nora())
    await userEvent.click(screen.getByRole('tab', { name: 'Dosis → velocidad' }))
    await userEvent.selectOptions(screen.getByLabelText('Indicación'), 'Shock séptico')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '70')
    await userEvent.type(screen.getByLabelText('Dosis'), '3')
    expect(screen.getByRole('alert')).toHaveTextContent('supera la dosis máxima')
  })

  it('sin peso dice qué falta y no muestra resultado', async () => {
    montar(nora())
    await userEvent.click(screen.getByRole('tab', { name: 'Dosis → velocidad' }))
    await userEvent.type(screen.getByLabelText('Dosis'), '0,1')
    expect(screen.getByRole('status')).toHaveTextContent('Falta el peso')
    expect(screen.getByRole('status')).not.toHaveTextContent('ml/h')
  })

  it('ficha sin dosis pediátrica no calcula', async () => {
    montar(fichaValida('droga-a') as Ficha)
    await userEvent.click(screen.getByRole('tab', { name: 'Pediátrica' }))
    expect(screen.getByText('sin dosis pediátrica en la fuente')).toBeInTheDocument()
    expect(screen.queryByLabelText('Peso (kg)')).not.toBeInTheDocument()
  })

  it('pediátrica sobre el tope se limita y avisa', async () => {
    montar(obtenerFicha('atropina')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Pediátrica' }))
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '50')
    expect(screen.getByRole('status')).toHaveTextContent('0,6 mg')
    expect(screen.getByRole('alert')).toHaveTextContent('limitada a la dosis tope')
  })

  it('velocidad por tiempo calcula gotas', async () => {
    montar()
    await userEvent.click(screen.getByRole('tab', { name: 'Velocidad por tiempo' }))
    await userEvent.type(screen.getByLabelText('Volumen (ml)'), '100')
    await userEvent.type(screen.getByLabelText('Tiempo (min)'), '30')
    expect(screen.getByRole('status')).toHaveTextContent('200 ml/h')
    expect(screen.getByRole('status')).toHaveTextContent('67 gotas/min')
  })

  it('volumen a cargar usa la presentación chilena', async () => {
    montar(obtenerFicha('amiodarona')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Volumen a cargar' }))
    await userEvent.type(screen.getByLabelText('Dosis'), '300')
    expect(screen.getByRole('status')).toHaveTextContent('6 ml')
    expect(screen.getByRole('status')).toHaveTextContent('2 × ampolla')
  })

  it('cambiar la unidad de dosis no reetiqueta la concentración (fentanilo)', async () => {
    montar(obtenerFicha('fentanilo')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Dosis → velocidad' }))
    expect(screen.getByLabelText('Concentración')).toHaveValue('10')
    expect(screen.getByLabelText('Unidad de concentración')).toHaveValue('mcg')
    await userEvent.selectOptions(screen.getByLabelText('Unidad de dosis'), 'mg/kg/h')
    expect(screen.getByLabelText('Unidad de concentración')).toHaveValue('mcg')
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '70')
    await userEvent.type(screen.getByLabelText('Dosis'), '0,001')
    expect(screen.getByRole('status')).toHaveTextContent('7 ml/h')
  })

  it('pediátrica en bolo avisa si la dosis por kg supera el máximo de la ficha', async () => {
    montar(obtenerFicha('fentanilo')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Pediátrica' }))
    await userEvent.type(screen.getByLabelText('Peso (kg)'), '20')
    const porKg = screen.getByLabelText('Dosis por kg (mcg/kg)')
    await userEvent.clear(porKg)
    await userEvent.type(porKg, '20')
    expect(screen.getByRole('alert')).toHaveTextContent('supera la dosis máxima')
  })

  it('pediátrica: elegir una infusión no oculta las opciones en bolo', async () => {
    montar(obtenerFicha('ketamina')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Pediátrica' }))
    await userEvent.selectOptions(screen.getByLabelText('Indicación'), 'Sedación: infusión')
    const opciones = Array.from((screen.getByLabelText('Indicación') as HTMLSelectElement).options).map((o) => o.text)
    expect(opciones).toContain('Inducción de anestesia (bolo)')
    expect(screen.getByLabelText('Peso (kg)')).toBeInTheDocument()
  })

  it('velocidad por dosis convierte mcg/min a ml/h (noradrenalina)', async () => {
    montar(obtenerFicha('noradrenalina')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Velocidad por dosis' }))
    await userEvent.selectOptions(screen.getByLabelText('Indicación'), 'Dosis inicial y mantención (adulto)')
    await userEvent.type(screen.getByLabelText('Dosis'), '8')
    expect(screen.getByRole('status')).toHaveTextContent('12 ml/h')
  })

  it('velocidad por dosis avisa fuera de rango (morfina 10 mg/h)', async () => {
    montar(obtenerFicha('morfina')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Velocidad por dosis' }))
    await userEvent.type(screen.getByLabelText('Dosis'), '10')
    expect(screen.getByRole('alert')).toHaveTextContent('supera la dosis máxima')
  })

  it('cloruro de potasio: el selector de unidad muestra mEq y el resultado no pluraliza la forma', async () => {
    montar(obtenerFicha('cloruro-de-potasio')!)
    await userEvent.click(screen.getByRole('tab', { name: 'Volumen a cargar' }))
    expect(screen.getByLabelText('Unidad de la dosis')).toHaveValue('mEq')
    await userEvent.type(screen.getByLabelText('Dosis'), '20')
    expect(screen.getByRole('status')).toHaveTextContent('14,91 ml · 2 × ampolla 10 % (1 g)')
    expect(screen.getByRole('status')).not.toHaveTextContent('(1 g)s')
  })
})
