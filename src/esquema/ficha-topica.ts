import { z } from 'zod'
import { FuenteRef } from './ficha'

const positivo = z.number().positive()
const ids = z.array(z.string().min(1)).min(1)

export const Via = z.enum(['ojo', 'oido', 'nariz'])
export const FormaTopica = z.enum(['solucion', 'suspension', 'emulsion', 'unguento', 'gel', 'spray'])
export const UnidadTopica = z.enum(['gota', 'cm', 'pulverizacion', 'aplicacion'])
export const Sitio = z.enum(['ojo', 'oido', 'fosa'])

export const PresentacionTopica = z.strictObject({
  id: z.string().regex(/^[a-z0-9-]+$/),
  forma: FormaTopica,
  via: Via,
  /** Texto tal como lo registra el ISP (p. ej. «0,5 %», «50 mcg por pulverización»). */
  concentracion: z.string().min(1),
  registrosIsp: z.array(z.string().min(1)).min(1),
  unidosis: z.boolean().optional(),
  sinConservantes: z.boolean().optional(),
  nota: z.string().min(1).optional(),
  fuente: FuenteRef,
})

export const DosisTopica = z
  .strictObject({
    indicacion: z.string().min(1),
    poblacion: z.enum(['adulto', 'pediatrico']),
    texto: z.string().min(1),
    cantidad: positivo.optional(),
    unidad: UnidadTopica.optional(),
    vecesAlDia: positivo.optional(),
    porSitio: Sitio.optional(),
    duracion: z.string().min(1).optional(),
    estatus: z.enum(['autorizada', 'off_label']),
    condicion: z.string().min(1).optional(),
    /** Ids de presentaciones a las que aplica; ausente = todas. */
    presentaciones: ids.optional(),
    fuente: FuenteRef,
    /** Otras fuentes que concuerdan con esta misma pauta. */
    tambien: z.array(FuenteRef).optional(),
  })
  .superRefine((d, ctx) => {
    if (d.cantidad !== undefined && !d.unidad) {
      ctx.addIssue({ code: 'custom', path: ['unidad'], message: 'cantidad exige unidad' })
    }
  })

export const Discrepancia = z.strictObject({
  campo: z.string().min(1),
  valores: z.array(z.strictObject({ fuente: z.string(), valor: z.string() })).min(1),
  mostrado: z.string(),
  motivo: z.string(),
})

export const FichaTopica = z
  .strictObject({
    id: z.string().regex(/^[a-z0-9-]+$/),
    nombre: z.string().min(1),
    comerciales: z.array(z.string()),
    grupo: z.string().min(1),
    vias: z.array(Via).min(1),
    componentes: z.array(z.string().min(1)),
    altoRiesgo: z.boolean(),
    presentaciones: z.array(PresentacionTopica).min(1),
    dosis: z.array(DosisTopica),
    sinPauta: z.strictObject({ motivo: z.string().min(1) }).nullable(),
    pediatria: z.strictObject({
      estado: z.enum(['con_dosis', 'no_establecida', 'contraindicada', 'sin_datos']),
      motivo: z.string().min(1),
      edadMinima: z.string().min(1).optional(),
    }),
    conservacion: z.array(
      z.strictObject({
        presentaciones: ids.optional(),
        validezAbiertoDias: positivo.int().optional(),
        texto: z.string().min(1),
        fuente: FuenteRef,
      }),
    ),
    administracion: z.strictObject({ texto: z.string().min(1), fuente: FuenteRef }).nullable(),
    contraindicaciones: z.array(z.string().min(1)),
    alertas: z.array(z.string().min(1)),
    discrepancias: z.array(Discrepancia),
    meta: z.strictObject({ revisadoPor: z.string().optional(), fechaRevision: z.string().optional() }),
  })
  .superRefine((f, ctx) => {
    const hayPediatrica = f.dosis.some((d) => d.poblacion === 'pediatrico')
    if (f.pediatria.estado === 'con_dosis' && !hayPediatrica) {
      ctx.addIssue({ code: 'custom', path: ['dosis'], message: 'con_dosis exige al menos una dosis pediátrica' })
    }
    if (f.pediatria.estado !== 'con_dosis' && hayPediatrica) {
      ctx.addIssue({ code: 'custom', path: ['dosis'], message: `con pediatría ${f.pediatria.estado} no puede haber dosis pediátricas` })
    }
    if (f.sinPauta && f.dosis.length > 0) {
      ctx.addIssue({ code: 'custom', path: ['dosis'], message: 'una ficha sin pauta no puede tener dosis' })
    }
    if (!f.sinPauta && f.dosis.length === 0) {
      ctx.addIssue({ code: 'custom', path: ['dosis'], message: 'sin dosis hay que declarar sinPauta con su motivo' })
    }
    const existe = new Set(f.presentaciones.map((p) => p.id))
    const revisar = (lista: string[] | undefined, ruta: (string | number)[]) =>
      lista?.forEach((id, k) => {
        if (!existe.has(id)) {
          ctx.addIssue({ code: 'custom', path: [...ruta, k], message: `la presentación "${id}" no existe en presentaciones de esta ficha` })
        }
      })
    f.dosis.forEach((d, j) => revisar(d.presentaciones, ['dosis', j, 'presentaciones']))
    f.conservacion.forEach((c, j) => revisar(c.presentaciones, ['conservacion', j, 'presentaciones']))
    f.presentaciones.forEach((p, j) => {
      if (!f.vias.includes(p.via)) {
        ctx.addIssue({ code: 'custom', path: ['presentaciones', j, 'via'], message: `la vía "${p.via}" no está en vias` })
      }
    })
  })

export type Via = z.infer<typeof Via>
export type FormaTopica = z.infer<typeof FormaTopica>
export type UnidadTopica = z.infer<typeof UnidadTopica>
export type PresentacionTopica = z.infer<typeof PresentacionTopica>
export type DosisTopica = z.infer<typeof DosisTopica>
export type FichaTopica = z.infer<typeof FichaTopica>
