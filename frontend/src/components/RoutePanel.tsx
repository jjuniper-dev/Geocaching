import { useState } from 'react'

export interface RouteFilters {
  dogFriendly: boolean
  eBikeFriendly: boolean
  maxDifficulty: 'easy' | 'moderate' | 'hard'
  avoidSensitiveAreas: boolean
}

export interface POIHighlight {
  poi_id: string
  name: string
  context: string
  ecology?: string
  conservation?: string
}

export interface RouteEnrichment {
  narrative: string
  highlights: POIHighlight[]
  environmental_education: string[]
  stewardship_tips: string[]
}

interface RoutePanelProps {
  onGenerate: (
    start: [number, number],
    end: [number, number],
    filters: RouteFilters
  ) => Promise<void>
  loading: boolean
  narrative: string | null
  conservationImpact?: string | null
  enrichment?: RouteEnrichment | null
  onClose: () => void
}

export default function RoutePanel({
  onGenerate,
  loading,
  narrative,
  conservationImpact,
  enrichment,
  onClose,
}: RoutePanelProps) {
  const [startLat, setStartLat] = useState('45.497')
  const [startLng, setStartLng] = useState('-75.855')
  const [endLat, setEndLat] = useState('45.489')
  const [endLng, setEndLng] = useState('-75.922')
  const [dogFriendly, setDogFriendly] = useState(false)
  const [eBikeFriendly, setEBikeFriendly] = useState(false)
  const [maxDifficulty, setMaxDifficulty] = useState<'easy' | 'moderate' | 'hard'>('hard')
  const [avoidSensitiveAreas, setAvoidSensitiveAreas] = useState(true)

  const handleGenerate = async () => {
    await onGenerate(
      [parseFloat(startLat), parseFloat(startLng)],
      [parseFloat(endLat), parseFloat(endLng)],
      { dogFriendly, eBikeFriendly, maxDifficulty, avoidSensitiveAreas }
    )
  }

  if (narrative) {
    return (
      <div className="route-panel route-panel--result">
        <button className="route-panel__close" onClick={onClose}>
          ← Back
        </button>
        {conservationImpact && (
          <div className="route-panel__conservation">
            <h4>🌿 Conservation Impact</h4>
            <p>{conservationImpact}</p>
          </div>
        )}
        <div className="route-panel__narrative">
          <h3>📍 Route Overview</h3>
          <p>{narrative}</p>
        </div>

        {enrichment && (
          <div className="route-panel__enrichment">
            {enrichment.highlights && enrichment.highlights.length > 0 && (
              <div className="route-panel__section">
                <h4>⭐ Highlights Along the Way</h4>
                {enrichment.highlights.map((highlight) => (
                  <div key={highlight.poi_id} className="route-panel__highlight">
                    <h5>{highlight.name}</h5>
                    <p className="route-panel__highlight-context">{highlight.context}</p>
                    {highlight.ecology && (
                      <p className="route-panel__highlight-ecology">
                        <strong>Ecology:</strong> {highlight.ecology}
                      </p>
                    )}
                    {highlight.conservation && (
                      <p className="route-panel__highlight-conservation">
                        <strong>Conservation:</strong> {highlight.conservation}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}

            {enrichment.environmental_education &&
              enrichment.environmental_education.length > 0 && (
                <div className="route-panel__section">
                  <h4>🔬 Environmental Context</h4>
                  <ul className="route-panel__education-list">
                    {enrichment.environmental_education.map((edu, idx) => (
                      <li key={idx}>{edu}</li>
                    ))}
                  </ul>
                </div>
              )}

            {enrichment.stewardship_tips &&
              enrichment.stewardship_tips.length > 0 && (
                <div className="route-panel__section">
                  <h4>♻️ Stewardship Tips</h4>
                  <ul className="route-panel__stewardship-list">
                    {enrichment.stewardship_tips.map((tip, idx) => (
                      <li key={idx}>{tip}</li>
                    ))}
                  </ul>
                </div>
              )}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="route-panel">
      <button className="route-panel__close" onClick={onClose}>
        ← Back
      </button>

      <div className="route-panel__form">
        <h3>Generate a Route</h3>

        <div className="route-panel__section">
          <label>Start Location</label>
          <div className="route-panel__coords">
            <input
              type="number"
              placeholder="Latitude"
              value={startLat}
              onChange={(e) => setStartLat(e.target.value)}
              step="0.001"
            />
            <input
              type="number"
              placeholder="Longitude"
              value={startLng}
              onChange={(e) => setStartLng(e.target.value)}
              step="0.001"
            />
          </div>
          <small>Click on the map to auto-fill</small>
        </div>

        <div className="route-panel__section">
          <label>End Location</label>
          <div className="route-panel__coords">
            <input
              type="number"
              placeholder="Latitude"
              value={endLat}
              onChange={(e) => setEndLat(e.target.value)}
              step="0.001"
            />
            <input
              type="number"
              placeholder="Longitude"
              value={endLng}
              onChange={(e) => setEndLng(e.target.value)}
              step="0.001"
            />
          </div>
        </div>

        <div className="route-panel__section">
          <label style={{ marginBottom: '8px', display: 'block' }}>Trail Filters</label>
          <div className="route-panel__checkbox">
            <input
              type="checkbox"
              id="dogFriendly"
              checked={dogFriendly}
              onChange={(e) => setDogFriendly(e.target.checked)}
            />
            <label htmlFor="dogFriendly" style={{ marginBottom: 0 }}>🐕 Dog-friendly trails</label>
          </div>
          <div className="route-panel__checkbox">
            <input
              type="checkbox"
              id="eBikeFriendly"
              checked={eBikeFriendly}
              onChange={(e) => setEBikeFriendly(e.target.checked)}
            />
            <label htmlFor="eBikeFriendly" style={{ marginBottom: 0 }}>🚴 E-bike friendly</label>
          </div>
        </div>

        <div className="route-panel__section">
          <label>Max Difficulty</label>
          <select
            value={maxDifficulty}
            onChange={(e) => setMaxDifficulty(e.target.value as 'easy' | 'moderate' | 'hard')}
          >
            <option value="easy">Easy</option>
            <option value="moderate">Moderate</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <div className="route-panel__section">
          <div className="route-panel__checkbox">
            <input
              type="checkbox"
              id="avoidSensitive"
              checked={avoidSensitiveAreas}
              onChange={(e) => setAvoidSensitiveAreas(e.target.checked)}
            />
            <label htmlFor="avoidSensitive" style={{ marginBottom: 0 }}>🌿 Avoid sensitive habitats (soft)</label>
          </div>
          <small>Route will prefer conservation-friendly paths</small>
        </div>

        <button
          className="route-panel__generate"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Route'}
        </button>

        <p className="route-panel__hint">
          💡 Tip: Click on POIs to use them as start/end points
        </p>
      </div>
    </div>
  )
}
