import { HashRouter, Route, Routes } from 'react-router-dom'

export default function App() {
  return (
    <HashRouter>
      <header>
        <h1>Dilución EV</h1>
      </header>
      <Routes>
        <Route path="*" element={null} />
      </Routes>
    </HashRouter>
  )
}
