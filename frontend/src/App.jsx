import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ZoneDetail from './pages/ZoneDetail'
import Header from './components/Header'

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/zone/:zoneId" element={<ZoneDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
