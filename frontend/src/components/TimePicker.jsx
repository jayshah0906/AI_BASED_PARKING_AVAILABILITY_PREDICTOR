import React from 'react'
import './TimePicker.css'

const TimePicker = ({ date, hour, onDateChange, onHourChange }) => {
  const hours = Array.from({ length: 24 }, (_, i) => i)

  return (
    <div className="time-picker">
      <div className="time-picker-group">
        <label htmlFor="date-input" className="time-picker-label">
          Date:
        </label>
        <input
          id="date-input"
          type="date"
          className="time-picker-input"
          value={date}
          onChange={(e) => onDateChange(e.target.value)}
          min={new Date().toISOString().split('T')[0]}
        />
      </div>

      <div className="time-picker-group">
        <label htmlFor="hour-select" className="time-picker-label">
          Hour:
        </label>
        <select
          id="hour-select"
          className="time-picker-select"
          value={hour}
          onChange={(e) => onHourChange(Number(e.target.value))}
        >
          {hours.map((h) => (
            <option key={h} value={h}>
              {h.toString().padStart(2, '0')}:00
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}

export default TimePicker
