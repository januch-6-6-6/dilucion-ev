import type { CantidadOcular, DosisFinal, FamiliaOcular, FormaOcular, PresentacionOcular, RangoOcular, ViaOcular, Paso } from '../../esquema/ficha-ocular'

// Avisos fijos de la sección (textos exactos acordados en la spec).
export const AVISO_FORMACION = 'Material de formación, no de prescripción.'
export const AVISO_PABELLON = 'Verifica el protocolo de tu pabellón.'
export const AVISO_NO_REGISTRADO = 'No registrado en Chile (puede usarse por importación o uso compasivo).'
export const AVISO_SIN_PASOS = 'La fuente no publica pasos de preparación; usa el protocolo de tu pabellón.'
export const AVISO_CIRUJANO = 'La dosis y el tiempo de aplicación los define el cirujano.'

export const TEXTO_SIN_PAUTA = 'Ficha informativa: no se muestra una pauta de dosis.'
export const TEXTO_INFORMATIVA = 'Ficha informativa: los volúmenes son referencia de la literatura y no hay verificador de preparación.'

export const FAMILIA: Record<FamiliaOcular, string> = {
  intracameral: 'Intracamerales',
  intravitreo: 'Intravítreas',
  bloqueo: 'Bloqueos',
  periocular: 'Perioculares',
  antifibrotico: 'Antifibróticos y toxina',
}

export const VIA_OCULAR: Record<ViaOcular, string> = {
  intracameral: 'Intracameral',
  intravitrea: 'Intravítrea',
  subconjuntival: 'Subconjuntival',
  subtenoniana: 'Subtenoniana',
  subretiniana: 'Subretiniana',
  retrobulbar: 'Retrobulbar',
  peribulbar: 'Peribulbar',
  intralesional: 'Intralesional',
  topica_intraoperatoria: 'Tópica intraoperatoria',
  intramuscular: 'Intramuscular',
}

export const FORMA_OCULAR: Record<FormaOcular, string> = {
  polvo: 'Polvo para reconstituir',
  solucion: 'Solución',
  suspension: 'Suspensión',
  implante: 'Implante',
  jeringa_precargada: 'Jeringa precargada',
}

export const PEDIATRIA = {
  con_dosis: 'Con dosis pediátrica',
  no_establecida: 'No establecida en niños',
  contraindicada: 'Contraindicada en niños',
  sin_datos: 'Sin datos pediátricos',
} as const

const num = (n: number) => String(n).replace('.', ',')
export const unidadTexto = (u: CantidadOcular['unidad']) => (u === 'mcg' ? 'µg' : u)

export const cantidadTexto = (c: CantidadOcular | RangoOcular): string =>
  'min' in c ? `${num(c.min)}–${num(c.max)} ${unidadTexto(c.unidad)}` : `${num(c.valor)} ${unidadTexto(c.unidad)}`

export const finalTexto = (f: DosisFinal): string => `${cantidadTexto(f.cantidad)} en ${num(f.volumenMl)} ml`

export const describirPresentacion = (p: PresentacionOcular): string =>
  `${FORMA_OCULAR[p.forma]} ${cantidadTexto(p.cantidad)}${p.volumenMl ? ` en ${num(p.volumenMl)} ml` : ''}`

export function pasoTexto(p: Paso): string {
  switch (p.tipo) {
    case 'reconstituir':
      return `Reconstituir con ${p.diluyente} hasta un volumen final de ${num(p.volumenMl)} ml.`
    case 'diluir':
      return `Tomar ${num(p.tomarMl)} ml y llevar a ${num(p.llevarAMl)} ml con ${p.diluyente}.`
    case 'cargar':
      return `Cargar ${num(p.volumenMl)} ml en la jeringa.`
    case 'texto':
      return p.texto
  }
}
