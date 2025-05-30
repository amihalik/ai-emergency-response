# 911 AI Emergency Response System (Proof of Concept)

## Project Overview

This project aims to develop a Python-based proof-of-concept (PoC) web application that demonstrates real-time processing of emergency (911-type) calls using Azure OpenAI and Azure Cognitive Services. The PoC will ingest audio, transcribe speech-to-text, analyze caller voice attributes, classify background noises, identify incident details, and dynamically suggest emergency response resources based on geolocation.

## Objectives

* Validate real-time audio ingestion and transcription accuracy.
* Demonstrate the effectiveness of Azure OpenAI for classifying emergencies and analyzing caller attributes and critical background sounds.
* Showcase integration of geolocation-based emergency resource recommendations.
* Provide a foundation for scaling into a full-scale emergency response application.

## Features

### Audio Ingestion

* Accept live audio streams or uploaded audio recordings simulating 911 calls.
* Simulate geolocation metadata associated with incoming calls.

### Real-time Speech-to-Text

* Implement Azure Speech-to-Text API to transcribe audio into text.

### Caller Attribute Analysis

* Identify caller attributes such as gender, approximate age, and emotional state using Azure Speech Analytics.
* The `CallerAttributes` dataclass encapsulates the inferred gender, age group, and emotional state for each call.
* Attribute analysis runs alongside speech-to-text transcription in the processing pipeline.

### Background Noise Classification

* Classify critical background sounds (e.g., gunfire, alarms, explosions, shouting) using Azure Audio Classification or custom models.

### Incident Classification

* Leverage Azure OpenAI GPT to analyze transcriptions and classified audio cues, identifying emergency type (car accident, violence, fire, medical emergency).
* Extract essential incident details including severity and number of persons affected.
* Example implementation provided in `incident_classifier.py` which sends a structured prompt to Azure OpenAI and parses JSON results.

### Geolocation-based Emergency Resource Management

* Query preloaded datasets to identify nearest appropriate emergency resources (fire stations, hospitals, police stations).
* Provide real-time feedback on resource availability, estimated arrival times, and recommended immediate actions.

### Incident Dashboard

* Create an interactive web dashboard showing live incidents, caller attributes, background noise details, geolocation, emergency resource assignments, and response times.
* Allow manual updates and adjustments of incident details and emergency responses.

### Running the Dashboard

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the server:
```bash
uvicorn app.main:app --reload
```
Then open `http://localhost:8000` in your browser.

### Processing Pipeline

* Speech-to-text transcription and background noise classification are performed
  together on the same audio input.
* The pipeline returns an `Incident` data object containing the transcript and a
  list of detected background sounds with timestamps and confidence scores.

## Technical Stack

* **Frontend:** Python-based UI framework (e.g., Streamlit, FastAPI with minimal frontend)
* **Backend:** Python (FastAPI)
* **Cloud Services:** Azure OpenAI GPT, Azure Cognitive Services (Speech-to-Text, Speech Analytics, Audio Classification)
* **Database:** SQLite or PostgreSQL for storing incident data and emergency resource information

## Setup

Create and activate a Python virtual environment before installing the core dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the development server with:

```bash
uvicorn app.main:app --reload
```

### Environment Variables

Copy `.env.example` to `.env` and add your Azure resource credentials:

```bash
cp .env.example .env
# Edit .env and provide endpoint URLs and API keys
```

The application expects the following variables:

* `AZURE_SPEECH_ENDPOINT` and `AZURE_SPEECH_KEY`
* `AZURE_AUDIO_ENDPOINT` and `AZURE_AUDIO_KEY`
* `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_KEY`

## Development Roadmap

1. **Setup and Configuration**

   * Initialize repository and project structure.
   * Configure Azure OpenAI and Cognitive Services.

2. **Core Functionality Implementation**

   * Develop audio ingestion and speech-to-text transcription.
   * Implement caller attribute and background noise analysis.
   * Integrate GPT-based incident classification.

3. **Resource Management Integration**

   * Populate and query geolocation-based emergency resource datasets.
   * Develop dynamic resource assignment logic.

4. **Incident Dashboard Development**

   * Create interactive dashboard interface.
   * Integrate real-time data updates and manual editing capabilities.

5. **Testing and Validation**

   * Conduct thorough testing of individual components.
   * Validate end-to-end functionality and accuracy of classifications.

## Next Steps

* Gather stakeholder feedback and iterate based on insights.
* Expand capabilities towards production-grade application.
* Explore additional integration opportunities with emergency response systems.

## Deployment

### Local Development

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the API locally:
   ```bash
   uvicorn main:app --reload
   ```

### Docker

1. Build the container:
   ```bash
   docker build -t emergency-response .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 emergency-response
   ```

### Azure App Service

1. Build and push the Docker image to a container registry (e.g., Azure Container Registry).
2. Create an Azure App Service Web App configured for Docker.
3. Provide environment variables and secrets as App Settings in Azure.
4. Deploy the container image to the Web App.

The application exposes a single `/incident` endpoint accepting an audio file upload.

Environment variables such as API keys for Azure services should be provided as standard environment variables (e.g., `AZURE_OPENAI_KEY`, `AZURE_SPEECH_KEY`). When running in Docker or Azure App Service, set these variables through the hosting environment's configuration options.

## Running the Resource Assignment Demo

The repository includes simple scripts to seed a SQLite database with sample emergency resources and assign them to incidents based on location and type.

```bash
# Install any required dependencies (only the Python standard library is used)
python demo.py
```

Running `demo.py` will create `emergency.db` in the repository folder, seed it with example fire stations, hospitals, and police stations, and process a sample incident. The script outputs the assigned resource identifier and the estimated arrival time in minutes.

## Running the PoC server

Install requirements and start the FastAPI server using Uvicorn:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### New API Endpoints

* `POST /upload-audio` - Accepts an audio file along with `latitude` and `longitude` form fields. The file is temporarily stored on the server for further processing.
* `WebSocket /ws/audio` - Accepts streaming audio bytes. Each received chunk is stored in a temporary directory on the server.

Geolocation values are currently simulated by the client and included as request data.

