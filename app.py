import sys
from pathlib import Path

# Ensure root directory is on sys.path so 'backend.app...' resolves correctly
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import gradio as gr
from backend.app.main import app as fastapi_app

# Create a clean status landing page for Hugging Face Spaces
with gr.Blocks(title="FaceVPlus API") as demo:
    gr.Markdown("# 👁️ FaceVPlus Attendance System API")
    gr.Markdown("The REST API is live and operational with **16 GB RAM**.")
    gr.Markdown("### Useful Links:")
    gr.Markdown("- 📖 **[Interactive API Documentation (Swagger)](/docs)**")
    gr.Markdown("- 🩺 **[API Health Check](/api/health)**")

# Attach all FastAPI backend routes into Gradio's internal FastAPI app
for route in fastapi_app.routes:
    if route not in demo.app.routes:
        demo.app.routes.append(route)

# In Hugging Face Spaces, demo.launch() natively handles port binding and startup
demo.launch()
