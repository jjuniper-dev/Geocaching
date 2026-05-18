from typing import Optional
import json


class QwenClient:
    def __init__(
        self,
        model: str = "qwen2.5:7b",
        use_ollama: bool = True,
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.use_ollama = use_ollama
        self.base_url = base_url
        if use_ollama:
            try:
                import ollama
                self.client = ollama.Client(host=base_url)
            except ImportError:
                print("Ollama not available, falling back to stub mode")
                self.use_ollama = False

    def enrich_route(
        self,
        route_geojson: dict,
        nearby_pois: list[dict],
        conservation_impact: Optional[dict] = None,
    ) -> dict:
        """
        Enrich a route with AI-generated narrative, POI context, and environmental education.

        Args:
            route_geojson: GeoJSON route object with coordinates
            nearby_pois: List of POI dicts with id, name, type, description, conservation_sensitivity, sector, trail_capabilities
            conservation_impact: Dict with impact_score, sensitivity_counts

        Returns:
            Dict with narrative, highlights, environmental_education, stewardship_tips
        """

        # Extract route info
        route_coords = route_geojson.get("coordinates", [])
        distance_km = route_geojson.get("properties", {}).get("distance_km", 0)
        duration_minutes = route_geojson.get("properties", {}).get("duration_minutes", 60)

        # Prepare POI context with validation (anti-hallucination)
        valid_pois = [
            {
                "id": poi.get("id"),
                "name": poi.get("name"),
                "type": poi.get("poi_type"),
                "description": poi.get("description"),
                "conservation_sensitivity": poi.get("conservation_sensitivity"),
                "sector": poi.get("sector"),
                "trail_capabilities": poi.get("trail_capabilities"),
            }
            for poi in nearby_pois
        ]

        # Build system prompt with geospatial grounding
        system_prompt = """You are an expert environmental guide and GIS analyst for the Chelsea QC and Gatineau Park region.
Your role is to provide contextually accurate, educational information about outdoor routes and landmarks.

CRITICAL CONSTRAINT: You MUST ONLY reference POIs and data provided in the context below.
Do NOT invent locations, facts, or recommendations not explicitly provided.
Do NOT hallucinate geographical features or trail characteristics.

Your response must be valid JSON with these fields:
{
  "narrative": "2-3 sentence overview of the route's character and significance",
  "highlights": [
    {
      "poi_id": "exact POI id from provided list",
      "name": "POI name",
      "context": "Why this stop matters (cultural, scenic, ecological)",
      "ecology": "Ecosystem/habitat type if relevant",
      "conservation": "Conservation status or stewardship note if applicable"
    }
  ],
  "environmental_education": [
    "Fact about geology, ecology, hydrology, or ecosystems encountered"
  ],
  "stewardship_tips": [
    "Low-impact practice or seasonal consideration for this route"
  ]
}"""

        user_prompt = f"""Enrich this outdoor route with environmental context:

ROUTE DETAILS:
- Distance: {distance_km:.1f} km
- Duration: {duration_minutes} minutes
- Sector: {self._extract_sector(valid_pois)}

AUTHORIZED POIs (only reference these):
{json.dumps(valid_pois[:8], indent=2)}

CONSERVATION IMPACT:
{json.dumps(conservation_impact or {}, indent=2)}

Generate JSON response with:
1. Narrative: Why is this route ecologically or culturally significant?
2. Highlights: 2-3 stops with cultural/ecological/scenic significance
   - Use ONLY poi_id values from the provided list
   - Explain why each stop matters
3. Environmental Education: Geological/ecological/hydrological facts about the area
4. Stewardship: Low-impact practices and seasonal considerations

Ensure all POI references match provided data exactly."""

        if self.use_ollama:
            return self._generate_with_ollama(system_prompt, user_prompt)
        else:
            return self._generate_stub(valid_pois, conservation_impact)

    def _generate_with_ollama(self, system_prompt: str, user_prompt: str) -> dict:
        """Generate enrichment using local Ollama."""
        try:
            response = self.client.generate(
                model=self.model,
                prompt=user_prompt,
                system=system_prompt,
                stream=False,
            )

            response_text = response.response.strip()
            # Extract JSON from response
            try:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                pass

            # Fallback: return structured response
            return {
                "narrative": response_text[:300],
                "highlights": [],
                "environmental_education": [],
                "stewardship_tips": []
            }
        except Exception as e:
            print(f"Error generating with Ollama: {e}")
            return self._generate_stub([], {})

    def _generate_stub(self, pois: list[dict], conservation_impact: Optional[dict]) -> dict:
        """Fallback stub response when Ollama unavailable."""
        highlights = []
        for poi in pois[:3]:
            highlights.append({
                "poi_id": poi.get("id"),
                "name": poi.get("name"),
                "context": f"{poi.get('type')} - {poi.get('description', '')[:100]}",
                "ecology": "See POI description for details",
                "conservation": poi.get("conservation_sensitivity", "Unknown")
            })

        return {
            "narrative": f"This route through Gatineau Park offers diverse natural experiences across {len(pois)} distinct points of interest.",
            "highlights": highlights,
            "environmental_education": [
                "Gatineau Park features a mix of deciduous and coniferous forests",
                "The region sits on the Canadian Shield with exposed bedrock and glaciated terrain",
                "Wetlands provide critical habitat for migratory birds and amphibians"
            ],
            "stewardship_tips": [
                "Stay on marked trails to protect vegetation and prevent erosion",
                "Avoid nesting areas during spring/early summer (April-June)",
                "Pack out all waste; this is a sensitive ecological zone"
            ]
        }

    def _extract_sector(self, pois: list[dict]) -> str:
        """Extract primary sector from POI list."""
        if pois and pois[0].get("sector"):
            return pois[0]["sector"]
        return "Gatineau Park"
