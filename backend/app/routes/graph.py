import strawberry
from typing import List, Optional
from app.data import POIS
from app.graph_schema import POI, Relationship, Coordinates, TrailCapabilities, calculate_relationships

@strawberry.type
class Query:
    @strawberry.field
    def pois(self) -> List[POI]:
        """Get all POIs."""
        return [
            POI(
                id=poi.id,
                name=poi.name,
                poi_type=poi.poi_type,
                coordinates=Coordinates(lat=poi.lat, lng=poi.lng),
                description=poi.description,
                conservation=poi.conservation,
                season=poi.season,
                source=poi.source,
                trailCapabilities=TrailCapabilities(
                    dogFriendly=poi.trail_capabilities.dogFriendly,
                    eBikeFriendly=poi.trail_capabilities.eBikeFriendly,
                    difficulty=poi.trail_capabilities.difficulty,
                    lengthKm=poi.trail_capabilities.lengthKm,
                ) if poi.trail_capabilities else None,
                conservationSensitivity=poi.conservation_sensitivity,
            )
            for poi in POIS
        ]

    @strawberry.field
    def poi(self, id: str) -> Optional[POI]:
        """Get a single POI by ID."""
        poi = next((p for p in POIS if p.id == id), None)
        if not poi:
            return None
        return POI(
            id=poi.id,
            name=poi.name,
            poi_type=poi.poi_type,
            coordinates=Coordinates(lat=poi.lat, lng=poi.lng),
            description=poi.description,
            conservation=poi.conservation,
            season=poi.season,
            source=poi.source,
            trailCapabilities=TrailCapabilities(
                dogFriendly=poi.trail_capabilities.dogFriendly,
                eBikeFriendly=poi.trail_capabilities.eBikeFriendly,
                difficulty=poi.trail_capabilities.difficulty,
                lengthKm=poi.trail_capabilities.lengthKm,
            ) if poi.trail_capabilities else None,
            conservationSensitivity=poi.conservation_sensitivity,
        )

    @strawberry.field
    def relationships(self) -> List[Relationship]:
        """Get all POI relationships."""
        return calculate_relationships(POIS)

    @strawberry.field
    def relationships_for(self, poi_id: str) -> List[Relationship]:
        """Get relationships for a specific POI."""
        all_relationships = calculate_relationships(POIS)
        return [r for r in all_relationships if r.source_id == poi_id or r.target_id == poi_id]

    @strawberry.field
    def poi_graph(self) -> "POIGraph":
        """Get complete POI graph (nodes + edges) for visualization."""
        pois = self.pois()
        relationships = self.relationships()
        return POIGraph(nodes=pois, edges=relationships)


@strawberry.type
class POIGraph:
    nodes: List[POI]
    edges: List[Relationship]


schema = strawberry.Schema(query=Query)
