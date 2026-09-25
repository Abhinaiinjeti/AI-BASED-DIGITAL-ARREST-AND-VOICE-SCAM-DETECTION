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

# Mount API routes under /api
app.include_router(api_router, prefix="/api")

# Mount frontend static files if dist directory exists (Production / Docker / Render)
DIST_DIR = BASE_DIR / "frontend" / "dist"
if DIST_DIR.exists() and (DIST_DIR / "index.html").exists():
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from fastapi import HTTPException

    if (DIST_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

    @app.get("/")
    def serve_frontend_index():
        return FileResponse(str(DIST_DIR / "index.html"))

    @app.get("/{full_path:path}")
    def serve_frontend_spa(full_path: str):
        if full_path.startswith("api/") or full_path in ("docs", "redoc", "openapi.json"):
            raise HTTPException(status_code=404, detail="Not Found")
        target_file = DIST_DIR / full_path
        if target_file.exists() and target_file.is_file():
            return FileResponse(str(target_file))
        return FileResponse(str(DIST_DIR / "index.html"))
else:
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
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=False)
