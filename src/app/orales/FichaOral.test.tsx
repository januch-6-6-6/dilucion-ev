import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fichaOralValida } from '../../esquema/__fixtures__/orales'
import { FichaOral as EsquemaFichaOral } from '../../esquema/ficha-oral'
import FichaOral from './FichaOral'

const { fichas } = vi.hoisted(() => ({ fichas: new Map<string, unknown>() }))

vi.mock('../../datos/cargarOrales', () => ({
  obtenerOral: (id: string) => fichas.get(id),
  fuentesOrales: [],
  verificacion: (f: { id: string }) => (f.id === 'unica' ? 'fuente_unica' : 'dos_fuentes'),
}))

const f = { ref: 'F1', detalle: 'p. 1' }
const crear = (id: string, extra: Record<string, unknown> = {}) => fichas.set(id, EsquemaFichaOral.parse(fichaOralValida(id, extra)))

function montar(id: string) {
  return render(
    <MemoryRouter initialEntries={[`/orales/m/${id}`]}>
      <Routes>
        <Route path="/orales/m/:id" element={<FichaOral />} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => {
  localStorage.clear()
  fichas.clear()
  crear('unica')
  crear('doble')
  crear('adulto', {
    dosis: [{ indicacion: 'Dolor', poblacion: 'adulto', regimen: 'fija', base: 'toma', unidad: 'mg', min: 500, estatus: 'off_label', fuente: f }],
    pediatria: { estado: 'solo_adulto', motivo: 'No hay dosis pediátrica en la fuente' },
  })
  crear('disc', {
    discrepancias: [
      {
        campo: 'dosis máxima diaria',
        valores: [
          { fuente: 'F1', valor: '4 g' },
          { fuente: 'F2', valor: '3 g' },
        ],
        mostrado: '3 g',
        motivo: 'Se muestra el valor más conservador',
      },
    ],
  })
  crear('presen', {
    presentaciones: [
      { id: 'lp', forma: 'comprimido', cantidad: { valor: 100, unidad: 'mg' }, partible: 'cuartos', liberacionProlongada: true, registroChile: 'sin_verificar', fuente: f },
      { id: 'nr', forma: 'capsula', cantidad: { valor: 50, unidad: 'mg' }, partible: 'no', liberacionProlongada: false, registroChile: 'no_registrado', fuente: f },
    ],
  })
})

describe('FichaOral', () => {
  it('una ficha de fuente única muestra el aviso arriba de las pestañas', () => {
    montar('unica')
    const nota = screen.getByRole('note')
    expect(nota).toHaveTextContent('Esta ficha se apoya en una sola fuente y no se pudo contrastar con otra.')
    const tabs = screen.getByRole('tablist')
    expect(nota.compareDocumentPosition(tabs) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('una ficha de dos fuentes no muestra el aviso', () => {
    montar('doble')
    expect(screen.queryByRole('note')).not.toBeInTheDocument()
  })

  it('una dosis restringida muestra «Solo con» con forma y concentración de cada presentación', () => {
    crear('restr', {
      dosis: [
        { indicacion: 'Dolor', poblacion: 'adulto', regimen: 'fija', base: 'toma', unidad: 'mg', max: 100, tomasPorDia: 3, estatus: 'autorizada', fuente: f, presentaciones: ['lp', 'nr'] },
        { indicacion: 'Dolor', poblacion: 'pediatrico', regimen: 'por_peso', base: 'toma', unidad: 'mg/kg', max: 1, tomasPorDia: 3, estatus: 'autorizada', fuente: f, presentaciones: ['lp'] },
      ],
      presentaciones: [
        { id: 'lp', forma: 'comprimido', cantidad: { valor: 100, unidad: 'mg' }, partible: 'cuartos', liberacionProlongada: true, registroChile: 'sin_verificar', fuente: f },
        { id: 'nr', forma: 'capsula', cantidad: { valor: 50, unidad: 'mg' }, partible: 'no', liberacionProlongada: false, registroChile: 'no_registrado', fuente: f },
        { id: 'jar', forma: 'jarabe', concentracion: { valor: 100, unidad: 'mg' }, partible: 'no', liberacionProlongada: false, registroChile: 'verificado', fuente: f },
      ],
    })
    montar('restr')
    expect(screen.getByText(/Solo con estas presentaciones: comprimido \(100 mg, liberación prolongada\); capsula \(50 mg\)/)).toBeInTheDocument()
    expect(screen.getByText(/Solo con la presentación: comprimido \(100 mg, liberación prolongada\)/)).toBeInTheDocument()
    expect(screen.queryByText(/jarabe/)).not.toBeInTheDocument()
  })

  it('M-2: si ningún id de la dosis resuelve, muestra «Sin presentación válida» y no «Solo con» vacío', () => {
    fichas.set('huerfana', fichaOralValida('huerfana', { dosis: [{ ...fichaOralValida().dosis[0], presentaciones: ['zzz'] }] }))
    montar('huerfana')
    expect(screen.getByText(/Sin presentación válida en la ficha/)).toBeInTheDocument()
    expect(screen.queryByText(/Solo con/)).not.toBeInTheDocument()
  })

  it('una dosis sin presentaciones no muestra «Solo con»', () => {
    montar('doble')
    expect(screen.queryByText(/Solo con:/)).not.toBeInTheDocument()
  })

  it('muestra las cinco pestañas', () => {
    montar('doble')
    for (const n of ['Dosis', 'Presentaciones', 'Administración', 'Discrepancias', 'Fuentes']) {
      expect(screen.getByRole('tab', { name: n })).toBeInTheDocument()
    }
  })

  it('solo_adulto muestra el motivo y no el enlace de calculadora', () => {
    montar('adulto')
    expect(screen.getByText(/No hay dosis pediátrica en la fuente/)).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Calculadora/ })).not.toBeInTheDocument()
  })

  it('con_dosis muestra el enlace a la calculadora', () => {
    montar('doble')
    expect(screen.getByRole('link', { name: /Calculadora/ })).toHaveAttribute('href', '/orales/m/doble/calcular')
  })

  it('cada dosis muestra Autorizada u Off-label', () => {
    montar('adulto')
    expect(screen.getByText('Off-label')).toBeInTheDocument()
    montar('doble')
    expect(screen.getAllByText('Autorizada').length).toBe(2)
  })

  it('Presentaciones muestra partible, liberación prolongada y registro en Chile', async () => {
    montar('presen')
    await userEvent.click(screen.getByRole('tab', { name: 'Presentaciones' }))
    expect(screen.getByText('Liberación prolongada')).toBeInTheDocument()
    expect(screen.getByText(/cuartos/)).toBeInTheDocument()
    expect(screen.getByText('Sin verificar')).toBeInTheDocument()
    expect(screen.getByText('No registrado')).toBeInTheDocument()
  })

  it('la forma se muestra legible: «Comprimido efervescente»', async () => {
    crear('efer', {
      presentaciones: [{ id: 'ef', forma: 'comprimido_efervescente', cantidad: { valor: 1, unidad: 'g' }, partible: 'no', liberacionProlongada: false, registroChile: 'verificado', fuente: f }],
    })
    montar('efer')
    await userEvent.click(screen.getByRole('tab', { name: 'Presentaciones' }))
    expect(screen.getByText(/Comprimido efervescente/)).toBeInTheDocument()
  })

  it('una dosis por edad con min, max y texto muestra los tres', () => {
    crear('edad', {
      dosis: [
        { indicacion: 'Dolor', poblacion: 'adulto', regimen: 'fija', base: 'toma', unidad: 'mg', min: 500, estatus: 'autorizada', fuente: f },
        { indicacion: 'Fiebre', poblacion: 'pediatrico', regimen: 'por_edad', base: 'toma', unidad: 'mg', min: 80, max: 120, texto: 'De 1 a 3 años', estatus: 'autorizada', fuente: f },
      ],
    })
    montar('edad')
    const dato = screen.getByText('Fiebre').closest('.dato') as HTMLElement
    expect(dato).toHaveTextContent('80–120 mg')
    expect(dato).toHaveTextContent('por toma')
    expect(dato).toHaveTextContent('De 1 a 3 años')
  })

  it('registro verificado se rotula Verificado', async () => {
    montar('doble')
    await userEvent.click(screen.getByRole('tab', { name: 'Presentaciones' }))
    expect(screen.getAllByText('Verificado').length).toBe(2)
  })

  it('Discrepancias muestra una fila por campo con cada valor y el mostrado', async () => {
    montar('disc')
    await userEvent.click(screen.getByRole('tab', { name: 'Discrepancias' }))
    const tabla = screen.getByRole('table')
    const fila = within(tabla).getByRole('row', { name: /dosis máxima diaria/ })
    expect(fila).toHaveTextContent('4 g')
    expect(fila).toHaveTextContent('3 g')
    expect(fila).toHaveTextContent('Se muestra el valor más conservador')
    expect(within(tabla).getAllByRole('row').length).toBe(2) // encabezado + 1
  })

  it('sin discrepancias muestra el estado vacío', async () => {
    montar('doble')
    await userEvent.click(screen.getByRole('tab', { name: 'Discrepancias' }))
    expect(screen.getByText('Sin discrepancias entre las fuentes')).toBeInTheDocument()
  })

  it('id inexistente muestra «Medicamento no encontrado»', () => {
    montar('no-existe')
    expect(screen.getByText('Medicamento no encontrado')).toBeInTheDocument()
  })

  it('la estrella alterna el favorito y se registra el reciente al abrir', async () => {
    montar('doble')
    expect(localStorage.getItem('dilucion-ev:recientes')).toContain('oral:doble')
    const estrella = screen.getByRole('button', { name: 'Favorito' })
    expect(estrella).toHaveAttribute('aria-pressed', 'false')
    await userEvent.click(estrella)
    expect(estrella).toHaveAttribute('aria-pressed', 'true')
    expect(localStorage.getItem('dilucion-ev:favoritos')).toContain('oral:doble')
  })
})
