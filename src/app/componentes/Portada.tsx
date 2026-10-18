import { useRef, type ReactNode } from 'react'
import { CAPTURAS, rutaCaptura } from '../capturas'
import type { ColorGrupo } from '../colores'

/** Íconos de línea simples (24×24), en SVG en línea para no cargar nada externo. */
const ICONOS: Record<string, ReactNode> = {
  gota: <path d="M12 3.5s6 6.4 6 10.8a6 6 0 0 1-12 0C6 9.9 12 3.5 12 3.5Z M9.5 15a2.5 2.5 0 0 0 2.5 2.5" />,
  calculadora: (
    <>
      <rect x="5" y="3" width="14" height="18" rx="2.5" />
      <path d="M8.5 7h7 M8.5 11.5h.01 M12 11.5h.01 M15.5 11.5h.01 M8.5 15h.01 M12 15h.01 M15.5 15h.01 M8.5 18h.01 M12 18h3.5" />
    </>
  ),
  y: <path d="M6 3v4.5a6 6 0 0 0 12 0V3 M12 13.5V21" />,
  fuente: <path d="M6.5 3h8l3.5 3.5V21h-11.5Z M14.5 3v3.5H18 M9.5 13.5l2 2 3.5-3.5" />,
}

const BENEFICIOS: { icono: keyof typeof ICONOS; color: ColorGrupo; titulo: string; texto: string }[] = [
  { icono: 'gota', color: 'turquesa', titulo: 'Preparar y administrar', texto: 'Presentación, dilución, estabilidad y velocidad de cada medicamento.' },
  { icono: 'calculadora', color: 'azul', titulo: 'Calculadoras', texto: 'ml/h, gotas/min, dosis por peso y pediatría con tope, con alertas.' },
  { icono: 'y', color: 'violeta', titulo: 'Compatibilidad en Y', texto: 'Qué se puede pasar por la misma vía y qué no, según la fuente.' },
  { icono: 'fuente', color: 'ambar', titulo: 'Fuente citada', texto: 'Cada dato indica de dónde sale y se muestran las discrepancias.' },
]

export function Icono({ nombre }: { nombre: keyof typeof ICONOS }) {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      {ICONOS[nombre]}
    </svg>
  )
}

export function Beneficios() {
  return (
    <section className="beneficios" aria-labelledby="beneficios-titulo">
      <h2 id="beneficios-titulo" className="visualmente-oculto">
        Qué encontrarás
      </h2>
      <ul className="beneficios-lista">
        {BENEFICIOS.map((b) => (
          <li key={b.titulo} className="beneficio" data-color={b.color}>
            <span className="beneficio-icono">
              <Icono nombre={b.icono} />
            </span>
            <span>
              <strong>{b.titulo}</strong>
              <span className="beneficio-texto">{b.texto}</span>
            </span>
          </li>
        ))}
      </ul>
    </section>
  )
}

const reducirMovimiento = () =>
  typeof window !== 'undefined' && typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

/** Carrusel deslizable de capturas reales, estilo ficha de Google Play. Se desliza con el dedo, la rueda, el teclado o los botones. */
export function Capturas() {
  const carril = useRef<HTMLUListElement>(null)
  const mover = (sentido: 1 | -1) => {
    const el = carril.current
    if (!el || typeof el.scrollBy !== 'function') return
    const paso = (el.querySelector('li')?.getBoundingClientRect().width ?? 220) + 14
    el.scrollBy({ left: sentido * paso, behavior: reducirMovimiento() ? 'auto' : 'smooth' })
  }
  return (
    <section className="capturas" aria-labelledby="capturas-titulo">
      <div className="capturas-cabeza">
        <h2 id="capturas-titulo" className="titulo-seccion">
          Así funciona
        </h2>
        <div className="capturas-botones">
          <button type="button" onClick={() => mover(-1)} aria-label="Captura anterior">
            <span aria-hidden="true">‹</span>
          </button>
          <button type="button" onClick={() => mover(1)} aria-label="Captura siguiente">
            <span aria-hidden="true">›</span>
          </button>
        </div>
      </div>
      {/* tabIndex: el carril se puede desplazar con las flechas del teclado */}
      <ul ref={carril} className="capturas-carril" aria-label="Capturas de la app" tabIndex={0}>
        {CAPTURAS.map((c) => (
          <li key={c.id}>
            <img src={rutaCaptura(c.id)} alt={c.alt} width={540} height={1080} loading="lazy" decoding="async" />
          </li>
        ))}
      </ul>
    </section>
  )
}
