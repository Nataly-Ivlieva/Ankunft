"""
Application entry point.

This module initializes the FastAPI application, configures
CORS middleware, and registers API routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.api import api_router
from app.api import auth

# Create FastAPI application instance
app = FastAPI()

# Configure CORS to allow requests from the frontend application
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register authentication-related routes
app.include_router(auth.router)
# Register main API routes
app.include_router(api_router)




