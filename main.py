from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI(title="Travel Planner Backend")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
