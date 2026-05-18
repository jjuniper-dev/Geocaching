import strawberry
from typing import List, Optional
import math

@strawberry.type
class Coordinates:
    lat: float
    lng: float

@strawberry.type
class TrailCapabilities:
    dogFriendly: bool
    eBikeFriendly: bool
    difficulty: str
    lengthKm: Optional[float] = None

@strawberry.type
class POI:
    id: str
    name: str
    poi_type: str
    coordinates: Coordinates
    description: str
    conservation: str = ""
    season: str = ""
    source: str = ""
    trailCapabilities: Optional[TrailCapabilities] = None
    conservationSensitivity: Optional[str] = None

@strawberry.type
class Relationship:
    source_id: str
    target_id: str
    source_name: str
    target_name: str
    relationship_type: str  # "proximity" | "same_type" | "thematic"
    strength: float  # 0-1, where 1 is strongest
    reason: str
    distance_m: int = 0

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance in meters between two coordinates (Haversine)."""
    R = 6371000  # Earth radius in meters
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_relationships(pois: List) -> List[Relationship]:
    """Calculate all relationships between POIs."""
    relationships = []

    for i, poi1 in enumerate(pois):
        for poi2 in pois[i+1:]:
            # Calculate proximity
            dist = calculate_distance(
                poi1.lat, poi1.lng,
                poi2.lat, poi2.lng
            )

            # Proximity relationship (within 5km)
            if dist < 5000:
                strength = max(0, 1 - (dist / 5000))
                relationships.append(Relationship(
                    source_id=poi1.id,
                    target_id=poi2.id,
                    source_name=poi1.name,
                    target_name=poi2.name,
                    relationship_type="proximity",
                    strength=strength,
                    reason=f"{int(dist/1000)}km apart",
                    distance_m=int(dist)
                ))

            # Same type relationship
            if poi1.poi_type == poi2.poi_type:
                thematic_names = {
                    "scenic": "Scenic viewpoint",
                    "trail": "Trail experience",
                    "historical": "Historical site",
                    "food": "Local dining",
                    "wildlife": "Nature habitat",
                    "cultural": "Cultural venue"
                }
                reason = thematic_names.get(poi1.poi_type, "Same category")
                relationships.append(Relationship(
                    source_id=poi1.id,
                    target_id=poi2.id,
                    source_name=poi1.name,
                    target_name=poi2.name,
                    relationship_type="same_type",
                    strength=0.7,
                    reason=reason,
                    distance_m=int(dist)
                ))

            # Thematic clustering (scenic + historical near each other)
            if (poi1.poi_type in ["scenic", "historical"] and
                poi2.poi_type in ["scenic", "historical"] and
                dist < 3000):
                relationships.append(Relationship(
                    source_id=poi1.id,
                    target_id=poi2.id,
                    source_name=poi1.name,
                    target_name=poi2.name,
                    relationship_type="thematic_cluster",
                    strength=0.6,
                    reason="Heritage & scenic cluster",
                    distance_m=int(dist)
                ))

    return relationships
