"""
FastAPI Application for HealthSense AI
Main API endpoints for the healthcare multi-agent system
Serves frontend and provides backend API
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.HospitalComparisonAgent import HospitalComparisonAgent
from src.constants import MODEL_NAME, OPENAI_API_KEY

# Import API routers
from src.routes import emergency, hospitals, doctors, tests, chat

# Initialize FastAPI app
app = FastAPI(
    title="HealthSense AI",
    description="AI-Driven Multi-Agent Healthcare System",
    version="1.0.0"
)

# CORS middleware (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    print(f"Static files mounted from: {static_path}")
else:
    print(f"Warning: Static directory not found at {static_path}")

# Include API routers
app.include_router(emergency.router, prefix="/api", tags=["Emergency Services"])
app.include_router(hospitals.router, prefix="/api", tags=["Hospitals"])
app.include_router(doctors.router, prefix="/api", tags=["Doctors"])
app.include_router(tests.router, prefix="/api", tags=["Lab Tests"])
app.include_router(chat.router, tags=["AI Chat"])

print("All API routers included")

# Initialize agents (legacy support)
hospital_agent = None
try:
    hospital_agent = HospitalComparisonAgent().hospital_info_agent
except Exception as e:
    print(f"Warning: Could not initialize Hospital Agent: {e}")
    hospital_agent = None

# Request/Response models (legacy support)
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    agent: str = "hospital_comparison"

@app.get("/")
def home():
    """Serve the frontend home page"""
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {
            "message": "Welcome to HealthSense AI",
            "version": "1.0.0",
            "description": "AI-Driven Multi-Agent Healthcare System",
            "api_docs": "/docs",
            "frontend": "Static files not found - please ensure frontend is in 'static' directory"
        }

@app.get("/index.html")
def index_page():
    """Serve index page"""
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/emergency.html")
def emergency_page():
    """Serve emergency page"""
    return FileResponse(os.path.join(static_path, "emergency.html"))

@app.get("/hospitals.html")
def hospitals_page():
    """Serve hospitals page"""
    return FileResponse(os.path.join(static_path, "hospitals.html"))

@app.get("/doctors.html")
def doctors_page():
    """Serve doctors page"""
    return FileResponse(os.path.join(static_path, "doctors.html"))

@app.get("/tests.html")
def tests_page():
    """Serve tests page"""
    return FileResponse(os.path.join(static_path, "tests.html"))

@app.get("/chat.html")
def chat_page():
    """Serve chat page"""
    return FileResponse(os.path.join(static_path, "chat.html"))

@app.get("/css/{file_path:path}")
def serve_css(file_path: str):
    """Serve CSS files"""
    return FileResponse(os.path.join(static_path, "css", file_path))

@app.get("/js/{file_path:path}")
def serve_js(file_path: str):
    """Serve JavaScript files"""
    return FileResponse(os.path.join(static_path, "js", file_path))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "api_key_set": bool(OPENAI_API_KEY),
        "frontend_available": os.path.exists(static_path),
        "agents": {
            "emergency": True,
            "hospital": True,
            "doctor": True,
            "diagnostic": True
        }
    }

# Legacy endpoints (backward compatibility)
@app.post("/compare-hospitals", response_model=QueryResponse)
def compare_hospitals(request: QueryRequest):
    """
    Compare hospitals based on user query (LEGACY)
    Use /api/hospitals instead

    Args:
        request: QueryRequest containing the user's query

    Returns:
        QueryResponse with comparison results
    """
    try:
        if not hospital_agent:
            raise HTTPException(status_code=503, detail="Hospital service unavailable")

        if not request.query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        response = hospital_agent.run(request.query)

        return QueryResponse(
            response=response,
            agent="hospital_comparison"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def general_query(request: QueryRequest):
    """
    General query endpoint (LEGACY)
    Use /chat instead

    Args:
        request: QueryRequest containing the user's query

    Returns:
        QueryResponse with results
    """
    try:
        if not hospital_agent:
            raise HTTPException(status_code=503, detail="Service unavailable")

        if not request.query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        response = hospital_agent.run(request.query)

        return {
            "response": response,
            "agent": "hospital_comparison"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    from src.constants import API_HOST, API_PORT

    print("\n" + "="*80)
    print("STARTING HEALTHSENSE AI SERVER")
    print("="*80)
    print(f"Host: {API_HOST}")
    print(f"Port: {API_PORT}")
    print(f"Static files: {static_path}")
    print(f"API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print(f"Frontend: http://{API_HOST}:{API_PORT}/")
    print("="*80 + "\n")

    uvicorn.run(app, host=API_HOST, port=API_PORT)
