from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.routing_service import OSRMClient
from app.services.ai_service import QwenClient
from app.data import get_pois_near_coordinate

router = APIRouter(prefix="/api/routes", tags=["routing"])

osrm = OSRMClient()
qwen = QwenClient()


class RouteRequest(BaseModel):
    start: tuple[float, float]  # (lat, lng)
    end: tuple[float, float]  # (lat, lng)
    route_type: str = "scenic"


class RouteResponse(BaseModel):
    coordinates: list[list[float]]
    distance: float
    duration: float
    narrative: Optional[str] = None


@router.post("/generate")
async def generate_route(req: RouteRequest) -> RouteResponse:
    """
    Generate a route with AI narrative.

    Request body:
    {
      "start": [lat, lng],
      "end": [lat, lng],
      "route_type": "scenic" (optional)
    }

    Returns:
    {
      "coordinates": [[lat, lng], ...],
      "distance": meters,
      "duration": seconds,
      "narrative": "AI-generated description"
    }
    """
    if not req.start or not req.end:
        raise HTTPException(status_code=400, detail="Missing start or end coordinates")

    route = await osrm.get_route(req.start, req.end)
    if not route:
        raise HTTPException(status_code=400, detail="Could not generate route")

    distance_km = route["distance"] / 1000
    duration_minutes = int(route["duration"] / 60)

    start_name = f"Location ({req.start[0]:.3f}, {req.start[1]:.3f})"
    end_name = f"Location ({req.end[0]:.3f}, {req.end[1]:.3f})"

    nearby_pois_start = get_pois_near_coordinate(req.start[0], req.start[1], radius_km=5)
    nearby_pois_end = get_pois_near_coordinate(req.end[0], req.end[1], radius_km=5)

    nearby_pois = list(
        {p.id: p for p in nearby_pois_start + nearby_pois_end}.values()
    )[:8]

    narrative = None
    if nearby_pois:
        pois_for_narrative = [
            {
                "name": p.name,
                "type": p.poi_type,
                "description": p.description,
            }
            for p in nearby_pois
        ]

        narrative = qwen.generate_route_narrative(
            start_name=start_name,
            end_name=end_name,
            distance_km=distance_km,
            duration_minutes=duration_minutes,
            nearby_pois=pois_for_narrative,
            conservation_notes=(
                "This route passes through Gatineau Park. "
                "Stay on marked trails and respect seasonal closures."
            ),
        )

    return RouteResponse(
        coordinates=route["coordinates"],
        distance=route["distance"],
        duration=route["duration"],
        narrative=narrative,
    )
