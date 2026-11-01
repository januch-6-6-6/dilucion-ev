import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders el título "Dilución EV"', () => {
    render(<App />)
    expect(screen.getByRole('heading', { name: 'Dilución EV' })).toBeInTheDocument()
  })
  it('el pie de página muestra al autor', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toHaveTextContent('Creado por Héctor Salvo Agüero')
  })
  it('muestra la navegación de secciones EV y Orales', () => {
    render(<App />)
    const nav = screen.getByRole('navigation', { name: 'Secciones' })
    expect(within(nav).getByRole('link', { name: 'EV' })).toHaveAttribute('href', '#/')
    expect(within(nav).getByRole('link', { name: 'Orales' })).toHaveAttribute('href', '#/orales')
  })
  it('la navegación tiene Oftalmología después de Tópicos', () => {
    render(<App />)
    const nav = screen.getByRole('navigation', { name: 'Secciones' })
    const textos = within(nav).getAllByRole('link').map((a) => a.textContent)
    expect(textos).toEqual(['EV', 'Orales', 'Tópicos', 'Oftalmología'])
    expect(within(nav).getByRole('link', { name: 'Oftalmología' })).toHaveAttribute('href', '#/oftalmologia')
  })
  it('/oftalmologia/m/cefuroxima renderiza la ficha y /oftalmologia el centro', async () => {
    window.location.hash = '#/oftalmologia/m/cefuroxima'
    const { unmount } = render(<App />)
    expect(await screen.findByRole('heading', { name: /Cefuroxima intracameral/ })).toBeInTheDocument()
    unmount()
    window.location.hash = '#/oftalmologia'
    render(<App />)
    expect(await screen.findByRole('tab', { name: 'Pabellón' })).toBeInTheDocument()
    window.location.hash = ''
  })
  it('/oftalmologia/m/cefuroxima/verificar renderiza el verificador', async () => {
    window.location.hash = '#/oftalmologia/m/cefuroxima/verificar'
    render(<App />)
    expect(await screen.findByRole('heading', { name: /Verificar mi preparación/ })).toBeInTheDocument()
    window.location.hash = ''
  })
  it('«Orales» queda activa en rutas que empiezan por /orales', async () => {
    window.location.hash = '#/orales'
    render(<App />)
    const nav = screen.getByRole('navigation', { name: 'Secciones' })
    expect(within(nav).getByRole('link', { name: 'Orales' })).toHaveAttribute('aria-current', 'page')
    expect(within(nav).getByRole('link', { name: 'EV' })).not.toHaveAttribute('aria-current')
    window.location.hash = ''
  })
  it('la presentación de la portada aparece solo en el inicio', () => {
    window.location.hash = '#/'
    const { unmount } = render(<App />)
    expect(screen.getByRole('banner')).toHaveTextContent(/Para estudiantes, TENS y equipos de enfermería en formación: 89 medicamentos/)
    unmount()
    window.location.hash = '#/acerca'
    render(<App />)
    expect(screen.getByRole('banner')).not.toHaveTextContent('Para estudiantes')
    window.location.hash = ''
  })
})
