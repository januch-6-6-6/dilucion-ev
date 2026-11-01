import { lazy, Suspense } from 'react'
import { HashRouter, Link, NavLink, Route, Routes, useLocation } from 'react-router-dom'
import { medicamentos } from '../datos/cargar'
import AvisoInicial from './componentes/AvisoInicial'
import Acerca from './paginas/Acerca'
import Calculadora from './paginas/Calculadora'
import Ficha from './paginas/Ficha'
import Inicio from './paginas/Inicio'
import Lista from './paginas/Lista'
import ContadorVisitas from './visitas'

const ListaOrales = lazy(() => import('./orales/ListaOrales'))
const FichaOral = lazy(() => import('./orales/FichaOral'))
const CalculadoraOral = lazy(() => import('./orales/CalculadoraOral'))
const ListaTopicos = lazy(() => import('./topicos/ListaTopicos'))
const FichaTopica = lazy(() => import('./topicos/FichaTopica'))
const CalculadoraTopica = lazy(() => import('./topicos/CalculadoraTopica'))

/** Cabecera con degradado. En la portada (/) agrega la presentación: qué es y para quién. */
function Cabecera() {
  const portada = useLocation().pathname === '/'
  return (
    <header className={portada ? 'cabecera cabecera-portada' : 'cabecera'}>
      <div className="cabecera-contenido">
        <h1>
          <Link to="/">Dilución EV</Link>
        </h1>
        <p className="subtitulo">Dilución, velocidad y compatibilidad EV</p>
        <nav aria-label="Secciones" className="secciones">
          <NavLink to="/" end>EV</NavLink>
          <NavLink to="/orales">Orales</NavLink>
          <NavLink to="/topicos">Tópicos</NavLink>
        </nav>
        {portada && (
          <div className="presentacion">
            <p className="presentacion-titular">Prepara y administra medicamentos endovenosos con la fuente a la vista.</p>
            <p className="presentacion-para">
              Para estudiantes, TENS y equipos de enfermería en formación: {medicamentos.length} medicamentos EV usados en Chile.
            </p>
            <ul className="presentacion-chips" aria-label="Características">
              <li>Funciona sin internet</li>
              <li>Se instala en el celular</li>
              <li>Gratis y sin registro</li>
            </ul>
          </div>
        )}
      </div>
    </header>
  )
}

export default function App() {
  return (
    <HashRouter>
      <ContadorVisitas />
      <Cabecera />
      <main>
        <Suspense fallback={<p>Cargando…</p>}>
          <Routes>
          <Route path="/" element={<Inicio />} />
          <Route path="/orales" element={<ListaOrales />} />
          <Route path="/orales/m/:id" element={<FichaOral />} />
          <Route path="/orales/m/:id/calcular" element={<CalculadoraOral />} />
          <Route path="/topicos" element={<ListaTopicos />} />
          <Route path="/topicos/m/:id" element={<FichaTopica />} />
          <Route path="/topicos/m/:id/calcular" element={<CalculadoraTopica />} />
          <Route path="/ambito/:ambito" element={<Lista />} />
          <Route path="/grupo/:grupo" element={<Lista />} />
          <Route path="/m/:id" element={<Ficha />} />
          <Route path="/m/:id/calcular" element={<Calculadora />} />
          <Route path="/calcular" element={<Calculadora />} />
          <Route path="/acerca" element={<Acerca />} />
          <Route path="*" element={<p>Página no encontrada.</p>} />
          </Routes>
        </Suspense>
      </main>
      <footer className="pie">
        <p className="autor">
          Creado por <strong>Héctor Salvo Agüero</strong> · TENS e Ingeniero en Informática
        </p>
        <p>
          <a href="https://github.com/januch-6-6-6/dilucion-ev" target="_blank" rel="noreferrer">Código en GitHub</a> ·{' '}
          <Link to="/acerca">Material de formación · Acerca de</Link>
        </p>
      </footer>
      <AvisoInicial />
    </HashRouter>
  )
}
