export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1'

export const AVAILABILITY_COLORS = {
  High: '#05A357', // Uber green
  Medium: '#FFC043', // Uber amber
  Low: '#CD0000' // Uber red
}

export const AVAILABILITY_LABELS = {
  High: 'High Availability',
  Medium: 'Medium Availability',
  Low: 'Low Availability'
}
