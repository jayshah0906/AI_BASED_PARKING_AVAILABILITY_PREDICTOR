import React, { useState, useEffect } from 'react'
import ZoneSelector from '../components/ZoneSelector'
import TimePicker from '../components/TimePicker'
import PredictionCard from '../components/PredictionCard'
import MapView from '../components/MapView'
import { usePrediction } from '../hooks/usePrediction'
import { getZones } from '../services/predictionApi'
import './Dashboard.css'

const Dashboard = () => {
  const [zones, setZones] = useState([])
  const [selectedZone, setSelectedZone] = useState(null)
  const [date, setDate] = useState(new Date().toISOString().split('T')[0])
  const [hour, setHour] = useState(new Date().getHours())
  
  const { makePrediction, loading, error, prediction } = usePrediction()

  useEffect(() => {
    loadZones()
  }, [])

  useEffect(() => {
    if (selectedZone !== null && date && hour !== null) {
      makePrediction(selectedZone, date, hour)
    }
  }, [selectedZone, date, hour])

  const loadZones = async () => {
    try {
      const zonesData = await getZones()
      setZones(zonesData)
    } catch (err) {
      console.error('Failed to load zones:', err)
    }
  }

  const handleZoneChange = (zoneId) => {
    setSelectedZone(zoneId)
  }

  const handleDateChange = (newDate) => {
    setDate(newDate)
  }

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Parking Availability Predictor</h1>
          <p>Predict parking availability across city zones</p>
        </div>

        <div className="dashboard-content">
          <div className="dashboard-left">
            <div className="selection-panel">
              <MapView
                zones={zones}
                selectedZone={selectedZone}
                onZoneSelect={handleZoneChange}
              />
              
              <ZoneSelector
                zones={zones}
                selectedZone={selectedZone}
                onZoneChange={handleZoneChange}
              />

              <TimePicker
                date={date}
                hour={hour}
                onDateChange={handleDateChange}
                onHourChange={setHour}
              />
            </div>
          </div>

          <div className="dashboard-right">
            <PredictionCard
              prediction={prediction}
              loading={loading}
              error={error}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
