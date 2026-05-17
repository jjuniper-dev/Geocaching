import { useState } from 'react'

interface RoutePanelProps {
  onGenerate: (start: [number, number], end: [number, number]) => Promise<void>
  loading: boolean
  narrative: string | null
  onClose: () => void
}

export default function RoutePanel({
  onGenerate,
  loading,
  narrative,
  onClose,
}: RoutePanelProps) {
  const [startLat, setStartLat] = useState('45.497')
  const [startLng, setStartLng] = useState('-75.855')
  const [endLat, setEndLat] = useState('45.489')
  const [endLng, setEndLng] = useState('-75.922')

  const handleGenerate = async () => {
    await onGenerate(
      [parseFloat(startLat), parseFloat(startLng)],
      [parseFloat(endLat), parseFloat(endLng)]
    )
  }

  if (narrative) {
    return (
      <div className="route-panel route-panel--result">
        <button className="route-panel__close" onClick={onClose}>
          ← Back
        </button>
        <div className="route-panel__narrative">
          <h3>Route Narrative</h3>
          <p>{narrative}</p>
        </div>
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
