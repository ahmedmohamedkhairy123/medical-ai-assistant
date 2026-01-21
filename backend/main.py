from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Initialize the App
app = FastAPI(
    title="Medical AI Assistant API",
    description="Backend for analyzing medical symptoms using AI",
    version="1.0.0"
)

# 3. Setup CORS (Cross-Origin Resource Sharing)
# This allows your React frontend (Phase 4) to talk to this Python backend.
# For now, we allow all origins ("*") for development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Basic Routes
@app.get("/")
def read_root():
    return {"message": "Medical AI API is running", "status": "active"}

@app.get("/health")
def health_check():
    """Checks if the server is active."""
    return {"status": "ok"}