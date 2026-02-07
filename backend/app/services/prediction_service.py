"""Prediction service for parking availability."""
import os
import sys
import pickle
from datetime import datetime
from typing import Dict, Optional

from app.config import settings
from app.services.feature_builder import build_features, get_feature_vector
from app.services.confidence_service import calculate_confidence
from app.models.prediction_model import AvailabilityLevel


def _ml_src_path():
    """Path to ml/src for importing ML predict module."""
    # Get the directory containing this file (services/)
    services_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up to app/
    app_dir = os.path.dirname(services_dir)
    # Go up to backend/
    backend_dir = os.path.dirname(app_dir)
    # Go up to project root
    project_root = os.path.dirname(backend_dir)
    # Return ml/src path
    ml_src = os.path.join(project_root, "ml", "src")
    return ml_src


class PredictionService:
    """Service for making parking availability predictions."""

    def __init__(self):
        """Initialize prediction service. Prefer ML model from ml/ if available."""
        self.model = None
        self.ml_available = False
        self._ml_predict_fn = None
        self._ml_model_path = None
        self._ml_data_dir = None
        self._init_ml_or_legacy()

    def _init_ml_or_legacy(self):
        """Try to load ML model from ml/ folder; otherwise keep rule-based fallback."""
        if not settings.USE_ML_MODEL:
            return
        model_path = settings.ML_MODEL_PATH
        data_dir = settings.ML_DATA_DIR
        if not os.path.isfile(model_path) or not os.path.isdir(data_dir):
            return
        ml_src = _ml_src_path()
        if ml_src not in sys.path:
            sys.path.insert(0, ml_src)
        try:
            from predict import predict_occupancy_at_time
            from predict import load_model
            load_model(model_path=model_path, data_dir=data_dir)
            self._ml_predict_fn = predict_occupancy_at_time
            self._ml_model_path = model_path
            self._ml_data_dir = data_dir
            self.ml_available = True
        except Exception as e:
            print(f"ML model not used: {e}")

    def predict_occupancy(
        self,
        zone_id: int,
        date_str: str,
        hour: int,
        day_of_week: int,
        events: list = None
    ) -> Dict:
        """Predict parking occupancy for given parameters.
        Uses ML model from ml/ folder when available, else rule-based.
        """
        features = build_features(zone_id, date_str, hour, day_of_week, events)

        if self.ml_available and self._ml_predict_fn:
            ml_zone_id = settings.ML_ZONE_ID_MAP.get(zone_id)
            if ml_zone_id:
                try:
                    target_dt = datetime.strptime(
                        f"{date_str} {hour:02d}:00:00",
                        "%Y-%m-%d %H:%M:%S"
                    )
                    result = self._ml_predict_fn(
                        ml_zone_id,
                        target_dt,
                        model_path=self._ml_model_path,
                        data_dir=self._ml_data_dir,
                    )
                    occupancy = result.get("occupancy_percent", result.get("occupancy_rate", 0.5) * 100)
                    confidence = result.get("confidence", 85) / 100.0  # Convert to 0-1 range
                    availability_level = self._occupancy_to_availability(occupancy)
                    return {
                        "occupancy": round(occupancy, 1),
                        "availability_level": availability_level,
                        "confidence": confidence,
                        "features": features,
                    }
                except Exception as e:
                    print(f"ML prediction error, using fallback: {e}")

        # Fallback: rule-based or legacy pickle model
        feature_vector = get_feature_vector(features)
        if self.model:
            try:
                occupancy = self.model.predict([feature_vector])[0]
                occupancy = max(0, min(100, float(occupancy)))
            except Exception:
                occupancy = self._rule_based_prediction(features)
        else:
            occupancy = self._rule_based_prediction(features)
        confidence = calculate_confidence(features)
        availability_level = self._occupancy_to_availability(occupancy)
        return {
            "occupancy": round(occupancy, 1),
            "availability_level": availability_level,
            "confidence": confidence,
            "features": features,
        }
    
    def _rule_based_prediction(self, features: Dict) -> float:
        """Rule-based prediction when ML model is not available.
        
        Args:
            features: Feature dictionary
        
        Returns:
            Predicted occupancy percentage
        """
        base_occupancy = 50.0
        
        # Zone-specific base occupancy
        if features["is_business_district"]:
            base_occupancy = 70.0
        elif features["is_shopping_area"]:
            base_occupancy = 60.0
        elif features["is_residential"]:
            base_occupancy = 40.0
        elif features["is_educational"]:
            base_occupancy = 65.0
        
        # Time adjustments
        if features["is_rush_hour"]:
            base_occupancy += 20.0
        elif features["is_night"]:
            base_occupancy -= 30.0
        elif features["is_morning"]:
            base_occupancy += 10.0
        
        # Weekend adjustments
        if features["is_weekend"]:
            if features["is_shopping_area"]:
                base_occupancy += 15.0
            elif features["is_business_district"]:
                base_occupancy -= 20.0
        
        # Traffic impact
        base_occupancy += features["traffic_impact"] * 30.0
        
        # Event impact
        base_occupancy += features["event_impact"] * 40.0
        
        # Ensure within bounds
        return max(0.0, min(100.0, base_occupancy))
    
    def _occupancy_to_availability(self, occupancy: float) -> AvailabilityLevel:
        """Convert occupancy percentage to availability level.
        
        Args:
            occupancy: Occupancy percentage (0-100)
        
        Returns:
            Availability level
        """
        if occupancy < 50:
            return "High"
        elif occupancy < 80:
            return "Medium"
        else:
            return "Low"


# Singleton instance
prediction_service = PredictionService()
