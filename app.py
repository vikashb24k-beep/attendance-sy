import sys
import os
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
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.app.main import app

# Ensure wide-open CORS so Render frontend and local development work seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional Gradio Blocks UI (for monitoring / demo)
with gr.Blocks(title="FaceVPlus API") as demo:
    gr.Markdown("# 👁️ FaceVPlus Attendance System API")
    gr.Markdown("The REST API is live and operational on Hugging Face Spaces.")
    gr.Markdown("### Useful Links:")
    gr.Markdown("- 📖 **[Interactive Swagger API Docs](/docs)**")
    gr.Markdown("- 🩺 **[API Health Check](/api/health)**")

# Mount Gradio at /gradio so it doesn't collide with FastAPI root or API routes
app = gr.mount_gradio_app(app, demo, path="/gradio")

@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect root visitors directly to the interactive Swagger API documentation."""
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
