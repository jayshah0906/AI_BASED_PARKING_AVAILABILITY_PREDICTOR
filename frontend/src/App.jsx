import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MainPage from './pages/MainPage'
import Dashboard from './pages/Dashboard'
import ZoneDetail from './pages/ZoneDetail'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/zone/:zoneId" element={<ZoneDetail />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
