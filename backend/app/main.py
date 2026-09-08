from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import SearchResult, EffectsResponse
from .search import search_strains
from .data import get_strain_by_id
from .ai_agent import get_effects

app = FastAPI(title="Canna-AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before deploying
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/search", response_model=list[SearchResult])
def search(q: str):
    """Fuzzy search by strain name and/or brand name."""
    return search_strains(q)


@app.get("/api/strain/{strain_id}/effects", response_model=EffectsResponse)
def effects(strain_id: str):
    """Given a strain id, return likely effects synthesized from COA + anecdotal data."""
    strain = get_strain_by_id(strain_id)
    if strain is None:
        raise HTTPException(status_code=404, detail="Strain not found")
    return get_effects(strain)


@app.get("/api/health")
def health():
    return {"status": "ok"}
