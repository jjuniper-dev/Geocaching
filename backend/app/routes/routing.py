from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
from app.services.routing_service import OSRMClient
from app.services.ai_service import QwenClient
from app.data import get_pois_near_coordinate

router = APIRouter(prefix="/api/routes", tags=["routing"])

osrm = OSRMClient()
qwen = QwenClient()


class RouteFilters(BaseModel):
    dogFriendly: bool = False
    eBikeFriendly: bool = False
    maxDifficulty: Literal["easy", "moderate", "hard"] = "hard"
    avoidSensitiveAreas: bool = True


class RouteRequest(BaseModel):
    start: tuple[float, float]  # (lat, lng)
    end: tuple[float, float]  # (lat, lng)
    route_type: str = "scenic"
    filters: Optional[RouteFilters] = None


class RouteResponse(BaseModel):
    coordinates: list[list[float]]
    distance: float
    duration: float
    narrative: Optional[str] = None
    conservationImpact: Optional[str] = None


def _filter_pois_by_trail_capabilities(pois: list, filters: Optional[RouteFilters]) -> list:
    """Filter POIs based on trail capability preferences."""
    if not filters:
        return pois

    filtered = pois

    if filters.dogFriendly:
        filtered = [
            p for p in filtered
            if p.trail_capabilities and p.trail_capabilities.get("dogFriendly", False)
        ]

    if filters.eBikeFriendly:
        filtered = [
            p for p in filtered
            if p.trail_capabilities and p.trail_capabilities.get("eBikeFriendly", False)
        ]

    difficulty_order = {"easy": 0, "moderate": 1, "hard": 2}
    max_difficulty_level = difficulty_order.get(filters.maxDifficulty, 2)
    filtered = [
        p for p in filtered
        if not p.trail_capabilities
        or difficulty_order.get(p.trail_capabilities.get("difficulty"), 2) <= max_difficulty_level
    ]

    return filtered


def _calculate_conservation_impact(pois: list, filters: Optional[RouteFilters]) -> str:
    """Calculate conservation impact of the route."""
    if not filters or not filters.avoidSensitiveAreas:
        return "Conservation awareness: Off"

    sensitivity_levels = {
        p.conservation_sensitivity
        for p in pois
        if hasattr(p, "conservation_sensitivity") and p.conservation_sensitivity
    }

    if "high" in sensitivity_levels:
        return "🌿 High conservation sensitivity. Route passes through sensitive areas. Please stay on marked trails and minimize noise."
    elif "medium" in sensitivity_levels:
        return "🌿 Moderate conservation sensitivity. Some areas have habitat concerns. Follow local guidance."
    else:
        return "🟢 Low conservation impact. This route is conservation-friendly."


@router.post("/generate")
async def generate_route(req: RouteRequest) -> RouteResponse:
    """
    Generate a route with AI narrative and conservation awareness.

    Request body:
    {
      "start": [lat, lng],
      "end": [lat, lng],
      "route_type": "scenic" (optional),
      "filters": {
        "dogFriendly": false,
        "eBikeFriendly": false,
        "maxDifficulty": "hard",
        "avoidSensitiveAreas": true
      }
    }

    Returns:
    {
      "coordinates": [[lat, lng], ...],
      "distance": meters,
      "duration": seconds,
      "narrative": "AI-generated description",
      "conservationImpact": "Conservation summary"
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

    # Filter POIs by trail capabilities
    filtered_pois = _filter_pois_by_trail_capabilities(nearby_pois, req.filters)
    if not filtered_pois:
        filtered_pois = nearby_pois

    # Calculate conservation impact
    conservation_impact = _calculate_conservation_impact(nearby_pois, req.filters)

    narrative = None
    if filtered_pois:
        pois_for_narrative = [
            {
                "name": p.name,
                "type": p.poi_type,
                "description": p.description,
            }
            for p in filtered_pois
        ]

        narrative = qwen.generate_route_narrative(
            start_name=start_name,
            end_name=end_name,
            distance_km=distance_km,
            duration_minutes=duration_minutes,
            nearby_pois=pois_for_narrative,
            conservation_notes=conservation_impact,
        )

    return RouteResponse(
        coordinates=route["coordinates"],
        distance=route["distance"],
        duration=route["duration"],
        narrative=narrative,
        conservationImpact=conservation_impact,
    )
