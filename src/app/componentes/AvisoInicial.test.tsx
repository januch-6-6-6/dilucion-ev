import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { AVISO } from '../aviso'
import AvisoInicial from './AvisoInicial'

describe('AvisoInicial', () => {
  it('el texto del aviso es el exacto del diseño', () =>
    expect(AVISO).toBe('Material de formación. No reemplaza el protocolo local ni la indicación médica. Verifique siempre con la fuente y la normativa de su institución.'))

  it('se muestra en la primera apertura y no vuelve tras aceptarlo', async () => {
    const { unmount } = render(<AvisoInicial />)
    expect(screen.getByRole('dialog')).toHaveTextContent(AVISO)
    await userEvent.click(screen.getByRole('button', { name: 'Entendido' }))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    unmount()
    render(<AvisoInicial />)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })
})
