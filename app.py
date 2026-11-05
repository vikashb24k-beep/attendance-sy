import sys
from pathlib import Path

# Ensure root directory is on sys.path so 'backend.app...' resolves correctly
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import gradio as gr
import uvicorn
from backend.app.main import app as fastapi_app

# Create a clean status landing page for Hugging Face Spaces
with gr.Blocks(title="FaceVPlus API") as demo:
    gr.Markdown("# 👁️ FaceVPlus Attendance System API")
    gr.Markdown("The REST API is live and operational with **16 GB RAM**.")
    gr.Markdown("### Useful Links:")
    gr.Markdown("- 📖 **Interactive API Documentation (Swagger)**: [/docs](/docs)")
    gr.Markdown("- 🩺 **API Health Check**: [/api/health](/api/health)")

# Mount the Gradio UI onto our FastAPI app (so all /api routes remain active)
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

