import React, { useState, useEffect } from 'react'
import './InteractiveMap.css'

// Seattle center coordinates
const SEATTLE_CENTER = { lat: 47.6062, lng: -122.3321 }

// Color scheme based on availability (keeping your color scheme)
const AVAILABILITY_COLORS = {
  High: '#10b981',    // Green - lots of spaces
  Medium: '#f59e0b',  // Amber - moderate
  Low: '#ef4444'      // Red - few spaces
}

const InteractiveMap = ({ zones, onZoneClick }) => {
  const [selectedZone, setSelectedZone] = useState(null)
  const [hoveredZone, setHoveredZone] = useState(null)

  // Calculate zone position on map (simplified grid layout)
  const getZonePosition = (zone, index) => {
    // Spread zones across Seattle map area
    const neighborhoods = {
      'Downtown': { x: 50, y: 50 },
      'Stadium': { x: 48, y: 60 },
      'Capitol Hill': { x: 55, y: 45 },
      'University': { x: 52, y: 25 },
      'Fremont': { x: 45, y: 35 }
    }

    // Determine neighborhood from zone name
    let basePos = { x: 50, y: 50 }
    if (zone.name.includes('Downtown')) basePos = neighborhoods['Downtown']
    else if (zone.name.includes('Stadium')) basePos = neighborhoods['Stadium']
    else if (zone.name.includes('Capitol')) basePos = neighborhoods['Capitol Hill']
    else if (zone.name.includes('University')) basePos = neighborhoods['University']
    else if (zone.name.includes('Fremont')) basePos = neighborhoods['Fremont']

    // Add slight offset for multiple zones in same area
    const offset = (index % 3) * 3
    return {
      left: `${basePos.x + offset}%`,
      top: `${basePos.y + (Math.floor(index / 3) * 3)}%`
    }
  }

  const getAvailabilityColor = (availability) => {
    return AVAILABILITY_COLORS[availability] || '#6b7280'
  }

  const handleZoneClick = (zone) => {
    setSelectedZone(zone)
    if (onZoneClick) {
      onZoneClick(zone)
    }
  }

  return (
    <div className="interactive-map">
      {/* Map Background */}
      <div className="map-background">
        <div className="map-grid"></div>
        
        {/* Neighborhood Labels */}
        <div className="neighborhood-label" style={{ left: '50%', top: '48%' }}>
          Downtown
        </div>
        <div className="neighborhood-label" style={{ left: '48%', top: '58%' }}>
          Stadium District
        </div>
        <div className="neighborhood-label" style={{ left: '55%', top: '43%' }}>
          Capitol Hill
        </div>
        <div className="neighborhood-label" style={{ left: '52%', top: '23%' }}>
          University District
        </div>
        <div className="neighborhood-label" style={{ left: '45%', top: '33%' }}>
          Fremont
        </div>
      </div>

      {/* Zone Markers */}
      {zones.map((zone, index) => {
        const position = getZonePosition(zone, index)
        const color = getAvailabilityColor(zone.availability_level)
        const isHovered = hoveredZone?.zone_id === zone.zone_id
        const isSelected = selectedZone?.zone_id === zone.zone_id

        return (
          <div
            key={zone.zone_id}
            className={`zone-marker ${isHovered ? 'hovered' : ''} ${isSelected ? 'selected' : ''}`}
            style={{
              ...position,
              backgroundColor: color,
              borderColor: color
            }}
            onClick={() => handleZoneClick(zone)}
            onMouseEnter={() => setHoveredZone(zone)}
            onMouseLeave={() => setHoveredZone(null)}
          >
            {/* Zone Circle */}
            <div className="zone-circle">
              <div className="zone-pulse" style={{ backgroundColor: color }}></div>
            </div>

            {/* Zone Info Tooltip */}
            {(isHovered || isSelected) && (
              <div className="zone-tooltip">
                <div className="tooltip-header">
                  <h4>{zone.name}</h4>
                  <span className="zone-id">{zone.zone_id}</span>
                </div>
                <div className="tooltip-body">
                  <div className="availability-badge" style={{ backgroundColor: color }}>
                    {zone.availability_level} Availability
                  </div>
                  <div className="stats">
                    <div className="stat">
                      <span className="label">Available:</span>
                      <span className="value">{zone.available_spaces}/{zone.total_spaces}</span>
                    </div>
                    <div className="stat">
                      <span className="label">Occupancy:</span>
                      <span className="value">{zone.occupancy}%</span>
                    </div>
                    <div className="stat">
                      <span className="label">Confidence:</span>
                      <span className="value">{Math.round(zone.confidence * 100)}%</span>
                    </div>
                  </div>
                </div>
                <div className="tooltip-footer">
                  <button className="view-details-btn">View Details →</button>
                </div>
              </div>
            )}
          </div>
        )
      })}

      {/* Map Legend */}
      <div className="map-legend">
        <h3>Parking Availability</h3>
        <div className="legend-items">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: AVAILABILITY_COLORS.High }}></div>
            <span>High (&lt;50% full)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: AVAILABILITY_COLORS.Medium }}></div>
            <span>Medium (50-80% full)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: AVAILABILITY_COLORS.Low }}></div>
            <span>Low (&gt;80% full)</span>
          </div>
        </div>
      </div>

      {/* Zone Count Badge */}
      <div className="zone-count-badge">
        <span className="count">{zones.length}</span>
        <span className="label">Zones</span>
      </div>
    </div>
  )
}

export default InteractiveMap
