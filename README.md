# AI-Based Parking Availability Predictor

A web application that predicts parking availability across city zones using machine learning. The system analyzes historical parking data, events, and traffic patterns to help drivers find parking more efficiently.

## Features

- Real-time parking availability predictions
- Interactive map interface with zone selection
- Machine learning model with 87% accuracy
- Event-aware predictions (concerts, sports games, etc.)
- User authentication and personalized dashboard
- Confidence scores for prediction reliability

## Tech Stack

**Frontend**
- React 18
- Vite
- Leaflet Maps
- Axios

**Backend**
- FastAPI
- MongoDB Atlas
- JWT Authentication
- Motor (async MongoDB driver)

**Machine Learning**
- Scikit-learn (Random Forest)
- Pandas & NumPy
- 10,000+ training samples

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python3 run_server.py
```

Create a `.env` file in the backend directory:
```
DATABASE_URL=your_mongodb_connection_string
SECRET_KEY=your_secret_key
USE_ML_MODEL=true
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:8001/api/v1
```

## Usage

1. Start the backend server (runs on port 8001)
2. Start the frontend development server (runs on port 5173)
3. Open http://localhost:5173 in your browser
4. Register an account or log in
5. Select a date and time
6. Click on a zone to view parking predictions

## API Documentation

Once the backend is running, visit http://localhost:8001/docs for interactive API documentation.

## Project Structure

```
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── ml/              # ML model and training scripts
├── data/            # Dataset files
└── docs/            # API documentation
```

## Model Performance

- Accuracy: 87%
- Prediction Speed: <10ms
- Zones Covered: 10 Seattle zones
- Features: 15+ temporal and spatial features

## Deployment

The application is deployed on Render:
- Backend: Python web service
- Frontend: Static site
- Database: MongoDB Atlas

## License

MIT License

## Contributors

Built for IITG Hackathon 2026
