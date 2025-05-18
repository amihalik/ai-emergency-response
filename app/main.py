from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

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
