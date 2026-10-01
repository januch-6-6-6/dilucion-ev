import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { AVISO } from '../aviso'
import Acerca from './Acerca'

describe('Acerca', () => {
  it('muestra el aviso, la versión y las fuentes', () => {
    render(<MemoryRouter><Acerca /></MemoryRouter>)
    expect(screen.getByText(AVISO)).toBeInTheDocument()
    expect(screen.getByText(/Versión 0\.1\.0/)).toBeInTheDocument()
    expect(screen.getByText(/PUCON-2022/)).toBeInTheDocument()
  })

  it('permite cambiar a tema oscuro', async () => {
    render(<MemoryRouter><Acerca /></MemoryRouter>)
    await userEvent.selectOptions(screen.getByLabelText('Tema'), 'oscuro')
    expect(document.documentElement).toHaveAttribute('data-theme', 'oscuro')
  })
})
