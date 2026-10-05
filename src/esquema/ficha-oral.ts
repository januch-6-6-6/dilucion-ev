import { z } from 'zod'
import { Cantidad, FuenteRef, UnidadMasa } from './ficha'

const positivo = z.number().positive()

const FORMAS_SOLIDAS = ['comprimido', 'capsula', 'sobre', 'comprimido_efervescente']
const FORMAS_LIQUIDAS = ['jarabe', 'suspension', 'gotas']

export const FormaOral = z.enum([
  'comprimido',
  'capsula',
  'jarabe',
  'suspension',
  'gotas',
  'sobre',
  'comprimido_efervescente',
])

export const RegistroChile = z.enum(['verificado', 'sin_verificar', 'no_registrado'])

export const PresentacionOral = z
  .strictObject({
    id: z.string().min(1),
    forma: FormaOral,
    /** Por unidad (formas sólidas). */
    cantidad: Cantidad.optional(),
    /** Valor por 1 ml (formas líquidas). */
    concentracion: Cantidad.optional(),
    gotasPorMl: positivo.optional(),
    partible: z.enum(['no', 'mitades', 'cuartos']),
    liberacionProlongada: z.boolean(),
    elemental: z.strictObject({ valor: positivo, unidad: UnidadMasa, de: z.string().min(1) }).optional(),
    registroChile: RegistroChile,
    fuente: FuenteRef,
  })
  .superRefine((p, ctx) => {
    if (FORMAS_SOLIDAS.includes(p.forma) && !p.cantidad) {
      ctx.addIssue({ code: 'custom', path: ['cantidad'], message: 'Las formas sólidas exigen cantidad por unidad' })
    }
    if (FORMAS_LIQUIDAS.includes(p.forma) && !p.concentracion) {
      ctx.addIssue({ code: 'custom', path: ['concentracion'], message: 'Las formas líquidas exigen concentración por 1 ml' })
    }
    if (p.forma === 'gotas' && p.gotasPorMl === undefined) {
      ctx.addIssue({ code: 'custom', path: ['gotasPorMl'], message: 'Las gotas exigen gotasPorMl' })
    }
  })

export const DosisOral = z
  .strictObject({
    indicacion: z.string().min(1),
    poblacion: z.enum(['adulto', 'pediatrico']),
    regimen: z.enum(['fija', 'por_peso', 'por_edad', 'por_superficie']),
    base: z.enum(['toma', 'dia']).optional(),
    unidad: z.string().min(1),
    min: positivo.optional(),
    max: positivo.optional(),
    tomasPorDia: positivo.optional(),
    intervaloH: positivo.optional(),
    topePorToma: Cantidad.optional(),
    topeDiario: Cantidad.optional(),
    estatus: z.enum(['autorizada', 'off_label']),
    condicion: z.string().optional(),
    texto: z.string().min(1).optional(),
    fuente: FuenteRef,
  })
  .superRefine((d, ctx) => {
    if (d.regimen === 'por_peso') {
      if (!d.base) ctx.addIssue({ code: 'custom', path: ['base'], message: 'La dosis por peso exige base (toma o dia)' })
      if (!d.unidad.endsWith('/kg')) {
        ctx.addIssue({ code: 'custom', path: ['unidad'], message: 'La dosis por peso exige una unidad por kg (p. ej. mg/kg)' })
      }
    }
    if ((d.regimen === 'por_edad' || d.regimen === 'por_superficie') && !d.texto) {
      ctx.addIssue({ code: 'custom', path: ['texto'], message: 'La dosis por edad o por superficie exige texto' })
    }
  })

export const FichaOral = z
  .strictObject({
    id: z.string().regex(/^[a-z0-9-]+$/),
    nombre: z.string().min(1),
    comerciales: z.array(z.string()),
    grupo: z.string().min(1),
    ambitos: z.array(z.literal('aps')),
    altoRiesgo: z.boolean(),
    presentaciones: z.array(PresentacionOral).min(1),
    dosis: z.array(DosisOral).min(1),
    pediatria: z.strictObject({ estado: z.enum(['con_dosis', 'solo_adulto']), motivo: z.string().min(1).optional() }),
    discrepancias: z.array(
      z.strictObject({
        campo: z.string().min(1),
        valores: z.array(z.strictObject({ fuente: z.string(), valor: z.string() })),
        mostrado: z.string(),
        motivo: z.string(),
      }),
    ),
    administracion: z.strictObject({
      comida: z.enum(['ayunas', 'con_comida', 'indiferente', 'antes', 'despues']),
      texto: z.string().min(1),
      noTriturar: z.boolean().optional(),
      fuente: FuenteRef,
    }),
    ajusteRenalHepatico: z
      .strictObject({ renal: z.string().optional(), hepatico: z.string().optional(), fuente: FuenteRef })
      .nullable(),
    alertas: z.array(z.string()),
    meta: z.strictObject({ revisadoPor: z.string().optional(), fechaRevision: z.string().optional() }),
  })
  .superRefine((f, ctx) => {
    const hayPediatrica = f.dosis.some((d) => d.poblacion === 'pediatrico')
    if (f.pediatria.estado === 'solo_adulto') {
      if (!f.pediatria.motivo) {
        ctx.addIssue({ code: 'custom', path: ['pediatria', 'motivo'], message: 'solo_adulto exige motivo' })
      }
      if (hayPediatrica) {
        ctx.addIssue({ code: 'custom', path: ['dosis'], message: 'Con pediatría solo_adulto no puede haber dosis pediátricas' })
      }
    } else if (!hayPediatrica) {
      ctx.addIssue({ code: 'custom', path: ['dosis'], message: 'con_dosis exige al menos una dosis pediátrica' })
    }
  })

export type FormaOral = z.infer<typeof FormaOral>
export type RegistroChile = z.infer<typeof RegistroChile>
export type PresentacionOral = z.infer<typeof PresentacionOral>
export type DosisOral = z.infer<typeof DosisOral>
export type FichaOral = z.infer<typeof FichaOral>
