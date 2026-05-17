import httpx
from typing import Optional


class OSRMClient:
    def __init__(self, base_url: str = "http://router.project-osrm.org/route/v1/driving"):
        self.base_url = base_url

    async def get_route(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        alternatives: bool = False
    ) -> Optional[dict]:
        """
        Get a route from OSRM public API.

        Args:
            start: (lat, lng) tuple
            end: (lat, lng) tuple
            alternatives: Return alternative routes

        Returns:
            {
                "coordinates": [[lat, lng], ...],
                "distance": meters,
                "duration": seconds
            }
        """
        start_lng, start_lat = start[1], start[0]
        end_lng, end_lat = end[1], end[0]

        url = f"{self.base_url}/{start_lng},{start_lat};{end_lng},{end_lat}"
        params = {
            "alternatives": "true" if alternatives else "false",
            "geometries": "geojson",
            "overview": "full",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                if data.get("code") != "Ok" or not data.get("routes"):
                    return None

                route = data["routes"][0]
                coords = route["geometry"]["coordinates"]

                return {
                    "coordinates": [[lat, lng] for lng, lat in coords],
                    "distance": route["distance"],
                    "duration": route["duration"],
                }
        except Exception:
            return None
