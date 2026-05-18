"""POI and Trail data using authoritative Gatineau Park trail data."""
from dataclasses import dataclass
from typing import Optional, Literal
import csv
import os

@dataclass
class TrailCapabilities:
    dogFriendly: bool
    eBikeFriendly: bool
    difficulty: Literal["easy", "moderate", "hard"]
    lengthKm: Optional[float] = None

@dataclass
class POI:
    id: str
    name: str
    poi_type: str
    lat: float
    lng: float
    description: str
    conservation: str = ""
    season: str = ""
    source: str = ""
    trail_capabilities: Optional[TrailCapabilities] = None
    conservation_sensitivity: Optional[Literal["low", "medium", "high"]] = None
    parking_lot: str = ""
    sector: str = ""

# Sector coordinate mapping (approximate centers)
SECTOR_COORDS = {
    "Champlain Parkway": (45.4890, -75.8650),
    "King Mountain": (45.4695, -75.8099),
    "Asticou": (45.4500, -75.7600),
    "Pink Lake": (45.4564, -75.7925),
    "Western Sector": (45.5200, -75.9000),
    "Carbide Willson": (45.4582, -75.7965),
    "Camp Fortune": (45.5009, -75.8489),
    "Meech Lake": (45.4989, -75.8699),
    "Philippe Lake": (45.5456, -75.9301),
    "La Pêche": (45.5724, -75.9527),
    "Old Chelsea": (45.5174, -75.7878),
    "Luskville": (45.5850, -75.8200),
}

def assess_difficulty(typical_use: str, notes: str) -> Literal["easy", "moderate", "hard"]:
    """Assess trail difficulty from metadata."""
    notes_lower = notes.lower()
    if any(x in notes_lower for x in ["steep", "climbing", "technical", "waterfall ascent", "escarpment", "ridge"]):
        return "hard"
    if any(x in notes_lower for x in ["accessible", "family", "interpretive loop", "short connector"]):
        return "easy"
    if "family" in typical_use.lower():
        return "easy"
    return "moderate"

def assess_dog_friendly(typical_use: str, notes: str) -> bool:
    """Assess if trail is dog-friendly."""
    if "multi-use" in typical_use.lower():
        return True
    if "family" in typical_use.lower():
        return True
    return False

def assess_ebike_friendly(typical_use: str, notes: str) -> bool:
    """Assess if trail is e-bike friendly."""
    if "multi-use" in typical_use.lower():
        if not any(x in notes.lower() for x in ["technical", "climbing", "steep", "ridge"]):
            return True
    return False

def assess_conservation_sensitivity(sector: str, notes: str) -> Literal["low", "medium", "high"]:
    """Assess conservation sensitivity based on sector and characteristics."""
    notes_lower = notes.lower()
    sector_lower = sector.lower()
    if any(x in sector_lower for x in ["la pêche", "western sector"]):
        return "high"
    if any(x in notes_lower for x in ["remote", "backcountry", "interior"]) and "connector" not in notes_lower:
        return "medium"
    if "carbide" in sector_lower or "fortune" in sector_lower:
        if "connector" not in notes_lower:
            return "medium"
    return "low"

def estimate_length(typical_use: str, notes: str, difficulty: str) -> float:
    """Estimate trail length in km."""
    if "short" in notes.lower():
        return 2.0
    if "connector" in notes.lower():
        return 1.5
    if difficulty == "hard":
        return 8.0
    if difficulty == "moderate":
        return 5.0
    return 3.0

def load_pois_from_csv() -> list:
    """Load POIs from official Gatineau Park trail data."""
    pois = []
    csv_path = os.path.join(os.path.dirname(__file__), "trails.csv")

    if not os.path.exists(csv_path):
        # Fallback: return legacy POIs if CSV not found
        return _get_legacy_pois()

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trail_id = row['Trail_ID'].strip()
            trail_name = row['Trail_Name'].strip()
            sector = row['Sector'].strip()
            typical_use = row['Typical_Use'].strip()
            notes = row['Notes'].strip()
            parking = row['Closest_Parking_Lot'].strip()

            # Get coordinates from sector or use parking lot info
            if sector in SECTOR_COORDS:
                lat, lng = SECTOR_COORDS[sector]
            else:
                # Default to center of park
                lat, lng = 45.49, -75.85

            # Assess trail characteristics
            difficulty = assess_difficulty(typical_use, notes)
            dog_friendly = assess_dog_friendly(typical_use, notes)
            ebike_friendly = assess_ebike_friendly(typical_use, notes)
            conservation_sensitivity = assess_conservation_sensitivity(sector, notes)
            length_km = estimate_length(typical_use, notes, difficulty)

            # Create POI
            poi = POI(
                id=trail_id.lower().replace(' ', '_'),
                name=trail_name,
                poi_type="trail",
                lat=lat,
                lng=lng,
                description=f"{trail_name} in {sector}. {notes}",
                source="NCC Gatineau Park Official Trail Network",
                trail_capabilities=TrailCapabilities(
                    dogFriendly=dog_friendly,
                    eBikeFriendly=ebike_friendly,
                    difficulty=difficulty,
                    lengthKm=length_km,
                ),
                conservation_sensitivity=conservation_sensitivity,
                parking_lot=parking,
                sector=sector,
            )
            pois.append(poi)

    return pois

def _get_legacy_pois() -> list:
    """Return legacy POI data for backwards compatibility."""
    return [
        POI(
            id="pink-lake",
            name="Pink Lake",
            poi_type="wildlife",
            lat=45.4564, lng=-75.7925,
            description="A meromictic lake — its layers never mix, preserving ancient sediment records.",
            source="Parks Canada",
            conservation_sensitivity="high"
        ),
    ]

# Load POIs from CSV on module import
POIS = load_pois_from_csv()

def get_pois_near_coordinate(lat: float, lng: float, radius_km: float = 3) -> list:
    """Find POIs within radius_km of a coordinate."""
    nearby = []
    for poi in POIS:
        dlat = (poi.lat - lat) * 111
        dlng = (poi.lng - lng) * 111 * (1 - 0.0066 * ((poi.lat + lat) / 2))
        distance = (dlat**2 + dlng**2) ** 0.5
        if distance <= radius_km:
            nearby.append(poi)
    return sorted(nearby, key=lambda p: ((p.lat - lat)**2 + (p.lng - lng)**2) ** 0.5)
