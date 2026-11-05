import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path so 'backend.app...' resolves correctly
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from gradio import Server
import spaces
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.routes import auth, subjects, attendance, admin

# Initialize Gradio Server (inherits directly from FastAPI)
app = Server(title=settings.APP_NAME)

# Satisfy ZeroGPU requirement with a registered API endpoint
@app.api(name="ping")
@spaces.GPU
def ping(text: str = "health") -> str:
    return f"ZeroGPU API active: {text}"

# Enable wide-open CORS so Render frontend and localhost connect without issues
cors_origins = settings.get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all REST API routes
app.include_router(auth.router, prefix="/api")
app.include_router(subjects.router, prefix="/api")
app.include_router(subjects.invitation_router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/api/health")
def api_health():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "supabase_configured": bool(settings.SUPABASE_URL and settings.SUPABASE_KEY),
    }

@app.get("/")
def root_status():
    return {
        "message": "FaceVPlus API is running successfully on Hugging Face Spaces!",
        "health": "/api/health",
        "docs": "/docs",
    }

if __name__ == "__main__":
    app.launch()
