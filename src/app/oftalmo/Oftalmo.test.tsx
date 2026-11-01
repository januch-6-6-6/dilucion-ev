import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it } from 'vitest'
import { oculares } from '../../datos/cargarOculares'
import CentroOftalmologia from './CentroOftalmologia'
import FichaOcular from './FichaOcular'
import { esFavoritoOcular } from './guardadoOculares'
import { AVISO_CIRUJANO, AVISO_FORMACION, AVISO_NO_REGISTRADO, AVISO_PABELLON, AVISO_SIN_PASOS } from './textos'

// Usa los datos reales (datos/oftalmo, orales y tópicos): así la prueba cubre también los cargadores.
function montar(ruta: string) {
  return render(
    <MemoryRouter initialEntries={[ruta]}>
      <Routes>
        <Route path="/oftalmologia" element={<CentroOftalmologia />} />
        <Route path="/oftalmologia/m/:id" element={<FichaOcular />} />
        <Route path="/oftalmologia/m/:id/verificar" element={<p>página del verificador</p>} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => localStorage.clear())

describe('CentroOftalmologia', () => {
  it('muestra las 3 pestañas y Pabellón agrupa por familia', () => {
    montar('/oftalmologia')
    expect(screen.getAllByRole('tab').map((t) => t.textContent)).toEqual(['Pabellón', 'Orales', 'Colirios'])
    const grupos = screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent)
    expect(grupos).toEqual(['Intracamerales', 'Intravítreas', 'Bloqueos', 'Perioculares', 'Antifibróticos y toxina'])
    expect(screen.getAllByRole('link').filter((a) => a.getAttribute('href')?.startsWith('/oftalmologia/m/'))).toHaveLength(41)
  })

  it('muestra los avisos de formación y de pabellón', () => {
    montar('/oftalmologia')
    expect(screen.getByText(AVISO_FORMACION)).toBeInTheDocument()
    expect(screen.getByText(AVISO_PABELLON)).toBeInTheDocument()
  })

  it('pestaña Orales lista 11 y enlaza a /orales/m/:id', async () => {
    montar('/oftalmologia')
    await userEvent.click(screen.getByRole('tab', { name: 'Orales' }))
    const enlaces = screen.getAllByRole('link').filter((a) => a.getAttribute('href')?.startsWith('/orales/m/'))
    expect(enlaces).toHaveLength(11)
    expect(screen.getByRole('link', { name: /Acetazolamida/ })).toHaveAttribute('href', '/orales/m/acetazolamida')
  })

  it('pestaña Colirios solo trae tópicos con vía ojo', async () => {
    montar('/oftalmologia')
    await userEvent.click(screen.getByRole('tab', { name: 'Colirios' }))
    expect(screen.getByRole('link', { name: /Timolol oftálmico/ })).toHaveAttribute('href', '/topicos/m/timolol')
    expect(screen.queryByRole('link', { name: /Mometasona nasal/ })).not.toBeInTheDocument()
    const enlaces = screen.getAllByRole('link').filter((a) => a.getAttribute('href')?.startsWith('/topicos/m/'))
    expect(enlaces.length).toBeGreaterThan(3)
  })

  it('busca por nombre comercial dentro de Pabellón', async () => {
    montar('/oftalmologia')
    await userEvent.type(screen.getByRole('searchbox'), 'lucentis')
    const enlaces = screen.getAllByRole('link').filter((a) => a.getAttribute('href')?.startsWith('/oftalmologia/m/'))
    expect(enlaces).toHaveLength(1)
    expect(enlaces[0]).toHaveAttribute('href', '/oftalmologia/m/ranibizumab')
  })
})

