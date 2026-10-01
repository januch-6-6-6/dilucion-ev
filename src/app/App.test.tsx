import { render, screen } from '@testing-library/react'
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
})
