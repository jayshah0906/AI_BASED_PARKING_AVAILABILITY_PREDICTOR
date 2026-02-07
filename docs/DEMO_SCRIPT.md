# Demo Script

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Seed database with zones:
```bash
python scripts/seed_zones.py
```

5. (Optional) Import sample data:
```bash
python scripts/import_data.py
```

6. Start the server:
```bash
python run_server.py
```

The API will be available at `http://localhost:8001`
API documentation at `http://localhost:8001/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Demo Flow

### 1. Homepage
- Show the dashboard with zone map
- Explain the system purpose

### 2. Select Zone
- Click on a zone marker on the map OR
- Select from the dropdown menu
- Show zone information

### 3. Select Time
- Choose a date (default: today)
- Select hour of day
- Day of week updates automatically

### 4. View Prediction
- System automatically predicts availability
- Show:
  - Availability level (High/Medium/Low)
  - Predicted occupancy percentage
  - Confidence score
  - Factors influencing prediction

### 5. Explore Different Scenarios

**Scenario 1: Rush Hour**
- Select: Business District, Weekday, 8 AM
- Expected: Low availability, high confidence

**Scenario 2: Weekend Shopping**
- Select: Shopping Mall, Saturday, 2 PM
- Expected: Low availability, medium confidence

**Scenario 3: Late Night**
- Select: Any zone, 2 AM
- Expected: High availability, lower confidence

**Scenario 4: Event Day**
- Select: Downtown, Feb 7, 7 PM
- Expected: Low availability due to Music Festival

### 6. Zone Detail Page
- Navigate to specific zone page
- View upcoming events
- Compare predictions for different times

## Key Features to Highlight

1. **Real-time Predictions**: Instant predictions based on selected parameters
2. **Confidence Scores**: Shows prediction reliability
3. **Factor Analysis**: Explains what influences the prediction
4. **Event Integration**: Considers nearby events
5. **Multiple Zones**: Compare different city zones
6. **Time-based Analysis**: See how availability changes throughout the day

## API Testing

### Test Health Endpoint
```bash
curl http://localhost:8001/api/v1/health
```

### Test Zones Endpoint
```bash
curl http://localhost:8001/api/v1/zones
```

### Test Prediction Endpoint
```bash
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "zone_id": 1,
    "day_of_week": 1,
    "hour": 14,
    "date": "2026-02-07"
  }'
```

## Troubleshooting

### Backend Issues
- Ensure port 8000 is not in use
- Check database file permissions
- Verify all dependencies are installed

### Frontend Issues
- Ensure backend is running
- Check CORS settings if API calls fail
- Verify API URL in `.env` file

### Common Errors
- **404 on zones**: Run `seed_zones.py` script
- **CORS errors**: Check `CORS_ORIGINS` in `config.py`
- **Module not found**: Ensure virtual environment is activated
