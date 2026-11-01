import { describe, expect, it } from 'vitest'
import { masaAMl } from '../calculos/oralConversion'
import { validarOrales } from '../esquema/validar-orales'
import { fuentesOrales, obtenerOral, orales, verificacion } from './cargarOrales'

const ESPERADOS_FUENTE_UNICA = [
  'carbamazepina',
  'ciclobenzaprina',
  'doxiciclina',
  'empagliflozina',
  'escitalopram',
  'flucloxacilina',
  'gemfibrozilo',
  'isosorbide',
  'minociclina',
  'mirtazapina',
  'paracetamol-tramadol',
  'quetiapina',
  'sertralina',
  'tramadol',
  'trimebutino',
  'vildagliptina',
  'zopiclona',
].sort()

const ESPERADOS_SOLO_ADULTO = [
  'acido-acetilsalicilico',
  'ciclobenzaprina',
  'domperidona',
  'doxiciclina',
  'escitalopram',
  'famciclovir',
  'gemfibrozilo',
  'isosorbide',
  'levonorgestrel',
  'minociclina',
  'mirtazapina',
  'paracetamol-tramadol',
  'quetiapina',
  'venlafaxina',
  'vildagliptina',
  'zopiclona',
].sort()

const ESPERADOS_ALTO_RIESGO = [
  'clonazepam',
  'diazepam',
  'fenobarbital',
  'morfina',
  'paracetamol-tramadol',
  'tramadol',
].sort()

describe('datos reales de medicamentos orales', () => {
  it('hay exactamente 86 fichas orales y ningún id está repetido', () => {
    expect(orales).toHaveLength(86)
    const ids = orales.map((o) => o.id)
    expect(new Set(ids).size).toBe(86)
  })

  it('validarOrales sobre los datos reales no da errores', () => {
    const errores = validarOrales(orales, fuentesOrales)
    expect(errores).toEqual([])
  })

  it('los ids con verificacion fuente_unica son exactamente los 17 esperados', () => {
    const fuenteUnica = orales
      .filter((o) => verificacion(o) === 'fuente_unica')
      .map((o) => o.id)
      .sort()
    expect(fuenteUnica).toEqual(ESPERADOS_FUENTE_UNICA)
  })

  it('los ids solo_adulto son exactamente los 16 esperados', () => {
    const soloAdulto = orales
      .filter((o) => o.pediatria.estado === 'solo_adulto')
      .map((o) => o.id)
      .sort()
    expect(soloAdulto).toEqual(ESPERADOS_SOLO_ADULTO)
  })

  it('los ids altoRiesgo son exactamente los 6 esperados', () => {
    const altoRiesgo = orales
      .filter((o) => o.altoRiesgo)
      .map((o) => o.id)
      .sort()
    expect(altoRiesgo).toEqual(ESPERADOS_ALTO_RIESGO)
  })

  it('toda presentación líquida tiene concentración y toda de gotas tiene gotasPorMl', () => {
    const formasLiquidas = new Set(['jarabe', 'gotas', 'suspension', 'solucion'])
    for (const ficha of orales) {
      for (const p of ficha.presentaciones) {
        if (formasLiquidas.has(p.forma)) {
          expect(p.concentracion, `${ficha.id}.${p.id} debe tener concentración`).toBeDefined()
        }
        if (p.forma === 'gotas') {
          expect(p.gotasPorMl, `${ficha.id}.${p.id} debe tener gotasPorMl`).toBeDefined()
        }
      }
    }
  })

  it('ninguna ficha tiene meta.revisadoPor y todas las presentaciones están en sin_verificar, salvo las sin registro', () => {
    const SIN_REGISTRO = ['famciclovir', 'metazolamida']
    for (const ficha of orales) {
      expect(ficha.meta?.revisadoPor).toBeUndefined()
      for (const p of ficha.presentaciones) {
        expect(p.registroChile, `${ficha.id}.${p.id}`).toBe(SIN_REGISTRO.includes(ficha.id) ? 'no_registrado' : 'sin_verificar')
      }
    }
  })

  it('11 orales llevan usos oftalmologia y cada uno tiene al menos una dosis oftálmica', () => {
    const OFTALMICOS = [
      'acetazolamida', 'aciclovir', 'azitromicina', 'cotrimoxazol', 'doxiciclina', 'famciclovir',
      'metazolamida', 'minociclina', 'pirimetamina', 'prednisona', 'valaciclovir',
    ]
    const conUso = orales.filter((o) => o.usos?.includes('oftalmologia')).map((o) => o.id).sort()
    expect(conUso).toEqual(OFTALMICOS)
    for (const id of OFTALMICOS) {
      const ficha = obtenerOral(id)!
      expect(ficha.dosis.some((d) => d.oftalmica), `${id} sin dosis oftálmica`).toBe(true)
    }
    // ninguna ficha fuera de las 11 puede traer dosis oftálmicas (el validador ya lo exige; aquí se fija el conjunto)
    const huerfanas = orales.filter((o) => !o.usos && o.dosis.some((d) => d.oftalmica))
    expect(huerfanas).toEqual([])
  })

  it('las dosis oftálmicas de las 4 fichas preexistentes se suman sin tocar las dosis anteriores', () => {
    const previas = { aciclovir: 10, azitromicina: 4, prednisona: 3, cotrimoxazol: 4 }
    for (const [id, n] of Object.entries(previas)) {
      const ficha = obtenerOral(id)!
      expect(ficha.dosis.filter((d) => !d.oftalmica), id).toHaveLength(n)
      expect(ficha.dosis.filter((d) => d.oftalmica).length, id).toBeGreaterThan(0)
    }
  })

  it('la lactulosa se convierte: 10 g con su concentración da entre 14,9 y 15,1 ml', () => {
    const lactulosa = obtenerOral('lactulosa')
    expect(lactulosa).toBeDefined()
    const presentacion = lactulosa!.presentaciones.find((p) => p.concentracion)
    expect(presentacion).toBeDefined()
    const r = masaAMl({ valor: 10, unidad: 'g' }, presentacion!)
    expect(r.ok).toBe(true)
    if (r.ok) {
      expect(r.valor).toBeGreaterThan(14.9)
      expect(r.valor).toBeLessThan(15.1)
    }
  })

  it('la morfina en gotas declara su concentración', () => {
    const morfina = obtenerOral('morfina')
    expect(morfina).toBeDefined()
    const gotas = morfina!.presentaciones.find((p) => p.id.includes('gotas'))
    expect(gotas).toBeDefined()
    expect(gotas!.concentracion).toBeDefined()
  })
})
