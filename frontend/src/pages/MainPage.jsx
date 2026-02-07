import { useState, useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import './MainPage.css'
import api from '../services/api'

// Zone data with coordinates
const ZONES = [
  { id: 1, name: 'Downtown Pike St', lat: 47.6105, lng: -122.3380 },
  { id: 2, name: 'Downtown 1st Ave', lat: 47.6050, lng: -122.3350 },
  { id: 3, name: 'Downtown 3rd Ave', lat: 47.6080, lng: -122.3310 },
  { id: 4, name: 'Capitol Hill - Broadway', lat: 47.6240, lng: -122.3210 },
  { id: 5, name: 'University District - University Way', lat: 47.6650, lng: -122.3130 },
  { id: 6, name: 'Stadium District - Occidental', lat: 47.5920, lng: -122.3330 },
  { id: 7, name: 'Stadium District - 1st Ave S', lat: 47.5970, lng: -122.3280 },
  { id: 8, name: 'Capitol Hill - Pike St', lat: 47.6180, lng: -122.3150 },
  { id: 9, name: 'University District - 45th St', lat: 47.6590, lng: -122.3080 },
  { id: 10, name: 'Fremont - Fremont Ave', lat: 47.6505, lng: -122.3493 }
]

// Uber-inspired color scheme
const COLORS = {
  High: '#05A357',    // Uber green
  Medium: '#FFC043',  // Uber amber
  Low: '#CD0000'      // Uber red
}

function MainPage() {
  const [selectedDate, setSelectedDate] = useState('')
  const [selectedHour, setSelectedHour] = useState('')
  const [showResults, setShowResults] = useState(false)
  const [selectedZone, setSelectedZone] = useState('')
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(false)
  const [zoneColors, setZoneColors] = useState({})
  const [eventAlert, setEventAlert] = useState(null)
  
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const markersRef = useRef({})
  const resultsSectionRef = useRef(null)

  // Generate hour options (0-23)
  const hourOptions = Array.from({ length: 24 }, (_, i) => i)

  // Auto-show results when date and hour are selected
  useEffect(() => {
    if (selectedDate && selectedHour !== '' && !showResults) {
      setShowResults(true)
      setTimeout(() => {
        resultsSectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
        setTimeout(() => {
          initializeMap()
        }, 600)
      }, 100)
    }
  }, [selectedDate, selectedHour])

  // Initialize Leaflet map
  const initializeMap = async () => {
    if (mapInstanceRef.current) return

    const map = L.map(mapRef.current, {
      zoomControl: false
    }).setView([47.6205, -122.3321], 12)

    // Uber-style map tiles (light, minimal)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map)

    // Add zoom control to bottom right
    L.control.zoom({
      position: 'bottomright'
    }).addTo(map)

    mapInstanceRef.current = map

    await fetchZoneColors()

    ZONES.forEach(zone => {
      addZoneMarker(zone)
    })
  }

  // Fetch zone colors
  const fetchZoneColors = async () => {
    if (!selectedDate || selectedHour === '') return

    try {
      const hour = parseInt(selectedHour)
      const date = new Date(selectedDate)
      const dayOfWeek = date.getDay() === 0 ? 6 : date.getDay() - 1

      const colors = {}
      
      for (const zone of ZONES) {
        try {
          const response = await api.post('/predict', {
            zone_id: zone.id,
            date: selectedDate,
            hour: hour,
            day_of_week: dayOfWeek
          })
          
          colors[zone.id] = COLORS[response.data.availability_level] || '#666666'
        } catch (error) {
          console.error(`Error fetching color for zone ${zone.id}:`, error)
          colors[zone.id] = '#666666'
        }
      }

      setZoneColors(colors)
    } catch (error) {
      console.error('Error fetching zone colors:', error)
    }
  }

  // Add zone marker
  const addZoneMarker = (zone) => {
    if (!mapInstanceRef.current) return

    const color = zoneColors[zone.id] || '#666666'

    const marker = L.circleMarker([zone.lat, zone.lng], {
      radius: 12,
      fillColor: color,
      color: '#000000',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9
    }).addTo(mapInstanceRef.current)

    marker.bindPopup(`<b>${zone.name}</b>`)

    marker.on('click', () => {
      handleZoneSelect(zone.id.toString())
    })

    markersRef.current[zone.id] = marker
  }

  // Update marker colors
  useEffect(() => {
    if (Object.keys(zoneColors).length > 0) {
      Object.entries(markersRef.current).forEach(([zoneId, marker]) => {
        const color = zoneColors[parseInt(zoneId)] || '#666666'
        marker.setStyle({ fillColor: color })
      })
    }
  }, [zoneColors])

  // Handle zone selection
  const handleZoneSelect = async (zoneId) => {
    setSelectedZone(zoneId)
    setLoading(true)
    setPredictions([])
    setEventAlert(null)

    try {
      const hour = parseInt(selectedHour)
      const date = new Date(selectedDate)
      const dayOfWeek = date.getDay() === 0 ? 6 : date.getDay() - 1

      // Fetch events
      let eventsHappening = []
      try {
        const eventsResponse = await api.get(`/events?zone_id=${zoneId}&date=${selectedDate}`)
        const events = eventsResponse.data
        
        eventsHappening = events.filter(event => {
          const eventStart = parseInt(event.start_time.split(':')[0])
          const eventEnd = parseInt(event.end_time.split(':')[0])
          return hour >= eventStart && hour <= eventEnd
        })
        
        if (eventsHappening.length > 0) {
          setEventAlert({
            eventNames: eventsHappening.map(e => e.name),
            impact: eventsHappening[0].expected_impact
          })
        }
      } catch (error) {
        console.error('Error fetching events:', error)
      }

      const predictionResults = []

      // Fetch predictions for next 4 hours
      for (let i = 0; i < 4; i++) {
        const targetHour = (hour + i) % 24
        
        const response = await api.post('/predict', {
          zone_id: parseInt(zoneId),
          date: selectedDate,
          hour: targetHour,
          day_of_week: dayOfWeek
        })

        const availability = 100 - response.data.predicted_occupancy
        const confidence = response.data.confidence_score * 100
        const predictionScore = response.data.predicted_occupancy
        const availableSpaces = response.data.available_spaces
        const totalSpaces = response.data.total_spaces

        predictionResults.push({
          hour: targetHour,
          availability: availability,
          confidence: confidence,
          predictionScore: predictionScore,
          availabilityLevel: response.data.availability_level,
          availableSpaces: availableSpaces,
          totalSpaces: totalSpaces
        })
      }

      setPredictions(predictionResults)
    } catch (error) {
      console.error('Error fetching predictions:', error)
      alert('Error loading predictions. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Format hour
  const formatHour = (hour) => {
    const ampm = hour >= 12 ? 'PM' : 'AM'
    const h = hour % 12 || 12
    return `${h}:00 ${ampm}`
  }

  const selectedZoneName = ZONES.find(z => z.id === parseInt(selectedZone))?.name

  return (
    <div className="uber-page">
      {/* Hero Section */}
      <section className="uber-hero">
        <div className="uber-container">
          <h1 className="uber-title">Find parking in Seattle</h1>
          <p className="uber-subtitle">AI-powered predictions for smarter parking decisions</p>
          
          {/* Input Card */}
          <div className="uber-input-card">
            <div className="uber-input-group">
              <label className="uber-label">When do you need parking?</label>
              <div className="uber-inputs">
                <input
                  type="date"
                  className="uber-input"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  placeholder="Select date"
                />
                <select
                  className="uber-input"
                  value={selectedHour}
                  onChange={(e) => setSelectedHour(e.target.value)}
                >
                  <option value="">Select time</option>
                  {hourOptions.map(hour => (
                    <option key={hour} value={hour}>
                      {formatHour(hour)}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Results Section */}
      {showResults && (
        <section className="uber-results" ref={resultsSectionRef}>
          <div className="uber-container-full">
            <div className="uber-split">
              {/* Map Side */}
              <div className="uber-map-side">
                <div className="uber-map-header">
                  <h2>Available zones</h2>
                  <div className="uber-legend">
                    <span className="uber-legend-item">
                      <span className="uber-dot" style={{background: '#05A357'}}></span>
                      High
                    </span>
                    <span className="uber-legend-item">
                      <span className="uber-dot" style={{background: '#FFC043'}}></span>
                      Medium
                    </span>
                    <span className="uber-legend-item">
                      <span className="uber-dot" style={{background: '#CD0000'}}></span>
                      Low
                    </span>
                  </div>
                </div>
                <div ref={mapRef} className="uber-map"></div>
              </div>

              {/* Details Side */}
              <div className="uber-details-side">
                {!selectedZone && (
                  <div className="uber-empty-state">
                    <div className="uber-empty-icon">📍</div>
                    <h3>Select a zone</h3>
                    <p>Click on a zone marker or choose from the list below</p>
                    
                    <div className="uber-zone-list">
                      {ZONES.map(zone => (
                        <button
                          key={zone.id}
                          className="uber-zone-button"
                          onClick={() => handleZoneSelect(zone.id.toString())}
                        >
                          <span className="uber-zone-name">{zone.name}</span>
                          <span 
                            className="uber-zone-indicator"
                            style={{background: zoneColors[zone.id] || '#666666'}}
                          ></span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {loading && (
                  <div className="uber-loading">
                    <div className="uber-spinner"></div>
                    <p>Loading predictions...</p>
                  </div>
                )}

                {!loading && eventAlert && (
                  <div className="uber-alert">
                    <div className="uber-alert-icon">⚠️</div>
                    <div>
                      <h4>Event nearby</h4>
                      <p>{eventAlert.eventNames.join(', ')}</p>
                    </div>
                  </div>
                )}

                {!loading && predictions.length > 0 && (
                  <div className="uber-predictions">
                    <div className="uber-predictions-header">
                      <h2>{selectedZoneName}</h2>
                      <p className="uber-confidence">
                        {predictions[0].confidence.toFixed(0)}% confidence
                      </p>
                    </div>

                    <div className="uber-predictions-grid">
                      {predictions.map((pred, index) => {
                        const levelColor = COLORS[pred.availabilityLevel]
                        
                        return (
                          <div key={index} className="uber-prediction-card">
                            <div className="uber-card-header">
                              <span className="uber-card-time">{formatHour(pred.hour)}</span>
                              <span 
                                className="uber-card-badge"
                                style={{background: levelColor}}
                              >
                                {pred.availabilityLevel}
                              </span>
                            </div>
                            <div className="uber-card-body">
                              <div className="uber-card-main">
                                <span className="uber-card-number">{pred.availableSpaces}</span>
                                <span className="uber-card-label">/ {pred.totalSpaces} spaces</span>
                              </div>
                              <div className="uber-card-sub">
                                {pred.predictionScore.toFixed(0)}% occupied
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default MainPage
