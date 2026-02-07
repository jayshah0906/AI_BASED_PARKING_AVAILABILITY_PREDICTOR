"""Event routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.request_response import EventResponse

router = APIRouter()

# In-memory events storage (can be replaced with database)
EVENTS_STORAGE = [
    # Zone 1 - Downtown Pike St
    {
        "id": 1,
        "name": "Tech Innovation Summit",
        "zone_id": 1,
        "date": "2026-02-07",
        "start_time": "09:00",
        "end_time": "17:00",
        "expected_impact": "High"
    },
    # Zone 2 - Downtown 1st Ave
    {
        "id": 2,
        "name": "Business Conference",
        "zone_id": 2,
        "date": "2026-02-07",
        "start_time": "09:00",
        "end_time": "17:00",
        "expected_impact": "Medium"
    },
    # Zone 3 - Downtown 3rd Ave
    {
        "id": 3,
        "name": "Weekend Market",
        "zone_id": 3,
        "date": "2026-02-08",
        "start_time": "10:00",
        "end_time": "16:00",
        "expected_impact": "High"
    },
    # Zone 4 - Capitol Hill - Broadway
    {
        "id": 4,
        "name": "Capitol Hill Block Party",
        "zone_id": 4,
        "date": "2026-07-24",
        "start_time": "12:00",
        "end_time": "22:00",
        "expected_impact": "High"
    },
    # Zone 6 - Stadium District - Occidental
    {
        "id": 5,
        "name": "Seahawks vs 49ers",
        "zone_id": 6,
        "date": "2026-09-13",
        "start_time": "13:00",
        "end_time": "17:00",
        "expected_impact": "High"
    },
    # Zone 6 - Stadium District (Super Bowl Watch Party)
    {
        "id": 6,
        "name": "Super Bowl Watch Party",
        "zone_id": 6,
        "date": "2026-02-08",
        "start_time": "15:00",
        "end_time": "20:00",
        "expected_impact": "High"
    },
    # Zone 7 - Stadium District - 1st Ave S
    {
        "id": 7,
        "name": "Mariners vs Yankees",
        "zone_id": 7,
        "date": "2026-04-17",
        "start_time": "19:00",
        "end_time": "22:00",
        "expected_impact": "High"
    },
    # Zone 8 - Capitol Hill - Pike St
    {
        "id": 8,
        "name": "Seattle International Film Festival",
        "zone_id": 8,
        "date": "2026-05-16",
        "start_time": "10:00",
        "end_time": "22:00",
        "expected_impact": "High"
    },
    # Zone 9 - University District - 45th St
    {
        "id": 9,
        "name": "University District Street Fair",
        "zone_id": 9,
        "date": "2026-05-23",
        "start_time": "10:00",
        "end_time": "18:00",
        "expected_impact": "High"
    },
    # Zone 10 - Fremont - Fremont Ave
    {
        "id": 10,
        "name": "Fremont Solstice Parade",
        "zone_id": 10,
        "date": "2026-06-20",
        "start_time": "13:00",
        "end_time": "17:00",
        "expected_impact": "High"
    },
]


async def get_events_for_zone(
    zone_id: int,
    date: str,
    db: Session
) -> List[EventResponse]:
    """Get events for a specific zone on a given date."""
    events = [
        EventResponse(**event)
        for event in EVENTS_STORAGE
        if event["zone_id"] == zone_id and event["date"] == date
    ]
    return events


@router.get("/events", response_model=List[EventResponse])
async def get_events(
    zone_id: Optional[int] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all events, optionally filtered by zone and date."""
    events = EVENTS_STORAGE
    
    if zone_id:
        events = [e for e in events if e["zone_id"] == zone_id]
    
    if date:
        events = [e for e in events if e["date"] == date]
    
    return [EventResponse(**event) for event in events]


@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID."""
    event = next((e for e in EVENTS_STORAGE if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(**event)
