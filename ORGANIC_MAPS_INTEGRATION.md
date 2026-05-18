# Organic Maps Integration Strategy
## Future Phase: Mobile Companion & Offline Exploration

### Vision
Enable seamless transition from Cartograph web planning to offline navigation in Organic Maps, leveraging open data, privacy-first principles, and low-impact exploration guidance.

---

## Phase Overview: "Cartograph → Organic Maps Bridge"

### Goals
1. **Export routes** from Cartograph as GPX/KML for offline navigation in Organic Maps
2. **Create custom POI layers** from Cartograph's 53 authoritative trails
3. **Sync enrichment data** (stewardship tips, conservation context) to Organic Maps bookmarks
4. **Enable offline-first workflows** for remote exploration
5. **Maintain geospatial grounding** across platforms

### Target Users
- Outdoor enthusiasts planning in Cartograph, navigating offline in Organic Maps
- Hikers without cellular connectivity in Gatineau Park
- Privacy-conscious explorers avoiding commercial map tracking

---

## Data Export Strategy

### 1. Route Exports (KML/GPX)

**From Cartograph to Organic Maps:**

```
POST /api/routes/{route_id}/export?format=gpx|kml
Response:
```xml
<?xml version="1.0"?>
<gpx version="1.1">
  <metadata>
    <name>Scenic Loop: Fortune to Pink Lake</name>
    <desc>Conservation-aware route with stewardship tips</desc>
    <time>2026-05-18T00:18:37Z</time>
  </metadata>
  <trk>
    <name>Route</name>
    <desc>2.5 km • 45 min • Low conservation impact</desc>
    <trkseg>
      <trkpt lat="45.5009" lon="-75.8489">
        <ele>250</ele>
      </trkpt>
      ...
    </trkseg>
  </trk>
  
  <!-- POI Waypoints -->
  <wpt lat="45.4989" lon="-75.8699">
    <name>Pink Lake Trail</name>
    <desc>Popular interpretive loop. Conservation: Low</desc>
    <sym>scenic</sym>
  </wpt>
</gpx>
```

**Features:**
- Track geometry with elevation data from DEM
- Waypoints for highlighted stops with descriptions
- Custom symbols for POI types (scenic, historical, trail, etc.)
- Conservation sensitivity encoded in description
- Stewardship tips in extended data

### 2. Custom POI Layers (OMaps Format)

**Generate Organic Maps custom map (bookmarks collection):**

```json
{
  "type": "FeatureCollection",
  "name": "Cartograph: Gatineau Park Trails",
  "description": "53 official NCC trails with difficulty, dog-friendly, e-bike ratings",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-75.8489, 45.5009]
      },
      "properties": {
        "id": "trail_37",
        "name": "Trail 37",
        "description": "Steeper elevation gain. Multi-use trail.",
        "category": "trail",
        "difficulty": "moderate",
        "dog_friendly": true,
        "ebike_friendly": true,
        "conservation_sensitivity": "medium",
        "parking": "P10 Fortune",
        "sector": "Camp Fortune"
      }
    },
    ...
  ]
}
```

**Organic Maps Import:**
- Users import GeoJSON as custom map bookmark collection
- Symbols color-coded by difficulty/conservation
- Search works across all POI metadata

### 3. Enrichment Data Sync

**Bookmark descriptions with stewardship context:**

```
Pin: Pink Lake Trail
────────────────────
🎯 Route Context
  Difficulty: easy
  Distance: 2.0 km
  Duration: 25 min
  Dog-friendly: ✓

🌿 Conservation
  Sensitivity: low
  Impact: minimal
  
♻️ Stewardship Tips
  • Stay on marked trail to protect vegetation
  • Peak season: June-September
  • Nesting birds present April-June (minimize noise)
  
🔬 Environmental Context
  • Glaciated terrain with exposed bedrock
  • Mixed forest (deciduous-coniferous transition)
  • Critical wetland habitat for migratory birds
```

---

## Implementation Architecture

### Backend Enhancements

**New Route: `routes/export.py`**

```python
@router.get("/routes/{route_id}/export")
async def export_route(
    route_id: str,
    format: Literal["gpx", "kml"] = "gpx",
    include_enrichment: bool = True
):
    """Export route for offline navigation."""
    route = db.query(Route).filter(Route.id == route_id).first()
    nearby_pois = get_pois_near_route(route.geometry)
    
    if format == "gpx":
        return generate_gpx(route, nearby_pois, include_enrichment)
    elif format == "kml":
        return generate_kml(route, nearby_pois, include_enrichment)
```

**New Service: `services/export_service.py`**

```python
def generate_gpx(route, pois, enrichment_data):
    """Convert route + POIs to GPX with enrichment metadata."""
    # Use gpxpy library to create structured GPX
    # Encode trail capabilities, conservation data, stewardship tips
    # Return valid GPX 1.1 document

