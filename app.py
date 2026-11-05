import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path so 'backend.app...' resolves correctly
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import gradio as gr
import spaces
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.routes import auth, subjects, attendance, admin

# 1. ZeroGPU Inference Handler (satisfies Hugging Face ZeroGPU startup scanner)
@spaces.GPU
def gpu_health_check(query: str):
    """ZeroGPU check endpoint."""
    return f"ZeroGPU backend active. Query: {query or 'health'}"

# 2. Gradio Interface
demo = gr.Interface(
    fn=gpu_health_check,
    inputs=gr.Textbox(label="Test Input", placeholder="Type a message or ping..."),
    outputs=gr.Textbox(label="Response"),
    title="👁️ FaceVPlus Attendance System API",
    description="The REST API is live and operational on Hugging Face Spaces (ZeroGPU Free Tier). Visit `/docs` for interactive API documentation.",
)

# 3. Register all FastAPI backend routes directly onto Gradio's internal FastAPI app
app = demo.app

# Enable CORS for Render frontend and local testing
cors_origins = settings.get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes under /api
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

# 4. Launch Gradio using native launch
if __name__ == "__main__":
    demo.launch(
        ssr_mode=False,
    )
