from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.ai_service import QwenClient
from app.data import POIS

router = APIRouter(prefix="/api/ai", tags=["ai"])


class RouteEnrichmentRequest(BaseModel):
    route: dict  # GeoJSON feature
    nearby_poi_ids: List[str]  # POI IDs along/near route
    conservation_impact: Optional[dict] = None


class POIHighlight(BaseModel):
    poi_id: str
    name: str
    context: str
    ecology: Optional[str] = None
    conservation: Optional[str] = None


class RouteEnrichment(BaseModel):
    narrative: str
    highlights: List[POIHighlight]
    environmental_education: List[str]
    stewardship_tips: List[str]


@router.post("/enrich-route", response_model=RouteEnrichment)
async def enrich_route(request: RouteEnrichmentRequest) -> RouteEnrichment:
    """
    Enrich a route with AI-generated narrative, environmental context, and stewardship guidance.

    The AI only references POIs provided in the request (geospatial grounding constraint).
    """

    # Validate POI IDs and retrieve POI data
    nearby_pois = []
    for poi_id in request.nearby_poi_ids:
        poi = next((p for p in POIS if p.id == poi_id), None)
        if not poi:
            raise HTTPException(status_code=400, detail=f"Unknown POI ID: {poi_id}")
        nearby_pois.append({
            "id": poi.id,
            "name": poi.name,
            "poi_type": poi.poi_type,
            "description": poi.description,
            "conservation_sensitivity": poi.conservation_sensitivity,
            "sector": poi.sector,
            "trail_capabilities": {
                "dogFriendly": poi.trail_capabilities.dogFriendly if poi.trail_capabilities else False,
                "eBikeFriendly": poi.trail_capabilities.eBikeFriendly if poi.trail_capabilities else False,
                "difficulty": poi.trail_capabilities.difficulty if poi.trail_capabilities else "moderate",
                "lengthKm": poi.trail_capabilities.lengthKm if poi.trail_capabilities else None,
            } if poi.trail_capabilities else None,
        })

    # Initialize Qwen client
    qwen = QwenClient(use_ollama=True)

    # Generate enrichment
    enrichment = qwen.enrich_route(
        route_geojson=request.route,
        nearby_pois=nearby_pois,
        conservation_impact=request.conservation_impact,
    )

    # Validate response structure
    if not enrichment:
        raise HTTPException(status_code=500, detail="Failed to generate route enrichment")

    # Convert highlights to POIHighlight objects
    highlights = [
        POIHighlight(
            poi_id=h.get("poi_id", ""),
            name=h.get("name", ""),
            context=h.get("context", ""),
            ecology=h.get("ecology"),
            conservation=h.get("conservation")
        )
        for h in enrichment.get("highlights", [])
    ]

    return RouteEnrichment(
        narrative=enrichment.get("narrative", ""),
        highlights=highlights,
        environmental_education=enrichment.get("environmental_education", []),
        stewardship_tips=enrichment.get("stewardship_tips", [])
    )
