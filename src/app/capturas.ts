/**
 * Capturas de funcionamiento (estilo ficha de Google Play) que se muestran en la portada y en el README.
 * Las imágenes son capturas REALES de la app, generadas con `scripts/capturas/generar-capturas.mjs`
 * y guardadas en `public/capturas/<id>.webp`. Si se cambia esta lista, regenerarlas.
 */
export interface Captura {
  id: string
  /** Titular corto que va impreso sobre la imagen. */
  titular: string
  /** Texto alternativo: repite el titular y describe lo que se ve. */
  alt: string
}

export const CAPTURAS: Captura[] = [
  {
    id: 'busqueda',
    titular: 'Encuentra el medicamento en segundos',
    alt: 'Encuentra el medicamento en segundos: búsqueda por nombre genérico o comercial con resultados por grupo y marca de alto riesgo.',
  },
  {
    id: 'ficha',
    titular: 'Cómo preparar, con la fuente citada',
    alt: 'Cómo preparar, con la fuente citada: ficha de noradrenalina con presentaciones, reconstitución y dilución, cada dato con su fuente.',
  },
  {
    id: 'calculadora',
    titular: 'De la dosis a los ml/h',
    alt: 'De la dosis a los ml/h: calculadora de noradrenalina que convierte la dosis por peso en velocidad de infusión.',
  },
  {
    id: 'compatibilidad',
    titular: 'Compatibilidad en Y de un vistazo',
    alt: 'Compatibilidad en Y de un vistazo: tabla de compatibilidad de noradrenalina con otros medicamentos, compatible o incompatible según la fuente.',
  },
  {
    id: 'oscuro',
    titular: 'Modo oscuro para el turno de noche',
    alt: 'Modo oscuro para el turno de noche: la ficha de un medicamento con el tema oscuro.',
  },
]

export const rutaCaptura = (id: string) => `${import.meta.env.BASE_URL}capturas/${id}.webp`
