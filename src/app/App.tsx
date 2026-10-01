import { HashRouter, Link, Route, Routes } from 'react-router-dom'
import AvisoInicial from './componentes/AvisoInicial'
import Acerca from './paginas/Acerca'
import Calculadora from './paginas/Calculadora'
import Ficha from './paginas/Ficha'
import Inicio from './paginas/Inicio'
import Lista from './paginas/Lista'

export default function App() {
  return (
    <HashRouter>
      <header className="cabecera">
        <h1>
          <Link to="/">Dilución EV</Link>
        </h1>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Inicio />} />
          <Route path="/ambito/:ambito" element={<Lista />} />
          <Route path="/grupo/:grupo" element={<Lista />} />
          <Route path="/m/:id" element={<Ficha />} />
          <Route path="/m/:id/calcular" element={<Calculadora />} />
          <Route path="/calcular" element={<Calculadora />} />
          <Route path="/acerca" element={<Acerca />} />
          <Route path="*" element={<p>Página no encontrada.</p>} />
        </Routes>
      </main>
      <footer className="pie">
        <Link to="/acerca">Material de formación · Acerca de</Link>
      </footer>
      <AvisoInicial />
    </HashRouter>
  )
}