describe('FichaOcular', () => {
  it('cefuroxima muestra el protocolo con fuente y el botón Verificar mi preparación', async () => {
    montar('/oftalmologia/m/cefuroxima')
    expect(screen.getByRole('link', { name: 'Verificar mi preparación' })).toHaveAttribute('href', '/oftalmologia/m/cefuroxima/verificar')
    await userEvent.click(screen.getByRole('tab', { name: 'Preparación' }))
    expect(screen.getByText('Desde el vial de 750 mg (PNT SEFH)')).toBeInTheDocument()
    expect(screen.getAllByText(/\[SEFH-PNT-PN-CEFUROXIMA-INTRACAMERULAR\]/).length).toBeGreaterThan(0)
  })

  it('una ficha informativa (bupivacaína) no muestra Verificar', () => {
    montar('/oftalmologia/m/bupivacaina')
    expect(screen.queryByRole('link', { name: 'Verificar mi preparación' })).not.toBeInTheDocument()
  })

  it('una ficha usoDirecto (ranibizumab) no muestra Verificar y sí la alerta de eliminar el exceso', async () => {
    montar('/oftalmologia/m/ranibizumab')
    expect(screen.queryByRole('link', { name: 'Verificar mi preparación' })).not.toBeInTheDocument()
    await userEvent.click(screen.getByRole('tab', { name: 'Alertas' }))
    expect(screen.getAllByText(/elimina el exceso/).length).toBeGreaterThan(0)
  })

  it('carbacol muestra AVISO_NO_REGISTRADO', () => {
    montar('/oftalmologia/m/carbacol')
    expect(screen.getByText(AVISO_NO_REGISTRADO)).toBeInTheDocument()
  })

  it('una ficha registrada no muestra AVISO_NO_REGISTRADO', () => {
    montar('/oftalmologia/m/cefuroxima')
    expect(screen.queryByText(AVISO_NO_REGISTRADO)).not.toBeInTheDocument()
  })

  it('amikacina muestra AVISO_SIN_PASOS y cefuroxima no', () => {
    montar('/oftalmologia/m/amikacina')
    expect(screen.getByText(AVISO_SIN_PASOS)).toBeInTheDocument()
  })

  it('cefuroxima no muestra AVISO_SIN_PASOS porque sí tiene protocolo', () => {
    montar('/oftalmologia/m/cefuroxima')
    expect(screen.queryByText(AVISO_SIN_PASOS)).not.toBeInTheDocument()
  })

  it('mitomicina muestra AVISO_CIRUJANO', () => {
    montar('/oftalmologia/m/mitomicina')
    expect(screen.getByText(AVISO_CIRUJANO)).toBeInTheDocument()
  })

  it('toda ficha muestra AVISO_FORMACION y AVISO_PABELLON y la marca de alto riesgo', () => {
    for (const o of oculares) {
      const { unmount } = montar(`/oftalmologia/m/${o.id}`)
      expect(screen.getByText(AVISO_FORMACION), o.id).toBeInTheDocument()
      expect(screen.getByText(AVISO_PABELLON), o.id).toBeInTheDocument()
      expect(screen.getByText('Alto riesgo'), o.id).toBeInTheDocument()
      unmount()
    }
  })

  it('triamcinolona rotula 40 mg en 1 ml como concentración de referencia, nunca como «Dosis final»', () => {
    montar('/oftalmologia/m/triamcinolona')
    expect(screen.queryByText(/Dosis final/)).not.toBeInTheDocument()
    expect(screen.getAllByText(/Concentración de referencia: 40 mg en 1 ml/).length).toBeGreaterThan(0)
  })

  it('la ficha de toxina botulínica muestra la vía intramuscular con su etiqueta', () => {
    montar('/oftalmologia/m/toxina-botulinica')
    expect(screen.getAllByText(/Intramuscular/).length).toBeGreaterThan(0)
  })

  it('mepivacaína (sin pauta) explica que no hay pauta y no ofrece Verificar', () => {
    montar('/oftalmologia/m/mepivacaina')
    expect(screen.getAllByText(/Ficha informativa/).length).toBeGreaterThan(0)
    expect(screen.queryByRole('link', { name: 'Verificar mi preparación' })).not.toBeInTheDocument()
  })

  it('una ficha de fuente única muestra el aviso y el favorito se guarda con prefijo oft:', async () => {
    montar('/oftalmologia/m/toxina-botulinica')
    expect(screen.getByText(/una sola fuente/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Favorito' }))
    expect(esFavoritoOcular('toxina-botulinica')).toBe(true)
    expect(JSON.stringify(localStorage)).toContain('oft:toxina-botulinica')
  })

  it('la pestaña Discrepancias muestra la tabla de moxifloxacino', async () => {
    montar('/oftalmologia/m/moxifloxacino')
    await userEvent.click(screen.getByRole('tab', { name: 'Discrepancias' }))
    expect(within(screen.getByRole('tabpanel')).getByRole('table')).toBeInTheDocument()
  })

  it('un id inexistente dice que no se encontró', () => {
    montar('/oftalmologia/m/no-existe')
    expect(screen.getByText('Medicamento no encontrado')).toBeInTheDocument()
  })
})
