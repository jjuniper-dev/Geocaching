# Snuggly Anchor
**AI-assisted spatial exploration platform for Chelsea QC and Gatineau Park**

An interactive web app combining Leaflet mapping, route generation, and local LLM recommendations to explore outdoor locations with contextual environmental and cultural intelligence.

---

## Quick Start

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.11+ (for backend)
- **Ollama** running locally with Qwen2.5-7B model
- **OSRM** public API access (automatic, no setup)

### 1. Prepare Ollama (Local LLM)

In a separate terminal, start Ollama and pull Qwen2.5:

```bash
# Install Ollama from https://ollama.ai
ollama serve

# In another terminal, pull the model
ollama pull qwen2.5:7b
```

### 2. Start the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open Browser

Navigate to: **http://localhost:5173**

---

## Features

### ✓ Phase 2: Interactive Map
- Full-screen Leaflet map with 20 curated POIs
- Colour-coded markers (scenic, historical, food, trail, wildlife, cultural)
- Click POI → sidebar with description, conservation notes, source attribution
- Layer legend with POI types

### ✓ Phase 3: Route Generation
- Route generation mode with OSRM + Qwen narrative
- Start/end coordinate inputs
- AI-generated contextual descriptions for routes
- Polyline visualization on map
- Nearby POI enrichment

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 18 + Vite + TypeScript + Leaflet |
| Backend | FastAPI + Uvicorn |
| Mapping | Leaflet + OpenStreetMap |
| Routing | OSRM public API |
| AI/LLM | Qwen2.5-7B via Ollama (local) |
| Database | Hardcoded POIs (Phase 3) → PostgreSQL+PostGIS (Phase 4) |

---

## Project Structure

```
/
├── frontend/           # React app
│   ├── src/
│   │   ├── components/ # Map, POIPanel, RoutePanel
│   │   ├── data/       # 20 curated POIs
│   │   ├── types/      # TypeScript geospatial types
│   │   └── App.tsx     # Main app
│   └── package.json
│
├── backend/            # FastAPI server
│   ├── app/
│   │   ├── main.py     # FastAPI app
│   │   ├── data.py     # POI storage
│   │   ├── routes/     # API endpoints
│   │   └── services/   # OSRM, Qwen clients
│   └── requirements.txt
│
└── docker-compose.yml  # PostgreSQL + PostGIS (for later)
```

---

## API Endpoints

### POST /api/routes/generate
Generate a route with AI narrative.

**Request:**
```json
{
  "start": [45.497, -75.855],
  "end": [45.489, -75.922]
}
```

**Response:**
```json
{
  "coordinates": [[lat, lng], ...],
  "distance": 12500,
  "duration": 450,
  "narrative": "This scenic route..."
}
```

---

## Troubleshooting

**Cannot connect to Ollama:**
- Ensure `ollama serve` is running in a separate terminal
- Check: `curl http://localhost:11434/api/tags`

**Frontend won't connect to backend:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS in `backend/app/main.py`

**OSRM returns no route:**
- Coordinates must be in Chelsea/Gatineau area
- Try with default coordinates in the form

---

## Next Steps

- Phase 4: PostgreSQL + PostGIS database
- Phase 4.5: Conservation-aware routing with Valhalla
- Phase 5: Advanced GeoAI features (embeddings, seasonal context)
- Phase 6: User authentication and saved routes

---

**Happy exploring! 🗺️**