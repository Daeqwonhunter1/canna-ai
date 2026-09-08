from .models import Strain, Company, CoaData, AnecdotalSnippet

# This is a stand-in for your ~10k-row Postgres table. Same shape, just in
# memory so the API runs with zero setup. Swap `get_all_strains()` for a
# real DB query later — nothing else in main.py/search.py needs to change.

STRAINS: list[Strain] = [
    Strain(
        id="1",
        name="Blue Dream",
        brand="Cannaco",
        company=Company(name="Cannaco", state="CA", reputation_notes="consistent COAs, mid-tier pricing"),
        strain_type="hybrid",
        coa=CoaData(
            thc_pct=21.4,
            cbd_pct=0.1,
            terpenes={"myrcene": 0.62, "pinene": 0.31, "caryophyllene": 0.28},
            lab_name="SC Labs",
            test_date="2026-05-10",
        ),
        anecdotes=[
            AnecdotalSnippet(source="reddit", text="Good daytime strain, uplifting but not jittery", sentiment="positive"),
            AnecdotalSnippet(source="reddit", text="Helped with focus, mild body relaxation", sentiment="positive"),
        ],
    ),
    Strain(
        id="2",
        name="Blue Dream",
        brand="GreenPeak",
        company=Company(name="GreenPeak", state="CA", reputation_notes="premium pricing, small batch"),
        strain_type="hybrid",
        coa=CoaData(
            thc_pct=24.8,
            cbd_pct=0.05,
            terpenes={"myrcene": 0.9, "pinene": 0.2, "limonene": 0.35},
            lab_name="Confidence Analytics",
            test_date="2026-06-01",
        ),
        anecdotes=[
            AnecdotalSnippet(source="reddit", text="Hits harder than other Blue Dreams I've had, more sedating", sentiment="mixed"),
        ],
    ),
    Strain(
        id="3",
        name="Wedding Cake",
        brand="Cannaco",
        company=Company(name="Cannaco", state="CA", reputation_notes="consistent COAs, mid-tier pricing"),
        strain_type="indica",
        coa=CoaData(
            thc_pct=26.1,
            cbd_pct=0.08,
            terpenes={"limonene": 0.5, "caryophyllene": 0.45, "linalool": 0.2},
            lab_name="SC Labs",
            test_date="2026-04-22",
        ),
        anecdotes=[
            AnecdotalSnippet(source="reddit", text="Heavy relaxation, good for night, munchies are real", sentiment="positive"),
        ],
    ),
]


def get_all_strains() -> list[Strain]:
    return STRAINS


def get_strain_by_id(strain_id: str) -> Strain | None:
    return next((s for s in STRAINS if s.id == strain_id), None)