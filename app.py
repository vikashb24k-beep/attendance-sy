import sys
from pathlib import Path

# Ensure root directory is on sys.path so 'backend.app...' resolves correctly
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Satisfy Hugging Face ZeroGPU requirement if running on ZeroGPU hardware
try:
    import spaces
    @spaces.GPU
    def _zero_gpu_init():
        return True
except Exception:
    pass

import gradio as gr
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.routes import auth, subjects, attendance, admin

# 1. Create the Gradio interface
with gr.Blocks(title="FaceVPlus API") as demo:
    gr.Markdown("# 👁️ FaceVPlus Attendance System API")
    gr.Markdown("The REST API is live and operational with **16 GB RAM** on Hugging Face Spaces.")
    gr.Markdown("### Useful Links:")
    gr.Markdown("- 📖 **[Interactive Swagger API Docs](/docs)**")
    gr.Markdown("- 🩺 **[API Health Check](/api/health)**")

# 2. Register all FastAPI backend routers directly onto Gradio's internal FastAPI app
demo.app.include_router(auth.router, prefix="/api")
demo.app.include_router(subjects.router, prefix="/api")
demo.app.include_router(subjects.invitation_router, prefix="/api")
demo.app.include_router(attendance.router, prefix="/api")
demo.app.include_router(admin.router, prefix="/api")

@demo.app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "supabase_configured": bool(settings.SUPABASE_URL and settings.SUPABASE_KEY),
    }

# 3. Add CORS middleware so the frontend can query the API
cors_origins = settings.get_cors_origins()
demo.app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Launch Gradio with ssr_mode=False
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        ssr_mode=False,
    )
