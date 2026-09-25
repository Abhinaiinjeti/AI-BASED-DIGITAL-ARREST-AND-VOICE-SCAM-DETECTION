"""
Main FastAPI Application Entrypoint
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION
"""

import sys
from pathlib import Path

# Add project root to sys.path so ml and backend modules import seamlessly
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.api.routes import router as api_router

# Initialize FastAPI app with exact project title
app = FastAPI(
    title="AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION",
    description="Multilingual risk detection and explainable decision-support system for digital arrest and voice scams.",
    version="1.0.0",
)

# Enable CORS for frontend development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes under /api and root
app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "project": "AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION",
        "status": "operational",
        "documentation": "/docs",
        "health_check": "/api/health",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Hide raw internal stack trace while returning informative user error
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": f"An error occurred during analysis: {str(exc)}",
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