def generate_geojson_layers(pois, filters=None):
    """Generate Organic Maps-compatible GeoJSON POI layers."""
    # Convert trail data to FeatureCollection
    # Color/icon mapping for difficulty, conservation
    # Searchable properties

def create_bookmark_descriptions(poi, enrichment):
    """Create formatted Organic Maps bookmark text with context."""
    # Include difficulty, dog-friendly, e-bike, conservation
    # Add stewardship tips and environmental education
```

**New Endpoint: `POST /api/pois/export-layers`**

```
Request:
{
  "poi_ids": ["trail_37", "trail_1", "pink-lake"],
  "format": "geojson",
  "include_enrichment": true
}

Response: GeoJSON FeatureCollection with POI metadata
```

### Frontend Integration

**New Route Export UI in RoutePanel:**

```tsx
<div className="route-panel__export">
  <h4>📱 Offline Navigation</h4>
  <p>Download this route for offline use in Organic Maps</p>
  <button onClick={exportToGPX}>
    📥 Export as GPX
  </button>
  <button onClick={exportToKML}>
    📥 Export as KML
  </button>
  <small>Works with Organic Maps (Android/iOS) • No tracking • Fully offline</small>
</div>
```

**Fetch & Download Logic:**

```tsx
const exportToGPX = async () => {
  const response = await fetch(
    `${API_BASE}/api/routes/${routeId}/export?format=gpx`,
    { method: 'GET' }
  );
  const gpx = await response.text();
  downloadFile(gpx, 'route.gpx', 'application/gpx+xml');
};
```

### Data Format Specifications

**GPX 1.1 with Custom Extensions:**

```xml
<gpx version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <metadata>
    <source>Cartograph (github.com/jjuniper-dev/Geocaching)</source>
    <license>CC-BY 4.0 + Open Data</license>
  </metadata>
  
  <!-- Route Track -->
  <trk>
    <extensions>
      <cartograph:route_id>route_12345</cartograph:route_id>
      <cartograph:conservation_impact>low</cartograph:conservation_impact>
      <cartograph:stewardship_tips>
        <tip>Stay on marked trail</tip>
        <tip>Nesting season: April-June</tip>
      </cartograph:stewardship_tips>
    </extensions>
  </trk>
  
  <!-- POI Waypoints -->
  <wpt lat="45.5009" lon="-75.8489">
    <extensions>
      <cartograph:poi_type>trail</cartograph:poi_type>
      <cartograph:difficulty>moderate</cartograph:difficulty>
      <cartograph:dog_friendly>true</cartograph:dog_friendly>
      <cartograph:conservation_sensitivity>medium</cartograph:conservation_sensitivity>
      <cartograph:enrichment>
        <context>Steeper elevation gain with scenic viewpoint</context>
        <ecology>Mixed forest transition zone</ecology>
      </cartograph:enrichment>
    </extensions>
  </wpt>
