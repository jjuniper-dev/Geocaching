import { MapContainer, TileLayer, Marker, useMap } from 'react-leaflet'
import L from 'leaflet'
import type { POI, POIType } from '../types/geospatial'
import { POI_TYPE_COLORS } from '../types/geospatial'

const CHELSEA_CENTER: [number, number] = [45.497, -75.855]
const DEFAULT_ZOOM = 12

function createMarkerIcon(type: POIType, selected: boolean) {
  const color = POI_TYPE_COLORS[type]
  const size = selected ? 18 : 13
  const border = selected ? '3px solid white' : '2px solid white'
  const shadow = selected
    ? '0 0 0 2px ' + color + ', 0 2px 6px rgba(0,0,0,0.5)'
    : '0 1px 4px rgba(0,0,0,0.35)'
  return L.divIcon({
    className: '',
    html: `<div style="width:${size}px;height:${size}px;border-radius:50%;background:${color};border:${border};box-shadow:${shadow};transition:all 0.15s ease"></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  })
}

function FlyToSelected({ poi }: { poi: POI | null }) {
  const map = useMap()
  if (poi) {
    map.flyTo(poi.coordinates, Math.max(map.getZoom(), 14), { duration: 0.8 })
  }
  return null
}

interface MapProps {
  pois: POI[]
  selectedPOI: POI | null
  onSelectPOI: (poi: POI) => void
}

export default function Map({ pois, selectedPOI, onSelectPOI }: MapProps) {
  return (
    <MapContainer
      center={CHELSEA_CENTER}
      zoom={DEFAULT_ZOOM}
      style={{ height: '100%', width: '100%' }}
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={19}
      />
      {pois.map((poi) => (
        <Marker
          key={poi.id}
          position={poi.coordinates}
          icon={createMarkerIcon(poi.type, selectedPOI?.id === poi.id)}
          eventHandlers={{ click: () => onSelectPOI(poi) }}
        />
      ))}
      <FlyToSelected poi={selectedPOI} />
    </MapContainer>
  )
}
