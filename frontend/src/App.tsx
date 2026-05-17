import { useState } from 'react'
import Map from './components/Map'
import POIPanel from './components/POIPanel'
import type { POI } from './types/geospatial'
import pois from './data/pois'
import './App.css'

export default function App() {
  const [selectedPOI, setSelectedPOI] = useState<POI | null>(null)

  return (
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <span className="header__icon">⊕</span>
          <span className="header__title">Snuggly Anchor</span>
          <span className="header__sub">Chelsea · Gatineau Park</span>
        </div>
        <div className="header__count">{pois.length} locations</div>
      </header>
      <div className="main">
        <aside className="sidebar">
          <POIPanel poi={selectedPOI} />
        </aside>
        <div className="map-wrapper">
          <Map
            pois={pois}
            selectedPOI={selectedPOI}
            onSelectPOI={setSelectedPOI}
          />
        </div>
      </div>
    </div>
  )
}
