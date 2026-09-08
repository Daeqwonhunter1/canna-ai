"use client";

import { useState } from "react";
import { SearchResult, searchStrains } from "@/lib/api";
import StrainCard from "./StrainCard";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [errored, setErrored] = useState(false);

  async function runSearch() {
    const q = query.trim();
    if (!q) return;
    setLoading(true);
    setErrored(false);
    try {
      const data = await searchStrains(q);
      setResults(data);
    } catch {
      setErrored(true);
      setResults(null);
    } finally {
      setLoading(false);
    }
  }

  // group by strain name so "Blue Dream" from two brands sits together
  const groups: Record<string, SearchResult[]> = {};
  (results ?? []).forEach((r) => {
    groups[r.name] = groups[r.name] ?? [];
    groups[r.name].push(r);
  });

  return (
    <div>
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runSearch()}
          placeholder="e.g. Blue Dream, or Cannaco"
          autoComplete="off"
          className="flex-1 rounded-card border border-border bg-panel px-4 py-3.5 text-text placeholder:text-muted outline-none focus:border-accent-dim"
        />
        <button
          onClick={runSearch}
          disabled={loading}
          className="rounded-card bg-accent px-[22px] font-semibold text-[#14200f] hover:bg-[#d6ae57] disabled:opacity-50"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-muted text-center mt-10 text-sm">Searching…</p>}

      {errored && (
        <p className="text-muted text-center mt-10 text-sm">
          Couldn&apos;t reach the backend. Is it running at{" "}
          {process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8811"}?
        </p>
      )}

      {!loading && !errored && results && results.length === 0 && (
        <p className="text-muted text-center mt-10 text-sm">No matches. Try a different spelling.</p>
      )}

      {!loading &&
        Object.entries(groups).map(([name, variants]) => (
          <div key={name} className="mt-8">
            <div className="text-muted text-xs uppercase tracking-widest mb-2.5">
              {variants.length > 1 ? `${name} — ${variants.length} brands` : name}
            </div>
            {variants.map((v) => (
              <StrainCard key={v.id} strain={v} />
            ))}
          </div>
        ))}
    </div>
  );
}
