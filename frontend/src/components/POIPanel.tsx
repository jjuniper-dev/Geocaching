import type { POI } from '../types/geospatial'
import { POI_TYPE_COLORS, POI_TYPE_LABELS } from '../types/geospatial'

interface POIPanelProps {
  poi: POI | null
}

export default function POIPanel({ poi }: POIPanelProps) {
  if (!poi) {
    return (
      <div className="poi-panel poi-panel--empty">
        <div className="poi-panel__placeholder">
          <div className="poi-panel__compass">⊕</div>
          <p>Click a location on the map to discover it</p>
        </div>
        <div className="poi-panel__legend">
          <h4>Layers</h4>
          <ul>
            {Object.entries(POI_TYPE_COLORS).map(([type, color]) => (
              <li key={type}>
                <span className="legend-dot" style={{ background: color }} />
                {POI_TYPE_LABELS[type as keyof typeof POI_TYPE_LABELS]}
              </li>
            ))}
          </ul>
        </div>
      </div>
    )
  }

  const color = POI_TYPE_COLORS[poi.type]
  const label = POI_TYPE_LABELS[poi.type]
  const [lat, lng] = poi.coordinates

  return (
    <div className="poi-panel">
      <div className="poi-panel__type-bar" style={{ background: color }} />
      <div className="poi-panel__content">
        <span className="poi-badge" style={{ background: color }}>
          {label}
        </span>
        <h2 className="poi-panel__name">{poi.name}</h2>
        <p className="poi-panel__description">{poi.description}</p>

        {poi.conservation && (
          <div className="poi-panel__conservation">
            <span className="poi-panel__conservation-icon">🌿</span>
            <p>{poi.conservation}</p>
          </div>
        )}

        {poi.season && (
          <div className="poi-panel__meta">
            <span>📅</span>
            <p>{poi.season}</p>
          </div>
        )}

        <div className="poi-panel__coords">
          {lat.toFixed(5)}, {lng.toFixed(5)}
          {poi.source && <span className="poi-panel__source"> · {poi.source}</span>}
        </div>
      </div>
    </div>
  )
}
