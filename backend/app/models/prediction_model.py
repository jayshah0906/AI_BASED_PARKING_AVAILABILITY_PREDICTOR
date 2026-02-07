"""Prediction result model."""
from typing import Literal
from pydantic import BaseModel, Field


AvailabilityLevel = Literal["High", "Medium", "Low"]


class PredictionRequest(BaseModel):
    """Request model for parking prediction."""
    
    zone_id: int = Field(..., description="Zone ID for prediction")
    day_of_week: int = Field(..., ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "zone_id": 1,
                "day_of_week": 1,
                "hour": 14,
                "date": "2026-02-07"
            }
        }


class PredictionResponse(BaseModel):
    """Response model for parking prediction."""
    
    zone_id: int
    zone_name: str
    availability_level: AvailabilityLevel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    predicted_occupancy: float = Field(..., ge=0.0, le=100.0, description="Predicted occupancy percentage")
    available_spaces: int = Field(..., description="Number of available parking spaces")
    total_spaces: int = Field(..., description="Total parking spaces in zone")
    timestamp: str
    factors: dict = Field(default_factory=dict, description="Factors influencing prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "zone_id": 1,
                "zone_name": "Downtown",
                "availability_level": "Medium",
                "confidence_score": 0.85,
                "predicted_occupancy": 65.5,
                "timestamp": "2026-02-07T14:00:00",
                "factors": {
                    "time_of_day": "afternoon",
                    "is_weekend": False,
                    "traffic_level": "moderate",
                    "events_nearby": 0
                }
            }
        }
