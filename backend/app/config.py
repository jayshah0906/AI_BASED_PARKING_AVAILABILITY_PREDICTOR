"""Configuration settings for the parking prediction API."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


def _project_root():
    """Project root (parent of backend/)."""
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(backend_dir)


def _ml_paths():
    """Paths to ML model and data (from project root)."""
    root = _project_root()
    return {
        "model": os.path.join(root, "ml", "models", "parking_model.pkl"),
        "data_dir": os.path.join(root, "ml", "data", "processed"),
    }


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_TITLE: str = "Parking Availability Prediction API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database Settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./parking_prediction.db"
    )
    
    # Model Settings (legacy; used only if ML not enabled)
    MODEL_PATH: str = os.getenv(
        "MODEL_PATH",
        "../models_store/parking_model.pkl"
    )
    
    # ML integration: paths and zone mapping
    USE_ML_MODEL: bool = os.getenv("USE_ML_MODEL", "true").lower() in ("true", "1", "yes")
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", _ml_paths()["model"])
    ML_DATA_DIR: str = os.getenv("ML_DATA_DIR", _ml_paths()["data_dir"])
    # Map backend zone_id (1-10) to ML zone_id (e.g. BF_001)
    ML_ZONE_ID_MAP: dict = {
        1: "BF_001",  # Downtown Pike St
        2: "BF_002",  # Downtown 1st Ave
        3: "BF_003",  # Downtown 3rd Ave
        4: "BF_120",  # Capitol Hill - Broadway
        5: "BF_200",  # University District - University Way
        6: "BF_045",  # Stadium District - Occidental
        7: "BF_046",  # Stadium District - 1st Ave S
        8: "BF_121",  # Capitol Hill - Pike St
        9: "BF_201",  # University District - 45th St
        10: "BF_202", # Fremont - Fremont Ave
    }
    
    # Data Paths
    DATA_DIR: str = os.getenv("DATA_DIR", "../data")
    RAW_DATA_DIR: str = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR: str = os.path.join(DATA_DIR, "processed")
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # Prediction Settings
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.7
    PREDICTION_HORIZON_HOURS: int = 2
    
    # Zone Settings
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
