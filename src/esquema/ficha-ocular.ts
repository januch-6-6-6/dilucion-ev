import { z } from 'zod'
import { FuenteRef } from './ficha'
import { Discrepancia } from './ficha-topica'

const positivo = z.number().positive()
const ids = z.array(z.string().min(1)).min(1)

export const UnidadOcular = z.enum(['mg', 'mcg', 'UI', 'U'])
export const CantidadOcular = z.strictObject({ valor: positivo, unidad: UnidadOcular })
export const RangoOcular = z
  .strictObject({ min: positivo, max: positivo, unidad: UnidadOcular })
  .refine((r) => r.max >= r.min, { message: 'el máximo no puede ser menor que el mínimo' })
export const DosisFinal = z.strictObject({ cantidad: z.union([CantidadOcular, RangoOcular]), volumenMl: positivo })

export const FamiliaOcular = z.enum(['intracameral', 'intravitreo', 'bloqueo', 'periocular', 'antifibrotico'])
export const ViaOcular = z.enum([
  'intracameral',
  'intravitrea',
  'subconjuntival',
  'subtenoniana',
  'subretiniana',
  'retrobulbar',
  'peribulbar',
  'intralesional',
  'topica_intraoperatoria',
])
export const FormaOcular = z.enum(['polvo', 'solucion', 'suspension', 'implante', 'jeringa_precargada'])

export const PresentacionOcular = z.strictObject({
  id: z.string().regex(/^[a-z0-9-]+$/),
  forma: FormaOcular,
  cantidad: CantidadOcular,
  volumenMl: positivo.optional(),
  registrosIsp: z.array(z.string().min(1)),
  /** Ya viene a la concentración de uso (Lucentis, Eylia, Vabysmo, Ozurdex, Mydrane). */
  usoDirecto: z.boolean(),
  sinConservantes: z.boolean().optional(),
  nota: z.string().min(1).optional(),
  fuente: FuenteRef,
})

export const DosisOcular = z.strictObject({
  indicacion: z.string().min(1),
  via: ViaOcular,
  poblacion: z.enum(['adulto', 'pediatrico']),
  final: DosisFinal.optional(),
  texto: z.string().min(1),
  estatus: z.enum(['autorizada', 'off_label']),
  condicion: z.string().min(1).optional(),
  presentaciones: ids.optional(),
  fuente: FuenteRef,
  tambien: z.array(FuenteRef).optional(),
})

export const Paso = z.discriminatedUnion('tipo', [
  z.strictObject({ tipo: z.literal('reconstituir'), diluyente: z.string().min(1), volumenMl: positivo }),
  z.strictObject({ tipo: z.literal('diluir'), tomarMl: positivo, llevarAMl: positivo, diluyente: z.string().min(1) }),
  z.strictObject({ tipo: z.literal('cargar'), volumenMl: positivo }),
  z.strictObject({ tipo: z.literal('texto'), texto: z.string().min(1) }),
])

export const ProtocoloOcular = z.strictObject({
  id: z.string().regex(/^[a-z0-9-]+$/),
  /** Índice de la dosis (en `dosis`) que este protocolo prepara. */
  dosis: z.number().int().min(0),
  titulo: z.string().min(1),
  partida: z.string().min(1),
  pasos: z.array(Paso).min(1),
  resultado: z.strictObject({ valor: positivo, unidad: UnidadOcular, volumenMl: positivo }),
  fuente: FuenteRef,
})

/** Factor para pasar de `de` a `a`; null si las unidades no son comparables (UI o U solo con la misma). */
export function convertirOcular(valor: number, de: UnidadOcular, a: UnidadOcular): number | null {
  if (de === a) return valor
  const masa: Record<string, number> = { mg: 1000, mcg: 1 }
  if (de in masa && a in masa) return (valor * masa[de]) / masa[a]
  return null
}

export const TOLERANCIA_OCULAR = 0.05

