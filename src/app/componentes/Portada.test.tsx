/// <reference types="node" />
import { existsSync, statSync } from 'node:fs'
import { join } from 'node:path'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { AVISO } from '../aviso'
import { CAPTURAS } from '../capturas'
import Inicio from '../paginas/Inicio'
import { Capturas } from './Portada'

const montar = () =>
  render(
    <MemoryRouter>
      <Inicio />
    </MemoryRouter>,
  )

describe('Portada', () => {
  it('muestra el aviso de formación, también mientras se busca', async () => {
    montar()
    expect(screen.getByRole('note')).toHaveTextContent(AVISO)
    await userEvent.type(screen.getByRole('searchbox', { name: /buscar/i }), 'fenta')
    expect(screen.getByRole('note')).toHaveTextContent(AVISO)
  })

  it('presenta cuatro beneficios con íconos decorativos', () => {
    montar()
    const lista = screen.getByRole('region', { name: 'Qué encontrarás' })
    const items = within(lista).getAllByRole('listitem')
    expect(items).toHaveLength(4)
    for (const item of items) expect(item.querySelector('svg')).toHaveAttribute('aria-hidden', 'true')
  })

  it('la búsqueda sigue siendo lo primero de la página', () => {
    montar()
    const buscador = screen.getByRole('searchbox', { name: /buscar/i })
    const beneficios = screen.getByRole('region', { name: 'Qué encontrarás' })
    expect(buscador.compareDocumentPosition(beneficios) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('al buscar se ocultan beneficios y capturas', async () => {
    montar()
    await userEvent.type(screen.getByRole('searchbox', { name: /buscar/i }), 'nora')
    expect(screen.queryByRole('region', { name: 'Qué encontrarás' })).not.toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'Así funciona' })).not.toBeInTheDocument()
  })
})

describe('Capturas de funcionamiento', () => {
  it('cada captura tiene texto alternativo que empieza con su titular y tamaño reservado', () => {
    render(<Capturas />)
    const imgs = within(screen.getByRole('list', { name: 'Capturas de la app' })).getAllByRole('img')
    expect(imgs).toHaveLength(CAPTURAS.length)
    imgs.forEach((img, i) => {
      expect(img.getAttribute('alt')?.startsWith(CAPTURAS[i].titular)).toBe(true)
      expect(img).toHaveAttribute('width', '540')
      expect(img).toHaveAttribute('height', '1080')
      expect(img).toHaveAttribute('loading', 'lazy')
    })
  })

  it('el carril se puede enfocar con teclado y tiene botones con nombre', async () => {
    render(<Capturas />)
    expect(screen.getByRole('list', { name: 'Capturas de la app' })).toHaveAttribute('tabindex', '0')
    // jsdom no implementa scrollBy: los botones no deben romper nada
    await userEvent.click(screen.getByRole('button', { name: 'Captura siguiente' }))
    await userEvent.click(screen.getByRole('button', { name: 'Captura anterior' }))
  })

  it.each(CAPTURAS.map((c) => c.id))('public/capturas/%s.webp existe y pesa ≤ 120 KB', (id) => {
    const archivo = join(process.cwd(), 'public/capturas', `${id}.webp`)
    expect(existsSync(archivo)).toBe(true)
    expect(statSync(archivo).size).toBeLessThanOrEqual(120 * 1024)
  })
})
