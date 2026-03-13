import asyncio
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Core Nanobot Imports (Adjust paths if your installation differs)
from nanobot.core.manager import AgentManager  
from nanobot.config import Config

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Nanobot Logic
# Ensure you have your config.yaml path correct
config = Config.from_file("config.yaml") 
manager = AgentManager(config)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def run_nanobot_stream(prompt: str):
    """
    Calls the Nanobot agent and yields tokens as they arrive.
    """
    try:
        # We use the manager to dispatch the task to the Chinese/Multi-Agent system
        # Assuming nanobot provides an async generator for streaming
        async for chunk in manager.arun(prompt):
            # Format for SSE (Server-Sent Events)
            # We wrap the text in a span to keep it inline during the swap
            yield f"data: <span>{chunk}</span>\n\n"
            await asyncio.sleep(0.02) # Smooth out the typing effect
    except Exception as e:
        yield f"data: <span class='text-red-500'>Error: {str(e)}</span>\n\n"
    
    # Send a custom 'end' event to tell HTMX to stop listening
    yield "event: end\ndata: \n\n"

@app.get("/chat-stream")
async def chat_stream(prompt: str):
    return StreamingResponse(
        run_nanobot_stream(prompt), 
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
