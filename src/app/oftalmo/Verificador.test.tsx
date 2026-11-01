import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it } from 'vitest'
import VerificadorOcular from './VerificadorOcular'
import { AVISO_PABELLON } from './textos'

// Usa los datos reales (datos/oftalmo): cefuroxima (polvo) y moxifloxacino (solución).
function montar(id: string) {
  return render(
    <MemoryRouter initialEntries={[`/oftalmologia/m/${id}/verificar`]}>
      <Routes>
        <Route path="/oftalmologia/m/:id/verificar" element={<VerificadorOcular />} />
        <Route path="/oftalmologia/m/:id" element={<p>ficha</p>} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => localStorage.clear())

async function cefuroximaVial750(reconstituir: string, tomar: string, llevarA: string) {
  montar('cefuroxima')
  await userEvent.selectOptions(screen.getByLabelText('Presentación'), 'vial-750')
  await userEvent.type(screen.getByLabelText('Paso 1: diluyente agregado (ml)'), reconstituir)
  await userEvent.click(screen.getByRole('button', { name: 'Agregar paso' }))
  await userEvent.selectOptions(screen.getByLabelText('Paso 2: tipo'), 'diluir')
  await userEvent.type(screen.getByLabelText('Paso 2: tomar (ml)'), tomar)
  await userEvent.type(screen.getByLabelText('Paso 2: llevar a (ml)'), llevarA)
}

describe('VerificadorOcular', () => {
  it('cefuroxima: frasco de 750 mg, reconstituir 7,5 y diluir 1→10 coincide con la fuente', async () => {
    await cefuroximaVial750('7,5', '1', '10')
    const estado = screen.getByRole('status')
    expect(estado).toHaveTextContent('Coincide con')
    expect(estado).toHaveTextContent('1 mg en 0,1 ml')
    expect(estado).not.toHaveTextContent('NO coincide')
  })

  it('cefuroxima: diluir 1→8 da el texto rojo exacto, sin otras cifras', async () => {
    await cefuroximaVial750('7,5', '1', '8')
    expect(
      screen.getByText('NO coincide: obtuviste 1,25 mg en 0,1 ml; la fuente dice 1 mg en 0,1 ml. No administres; revisa los pasos.'),
    ).toBeInTheDocument()
    expect(screen.getByRole('status')).not.toHaveTextContent('Coincide con')
  })

  it('moxifloxacino: diluir 3→10 coincide con la pauta de Arshinoff', async () => {
    montar('moxifloxacino')
    await userEvent.type(screen.getByLabelText('Paso 1: tomar (ml)'), '3')
    await userEvent.type(screen.getByLabelText('Paso 1: llevar a (ml)'), '10')
    const estado = screen.getByRole('status')
    expect(estado).toHaveTextContent('Coincide con')
    expect(estado).toHaveTextContent(/Arshinoff/)
  })

  it('una ficha informativa (bupivacaína) dice que no tiene verificador y conserva el aviso de pabellón', () => {
    montar('bupivacaina')
    expect(screen.getByText('Esta ficha no tiene verificador')).toBeInTheDocument()
    expect(screen.getByText(AVISO_PABELLON)).toBeInTheDocument()
  })

  it('una ficha de uso directo (ranibizumab) tampoco tiene verificador', () => {
    montar('ranibizumab')
    expect(screen.getByText('Esta ficha no tiene verificador')).toBeInTheDocument()
  })

  it('un id inexistente dice que no se encontró', () => {
    montar('no-existe')
    expect(screen.getByText('Medicamento no encontrado')).toBeInTheDocument()
  })

  it('muestra el supuesto del volumen tras reconstituir y el aviso de pabellón', () => {
    montar('cefuroxima')
    expect(screen.getByText(/el volumen final se toma igual al diluyente agregado/)).toBeInTheDocument()
    expect(screen.getByText(AVISO_PABELLON)).toBeInTheDocument()
  })

  it('muestra la concentración por ml y la cantidad en el volumen de la dosis', async () => {
    await cefuroximaVial750('7,5', '1', '10')
    const estado = screen.getByRole('status')
    expect(estado).toHaveTextContent('Concentración final: 10 mg por ml')
    expect(estado).toHaveTextContent('En 0,1 ml hay 1 mg')
  })

  it('solo ofrece presentaciones que se preparan y pide completar los volúmenes antes de calcular', () => {
    montar('cefuroxima')
    const opciones = within(screen.getByLabelText('Presentación')).getAllByRole('option')
    expect(opciones).toHaveLength(2)
    expect(screen.getByRole('status')).toHaveTextContent('Completa los volúmenes de todos los pasos')
  })

  it('el polvo sin reconstituir avisa que primero se reconstituye', async () => {
    montar('cefuroxima')
    await userEvent.click(screen.getByRole('button', { name: 'Quitar paso 1' }))
    expect(screen.getByRole('status')).toHaveTextContent('Primero reconstituye el polvo')
  })

  it('permite hasta 4 pasos y después deshabilita Agregar paso', async () => {
    montar('cefuroxima')
    const agregar = screen.getByRole('button', { name: 'Agregar paso' })
    await userEvent.click(agregar)
    await userEvent.click(agregar)
    await userEvent.click(agregar)
    expect(screen.getAllByLabelText(/^Paso \d: tipo$/)).toHaveLength(4)
    expect(agregar).toBeDisabled()
  })

  it('un volumen que no se puede tomar muestra el error del cálculo, no una coincidencia', async () => {
    await cefuroximaVial750('7,5', '9', '10')
    const estado = screen.getByRole('status')
    expect(estado).toHaveTextContent('No puedes tomar más volumen del que tienes')
    expect(estado).not.toHaveTextContent('Coincide con')
  })
})
