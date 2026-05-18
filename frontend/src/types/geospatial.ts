export type POIType = 'scenic' | 'historical' | 'food' | 'trail' | 'wildlife' | 'cultural'
export type Difficulty = 'easy' | 'moderate' | 'hard'
export type ConservationSensitivity = 'low' | 'medium' | 'high'

export interface TrailCapabilities {
  dogFriendly: boolean
  eBikeFriendly: boolean
  difficulty: Difficulty
  lengthKm?: number
  wheelchairAccessible?: boolean
}

export interface POI {
  id: string
  name: string
  type: POIType
  coordinates: [number, number] // [lat, lng]
  description: string
  conservation?: string
  season?: string
  source?: string
  trailCapabilities?: TrailCapabilities
  conservationSensitivity?: ConservationSensitivity
}

export const POI_TYPE_LABELS: Record<POIType, string> = {
  scenic: 'Scenic',
  historical: 'Historical',
  food: 'Food & Drink',
  trail: 'Trail',
  wildlife: 'Wildlife',
  cultural: 'Cultural',
}

export const POI_TYPE_COLORS: Record<POIType, string> = {
  scenic: '#2e7d32',
  historical: '#b71c1c',
  food: '#e65100',
  trail: '#1565c0',
  wildlife: '#6a1b9a',
  cultural: '#4e342e',
}
