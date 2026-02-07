# API Specification

## Base URL
```
http://localhost:8001/api/v1
```

## Endpoints

### Health Check
```
GET /health
```
Returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-07T14:00:00",
  "service": "parking-prediction-api"
}
```

### Get All Zones
```
GET /zones
```
Returns list of all parking zones.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Downtown",
    "lat": 40.7128,
    "lng": -74.0060,
    "description": "Central business district"
  }
]
```

### Get Zone by ID
```
GET /zones/{zone_id}
```
Returns details of a specific zone.

**Response:**
```json
{
  "id": 1,
  "name": "Downtown",
  "lat": 40.7128,
  "lng": -74.0060,
  "description": "Central business district"
}
```

### Predict Parking Availability
```
POST /predict
```
Predicts parking availability for a zone at a specific time.

**Request Body:**
```json
{
  "zone_id": 1,
  "day_of_week": 1,
  "hour": 14,
  "date": "2026-02-07"
}
```

**Response:**
```json
{
  "zone_id": 1,
  "zone_name": "Downtown",
  "availability_level": "Medium",
  "confidence_score": 0.85,
  "predicted_occupancy": 65.5,
  "timestamp": "2026-02-07T14:00:00",
  "factors": {
    "time_of_day": "afternoon",
    "is_weekend": false,
    "traffic_level": "moderate",
    "events_nearby": 0
  }
}
```

### Get Events
```
GET /events?zone_id={zone_id}&date={date}
```
Returns events filtered by zone and/or date.

**Query Parameters:**
- `zone_id` (optional): Filter by zone ID
- `date` (optional): Filter by date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Music Festival",
    "zone_id": 1,
    "date": "2026-02-07",
    "start_time": "18:00",
    "end_time": "22:00",
    "expected_impact": "High"
  }
]
```

### Get Event by ID
```
GET /events/{event_id}
```
Returns details of a specific event.

**Response:**
```json
{
  "id": 1,
  "name": "Music Festival",
  "zone_id": 1,
  "date": "2026-02-07",
  "start_time": "18:00",
  "end_time": "22:00",
  "expected_impact": "High"
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message",
  "detail": "Detailed error description"
}
```

**Status Codes:**
- `200`: Success
- `404`: Resource not found
- `422`: Validation error
- `500`: Internal server error
