"use client";

import { useState } from "react";
import { SearchResult, EffectsResponse, getEffects } from "@/lib/api";

export default function StrainCard({ strain }: { strain: SearchResult }) {
  const [effects, setEffects] = useState<EffectsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  async function handleClick() {
    if (effects || loading) return;
    setLoading(true);
    setError(false);
    try {
      const data = await getEffects(strain.id);
      setEffects(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      onClick={handleClick}
      className="cursor-pointer rounded-card border border-border bg-panel px-[18px] py-4 mb-2.5 transition-colors hover:bg-panel-hover"
    >
      <div className="flex items-baseline justify-between">
        <span className="font-display text-[1.1rem] font-semibold">{strain.name}</span>
        <span className="text-accent text-sm">{strain.brand}</span>
      </div>
      <div className="text-muted text-xs mt-0.5">
        {strain.strain_type ?? ""} · match {strain.match_score}
      </div>

      <div className="mt-2.5 pt-2.5 border-t border-border text-[0.88rem] text-muted">
        {!effects && !loading && !error && "Tap to load likely effects"}
        {loading && "Loading effects…"}
        {error && "Couldn't load effects."}
        {effects && (
          <>
            <div className="flex flex-wrap gap-1.5">
              {effects.likely_effects.map((e) => (
                <span
                  key={e}
                  className="inline-block rounded-pill bg-tag text-tag-text px-2.5 py-[3px] text-[0.78rem]"
                >
                  {e}
                </span>
              ))}
            </div>
            <div className="text-accent text-xs mt-1.5">
              confidence: {effects.confidence} · {effects.sources_used.join(", ")}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
