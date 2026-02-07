"""CORS middleware configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def setup_cors(app: FastAPI):
    """Configure CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )
