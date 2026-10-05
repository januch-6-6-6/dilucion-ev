import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { FichaOral } from '../../esquema/ficha-oral'
import { fichaOralValida } from '../../esquema/__fixtures__/orales'
import { alternarFavoritoOral, registrarRecienteOral } from './guardadoOrales'
import ListaOrales from './ListaOrales'

const datos = vi.hoisted(() => ({ orales: [] as unknown[] }))
vi.mock('../../datos/cargarOrales', () => ({
  get orales() {
    return datos.orales
  },
  obtenerOral: (id: string) => (datos.orales as FichaOral[]).find((o) => o.id === id),
  verificacion: (f: { id: string }) => (f.id === 'ketorolaco' ? 'fuente_unica' : 'dos_fuentes'),
}))

const ficha = (id: string, extra: Record<string, unknown> = {}) => fichaOralValida(id, { grupo: 'analgesico-no-opioide', ...extra }) as unknown as FichaOral

function montar() {
  return render(
    <MemoryRouter>
      <ListaOrales />
    </MemoryRouter>,
  )
}

describe('ListaOrales', () => {
  beforeEach(() => {
    localStorage.clear()
    datos.orales = [ficha('ketorolaco'), ficha('paracetamol')]
  })

  it('buscar «ketorolaco» lista el oral con enlace a /orales/m/ketorolaco', async () => {
    montar()
    await userEvent.type(screen.getByRole('searchbox'), 'ketorolaco')
    const enlace = screen.getByRole('link', { name: /ketorolaco/i })
    expect(enlace).toHaveAttribute('href', '/orales/m/ketorolaco')
  })

  it('una ficha de fuente única muestra «Una sola fuente»', async () => {
    montar()
    await userEvent.type(screen.getByRole('searchbox'), 'ketorolaco')
    expect(screen.getByText('Una sola fuente')).toBeInTheDocument()
  })

  it('una ficha con dos fuentes no muestra «Una sola fuente»', async () => {
    montar()
    await userEvent.type(screen.getByRole('searchbox'), 'paracetamol')
    expect(screen.queryByText('Una sola fuente')).not.toBeInTheDocument()
  })

  it('sin orales muestra «No hay medicamentos para mostrar»', async () => {
    datos.orales = []
    montar()
    await userEvent.type(screen.getByRole('searchbox'), 'x')
    expect(screen.getByText(/No hay medicamentos para mostrar/)).toBeInTheDocument()
  })

  it('muestra favoritos y recientes de guardadoOrales', () => {
    alternarFavoritoOral('ketorolaco')
    registrarRecienteOral('paracetamol')
    montar()
    expect(screen.getByRole('heading', { name: 'Mis favoritos' })).toBeInTheDocument()
    expect(screen.getByRole('list', { name: 'Medicamentos favoritos' })).toHaveTextContent('ketorolaco')
    expect(screen.getByRole('heading', { name: 'Últimos consultados' })).toBeInTheDocument()
    expect(screen.getByRole('list', { name: 'Medicamentos consultados recientemente' })).toHaveTextContent('paracetamol')
  })

  it('agrupa la lista por grupo', () => {
    montar()
    expect(screen.getByRole('heading', { name: 'Analgésicos no opioides' })).toBeInTheDocument()
  })
})
