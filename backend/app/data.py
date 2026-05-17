from dataclasses import dataclass

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

POIS = [
    POI(
        id="pink-lake",
        name="Pink Lake",
        poi_type="wildlife",
        lat=45.4564, lng=-75.7925,
        description="A meromictic lake — its layers never mix, preserving ancient sediment records dating back 11,000 years.",
        conservation="Fencing protects the shoreline. Stay on the boardwalk.",
        source="Parks Canada"
    ),
    POI(
        id="champlain-lookout",
        name="Champlain Lookout",
        poi_type="scenic",
        lat=45.4887, lng=-75.9221,
        description="The most panoramic viewpoint in Gatineau Park. On clear days you can see the Ottawa River valley.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="lusk-cave",
        name="Lusk Cave",
        poi_type="trail",
        lat=45.5372, lng=-75.9116,
        description="A 100-metre marble cave accessible via an 11 km round-trip trail. Wading through an underground stream.",
        conservation="Do not disturb hibernating bats (November–April).",
        season="Best: May–October. Trail closed during winter.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="mackenzie-king-estate",
        name="Mackenzie King Estate",
        poi_type="historical",
        lat=45.4741, lng=-75.8512,
        description="Canada's longest-serving PM's retreat from 1903 until his death in 1950.",
        season="Open May–October.",
        source="NCC"
    ),
    POI(
        id="carbide-willson-ruins",
        name="Carbide Willson Ruins",
        poi_type="historical",
        lat=45.4582, lng=-75.7965,
        description="Stone ruins of a 1900s calcium carbide laboratory on Meech Creek.",
        conservation="Ruins are structurally fragile. Do not climb on the walls.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="meech-lake",
        name="Meech Lake",
        poi_type="scenic",
        lat=45.4989, lng=-75.8699,
        description="A pristine lake with a public beach, canoe rentals, and calm water ideal for swimming.",
        season="Swimming season: June–August.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="skyline-trail",
        name="Skyline Trail",
        poi_type="trail",
        lat=45.4962, lng=-75.8920,
        description="A moderately challenging ridge trail offering continuous views westward across the Gatineau Hills.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="king-mountain",
        name="King Mountain Viewpoint",
        poi_type="scenic",
        lat=45.4695, lng=-75.8099,
        description="A rocky summit accessible via a short but steep trail, offering close-up views of the Ottawa Valley farmland.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="etienne-brule-lookout",
        name="Étienne Brûlé Lookout",
        poi_type="scenic",
        lat=45.4879, lng=-75.8944,
        description="A sweeping view over the Ottawa River and Outaouais region. One of the quieter viewpoints.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="camp-fortune",
        name="Camp Fortune",
        poi_type="trail",
        lat=45.5009, lng=-75.8489,
        description="A four-season outdoor recreation area. In winter a ski hill, in summer a hub for mountain biking.",
        source="Chelsea, QC"
    ),
    POI(
        id="chelsea-pub",
        name="The Chelsea Pub",
        poi_type="food",
        lat=45.5172, lng=-75.7884,
        description="A beloved village institution. Solid pub food, local craft beers, and a lively patio.",
        source="Old Chelsea, QC"
    ),
    POI(
        id="la-cigale",
        name="La Cigale",
        poi_type="food",
        lat=45.5175, lng=-75.7875,
        description="Chelsea's neighbourhood restaurant with seasonal menus and strong local ingredients.",
        source="Old Chelsea, QC"
    ),
    POI(
        id="wakefield-village",
        name="Wakefield Village",
        poi_type="cultural",
        lat=45.6351, lng=-75.8335,
        description="A small arts village straddling the Gatineau River, known for its covered bridge and Black Sheep Inn.",
        source="Wakefield, QC"
    ),
    POI(
        id="black-sheep-inn",
        name="Black Sheep Inn",
        poi_type="cultural",
        lat=45.6353, lng=-75.8329,
        description="A legendary live-music venue that has hosted Canadian and international artists for over 30 years.",
        source="Wakefield, QC"
    ),
    POI(
        id="lac-la-peche",
        name="Lac La Pêche",
        poi_type="wildlife",
        lat=45.5724, lng=-75.9527,
        description="A remote wilderness lake in the western backcountry. Canoe camping is permitted here.",
        conservation="Carry-in, carry-out rules apply. No motorized watercraft.",
        season="Access May–October only.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="herridge-shelter",
        name="Herridge Shelter",
        poi_type="trail",
        lat=45.5181, lng=-75.8943,
        description="A backcountry lean-to accessible via multiple trail routes. A useful navigation landmark.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="gatineau-visitor-centre",
        name="Gatineau Park Visitor Centre",
        poi_type="scenic",
        lat=45.4625, lng=-75.7810,
        description="The main entry point for park information, trail maps, and seasonal programming.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="sugarbush-trail",
        name="Sugarbush Heritage Trail",
        poi_type="cultural",
        lat=45.4897, lng=-75.8601,
        description="A 6 km interpretive trail through old maple groves used for syrup production.",
        season="Sugarbush season: late February–April.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="philippe-lake",
        name="Philippe Lake Campground",
        poi_type="scenic",
        lat=45.5456, lng=-75.9301,
        description="A well-maintained NCC campground on a large lake in the western park with canoe rentals.",
        season="Camping season: May–October.",
        source="NCC Gatineau Park"
    ),
    POI(
        id="old-chelsea-cemetery",
        name="Old Chelsea Cemetery",
        poi_type="historical",
        lat=45.5174, lng=-75.7878,
        description="A historic rural cemetery with graves dating to the early 1800s.",
        source="Chelsea, QC Heritage Registry"
    ),
]

def get_pois_near_coordinate(lat: float, lng: float, radius_km: float = 3) -> list[POI]:
    """Find POIs within radius_km of a coordinate."""
    nearby = []
    for poi in POIS:
        # Simple distance approximation (good enough for ~3km)
        dlat = (poi.lat - lat) * 111  # ~111 km per degree latitude
        dlng = (poi.lng - lng) * 111 * (1 - 0.0066 * ((poi.lat + lat) / 2))
        distance = (dlat**2 + dlng**2) ** 0.5
        if distance <= radius_km:
            nearby.append(poi)
    return sorted(nearby, key=lambda p: ((p.lat - lat)**2 + (p.lng - lng)**2) ** 0.5)
