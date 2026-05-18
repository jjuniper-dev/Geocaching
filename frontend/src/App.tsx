import { useState, useEffect } from 'react'
import Map from './components/Map'
import POIPanel from './components/POIPanel'
import RoutePanel, { type RouteFilters, type RouteEnrichment } from './components/RoutePanel'
import GraphView from './components/GraphView'
import type { POI } from './types/geospatial'
import pois from './data/pois'
import { apiClient } from './api/client'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [selectedPOI, setSelectedPOI] = useState<POI | null>(null)
  const [mode, setMode] = useState<'explore' | 'route' | 'graph'>('explore')
  const [route, setRoute] = useState<[number, number][] | null>(null)
  const [narrative, setNarrative] = useState<string | null>(null)
  const [conservationImpact, setConservationImpact] = useState<string | null>(null)
  const [enrichment, setEnrichment] = useState<RouteEnrichment | null>(null)
  const [loading, setLoading] = useState(false)
  const [visitedPois, setVisitedPois] = useState<Set<string>>(new Set())

  useEffect(() => {
    const saved = localStorage.getItem('visitedPois')
    if (saved) {
      setVisitedPois(new Set(JSON.parse(saved)))
    }
  }, [])

  const markPOIAsVisited = (poiId: string) => {
    setVisitedPois((prev) => {
      const updated = new Set(prev)
      updated.add(poiId)
      localStorage.setItem('visitedPois', JSON.stringify([...updated]))
      return updated
    })
  }

  const handleSelectPOI = (poi: POI) => {
    setSelectedPOI(poi)
    markPOIAsVisited(poi.id)
  }

  const handleGenerateRoute = async (
    start: [number, number],
    end: [number, number],
    filters: RouteFilters
  ) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/routes/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start, end, filters }),
      })
      if (!response.ok) throw new Error('Failed to generate route')
      const data = await response.json()
      setRoute(data.coordinates)
      setNarrative(data.narrative)
      setConservationImpact(data.conservationImpact || null)

      // Fetch AI enrichment
      try {
        const enrichmentData = await apiClient.enrichRoute({
          route: data.route || { coordinates: data.coordinates, properties: { distance_km: data.distance_km } },
          nearby_poi_ids: data.nearby_poi_ids || [],
          conservation_impact: data.conservationImpact ? { impact_score: data.conservationImpact } : undefined,
        })
        setEnrichment(enrichmentData)
      } catch (enrichErr) {
        console.warn('Enrichment failed (AI service may not be available):', enrichErr)
        // Continue without enrichment
      }
    } catch (err) {
      console.error('Route generation failed:', err)
      alert('Failed to generate route. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <span className="header__icon">⊕</span>
          <span className="header__title">Cartograph</span>
          <span className="header__sub">Chelsea · Gatineau Park</span>
        </div>
        <div className="header__controls">
          <button
            className={`header__mode ${mode === 'explore' ? 'active' : ''}`}
            onClick={() => {
              setMode('explore')
              setRoute(null)
              setNarrative(null)
              setEnrichment(null)
            }}
          >
            Explore
          </button>
          <button
            className={`header__mode ${mode === 'route' ? 'active' : ''}`}
            onClick={() => setMode('route')}
          >
            Route
          </button>
          <button
            className={`header__mode ${mode === 'graph' ? 'active' : ''}`}
            onClick={() => setMode('graph')}
          >
            Graph
          </button>
          <span className="header__count">{pois.length} locations</span>
        </div>
      </header>
      {mode === 'graph' ? (
        <GraphView pois={pois} visitedPois={visitedPois} onSelectPOI={handleSelectPOI} />
      ) : (
        <div className="main">
          <aside className="sidebar">
            {mode === 'explore' ? (
              <POIPanel poi={selectedPOI} />
            ) : (
              <RoutePanel
                onGenerate={handleGenerateRoute}
                loading={loading}
                narrative={narrative}
                conservationImpact={conservationImpact}
                enrichment={enrichment}
                onClose={() => {
                  setMode('explore')
                  setRoute(null)
                  setNarrative(null)
                  setConservationImpact(null)
                  setEnrichment(null)
                }}
              />
            )}
          </aside>
          <div className="map-wrapper">
            <Map
              pois={pois}
              selectedPOI={selectedPOI}
              onSelectPOI={handleSelectPOI}
              route={route}
            />
          </div>
        </div>
      )}
    </div>
  )
}
