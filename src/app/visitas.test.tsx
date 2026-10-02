import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Link, MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import ContadorVisitas from './visitas'

function montar() {
  return render(
    <MemoryRouter initialEntries={['/']}>
      <ContadorVisitas />
      <Link to="/m/noradrenalina">ir</Link>
    </MemoryRouter>,
  )
}

afterEach(() => {
  delete window.goatcounter
})

describe('ContadorVisitas', () => {
  it('no cuenta la primera pantalla (la cuenta el script al cargar) y sí cada navegación', async () => {
    const count = vi.fn()
    window.goatcounter = { count }
    montar()
    expect(count).not.toHaveBeenCalled()
    await userEvent.click(screen.getByText('ir'))
    expect(count).toHaveBeenCalledWith({ path: '/m/noradrenalina' })
  })

  it('sin el script (bloqueado o sin internet) no falla', async () => {
    montar()
    await userEvent.click(screen.getByText('ir'))
    expect(screen.getByText('ir')).toBeInTheDocument()
  })
})
