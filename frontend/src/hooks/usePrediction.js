import { useState } from 'react'
import { predictAvailability } from '../services/predictionApi'

export const usePrediction = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [prediction, setPrediction] = useState(null)

  const makePrediction = async (zoneId, date, hour) => {
    setLoading(true)
    setError(null)
    setPrediction(null)

    // Derive day of week from date (Monday=0, Sunday=6) for API
    const d = new Date(date)
    const dayOfWeek = d.getDay() === 0 ? 6 : d.getDay() - 1

    try {
      const result = await predictAvailability({
        zone_id: zoneId,
        date: date,
        hour: hour,
        day_of_week: dayOfWeek
      })
      setPrediction(result)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to make prediction')
    } finally {
      setLoading(false)
    }
  }

  return {
    makePrediction,
    loading,
    error,
    prediction
  }
}
