from rapidfuzz import fuzz
from .models import Strain, SearchResult
from .data import get_all_strains


def search_strains(query: str, limit: int = 15) -> list[SearchResult]:
    """
    Simple single-strategy fuzzy match for now (name + brand combined).
    This is where your four-strategy waterfall (exact -> fuzzy -> phonetic
    -> AI-assisted) plugs in later — start here, add strategies as misses
    show up in your miss-tracking table.
    """
    query = query.strip()
    if not query:
        return []

    scored: list[tuple[float, Strain]] = []
    for strain in get_all_strains():
        haystack = f"{strain.name} {strain.brand}"
        score = fuzz.WRatio(query, haystack)
        # also check name-only and brand-only so "wedding cake" and
        # "cannaco" both score well even when combined string dilutes it
        score = max(score, fuzz.WRatio(query, strain.name), fuzz.WRatio(query, strain.brand))
        if score >= 60:
            scored.append((score, strain))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    return [
        SearchResult(
            id=s.id,
            name=s.name,
            brand=s.brand,
            strain_type=s.strain_type,
            match_score=round(score, 1),
        )
        for score, s in scored[:limit]
    ]