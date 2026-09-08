"""
Loads scraped strain JSON into Postgres. No brand handling — one row per
strain name.

Usage:
    python -m app.ingest sample_data/my_strains.json
"""

import sys
import json
from pathlib import Path

from .db import engine, SessionLocal
from .db_models import Base, Strain


def init_db() -> None:
    Base.metadata.create_all(engine)


def ingest_profile(session, profile: dict) -> None:
    name = profile["strain_name"]
    strain = session.query(Strain).filter(Strain.name.ilike(name)).one_or_none()

    if strain is not None:
        print(f"  skip (already have {name})")
        return

    strain = Strain(
        name=name,
        strain_type=profile.get("strain_type"),
        thc_pct=profile.get("thc_pct_typical"),
        cbd_pct=profile.get("cbd_pct_typical"),
        terpenes=profile.get("terpenes", []),
        top_effects=profile.get("top_effects", []),
        top_flavors=profile.get("top_flavors", []),
        description=profile.get("description"),
        source_name=profile.get("source_name", "manual"),
        source_url=profile.get("source_url"),
    )
    session.add(strain)


def run(json_path: str) -> None:
    init_db()
    loaded = json.loads(Path(json_path).read_text())
    profiles = loaded if isinstance(loaded, list) else [loaded]

    session = SessionLocal()
    try:
        for profile in profiles:
            print(f"ingesting: {profile['strain_name']}")
            ingest_profile(session, profile)
        session.commit()
        print(f"\nDone. {len(profiles)} profile(s) processed.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.ingest <path-to-strains.json>")
        sys.exit(1)
    run(sys.argv[1])