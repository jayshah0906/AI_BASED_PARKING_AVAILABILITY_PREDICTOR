"""Prediction routes."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.zone_model import Zone
from app.models.prediction_model import PredictionRequest, PredictionResponse
from app.services.prediction_service import prediction_service
from app.routes.events import get_events_for_zone

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_availability(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """Predict parking availability for a zone at a specific time."""
    
    # Get zone information
    zone = db.query(Zone).filter(Zone.id == request.zone_id).first()
    if not zone:
        from app.config import settings
        default_zone = next((z for z in settings.DEFAULT_ZONES if z["id"] == request.zone_id), None)
        if not default_zone:
            raise HTTPException(status_code=404, detail="Zone not found")
        zone_name = default_zone["name"]
    else:
        zone_name = zone.name
    
    # Get zone capacity from ML config
    from app.config import settings
    ml_zone_id = settings.ML_ZONE_ID_MAP.get(request.zone_id)
    
    # Import ML config to get capacity
    import sys
    import os
    ml_src = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "ml", "src")
    if ml_src not in sys.path:
        sys.path.insert(0, ml_src)
    
    try:
        from config import ZONE_METADATA
        zone_metadata = ZONE_METADATA.get(ml_zone_id, {})
        total_spaces = zone_metadata.get('capacity', 20)
    except:
        total_spaces = 20  # Default fallback
    
    # Get events for the zone
    events = await get_events_for_zone(request.zone_id, request.date, db)
    
    # Make prediction
    prediction_result = prediction_service.predict_occupancy(
        zone_id=request.zone_id,
        date_str=request.date,
        hour=request.hour,
        day_of_week=request.day_of_week,
        events=events
    )
    
    # Calculate available spaces
    occupancy_rate = prediction_result["occupancy"] / 100.0
    available_spaces = int((1 - occupancy_rate) * total_spaces)
    
    # Build factors dictionary
    features = prediction_result["features"]
    time_of_day = "night"
    if features.get("is_morning"):
        time_of_day = "morning"
    elif features.get("is_afternoon"):
        time_of_day = "afternoon"
    elif features.get("is_evening"):
        time_of_day = "evening"
    
    factors = {
        "time_of_day": time_of_day,
        "is_weekend": features["is_weekend"],
        "traffic_level": features["traffic_level"],
        "events_nearby": features["events_count"]
    }
    
    # Create response
    timestamp = datetime.strptime(
        f"{request.date} {request.hour:02d}:00:00",
        "%Y-%m-%d %H:%M:%S"
    ).isoformat()
    
    return PredictionResponse(
        zone_id=request.zone_id,
        zone_name=zone_name,
        availability_level=prediction_result["availability_level"],
        confidence_score=prediction_result["confidence"],
        predicted_occupancy=prediction_result["occupancy"],
        available_spaces=available_spaces,
        total_spaces=total_spaces,
        timestamp=timestamp,
        factors=factors
    )
