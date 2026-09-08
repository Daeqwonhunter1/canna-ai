from pydantic import BaseModel
from datetime import datetime


class ScrapedProfile(BaseModel):
    """
       A strain's terpene/potency profile as reported by a public strain database
       (Leafly, etc). This is COMMUNITY-AGGREGATED / TYPICAL data, not a real lab
       Certificate of Analysis for a specific batch. Keep it in its own table,
       separate from CoaData — conflating the two would let the AI agent present
       a guess as a verified lab result.
       """

    strain_name: str
    strain_type: str | None = None

    thc_pct_typical: float | None = None
    cbd_pct_typical: float | None = None

    terpenes: list[str] = []
    top_effects: list[str] = []
    top_flavors: list[str] = []

    description: str | None = None

    brand: str | None = None
    source_name: str
    source_url: str
