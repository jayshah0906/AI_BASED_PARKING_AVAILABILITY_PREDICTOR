# Parking Availability Prediction System

An AI-powered system that predicts parking availability across different city zones based on time, location, events, and traffic patterns.

## Features

- 🎯 **Zone-based Predictions**: Predict parking availability for specific city zones
- ⏰ **Time-aware**: Considers hour of day, day of week, and special dates
- 🎪 **Event Integration**: Factors in nearby events that affect parking demand
- 🚦 **Traffic Analysis**: Incorporates traffic patterns into predictions
- 📊 **Confidence Scores**: Provides reliability indicators for each prediction
- 🗺️ **Interactive Map**: Visual zone selection interface
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
├── backend/          # FastAPI backend application
├── frontend/         # React frontend application
├── data/            # Data files (CSV, JSON)
└── docs/            # Documentation
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed_zones.py
python run_server.py
```

Backend runs on `http://localhost:8001`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Usage

1. **Select a Zone**: Choose a parking zone from the map or dropdown
2. **Pick a Time**: Select date and hour for prediction
3. **View Prediction**: See availability level, occupancy, and confidence score
4. **Explore Factors**: Understand what influences the prediction

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

See [API_SPEC.md](docs/API_SPEC.md) for detailed API documentation.

## Documentation

- [API Specification](docs/API_SPEC.md)
- [Data Format](docs/DATA_FORMAT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Demo Script](docs/DEMO_SCRIPT.md)

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- scikit-learn (optional)

### Frontend
- React 18
- Vite
- React Router
- Axios

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Building for Production

```bash
# Frontend
cd frontend
npm run build

# Backend
# Use production ASGI server (Gunicorn + Uvicorn)
```

## License

MIT License

## Contributors

Built for IITG Hackathon 2026
