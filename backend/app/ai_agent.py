"""
Effects synthesis agent.

Takes one Strain (COA + company + anecdotes) and returns a plain-language
effects summary. Two modes:

- LLM mode: builds a grounded prompt and calls out to your model of choice
  (Ollama/LangChain, per your stack). Plug in `call_llm()` below.
- Fallback mode: if no LLM is wired up (or the call fails), falls back to a
  deterministic terpene-based heuristic so the endpoint always returns
  something usable instead of erroring.

Keeping both means the API works today with zero LLM setup, and upgrades
cleanly once you wire in Ollama.
"""

from .models import Strain, EffectsResponse

# Rough, widely-cited terpene -> effect associations. Not medical claims —
# just priors to ground the heuristic fallback and to steer the LLM prompt.
TERPENE_EFFECTS = {
    "myrcene": ["relaxing", "sedating", "body-heavy"],
    "limonene": ["uplifting", "mood-boosting", "stress-relief"],
    "pinene": ["alertness", "focus", "counteracts anxiety"],
    "caryophyllene": ["calming", "anti-inflammatory feel", "mellow"],
    "linalool": ["calming", "sleep-supportive", "anxiety-reducing"],
    "humulene": ["appetite-suppressing", "mellow"],
    "terpinolene": ["uplifting", "creative", "light"],
}


def build_prompt(strain: Strain) -> str:
    coa = strain.coa
    terp_lines = ", ".join(f"{name} {pct}%" for name, pct in coa.terpenes.items()) or "no terpene data"
    anecdote_lines = "\n".join(f"- ({a.source}, {a.sentiment}): {a.text}" for a in strain.anecdotes) or "none available"

    return f"""You are helping a cannabis consumer pick between similar strains.

Strain: {strain.name}
Brand: {strain.brand} ({strain.company.state or "unknown state"})
Type: {strain.strain_type or "unknown"}
THC: {coa.thc_pct if coa.thc_pct is not None else "unknown"}%
CBD: {coa.cbd_pct if coa.cbd_pct is not None else "unknown"}%
Terpenes: {terp_lines}

Anecdotal reports:
{anecdote_lines}

Based ONLY on the above, list the 3-5 most likely effects, note your
confidence (high/medium/low depending on how much data is present), and
give a one-sentence reason. Do not invent lab data or reports that weren't
given to you."""


def call_llm(prompt: str) -> str | None:
    """
    Wire this up to Ollama / LangChain / whatever you're running.
    Return None on failure so the caller falls back gracefully.

    Example (Ollama, once you have it running locally):

        import ollama
        resp = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
        return resp["message"]["content"]
    """
    return None  # not wired up yet — falls through to heuristic


def heuristic_effects(strain: Strain) -> EffectsResponse:
    """Deterministic fallback: derive effects from terpene profile + anecdotes."""
    sources_used = []
    effect_votes: dict[str, int] = {}

    if strain.coa.terpenes:
        sources_used.append("COA terpene data")
        for terp_name, pct in strain.coa.terpenes.items():
            for effect in TERPENE_EFFECTS.get(terp_name.lower(), []):
                effect_votes[effect] = effect_votes.get(effect, 0) + pct

    if strain.anecdotes:
        sources_used.append(f"{len(strain.anecdotes)} anecdotal report(s)")
        for a in strain.anecdotes:
            if a.sentiment == "positive":
                effect_votes["generally well-liked"] = effect_votes.get("generally well-liked", 0) + 1

    ranked = sorted(effect_votes.items(), key=lambda kv: kv[1], reverse=True)
    likely_effects = [name for name, _ in ranked[:5]] or ["not enough data to estimate effects"]

    if strain.coa.terpenes and strain.anecdotes:
        confidence = "medium"
    elif strain.coa.terpenes or strain.anecdotes:
        confidence = "low"
    else:
        confidence = "low"

    reasoning = (
        f"Derived from terpene profile ({', '.join(strain.coa.terpenes) or 'none'}) "
        f"and {len(strain.anecdotes)} anecdotal report(s)."
    )

    return EffectsResponse(
        strain_id=strain.id,
        name=strain.name,
        brand=strain.brand,
        likely_effects=likely_effects,
        confidence=confidence,
        reasoning=reasoning,
        sources_used=sources_used or ["none — no COA or anecdotal data on file"],
    )


def get_effects(strain: Strain) -> EffectsResponse:
    prompt = build_prompt(strain)
    llm_output = call_llm(prompt)

    if llm_output is None:
        return heuristic_effects(strain)

    # TODO once call_llm is wired up: parse llm_output into EffectsResponse
    # (ask the model for JSON, or parse structured text) instead of raw string.
    return heuristic_effects(strain)