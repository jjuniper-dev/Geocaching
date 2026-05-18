const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "cartograph_token";

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem(TOKEN_KEY);
  return {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };
}

export interface POIHighlight {
  poi_id: string;
  name: string;
  context: string;
  ecology?: string;
  conservation?: string;
}

export interface RouteEnrichment {
  narrative: string;
  highlights: POIHighlight[];
  environmental_education: string[];
  stewardship_tips: string[];
}

export interface RouteEnrichmentRequest {
  route: Record<string, any>;
  nearby_poi_ids: string[];
  conservation_impact?: Record<string, any>;
}

export const apiClient = {
  async enrichRoute(request: RouteEnrichmentRequest): Promise<RouteEnrichment> {
    const response = await fetch(`${API_BASE}/api/ai/enrich-route`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      throw new Error(`Failed to enrich route: ${response.statusText}`);
    }
    return response.json();
  },

  async generateRoute(params: Record<string, any>) {
    const response = await fetch(`${API_BASE}/api/routes/generate`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(params),
    });
    if (!response.ok) {
      throw new Error(`Failed to generate route: ${response.statusText}`);
    }
    return response.json();
  },

  async getPOIs(bounds?: Record<string, number>) {
    const query = new URLSearchParams();
    if (bounds) {
      query.append(
        "bounds",
        `${bounds.minLat},${bounds.minLng},${bounds.maxLat},${bounds.maxLng}`
      );
    }
    const response = await fetch(`${API_BASE}/api/pois?${query}`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch POIs");
    return response.json();
  },

  async graphQL(query: string, variables?: Record<string, any>) {
    const response = await fetch(`${API_BASE}/graphql`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ query, variables }),
    });
    if (!response.ok) throw new Error("GraphQL request failed");
    return response.json();
  },

  async saveRoute(routeData: Record<string, any>) {
    const response = await fetch(`${API_BASE}/api/user/routes`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(routeData),
    });
    if (!response.ok) throw new Error("Failed to save route");
    return response.json();
  },

  async getSavedRoutes() {
    const response = await fetch(`${API_BASE}/api/user/routes`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch saved routes");
    return response.json();
  },
};
