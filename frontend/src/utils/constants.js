export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const AVAILABILITY_COLORS = {
  High: '#10b981', // green
  Medium: '#f59e0b', // amber
  Low: '#ef4444' // red
}

export const AVAILABILITY_LABELS = {
  High: 'High Availability',
  Medium: 'Medium Availability',
  Low: 'Low Availability'
}
