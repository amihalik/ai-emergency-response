"""FastAPI application exposing the incident processing endpoint."""

from fastapi import FastAPI, UploadFile, File
from emergency.flow import process_audio

app = FastAPI()


@app.post("/incident")
async def handle_incident(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    result = process_audio(audio_bytes)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
