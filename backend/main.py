from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# 1. Load environment variables (API Keys)
load_dotenv()

# 2. Configure Google Gemini AI
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# 3. Initialize the FastAPI App
app = FastAPI(
    title="Medical AI Assistant API",
    description="Backend for analyzing medical symptoms using Google Gemini AI",
    version="1.0.0"
)

# 4. Setup CORS (Allows React Frontend to talk to this Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change this to specific URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models (Pydantic) ---
# These define the structure of data we send and receive

class SymptomInput(BaseModel):
    description: str

class DiagnosisResponse(BaseModel):
    disease_name: str
    analysis_reasoning: str
    suggested_treatment: str
    disclaimer: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Medical AI API is running", "status": "active"}

@app.get("/health")
def health_check():
    """Checks if the server is active."""
    return {"status": "ok"}

@app.post("/analyze", response_model=DiagnosisResponse)
async def analyze_symptoms(symptoms: SymptomInput):
    """
    Receives a symptom description, sends it to Gemini AI, 
    and returns a structured medical analysis with a mandatory disclaimer.
    """
    if not symptoms.description:
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    # Prompt Engineering: Instructing the AI on how to behave
    prompt = f"""
    Act as a medical diagnostic assistant. Analyze the following patient symptoms:
    "{symptoms.description}"

    Return a strictly valid JSON object (no markdown formatting, no backticks) with the following keys:
    1. "disease_name": A likely condition based on symptoms.
    2. "analysis_reasoning": Explain why this condition fits the symptoms based on medical logic.
    3. "suggested_treatment": Suggest standard medical treatments or medicines.
    4. "disclaimer": EXACTLY THIS TEXT: "PLEASE DONT DEPEND ON THESE RESULTS BECAUSE IT MIGHT BE FALSE ALWAYS GO TO THE DOCTOR I AM NOT RESPONSIBLE IF YOU PURELY DEPENT ON THIS."

    Do not include any text outside the JSON object.
    """

    try:
        # Call Google Gemini API
        response = model.generate_content(prompt)
        
        # Clean the response (Remove markdown ```json ... ``` if the AI adds it)
        response_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # Parse text into a Python Dictionary
        data = json.loads(response_text)

        # Return structured data to the user
        return DiagnosisResponse(
            disease_name=data.get("disease_name", "Unknown Condition"),
            analysis_reasoning=data.get("analysis_reasoning", "Analysis unavailable"),
            suggested_treatment=data.get("suggested_treatment", "Consult a doctor"),
            disclaimer=data.get("disclaimer", "PLEASE DONT DEPEND ON THESE RESULTS BECAUSE IT MIGHT BE FALSE ALWAYS GO TO THE DOCTOR I AM NOT RESPONSIBLE IF YOU PURELY DEPENT ON THIS.")
        )

    except json.JSONDecodeError:
        # This happens if the AI returns text instead of JSON
        raise HTTPException(status_code=500, detail="AI response format error. Please try again.")
    except Exception as e:
        # General error handling
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during AI analysis")