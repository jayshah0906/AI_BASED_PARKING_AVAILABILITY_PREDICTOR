# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Step-by-Step Setup

### 1. Backend Setup

Open a terminal and run:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database with zones
python scripts/seed_zones.py

# (Optional) Import sample data
python scripts/import_data.py

# Start the backend server
python run_server.py
```

The backend API will be running at `http://localhost:8001`
- API Docs: `http://localhost:8001/docs`
- Health Check: `http://localhost:8001/api/v1/health`

### 2. Frontend Setup

Open a **new terminal** and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be running at `http://localhost:5173`

### 3. Using the Application

1. Open your browser and go to `http://localhost:5173`
2. Select a parking zone from the map or dropdown
3. Choose a date and time
4. View the parking availability prediction

## Testing the API

### Using curl:

```bash
# Health check
curl http://localhost:8001/api/v1/health

# Get all zones
curl http://localhost:8001/api/v1/zones

# Make a prediction
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "zone_id": 1,
    "day_of_week": 1,
    "hour": 14,
    "date": "2026-02-07"
  }'
```

### Using the Swagger UI:

Visit `http://localhost:8001/docs` for an interactive API documentation interface.

## Troubleshooting

### Backend Issues

**Port 8001 already in use:**
- Change the port in `backend/run_server.py` or kill the process using port 8001

**Module not found errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Database errors:**
- Delete `parking_prediction.db` and run `python scripts/seed_zones.py` again

### Frontend Issues

**Cannot connect to API:**
- Ensure backend is running on port 8001
- Check `frontend/.env` file has correct API URL
- Verify CORS settings in `backend/app/config.py`

**npm install fails:**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then run `npm install` again

## Project Structure

```
IITG_HACK/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   ├── scripts/         # Utility scripts
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/            # Source code
│   └── package.json    # Node dependencies
├── data/                # Data files
└── docs/               # Documentation
```

## Next Steps

- Read the [Architecture Documentation](docs/ARCHITECTURE.md)
- Check the [API Specification](docs/API_SPEC.md)
- Review the [Demo Script](docs/DEMO_SCRIPT.md) for presentation tips

## Support

For issues or questions, refer to the documentation in the `docs/` directory.