</gpx>
```

---

## Integration Phases

### Phase A: Route Export (MVP - Week 1)
**Deliverable:** Export any Cartograph route as GPX/KML for Organic Maps navigation

**Steps:**
1. Create `services/export_service.py` with GPX/KML generation
2. Add `GET /api/routes/{route_id}/export` endpoint
3. Add export buttons to RoutePanel UI
4. Test: generate route, export to GPX, open in Organic Maps

**Testing:**
- [ ] Export route as GPX, verify structure
- [ ] Import GPX into Organic Maps (Android/iOS)
- [ ] Navigation follows route correctly
- [ ] Waypoints appear at POI locations
- [ ] Elevation profile displays

### Phase B: POI Layer Export (Week 2)
**Deliverable:** Export curated trail data as Organic Maps custom maps

**Steps:**
1. Create `POST /api/pois/export-layers` endpoint
2. Generate GeoJSON from trail database with metadata
3. Create UI for "Download all 53 trails" as bookmarks
4. Document how to import into Organic Maps

**Testing:**
- [ ] Export all 53 trails as GeoJSON
- [ ] Import into Organic Maps as custom map
- [ ] POIs appear with correct icons/colors
- [ ] Search functionality works
- [ ] Metadata displays in bookmark info

### Phase C: Enrichment Sync (Week 3)
**Deliverable:** Stewardship tips and environmental context in exported routes

**Steps:**
1. Extend GPX export to include enrichment data
2. Format enrichment as readable bookmark descriptions
3. Add conservation icons/colors to waypoint symbols
4. Include environmental education in metadata

**Testing:**
- [ ] Exported route includes stewardship tips
- [ ] Enrichment displays in Organic Maps bookmark details
- [ ] Conservation sensitivity color-coded
- [ ] Geospatial grounding maintained (no hallucinations in export)

### Phase D: Reverse Sync (Future)
**Deliverable:** Import Organic Maps bookmarks/notes back into Cartograph

**Steps:**
1. Parse GPX import from Organic Maps
2. Create user-generated POI collections
3. Merge with authoritative data (flagged as user observations)
4. Contribute validated observations to community dataset

---

## Data Privacy & Licensing

### User Data
- **Export files are created client-side** (stored locally, never uploaded)
- Cartograph tracks exports for analytics only (optional, user-controlled)
- Organic Maps stores files locally on user device

### Licensing
- Cartograph exports inherit CC-BY 4.0 + Open Data licenses
- Include source attribution in all exported files
- Document: "Data from NCC, Parks Canada, NRCan, OSM contributors"

### Offline Guarantee
- Exported routes work 100% offline in Organic Maps
- No callbacks to Cartograph during navigation
- Users own their exported data

---

## Competitive Advantages

| Aspect | Commercial Maps | Organic Maps | Cartograph + Organic Maps |
|--------|-----------------|--------------|--------------------------|
| **Offline maps** | Limited coverage | Full OSM coverage | ✓ Full + authoritative trails |
| **Privacy** | Tracking, analytics | None | ✓ None + no tracking |
| **Conservation context** | None | None | ✓ Stewardship tips |
| **AI enrichment** | Generic | None | ✓ Geospatial-grounded insights |
| **Trail metadata** | Crowdsourced | OSM | ✓ Official NCC data |
| **Environmental education** | None | None | ✓ Ecology/geology/hydrology |
| **Geospatial grounding** | Hallucinations possible | Not applicable | ✓ Strictly validated |

---

## Technical Dependencies

```python
# Export service requirements
pip install gpxpy kml xml.etree.ElementTree geojson
```

**Libraries:**
- `gpxpy`: GPX file generation and parsing
- `fastkml`: KML generation
- `geojson`: GeoJSON validation
- Standard: `xml.etree.ElementTree` for XML manipulation

---

## Post-Integration Opportunities

### 1. Offline POI Search
- Include full-text search index in exported GeoJSON
- Organic Maps can index and search across all trails

### 2. Trail Conditions Reporting
- Users report trail conditions in Organic Maps
- Sync back to Cartograph (validated, community-sourced)

### 3. Wildlife Observation Integration
- Export routes compatible with iNaturalist observations
- Contribute observations to scientific datasets

### 4. Seasonal Trail Updates
- Sync seasonal closures/restrictions from Parks Canada
- Push to Organic Maps bookmarks as "status updates"

### 5. Multi-Platform Route Sync
- Cloud sync of routes (optional, privacy-respecting)
- Share routes via immutable links (no user tracking)

---

## Implementation Timeline

```
Current: Phase 5 (AI Enrichment) ✓
↓
Phase 6: User Authentication (2 weeks)
↓
Phase 6.5: Advanced Search & Discovery (1 week)
↓
Phase 7: Organic Maps Integration (3 weeks)
  ├─ Week 1: Route exports (GPX/KML)
  ├─ Week 2: POI layer exports
  └─ Week 3: Enrichment sync + testing
↓
Phase 8: Mobile Native App (Organic Maps fork / custom React Native)
```

---

## Success Criteria

- [ ] Users can export any route as GPX/KML in <2 clicks
- [ ] Exported routes navigate correctly in Organic Maps
- [ ] All 53 trails available as downloadable custom map layer
- [ ] Stewardship tips appear in Organic Maps bookmark details
- [ ] Conservation sensitivity visible via icon colors
- [ ] Zero hallucinated POIs in exports (validation passes)
- [ ] Export + import cycle preserves all metadata
- [ ] Works offline in Organic Maps without internet
- [ ] Documentation helps users discover Organic Maps integration
- [ ] Analytics show >10% of routes exported for offline use within 1 month

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Organic Maps API changes | Export format breaks | Version GPX/KML outputs, monitor releases |
| Large POI layer performance | Slow import in Organic Maps | Implement filtering (difficulty, dog-friendly), compress GeoJSON |
| User confusion on sync | Data loss if overwritten | Clear UI: "Download for offline use • No sync" |
| Licensing disputes | Legal issues | Document CC-BY-4.0, attribute all sources |
| Offline data staleness | Outdated trail info | Include export date, recommend quarterly updates |

---

## References

- Organic Maps GitHub: https://github.com/organicmaps/organicmaps
- GPX 1.1 Specification: https://www.topografix.com/gpx.asp
- GeoJSON RFC: https://www.rfc-editor.org/rfc/rfc7946
- OSM Data: https://www.openstreetmap.org/
- Cartograph Plan: `/root/.claude/plans/i-want-to-prototype-snuggly-anchor.md`
