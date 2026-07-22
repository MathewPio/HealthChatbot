from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.health_profile import (
    router as health_profile_router
)
from app.api.chat import router as chat_router

app = FastAPI(
    title = "Health Chatbot API",
    version="1.0.0",
    description="Backend API for the Health Chatbot Final Year Project"
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(health_profile_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Health Chatbot API"
    }