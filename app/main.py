from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
import os
import uuid

from app.utils.config import Settings, get_settings

app = FastAPI()

TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

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