export const FichaOcular = z
  .strictObject({
    id: z.string().regex(/^[a-z0-9-]+$/),
    nombre: z.string().min(1),
    comerciales: z.array(z.string()),
    grupo: z.string().min(1),
    familias: z.array(FamiliaOcular).min(1),
    modo: z.enum(['intraocular', 'informativa']),
    componentes: z.array(z.string().min(1)),
    altoRiesgo: z.literal(true),
    registroChile: z.enum(['verificado', 'no_registrado']),
    presentaciones: z.array(PresentacionOcular).min(1),
    dosis: z.array(DosisOcular),
    protocolos: z.array(ProtocoloOcular),
    sinPauta: z.strictObject({ motivo: z.string().min(1) }).nullable(),
    pediatria: z.strictObject({
      estado: z.enum(['con_dosis', 'no_establecida', 'contraindicada', 'sin_datos']),
      motivo: z.string().min(1),
    }),
    conservacion: z.array(z.strictObject({ texto: z.string().min(1), horas: positivo.optional(), fuente: FuenteRef })),
    contraindicaciones: z.array(z.string().min(1)),
    alertas: z.array(z.string().min(1)),
    discrepancias: z.array(Discrepancia),
    meta: z.strictObject({ revisadoPor: z.string().optional(), fechaRevision: z.string().optional() }),
  })
  .superRefine((f, ctx) => {
    const err = (path: (string | number)[], message: string) => ctx.addIssue({ code: 'custom', path, message })
    const hayPediatrica = f.dosis.some((d) => d.poblacion === 'pediatrico')
    if (f.pediatria.estado === 'con_dosis' && !hayPediatrica) err(['dosis'], 'con_dosis exige al menos una dosis pediátrica')
    if (f.pediatria.estado !== 'con_dosis' && hayPediatrica) {
      err(['dosis'], `con pediatría ${f.pediatria.estado} no puede haber dosis pediátricas`)
    }
    if (f.sinPauta && f.dosis.length > 0) err(['dosis'], 'una ficha sin pauta no puede tener dosis')
    if (!f.sinPauta && f.dosis.length === 0) err(['dosis'], 'sin dosis hay que declarar sinPauta con su motivo')
    if (f.modo === 'intraocular' && !f.sinPauta && !f.dosis.some((d) => d.final)) {
      err(['dosis'], 'una ficha intraocular exige al menos una dosis con final')
    }
    if (f.modo === 'informativa' && f.protocolos.length > 0) err(['protocolos'], 'una ficha informativa no tiene protocolos')
    if (f.registroChile === 'verificado' && !f.presentaciones.some((p) => p.registrosIsp.length > 0)) {
      err(['presentaciones'], 'registroChile verificado exige registrosIsp en alguna presentación')
    }
    f.presentaciones.forEach((p, j) => {
      if (p.usoDirecto && p.volumenMl === undefined) err(['presentaciones', j, 'volumenMl'], 'usoDirecto exige volumenMl')
    })
    const existe = new Set(f.presentaciones.map((p) => p.id))
    f.dosis.forEach((d, j) =>
      d.presentaciones?.forEach((id, k) => {
        if (!existe.has(id)) err(['dosis', j, 'presentaciones', k], `la presentación "${id}" no existe en presentaciones de esta ficha`)
      }),
    )
    f.protocolos.forEach((p, j) => {
      if (!existe.has(p.partida)) err(['protocolos', j, 'partida'], `la presentación "${p.partida}" no existe en presentaciones de esta ficha`)
      const d = f.dosis[p.dosis]
      if (!d) return err(['protocolos', j, 'dosis'], 'el protocolo apunta a una dosis que no existe')
      if (!d.final) return err(['protocolos', j, 'dosis'], 'el protocolo apunta a una dosis sin final')
      // Se comparan concentraciones por ml: el resultado y la dosis pueden venir en volúmenes distintos.
      const concResultado = p.resultado.valor / p.resultado.volumenMl
      const c = d.final.cantidad
      if ('min' in c) {
        const min = convertirOcular(c.min, c.unidad, p.resultado.unidad)
        const max = convertirOcular(c.max, c.unidad, p.resultado.unidad)
        if (min === null || max === null) return err(['protocolos', j, 'resultado'], 'el resultado del protocolo y la dosis final tienen unidades no comparables')
        if (concResultado < min / d.final.volumenMl - 1e-9 || concResultado > max / d.final.volumenMl + 1e-9) {
          err(['protocolos', j, 'resultado'], 'el resultado del protocolo queda fuera del rango de la dosis final')
        }
      } else {
        const objetivo = convertirOcular(c.valor, c.unidad, p.resultado.unidad)
        if (objetivo === null) return err(['protocolos', j, 'resultado'], 'el resultado del protocolo y la dosis final tienen unidades no comparables')
        const concObjetivo = objetivo / d.final.volumenMl
        if (Math.abs(concResultado - concObjetivo) / concObjetivo > TOLERANCIA_OCULAR + 1e-9) {
          err(['protocolos', j, 'resultado'], 'el resultado del protocolo difiere más de 5 % de la dosis final')
        }
      }
    })
  })

export type UnidadOcular = z.infer<typeof UnidadOcular>
export type CantidadOcular = z.infer<typeof CantidadOcular>
export type RangoOcular = z.infer<typeof RangoOcular>
export type DosisFinal = z.infer<typeof DosisFinal>
export type PresentacionOcular = z.infer<typeof PresentacionOcular>
export type DosisOcular = z.infer<typeof DosisOcular>
export type Paso = z.infer<typeof Paso>
export type ProtocoloOcular = z.infer<typeof ProtocoloOcular>
export type FichaOcular = z.infer<typeof FichaOcular>
