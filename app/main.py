from fastapi import FastAPI, Depends
from app.utils.config import Settings, get_settings

app = FastAPI()

@app.get('/health')
def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok"}
