export interface SearchResult {
  id: string;
  name: string;
  brand: string;
  strain_type: string | null;
  match_score: number;
}

export interface EffectsResponse {
  strain_id: string;
  name: string;
  brand: string;
  likely_effects: string[];
  confidence: "high" | "medium" | "low";
  reasoning: string;
  sources_used: string[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8811";

export async function searchStrains(query: string): Promise<SearchResult[]> {
  const res = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error(`Search failed: ${res.status}`);
  return res.json();
}

export async function getEffects(strainId: string): Promise<EffectsResponse> {
  const res = await fetch(`${API_BASE}/api/strain/${strainId}/effects`);
  if (!res.ok) throw new Error(`Effects lookup failed: ${res.status}`);
  return res.json();
}
