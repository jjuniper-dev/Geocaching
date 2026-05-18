"""Load and parse official Gatineau Park trail data with enhanced metadata."""
import csv
from typing import Optional, Literal

def assess_difficulty(typical_use: str, notes: str, trail_name: str) -> Literal["easy", "moderate", "hard"]:
    """Assess trail difficulty from metadata."""
    notes_lower = notes.lower()

    # Hard trails
    if any(x in notes_lower for x in ["steep", "climbing", "technical", "waterfall ascent", "escarpment", "ridge"]):
        return "hard"
    if any(x in typical_use.lower() for x in []):  # No Multi-use means likely harder
        if "family" not in typical_use.lower() and "connector" not in notes_lower and "short" not in notes_lower:
            return "hard"

    # Easy trails
    if any(x in notes_lower for x in ["accessible", "family", "interpretive loop", "connector"]):
        if "short" in notes_lower or "family" in typical_use.lower():
            return "easy"
    if "family" in typical_use.lower():
        return "easy"

    # Default to moderate
    return "moderate"

def assess_dog_friendly(typical_use: str, notes: str, sector: str) -> bool:
    """Assess if trail is dog-friendly."""
    # Most multi-use trails are dog-friendly
    if "multi-use" in typical_use.lower():
        return True
    # Family trails might be dog-friendly
    if "family" in typical_use.lower():
        return True
    return False

def assess_ebike_friendly(typical_use: str, notes: str) -> bool:
    """Assess if trail is e-bike friendly."""
    # Only multi-use non-technical trails
    if "multi-use" in typical_use.lower():
        if not any(x in notes.lower() for x in ["technical", "climbing", "steep", "ridge"]):
            return True
    return False

def assess_conservation_sensitivity(sector: str, notes: str) -> Literal["low", "medium", "high"]:
    """Assess conservation sensitivity based on sector and characteristics."""
    notes_lower = notes.lower()
    sector_lower = sector.lower()

    # High sensitivity: remote areas, fragile zones
    if any(x in sector_lower for x in ["la pêche", "western sector"]):
        return "high"
    if any(x in notes_lower for x in ["remote", "backcountry", "interior"]):
        return "medium"  # Remote but not highest

    # Medium sensitivity: some interior areas
    if "carbide" in sector_lower or "fortune" in sector_lower:
        if "connector" not in notes_lower:
            return "medium"

    # Low sensitivity: accessible areas, connectors
    return "low"

def load_trails_from_csv(csv_path: str) -> dict:
    """Load trail data from CSV and return formatted POI dictionary."""
    trails = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trail_id = row['Trail_ID'].strip()
            trail_name = row['Trail_Name'].strip()
            sector = row['Sector'].strip()
            typical_use = row['Typical_Use'].strip()
            notes = row['Notes'].strip()
            parking = row['Closest_Parking_Lot'].strip()

            # Assess trail characteristics
            difficulty = assess_difficulty(typical_use, notes, trail_name)
            dog_friendly = assess_dog_friendly(typical_use, notes, sector)
            ebike_friendly = assess_ebike_friendly(typical_use, notes)
            conservation_sensitivity = assess_conservation_sensitivity(sector, notes)

            # Estimate length based on difficulty and notes
            if "short" in notes.lower():
                length_km = 2.0
            elif difficulty == "hard":
                length_km = 8.0
            elif "connector" in notes.lower():
                length_km = 1.5
            else:
                length_km = 5.0 if difficulty == "moderate" else 3.0

            trails[trail_id] = {
                'id': trail_id.lower().replace(' ', '_'),
                'name': trail_name,
                'sector': sector,
                'parking': parking,
                'typical_use': typical_use,
                'notes': notes,
                'difficulty': difficulty,
                'dogFriendly': dog_friendly,
                'eBikeFriendly': ebike_friendly,
                'lengthKm': length_km,
                'conservationSensitivity': conservation_sensitivity,
            }

    return trails

if __name__ == '__main__':
    trails = load_trails_from_csv('trails.csv')
    print(f"Loaded {len(trails)} trails")
    for trail_id, trail in list(trails.items())[:3]:
        print(f"\n{trail['name']}:")
        print(f"  Difficulty: {trail['difficulty']}")
        print(f"  Dog-friendly: {trail['dogFriendly']}")
        print(f"  E-bike: {trail['eBikeFriendly']}")
        print(f"  Conservation: {trail['conservationSensitivity']}")
