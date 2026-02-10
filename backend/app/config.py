import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


def _project_root():
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(backend_dir)


def _ml_paths():
    root = _project_root()
    return {
        "model": os.path.join(root, "ml", "models", "parking_model.pkl"),
        "data_dir": os.path.join(root, "ml", "data", "processed"),
    }


class Settings(BaseSettings):
    API_TITLE: str = "Parking Availability Prediction API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mongodb://localhost:27017/parking_db"
    )
    
    MODEL_PATH: str = os.getenv(
        "MODEL_PATH",
        "../models_store/parking_model.pkl"
    )
    
    USE_ML_MODEL: bool = os.getenv("USE_ML_MODEL", "true").lower() in ("true", "1", "yes")
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", _ml_paths()["model"])
    ML_DATA_DIR: str = os.getenv("ML_DATA_DIR", _ml_paths()["data_dir"])
    
    ML_ZONE_ID_MAP: dict = {
        1: "BF_001",
        2: "BF_002",
        3: "BF_003",
        4: "BF_120",
        5: "BF_200",
        6: "BF_045",
        7: "BF_046",
        8: "BF_121",
        9: "BF_201",
        10: "BF_202",
    }
    
    DATA_DIR: str = os.getenv("DATA_DIR", "../data")
    RAW_DATA_DIR: str = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR: str = os.path.join(DATA_DIR, "processed")
    
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://ai-based-parking-availability-predictor-3.onrender.com",
    ]
    
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.7
    PREDICTION_HORIZON_HOURS: int = 2
    
    DEFAULT_ZONES: list = [
        {"id": 1, "name": "Downtown Pike St", "lat": 47.6105, "lng": -122.3380},
        {"id": 2, "name": "Downtown 1st Ave", "lat": 47.6050, "lng": -122.3350},
        {"id": 3, "name": "Downtown 3rd Ave", "lat": 47.6080, "lng": -122.3310},
        {"id": 4, "name": "Capitol Hill - Broadway", "lat": 47.6240, "lng": -122.3210},
        {"id": 5, "name": "University District - University Way", "lat": 47.6650, "lng": -122.3130},
        {"id": 6, "name": "Stadium District - Occidental", "lat": 47.5920, "lng": -122.3330},
        {"id": 7, "name": "Stadium District - 1st Ave S", "lat": 47.5970, "lng": -122.3280},
        {"id": 8, "name": "Capitol Hill - Pike St", "lat": 47.6180, "lng": -122.3150},
        {"id": 9, "name": "University District - 45th St", "lat": 47.6590, "lng": -122.3080},
        {"id": 10, "name": "Fremont - Fremont Ave", "lat": 47.6505, "lng": -122.3493},
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
