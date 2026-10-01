import { z } from 'zod'

const positivo = z.number().positive()

export const FuenteRef = z.object({ ref: z.string().min(1), detalle: z.string().min(1) })
export const Fuente = z.object({
  id: z.string().min(1),
  titulo: z.string().min(1),
  institucion: z.string().min(1),
  url: z.string().url(),
  anio: z.number().int(),
  consultado: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
})

export const UnidadMasa = z.enum(['g', 'mg', 'mcg', 'UI'])
export const Cantidad = z.object({ valor: positivo, unidad: UnidadMasa })
const CantidadConFuente = Cantidad.extend({ fuente: FuenteRef })

export const Ambito = z.enum(['samu', 'urgencia', 'upc', 'hospitalizacion', 'aps'])
export const Via = z.enum(['bolo', 'infusion_intermitente', 'infusion_continua'])
export const EstadoCompatibilidad = z.enum(['compatible', 'incompatible', 'sin_datos'])

export const Dosis = z.object({
  indicacion: z.string().min(1),
  poblacion: z.enum(['adulto', 'pediatrico']),
  unidad: z.string().min(1),
  min: positivo.optional(),
  max: positivo.optional(),
  maximaAbsoluta: positivo.optional(),
  topeAdulto: Cantidad.optional(),
  fuente: FuenteRef,
})

export const Ficha = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),
  nombre: z.string().min(1),
  comerciales: z.array(z.string()),
  grupo: z.string().min(1),
  ambitos: z.array(Ambito).min(1),
  altoRiesgo: z.boolean(),
  presentaciones: z
    .array(z.object({ id: z.string().min(1), forma: z.string().min(1), cantidad: Cantidad, volumenMl: positivo, fuente: FuenteRef }))
    .min(1),
  reconstitucion: z.object({ diluyente: z.string().min(1), volumenMl: positivo, fuente: FuenteRef }).nullable(),
  dilucion: z.object({
    sueros: z.array(z.string()),
    concentracionMin: CantidadConFuente.optional(),
    concentracionMax: CantidadConFuente.optional(),
    estandar: z.array(
      z.object({ descripcion: z.string().min(1), cantidad: Cantidad, volumenFinalMl: positivo, fuente: FuenteRef }),
    ),
  }),
  administracion: z.object({
    vias: z.array(Via).min(1),
    texto: z.string().min(1),
    tiempoMinimoMin: positivo.optional(),
    requiereViaCentral: z.boolean(),
    requiereBomba: z.boolean(),
    fuente: FuenteRef,
  }),
  dosis: z.array(Dosis),
  sinDosisPediatrica: z.boolean(),
  estabilidad: z.object({
    ambienteH: positivo.optional(),
    refrigeradoH: positivo.optional(),
    protegerLuz: z.boolean(),
    fuente: FuenteRef,
  }),
  compatibilidad: z.array(z.object({ con: z.string().min(1), estado: EstadoCompatibilidad, fuente: FuenteRef })),
  interaccionesGraves: z.array(z.object({ con: z.string().min(1), efecto: z.string().min(1), fuente: FuenteRef })),
  efectosAdversos: z.object({
    frecuentes: z.array(z.string()),
    graves: z.array(z.string()),
    vigilar: z.array(z.string()),
    fuente: FuenteRef,
  }),
  alertas: z.array(z.string()),
  meta: z.object({
    revisadoPor: z.string().optional(),
    fechaRevision: z.string().optional(),
    discrepancias: z.array(z.object({ campo: z.string(), valores: z.array(z.string()), decision: z.string() })),
  }),
})

export type Ficha = z.infer<typeof Ficha>
export type Fuente = z.infer<typeof Fuente>
export type Dosis = z.infer<typeof Dosis>
