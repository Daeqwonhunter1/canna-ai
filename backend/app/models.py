from pydantic import BaseModel
from typing import Optional


class CoaData(BaseModel):
    """Certificate of Analysis data — the structured, verifiable stuff."""
    thc_pct: Optional[float] = None
    cbd_pct: Optional[float] = None
    # terpene name -> percentage
    terpenes: dict[str, float] = {}
    lab_name: Optional[str] = None
    test_date: Optional[str] = None


class Company(BaseModel):
    name: str
    state: Optional[str] = None
    reputation_notes: Optional[str] = None  # e.g. "known for consistent COAs"


class AnecdotalSnippet(BaseModel):
    source: str  # "reddit", "leafly", etc.
    text: str
    sentiment: Optional[str] = None  # "positive" | "negative" | "mixed"


class Strain(BaseModel):
    id: str
    name: str
    brand: str
    company: Company
    strain_type: Optional[str] = None  # indica/sativa/hybrid
    coa: CoaData = CoaData()
    anecdotes: list[AnecdotalSnippet] = []


class SearchResult(BaseModel):
    id: str
    name: str
    brand: str
    strain_type: Optional[str] = None
    match_score: float


class EffectsResponse(BaseModel):
    strain_id: str
    name: str
    brand: str
    likely_effects: list[str]
    confidence: str  # "high" | "medium" | "low" — based on how much data backs it
    reasoning: str
    sources_used: list[str]