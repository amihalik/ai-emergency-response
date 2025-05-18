from fastapi import (
    Request, 
    Depends,
    FastAPI,
    File,
    Form,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from app.utils.config import Settings, get_settings

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(TMP_DIR, exist_ok=True)


# In-memory incident store for demo purposes
incidents = [
    {
        "id": 1,
        "caller": "John Doe",
        "transcription": "There's smoke coming from my neighbor's house!",
        "background_noise": "sirens",
        "incident_type": "Fire",
        "severity": "High",
        "resources": "2 Engines",
        "eta": "5 min",
        "lat": 37.7749,
        "lon": -122.4194,
    },
    {
        "id": 2,
        "caller": "Jane Smith",
        "transcription": "I think someone is breaking in next door",
        "background_noise": "dogs barking",
        "incident_type": "Burglary",
        "severity": "Medium",
        "resources": "1 Patrol Car",
        "eta": "3 min",
        "lat": 34.0522,
        "lon": -118.2437,
    },
]

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "incidents": incidents})

@app.get("/edit/{incident_id}", response_class=HTMLResponse)
async def edit_incident(request: Request, incident_id: int):
    incident = next((i for i in incidents if i["id"] == incident_id), None)
    if not incident:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("edit.html", {"request": request, "incident": incident})

@app.post("/update/{incident_id}")
async def update_incident(
    incident_id: int,
    severity: str = Form(...),
    resources: str = Form(...),
):
    for incident in incidents:
        if incident["id"] == incident_id:
            incident["severity"] = severity
            incident["resources"] = resources
            break
    return RedirectResponse("/", status_code=302)


@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok"}

@app.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
):
    """Receive an audio file and associated geolocation metadata."""
    file_id = str(uuid.uuid4())
    temp_path = os.path.join(TMP_DIR, f"{file_id}_{file.filename}")
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Placeholder: send file to Azure APIs here

    return {
        "file_id": file_id,
        "saved_to": temp_path,
        "latitude": latitude,
        "longitude": longitude,
    }


@app.websocket("/ws/audio")
async def websocket_endpoint(
    websocket: WebSocket,
    latitude: float,
    longitude: float,
):
    await websocket.accept()
    try:
        # Generate a unique id per connection to store streamed chunks
        conn_id = str(uuid.uuid4())
        conn_dir = os.path.join(TMP_DIR, conn_id)
        os.makedirs(conn_dir, exist_ok=True)

        # Save geolocation metadata for the connection
        with open(os.path.join(conn_dir, "metadata.txt"), "w") as meta:
            meta.write(f"{latitude},{longitude}")

        index = 0
        while True:
            data = await websocket.receive_bytes()
            chunk_path = os.path.join(conn_dir, f"chunk_{index}.wav")
            with open(chunk_path, "wb") as chunk_file:
                chunk_file.write(data)
            index += 1
            # Placeholder: stream chunk to Azure APIs here
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()
