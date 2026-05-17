from typing import Optional
import ollama


class QwenClient:
    def __init__(
        self,
        model: str = "qwen2.5:7b",
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)

    def generate_route_narrative(
        self,
        start_name: str,
        end_name: str,
        distance_km: float,
        duration_minutes: int,
        nearby_pois: list[dict],
        conservation_notes: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a narrative description of a route using Qwen.

        Args:
            start_name: Starting location name
            end_name: Destination name
            distance_km: Route distance in kilometers
            duration_minutes: Estimated duration in minutes
            nearby_pois: List of nearby POIs with name, type, description
            conservation_notes: Optional conservation/environmental info

        Returns:
            Narrative text or None if generation fails
        """

        pois_text = "\n".join(
            f"- {poi['name']} ({poi['type']}): {poi['description'][:150]}"
            for poi in nearby_pois[:5]
        )

        prompt = f"""You are a knowledgeable outdoor guide for the Chelsea QC and Gatineau Park region.
Generate a brief, engaging 2-3 sentence narrative about this route for an explorer.

Route: {start_name} → {end_name}
Distance: {distance_km:.1f} km
Duration: {duration_minutes} minutes

Nearby Points of Interest:
{pois_text}

{f"Conservation note: {conservation_notes}" if conservation_notes else ""}

Write a narrative that:
1. Describes what makes this route special or interesting
2. Mentions 1-2 of the nearby POIs as highlights
3. Includes something about the landscape, ecology, or local character
4. Is concise (under 150 words)

Keep it conversational and inviting."""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
            )
            return response.response.strip()
        except Exception as e:
            print(f"Error generating narrative: {e}")
            return None
